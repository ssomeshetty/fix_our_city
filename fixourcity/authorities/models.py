# authorities/models.py
from django.db import models
from public.models import User

class Authority(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='authority_profile')
    name = models.CharField(max_length=255)
    description = models.TextField()
    jurisdiction = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Authorities"
