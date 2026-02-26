"""
Контекстные процессоры для глобальных переменных в шаблонах.
"""

from django.conf import settings


def site_settings(request):
    """
    Добавляет глобальные настройки сайта во все шаблоны.
    """
    return {
        'SITE_NAME': 'MoldTool',
        'SITE_TAGLINE': 'Închiriere de scule de construcție',
        'SITE_PHONE': '0 (60) 998 803',
        'SITE_EMAIL': 'info@moldtool.com',
        'SITE_ADDRESS': 'mun. Chișinău, str. Independenței 7',
        'DEBUG': settings.DEBUG,
    }
