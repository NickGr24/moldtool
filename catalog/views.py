"""
Views для каталога инструментов.
"""

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Category, Tool


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
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Фильтр по доступности
        availability = self.request.GET.get('availability')
        if availability:
            queryset = queryset.filter(availability=availability)

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
        return context


class ToolDetailView(DetailView):
    """Детальная страница инструмента."""

    model = Tool
    template_name = 'catalog/tool_detail.html'
    context_object_name = 'tool'

    def get_queryset(self):
        return Tool.objects.filter(is_active=True).select_related('category').prefetch_related('images')

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

        return context
