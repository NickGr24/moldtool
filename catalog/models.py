"""
Модели каталога инструментов для платформы MoldTool.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Категория инструментов."""

    name = models.CharField(
        _('название'),
        max_length=100,
    )
    slug = models.SlugField(
        _('URL'),
        max_length=100,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        _('описание'),
        blank=True,
    )
    image = models.ImageField(
        _('изображение'),
        upload_to='categories/',
        blank=True,
        null=True,
    )
    icon = models.CharField(
        _('CSS-класс иконки'),
        max_length=50,
        blank=True,
        help_text=_('Например: icon-drill, icon-hammer'),
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('родительская категория'),
    )
    is_active = models.BooleanField(
        _('активна'),
        default=True,
    )
    order = models.PositiveIntegerField(
        _('порядок сортировки'),
        default=0,
    )
    created_at = models.DateTimeField(
        _('дата создания'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')
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
        """Количество активных инструментов в категории."""
        return self.tools.filter(is_active=True).count()


class Tool(models.Model):
    """Инструмент для аренды."""

    class Condition(models.TextChoices):
        NEW = 'new', _('Новый')
        EXCELLENT = 'excellent', _('Отличное')
        GOOD = 'good', _('Хорошее')
        FAIR = 'fair', _('Удовлетворительное')

    class Availability(models.TextChoices):
        AVAILABLE = 'available', _('Доступен')
        RENTED = 'rented', _('В аренде')
        MAINTENANCE = 'maintenance', _('На обслуживании')
        UNAVAILABLE = 'unavailable', _('Недоступен')

    # Основная информация
    name = models.CharField(
        _('название'),
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
        verbose_name=_('категория'),
    )
    description = models.TextField(
        _('описание'),
    )
    short_description = models.CharField(
        _('краткое описание'),
        max_length=300,
        blank=True,
    )

    # Изображения
    image = models.ImageField(
        _('основное изображение'),
        upload_to='tools/',
    )

    # Характеристики
    brand = models.CharField(
        _('бренд'),
        max_length=100,
        blank=True,
    )
    model_name = models.CharField(
        _('модель'),
        max_length=100,
        blank=True,
    )
    specifications = models.JSONField(
        _('характеристики'),
        default=dict,
        blank=True,
        help_text=_('Технические характеристики в формате JSON'),
    )

    # Цены
    price_per_day = models.DecimalField(
        _('цена за день'),
        max_digits=10,
        decimal_places=2,
    )
    deposit = models.DecimalField(
        _('залог'),
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # Статус
    condition = models.CharField(
        _('состояние'),
        max_length=20,
        choices=Condition.choices,
        default=Condition.EXCELLENT,
    )
    availability = models.CharField(
        _('доступность'),
        max_length=20,
        choices=Availability.choices,
        default=Availability.AVAILABLE,
    )
    quantity = models.PositiveIntegerField(
        _('количество'),
        default=1,
    )
    quantity_available = models.PositiveIntegerField(
        _('доступное количество'),
        default=1,
    )

    # Метаданные
    is_active = models.BooleanField(
        _('активен'),
        default=True,
    )
    is_featured = models.BooleanField(
        _('рекомендуемый'),
        default=False,
    )
    views_count = models.PositiveIntegerField(
        _('количество просмотров'),
        default=0,
    )
    created_at = models.DateTimeField(
        _('дата добавления'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('дата обновления'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('инструмент')
        verbose_name_plural = _('инструменты')
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
        """Проверяет, доступен ли инструмент для аренды."""
        return (
            self.is_active
            and self.availability == self.Availability.AVAILABLE
            and self.quantity_available > 0
        )

    def increment_views(self):
        """Увеличивает счётчик просмотров."""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ToolImage(models.Model):
    """Дополнительные изображения инструмента."""

    tool = models.ForeignKey(
        Tool,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('инструмент'),
    )
    image = models.ImageField(
        _('изображение'),
        upload_to='tools/gallery/',
    )
    alt_text = models.CharField(
        _('альтернативный текст'),
        max_length=200,
        blank=True,
    )
    order = models.PositiveIntegerField(
        _('порядок'),
        default=0,
    )

    class Meta:
        verbose_name = _('изображение инструмента')
        verbose_name_plural = _('изображения инструментов')
        ordering = ['order']

    def __str__(self):
        return f'{self.tool.name} - изображение {self.order}'
