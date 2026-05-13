"""
Views pentru catalogul de scule.
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


class CompareView(TemplateView):
    """Compararea a două scule din aceeași categorie."""

    template_name = 'catalog/compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ids_param = self.request.GET.get('ids', '')
        tool_ids = [x for x in ids_param.split(',') if x.isdigit()][:2]

        tools = list(
            Tool.objects.filter(id__in=tool_ids, is_active=True)
            .select_related('category')
        )

        context['tools'] = tools

        if len(tools) == 2:
            # Adunăm toate cheile caracteristicilor din ambele scule
            all_spec_keys = []
            seen = set()
            for tool in tools:
                for key in (tool.specifications or {}):
                    if key not in seen:
                        all_spec_keys.append(key)
                        seen.add(key)

            specs_rows = []
            for key in all_spec_keys:
                val1 = (tools[0].specifications or {}).get(key)
                val2 = (tools[1].specifications or {}).get(key)
                specs_rows.append({
                    'key': key,
                    'val1': val1 or '—',
                    'val2': val2 or '—',
                    'different': val1 != val2,
                })

            context['specs_rows'] = specs_rows
            context['same_category'] = tools[0].category_id == tools[1].category_id

        # Pentru selectarea sculei: produse din aceeași categorie
        if tools:
            category = tools[0].category
            context['category_tools'] = Tool.objects.filter(
                is_active=True, category=category,
            ).exclude(id__in=[t.id for t in tools]).order_by('name')[:20]

        return context


class CatalogView(ListView):
    """Lista tuturor sculelor."""

    model = Tool
    template_name = 'catalog/catalog.html'
    context_object_name = 'tools'
    paginate_by = 12

    def get_queryset(self):
        queryset = Tool.objects.filter(is_active=True).select_related('category')

        # Căutare
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(brand__icontains=search)
            )

        # Filtru după categorie
        category_slug = self.request.GET.get('category')
        if category_slug and category_slug != 'None':
            queryset = queryset.filter(category__slug=category_slug)

        # Filtru după disponibilitate
        availability = self.request.GET.get('availability')
        if availability:
            queryset = queryset.filter(availability=availability)

        # Filtru după preț
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

        # Sortare
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

        # Intervalul de prețuri
        price_range = Tool.objects.filter(is_active=True).aggregate(
            min_price=Min('price_per_day'),
            max_price=Max('price_per_day')
        )
        context['price_min'] = price_range['min_price'] or 0
        context['price_max'] = price_range['max_price'] or 1000
        context['current_price_min'] = self.request.GET.get('price_min', '')
        context['current_price_max'] = self.request.GET.get('price_max', '')

        # Favoritele utilizatorului
        if self.request.user.is_authenticated:
            context['favorite_ids'] = list(
                Favorite.objects.filter(user=self.request.user).values_list('tool_id', flat=True)
            )
        else:
            context['favorite_ids'] = []

        return context


class CategoryView(ListView):
    """Scule dintr-o categorie."""

    model = Tool
    template_name = 'catalog/category.html'
    context_object_name = 'tools'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)

        # Obținem sculele din categorie și subcategoriile ei
        category_ids = [self.category.id]
        category_ids.extend(
            self.category.children.filter(is_active=True).values_list('id', flat=True)
        )

        queryset = Tool.objects.filter(
            is_active=True,
            category_id__in=category_ids
        ).select_related('category')

        # Sortare
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

        # Favoritele utilizatorului
        if self.request.user.is_authenticated:
            context['favorite_ids'] = list(
                Favorite.objects.filter(user=self.request.user).values_list('tool_id', flat=True)
            )
        else:
            context['favorite_ids'] = []

        return context


class ToolDetailView(DetailView):
    """Pagina de detalii a sculei."""

    model = Tool
    template_name = 'catalog/tool_detail.html'
    context_object_name = 'tool'

    def get_queryset(self):
        return Tool.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'reviews__user')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Incrementăm contorul de vizualizări
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Scule similare
        context['related_tools'] = Tool.objects.filter(
            is_active=True,
            category=self.object.category
        ).exclude(pk=self.object.pk).order_by('-views_count')[:4]

        # Recenzii
        context['reviews'] = self.object.reviews.filter(is_approved=True).select_related('user')

        # Verificare: este la favorite?
        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(
                user=self.request.user, tool=self.object
            ).exists()
            # Verificare: a lăsat o recenzie?
            context['user_review'] = Review.objects.filter(
                user=self.request.user, tool=self.object
            ).first()
        else:
            context['is_favorite'] = False
            context['user_review'] = None

        return context


class ToggleFavoriteView(LoginRequiredMixin, View):
    """Adăugare/eliminare de la favorite (AJAX)."""

    def post(self, request, tool_id):
        tool = get_object_or_404(Tool, pk=tool_id, is_active=True)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user, tool=tool
        )

        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed', 'message': _('Eliminată de la favorite')})

        return JsonResponse({'status': 'added', 'message': _('Adăugată la favorite')})


class FavoritesListView(LoginRequiredMixin, ListView):
    """Lista sculelor favorite."""

    model = Favorite
    template_name = 'catalog/favorites.html'
    context_object_name = 'favorites'
    paginate_by = 12

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('tool', 'tool__category')


class AddReviewView(LoginRequiredMixin, View):
    """Adăugare recenzie (AJAX)."""

    def post(self, request, tool_id):
        tool = get_object_or_404(Tool, pk=tool_id, is_active=True)

        # Verificăm dacă utilizatorul a lăsat deja o recenzie
        if Review.objects.filter(user=request.user, tool=tool).exists():
            return JsonResponse({
                'status': 'error',
                'message': _('Ați lăsat deja o recenzie pentru această sculă')
            }, status=400)

        try:
            data = json.loads(request.body)
            rating = int(data.get('rating', 0))
            text = data.get('text', '').strip()

            if not 1 <= rating <= 5:
                return JsonResponse({
                    'status': 'error',
                    'message': _('Nota trebuie să fie între 1 și 5')
                }, status=400)

            review = Review.objects.create(
                user=request.user,
                tool=tool,
                rating=rating,
                text=text
            )

            return JsonResponse({
                'status': 'success',
                'message': _('Recenzia a fost adăugată'),
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
                'message': _('Date incorecte')
            }, status=400)


class FAQView(TemplateView):
    """Pagina FAQ."""

    template_name = 'catalog/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True)
        return context
