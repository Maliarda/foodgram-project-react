from recipes.models import Ingredient, RecipeIngredient, Recipe
from rest_framework import serializers
from tags.models import Tag
from drf_base64.fields import Base64ImageField
from users.serializers import CustomUserSerializer
from tags.serializers import TagSerializer
from django.db.models import F
from rest_framework.exceptions import ValidationError


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор вывода ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )


class ShowIngredientsInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода ингредиентов в рецепте."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class AddRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления рецепта."""

    ingredients = AddIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()
    name = serializers.CharField(max_length=200)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
            "author",
        )

    def validate_ingredients(self, ingredients):
        """Валидируем ингредиенты."""
        if not ingredients:
            raise ValidationError("Необходимо добавить ингредиенты")
        for ingredient in ingredients:
            if int(ingredient["amount"]) <= 0:
                raise ValidationError(
                    "Необходимо добавить хотя бы один ингредиент"
                )
        ingrs = [item["id"] for item in ingredients]
        if len(ingrs) != len(set(ingrs)):
            raise ValidationError(
                "Ингредиенты в рецепте должны быть уникальными!"
            )
        return ingredients

    @staticmethod
    def add_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient["id"]
            amount = ingredient["amount"]
            if RecipeIngredient.objects.filter(
                recipe=recipe, ingredient=ingredient_id
            ).exists():
                amount += F("amount")
            RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient_id,
                defaults={"amount": amount},
            )

    def create(self, validated_data):
        author = self.context.get("request").user
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        image = validated_data.pop("image")
        recipe = Recipe.objects.create(
            image=image, author=author, **validated_data
        )
        self.add_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        self.add_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        data = ShowRecipeSerializer(
            recipe, context={"request": self.context.get("request")}
        ).data
        return data


class ShowRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения рецепта.
    """

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    @staticmethod
    def get_ingredients(obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return ShowIngredientsInRecipeSerializer(ingredients, many=True).data
