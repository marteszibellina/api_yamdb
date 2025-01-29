"""Вьюсеты для моделей отзывов и комментариев."""

from django.shortcuts import viewsets

from .models import Comments, Reviews
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов"""

    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
