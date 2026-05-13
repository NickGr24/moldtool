"""
Modele pentru cererile de închiriere ale platformei MoldTool.
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
    """Cerere de închiriere a unei scule."""

    DELIVERY_FEE = Decimal('200')

    class Status(models.TextChoices):
        PENDING = 'pending', _('În așteptare')
        CONFIRMED = 'confirmed', _('Confirmată')
        IN_PROGRESS = 'in_progress', _('În curs de închiriere')
        COMPLETED = 'completed', _('Finalizată')
        CANCELLED = 'cancelled', _('Anulată')
        REJECTED = 'rejected', _('Respinsă')

    class DeliveryMethod(models.TextChoices):
        PICKUP = 'pickup', _('Ridicare personală')
        DELIVERY = 'delivery', _('Livrare')

    # Numărul unic al cererii
    number = models.CharField(
        _('numărul cererii'),
        max_length=20,
        unique=True,
        editable=False,
    )

    # Relații
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rental_requests',
        verbose_name=_('utilizator'),
        null=True,
        blank=True,
    )
    tool = models.ForeignKey(
        Tool,
        on_delete=models.PROTECT,
        related_name='rental_requests',
        verbose_name=_('sculă'),
    )

    # Date de contact (pentru oaspeți și pentru duplicare)
    customer_name = models.CharField(
        _('numele clientului'),
        max_length=100,
    )
    customer_email = models.EmailField(
        _('email-ul clientului'),
    )
    customer_phone = models.CharField(
        _('telefonul clientului'),
        max_length=20,
    )

    # Datele închirierii
    start_date = models.DateField(
        _('data de început'),
    )
    end_date = models.DateField(
        _('data de sfârșit'),
    )

    # Finanțe
    price_per_day = models.DecimalField(
        _('preț pe zi'),
        max_digits=10,
        decimal_places=2,
    )
    total_days = models.PositiveIntegerField(
        _('număr de zile'),
    )
    total_price = models.DecimalField(
        _('cost total'),
        max_digits=10,
        decimal_places=2,
    )

    # Livrare
    delivery_method = models.CharField(
        _('metoda de primire'),
        max_length=20,
        choices=DeliveryMethod.choices,
        default=DeliveryMethod.PICKUP,
    )
    delivery_address = models.CharField(
        _('adresa de livrare'),
        max_length=500,
        blank=True,
    )
    delivery_price = models.DecimalField(
        _('costul livrării'),
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # Status
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # Suplimentar
    comment = models.TextField(
        _('comentariul clientului'),
        blank=True,
    )
    admin_notes = models.TextField(
        _('notele administratorului'),
        blank=True,
    )

    # Memento
    reminder_sent = models.BooleanField(
        _('memento trimis'),
        default=False,
    )

    # Metadate
    created_at = models.DateTimeField(
        _('data creării'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('data actualizării'),
        auto_now=True,
    )
    confirmed_at = models.DateTimeField(
        _('data confirmării'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('cerere de închiriere')
        verbose_name_plural = _('cereri de închiriere')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['number']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f'Cerere #{self.number} - {self.tool.name}'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self._generate_number()

        # Costul livrării este determinat de metoda de primire
        if self.delivery_method == self.DeliveryMethod.DELIVERY:
            self.delivery_price = self.DELIVERY_FEE
        else:
            self.delivery_price = Decimal('0')
            self.delivery_address = ''

        # Calculăm numărul de zile și suma
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.total_days = delta.days + 1  # Inclusiv ziua de început

            if self.price_per_day:
                self.total_price = (
                    self.price_per_day * Decimal(self.total_days)
                    + self.delivery_price
                )

        super().save(*args, **kwargs)

    def _generate_number(self):
        """Generează un număr unic pentru cerere."""
        today = timezone.now()
        prefix = today.strftime('%Y%m')
        random_suffix = uuid.uuid4().hex[:6].upper()
        return f'{prefix}-{random_suffix}'

    def get_absolute_url(self):
        return reverse('rentals:request_detail', kwargs={'number': self.number})

    def confirm(self):
        """Confirmă cererea."""
        self.status = self.Status.CONFIRMED
        self.confirmed_at = timezone.now()
        self.save(update_fields=['status', 'confirmed_at', 'updated_at'])

    def cancel(self):
        """Anulează cererea."""
        self.status = self.Status.CANCELLED
        self.save(update_fields=['status', 'updated_at'])

    def reject(self):
        """Respinge cererea."""
        self.status = self.Status.REJECTED
        self.save(update_fields=['status', 'updated_at'])

    def start_rental(self):
        """Începe închirierea."""
        self.status = self.Status.IN_PROGRESS
        self.save(update_fields=['status', 'updated_at'])

        # Reducem cantitatea disponibilă a sculei
        self.tool.quantity_available -= 1
        if self.tool.quantity_available == 0:
            self.tool.availability = Tool.Availability.RENTED
        self.tool.save(update_fields=['quantity_available', 'availability'])

    def complete_rental(self):
        """Finalizează închirierea."""
        self.status = self.Status.COMPLETED
        self.save(update_fields=['status', 'updated_at'])

        # Returnăm scula
        self.tool.quantity_available += 1
        self.tool.availability = Tool.Availability.AVAILABLE
        self.tool.save(update_fields=['quantity_available', 'availability'])

    @property
    def is_editable(self):
        """Indică dacă cererea poate fi editată."""
        return self.status in [self.Status.PENDING]

    @property
    def can_be_cancelled(self):
        """Indică dacă cererea poate fi anulată."""
        return self.status in [self.Status.PENDING, self.Status.CONFIRMED]
