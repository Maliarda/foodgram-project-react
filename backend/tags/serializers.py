from rest_framework import serializers

from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов."""

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )
        extra_kwargs = {"url": {"lookup_field": "id"}}
