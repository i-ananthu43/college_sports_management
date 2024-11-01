# core/models.py
from django.db import models
from django.contrib.auth.models import User

class CoreStudent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User model
    full_name = models.CharField(max_length=255)
    register_number = models.CharField(max_length=50, unique=True, default="")
    email = models.EmailField()
    course = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    year_of_study = models.IntegerField()
    is_approved = models.BooleanField(default=False)  # New field for approval status

    def __str__(self):
        return self.full_name
