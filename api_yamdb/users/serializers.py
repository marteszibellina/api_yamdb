from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from .models import CustomUser
from .utils import send_code


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        send_code(user)
        return user

    def update(self, validated_data):
        return validated_data

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError(
                'Невозможно использовать "me" в качестве никнейма.'
            )
        return username


class ConfirmationCodeSerializer(serializers.Serializer):

    username = serializers.CharField(required=True,)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user, data['confirmation_code']
        ):
            raise serializers.ValidationError('Неверный код подтверждения')
        return data
