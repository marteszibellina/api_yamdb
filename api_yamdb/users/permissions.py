from rest_framework.permissions import BasePermission


class IsAdminOrSuperuser(BasePermission):
    """Разрешение для администраторов и суперпользователей."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)
