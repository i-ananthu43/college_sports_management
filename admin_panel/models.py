from django.db import models
from django.contrib.auth.models import User

class Coordinator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=30, blank=True)  # Updated related_name

    def __str__(self):
        return self.user.username
    
class SportEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    sport_type = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class CoordinatorAssignedEvent(models.Model):
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    sport_event = models.ForeignKey(SportEvent, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('coordinator', 'sport_event')  # Ensure a coordinator can't be assigned the same event multiple times