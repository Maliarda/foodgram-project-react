from colorfield.fields import ColorField
from django.db import models


class Tag(models.Model):
    """Тэг."""

    name = models.CharField(
        max_length=20,
        verbose_name="Название тэга",
    )

    color = ColorField(
        max_length=7, default="#ffffff", unique=True, verbose_name="Цвет тэга"
    )

    slug = models.SlugField(
        max_length=20,
        unique=True,
        verbose_name="Идентификатор тэга",
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name
