"""
Админка для управления заявками на аренду.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import RentalRequest


@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
    """Админка для заявок на аренду."""

    list_display = (
        'number',
        'tool',
        'customer_name',
        'customer_phone',
        'start_date',
        'end_date',
        'total_days',
        'total_price_display',
        'status_badge',
        'created_at',
    )
    list_filter = ('status', 'created_at', 'start_date', 'tool__category')
    search_fields = ('number', 'customer_name', 'customer_email', 'customer_phone', 'tool__name')
    readonly_fields = ('number', 'total_days', 'total_price', 'created_at', 'updated_at', 'confirmed_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        (_('Информация о заявке'), {
            'fields': ('number', 'status', 'tool')
        }),
        (_('Данные клиента'), {
            'fields': ('user', 'customer_name', 'customer_email', 'customer_phone')
        }),
        (_('Период аренды'), {
            'fields': ('start_date', 'end_date', 'total_days')
        }),
        (_('Финансы'), {
            'fields': ('price_per_day', 'total_price', 'deposit_amount')
        }),
        (_('Комментарии'), {
            'fields': ('comment', 'admin_notes'),
            'classes': ('collapse',)
        }),
        (_('Системная информация'), {
            'fields': ('created_at', 'updated_at', 'confirmed_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['confirm_requests', 'reject_requests', 'cancel_requests']

    def status_badge(self, obj):
        """Отображает статус с цветовой меткой."""
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
    status_badge.short_description = _('Статус')

    def total_price_display(self, obj):
        """Отображает стоимость с валютой."""
        return f'{obj.total_price} MDL'
    total_price_display.short_description = _('Сумма')

    @admin.action(description=_('Подтвердить выбранные заявки'))
    def confirm_requests(self, request, queryset):
        """Подтверждает выбранные заявки."""
        count = 0
        for rental in queryset.filter(status=RentalRequest.Status.PENDING):
            rental.confirm()
            count += 1
        self.message_user(request, _(f'Подтверждено заявок: {count}'))

    @admin.action(description=_('Отклонить выбранные заявки'))
    def reject_requests(self, request, queryset):
        """Отклоняет выбранные заявки."""
        count = 0
        for rental in queryset.filter(status=RentalRequest.Status.PENDING):
            rental.reject()
            count += 1
        self.message_user(request, _(f'Отклонено заявок: {count}'))

    @admin.action(description=_('Отменить выбранные заявки'))
    def cancel_requests(self, request, queryset):
        """Отменяет выбранные заявки."""
        count = 0
        for rental in queryset.filter(status__in=[RentalRequest.Status.PENDING, RentalRequest.Status.CONFIRMED]):
            rental.cancel()
            count += 1
        self.message_user(request, _(f'Отменено заявок: {count}'))
