"""
Формы для заявок на аренду.
"""

from datetime import date

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import RentalRequest


class RentalRequestForm(forms.ModelForm):
    """Форма создания заявки на аренду."""

    class Meta:
        model = RentalRequest
        fields = [
            'customer_name',
            'customer_email',
            'customer_phone',
            'start_date',
            'end_date',
            'comment',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+373 XX XXX XXX',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Дополнительные пожелания...',
                'rows': 3,
            }),
        }

    def clean_start_date(self):
        """Проверка даты начала."""
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < date.today():
            raise forms.ValidationError(_('Дата начала не может быть в прошлом.'))
        return start_date

    def clean(self):
        """Проверка дат."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError(_('Дата окончания должна быть позже даты начала.'))

            # Минимальный срок аренды - 1 день
            if start_date == end_date:
                pass  # 1 день - нормально

        return cleaned_data
