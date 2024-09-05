from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'body', 'image_blog']
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        blog = form.save()
        user = self.request.user
        blog.owner = user
        blog.save()
        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blog_list.html'


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'body', 'image_blog']
    success_url = reverse_lazy('blog:blog_detail')

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.object.pk])


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
