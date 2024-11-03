
from django.urls import include, path
from coordinator import views

urlpatterns = [
    path('dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('dashboard/manage_events/', views.manage_events, name='manage_events'),
    path('coordinator/details/', views.coordinator_details, name='coordinator_details'),
    path('coordinator/events/', views.view_events, name='view_events'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('view_events/', views.view_events, name='view_events'),
    path('assigned_events/', views.view_assigned_events, name='view_assigned_events'),
    path('approve_registration/<int:registration_id>/', views.approve_registration, name='approve_registration'),
   
    path('manage_events/', views.manage_events, name='manage_events'),  # Ensure this is defined
    path('event/<int:event_id>/fixture/', views.generate_fixture_view, name='match_fixture'),
    path('match/<int:match_id>/enter_score/', views.enter_score_view, name='enter_score'),
    path('select_winners/<int:event_id>/', views.select_winners, name='select_winners'),
    
    path('coordinator/view-results/', views.view_assigned_event_results, name='view_assigned_event_results'),
    path('generate_certificates/<int:event_id>/', views.generate_certificates_view, name='generate_certificates_view'),
    path('manage_certificates/', views.manage_certificates_view, name='manage_certificates'),
    path('report/<int:event_id>/', views.generate_report_view, name='generate_report'),
    path('event-registered-students/', views.event_registered_students_view, name='event_registered_students'),

]