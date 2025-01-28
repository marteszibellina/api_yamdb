from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

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

    confirmation_code = serializers.CharField()
    username = serializers.CharField()
