from django import forms


from coordinator.models import House
from .models import EventRegistration  # Assuming you have a model for registration

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['full_name', 'course', 'branch', 'house']  # Include house in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['house'].queryset = House.objects.all()  # Populate the house field with all houses