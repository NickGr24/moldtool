"""
URL маршруты для заявок на аренду.
"""

from django.urls import path

from . import views

app_name = 'rentals'

urlpatterns = [
    path('rent/<slug:tool_slug>/', views.CreateRentalRequestView.as_view(), name='create_request'),
    path('success/<str:number>/', views.RentalRequestSuccessView.as_view(), name='request_success'),
    path('request/<str:number>/', views.RentalRequestDetailView.as_view(), name='request_detail'),
    path('my-requests/', views.UserRentalRequestsView.as_view(), name='user_requests'),
    path('cancel/<str:number>/', views.CancelRentalRequestView.as_view(), name='cancel_request'),
]
