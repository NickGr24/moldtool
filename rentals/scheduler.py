"""
Planificator in-process pentru rularea regulată a sarcinilor de fundal.
Pornește automat la inițializarea Django (vezi rentals/apps.py).
"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.management import call_command

logger = logging.getLogger(__name__)

_scheduler = None


def _run_send_rental_reminders():
    try:
        call_command('send_rental_reminders')
    except Exception:
        logger.exception('Eroare la rularea send_rental_reminders din planificator')


def start():
    global _scheduler
    if _scheduler is not None:
        return

    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(
        _run_send_rental_reminders,
        trigger='interval',
        minutes=15,
        id='send_rental_reminders',
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    scheduler.start()
    _scheduler = scheduler
    logger.info('Background scheduler started: send_rental_reminders every 15 min')
