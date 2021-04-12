from django.db import models

# Create your models here.
class Subscribe(models.Model):
    """Подписка на рассылку по емейл"""
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email