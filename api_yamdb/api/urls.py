from rest_framework.routers import SimpleRouter

from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

router_v1 = routers.DefaultRouter()
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
    path("v1/", include(router_v1.urls)),
    path('v1/', include('users.urls')),
]