from django.core.management.base import BaseCommand
from mailing.mailing_service import send_mailing


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        send_mailing()
