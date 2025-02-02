from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class CustonUserAdmin(BaseUserAdmin):
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
