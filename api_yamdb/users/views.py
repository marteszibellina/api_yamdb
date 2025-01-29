from django.contrib.auth import get_user_model
# from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminOrSuperuser
from .serializers import (
    CustomUserSerializer,
    SignUpSerializer,
    ConfirmationCodeSerializer
)


User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminOrSuperuser,)


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)


class GetTokenViewSet():
    pass
#     serializer_class = ConfirmationCodeSerializer
#     permission_classes = (AllowAny,)
