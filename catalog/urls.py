"""
URL маршруты для каталога инструментов.
"""

from django.urls import path, re_path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.CatalogView.as_view(), name='catalog'),
    re_path(r'^category/(?P<slug>[\w-]+)/$', views.CategoryView.as_view(), name='category'),
    re_path(r'^tool/(?P<slug>[\w-]+)/$', views.ToolDetailView.as_view(), name='tool_detail'),
    path('favorites/', views.FavoritesListView.as_view(), name='favorites'),
    path('favorite/toggle/<int:tool_id>/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('review/add/<int:tool_id>/', views.AddReviewView.as_view(), name='add_review'),
    path('faq/', views.FAQView.as_view(), name='faq'),
]
