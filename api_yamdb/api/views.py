from django.shortcuts import render

# Create your views here.


from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters, pagination, mixins

from reviews.models import Category, Genre, Title
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, TitleReadSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def get_serializer(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer
