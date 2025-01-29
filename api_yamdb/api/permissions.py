"""Права доступа для пользователей."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешает изменение только автору объекта."""

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем: анон, пользователь, админ
        if request.method in permissions.SAFE_METHODS:
            return True

        # Запись разрешена только автору
        return obj.author == request.user


class IsAdminOrModerator(permissions.BasePermission):
    """Разрешает изменение только администратору или модератору."""

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_superuser
