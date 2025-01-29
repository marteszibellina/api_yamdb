"""Сериализаторы моделей отзывов и комментариев."""

from rest_framework import serializers
from reviews.models import Comments, Reviews


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
