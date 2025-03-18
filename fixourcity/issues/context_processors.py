# Create issues/context_processors.py

def issue_utils(request):
    """
    Add utility functions for issue templates
    """
    from issues.models import UserRating
    
    def has_been_rated_by(issue, user):
        if not user.is_authenticated:
            return False
        return UserRating.objects.filter(issue=issue, user=user).exists()
    
    return {
        'has_been_rated_by': has_been_rated_by
    }