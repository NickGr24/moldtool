"""
URL маршруты для core приложения.
"""

from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('terms/', views.TermsConditionsView.as_view(), name='terms'),
]
