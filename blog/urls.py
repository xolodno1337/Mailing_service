from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name


urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('list/', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('view/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='blog_detail'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
