"""
Views для личного кабинета пользователя.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _

from accounts.models import User
from rentals.models import RentalRequest
from catalog.models import Favorite


class DashboardMixin(LoginRequiredMixin):
    """Миксин для добавления общего контекста в личный кабинет."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Счётчики для sidebar
        context['active_orders_count'] = RentalRequest.objects.filter(
            user=user,
            status__in=[RentalRequest.Status.PENDING, RentalRequest.Status.CONFIRMED, RentalRequest.Status.IN_PROGRESS]
        ).count()
        context['favorites_count'] = Favorite.objects.filter(user=user).count()

        return context


class DashboardIndexView(DashboardMixin, TemplateView):
    """Главная страница личного кабинета."""

    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'overview'
        user = self.request.user

        # Статистика заявок
        context['total_requests'] = RentalRequest.objects.filter(user=user).count()
        context['active_requests'] = context['active_orders_count']
        context['completed_requests'] = RentalRequest.objects.filter(
            user=user,
            status=RentalRequest.Status.COMPLETED
        ).count()

        # Последние заявки
        context['recent_requests'] = RentalRequest.objects.filter(
            user=user
        ).select_related('tool').order_by('-created_at')[:5]

        # Избранные товары
        context['recent_favorites'] = Favorite.objects.filter(
            user=user
        ).select_related('tool', 'tool__category').order_by('-created_at')[:4]

        return context


class OrdersListView(DashboardMixin, ListView):
    """Список заказов пользователя."""

    model = RentalRequest
    template_name = 'dashboard/orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = RentalRequest.objects.filter(
            user=self.request.user
        ).select_related('tool').order_by('-created_at')

        # Фильтр по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'orders'
        context['current_status'] = self.request.GET.get('status', '')
        context['statuses'] = RentalRequest.Status.choices
        return context


class FavoritesListView(DashboardMixin, ListView):
    """Список избранных инструментов."""

    model = Favorite
    template_name = 'dashboard/favorites.html'
    context_object_name = 'favorites'
    paginate_by = 12

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('tool', 'tool__category').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'favorites'
        return context


class ProfileUpdateView(DashboardMixin, UpdateView):
    """Редактирование профиля."""

    model = User
    template_name = 'dashboard/profile.html'
    fields = ['first_name', 'last_name', 'phone', 'avatar', 'receive_notifications']
    success_url = reverse_lazy('dashboard:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'profile'
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Профиль успешно обновлён.'))
        return super().form_valid(form)
