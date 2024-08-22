from django.db import models

NULLABLE = {'blank': True, 'null': True}

periodicity_choices = [  # Периодичность рассылки
    ('daily', 'Раз в день'),
    ('weekly', 'Раз в неделю'),
    ('monthly', 'Раз в месяц'),
]
status_choices = [  # Статус рассылки
    ('created', 'Создана'),
    ('running', 'Запущена'),
    ('completed', 'Завершена'),
]


class Client(models.Model):  # Клиенты сервиса — это те, кто получает рассылки
    email = models.EmailField(max_length=255, unique=True, verbose_name='Контактный email',
                              help_text='Укажите свой Email')
    full_name = models.CharField(max_length=255, verbose_name='Ф.И.О.', help_text='Укажите свои Ф.И.О.')
    comment = models.TextField(verbose_name='Комментарий', help_text='Оставьте комментарий', **NULLABLE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):   # Рассылка
    name_mailing = models.CharField(max_length=50, verbose_name='Название рассылки',
                                    help_text='Укажите название рассылки', **NULLABLE)
    first_send_datetime = models.DateTimeField(verbose_name='Дата и время первой отправки рассылки')
    periodicity = models.CharField(max_length=10, choices=periodicity_choices, verbose_name='Периодичность рассылки',
                                   default='daily', help_text='Выберите периодичность рассылки')
    status = models.CharField(max_length=10, choices=status_choices, verbose_name='Статус рассылки',
                              default='created')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты', help_text='Выберите клиентов для рассылки')
    message = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)

    def __str__(self):
        return self.name_mailing

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
