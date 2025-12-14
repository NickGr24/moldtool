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
        'SITE_PHONE': '+373 XX XXX XXX',
        'SITE_EMAIL': 'info@moldtool.md',
        'SITE_ADDRESS': 'г. Кишинёв, ул. Примерная, 123',
        'DEBUG': settings.DEBUG,
    }
