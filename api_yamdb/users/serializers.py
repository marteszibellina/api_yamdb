from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_email(self, value):
        """Проверка на уникальность email."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует')
        return value

    def validate_username(self, value):
        """Проверка на уникальность username."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует')
        return value


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
