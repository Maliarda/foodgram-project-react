from django.shortcuts import render
from users.models import User
from rest_framework import filters, permissions, status, viewsets
from rest_framework import permissions
from rest_framework.decorators import action, api_view, permission_classes
from users.serializers import CustomUserSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from djoser.views import UserViewSet


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
