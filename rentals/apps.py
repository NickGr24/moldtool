import os
import sys

from django.apps import AppConfig


class RentalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rentals'

    def ready(self):
        # Скипаем команды, при которых scheduler не нужен (миграции, тесты, shell и т.п.)
        skip_commands = {
            'migrate', 'makemigrations', 'shell', 'shell_plus',
            'collectstatic', 'createsuperuser', 'changepassword',
            'test', 'compilemessages', 'makemessages',
            'send_rental_reminders', 'create_test_data',
            'dumpdata', 'loaddata', 'flush', 'sqlmigrate', 'showmigrations',
        }
        if len(sys.argv) > 1 and sys.argv[1] in skip_commands:
            return

        # При runserver Django порождает дочерний процесс для автоперезагрузки;
        # запускаем планировщик только в нём, чтобы не было двух экземпляров.
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
            return

        from rentals import scheduler
        scheduler.start()
