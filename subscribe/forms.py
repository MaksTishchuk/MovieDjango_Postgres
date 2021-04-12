from django import forms
from .models import Subscribe
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class SubscribeForm(forms.ModelForm):
    """Форма подписки на рассылку"""
    captcha = ReCaptchaField()

    class Meta:
        model = Subscribe
        fields = ('email', 'captcha')
        widgets = {
            'email': forms.TextInput(attrs={"class": "editContent", "placeholder": "Введите свой email.."})
        }

        labels = {
            'email': ''
        }
