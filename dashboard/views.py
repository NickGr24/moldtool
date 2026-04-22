"""
Views для личного кабинета пользователя.
"""

from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum, Avg, F
from django.views.generic import TemplateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _

from accounts.models import User
from rentals.models import RentalRequest
from catalog.models import Tool, Favorite


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

        user_requests = RentalRequest.objects.filter(user=user)

        # Статистика заявок
        context['total_requests'] = user_requests.count()
        context['active_requests'] = context['active_orders_count']
        context['completed_requests'] = user_requests.filter(
            status=RentalRequest.Status.COMPLETED
        ).count()

        # Финансовая статистика
        financial = user_requests.exclude(
            status__in=[RentalRequest.Status.CANCELLED, RentalRequest.Status.REJECTED]
        ).aggregate(
            total_spent=Sum('total_price'),
            total_days=Sum('total_days'),
            avg_order=Avg('total_price'),
        )
        context['total_spent'] = financial['total_spent'] or 0
        context['total_rental_days'] = financial['total_days'] or 0
        context['avg_order_price'] = round(financial['avg_order'] or 0, 2)

        # Последние заявки
        context['recent_requests'] = user_requests.select_related(
            'tool'
        ).order_by('-created_at')[:5]

        # Избранные товары
        context['recent_favorites'] = Favorite.objects.filter(
            user=user
        ).select_related('tool', 'tool__category').order_by('-created_at')[:4]

        # Популярные инструменты на платформе (самые арендуемые)
        context['popular_tools'] = Tool.objects.filter(
            is_active=True,
        ).annotate(
            rentals_count=Count('rental_requests'),
        ).order_by('-rentals_count')[:6]

        # Инструменты, которые пользователь чаще всего арендует
        context['user_top_tools'] = Tool.objects.filter(
            rental_requests__user=user,
        ).annotate(
            user_rentals=Count('rental_requests'),
        ).order_by('-user_rentals')[:3]

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


class FinancialReportView(DashboardMixin, UserPassesTestMixin, TemplateView):
    """Финансовый рапорт. Доступен только администраторам."""

    template_name = 'dashboard/financial_report.html'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        # Аноним — на логин; авторизованный без прав — 403.
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'financial'

        # Мок-данные: помесячная выручка
        context['monthly_revenue'] = [
            {'month': 'Octombrie 2025', 'revenue': Decimal('12450.00'), 'orders': 18, 'avg_check': Decimal('691.67')},
            {'month': 'Noiembrie 2025', 'revenue': Decimal('15800.00'), 'orders': 23, 'avg_check': Decimal('686.96')},
            {'month': 'Decembrie 2025', 'revenue': Decimal('9200.00'), 'orders': 12, 'avg_check': Decimal('766.67')},
            {'month': 'Ianuarie 2026', 'revenue': Decimal('18350.00'), 'orders': 27, 'avg_check': Decimal('679.63')},
            {'month': 'Februarie 2026', 'revenue': Decimal('21600.00'), 'orders': 31, 'avg_check': Decimal('696.77')},
            {'month': 'Martie 2026', 'revenue': Decimal('8900.00'), 'orders': 14, 'avg_check': Decimal('635.71')},
        ]

        # Мок-данные: топ инструменты по доходу
        context['top_tools_revenue'] = [
            {'name': 'Perforator Bosch GBH 2-26', 'revenue': Decimal('8450.00'), 'rentals': 42, 'percent': 100},
            {'name': 'Betonieră 180L', 'revenue': Decimal('7200.00'), 'rentals': 18, 'percent': 85},
            {'name': 'Polizor unghiular Makita', 'revenue': Decimal('5800.00'), 'rentals': 58, 'percent': 69},
            {'name': 'Generator 5kW', 'revenue': Decimal('5100.00'), 'rentals': 12, 'percent': 60},
            {'name': 'Compresor 50L', 'revenue': Decimal('4350.00'), 'rentals': 29, 'percent': 51},
        ]

        # Мок-данные: статусы заказов
        context['orders_by_status'] = [
            {'status': 'Confirmate', 'count': 34, 'color': 'green'},
            {'status': 'În așteptare', 'count': 8, 'color': 'yellow'},
            {'status': 'În desfășurare', 'count': 12, 'color': 'blue'},
            {'status': 'Finalizate', 'count': 89, 'color': 'gray'},
            {'status': 'Anulate', 'count': 7, 'color': 'red'},
        ]

        # Мок-данные: сводка
        context['summary'] = {
            'total_revenue': Decimal('86300.00'),
            'total_orders': 125,
            'avg_order_value': Decimal('690.40'),
            'total_rental_days': 847,
            'outstanding_deposits': Decimal('4200.00'),
            'growth_percent': 12.5,
        }

        # Мок-данные: последние транзакции
        context['recent_transactions'] = [
            {'date': '07.03.2026', 'client': 'Ion Popescu', 'tool': 'Perforator Bosch GBH 2-26', 'amount': Decimal('450.00'), 'status': 'paid'},
            {'date': '06.03.2026', 'client': 'Maria Ionescu', 'tool': 'Betonieră 180L', 'amount': Decimal('1200.00'), 'status': 'paid'},
            {'date': '05.03.2026', 'client': 'Andrei Rusu', 'tool': 'Generator 5kW', 'amount': Decimal('850.00'), 'status': 'pending'},
            {'date': '04.03.2026', 'client': 'Elena Moraru', 'tool': 'Polizor unghiular Makita', 'amount': Decimal('300.00'), 'status': 'paid'},
            {'date': '03.03.2026', 'client': 'Victor Ceban', 'tool': 'Compresor 50L', 'amount': Decimal('600.00'), 'status': 'pending'},
            {'date': '02.03.2026', 'client': 'Ana Stratulat', 'tool': 'Perforator Bosch GBH 2-26', 'amount': Decimal('450.00'), 'status': 'paid'},
        ]

        return context
