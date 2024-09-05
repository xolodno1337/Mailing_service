from django.db import models
from django.urls import reverse

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок блога', help_text='Укажите название блога')
    body = models.TextField(verbose_name='Содержание статьи', help_text='Введите содержание статьи')
    image_blog = models.ImageField(upload_to='blog/', verbose_name='Изображение', help_text='Загрузите изображение',
                                   **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
