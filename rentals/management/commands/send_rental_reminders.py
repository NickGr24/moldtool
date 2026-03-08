"""
Management command для отправки напоминаний об окончании аренды.
Запускать через cron каждые 30 минут: python manage.py send_rental_reminders
"""

from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.utils import timezone

from rentals.models import RentalRequest


class Command(BaseCommand):
    help = 'Отправляет напоминания за 3 часа до окончания аренды'

    def handle(self, *args, **options):
        now = timezone.now()
        today = now.date()

        rentals = RentalRequest.objects.filter(
            end_date=today,
            status__in=[
                RentalRequest.Status.CONFIRMED,
                RentalRequest.Status.IN_PROGRESS,
            ],
            reminder_sent=False,
        )

        end_of_day = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.min.time())
        ) + timedelta(days=1)
        hours_left = (end_of_day - now).total_seconds() / 3600

        if hours_left > 3:
            self.stdout.write('Ещё не время для напоминаний.')
            return

        sent_count = 0
        for rental in rentals:
            try:
                self._send_reminder(rental)
                rental.reminder_sent = True
                rental.save(update_fields=['reminder_sent'])
                sent_count += 1
            except Exception as e:
                self.stderr.write(f'Ошибка для заявки {rental.number}: {e}')

        self.stdout.write(f'Отправлено напоминаний: {sent_count}')

    def _send_reminder(self, rental):
        subject = f'MoldTool — Termenul de închiriere expiră astăzi #{rental.number}'

        text = (
            f'Bună ziua, {rental.customer_name}!\n\n'
            f'Vă reamintim că termenul de închiriere a sculei '
            f'"{rental.tool.name}" expiră astăzi, {rental.end_date.strftime("%d.%m.%Y")}.\n\n'
            f'Vă rugăm să returnați scula la timp pentru a evita '
            f'eventualele penalități.\n\n'
            f'Dacă doriți să prelungiți perioada de închiriere, '
            f'contactați-ne la 0 (60) 998 803.\n\n'
            f'Cu respect,\nEchipa MoldTool'
        )

        html = f'''<!DOCTYPE html>
<html lang="ro">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background-color:#f5f5f5;font-family:Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f5f5f5;padding:30px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background-color:#fff;border-radius:8px;overflow:hidden;">

<tr><td style="background-color:#E53935;padding:25px 30px;text-align:center;">
    <h1 style="margin:0;color:#fff;font-size:26px;">MoldTool</h1>
    <p style="margin:5px 0 0;color:rgba(255,255,255,0.85);font-size:13px;">Închiriere de scule de construcție</p>
</td></tr>

<tr><td style="padding:30px;">
    <h2 style="color:#333;margin:0 0 15px;font-size:20px;">Bună ziua, {rental.customer_name}!</h2>

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#FFF3E0;border-radius:6px;border-left:4px solid #FF9800;margin:0 0 20px;">
    <tr><td style="padding:15px;">
        <p style="margin:0 0 5px;color:#E65100;font-weight:bold;font-size:15px;">Termenul de închiriere expiră astăzi!</p>
        <p style="margin:0;color:#555;font-size:14px;line-height:1.6;">
            Vă reamintim că termenul de închiriere a sculei
            <strong>{rental.tool.name}</strong> expiră astăzi,
            <strong>{rental.end_date.strftime("%d.%m.%Y")}</strong>.
        </p>
    </td></tr>
    </table>

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f9f9f9;border-radius:6px;margin:0 0 20px;">
    <tr><td style="padding:15px;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td style="padding:8px 0;color:#888;font-size:13px;border-bottom:1px solid #eee;">Nr. cerere</td>
                <td style="padding:8px 0;text-align:right;font-weight:bold;color:#333;border-bottom:1px solid #eee;">#{rental.number}</td>
            </tr>
            <tr>
                <td style="padding:8px 0;color:#888;font-size:13px;border-bottom:1px solid #eee;">Sculă</td>
                <td style="padding:8px 0;text-align:right;color:#333;border-bottom:1px solid #eee;">{rental.tool.name}</td>
            </tr>
            <tr>
                <td style="padding:8px 0;color:#888;font-size:13px;">Data returnării</td>
                <td style="padding:8px 0;text-align:right;font-weight:bold;color:#E53935;">{rental.end_date.strftime("%d.%m.%Y")}</td>
            </tr>
        </table>
    </td></tr>
    </table>

    <p style="color:#555;line-height:1.6;margin:0 0 20px;">
        Vă rugăm să returnați scula la timp pentru a evita eventualele penalități.
        Dacă doriți să prelungiți perioada de închiriere, contactați-ne.
    </p>

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#E8F5E9;border-radius:6px;border-left:4px solid #4CAF50;margin:0 0 10px;">
    <tr><td style="padding:15px;">
        <p style="margin:0 0 5px;color:#555;font-size:13px;">Contacte:</p>
        <p style="margin:0;color:#333;font-size:14px;">
            <strong>Telefon:</strong> 0 (60) 998 803<br>
            <strong>Email:</strong> moldtooloffice@gmail.com
        </p>
    </td></tr>
    </table>
</td></tr>

<tr><td style="background-color:#1a1a1a;padding:20px 30px;text-align:center;">
    <p style="margin:0;color:#888;font-size:12px;">&copy; MoldTool | mun. Chișinău, str. Independenței 7</p>
</td></tr>

</table>
</td></tr>
</table>
</body>
</html>'''

        email = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[rental.customer_email],
            reply_to=[settings.EMAIL_HOST_USER],
            headers={
                'X-Mailer': 'MoldTool',
                'List-Unsubscribe': f'<mailto:{settings.EMAIL_HOST_USER}?subject=unsubscribe>',
            },
        )
        email.attach_alternative(html, 'text/html')
        email.send(fail_silently=False)
