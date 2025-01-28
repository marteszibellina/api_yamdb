from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet, SignUpViewSet, GetTokenViewSet

users_router_v1 = DefaultRouter()
auth_router_v1 = DefaultRouter()

users_router_v1.register('users', CustomUserViewSet, basename='users')
auth_router_v1.register('signup', SignUpViewSet, basename='signup')
auth_router_v1.register('token', GetTokenViewSet, basename='get_token')

urlpatterns = [
    path('', include(users_router_v1.urls)),
    path('auth/', include(auth_router_v1.urls)),
]
