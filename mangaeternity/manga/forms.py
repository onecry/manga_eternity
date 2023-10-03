from django import forms

class MangaTitleForm(forms.Form):
    title = forms.CharField(max_length=100)