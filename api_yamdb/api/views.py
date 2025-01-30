from django.db.models import Avg
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import viewsets, permissions, filters, pagination, mixins

from reviews.models import Category, Genre, Title, Comments, Reviews

from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    CommentSerializer, ReviewSerializer,
    GenreSerializer, TitleSerializer, TitleReadSerializer
)
from .permissions import IsAuthorOrReadOnly, IsAdminOrModerator, IsAdminOrSuperuserOrReadOnly


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrSuperuserOrReadOnly, )
    pagination_class = LimitOffsetPagination
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
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrSuperuserOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrSuperuserOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    
    def get_serializer(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        avg = Reviews.objects.filter(title=instance).aggregate(Avg('score'))
        instance.rating = avg['score__avg']
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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
