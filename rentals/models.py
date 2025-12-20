"""
Модели заявок на аренду для платформы MoldTool.
"""

import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from catalog.models import Tool


class RentalRequest(models.Model):
    """Заявка на аренду инструмента."""

    class Status(models.TextChoices):
        PENDING = 'pending', _('Ожидает рассмотрения')
        CONFIRMED = 'confirmed', _('Подтверждена')
        IN_PROGRESS = 'in_progress', _('В процессе аренды')
        COMPLETED = 'completed', _('Завершена')
        CANCELLED = 'cancelled', _('Отменена')
        REJECTED = 'rejected', _('Отклонена')

    # Уникальный номер заявки
    number = models.CharField(
        _('номер заявки'),
        max_length=20,
        unique=True,
        editable=False,
    )

    # Связи
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rental_requests',
        verbose_name=_('пользователь'),
        null=True,
        blank=True,
    )
    tool = models.ForeignKey(
        Tool,
        on_delete=models.PROTECT,
        related_name='rental_requests',
        verbose_name=_('инструмент'),
    )

    # Контактные данные (для гостей и дублирования)
    customer_name = models.CharField(
        _('имя клиента'),
        max_length=100,
    )
    customer_email = models.EmailField(
        _('email клиента'),
    )
    customer_phone = models.CharField(
        _('телефон клиента'),
        max_length=20,
    )

    # Даты аренды
    start_date = models.DateField(
        _('дата начала'),
    )
    end_date = models.DateField(
        _('дата окончания'),
    )

    # Финансы
    price_per_day = models.DecimalField(
        _('цена за день'),
        max_digits=10,
        decimal_places=2,
    )
    total_days = models.PositiveIntegerField(
        _('количество дней'),
    )
    total_price = models.DecimalField(
        _('общая стоимость'),
        max_digits=10,
        decimal_places=2,
    )
    deposit_amount = models.DecimalField(
        _('сумма залога'),
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # Статус
    status = models.CharField(
        _('статус'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # Дополнительно
    comment = models.TextField(
        _('комментарий клиента'),
        blank=True,
    )
    admin_notes = models.TextField(
        _('заметки менеджера'),
        blank=True,
    )

    # Метаданные
    created_at = models.DateTimeField(
        _('дата создания'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('дата обновления'),
        auto_now=True,
    )
    confirmed_at = models.DateTimeField(
        _('дата подтверждения'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('заявка на аренду')
        verbose_name_plural = _('заявки на аренду')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['number']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f'Заявка #{self.number} - {self.tool.name}'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self._generate_number()

        # Рассчитываем количество дней и сумму
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.total_days = delta.days + 1  # Включая день начала

            if self.price_per_day:
                self.total_price = self.price_per_day * Decimal(self.total_days)

        super().save(*args, **kwargs)

    def _generate_number(self):
        """Генерирует уникальный номер заявки."""
        today = timezone.now()
        prefix = today.strftime('%Y%m')
        random_suffix = uuid.uuid4().hex[:6].upper()
        return f'{prefix}-{random_suffix}'

    def get_absolute_url(self):
        return reverse('rentals:request_detail', kwargs={'number': self.number})

    def confirm(self):
        """Подтверждает заявку."""
        self.status = self.Status.CONFIRMED
        self.confirmed_at = timezone.now()
        self.save(update_fields=['status', 'confirmed_at', 'updated_at'])

    def cancel(self):
        """Отменяет заявку."""
        self.status = self.Status.CANCELLED
        self.save(update_fields=['status', 'updated_at'])

    def reject(self):
        """Отклоняет заявку."""
        self.status = self.Status.REJECTED
        self.save(update_fields=['status', 'updated_at'])

    def start_rental(self):
        """Начинает аренду."""
        self.status = self.Status.IN_PROGRESS
        self.save(update_fields=['status', 'updated_at'])

        # Уменьшаем доступное количество инструмента
        self.tool.quantity_available -= 1
        if self.tool.quantity_available == 0:
            self.tool.availability = Tool.Availability.RENTED
        self.tool.save(update_fields=['quantity_available', 'availability'])

    def complete_rental(self):
        """Завершает аренду."""
        self.status = self.Status.COMPLETED
        self.save(update_fields=['status', 'updated_at'])

        # Возвращаем инструмент
        self.tool.quantity_available += 1
        self.tool.availability = Tool.Availability.AVAILABLE
        self.tool.save(update_fields=['quantity_available', 'availability'])

    @property
    def is_editable(self):
        """Можно ли редактировать заявку."""
        return self.status in [self.Status.PENDING]

    @property
    def can_be_cancelled(self):
        """Можно ли отменить заявку."""
        return self.status in [self.Status.PENDING, self.Status.CONFIRMED]
