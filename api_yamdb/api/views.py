from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, filters, pagination, mixins

from reviews.models import Category, Genre, Title, Comments, Review

from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    CommentSerializer, ReviewSerializer,
    GenreSerializer, TitleSerializer, TitleReadSerializer
)
from .permissions import IsAdminOrReadOnly, IsAdminModeratorOwnerOrReadOnly


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
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
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Title."""

    queryset = (
        Title.objects.all().annotate(
            rating=Avg('reviews__score')
        ).order_by('name')
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly
    )
    http_method_names = ('delete', 'get', 'patch', 'post')

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            title=self.get_title(),
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    # queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    # def get_review(self):
    #     return get_object_or_404(
    #         Review,
    #         pk=self.kwargs.get('title_id'),
    #         title__id=self.kwargs.get('reviews_id')
    #     )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comments.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)