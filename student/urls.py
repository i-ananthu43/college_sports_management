from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('upcoming_events/', views.upcoming_events, name='upcoming_events'),
    path('event/<int:event_id>/register/', views.event_registration, name='event_registration'),
    path('student/view_registered_events/', views.view_registered_events, name='view_registered_events'),
    path('student/results/', views.view_results, name='view_results'),
    path('certificates/', views.view_certificates, name='view_certificates'),
    path('achievements/', views.view_achievements, name='view_achievements'),  # URL for viewing achievements
]
