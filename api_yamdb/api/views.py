"""Вьюсеты для работы с моделями приложений reviews и users."""
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                             IsAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitleReadSerializer,
                             TitleSerializer, TokenObtainSerializer,
                             UserSerializer)
from api.utils import send_confirmation_email
from api.viewset import CategoryGenreViewSet
from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User


class CategoryViewSet(CategoryGenreViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Title."""

    queryset = (
        Title.objects.all().annotate(
            rating=Avg('reviews__score')
        ).order_by('name')
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly
    )
    http_method_names = ('delete', 'get', 'patch', 'post')

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            title=self.get_title(),
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            review=self.get_review(),
            author=self.request.user
        )


class SignUpViewSet(viewsets.ViewSet):
    """Вьюсет для регистрации пользователей."""

    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Регистрация пользователя и повторная отправка кода."""
        serializer = SignUpSerializer(data=request.data)

        # Если данные валидны
        if serializer.is_valid():
            # Получаем username и email
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']

            # Проверяем, что user и email существуют
            user_username = User.objects.filter(username=username).first()
            user_email = User.objects.filter(email=email).first()

            # Если пользователь с таким username и email уже существует (1)
            if user_username and user_email:
                # Если username совпадает, но email не совпадает
                if user_username != user_email:
                    return Response(
                        {'error': 'Этот username уже есть с другим email'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Если email совпадает, обновляем код подтверждения
                user_username.confirmation_code = send_confirmation_email(
                    user_username)
                # Отправляем новый код подтверждения
                return Response(
                    {'message': 'Код подтверждения отправлен повторно.'},
                    status=status.HTTP_200_OK
                )

            # Если пользователя с таким username нет, но с таким email есть (2)
            if user_email and user_username is None:
                return Response(
                    {'error': 'Этот email уже есть с другим username'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Если пользователь с таким username есть, но с таким email нет (3)
            if user_username and user_email is None:
                return Response(
                    {'error': 'Этот username уже есть с другим email'},
                    status=status.HTTP_400_BAD_REQUEST)

            # Если пользователь с таким username и email нет (4)
            # Создаем пользователя
            if user_username is None and user_email is None:
                user = User.objects.create_user(
                    username=username, email=email)
                # Генерируем и отправляем код подтверждения
                user.confirmation_code = send_confirmation_email(user)
                # Сохраняем пользователя
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        # Если данные не валидны
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Создадим вью-функцию для получения JWT-токена по коду подтверждения
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token_obtain_view(request):
    """Вью-функция для получения JWT-токена по коду подтверждения."""

    # Создаем сериализатор
    serializer = TokenObtainSerializer(data=request.data)

    # Проверяем, что данные валидны
    if serializer.is_valid():
        # Получаем данные из сериализатора
        username = serializer.validated_data['username']
        # Если сериализатор проверил валидность, то confirmation_code уже есть
        user = User.objects.filter(username=username).first()

        # Генерируем JWT-токен
        # Для этого идеально подойдет RefreshToken
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Очищаем код подтверждения после успешной аутентификации
        user.confirmation_code = ''  # None - не очень хорошо
        # Сохраняем изменения
        user.save(update_fields=['confirmation_code'])

        return Response(
            {'access': access_token, 'refresh': str(refresh)},
            status=status.HTTP_200_OK
        )
    # Если данные не валидны
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    # Права доступа есть только у администратора.
    permission_classes = (IsAdmin,)

    # Выводим всех пользователей
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

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
