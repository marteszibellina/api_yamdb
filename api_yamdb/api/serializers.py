"""Сериализаторы моделей приложений reviews и users."""

import re

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from api.utils import send_confirmation_email
from reviews.models import Category, Comments, Genre, Review, Title
from users.constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователей."""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        """Валидация полученных данных."""
        email = attrs.get('email')
        username = attrs.get('username')

        # Проверка, что email и username не пустые
        if not email or not username:
            raise serializers.ValidationError(
                {'username': 'Неверные учетные данные'})

        # Проверка, что username соответствует требованиям
        if username.lower() == 'me':
            raise serializers.ValidationError(
                {'username': 'Недопустимое имя пользователя'})
        if len(username) > NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                {f'Длина username превышает {NAME_MAX_LENGTH} символов'})
        invalid_chars = re.sub(r'[\w.@+-]', '', username)
        if invalid_chars:
            raise serializers.ValidationError(
                {f'Недопустимые символы в username {invalid_chars}.'})

        # Проверка, что почта соответствует требованиям
        if len(email) > EMAIL_MAX_LENGTH:
            raise serializers.ValidationError(
                {f'Длина email превышает {EMAIL_MAX_LENGTH} символов'})

        # Проверка на наличие username и email в БД
        user_username = User.objects.filter(username=username).first()
        user_email = User.objects.filter(email=email).first()

        # Если пользователь с таким username и email уже существует
        if user_username and user_email:
            # Если username совпадает, но email не совпадает
            if user_username != user_email:
                raise serializers.ValidationError(
                    {'error': 'Этот username уже есть с другим email'})

        # Если email зарегистрирован, а username не зарегистрирован
        if user_email and not user_username:
            raise serializers.ValidationError(
                {'error': 'Этот email уже есть с другим username'})

        # Если username зарегистрирован, а email не зарегистрирован
        if user_username and not user_email:
            raise serializers.ValidationError(
                {'error': 'Этот username уже есть с другим email'})

        return attrs

    # Валидация полученных данных и создание пользователя
    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)
        if created:
            confirmation_code = default_token_generator.make_token(user)
            user.confirmation_code = confirmation_code
            user.save()
            send_confirmation_email(user)  # отправка кода подтверждения
        return user


class TokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        """Валидация полученных данных."""
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        # Проверяем, что username и confirmation_code не пустые
        if not username or not confirmation_code:
            raise serializers.ValidationError(
                {'Отсутствует username или confirmation_code'})

        # Проверяем, что пользователь с таким username существует
        user = User.objects.filter(username=username).first()
        # Если пользователь не найден
        if not user:
            raise NotFound(
                {'Пользователь с таким username не найден'})

        # Проверяем, что код подтверждения совпадает
        if not user.check_confirmation_code(confirmation_code):
            raise serializers.ValidationError(
                {'Неверный код подтверждения'})

        # Если данные верны, возвращаем данные
        return attrs

    def create(self, validated_data):
        """Валидация полученных данных и создание пользователя."""
        username = validated_data.get('username')
        user = get_object_or_404(User, username=username)

        # Генерируем JWT-токен
        refresh = AccessToken.for_user(user)
        return {'access': str(refresh)}


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'role',
                  'bio',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        fields = ('name', 'slug')
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений + rating."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        write_only=True,
        many=True,
        allow_null=False,
        allow_empty=False,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)

    def to_representation(self, instance):
        title_read_serializer = TitleReadSerializer(instance)
        return title_read_serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Проверяем, что отзыв только один."""
        request = self.context.get('request')
        if request.method == 'POST' and Review.objects.filter(
            title_id=self.context.get('view').kwargs.get('title_id'),
            author=request.user
        ).exists():
            raise ValidationError(
                'Вы уже писали отзыв на данное произведение.'
            )
        return data
