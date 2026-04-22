from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = _('Учётные записи')

    def ready(self):
        """Import signals when app is ready."""
        import accounts.signals  # noqa: F401
