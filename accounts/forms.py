"""
Custom authentication forms for MoldTool.
Extends django-allauth forms with styling.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm


class CustomSignupForm(SignupForm):
    """
    Simple registration form - just email and password.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Style email field
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({
                'class': 'w-full px-4 py-3 bg-dark-200 border border-dark-border rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-brand-yellow focus:ring-1 focus:ring-brand-yellow transition-colors',
                'placeholder': _('example@email.com'),
                'autocomplete': 'email',
            })
            self.fields['email'].label = _("Email")

        # Style password fields
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'class': 'w-full px-4 py-3 bg-dark-200 border border-dark-border rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-brand-yellow focus:ring-1 focus:ring-brand-yellow transition-colors',
                'placeholder': _('Creați o parolă'),
                'autocomplete': 'new-password',
            })
            self.fields['password1'].label = _("Parolă")

        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'class': 'w-full px-4 py-3 bg-dark-200 border border-dark-border rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-brand-yellow focus:ring-1 focus:ring-brand-yellow transition-colors',
                'placeholder': _('Repetați parola'),
                'autocomplete': 'new-password',
            })
            self.fields['password2'].label = _("Confirmați parola")


class CustomLoginForm(LoginForm):
    """
    Styled login form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'login' in self.fields:
            self.fields['login'].widget.attrs.update({
                'class': 'w-full px-4 py-3 bg-dark-200 border border-dark-border rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-brand-yellow focus:ring-1 focus:ring-brand-yellow transition-colors',
                'placeholder': _('example@email.com'),
                'autocomplete': 'email',
            })
            self.fields['login'].label = _("Email")

        if 'password' in self.fields:
            self.fields['password'].widget.attrs.update({
                'class': 'w-full px-4 py-3 bg-dark-200 border border-dark-border rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-brand-yellow focus:ring-1 focus:ring-brand-yellow transition-colors',
                'placeholder': _('Introduceți parola'),
                'autocomplete': 'current-password',
            })
            self.fields['password'].label = _("Parolă")

        if 'remember' in self.fields:
            self.fields['remember'].widget.attrs.update({
                'class': 'w-5 h-5 rounded border-dark-border bg-dark-200 text-brand-yellow focus:ring-brand-yellow focus:ring-offset-0 cursor-pointer',
            })
            self.fields['remember'].label = _("Ține-mă minte")


class CustomResetPasswordForm(ResetPasswordForm):
    """
    Styled password reset form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({
                'class': 'w-full px-4 py-3 bg-dark-200 border border-dark-border rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-brand-yellow focus:ring-1 focus:ring-brand-yellow transition-colors',
                'placeholder': _('Introduceți email pentru recuperare'),
                'autocomplete': 'email',
            })
            self.fields['email'].label = _("Email")
