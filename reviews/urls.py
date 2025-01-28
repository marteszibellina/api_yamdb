"""reviews URL Configuration"""

from django.urls import path, include
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]
