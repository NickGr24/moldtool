"""
URL маршруты для личного кабинета.
"""

from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardIndexView.as_view(), name='index'),
    path('orders/', views.OrdersListView.as_view(), name='orders'),
    path('favorites/', views.FavoritesListView.as_view(), name='favorites'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
]
