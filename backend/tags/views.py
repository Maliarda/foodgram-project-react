from rest_framework import viewsets

from recipes.permissions import IsAdminOrReadOnly
from tags.serializers import TagSerializer

from .models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
