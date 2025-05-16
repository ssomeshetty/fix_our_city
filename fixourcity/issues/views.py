
# issues/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Issue, IssueUpvote, IssueImage, Comment
from .forms import IssueForm, CommentForm, IssueImageForm
from django.conf import settings  # Add this at the top with other imports

@login_required
def create_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reported_by = request.user
            issue.save()

            if 'image' in request.FILES:
                image = request.FILES['image']
                IssueImage.objects.create(
                    issue=issue,
                    image=image,
                    uploaded_by=request.user
                )
                
            messages.success(request, 'Issue reported successfully with image!')
            return redirect('issue_detail', issue_id=issue.id)
    else:
        form = IssueForm()

    return render(request, 'create_issue.html', {
        'form': form,
    })


from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import F, Q
from .models import Issue
import json
import math

def view_issues(request):
    # Default query parameters
    new_issues = Issue.objects.filter(status='new')
    pending_issues = Issue.objects.filter(status='pending')
    completed_issues = Issue.objects.filter(status='completed')
    
    # Handle location filtering via AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            lat = data.get('latitude')
            lng = data.get('longitude')
            max_distance = data.get('max_distance', 1)  # Default to 1 km
            
            if lat is not None and lng is not None:
                # Find issues within the specified radius
                issues_with_coords = Issue.objects.filter(
                    latitude__isnull=False,
                    longitude__isnull=False
                )
                
                # We'll filter in Python rather than SQL for geographic calculations
                # You might want to switch to PostGIS for better performance in production
                nearby_ids = []
                
                for issue in issues_with_coords:
                    distance = calculate_distance(
                        float(lat), float(lng),
                        issue.latitude, issue.longitude
                    )
                    if distance <= max_distance:
                        nearby_ids.append(issue.id)
                
                # Filter the querysets
                new_issues = new_issues.filter(id__in=nearby_ids)
                pending_issues = pending_issues.filter(id__in=nearby_ids)
                completed_issues = completed_issues.filter(id__in=nearby_ids)
                
                return JsonResponse({
                    'status': 'success',
                    'new_count': new_issues.count(),
                    'pending_count': pending_issues.count(),
                    'completed_count': completed_issues.count(),
                    'ids': nearby_ids
                })
            
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid coordinates'
            }, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON'
            }, status=400)
    
    # Regular page load
    context = {
        'new_issues': new_issues,
        'pending_issues': pending_issues,
        'completed_issues': completed_issues
    }
    return render(request, 'view_issues.html', context)

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Radius of the Earth in km
    
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    
    a = (
        math.sin(dLat/2) * math.sin(dLat/2) +
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
        math.sin(dLon/2) * math.sin(dLon/2)
    )
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return distance

@login_required
def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    images = issue.images.all()
    comments = issue.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.issue = issue
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('issue_detail', issue_id=issue.id)
    else:
        comment_form = CommentForm()
    
    context = {
        'issue': issue,
        'images': images,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'issue_detail.html', context)

@login_required
def upload_issue_image(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    
    if request.method == 'POST':
        form = IssueImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.issue = issue
            image.uploaded_by = request.user
            image.save()
            messages.success(request, 'Image uploaded successfully!')
            return redirect('issue_detail', issue_id=issue.id)
    else:
        form = IssueImageForm()
    
    return render(request, 'issue_images.html', {
        'form': form,
        'issue': issue
    })
@login_required
def upvote_issue(request, issue_id):
    if request.method == 'POST':
        issue = get_object_or_404(Issue, id=issue_id)
        
        # Toggle the upvote
        upvote, created = IssueUpvote.objects.get_or_create(
            issue=issue,
            user=request.user
        )
        
        if not created:
            # If the user already upvoted, remove the upvote
            upvote.delete()
            action = 'removed'
        else:
            # If the user hasn't upvoted, create the upvote
            action = 'added'
        
        # Manually update the upvotes_count field
        issue.upvotes_count = issue.upvotes.count()
        issue.save()  # Save the updated count to the database
        
        # Return a JSON response with updated upvotes count and action taken
        return JsonResponse({
            'action': action,
            'upvotes_count': issue.upvotes_count
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


# Updated home view in issues/views.py to include top contractors

from django.db.models import Avg, Count
from contractor.models import Contractor

@login_required
def home(request):
    user_issues = Issue.objects.filter(reported_by=request.user)
    trending_issues = Issue.objects.filter(upvotes_count__gte=50)
    recent_issues = Issue.objects.order_by('-created_at')[:10]
    
    # Get top contractors for the widget
    top_contractors = Contractor.objects.annotate(
        avg_rating=Avg('received_ratings__rating'),
        num_ratings=Count('received_ratings')
    ).filter(
        num_ratings__gt=0  # Only include contractors with at least one rating
    ).order_by('-avg_rating')[:5]  # Get top 5
    
    ranked_top_contractors = []
    for contractor in top_contractors:
        ranked_top_contractors.append({
            'contractor': contractor,
            'avg_rating': contractor.avg_rating,
            'num_ratings': contractor.num_ratings
        })
    
    context = {
        'user_issues': user_issues,
        'trending_issues': trending_issues,
        'recent_issues': recent_issues,
        'top_contractors': ranked_top_contractors
    }
    return render(request, 'home.html', context)

# issues/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Issue, UserRating
from .forms import UserRatingForm
from django.contrib import messages  # For displaying success/error messages

@login_required
def rate_contractor(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id, status='completed')
    contractor = issue.contractor
    
    if not contractor:
        # Handle case where issue doesn't have a contractor assigned
        messages.error(request, "This issue doesn't have a contractor assigned.")
        return redirect('issue_detail', issue_id=issue.id)
    
    # Check if the user has already rated this issue
    existing_rating = UserRating.objects.filter(user=request.user, issue=issue).first()
    
    if request.method == 'POST':
        # If rating exists, update it; otherwise create new
        if existing_rating:
            form = UserRatingForm(request.POST, instance=existing_rating)
        else:
            form = UserRatingForm(request.POST)
            
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.issue = issue
            rating.contractor = contractor
            rating.updated_at = timezone.now()
            rating.save()
            
            # Update the contractor's average rating in the background
            # This could be done with signals or a post-save hook
            
            messages.success(request, "Your rating has been submitted successfully.")
            return redirect('issue_detail', issue_id=issue.id)
    else:
        # Pre-populate form if rating exists
        if existing_rating:
            form = UserRatingForm(instance=existing_rating)
        else:
            form = UserRatingForm()

    return render(request, 'rate_contractor.html', {
        'issue': issue,
        'contractor': contractor,
        'form': form,
        'existing_rating': existing_rating,
    })

# issues/views.py

from django.shortcuts import get_object_or_404, redirect
from .models import Issue, Comment
from .forms import CommentForm
from django.contrib import messages

@login_required
def add_comment(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.issue = issue
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('issue_detail', issue_id=issue.id)
    else:
        comment_form = CommentForm()
    
    return redirect('issue_detail', issue_id=issue.id)
