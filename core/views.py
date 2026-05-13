"""
Views pentru pagina principală și paginile statice.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from datetime import timedelta

from catalog.models import Category, Tool, Favorite, Review
from accounts.models import User


class HomeView(TemplateView):
    """Pagina principală."""

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obținem categoriile active
        context['categories'] = Category.objects.filter(
            is_active=True,
            parent__isnull=True  # Doar categoriile părinte
        ).order_by('order', 'name')[:8]

        # Obținem uneltele recomandate
        context['featured_tools'] = Tool.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category').order_by('-created_at')[:8]

        # Dacă nu există recomandate, afișăm ultimele adăugate
        if not context['featured_tools'].exists():
            context['featured_tools'] = Tool.objects.filter(
                is_active=True
            ).select_related('category').order_by('-created_at')[:8]

        return context


class ContactsView(TemplateView):
    """Pagina de contacte."""

    template_name = 'core/contacts.html'


class AboutView(TemplateView):
    """Pagina despre noi."""

    template_name = 'core/about.html'


@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(TemplateView):
    """Mini panou de admin cu statistici."""

    template_name = 'core/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        last_week = today - timedelta(days=7)
        last_month = today - timedelta(days=30)

        # Statistici generale
        context['total_tools'] = Tool.objects.count()
        context['active_tools'] = Tool.objects.filter(is_active=True).count()
        context['available_tools'] = Tool.objects.filter(
            is_active=True, availability='available'
        ).count()
        context['total_users'] = User.objects.count()
        context['total_reviews'] = Review.objects.count()
        context['pending_reviews'] = Review.objects.filter(is_approved=False).count()
        context['total_favorites'] = Favorite.objects.count()
        context['total_categories'] = Category.objects.filter(is_active=True).count()

        # Noi în ultima săptămână
        context['new_users_week'] = User.objects.filter(
            created_at__date__gte=last_week
        ).count()
        context['new_reviews_week'] = Review.objects.filter(
            created_at__date__gte=last_week
        ).count()

        # Unelte populare
        context['popular_tools'] = Tool.objects.filter(
            is_active=True
        ).order_by('-views_count')[:5]

        # Recenzii recente
        context['recent_reviews'] = Review.objects.select_related(
            'user', 'tool'
        ).order_by('-created_at')[:5]

        # Uneltele cu cele mai multe favorite
        context['most_favorited'] = Tool.objects.filter(
            is_active=True
        ).annotate(
            favorites_count=Count('favorited_by')
        ).order_by('-favorites_count')[:5]

        # Statistici pe categorii
        context['category_stats'] = Category.objects.filter(
            is_active=True
        ).annotate(
            num_tools=Count('tools', filter=models.Q(tools__is_active=True))
        ).order_by('-num_tools')[:5]

        # Rating mediu pentru toate uneltele
        avg_rating = Review.objects.filter(is_approved=True).aggregate(
            avg=Avg('rating')
        )['avg']
        context['average_rating'] = round(avg_rating, 1) if avg_rating else 0

        return context


class PrivacyPolicyView(TemplateView):
    """Politica de Confidențialitate."""

    template_name = 'core/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_date'] = timezone.now()
        return context


class TermsConditionsView(TemplateView):
    """Termeni și Condiții."""

    template_name = 'core/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_date'] = timezone.now()
        return context
