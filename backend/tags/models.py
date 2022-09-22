from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название тэга",
    )

    color = ColorField(
        max_length=7, default="#ffffff", unique=True, verbose_name="Цвет тэга"
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Идентификатор тэга",
    )

    def __str__(self):
        return self.name
