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
        'SITE_TAGLINE': 'Аренда строительных инструментов',
        'SITE_PHONE': '0 (60) 998 803',
        'SITE_EMAIL': 'info@moto4rent.md',
        'SITE_ADDRESS': 'г. Кишинёв, ул. Индепендеций 7',
        'DEBUG': settings.DEBUG,
    }
