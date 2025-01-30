"""Права доступа для пользователей."""

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAuthorAdminModeratorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        ):
            return True
"""Права доступа для пользователей."""

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAdminModeratorOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        ):
            return True