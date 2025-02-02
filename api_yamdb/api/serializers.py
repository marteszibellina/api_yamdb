"""Сериализаторы моделей приложений reviews и users."""

from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from api.utils import send_confirmation_email
from api.validators import validate_email, validate_username
from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователей."""

    email = serializers.EmailField(validators=[validate_email])
    username = serializers.CharField(validators=[validate_username])

    # Валидация полученных данных и создание пользователя
    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)
        if created:
            confirmation_code = default_token_generator.make_token(user)
            user.confirmation_code = confirmation_code
            user.save()
            send_confirmation_email(user)  # отправка кода подтверждения
        return user

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):  # 'attrs' has been renamed to 'data'
        """Валидация полученных данных."""
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        # Проверяем, что username и confirmation_code не пустые
        if not username or not confirmation_code:
            raise serializers.ValidationError(
                {'username': 'Неверные учетные данные'})

        # Проверяем, что пользователь с таким username существует
        user = User.objects.filter(username=username).first()
        # Если пользователь не найден
        if not user:
            raise NotFound(
                {'username': 'Неверные учетные данные'})

        # Проверяем, что код подтверждения совпадает
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})

        # Если данные верны, возвращаем данные
        return data


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
    rating = serializers.IntegerField(required=False, default=None)

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
        if request.method == 'POST':
            if Review.objects.filter(
                title_id=self.context.get('view').kwargs.get('title_id'),
                author=request.user
            ).exists():
                raise ValidationError(
                    'Вы уже писали отзыв на данное произведение.'
                )
        return data
