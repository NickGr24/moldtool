"""
Модели пользователей для платформы MoldTool.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Менеджер для кастомной модели пользователя.
    Использует email вместо username для аутентификации.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Создаёт и возвращает обычного пользователя."""
        if not email:
            raise ValueError(_('Email обязателен'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создаёт и возвращает суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Использует email для аутентификации вместо username.
    """

    username = None
    email = models.EmailField(
        _('email'),
        unique=True,
        error_messages={
            'unique': _('Пользователь с таким email уже существует.'),
        },
    )

    # Дополнительные поля профиля
    phone = models.CharField(
        _('телефон'),
        max_length=20,
        blank=True,
    )
    avatar = models.ImageField(
        _('аватар'),
        upload_to='avatars/',
        blank=True,
        null=True,
    )

    # Настройки
    receive_notifications = models.BooleanField(
        _('получать уведомления'),
        default=True,
    )

    # Метаданные
    created_at = models.DateTimeField(
        _('дата регистрации'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('дата обновления'),
        auto_now=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Возвращает полное имя пользователя."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.email

    def get_short_name(self):
        """Возвращает короткое имя пользователя."""
        return self.first_name or self.email.split('@')[0]
