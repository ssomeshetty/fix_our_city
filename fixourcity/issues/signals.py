# issues/signals.py (create new file)
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Issue, UserRating, Notification
from django.utils.html import strip_tags

@receiver(post_save, sender=Comment)
def notify_new_comment(sender, instance, created, **kwargs):
    if created:
        issue = instance.issue
        message = f"New comment on issue '{issue.title}' by {instance.user.username}"
        
        # Collect users to notify
        users_to_notify = set()
        users_to_notify.add(issue.reported_by)  # Issue reporter
        if issue.contractor:  # Assigned contractor
            users_to_notify.add(issue.contractor.user)
        users_to_notify.add(issue.government_authority.user)  # Responsible authority
        
        # Remove comment author from recipients
        users_to_notify.discard(instance.user)
        
        # Create notifications
        for user in users_to_notify:
            Notification.objects.create(
                user=user,
                message=message,
                related_issue=issue
            )

@receiver(post_save, sender=UserRating)
def notify_new_rating(sender, instance, created, **kwargs):
    if created:
        message = f"New {instance.rating}-star rating from {instance.user.username}"
        Notification.objects.create(
            user=instance.contractor.user,
            message=message,
            related_issue=instance.issue
        )