"""
Views для личного кабинета пользователя.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from accounts.models import User
from rentals.models import RentalRequest


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    """Главная страница личного кабинета."""

    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Статистика заявок
        context['total_requests'] = RentalRequest.objects.filter(user=user).count()
        context['active_requests'] = RentalRequest.objects.filter(
            user=user,
            status__in=[RentalRequest.Status.PENDING, RentalRequest.Status.CONFIRMED, RentalRequest.Status.IN_PROGRESS]
        ).count()
        context['completed_requests'] = RentalRequest.objects.filter(
            user=user,
            status=RentalRequest.Status.COMPLETED
        ).count()

        # Последние заявки
        context['recent_requests'] = RentalRequest.objects.filter(
            user=user
        ).select_related('tool').order_by('-created_at')[:5]

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля."""

    model = User
    template_name = 'dashboard/profile.html'
    fields = ['first_name', 'last_name', 'phone', 'avatar', 'receive_notifications']
    success_url = reverse_lazy('dashboard:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлён.')
        return super().form_valid(form)
