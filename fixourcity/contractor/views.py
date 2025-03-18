# contractor/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Contractor
from issues.models import Issue, ContractorAssignment
from django.db import models  # <-- Add this import
from django.db.models import Avg, Count

def is_contractor(user):
    return user.role == 'contractor'

@login_required
@user_passes_test(is_contractor)
def contractor_dashboard(request):
    contractor = get_object_or_404(Contractor, user=request.user)
    assigned_issues = Issue.objects.filter(contractor=contractor).exclude(status='completed')
    completed_issues = Issue.objects.filter(contractor=contractor, status='completed')
    
    context = {
        'contractor': contractor,
        'assigned_issues': assigned_issues,
        'completed_issues': completed_issues
    }
    return render(request, 'contractor.html', context)

@login_required
@user_passes_test(is_contractor)
def update_issue_status(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id, contractor__user=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['in_progress', 'completed']:
            issue.status = new_status
            issue.save()
            
            if new_status == 'completed':
                contractor = issue.contractor
                contractor.total_completed_issues += 1
                contractor.save()
            
            messages.success(request, f'Issue status updated to {new_status}!')
        return redirect('contractor_dashboard')
    
    return render(request, 'contractor_assignments.html', {'issue': issue})


# contractor/views.py
from django.shortcuts import render
from django.db.models import Avg, Count
from .models import Contractor
from issues.models import UserRating
from contractor.models import Contractor  # <-- Ensure this import is present


def contractor_leaderboard(request):
    """
    Display a leaderboard of contractors ranked by their average ratings
    """
    # Get all contractors with their average ratings
    contractors = Contractor.objects.annotate(
        avg_rating=Avg('received_ratings__rating'),
        num_ratings=Count('received_ratings'),
        num_completed=Count('assigned_issues', filter=models.Q(assigned_issues__status='completed'))
    ).filter(
        num_ratings__gt=0  # Only include contractors with at least one rating
    ).order_by('-avg_rating', '-num_completed')
    
    # Create ranks (accounting for ties)
    ranked_contractors = []
    current_rank = 1
    previous_rating = None
    previous_completed = None
    
    for i, contractor in enumerate(contractors):
        # If this contractor has a different rating than the previous one, update the rank
        if previous_rating != contractor.avg_rating or previous_completed != contractor.num_completed:
            current_rank = i + 1
        
        # Calculate rating distribution percentage
        distribution = contractor.get_rating_distribution()
        total_ratings = sum(distribution.values())
        
        if total_ratings > 0:
            distribution_percentage = {
                star: (count / total_ratings) * 100 
                for star, count in distribution.items()
            }
        else:
            distribution_percentage = {star: 0 for star in range(1, 6)}
        
        ranked_contractors.append({
            'rank': current_rank,
            'contractor': contractor,
            'avg_rating': contractor.avg_rating,
            'num_ratings': contractor.num_ratings,
            'num_completed': contractor.num_completed,
            'distribution': distribution,
            'distribution_percentage': distribution_percentage
        })
        
        previous_rating = contractor.avg_rating
        previous_completed = contractor.num_completed
    
    return render(request, 'leaderboard.html', {
        'ranked_contractors': ranked_contractors
    })

def contractor_detail(request, contractor_id):
    """
    Display detailed information about a specific contractor
    """
    contractor = Contractor.objects.get(id=contractor_id)
    
    # Get the contractor's completed issues with ratings
    completed_issues = contractor.assigned_issues.filter(status='completed')
    ratings = UserRating.objects.filter(contractor=contractor).order_by('-created_at')
    
    # Rating distribution
    distribution = contractor.get_rating_distribution()
    total_ratings = sum(distribution.values())
    
    if total_ratings > 0:
        distribution_percentage = {
            star: (count / total_ratings) * 100 
            for star, count in distribution.items()
        }
    else:
        distribution_percentage = {star: 0 for star in range(1, 6)}
    
    context = {
        'contractor': contractor,
        'completed_issues': completed_issues,
        'ratings': ratings,
        'avg_rating': contractor.get_average_rating(),
        'total_ratings': total_ratings,
        'distribution': distribution,
        'distribution_percentage': distribution_percentage
    }
    
    return render(request, 'detail.html', context)