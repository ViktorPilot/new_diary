from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Класс информации о пользователе"""

    username = None
    email = models.EmailField(verbose_name="email", unique=True)
    avatar = models.ImageField(verbose_name="аватар", upload_to="users/image/", blank=True, null=True)
    phone_number = models.CharField(verbose_name="номер телефона", max_length=20, blank=True, null=True)
    country = models.CharField(verbose_name="страна", max_length=50, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> Any:
        """Магический метод, возвращающий электронную почту пользователя"""
        return self.email
