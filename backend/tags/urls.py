from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register("tags", TagsViewSet, basename="tags")

urlpatterns = [
    path("", include(router.urls)),