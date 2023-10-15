from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserMangaList, Manga, UserProfile


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
    
class UserMangaForm(forms.ModelForm):
    class Meta:
        model = UserMangaList
        fields = ['user', 'manga', ]
        
class MangaForm(forms.ModelForm):
    class Meta:
        model = Manga
        fields = ['title', 'status', ]