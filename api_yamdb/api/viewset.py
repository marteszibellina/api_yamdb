from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly


class CategoryGenreViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
):
    """Базовый вьюсет для CategoryViewSet и GenreViewSet."""

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
