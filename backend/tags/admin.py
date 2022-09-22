from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )
