from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class YamdbUserAdmin(BaseUserAdmin):  # название модели по названию проекта
    """User admin."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email', 'role')
    empty_value_display = '-пусто-'

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'role')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'role')}),
    )

    ordering = ('username',)
