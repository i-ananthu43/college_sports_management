# admin_panel/forms.py
from django import forms
from django.contrib.auth.models import User


class CoordinatorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Specify the fields to include in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the password field by default; will be used only if updating
        if self.instance.pk:  # Check if the instance already exists
            self.fields['password'].widget = forms.HiddenInput()

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:  # If a new password is provided
            user.set_password(password)  # Hash the password
        if commit:
            user.save()
        return user