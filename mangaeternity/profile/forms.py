from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Manga, UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email address", required=True,
        help_text="Required.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class MangaListForm(forms.Form):
    reading = forms.BooleanField(required=False)
    planned = forms.BooleanField(required=False)
    read = forms.BooleanField(required=False)