from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, RecipeViewSet, FavoriteRecipeApiView


router = DefaultRouter()
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("recipes", RecipeViewSet, basename="recipes")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "recipes/<int:favorite_id>/favorite/", FavoriteRecipeApiView.as_view()
    ),
]
