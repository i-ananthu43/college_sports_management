from django.contrib import admin
from .models import House

class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'assigned_coordinator')
    search_fields = ('name',)

admin.site.register(House, HouseAdmin)

from .models import Achievement

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('student', 'achievement_type', 'date_achieved', 'result', 'created_at')
    search_fields = ('student__full_name', 'achievement_type', 'result__title')  # Assuming Result has a title field
    list_filter = ('achievement_type', 'date_achieved', 'result')