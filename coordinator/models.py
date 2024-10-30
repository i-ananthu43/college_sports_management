from django.db import models
from django.contrib.auth.models import User
from admin_panel.models import Coordinator, SportEvent
from core.models import CoreStudent

class EventReport(models.Model):
    event = models.ForeignKey(SportEvent, on_delete=models.CASCADE)
    report = models.TextField()
    coordinator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Report for {self.event.name} by {self.coordinator.username}'
# coordinator/models.py

class House(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    assigned_coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE, related_name='houses')

    def __str__(self):
        return self.name