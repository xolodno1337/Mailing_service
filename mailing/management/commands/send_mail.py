from django.core.management.base import BaseCommand
from mailing.mailing_service import send_mailing
from mailing.models import Mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status='Создана')
        for mailing in mailings:
            send_mailing(mailing)
