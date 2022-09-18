from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="Электронная почта",
        unique=True,
        max_length=254,
    )
    username = models.CharField(
        verbose_name="Имя пользователя",
        unique=True,
        max_length=150,
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=150, blank=True
    )
    bio = models.TextField(
        verbose_name="О себе",
        blank=True,
    )
    joined_date = models.DateTimeField(
        verbose_name="Дата регистрации",
        auto_now_add=True,
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=150,
        help_text="Введите пароль",
    )

    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
        "password",
    ]

    def __str__(self):
        return self.username
