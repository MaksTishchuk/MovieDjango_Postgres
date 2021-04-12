from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser


class LocalUser(AbstractUser):
    pass
    # date_of_birth = models.DateField(help_text='YYYY-MM-DD format')
    # location = models.CharField(max_length=255, null=True, blank=True)
    # is_admin = models.BooleanField(default=False)
    # created = models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True)
