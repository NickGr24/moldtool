"""
URL маршруты для core приложения.
"""

from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]
