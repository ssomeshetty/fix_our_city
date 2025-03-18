# issues/forms.py
from django import forms
from .models import Issue, Comment, IssueImage, UserRating

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'location', 'government_authority']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class IssueImageForm(forms.ModelForm):
    class Meta:
        model = IssueImage
        fields = ['image', 'caption']

class UserRatingForm(forms.ModelForm):
    class Meta:
        model = UserRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(1, '1 - Poor'), 
                                               (2, '2 - Fair'), 
                                               (3, '3 - Good'),
                                               (4, '4 - Very Good'),
                                               (5, '5 - Excellent')]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your experience with this contractor'}),
        }