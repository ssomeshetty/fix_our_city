from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    is_admin = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    is_contractor = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    is_authority = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    is_users = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_admin', 'is_contractor', 'is_authority', 'is_users')

    def clean(self):
        cleaned_data = super().clean()
        roles = ['is_admin', 'is_contractor', 'is_authority', 'is_users']
        selected_roles = [role for role in roles if cleaned_data.get(role)]

        if len(selected_roles) > 1:
            raise forms.ValidationError("You can only select one role.")
        elif len(selected_roles) == 0:
            raise forms.ValidationError("You must select at least one role.")

        for role in roles:
            if role in selected_roles:
                cleaned_data[role] = True
            else:
                cleaned_data[role] = False

        return cleaned_data
