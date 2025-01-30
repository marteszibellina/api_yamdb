import secrets

from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .serializers import SignUpSerializer, UserSerializer
from .utils import send_confirmation_email
from .permissions import IsAdminOrSuperuser


class SignUpViewSet(viewsets.ViewSet):
    """Вьюсет для регистрации пользователей."""

    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Регистрация пользователя и повторная отправка кода."""
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']

            user = User.objects.filter(username=username).first()

            if user:
                # Если пользователь с таким username уже существует
                # Проверяем, что email совпадает
                if user.email != email:
                    return Response(
                        {'error': 'Этот username уже есть с другим email'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Если email совпадает, обновляем код подтверждения
                user.confirmation_code = secrets.token_hex(16)
                user.save(update_fields=['confirmation_code'])
                # Отправляем новый код подтверждения
                send_confirmation_email(user.email, user.confirmation_code)
                return Response(
                    {'message': 'Код подтверждения отправлен повторно.'},
                    status=status.HTTP_200_OK)

            # Если пользователя с таким username нет, а почта есть
            # Вызываем исключение
            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Такая почта уже зарегистрирована'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Создаем пользователя
            user = User.objects.create_user(
                username=username,
                email=email,
                confirmation_code=secrets.token_hex(16)
            )

            # Отправляем код подтверждения
            send_confirmation_email(user.email, user.confirmation_code)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainPairView(viewsets.ViewSet):
    """Вьюсет для получения JWT-токена по коду подтверждения."""

    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Метод для получения токена."""
        # Получаем данные из запроса
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        # Проверяем, что данные не пусты
        if not username or not confirmation_code:
            return Response(
                {'error': 'Требуются username и confirmation_code'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, что пользователь с таким именем существует
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что код подтверждения совпадает
        if user.confirmation_code != confirmation_code:
            return Response(
                {'error': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Если данные верны, генерируем токен
        token_serializer = TokenObtainPairSerializer(
            data={'username': username, 'password': ''})

        if token_serializer.is_valid():
            # Очищаем код подтверждения после успешной аутентификации
            user.confirmation_code = ''
            user.save(update_fields=['confirmation_code'])

            return Response(token_serializer.validated_data,
                            status=status.HTTP_200_OK)

        return Response(token_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserMeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователем /me."""

    # Права доступа есть только у авторизированных.
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request):
        """Метод для получения информации о пользователе."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        """Метод для обновления информации о пользователе."""
        # Получаем данные из запроса
        data = request.data.copy()
        # Убираем роль, чтобы пользователь не мог поставить себе права
        data.pop('role')
        # Обновляем данные
        serializer = UserSerializer(request.user, data=data, partial=True)
        # Если данные сериализатора прошли валидацию:
        if serializer.is_valid():
            # Сохраняем изменения
            user = serializer.save()
            # Возвращаем роль пользователя
            user.role = request.user.role
            # Сохраняем изменения
            user.save(update_fields=['first_name', 'last_name', 'email', 'bio'])
            # Возвращаем ответ
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Если данные сериализатора не прошли валидацию:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    # Права доступа есть только у администратора.
    permission_classes = (IsAdminOrSuperuser,)

    # Выводим всех пользователей
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Переопределяем методы
    # Создание пользователей
    def create(self, request, *args, **kwargs):
        """Метод для создания пользователя."""
        # Пробуем создать пользователя с проверкой, что он не существует
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """Метод для получения списка пользователей."""
        queryset = self.get_queryset()
        # Дополнительная фильтрация по аттрибутам
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Метод для извлечения информации о пользователе."""
        queryset = self.get_queryset()
        # Находим пользователя по его id
        user = get_object_or_404(queryset, pk=pk)
        # Возвращаем информацию о пользователе
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """Метод для обновления информации о пользователе."""
        queryset = self.get_queryset()
        # Находим пользователя по его id
        user = get_object_or_404(queryset, pk=pk)
        # Обновляем данные
        serializer = self.get_serializer(user, data=request.data, partial=True)
        # Если данные сериализатора прошли валидацию:
        if serializer.is_valid():
            # Сохраняем изменения
            user = serializer.save()
            # Возвращаем роль пользователя
            user.role = request.user.role
            # Сохраняем изменения
            user.save(update_fields=['first_name',
                                     'last_name',
                                     'email','bio','role'])
            # Возвращаем ответ
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Если данные сериализатора не прошли валидацию:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Метод для удаления пользователя."""
        queryset = self.get_queryset()
        # Находим пользователя по его id
        user = get_object_or_404(queryset, pk=pk)
        # Удаляем пользователя
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
