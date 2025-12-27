"""
Custom allauth adapters for MoldTool.
"""

import logging
from django.conf import settings

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


logger = logging.getLogger(__name__)


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for django-allauth account operations.
    """

    def is_open_for_signup(self, request):
        """Check if registration is open."""
        return getattr(settings, 'ACCOUNT_ALLOW_SIGNUPS', True)

    def get_login_redirect_url(self, request):
        """Return URL to redirect to after successful login."""
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url and self.is_safe_url(next_url):
            return next_url
        return '/'

    def get_signup_redirect_url(self, request):
        """Return URL to redirect to after successful signup."""
        return '/'

    def get_email_verification_redirect_url(self, request, email_address):
        """Redirect URL after email verification."""
        return '/'

    def is_safe_url(self, url):
        """Check if URL is safe for redirects."""
        if not url:
            return False
        from django.utils.http import url_has_allowed_host_and_scheme
        return url_has_allowed_host_and_scheme(
            url,
            allowed_hosts={request.get_host() for request in []} if False else None,
            require_https=False
        )


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for social account (OAuth) operations.
    """

    def is_open_for_signup(self, request, sociallogin):
        """Check if social signup is allowed."""
        return getattr(settings, 'SOCIALACCOUNT_ALLOW_SIGNUPS', True)

    def get_connect_redirect_url(self, request, socialaccount):
        """Return URL to redirect to after connecting social account."""
        return '/'
