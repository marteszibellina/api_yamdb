from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrSuperuser(BasePermission):
    """Разрешение для администраторов и суперпользователей."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class IsUser(BasePermission):
    """Разрешение для пользователей."""

    def has_permission(self, request, view):
        """Проверка, является ли пользователь авторизованным."""
        return (
            request.method in SAFE_METHODS or (
                request.user.is_authenticated
                and request.user.is_admin_or_superuser
            )
        )
