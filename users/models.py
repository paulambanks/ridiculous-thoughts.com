from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # First/last name is not a global-friendly pattern
    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Email & Password are required by default.

    def __str__(self):
        return self.email
