# contractor/models.py
from django.db import models
from django.db.models import Avg
from public.models import User
from authorities.models import Authority

class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contractor_profile')
    name = models.CharField(max_length=255)
    expertise = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    credit_score = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, related_name='contractors')
    total_completed_issues = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_average_rating(self):
        """Calculate and return the average rating for this contractor"""
        from issues.models import UserRating
        result = UserRating.objects.filter(contractor=self).aggregate(Avg('rating'))
        return result['rating__avg'] or 0.0
    
    def get_total_ratings(self):
        """Return the total number of ratings received"""
        from issues.models import UserRating
        return UserRating.objects.filter(contractor=self).count()
    
    def get_rating_distribution(self):
        """Return the distribution of ratings (how many 1s, 2s, etc.)"""
        from issues.models import UserRating
        distribution = {}
        for i in range(1, 6):
            distribution[i] = UserRating.objects.filter(contractor=self, rating=i).count()
        return distribution
    
    def __str__(self):
        return self.name