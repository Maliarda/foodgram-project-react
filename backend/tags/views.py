from .models import Tag
from rest_framework import permissions, status, viewsets
from recipes.permissions import IsAdminOrReadOnly
from tags.serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
