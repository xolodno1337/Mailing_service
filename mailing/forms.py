from django.forms import ModelForm, BooleanField

from mailing.models import Mailing, Message, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"
            else:
                fild.widget.attrs['class'] = "form-control"


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
