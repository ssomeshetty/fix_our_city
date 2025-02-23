# contractor/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Contractor
from issues.models import Issue, ContractorAssignment

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
