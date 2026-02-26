"""
Сервисы для обработки заявок на аренду: генерация PDF и email-уведомления.
"""

import logging
from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import override as translation_override

from weasyprint import HTML

logger = logging.getLogger(__name__)

# Информация о компании (дублируем из context_processor,
# т.к. сервис может работать вне request-цикла)
SITE_INFO = {
    'SITE_NAME': 'MoldTool',
    'SITE_TAGLINE': 'Închiriere de scule de construcție',
    'SITE_PHONE': '0 (60) 998 803',
    'SITE_EMAIL': 'info@moldtool.com',
    'SITE_ADDRESS': 'mun. Chișinău, str. Independenței 7',
}


def generate_rental_contract_pdf(rental_request):
    """
    Генерирует PDF контракт аренды (Contract de închiriere).
    Контракт всегда на румынском языке.

    Args:
        rental_request: экземпляр RentalRequest (с загруженным tool)

    Returns:
        bytes: содержимое PDF файла
    """
    context = {
        'rental': rental_request,
        'tool': rental_request.tool,
        'now': timezone.now(),
        **SITE_INFO,
    }

    # Принудительно используем румынский для шаблона контракта
    with translation_override('ro'):
        html_string = render_to_string('rentals/pdf/contract.html', context)

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    return pdf_file.getvalue()


def send_rental_confirmation_email(rental_request):
    """
    Отправляет email-подтверждение клиенту с PDF контрактом во вложении.

    Args:
        rental_request: экземпляр RentalRequest (с загруженным tool)
    """
    context = {
        'rental': rental_request,
        'tool': rental_request.tool,
        **SITE_INFO,
    }

    subject = f'MoldTool — Cerere de închiriere #{rental_request.number}'

    # Рендерим email шаблоны
    text_content = render_to_string('rentals/email/confirmation.txt', context)
    html_content = render_to_string('rentals/email/confirmation.html', context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[rental_request.customer_email],
    )
    email.attach_alternative(html_content, 'text/html')

    # Генерируем и прикрепляем PDF
    try:
        pdf_content = generate_rental_contract_pdf(rental_request)
        filename = f'Contract_MoldTool_{rental_request.number}.pdf'
        email.attach(filename, pdf_content, 'application/pdf')
    except Exception:
        logger.exception(
            'Не удалось сгенерировать PDF для заявки %s',
            rental_request.number,
        )

    # Отправляем email
    try:
        email.send()
        logger.info(
            'Email-подтверждение отправлено для заявки %s на %s',
            rental_request.number,
            rental_request.customer_email,
        )
    except Exception:
        logger.exception(
            'Не удалось отправить email для заявки %s',
            rental_request.number,
        )
