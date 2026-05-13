"""
Admin pentru gestionarea cererilor de închiriere.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import RentalRequest


@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
    """Admin pentru cererile de închiriere."""

    list_display = (
        'number',
        'tool',
        'customer_name',
        'customer_phone',
        'start_date',
        'end_date',
        'total_days',
        'total_price_display',
        'delivery_method',
        'status_badge',
        'created_at',
    )
    list_filter = ('status', 'delivery_method', 'created_at', 'start_date', 'tool__category')
    search_fields = ('number', 'customer_name', 'customer_email', 'customer_phone', 'tool__name')
    readonly_fields = ('number', 'total_days', 'total_price', 'delivery_price', 'created_at', 'updated_at', 'confirmed_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        (_('Informații despre cerere'), {
            'fields': ('number', 'status', 'tool')
        }),
        (_('Date client'), {
            'fields': ('user', 'customer_name', 'customer_email', 'customer_phone')
        }),
        (_('Perioada de închiriere'), {
            'fields': ('start_date', 'end_date', 'total_days')
        }),
        (_('Livrare'), {
            'fields': ('delivery_method', 'delivery_address', 'delivery_price')
        }),
        (_('Finanțe'), {
            'fields': ('price_per_day', 'total_price')
        }),
        (_('Comentarii'), {
            'fields': ('comment', 'admin_notes'),
            'classes': ('collapse',)
        }),
        (_('Informații de sistem'), {
            'fields': ('created_at', 'updated_at', 'confirmed_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['confirm_requests', 'reject_requests', 'cancel_requests']

    def status_badge(self, obj):
        """Afișează statusul cu o etichetă colorată."""
        colors = {
            'pending': '#FFA500',
            'confirmed': '#4CAF50',
            'in_progress': '#2196F3',
            'completed': '#9E9E9E',
            'cancelled': '#F44336',
            'rejected': '#F44336',
        }
        color = colors.get(obj.status, '#9E9E9E')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = _('Status')

    def total_price_display(self, obj):
        """Afișează suma cu moneda."""
        return f'{obj.total_price} MDL'
    total_price_display.short_description = _('Sumă')

    @admin.action(description=_('Confirmă cererile selectate'))
    def confirm_requests(self, request, queryset):
        """Confirmă cererile selectate."""
        count = 0
        for rental in queryset.filter(status=RentalRequest.Status.PENDING):
            rental.confirm()
            count += 1
        self.message_user(request, _(f'Cereri confirmate: {count}'))

    @admin.action(description=_('Respinge cererile selectate'))
    def reject_requests(self, request, queryset):
        """Respinge cererile selectate."""
        count = 0
        for rental in queryset.filter(status=RentalRequest.Status.PENDING):
            rental.reject()
            count += 1
        self.message_user(request, _(f'Cereri respinse: {count}'))

    @admin.action(description=_('Anulează cererile selectate'))
    def cancel_requests(self, request, queryset):
        """Anulează cererile selectate."""
        count = 0
        for rental in queryset.filter(status__in=[RentalRequest.Status.PENDING, RentalRequest.Status.CONFIRMED]):
            rental.cancel()
            count += 1
        self.message_user(request, _(f'Cereri anulate: {count}'))
