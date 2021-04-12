from django.urls import path
from . import views

urlpatterns = [
    path('', views.SubscribeView.as_view(), name='subscribe'),
]