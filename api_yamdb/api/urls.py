from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from django.urls import include, path

from users.views import CustomUserViewSet, SignUpViewSet, get_token
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)


router_v1 = SimpleRouter()
users_router_v1 = DefaultRouter()
auth_router_v1 = DefaultRouter()
users_router_v1.register('users', CustomUserViewSet, basename='users')
auth_router_v1.register('signup', SignUpViewSet, basename='signup')
router_v1.register("categories", CategoryViewSet, basename="categories")
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register(
    r"titles/(?P<title_id>[0-9]+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments",
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('', include(users_router_v1.urls)),
    path('auth/', include(auth_router_v1.urls)),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', get_token),
]
