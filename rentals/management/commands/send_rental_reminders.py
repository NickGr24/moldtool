"""
Management command pentru trimiterea memento-urilor privind sfârșitul închirierii.
Rulează prin planificator (rentals/scheduler.py) la fiecare 15 minute,
sau manual: python manage.py send_rental_reminders
"""

from datetime import timedelta, time

from django.core.management.base import BaseCommand
from django.utils import timezone

from rentals.models import RentalRequest
from rentals.services import send_rental_expiry_reminder


class Command(BaseCommand):
    help = 'Trimite memento-uri cu 6 ore înainte de sfârșitul închirierii'

    REMINDER_HOURS_BEFORE = 6

    def handle(self, *args, **options):
        now = timezone.localtime()
        today = now.date()

        rentals = RentalRequest.objects.filter(
            end_date=today,
            status__in=[
                RentalRequest.Status.CONFIRMED,
                RentalRequest.Status.IN_PROGRESS,
            ],
            reminder_sent=False,
        )

        # Sfârșitul zilei de returnare = miezul nopții următoarei zile în TZ-ul local
        end_of_day = timezone.make_aware(
            timezone.datetime.combine(today, time.min)
        ) + timedelta(days=1)
        hours_left = (end_of_day - now).total_seconds() / 3600

        if hours_left > self.REMINDER_HOURS_BEFORE:
            self.stdout.write(
                f'Încă nu este momentul pentru memento-uri (au rămas {hours_left:.1f} h).'
            )
            return

        sent_count = 0
        for rental in rentals:
            try:
                send_rental_expiry_reminder(rental)
                rental.reminder_sent = True
                rental.save(update_fields=['reminder_sent'])
                sent_count += 1
            except Exception as e:
                self.stderr.write(f'Eroare pentru cererea {rental.number}: {e}')

        self.stdout.write(f'Memento-uri trimise: {sent_count}')
