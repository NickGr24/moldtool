"""
URL маршруты для каталога инструментов.
"""

from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.CatalogView.as_view(), name='catalog'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('tool/<slug:slug>/', views.ToolDetailView.as_view(), name='tool_detail'),
]
