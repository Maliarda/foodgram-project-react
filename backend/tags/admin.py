from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )
    search_fields = ("name",)
    ordering = ("color",)
    empty_value_display = "-пусто-"
