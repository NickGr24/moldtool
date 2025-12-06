"""
Views для главной страницы и статических страниц.
"""

from django.views.generic import TemplateView

from catalog.models import Category, Tool


class HomeView(TemplateView):
    """Главная страница."""

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем активные категории
        context['categories'] = Category.objects.filter(
            is_active=True,
            parent__isnull=True  # Только родительские категории
        ).order_by('order', 'name')[:8]

        # Получаем рекомендуемые инструменты
        context['featured_tools'] = Tool.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category').order_by('-created_at')[:8]

        # Если рекомендуемых нет, показываем последние добавленные
        if not context['featured_tools'].exists():
            context['featured_tools'] = Tool.objects.filter(
                is_active=True
            ).select_related('category').order_by('-created_at')[:8]

        return context
