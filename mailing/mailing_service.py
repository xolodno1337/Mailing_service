import smtplib
import pytz
from config.settings import EMAIL_HOST_USER
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Mailing, MailingAttempt


def send_mailing(obj):
    """ Функция отправки письма. """
    try:
        # Получаем emails клиентов
        clients_emails = [client.email for client in obj.clients.all()]

        subject = obj.message.subject_message
        content = obj.message.content

        # Отправка письма
        server_response = send_mail(
            subject,
            content,
            EMAIL_HOST_USER,
            recipient_list=clients_emails,
            fail_silently=False,
        )

        # Записываем успешную попытку
        successful_attempt = MailingAttempt.objects.create(
            mailing=obj,
            status='success',
            server_response=server_response,
            first_send_datetime=timezone.now()
        )
        if server_response:
            successful_attempt.is_successful = True
        successful_attempt.save()

    except smtplib.SMTPException as e:
        MailingAttempt.objects.create(
            mailing=obj,
            status='failed',
            server_response=e,
            first_send_datetime=timezone.now()
        )
    if obj.status == 'Создана':
        obj.status = 'Запущена'
        obj.save()


def send_mail_period():
    """ Функция отправляет рассылку с учетом периодичности. """
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(status__in=('Создана', 'Запущена'))

    for obj in mailings:
        if obj.first_send_datetime < current_datetime < obj.end_date:
            attempt = MailingAttempt.objects.filter(mailing=obj)
            if attempt.exists():
                last_attempt = attempt.order_by('-first_send_datetime').first()
                current_timedelta = current_datetime - last_attempt.first_send_datetime
                if current_timedelta > timedelta(days=1) and obj.periodicity == 'Ежедневно':
                    send_mailing(obj)
                elif current_timedelta >= timedelta(days=7) and obj.periodicity == 'Еженедельно':
                    send_mailing(obj)
                elif current_timedelta >= timedelta(days=30) and obj.periodicity == 'Ежемесячно':
                    send_mailing(obj)
            else:
                send_mailing(obj)
        elif current_datetime > obj.end_date:
            obj.status = 'Завершена'
            obj.save()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mail_period, 'interval', seconds=10)
    scheduler.start()
