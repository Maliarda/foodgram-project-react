from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название тэга",
    )

    color = models.Col

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Идентификатор тэга",
    )
