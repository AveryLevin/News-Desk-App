from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    """Form definition for User."""

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    """Form definition for UserProfile."""

    class Meta:
        """Meta definition for UserProfileform."""

        model = UserProfile
        fields = ('sources_list', 'tags_list',)
