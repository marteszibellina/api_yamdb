import django_filters
from .models import User


class UserFilter(django_filters.FilterSet):
    """Фильтры для модели User."""

    username = django_filters.CharFilter(field_name='username',
                                         lookup_expr='iexact')

    class Meta:
        model = User
        fields = ['username', ]
