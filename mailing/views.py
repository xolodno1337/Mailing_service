from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from mailing.models import Mailing


def home(request):
    return render(request, 'mailing/home.html')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_list.html'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'


class MailingCreateView(CreateView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
