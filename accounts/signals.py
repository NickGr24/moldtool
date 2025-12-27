"""
Signal handlers for authentication events.
Provides audit logging and custom behavior for auth events.
"""

import logging
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from allauth.account.signals import (
    user_signed_up,
    email_confirmed,
    password_changed,
    password_reset,
    email_added,
    email_removed,
)
from allauth.socialaccount.signals import (
    social_account_added,
    social_account_removed,
)


logger = logging.getLogger('accounts.auth')
User = get_user_model()


def get_client_ip(request):
    """Extract client IP from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def get_user_agent(request):
    """Extract user agent from request."""
    return request.META.get('HTTP_USER_AGENT', 'unknown')[:200]


# ============================================
# DJANGO AUTH SIGNALS
# ============================================

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log successful login."""
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    logger.info(
        f"LOGIN_SUCCESS | user={user.email} | ip={ip} | ua={ua}"
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log logout."""
    if user:
        ip = get_client_ip(request)
        logger.info(f"LOGOUT | user={user.email} | ip={ip}")


@receiver(user_login_failed)
def log_login_failed(sender, credentials, request=None, **kwargs):
    """Log failed login attempts."""
    email = credentials.get('email', credentials.get('username', 'unknown'))
    ip = get_client_ip(request) if request else 'unknown'
    logger.warning(
        f"LOGIN_FAILED | email={email} | ip={ip}"
    )


# ============================================
# ALLAUTH ACCOUNT SIGNALS
# ============================================

@receiver(user_signed_up)
def log_user_signup(request, user, **kwargs):
    """Log new user registration."""
    ip = get_client_ip(request)
    ua = get_user_agent(request)

    logger.info(
        f"SIGNUP | user={user.email} | name={user.get_full_name()} | ip={ip}"
    )

    # Could send welcome email, create related objects, etc.


@receiver(email_confirmed)
def log_email_confirmed(request, email_address, **kwargs):
    """Log email confirmation."""
    ip = get_client_ip(request)
    logger.info(
        f"EMAIL_CONFIRMED | email={email_address.email} | user={email_address.user.email} | ip={ip}"
    )


@receiver(password_changed)
def log_password_changed(request, user, **kwargs):
    """Log password change."""
    ip = get_client_ip(request)
    logger.info(
        f"PASSWORD_CHANGED | user={user.email} | ip={ip}"
    )


@receiver(password_reset)
def log_password_reset(request, user, **kwargs):
    """Log password reset."""
    ip = get_client_ip(request)
    logger.info(
        f"PASSWORD_RESET | user={user.email} | ip={ip}"
    )


@receiver(email_added)
def log_email_added(request, user, email_address, **kwargs):
    """Log new email added to account."""
    ip = get_client_ip(request)
    logger.info(
        f"EMAIL_ADDED | user={user.email} | new_email={email_address.email} | ip={ip}"
    )


@receiver(email_removed)
def log_email_removed(request, user, email_address, **kwargs):
    """Log email removed from account."""
    ip = get_client_ip(request)
    logger.info(
        f"EMAIL_REMOVED | user={user.email} | removed_email={email_address.email} | ip={ip}"
    )


# ============================================
# ALLAUTH SOCIAL SIGNALS
# ============================================

@receiver(social_account_added)
def log_social_account_added(request, sociallogin, **kwargs):
    """Log social account connection."""
    ip = get_client_ip(request)
    user = sociallogin.user
    provider = sociallogin.account.provider

    logger.info(
        f"SOCIAL_CONNECTED | user={user.email} | provider={provider} | ip={ip}"
    )


@receiver(social_account_removed)
def log_social_account_removed(request, socialaccount, **kwargs):
    """Log social account disconnection."""
    ip = get_client_ip(request)
    user = socialaccount.user
    provider = socialaccount.provider

    logger.info(
        f"SOCIAL_DISCONNECTED | user={user.email} | provider={provider} | ip={ip}"
    )
