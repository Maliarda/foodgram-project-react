from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCartApiView, FavoriteRecipeApiView,
                    IngredientViewSet, RecipeViewSet, ShoppingCartApiView)

router = DefaultRouter()
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("recipes", RecipeViewSet, basename="recipes")


urlpatterns = [
    path(
        "recipes/download_shopping_cart/",
        DownloadShoppingCartApiView.as_view(),
    ),
    path("", include(router.urls)),
    path(
        "recipes/<int:favorite_id>/favorite/", FavoriteRecipeApiView.as_view()
    ),
    path(
        "recipes/<int:recipe_id>/shopping_cart/", ShoppingCartApiView.as_view()
    ),
]
