"""
Formulare pentru cererile de închiriere.
"""

from datetime import date

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import RentalRequest


class RentalRequestForm(forms.ModelForm):
    """Formular pentru crearea unei cereri de închiriere."""

    class Meta:
        model = RentalRequest
        fields = [
            'customer_name',
            'customer_email',
            'customer_phone',
            'start_date',
            'end_date',
            'delivery_method',
            'delivery_address',
            'comment',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Numele dumneavoastră'),
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('email@example.com'),
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('+373 XX XXX XXX'),
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'delivery_method': forms.RadioSelect(),
            'delivery_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Strada, casa, apartamentul, orașul'),
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Dorințe suplimentare...'),
                'rows': 3,
            }),
        }

    def clean_start_date(self):
        """Validarea datei de început."""
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < date.today():
            raise forms.ValidationError(_('Data de început nu poate fi în trecut.'))
        return start_date

    def clean(self):
        """Validarea datelor și a adresei de livrare."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError(_('Data de sfârșit trebuie să fie ulterioară datei de început.'))

            # Termenul minim de închiriere - 1 zi
            if start_date == end_date:
                pass  # 1 zi - este în regulă

        # La livrare adresa este obligatorie
        delivery_method = cleaned_data.get('delivery_method')
        delivery_address = (cleaned_data.get('delivery_address') or '').strip()
        if delivery_method == RentalRequest.DeliveryMethod.DELIVERY and not delivery_address:
            self.add_error(
                'delivery_address',
                _('Indicați adresa de livrare.'),
            )

        return cleaned_data
