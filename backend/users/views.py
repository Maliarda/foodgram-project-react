from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.pagination import LimitPageNumberPaginator
from users.models import Follow, User
from users.serializers import CustomUserSerializer, FollowSerializer


class CustomUserViewSet(UserViewSet):
    """Вьюсет для пользователя."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


class FollowViewSet(APIView):
    """Апивью подписки и отписки."""

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitPageNumberPaginator

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        if user_id == request.user.id:
            return Response(
                {"error": "Невозможно подписаться на самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Follow.objects.filter(
            user=request.user, author_id=user_id
        ).exists():
            return Response(
                {"error": "Уже подписаны"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        author = get_object_or_404(User, id=user_id)
        Follow.objects.create(user=request.user, author_id=user_id)
        return Response(
            self.serializer_class(author, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        get_object_or_404(User, id=user_id)
        subscription = Follow.objects.filter(
            user=request.user, author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Вы не подписаны на пользователя"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class FollowListView(ListAPIView):
    """Просмотр подписок."""

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
