from django import template
from issues.models import UserRating
from django.utils.timesince import timesince
from datetime import datetime

register = template.Library()

@register.filter
def has_been_rated_by(issue, user):
    return UserRating.objects.filter(issue=issue, user=user).exists()

@register.filter(name='status_icon')
def status_icon(status):
    if not isinstance(status, str):
        return 'info-circle'
    icons = {
        'new': 'clock',
        'pending': 'hourglass-half',
        'in_progress': 'tools',
        'completed': 'check-circle',
        'rejected': 'times-circle'
    }
    return icons.get(status.lower(), 'info-circle')

@register.filter(name='status_color')
def status_color(status):
    if not isinstance(status, str):
        return 'secondary'
    colors = {
        'new': 'info',
        'pending': 'warning',
        'in_progress': 'primary',
        'completed': 'success',
        'rejected': 'danger'
    }
    return colors.get(status.lower(), 'secondary')

@register.filter(name='status_progress')
def status_progress(status):
    if not isinstance(status, str):
        return 0
    progress = {
        'new': 25,
        'pending': 50,
        'in_progress': 75,
        'completed': 100,
        'rejected': 0
    }
    return progress.get(status.lower(), 0)

@register.filter(name='status_description')
def status_description(status):
    if not isinstance(status, str):
        return 'Current status information is not available.'
    descriptions = {
        'new': 'This issue has been recently reported and is awaiting review.',
        'pending': 'The issue is being reviewed by our team for validation.',
        'in_progress': 'Work on resolving this issue is currently underway.',
        'completed': 'This issue has been successfully resolved!',
        'rejected': 'This issue has been reviewed and rejected as invalid.'
    }
    return descriptions.get(status.lower(), 'Current status information is not available.')

@register.filter(name='timesince')
def timesince_filter(value):
    if not value:
        return ''
    now = datetime.now()
    if value > now:
        return 'just now'
    return timesince(value, now) + ' ago'

from django.utils import timezone
from django.utils.timesince import timesince
from datetime import datetime

@register.filter(name='timesince')
def timesince_filter(value):
    """Custom timesince filter that handles future dates safely."""
    if not value:
        return ''

    now = timezone.now()  # Use timezone-aware datetime

    # Ensure the value is timezone-aware
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())

    if value > now:
        return 'just now'

    return timesince(value, now) + ' ago'


# Debug
print("Custom filters loaded.")
