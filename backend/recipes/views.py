from .models import Ingredient, Recipe
from rest_framework import permissions, status, viewsets
from recipes.permissions import IsAdminOrReadOnly, IsAdminAuthorOrReadOnly
from .serializers import IngredientSerializer
from django_filters.rest_framework import DjangoFilterBackend
from recipes.serializers import AddRecipeSerializer, ShowRecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    default_serializer_class = AddRecipeSerializer
    serializer_classes = {
        "retrieve": ShowRecipeSerializer,
        "list": ShowRecipeSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.default_serializer_class
        )
