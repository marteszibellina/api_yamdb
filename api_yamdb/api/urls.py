"""URLs для приложения api, работающая с Reviews и Users."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignUpViewSet, TitleViewSet, UserViewSet,
                       token_obtain_view)

router_v1 = DefaultRouter()  # Роутер API v1

# Регистрация пользователя
router_v1.register('auth/signup', SignUpViewSet, basename='signup')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

router_v1_simple = SimpleRouter()  # Для гибкой настройки

# Регистрация более сложных URL с параметрами
router_v1_simple.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1_simple.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    # Подключение общего эндпоинта
    path('v1/', include([
        # Авторизация
        path('auth/token/', token_obtain_view),
        # Подключение роутера
        path('', include(router_v1.urls)),
        # Подключение роутера для сложных URL
        path('', include(router_v1_simple.urls)),
    ])),
]
