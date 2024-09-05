from mailing.models import Mailing, Message, Client
from django.contrib import admin


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_mailing', 'first_send_datetime', 'periodicity', 'status')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject_message', 'owner')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment', 'owner')
