# issues/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from public.models import User
from authorities.models import Authority
from contractor.models import Contractor

class Issue(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    upvotes_count = models.PositiveIntegerField(default=0)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')
    contractor = models.ForeignKey(Contractor, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_issues')
    government_authority = models.ForeignKey(Authority, on_delete=models.CASCADE, related_name='jurisdiction_issues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class ContractorAssignment(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='assignments')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='issue_assignments')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_issues')
    assigned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='assigned')
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

class IssueUpvote(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('issue', 'user')

class IssueImage(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='issue_images/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class UserRating(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='received_ratings')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

