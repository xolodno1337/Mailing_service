from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):   # Клиенты сервиса — это те, кто получает рассылки
    email = models.EmailField(max_length=255, unique=True, verbose_name='Контактный email',
                              help_text='Укажите свой Email')
    full_name = models.CharField(max_length=255, verbose_name='Ф.И.О.', help_text='Укажите свои Ф.И.О.')
    comment = models.TextField(verbose_name='Комментарий', help_text='Оставьте комментарий', **NULLABLE)

    def __str__(self):
        return self.full_name
