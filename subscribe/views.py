from django.shortcuts import render
from .models import Subscribe
from .forms import SubscribeForm
from django.views.generic import CreateView


class SubscribeView(CreateView):
    model = Subscribe
    form_class = SubscribeForm
    success_url = '/'
