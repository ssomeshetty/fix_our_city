from django import forms
from .models import Issue, Comment, IssueImage, UserRating
import json

from authorities.models import Authority

class IssueForm(forms.ModelForm):
    # Make government_authority a ChoiceField with a more user-friendly display
    government_authority = forms.ModelChoiceField(
        queryset=Authority.objects.all(),
        required=False,  # Make it optional initially, as we'll try to auto-detect
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select an authority"
    )
    
    class Meta:
        model = Issue
        fields = ['title', 'description', 'government_authority', 'latitude', 'longitude', 'address']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief title of the issue'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Detailed description of the issue'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'address': forms.HiddenInput(),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure location data is provided
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        
        if not latitude or not longitude:
            self.add_error(None, "Please select a location on the map.")
            
        return cleaned_data

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