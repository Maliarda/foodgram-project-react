from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Follow, User

User = get_user_model()

RECIPES_LIMIT = 3


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор при создании пользователя."""

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomUserSerializer(UserSerializer):
    """Сериализатор для отображения пользователя."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj.id).exists()


class FollowShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецептов в подписке."""

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class ShowFollowsSerializer(CustomUserSerializer):
    """Сериализатор отображения подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        recipes = obj.recipes.all()[:RECIPES_LIMIT]
        return FollowShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return recipes.count()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    user = serializers.IntegerField(source="user.id")
    author = serializers.IntegerField(source="author.id")

    class Meta:
        model = Follow
        fields = ["user", "author"]

    def validate(self, data):
        user = data["user"]["id"]
        author = data["author"]["id"]
        follow_exist = Follow.objects.filter(
            user=user, author__id=author
        ).exists()
        if user == author:
            raise serializers.ValidationError(
                {"errors": "Невозможно подписаться на самого себя"}
            )
        elif follow_exist:
            raise serializers.ValidationError({"errors": "Уже подписаны"})
        return data

    def create(self, validated_data):
        author = validated_data.get("author")
        author = get_object_or_404(User, pk=author.get("id"))
        user = validated_data.get("user")
        return Follow.objects.create(user=user, author=author)
