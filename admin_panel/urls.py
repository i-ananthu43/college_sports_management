from django.urls import include, path
from django.contrib.auth import views as auth_views

import core
from . import views

urlpatterns = [
    path('',include('core.urls')),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-event/', views.create_event, name='create_event'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('test/', views.test_view, name='test_view'),
    path('approve_student/<int:student_id>/', views.approve_student, name='approve_student'),
    path('reject_student/<int:student_id>/', views.reject_student, name='reject_student'),
   
    path('coordinators/', views.coordinators_list, name='coordinators_list'),
    path('coordinators/add/', views.add_coordinator, name='add_coordinator'),         # Add a new coordinator
    path('coordinators/edit/<int:user_id>/', views.edit_coordinator, name='edit_coordinator'),  # Edit coordinator
    path('coordinators/delete/user/<int:user_id>/', views.delete_coordinator, name='delete_coordinator'),


    path('students/', views.student_list, name='student_list'),

    path('sport_events/', views.sport_event_list, name='sport_events'),
    path('sport_events/add/', views.sport_event_add, name='sport_event_add'),
    path('sport_events/edit/<int:event_id>/', views.sport_event_edit, name='sport_event_edit'),
    path('sport_events/delete/<int:event_id>/', views.sport_event_delete, name='sport_event_delete'),
]
