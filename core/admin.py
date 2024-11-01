from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CoreStudent

class CoreStudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'is_approved')
    actions = ['approve_students']

    def approve_students(self, request, queryset):
        for student in queryset:
            student.is_approved = True
            student.save()
        self.message_user(request, "Selected students have been approved.")

    approve_students.short_description = "Approve selected students"

admin.site.register(CoreStudent, CoreStudentAdmin)

