from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}

periodicity_choices = [  # Периодичность рассылки
    ('Раз в день', 'Раз в день'),
    ('Раз в неделю', 'Раз в неделю'),
    ('Раз в месяц', 'Раз в месяц'),
]
status_choices = [  # Статус рассылки
    ('Создана', 'Создана'),
    ('Запущена', 'Запущена'),
    ('Завершена', 'Завершена'),
]


class Client(models.Model):  # Клиенты сервиса — это те, кто получает рассылки
    email = models.EmailField(max_length=255, unique=True, verbose_name='Контактный email',
                              help_text='Укажите свой Email')
    full_name = models.CharField(max_length=255, verbose_name='Ф.И.О.', help_text='Укажите свои Ф.И.О.')
    comment = models.TextField(verbose_name='Комментарий', help_text='Оставьте комментарий', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):  # Сообщение для рассылки
    subject_message = models.CharField(max_length=150, verbose_name='Тема сообщения',
                                       help_text='Укажите тему сообщения')
    content = models.TextField(verbose_name='Содержимое сообщения', help_text='Укажите содержимое сообщения')
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.subject_message

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):  # Рассылка
    name_mailing = models.CharField(max_length=50, verbose_name='Название рассылки',
                                    help_text='Укажите название рассылки', **NULLABLE)
    first_send_datetime = models.DateTimeField(default=timezone.now,
                                               verbose_name='Дата и время первой отправки рассылки')
    periodicity = models.CharField(max_length=20, choices=periodicity_choices, verbose_name='Периодичность рассылки',
                                   default='daily', help_text='Выберите периодичность рассылки')
    status = models.CharField(max_length=10, choices=status_choices, verbose_name='Статус рассылки',
                              default='created')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты', help_text='Выберите клиентов для рассылки')
    message = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.name_mailing

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingAttempt(models.Model):  # Попытка рассылки
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts',
                                verbose_name='Рассылка')
    attempt_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки рассылки')

    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус попытки')
    response = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE)

    def __str__(self):
        return f"{self.mailing} - Попытка: {self.attempt_datetime} - Статус: {self.status}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
