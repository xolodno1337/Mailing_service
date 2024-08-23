from mailing.models import Mailing
from django.contrib import admin


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_mailing', 'first_send_datetime', 'periodicity', 'status')
