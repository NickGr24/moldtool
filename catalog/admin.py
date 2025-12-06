"""
Админка для управления каталогом инструментов.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Category, Tool, ToolImage


class ToolImageInline(admin.TabularInline):
    """Инлайн для дополнительных изображений инструмента."""
    model = ToolImage
    extra = 1
    fields = ('image', 'alt_text', 'order')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий."""

    list_display = ('name', 'slug', 'parent', 'tools_count', 'is_active', 'order')
    list_filter = ('is_active', 'parent')
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    """Админка для инструментов."""

    list_display = (
        'image_preview',
        'name',
        'category',
        'price_per_day',
        'availability',
        'quantity_available',
        'is_active',
        'is_featured',
    )
    list_display_links = ('image_preview', 'name')
    list_filter = ('category', 'availability', 'condition', 'is_active', 'is_featured')
    list_editable = ('is_active', 'is_featured', 'availability')
    search_fields = ('name', 'description', 'brand', 'model_name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'image_preview_large')
    inlines = [ToolImageInline]

    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'slug', 'category', 'description', 'short_description')
        }),
        (_('Изображение'), {
            'fields': ('image', 'image_preview_large')
        }),
        (_('Характеристики'), {
            'fields': ('brand', 'model_name', 'specifications')
        }),
        (_('Цены'), {
            'fields': ('price_per_day', 'deposit')
        }),
        (_('Статус'), {
            'fields': ('condition', 'availability', 'quantity', 'quantity_available')
        }),
        (_('Настройки'), {
            'fields': ('is_active', 'is_featured')
        }),
        (_('Статистика'), {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Превью изображения в списке."""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = _('Фото')

    def image_preview_large(self, obj):
        """Превью изображения в форме редактирования."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain;" />',
                obj.image.url
            )
        return '-'
    image_preview_large.short_description = _('Превью')


@admin.register(ToolImage)
class ToolImageAdmin(admin.ModelAdmin):
    """Админка для дополнительных изображений."""

    list_display = ('tool', 'image_preview', 'order')
    list_filter = ('tool__category',)
    search_fields = ('tool__name', 'alt_text')
    ordering = ('tool', 'order')

    def image_preview(self, obj):
        """Превью изображения."""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = _('Превью')
