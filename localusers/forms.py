from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from allauth.account.forms import SetPasswordField, PasswordField
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
