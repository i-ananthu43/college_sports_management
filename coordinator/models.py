from django.db import models
from django.contrib.auth.models import User
from admin_panel.models import Coordinator, SportEvent
from core.models import CoreStudent
from student.models import EventRegistration

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
    
class MatchFixture(models.Model):
    event = models.ForeignKey(SportEvent, on_delete=models.CASCADE)
    student_1 = models.ForeignKey(CoreStudent, related_name='match_student_1', on_delete=models.CASCADE)
    student_2 = models.ForeignKey(CoreStudent, related_name='match_student_2', on_delete=models.CASCADE, null=True)
    round_number = models.IntegerField()
    student_1_score = models.IntegerField(null=True, blank=True)  # For storing score of student 1
    student_2_score = models.IntegerField(null=True, blank=True)  # For storing score of student 2
    winner = models.ForeignKey(CoreStudent, related_name='winner_matches', on_delete=models.SET_NULL, null=True)
    is_finalized = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_1} vs {self.student_2} - Round {self.round_number}"
    
class Result(models.Model):
    sport_event = models.ForeignKey(SportEvent, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    first_prize = models.CharField(max_length=100)  # Use CharField for the winner's name or ID
    second_prize = models.CharField(max_length=100)  # Use CharField for runner-up's name or ID
    third_prize = models.CharField(max_length=100)  # Use CharField for third place's name or ID
    date = models.DateField(auto_now_add=True)

class Certificate(models.Model):
    event = models.ForeignKey(SportEvent, on_delete=models.CASCADE)
    student = models.ForeignKey(EventRegistration, on_delete=models.CASCADE)
    certificate_type = models.CharField(max_length=20, choices=[('winner', 'Winner'), ('participant', 'Participant')])
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    issue_date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='certificates/', null=True, blank=True)