import secrets

from django.db import IntegrityError

from rest_framework import status, viewsets, permissions

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import SignUpSerializer, UserSerializer
from .utils import send_confirmation_email


class SignUpViewSet(viewsets.ModelViewSet):
    """Вьюсет для регистрации пользователей."""

    def create(self, request):
        """Регистрация нового пользователя."""
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Создаем пользователя и отправляем код подтверждения
                user = serializer.save()
                user.confirmation_code = secrets.token_hex(16)
                user.save()
                send_confirmation_email(user.email, user.confirmation_code)
            # Если пользователь с таким email уже существует
            except IntegrityError as error:
                return Response(
                    f'{error}: Пользователь с таким email уже существует',
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(viewsets.ModelViewSet):
    """Вьюсет для получения токена."""

    def create(self, request):
        """Получение токена."""
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        try:
            User.objects.get(username=username,
                             confirmation_code=confirmation_code)
        except User.DoesNotExist:
            return Response('Неверные данные',
                            status=status.HTTP_400_BAD_REQUEST)
        return TokenObtainPairView.as_view()(request)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as error:
            return Response(
                f'{error}: Пользователь с таким username уже существует',
                status=status.HTTP_400_BAD_REQUEST)


class UserMeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с текущим пользователем."""

    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request):
        """Получение информации о текущем пользователе."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        """Обновление информации о текущем пользователе."""
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
