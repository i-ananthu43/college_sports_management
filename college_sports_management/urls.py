"""
URL configuration for college_sports_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required, user_passes_test

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include('core.urls')),
     path('', include('core.urls')),
    path('admin_panel/', include('admin_panel.urls')),
    path('student/', include('student.urls')),
    path('coordinator/', include('coordinator.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

def admin_required(user):
    return user.is_superuser

def coordinator_required(user):
    return user.is_staff

@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    # Admin-specific logic
    return render(request, 'admin_panel/dashboard.html')

@login_required
@user_passes_test(coordinator_required)
def coordinator_dashboard(request):
    # Coordinator-specific logic
    return render(request, 'coordinator/dashboard.html')