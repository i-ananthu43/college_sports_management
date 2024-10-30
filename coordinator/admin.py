from django.contrib import admin
from .models import House

class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'assigned_coordinator')
    search_fields = ('name',)

admin.site.register(House, HouseAdmin)