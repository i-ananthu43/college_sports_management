from django import forms

from core.models import CoreStudent
from admin_panel.models import SportEvent

class SportEventForm(forms.ModelForm):
    class Meta:
        model = SportEvent
        fields = '__all__'  # Include all fields or specify necessary ones

    def __init__(self, *args, **kwargs):
        self.coordinator_assigned = kwargs.pop('coordinator_assigned', False)
        super().__init__(*args, **kwargs)
        
        # If a coordinator is assigned, disable the coordinator field
        if self.coordinator_assigned:
            self.fields['coordinator'].disabled = True