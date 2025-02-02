"""Права доступа для пользователей."""

from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Разрешение для администраторов и суперпользователей."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
