from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from mailing.forms import MailingForm, MessageForm, ClientForm, MailingManagerForm
from mailing.models import Mailing, Message, Client, MailingAttempt


def home(request):
    return render(request, 'mailing/home.html')


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not (user.is_superuser or user.is_staff or obj.owner == user):
            raise PermissionDenied('У вас нет прав для просмотра этого рассылки.')
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.object.pk])

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj.owner and not (self.request.user.is_superuser or self.request.user.is_staff):
            raise PermissionDenied('У вас нет прав для редактирования этого объекта.')
        return obj

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if user.has_perm('mailing.can_view_mailing') and user.has_perm('mailing.can_mailing_is_active'):
            return MailingManagerForm
        raise PermissionDenied('У вас нет прав для выполнения этого действия.')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user != obj.owner and not user.is_superuser:
            raise PermissionDenied('У вас нет прав для удаления этого объекта.')
        return obj


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not (user.is_superuser or obj.owner == user):
            raise PermissionDenied('У вас нет прав для просмотра этого рассылки.')
        return obj


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def get_success_url(self):
        return reverse('mailing:message_detail', args=[self.object.pk])

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user != obj.owner and not user.is_superuser:
            raise PermissionDenied('У вас нет прав для редактирования этого объекта.')
        return obj


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user != obj.owner and not user.is_superuser:
            raise PermissionDenied('У вас нет прав для удаления этого объекта.')
        return obj


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not (user.is_superuser or obj.owner == user):
            raise PermissionDenied('У вас нет прав для просмотра этого рассылки.')
        return obj


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def get_success_url(self):
        return reverse('mailing:client_detail', args=[self.object.pk])

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user != obj.owner and not user.is_superuser:
            raise PermissionDenied('У вас нет прав для редактирования этого объекта.')
        return obj


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user != obj.owner and not user.is_superuser:
            raise PermissionDenied('У вас нет прав для удаления этого объекта.')
        return obj


def mailing_attempt_report(request):
    attempts = MailingAttempt.objects.all().order_by('-first_send_datetime')
    return render(request, 'mailing/report.html', {'attempts': attempts})
