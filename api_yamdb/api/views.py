from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, permissions, filters, pagination, mixins

from reviews.models import Category, Genre, Title, Comments, Reviews

from .serializers import (
    CategorySerializer,
    CommentSerializer, ReviewSerializer,
    GenreSerializer, TitleSerializer, TitleReadSerializer
)
from .permissions import IsAuthorOrReadOnly, IsAdminOrModerator


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()

    def get_serializer(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов"""

    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly | IsAdminOrModerator)

    def perform_create(self, serializer):
        """Создание отзыва с автоматическим созданием автора."""
        # Проверка уникальности отзыва на уровне логики вьюсета
        # Находим название произведения
        title = serializer.validated_data['title']
        # Проверяем, что пользователь не оставлял отзыв на это произведение
        if Reviews.objects.filter(title=title,
                                  author=self.request.user).exists():
            # Если пользователь уже оставлял отзыв, то возвращаем ошибку
            raise ValidationError('Вы уже оставляли отзыв на это произведение')
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly | IsAdminOrModerator)

    def perform_create(self, serializer):
        """Создание комментария с автоматическим созданием автора."""
        serializer.save(author=self.request.user)
