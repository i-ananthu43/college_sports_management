from django.contrib import admin

from admin_panel.models import Coordinator, SportEvent

# Register your models here.
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Display user information in the list view
    search_fields = ('user__username', 'user__email')  # Enable searching by username or email

admin.site.register(Coordinator, CoordinatorAdmin)

@admin.register(SportEvent)
class SportEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'sport_type')
    search_fields = ('title', 'description', 'location', 'sport_type')