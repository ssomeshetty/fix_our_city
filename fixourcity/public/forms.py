# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'contact_info']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    contact_info = forms.CharField(max_length=255, required=False)
    profile_picture = forms.ImageField(required=False)
    location = forms.CharField(max_length=100,required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'contact_info', 'profile_picture']
