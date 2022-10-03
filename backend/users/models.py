from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь."""

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLES = {
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    }

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

    role = models.CharField(
        verbose_name="Статус",
        max_length=20,
        choices=ROLES,
        default=USER,
    )

    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
        "password",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.is_staff or self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "user",
                    "author",
                ),
                name="unique_follow",
            ),
        )

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
