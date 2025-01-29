from django.shortcuts import render

# Create your views here.


from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters, pagination, mixins

from reviews.models import Category, Genre, Title, Comments, Reviews

from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, TitleReadSerializer
)


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


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date')  # пока только для чтения


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    class Meta:
        model = Reviews
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'pub_date')  # пока только для чтения
