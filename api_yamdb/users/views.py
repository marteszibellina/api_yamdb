"""Вьюсеты для работы с пользователями."""

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsAdmin
from users.serializers import (SignUpSerializer, TokenObtainSerializer,
                               UserSerializer)
# from users.utils import send_confirmation_email


class SignUpViewSet(viewsets.ViewSet):
    """Вьюсет для регистрации пользователей."""

    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Регистрация пользователя и повторная отправка кода."""
        serializer = SignUpSerializer(data=request.data)

        # Если данные валидны
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        # serializer.send_email(serializer.validated_data['email'])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# Создадим вью-функцию для получения JWT-токена по коду подтверждения
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token_obtain_view(request):
    """Вью-функция для получения JWT-токена по коду подтверждения."""

    # Создаем сериализатор
    serializer = TokenObtainSerializer(data=request.data)

    # Проверяем, что данные валидны
    serializer.is_valid(raise_exception=True)
    serializer.create(serializer.validated_data)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    # Права доступа есть только у администратора.
    permission_classes = (IsAdmin,)

    # Выводим всех пользователей
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    search_fields = ('=username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
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

    # def retrieve(self, request, *args, **kwargs):
    #     """Метод для извлечения информации о пользователе."""
    #     queryset = self.get_queryset()
    #     # Находим пользователя по его id
    #     user = get_object_or_404(queryset, username=kwargs['pk'])
    #     # Возвращаем информацию о пользователе
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     return Response({'detail': 'Method "PUT" not allowed.'},
    #                     status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # def partial_update(self, request, *args, **kwargs):
    #     """Метод для обновления информации о пользователе."""
    #     queryset = self.get_queryset()
    #     # Находим пользователя по его id
    #     user = get_object_or_404(queryset, username=kwargs['pk'])
    #     # Обновляем данные
    #     serializer = self.get_serializer(user, data=request.data, partial=True)
    #     # Если данные сериализатора прошли валидацию:
    #     if serializer.is_valid():
    #         # Сохраняем изменения
    #         user = serializer.save()
    #         # Возвращаем роль пользователя
    #         user.role = request.user.role
    #         # Сохраняем изменения
    #         user.save(update_fields=['first_name',
    #                                  'last_name',
    #                                  'email', 'bio', 'role'])
    #         # Возвращаем ответ
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     # Если данные сериализатора не прошли валидацию:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, *args, **kwargs):
    #     """Метод для удаления пользователя."""
    #     queryset = self.get_queryset()
    #     # Находим пользователя по его id
    #     user = get_object_or_404(queryset, username=kwargs['pk'])
    #     # Удаляем пользователя
    #     if user == request.user:
    #         return Response({'detail': 'Нельзя удалить самого себя.'},
    #                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
