"""
Views для заявок на аренду.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DetailView, ListView

from catalog.models import Tool

from .forms import RentalRequestForm
from .models import RentalRequest
from .services import send_rental_confirmation_email


class CreateRentalRequestView(CreateView):
    """Создание заявки на аренду."""

    model = RentalRequest
    form_class = RentalRequestForm
    template_name = 'rentals/create_request.html'

    def get_tool(self):
        """Получает инструмент по slug из URL."""
        return get_object_or_404(
            Tool.objects.select_related('category'),
            slug=self.kwargs['tool_slug'],
            is_active=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tool'] = self.get_tool()
        return context

    def get_initial(self):
        initial = super().get_initial()
        tool = self.get_tool()
        initial['price_per_day'] = tool.price_per_day
        initial['deposit_amount'] = tool.deposit

        # Предзаполняем данные для авторизованных пользователей
        if self.request.user.is_authenticated:
            initial['customer_name'] = self.request.user.get_full_name()
            initial['customer_email'] = self.request.user.email
            initial['customer_phone'] = self.request.user.phone

        return initial

    def form_valid(self, form):
        tool = self.get_tool()

        # Проверяем доступность инструмента
        if not tool.is_available:
            messages.error(self.request, _('К сожалению, этот инструмент сейчас недоступен.'))
            return redirect('catalog:tool_detail', slug=tool.slug)

        # Устанавливаем связи
        form.instance.tool = tool
        form.instance.price_per_day = tool.price_per_day
        form.instance.deposit_amount = tool.deposit

        if self.request.user.is_authenticated:
            form.instance.user = self.request.user

        response = super().form_valid(form)

        # Отправляем email с PDF контрактом
        send_rental_confirmation_email(self.object)

        messages.success(
            self.request,
            _('Заявка #%(number)s успешно создана! Мы свяжемся с вами в ближайшее время.') % {'number': self.object.number}
        )
        return response

    def get_success_url(self):
        return reverse_lazy('rentals:request_success', kwargs={'number': self.object.number})


class RentalRequestSuccessView(DetailView):
    """Страница успешного создания заявки."""

    model = RentalRequest
    template_name = 'rentals/request_success.html'
    context_object_name = 'rental'
    slug_field = 'number'
    slug_url_kwarg = 'number'


class RentalRequestDetailView(DetailView):
    """Детальная страница заявки."""

    model = RentalRequest
    template_name = 'rentals/request_detail.html'
    context_object_name = 'rental'
    slug_field = 'number'
    slug_url_kwarg = 'number'


class UserRentalRequestsView(LoginRequiredMixin, ListView):
    """Список заявок пользователя."""

    model = RentalRequest
    template_name = 'rentals/user_requests.html'
    context_object_name = 'rentals'
    paginate_by = 10

    def get_queryset(self):
        return RentalRequest.objects.filter(
            user=self.request.user
        ).select_related('tool').order_by('-created_at')


class CancelRentalRequestView(LoginRequiredMixin, DetailView):
    """Отмена заявки пользователем."""

    model = RentalRequest
    slug_field = 'number'
    slug_url_kwarg = 'number'

    def get_queryset(self):
        return RentalRequest.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        rental = self.get_object()

        if rental.can_be_cancelled:
            rental.cancel()
            messages.success(request, _('Заявка #%(number)s успешно отменена.') % {'number': rental.number})
        else:
            messages.error(request, _('Эту заявку нельзя отменить.'))

        return redirect('rentals:user_requests')
