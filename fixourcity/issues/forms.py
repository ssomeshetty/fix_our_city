from django import forms
from .models import Issue, Comment, IssueImage, UserRating
import json


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'address', 'latitude', 'longitude', 'location','government_authority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter issue title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the issue in detail', 'rows': 4}),
            # Hidden fields that will be populated via JavaScript
            'address': forms.HiddenInput(),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'location': forms.HiddenInput(),
        }

        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add your comment here'})
        }


class IssueImageForm(forms.ModelForm):
    class Meta:
        model = IssueImage
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief description of the image'})
        }


class UserRatingForm(forms.ModelForm):
    class Meta:
        model = UserRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience with the contractor'})
        }