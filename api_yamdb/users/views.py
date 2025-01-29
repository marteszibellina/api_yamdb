from django.contrib.auth import get_user_model
# from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
# from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from .permissions import IsAdminOrSuperuser
from .serializers import (
    CustomUserSerializer,
    SignUpSerializer,
    ConfirmationCodeSerializer,
    TokenSerializer
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


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Функция для получения токена"""

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    user = get_object_or_404(User, username=username)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)
