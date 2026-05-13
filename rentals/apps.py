import os
import sys

from django.apps import AppConfig


class RentalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rentals'

    def ready(self):
        # Sărim peste comenzile la care planificatorul nu este necesar (migrări, teste, shell etc.)
        skip_commands = {
            'migrate', 'makemigrations', 'shell', 'shell_plus',
            'collectstatic', 'createsuperuser', 'changepassword',
            'test', 'compilemessages', 'makemessages',
            'send_rental_reminders', 'create_test_data',
            'dumpdata', 'loaddata', 'flush', 'sqlmigrate', 'showmigrations',
        }
        if len(sys.argv) > 1 and sys.argv[1] in skip_commands:
            return

        # La runserver Django generează un proces fiu pentru auto-reîncărcare;
        # pornim planificatorul doar în acesta, pentru a nu avea două instanțe.
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
            return

        from rentals import scheduler
        scheduler.start()
