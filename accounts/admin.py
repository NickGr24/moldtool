"""
Admin pentru gestionarea utilizatorilor.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin pentru modelul personalizat de utilizator."""

    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'receive_notifications')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informații personale'), {'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        (_('Permisiuni'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Setări'), {'fields': ('receive_notifications',)}),
        (_('Date importante'), {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('created_at', 'last_login')
