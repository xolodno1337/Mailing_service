from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):  # Пользователь - тот, кто создает эти рассылки.
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Укажите ваш Email')
    avatar = models.ImageField(upload_to='users/avatars', verbose_name='Аватар', **NULLABLE,
                               help_text='Загрузите ваш аватар')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE,
                             help_text='Укажите ваш номер телефона')
    token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
