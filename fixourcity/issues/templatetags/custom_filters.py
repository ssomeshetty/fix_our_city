from django import template
from issues.models import UserRating

register = template.Library()

@register.filter
def has_been_rated_by(issue, user):
    """
    Custom template filter to check if a user has rated the contractor for a given issue.
    """
    return UserRating.objects.filter(issue=issue, user=user).exists()
