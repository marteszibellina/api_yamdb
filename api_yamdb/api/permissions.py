"""Права доступа для пользователей."""

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or (
                request.user.is_authenticated
                and request.user.is_admin_or_superuser
            )
        )

class IsAdminModeratorOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_superuser


class IsAdminOrSuperuserOrReadOnly(permissions.BasePermission):
    """Админ или суперюзер."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user 
                and request.user.is_authenticated 
                and request.user.is_admin)
        )
