# core/forms.py
from django import forms
from django.contrib.auth.models import User
from core.models import CoreStudent

class StudentSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = CoreStudent
        fields = ['full_name','register_number','email', 'course', 'branch', 'phone_number', 'year_of_study']