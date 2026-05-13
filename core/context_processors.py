"""
Procesoare de context pentru variabile globale în șabloane.
"""

from django.conf import settings


def site_settings(request):
    """
    Adaugă setările globale ale site-ului în toate șabloanele.
    """
    return {
        'SITE_NAME': 'MoldTool',
        'SITE_TAGLINE': 'Închiriere de scule de construcție',
        'SITE_PHONE': '0 (60) 998 803',
        'SITE_EMAIL': 'info@moldtool.com',
        'SITE_ADDRESS': 'mun. Chișinău, str. Independenței 7',
        'DEBUG': settings.DEBUG,
    }
