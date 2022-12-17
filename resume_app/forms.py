"""
            ------------------------------------------------------------
            |                   Aknowledgement                         |
            |----------------------------------------------------------|
            |   Project Name : Resume Screening Using Machine Learning |
            |   Coded By : Eng. Karim Mohammed Aboelazm                |
            |   Organization : Obour University                        |
            |----------------------------------------------------------|
"""

from django import forms
from .models import *

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('resume',)

class HRLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        user_name = self.cleaned_data["username"]
        if User.objects.filter(username=user_name).exists():
           pass
        else:
            raise forms.ValidationError('HR with this username is not exists.')
        return user_name