# core/urls.py
from django.urls import include, path

import student
from .views import edit_student, index, logout_view, student_list
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('student/', include('student.urls')),
    path('coordinator/', include('coordinator.urls')),

    path('login/', views.login_view, name='login'),
    path('', logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('admin_panel/students/', student_list, name='student_list'),
    path('admin_panel/students/edit/<int:student_id>/', edit_student, name='edit_student'),
   
    path('edit/<int:student_id>/', edit_student, name='edit_student'),
]
