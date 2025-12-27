"""
Views для каталога инструментов.
"""

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Min, Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Tool, Favorite, Review, FAQ


class CatalogView(ListView):
    """Список всех инструментов."""

    model = Tool
    template_name = 'catalog/catalog.html'
    context_object_name = 'tools'
    paginate_by = 12

    def get_queryset(self):
        queryset = Tool.objects.filter(is_active=True).select_related('category')

        # Поиск
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(brand__icontains=search)
            )

        # Фильтр по категории
        category_slug = self.request.GET.get('category')
        if category_slug and category_slug != 'None':
            queryset = queryset.filter(category__slug=category_slug)

        # Фильтр по доступности
        availability = self.request.GET.get('availability')
        if availability:
            queryset = queryset.filter(availability=availability)

        # Фильтр по цене
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min:
            try:
                queryset = queryset.filter(price_per_day__gte=float(price_min))
            except ValueError:
                pass
        if price_max:
            try:
                queryset = queryset.filter(price_per_day__lte=float(price_max))
            except ValueError:
                pass

        # Сортировка
        sort = self.request.GET.get('sort', '-created_at')
        if sort == 'price_asc':
            queryset = queryset.order_by('price_per_day')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price_per_day')
        elif sort == 'name':
            queryset = queryset.order_by('name')
        elif sort == 'popular':
            queryset = queryset.order_by('-views_count')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['current_category'] = self.request.GET.get('category')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        context['search_query'] = self.request.GET.get('q', '')

        # Диапазон цен
        price_range = Tool.objects.filter(is_active=True).aggregate(
            min_price=Min('price_per_day'),
            max_price=Max('price_per_day')
        )
        context['price_min'] = price_range['min_price'] or 0
        context['price_max'] = price_range['max_price'] or 1000
        context['current_price_min'] = self.request.GET.get('price_min', '')
        context['current_price_max'] = self.request.GET.get('price_max', '')

        # Избранное пользователя
        if self.request.user.is_authenticated:
            context['favorite_ids'] = list(
                Favorite.objects.filter(user=self.request.user).values_list('tool_id', flat=True)
            )
        else:
            context['favorite_ids'] = []

        return context


class CategoryView(ListView):
    """Инструменты в категории."""

    model = Tool
    template_name = 'catalog/category.html'
    context_object_name = 'tools'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)

        # Получаем инструменты из категории и её подкатегорий
        category_ids = [self.category.id]
        category_ids.extend(
            self.category.children.filter(is_active=True).values_list('id', flat=True)
        )

        queryset = Tool.objects.filter(
            is_active=True,
            category_id__in=category_ids
        ).select_related('category')

        # Сортировка
        sort = self.request.GET.get('sort', '-created_at')
        if sort == 'price_asc':
            queryset = queryset.order_by('price_per_day')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price_per_day')
        elif sort == 'name':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['subcategories'] = self.category.children.filter(is_active=True)
        context['current_sort'] = self.request.GET.get('sort', '-created_at')

        # Избранное пользователя
        if self.request.user.is_authenticated:
            context['favorite_ids'] = list(
                Favorite.objects.filter(user=self.request.user).values_list('tool_id', flat=True)
            )
        else:
            context['favorite_ids'] = []

        return context


class ToolDetailView(DetailView):
    """Детальная страница инструмента."""

    model = Tool
    template_name = 'catalog/tool_detail.html'
    context_object_name = 'tool'

    def get_queryset(self):
        return Tool.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'reviews__user')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Увеличиваем счётчик просмотров
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Похожие инструменты
        context['related_tools'] = Tool.objects.filter(
            is_active=True,
            category=self.object.category
        ).exclude(pk=self.object.pk).order_by('-views_count')[:4]

        # Отзывы
        context['reviews'] = self.object.reviews.filter(is_approved=True).select_related('user')

        # Проверка: в избранном ли
        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(
                user=self.request.user, tool=self.object
            ).exists()
            # Проверка: оставлял ли отзыв
            context['user_review'] = Review.objects.filter(
                user=self.request.user, tool=self.object
            ).first()
        else:
            context['is_favorite'] = False
            context['user_review'] = None

        return context


class ToggleFavoriteView(LoginRequiredMixin, View):
    """Добавление/удаление из избранного (AJAX)."""

    def post(self, request, tool_id):
        tool = get_object_or_404(Tool, pk=tool_id, is_active=True)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user, tool=tool
        )

        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed', 'message': _('Удалено из избранного')})

        return JsonResponse({'status': 'added', 'message': _('Добавлено в избранное')})


class FavoritesListView(LoginRequiredMixin, ListView):
    """Список избранных инструментов."""

    model = Favorite
    template_name = 'catalog/favorites.html'
    context_object_name = 'favorites'
    paginate_by = 12

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('tool', 'tool__category')


class AddReviewView(LoginRequiredMixin, View):
    """Добавление отзыва (AJAX)."""

    def post(self, request, tool_id):
        tool = get_object_or_404(Tool, pk=tool_id, is_active=True)

        # Проверяем, не оставлял ли уже отзыв
        if Review.objects.filter(user=request.user, tool=tool).exists():
            return JsonResponse({
                'status': 'error',
                'message': _('Вы уже оставляли отзыв для этого инструмента')
            }, status=400)

        try:
            data = json.loads(request.body)
            rating = int(data.get('rating', 0))
            text = data.get('text', '').strip()

            if not 1 <= rating <= 5:
                return JsonResponse({
                    'status': 'error',
                    'message': _('Рейтинг должен быть от 1 до 5')
                }, status=400)

            review = Review.objects.create(
                user=request.user,
                tool=tool,
                rating=rating,
                text=text
            )

            return JsonResponse({
                'status': 'success',
                'message': _('Отзыв добавлен'),
                'review': {
                    'id': review.id,
                    'rating': review.rating,
                    'text': review.text,
                    'user_name': request.user.get_short_name(),
                    'created_at': review.created_at.strftime('%d.%m.%Y')
                }
            })
        except (json.JSONDecodeError, ValueError) as e:
            return JsonResponse({
                'status': 'error',
                'message': _('Неверные данные')
            }, status=400)


class FAQView(TemplateView):
    """Страница FAQ."""

    template_name = 'catalog/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True)
        return context
