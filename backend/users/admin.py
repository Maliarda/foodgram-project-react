from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
    )
    list_filter = ("email", "username")
    search_fields = (
        "emil",
        "username",
    )
    empty_value_display = "-пусто-"
