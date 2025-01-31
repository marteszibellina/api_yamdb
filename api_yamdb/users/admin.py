from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'bio')
