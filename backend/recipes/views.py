from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.permissions import IsAdminAuthorOrReadOnly, IsAdminOrReadOnly
from recipes.serializers import AddRecipeSerializer, ShowRecipeSerializer

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart)
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          ShoppingCartSerializer)


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


class FavoriteRecipeApiView(APIView):
    """Апивью для избранного."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, favorite_id):
        user = request.user
        data = {"recipe": favorite_id, "user": user.id}
        serializer = FavoriteRecipeSerializer(
            data=data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, favorite_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=favorite_id)
        FavoriteRecipe.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartApiView(APIView):
    """Апивью для покупок."""

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, recipe_id):
        user = request.user
        data = {"recipe": recipe_id, "user": user.id}
        context = {"request": request}
        serializer = ShoppingCartSerializer(data=data, context=context)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCartApiView(APIView):
    """Апивью для выгрузки списка покупок."""

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        shopping_list = {}
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        )
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in shopping_list:
                shopping_list[name] = {
                    "measurement_unit": measurement_unit,
                    "amount": amount,
                }
            else:
                shopping_list[name]["amount"] += amount
        main_list = sorted(
            [
                f"{item}: {value['amount']} {value['measurement_unit']}\n"
                for item, value in shopping_list.items()
            ]
        )
        response = HttpResponse(main_list, content_type="text/plain")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="shoppint_list.txt"'
        return response
