# issues/forms.py
from django import forms
from .models import Issue, Comment, IssueImage

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'location', 'government_authority']

    # Add image field for issue image
    image = forms.ImageField(required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class IssueImageForm(forms.ModelForm):
    class Meta:
        model = IssueImage
        fields = ['image', 'caption']
