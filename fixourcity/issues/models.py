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
    
     
    # If you're using the is_nearby method in the Issue model, update that too:

    def is_nearby(self, user_lat, user_lng, max_distance=1):  # Changed from 10km to 1km
        """
        Check if the issue is within the specified distance from a given location
        Distance is calculated in kilometers using the Haversine formula
        """
        if self.latitude is None or self.longitude is None:
            return False
            
        import math
        
        # Radius of the Earth in km
        R = 6371
        
        # Convert coordinates to radians
        lat1_rad = math.radians(float(user_lat))
        lon1_rad = math.radians(float(user_lng))
        lat2_rad = math.radians(float(self.latitude))
        lon2_rad = math.radians(float(self.longitude))
        
        # Calculate differences
        dLat = lat2_rad - lat1_rad
        dLon = lon2_rad - lon1_rad
        
        # Haversine formula
        a = math.sin(dLat/2) * math.sin(dLat/2) + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * \
            math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance <= max_distance
    
    def distance_from(self, user_lat, user_lng):
        """
        Calculate the distance in kilometers from a given location
        """
        if self.latitude is None or self.longitude is None:
            return None
            
        import math
        
        # Radius of the Earth in km
        R = 6371
        
        # Convert coordinates to radians
        lat1_rad = math.radians(float(user_lat))
        lon1_rad = math.radians(float(user_lng))
        lat2_rad = math.radians(float(self.latitude))
        lon2_rad = math.radians(float(self.longitude))
        
        # Calculate differences
        dLat = lat2_rad - lat1_rad
        dLon = lon2_rad - lon1_rad
        
        # Haversine formula
        a = math.sin(dLat/2) * math.sin(dLat/2) + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * \
            math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return round(distance, 1)


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
    

# issues/models.py (add this to the end)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    related_issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"

    class Meta:
        ordering = ['-created_at']