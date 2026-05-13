"""
Admin pentru gestionarea catalogului de scule.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Category, Tool, ToolImage, Favorite, Review, FAQ


class ToolImageInline(admin.TabularInline):
    """Inline pentru imaginile suplimentare ale sculei."""
    model = ToolImage
    extra = 1
    fields = ('image', 'alt_text', 'order')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin pentru categorii."""

    list_display = ('name', 'slug', 'parent', 'tools_count', 'is_active', 'order')
    list_filter = ('is_active', 'parent')
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    """Admin pentru scule."""

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
        (_('Informații principale'), {
            'fields': ('name', 'slug', 'category', 'description', 'short_description')
        }),
        (_('Imagine'), {
            'fields': ('image', 'image_preview_large')
        }),
        (_('Caracteristici'), {
            'fields': ('brand', 'model_name', 'specifications')
        }),
        (_('Prețuri'), {
            'fields': ('price_per_day',)
        }),
        (_('Status'), {
            'fields': ('condition', 'availability', 'quantity', 'quantity_available')
        }),
        (_('Setări'), {
            'fields': ('is_active', 'is_featured')
        }),
        (_('Statistici'), {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Previzualizarea imaginii în listă."""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = _('Foto')

    def image_preview_large(self, obj):
        """Previzualizarea imaginii în formularul de editare."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain;" />',
                obj.image.url
            )
        return '-'
    image_preview_large.short_description = _('Previzualizare')


@admin.register(ToolImage)
class ToolImageAdmin(admin.ModelAdmin):
    """Admin pentru imaginile suplimentare."""

    list_display = ('tool', 'image_preview', 'order')
    list_filter = ('tool__category',)
    search_fields = ('tool__name', 'alt_text')
    ordering = ('tool', 'order')

    def image_preview(self, obj):
        """Previzualizarea imaginii."""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = _('Previzualizare')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin pentru favorite."""

    list_display = ('user', 'tool', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'tool__name')
    raw_id_fields = ('user', 'tool')
    ordering = ('-created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin pentru recenzii."""

    list_display = ('user', 'tool', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('user__email', 'tool__name', 'text')
    raw_id_fields = ('user', 'tool')
    ordering = ('-created_at',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin pentru FAQ."""

    list_display = ('question', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')
    ordering = ('order', '-created_at')
