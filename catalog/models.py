"""
Modele pentru catalogul de scule al platformei MoldTool.
"""

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Categorie de scule."""

    name = models.CharField(
        _('denumire'),
        max_length=100,
    )
    slug = models.SlugField(
        _('URL'),
        max_length=100,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        _('descriere'),
        blank=True,
    )
    image = models.ImageField(
        _('imagine'),
        upload_to='categories/',
        blank=True,
        null=True,
    )
    icon = models.CharField(
        _('clasă CSS pentru pictogramă'),
        max_length=50,
        blank=True,
        help_text=_('De exemplu: icon-drill, icon-hammer'),
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('categorie părinte'),
    )
    is_active = models.BooleanField(
        _('activă'),
        default=True,
    )
    order = models.PositiveIntegerField(
        _('ordinea de sortare'),
        default=0,
    )
    created_at = models.DateTimeField(
        _('data creării'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('categorie')
        verbose_name_plural = _('categorii')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug})

    @property
    def tools_count(self):
        """Numărul de scule active în categorie."""
        return self.tools.filter(is_active=True).count()


class Tool(models.Model):
    """Sculă disponibilă pentru închiriere."""

    class Condition(models.TextChoices):
        NEW = 'new', _('Nouă')
        EXCELLENT = 'excellent', _('Excelentă')
        GOOD = 'good', _('Bună')
        FAIR = 'fair', _('Satisfăcătoare')

    class Availability(models.TextChoices):
        AVAILABLE = 'available', _('Disponibilă')
        RENTED = 'rented', _('Închiriată')
        MAINTENANCE = 'maintenance', _('În mentenanță')
        UNAVAILABLE = 'unavailable', _('Indisponibilă')

    # Informații principale
    name = models.CharField(
        _('denumire'),
        max_length=200,
    )
    slug = models.SlugField(
        _('URL'),
        max_length=200,
        unique=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='tools',
        verbose_name=_('categorie'),
    )
    description = models.TextField(
        _('descriere'),
    )
    short_description = models.CharField(
        _('descriere scurtă'),
        max_length=300,
        blank=True,
    )

    # Imagini
    image = models.ImageField(
        _('imagine principală'),
        upload_to='tools/',
    )

    # Caracteristici
    brand = models.CharField(
        _('brand'),
        max_length=100,
        blank=True,
    )
    model_name = models.CharField(
        _('model'),
        max_length=100,
        blank=True,
    )
    specifications = models.JSONField(
        _('caracteristici'),
        default=dict,
        blank=True,
        help_text=_('Caracteristici tehnice în format JSON'),
    )

    # Prețuri
    price_per_day = models.DecimalField(
        _('preț pe zi'),
        max_digits=10,
        decimal_places=2,
    )

    # Status
    condition = models.CharField(
        _('stare'),
        max_length=20,
        choices=Condition.choices,
        default=Condition.EXCELLENT,
    )
    availability = models.CharField(
        _('disponibilitate'),
        max_length=20,
        choices=Availability.choices,
        default=Availability.AVAILABLE,
    )
    quantity = models.PositiveIntegerField(
        _('cantitate'),
        default=1,
    )
    quantity_available = models.PositiveIntegerField(
        _('cantitate disponibilă'),
        default=1,
    )

    # Metadate
    is_active = models.BooleanField(
        _('activă'),
        default=True,
    )
    is_featured = models.BooleanField(
        _('recomandată'),
        default=False,
    )
    views_count = models.PositiveIntegerField(
        _('număr de vizualizări'),
        default=0,
    )
    created_at = models.DateTimeField(
        _('data adăugării'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('data actualizării'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('sculă')
        verbose_name_plural = _('scule')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['availability']),
            models.Index(fields=['is_featured', '-created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:tool_detail', kwargs={'slug': self.slug})

    @property
    def is_available(self):
        """Verifică dacă scula este disponibilă pentru închiriere."""
        return (
            self.is_active
            and self.availability == self.Availability.AVAILABLE
            and self.quantity_available > 0
        )

    def increment_views(self):
        """Incrementează contorul de vizualizări."""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    @property
    def average_rating(self):
        """Returnează ratingul mediu al sculei."""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0

    @property
    def reviews_count(self):
        """Returnează numărul de recenzii."""
        return self.reviews.filter(is_approved=True).count()


class ToolImage(models.Model):
    """Imagini suplimentare ale sculei."""

    tool = models.ForeignKey(
        Tool,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('sculă'),
    )
    image = models.ImageField(
        _('imagine'),
        upload_to='tools/gallery/',
    )
    alt_text = models.CharField(
        _('text alternativ'),
        max_length=200,
        blank=True,
    )
    order = models.PositiveIntegerField(
        _('ordine'),
        default=0,
    )

    class Meta:
        verbose_name = _('imagine sculă')
        verbose_name_plural = _('imagini scule')
        ordering = ['order']

    def __str__(self):
        return f'{self.tool.name} - imagine {self.order}'


class Favorite(models.Model):
    """Sculele preferate ale utilizatorului."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('utilizator'),
    )
    tool = models.ForeignKey(
        Tool,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name=_('sculă'),
    )
    created_at = models.DateTimeField(
        _('data adăugării'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('favorită')
        verbose_name_plural = _('favorite')
        unique_together = ['user', 'tool']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.tool.name}'


class Review(models.Model):
    """Recenzie pentru o sculă."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('utilizator'),
    )
    tool = models.ForeignKey(
        Tool,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('sculă'),
    )
    rating = models.PositiveSmallIntegerField(
        _('notă'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField(
        _('text recenzie'),
        blank=True,
    )
    created_at = models.DateTimeField(
        _('data creării'),
        auto_now_add=True,
    )
    is_approved = models.BooleanField(
        _('aprobată'),
        default=True,
    )

    class Meta:
        verbose_name = _('recenzie')
        verbose_name_plural = _('recenzii')
        unique_together = ['user', 'tool']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.tool.name} ({self.rating}★)'


class FAQ(models.Model):
    """Întrebări frecvente."""

    question = models.CharField(
        _('întrebare'),
        max_length=500,
    )
    answer = models.TextField(
        _('răspuns'),
    )
    order = models.PositiveIntegerField(
        _('ordine'),
        default=0,
    )
    is_active = models.BooleanField(
        _('activă'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('data creării'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQ')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.question[:50]
