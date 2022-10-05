from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from recipes.permissions import IsAdminAuthorOrReadOnly, IsAdminOrReadOnly
from recipes.serializers import AddRecipeSerializer, ShowRecipeSerializer
from recipes.services import convert_to_file

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
)
from .serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    ShoppingCartSerializer,
)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки рецептов."""

    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    default_serializer_class = AddRecipeSerializer
    serializer_classes = {
        "retrieve": ShowRecipeSerializer,
        "list": ShowRecipeSerializer,
    }
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.default_serializer_class
        )

    def __add_or_del_recipe(self, method, user, pk, model, serializer):
        """Добавление/удаление в избранное или список покупок."""
        recipe = get_object_or_404(Recipe, pk=pk)
        if method == "POST":
            model.objects.get_or_create(user=user, recipe=recipe)
            return Response(
                serializer.to_representation(instance=recipe),
                status=status.HTTP_201_CREATED,
            )
        if method == "DELETE":
            model.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="favorite",
        url_name="favorite",
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        """Добавление в избранное, удаление из избранного"""
        return self.__add_or_del_recipe(
            request.method,
            request.user,
            pk,
            model=FavoriteRecipe,
            serializer=FavoriteRecipeSerializer(),
        )

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_name="shopping_cart",
        url_path="shopping_cart",
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        """Добавление покупок в корзине, удаление покупок из корзины."""
        return self.__add_or_del_recipe(
            request.method,
            request.user,
            pk,
            model=ShoppingCart,
            serializer=ShoppingCartSerializer(),
        )

    @action(
        detail=False,
        methods=[
            "GET",
        ],
        url_name="download_shopping_cart",
        url_path="download_shopping_cart",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def download_shopping_cart(self, request):
        """Выгрузка списка покупок."""
        cart_ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .values(
                "ingredient__name",
                "ingredient__measurement_unit",
            )
            .annotate(ingredient_total_amount=Sum("amount"))
        )
        return convert_to_file(cart_ingredients)
