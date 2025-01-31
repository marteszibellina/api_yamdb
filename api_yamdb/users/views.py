import secrets

from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .permissions import IsAdminOrSuperuser, IsUser
from .serializers import SignUpSerializer, UserSerializer
from .utils import send_confirmation_email


class SignUpViewSet(viewsets.ViewSet):
    """Вьюсет для регистрации пользователей."""

    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Регистрация пользователя и повторная отправка кода."""
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']

            # Проверка на существование пользователя с таким username
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
                user.confirmation_code = send_confirmation_email(user.email)
                user.save(update_fields=['confirmation_code'])

                # Отправляем новый код подтверждения
                return Response(
                    {'message': 'Код подтверждения отправлен повторно.'},
                    status=status.HTTP_200_OK
                )

            # Если пользователя с таким username нет
            # Но почта уже зарегистрирована
            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Такая почта уже зарегистрирована'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Создаем нового пользователя
            user = User.objects.create_user(
                username=username,
                email=email,
                confirmation_code=secrets.token_hex(16)  # Гененируем код
            )

            # Отправляем код подтверждения
            send_confirmation_email(user.email)

            return Response(serializer.data, status=status.HTTP_200_OK)

        # Если данные не валидны
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

    def retrieve(self, request):
        """Метод для получения токена через GET."""
        username = request.query_params.get('username')
        confirmation_code = request.query_params.get('confirmation_code')

        if not username or not confirmation_code:
            return Response(
                {'error': 'Требуются username и confirmation_code'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.confirmation_code != confirmation_code:
            return Response(
                {'error': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token_serializer = TokenObtainPairSerializer(
            data={'username': username, 'password': ''})

        if token_serializer.is_valid():
            user.confirmation_code = ''
            user.save(update_fields=['confirmation_code'])
            return Response(token_serializer.validated_data,
                            status=status.HTTP_200_OK)

        return Response(token_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserMeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователем /me."""

    # Права доступа есть только у авторизированных.
    permission_classes = (IsAdminOrSuperuser, IsUser)

    def retrieve(self, request):
        """Метод для получения информации о пользователе."""
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = User.objects.get(username=request.user.username)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        """Метод для обновления информации о пользователе."""
        # Получаем данные из запроса и копируем их
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
            user.save(
                update_fields=['first_name', 'last_name', 'email', 'bio'])
            # Возвращаем ответ
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Если данные сериализатора не прошли валидацию:
        return Response(serializer.errors,
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request):
        """Метод для удаления пользователя."""
        return Response({'detail': 'Method "DELETE" not allowed.'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    # Права доступа есть только у администратора.
    permission_classes = (IsAdminOrSuperuser,)

    # Выводим всех пользователей
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class = UserPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

    @action(
        detail=False,
        methods=['get', 'put', 'patch'],
        url_path='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        """API для редактирования текущим пользователем своих данных."""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data)

    # Переопределяем методы
    # Создание пользователей
    def create(self, request, *args, **kwargs):
        """Метод для создания пользователя."""
        # Пробуем создать пользователя с проверкой, что он не существует
        username = request.data.get('username')
        email = request.data.get('email')
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Пользователь с таким username уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Пользователь с таким email уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Метод для извлечения информации о пользователе."""
        queryset = self.get_queryset()
        # Находим пользователя по его id
        user = get_object_or_404(queryset, username=kwargs['pk'])
        # Возвращаем информацию о пользователе
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Method "PUT" not allowed.'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        """Метод для обновления информации о пользователе."""
        queryset = self.get_queryset()
        # Находим пользователя по его id
        user = get_object_or_404(queryset, username=kwargs['pk'])
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
                                     'email', 'bio', 'role'])
            # Возвращаем ответ
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Если данные сериализатора не прошли валидацию:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Метод для удаления пользователя."""
        queryset = self.get_queryset()
        # Находим пользователя по его id
        user = get_object_or_404(queryset, username=kwargs['pk'])
        # Удаляем пользователя
        if user == request.user:
            return Response({'detail': 'Нельзя удалить самого себя.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
