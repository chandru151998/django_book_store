from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_no = models.BigIntegerField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
