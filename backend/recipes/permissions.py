from rest_framework import permissions


# class IsAuthorOrReadOnly(permissions.BasePermission):
#     """Разрешено автору или только для чтения"""

#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or obj.author == request.user
#         )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешено администратору или только для чтения"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    """Разрешено автору или администратору, остальные только для чтения"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (
            request.user.is_admin
            or obj.author == request.user
            or request.method == "POST"
        ):
            return True
        return request.method in permissions.SAFE_METHODS
