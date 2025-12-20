"""
URL configuration for MoldTool project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication (django-allauth)
    path('accounts/', include('allauth.urls')),

    # Local apps
    path('', include('core.urls', namespace='core')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('rentals/', include('rentals.urls', namespace='rentals')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from both STATICFILES_DIRS and STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = 'MoldTool Administration'
admin.site.site_title = 'MoldTool Admin'
admin.site.index_title = 'Панель управления'
