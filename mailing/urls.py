from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import home, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    MailingDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('create', MailingCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
]
