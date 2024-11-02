from django.db import models
from django.contrib.auth.models import User
from admin_panel.models import SportEvent
from core.models import CoreStudent



class ActivityPoint(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(SportEvent, on_delete=models.CASCADE)
    points = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.student.username} - {self.points} Points'
    
class EventRegistration(models.Model):
    full_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    event = models.ForeignKey(SportEvent, on_delete=models.CASCADE)
    student = models.ForeignKey(CoreStudent, on_delete=models.CASCADE,null=True)
    house = models.ForeignKey('coordinator.House', on_delete=models.CASCADE, default=1)  # Link to the House model
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"
