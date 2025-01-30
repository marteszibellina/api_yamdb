from rest_framework.routers import DefaultRouter

from django.urls import include, path

from users.views import (SignUpViewSet, CustomTokenObtainPairView, UserViewSet,
                         UserMeViewSet)
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)


router_v1 = DefaultRouter()
router_v1.register('auth/signup', SignUpViewSet, basename='signup')
router_v1.register('auth/token', CustomTokenObtainPairView, basename='token')
router_v1.register('users', UserViewSet)
router_v1.register('users/me', UserMeViewSet, basename='me')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    # path('', include(router_v1.urls)),
    path('auth/', include(router_v1.urls)),
    path('v1/', include(router_v1.urls)),
]
