from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from public.models import User
from authorities.models import Authority
from contractor.models import Contractor
import json


class Issue(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    # Store the complete location data as JSON string
    location = models.TextField()
    # Extract these fields for easier querying
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=512, null=True, blank=True)
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    upvotes_count = models.PositiveIntegerField(default=0)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')
    contractor = models.ForeignKey('contractor.Contractor', null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_issues')
    government_authority = models.ForeignKey('authorities.Authority', on_delete=models.CASCADE, related_name='jurisdiction_issues')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.location:
            try:
                location_data = json.loads(self.location)
                self.latitude = location_data.get('latitude')
                self.longitude = location_data.get('longitude')

                address = location_data.get('address', {})
                self.address = ', '.join(filter(None, [
                    address.get('suburb') or address.get('neighbourhood'),
                    address.get('city'),
                    address.get('country')
                ]))
            except (ValueError, json.JSONDecodeError):
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


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
    
    def __str__(self):
        return f"{self.issue.title} - {self.contractor.name}"


class IssueUpvote(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_upvotes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('issue', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.issue.title}"


class IssueImage(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='issue_images/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.issue.title}"


class UserRating(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='received_ratings')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s rating for {self.contractor.name}"


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.issue.title}"