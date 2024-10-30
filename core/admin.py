from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CoreStudent

@admin.register(CoreStudent)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'course', 'branch', 'phone_number', 'year_of_study')  # Remove 'username'
    
    # You can add other configurations like search_fields, list_filter, etc.
    

