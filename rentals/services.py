"""
Servicii pentru procesarea cererilor de închiriere: generare PDF și notificări email.
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

# Informații despre companie (duplicate din context_processor,
# deoarece serviciul poate funcționa în afara ciclului de request)
SITE_INFO = {
    'SITE_NAME': 'MoldTool',
    'SITE_TAGLINE': 'Închiriere de scule de construcție',
    'SITE_PHONE': '0 (60) 998 803',
    'SITE_EMAIL': 'info@moldtool.com',
    'SITE_ADDRESS': 'mun. Chișinău, str. Independenței 7',
}


def generate_rental_contract_pdf(rental_request):
    """
    Generează contractul PDF de închiriere (Contract de închiriere).
    Contractul este întotdeauna în limba română.

    Args:
        rental_request: instanță RentalRequest (cu tool încărcat)

    Returns:
        bytes: conținutul fișierului PDF
    """
    context = {
        'rental': rental_request,
        'tool': rental_request.tool,
        'now': timezone.now(),
        **SITE_INFO,
    }

    # Forțăm limba română pentru șablonul contractului
    with translation_override('ro'):
        html_string = render_to_string('rentals/pdf/contract.html', context)

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    return pdf_file.getvalue()


def generate_invoice_pdf(rental_request):
    """
    Generează factura PDF pentru achitare (Factură pentru achitare).
    Factura este întotdeauna în limba română.

    Args:
        rental_request: instanță RentalRequest (cu tool încărcat)

    Returns:
        bytes: conținutul fișierului PDF
    """
    context = {
        'rental': rental_request,
        'tool': rental_request.tool,
        'now': timezone.now(),
        **SITE_INFO,
    }

    with translation_override('ro'):
        html_string = render_to_string('rentals/pdf/invoice.html', context)

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    return pdf_file.getvalue()


def send_rental_expiry_reminder(rental_request):
    """
    Trimite clientului un email de memento despre expirarea apropiată a închirierii
    (cu 6 ore înainte de sfârșitul zilei de returnare).
    """
    context = {
        'rental': rental_request,
        'tool': rental_request.tool,
        **SITE_INFO,
    }

    subject = f'MoldTool — Termenul de închiriere expiră în curând #{rental_request.number}'

    with translation_override('ro'):
        text_content = render_to_string('rentals/email/expiry_reminder.txt', context)
        html_content = render_to_string('rentals/email/expiry_reminder.html', context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[rental_request.customer_email],
        reply_to=[settings.EMAIL_HOST_USER],
        headers={
            'X-Mailer': 'MoldTool',
            'List-Unsubscribe': f'<mailto:{settings.EMAIL_HOST_USER}?subject=unsubscribe>',
        },
    )
    email.attach_alternative(html_content, 'text/html')

    try:
        email.send(fail_silently=False)
        logger.info(
            'Memento privind sfârșitul închirierii trimis pentru cererea %s la %s',
            rental_request.number,
            rental_request.customer_email,
        )
    except Exception:
        logger.exception(
            'Nu s-a putut trimite memento-ul pentru cererea %s la %s',
            rental_request.number,
            rental_request.customer_email,
        )
        raise


def send_rental_confirmation_email(rental_request):
    """
    Trimite email-ul de confirmare clientului cu contractul PDF atașat.

    Args:
        rental_request: instanță RentalRequest (cu tool încărcat)
    """
    context = {
        'rental': rental_request,
        'tool': rental_request.tool,
        **SITE_INFO,
    }

    subject = f'MoldTool — Cerere de închiriere #{rental_request.number}'

    # Randăm șabloanele de email
    text_content = render_to_string('rentals/email/confirmation.txt', context)
    html_content = render_to_string('rentals/email/confirmation.html', context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[rental_request.customer_email],
        reply_to=[settings.EMAIL_HOST_USER],
        headers={
            'X-Mailer': 'MoldTool',
            'List-Unsubscribe': f'<mailto:{settings.EMAIL_HOST_USER}?subject=unsubscribe>',
        },
    )
    email.attach_alternative(html_content, 'text/html')

    # Generăm și atașăm contractul PDF
    try:
        pdf_content = generate_rental_contract_pdf(rental_request)
        filename = f'Contract_MoldTool_{rental_request.number}.pdf'
        email.attach(filename, pdf_content, 'application/pdf')
    except Exception:
        logger.exception(
            'Nu s-a putut genera contractul PDF pentru cererea %s',
            rental_request.number,
        )

    # Generăm și atașăm factura PDF
    try:
        invoice_pdf = generate_invoice_pdf(rental_request)
        invoice_filename = f'Factura_MoldTool_{rental_request.number}.pdf'
        email.attach(invoice_filename, invoice_pdf, 'application/pdf')
    except Exception:
        logger.exception(
            'Nu s-a putut genera factura PDF pentru cererea %s',
            rental_request.number,
        )

    # Trimitem email-ul
    try:
        email.send(fail_silently=False)
        logger.info(
            'Email-ul de confirmare a fost trimis pentru cererea %s la %s',
            rental_request.number,
            rental_request.customer_email,
        )
    except Exception:
        logger.exception(
            'Nu s-a putut trimite email-ul pentru cererea %s la %s. '
            'Verificați EMAIL_HOST_USER și EMAIL_HOST_PASSWORD în setări.',
            rental_request.number,
            rental_request.customer_email,
        )
