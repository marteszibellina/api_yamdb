"""Сериализаторы для пользователей."""

from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from users.models import User
from users.utils import send_confirmation_email
from users.validators import validate_email, validate_username


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
