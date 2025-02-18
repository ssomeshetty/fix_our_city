# authorities/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Authority
from issues.models import Issue
from contractor.models import Contractor
# authorities/views.py

def is_authority(user):
    return user.role == 'authority'

@login_required
@user_passes_test(is_authority)
def authority_dashboard(request):
    try:
        # Attempt to get the Authority object for the logged-in user
        authority = Authority.objects.get(user=request.user)
    except Authority.DoesNotExist:
        # If the Authority object doesn't exist, show an error and redirect
        messages.error(request, 'Your authority profile is not set up. Please complete your profile.')
        return redirect('profile')  # Redirect to profile page where they can complete their info
    
    # Fetch trending and pending issues related to this authority
    trending_issues = Issue.objects.filter(
        government_authority=authority,
        upvotes_count__gte=1,  # Only issues with at least 50 upvotes
        status='new'            # Filter by status 'new'
    )
    pending_issues = Issue.objects.filter(
        government_authority=authority,
        status='pending'        # Only pending issues
    )

    # Prepare context data to be passed to the template
    context = {
        'authority': authority,
        'trending_issues': trending_issues,
        'pending_issues': pending_issues
    }

    # Render the authority dashboard template
    return render(request, 'authority.html', context)

@login_required
@user_passes_test(is_authority)
def assign_contractor(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    authority = get_object_or_404(Authority, user=request.user)
    
    if request.method == 'POST':
        contractor_id = request.POST.get('contractor')
        contractor = get_object_or_404(Contractor, id=contractor_id)
        
        issue.contractor = contractor
        issue.status = 'pending'
        issue.save()
        
        messages.success(request, 'Contractor assigned successfully!')
        return redirect('authority_dashboard')
    
    available_contractors = Contractor.objects.filter(authority=authority, is_active=True)
    return render(request, 'assign_contractor.html', {
        'issue': issue,
        'contractors': available_contractors
    })

