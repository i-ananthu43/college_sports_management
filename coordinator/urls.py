from django.urls import include, path
from . import views

urlpatterns = [
    path('dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('dashboard/manage_events/', views.manage_events, name='manage_events'),
    path('coordinator/details/', views.coordinator_details, name='coordinator_details'),
    path('coordinator/events/', views.view_events, name='view_events'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('view_events/', views.view_events, name='view_events'),
    path('coordinator/assigned_events/', views.view_assigned_events, name='view_assigned_events'),
    path('coordinator/approve_registration/<int:registration_id>/', views.approve_registration, name='approve_registration'),
 
]