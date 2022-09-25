from django.contrib.auth import get_user_model
from django.db import models
from tags.models import Tag
from users.models import User
from django.core.validators import MinValueValidator

User = get_user_model()


class Ingredient(models.Model):
    """Ингредиент"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название ингредиента",
    )

    measurement_unit = models.CharField(
        max_length=200, verbose_name="Единица измерения"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт"""

    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        verbose_name="Ингредиенты рецепта",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги рецепта",
        related_name="recipes",
    )
    image = models.ImageField(
        verbose_name="Фото готового блюда",
        upload_to="recipes/",
    )
    name = models.CharField(
        verbose_name="Название рецепта",
        max_length=200,
    )
    text = models.TextField(verbose_name="Описание рецепта")
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message="Время приготовления должно быть больше 0"
            ),
        ],
        verbose_name="Время приготовления (в минутах)",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredient",
        verbose_name="Рецепт",
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_recipe",
        verbose_name="Ингредиент",
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1, message="Укажите количество больше нуля!"),
        ),
        verbose_name="Количество ингредиента",
    )

    constraints = (
        models.UniqueConstraint(
            fields=(
                "ingredient",
                "recipe",
            ),
            name="unique ingredient recipe",
        ),
    )
