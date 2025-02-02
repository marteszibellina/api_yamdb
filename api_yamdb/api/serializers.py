"""Сериализаторы моделей приложений reviews и users."""

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from api.utils import send_confirmation_email
from reviews.models import Category, Comments, Genre, Review, Title
from users.constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH
from users.validators import validate_username

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователей."""

    username = serializers.CharField(
        required=True,
        validators=[validate_username],
        max_length=NAME_MAX_LENGTH
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH)

    def validate(self, attrs):
        """Валидация полученных данных."""
        email = attrs.get('email')
        username = attrs.get('username')

        # Проверка на наличие username и email в БД
        user_username = User.objects.filter(username=username).first()
        user_email = User.objects.filter(email=email).first()

        if user_username != user_email:
            # Если email зарегистрирован, а username не зарегистрирован
            if user_email and not user_username:
                raise serializers.ValidationError(
                    {'error': 'Этот email уже есть с другим username'}
                )

            # Если username зарегистрирован, а email не зарегистрирован
            if user_username and not user_email:
                raise serializers.ValidationError(
                    {'error': 'Этот username уже есть с другим email'}
                )

        return attrs

    # Валидация полученных данных и создание пользователя
    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_email(user, confirmation_code)
        return user


class TokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        """Валидация полученных данных."""
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

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
        token = AccessToken.for_user(user)
        return {'access': str(token)}


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
