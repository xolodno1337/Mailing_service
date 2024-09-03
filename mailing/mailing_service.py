import smtplib
import pytz
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Mailing, MailingAttempt


def send_mailing(mailing: Mailing):
    try:
        # Получаем emails клиентов
        clients_emails = [client.email for client in mailing.clients.all()]
        subject = mailing.message.subject_message
        content = mailing.message.content

        # Отправка письма
        server_response = send_mail(
            subject,
            content,
            'butakov.s.a@yandex.ru',
            clients_emails,
            fail_silently=False,
        )

        # Записываем успешную попытку
        MailingAttempt.objects.create(
            mailing=mailing,
            status='success',
            response=str(server_response),
            attempt_datetime=timezone.now()
        )

    except smtplib.SMTPException as e:
        MailingAttempt.objects.create(
            mailing=mailing,
            status='failed',
            response=str(e),
            attempt_datetime=timezone.now()
        )


def send_mail_period():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(first_send_datetime__gte=current_datetime, status='Запущена')

    for mailing in mailings:
        last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-attempt_datetime').first()

        if last_attempt:
            time_since_last_attempt = current_datetime - last_attempt.attempt_datetime
            if mailing.periodicity == 'Раз в день' and time_since_last_attempt.days < 1:
                continue
            elif mailing.periodicity == 'Раз в неделю' and time_since_last_attempt.days < 7:
                continue
            elif mailing.periodicity == 'Раз в месяц' and time_since_last_attempt.days < 30:
                continue

        # Отправка сообщений
        for client in mailing.clients.all():
            send_mail(
                subject=mailing.subject,
                message=mailing.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email]
            )

        # Сохраняем попытку рассылки
        MailingAttempt.objects.create(mailing=mailing, status='Успех')


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mail_period, 'interval', seconds=10)
    scheduler.start()
