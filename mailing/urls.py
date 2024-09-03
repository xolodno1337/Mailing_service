from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import home, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    MailingDetailView, MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView, \
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientDetailView, mailing_attempt_report

app_name = MailingConfig.name

urlpatterns = [
    path('', home, name='home'),
    # Рассылка:
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    # Сообщения:
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    # Клиенты:
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),

    path('report/', mailing_attempt_report, name='report'),
]
