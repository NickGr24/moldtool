"""
Modele de utilizatori pentru platforma MoldTool.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Manager pentru modelul personalizat de utilizator.
    Folosește email în loc de username pentru autentificare.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Creează și returnează un utilizator obișnuit."""
        if not email:
            raise ValueError(_('Email-ul este obligatoriu'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creează și returnează un superutilizator."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superutilizatorul trebuie să aibă is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superutilizatorul trebuie să aibă is_superuser=True'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Model personalizat de utilizator.
    Folosește email pentru autentificare în loc de username.
    """

    username = None
    email = models.EmailField(
        _('email'),
        unique=True,
        error_messages={
            'unique': _('Un utilizator cu acest email există deja.'),
        },
    )

    # Câmpuri suplimentare ale profilului
    phone = models.CharField(
        _('telefon'),
        max_length=20,
        blank=True,
    )
    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/',
        blank=True,
        null=True,
    )

    # Setări
    receive_notifications = models.BooleanField(
        _('primește notificări'),
        default=True,
    )

    # Metadate
    created_at = models.DateTimeField(
        _('data înregistrării'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('data actualizării'),
        auto_now=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('utilizator')
        verbose_name_plural = _('utilizatori')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Returnează numele complet al utilizatorului."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.email

    def get_short_name(self):
        """Returnează numele scurt al utilizatorului."""
        return self.first_name or self.email.split('@')[0]
