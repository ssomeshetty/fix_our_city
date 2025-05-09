
# issues/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Issue, IssueUpvote, IssueImage, Comment
from .forms import IssueForm, CommentForm, IssueImageForm

@login_required
def create_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the issue object first
            issue = form.save(commit=False)
            issue.reported_by = request.user
            issue.save()

            # If the user uploaded an image, associate it with the issue
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

    return render(request, 'create_issue.html', {'form': form})

def view_issues(request):
    new_issues = Issue.objects.filter(upvotes_count__lt=50, status='new')
    pending_issues = Issue.objects.filter(status='pending')
    completed_issues = Issue.objects.filter(status='completed')
    
    context = {
        'new_issues': new_issues,
        'pending_issues': pending_issues,
        'completed_issues': completed_issues
    }
    return render(request, 'view_issues.html', context)

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
