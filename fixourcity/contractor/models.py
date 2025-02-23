# contractor/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from public.models import User
from authorities.models import Authority

class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contractor_profile')
    name = models.CharField(max_length=255)
    expertise = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, related_name='contractors')
    credit_score = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=1.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_completed_issues = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
