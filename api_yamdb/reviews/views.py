# """Вьюсеты для моделей отзывов и комментариев."""

# from rest_framework import viewsets
# from rest_framework.exceptions import ValidationError
# from rest_framework.permissions import IsAuthenticatedOrReadOnly

# from .models import Comments, Review
# from .serializers import CommentSerializer, Reviewerializer
# from .permissions import IsAuthorOrReadOnly, IsAdminOrModerator


# class ReviewViewSet(viewsets.ModelViewSet):
#     """Вьюсет для отзывов"""

#     queryset = Review.objects.all()
#     serializer_class = Reviewerializer
#     permission_classes = (
#         IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly | IsAdminOrModerator)

#     def perform_create(self, serializer):
#         """Создание отзыва с автоматическим созданием автора."""
#         # Проверка уникальности отзыва на уровне логики вьюсета
#         # Находим название произведения
#         title = serializer.validated_data['title']
#         # Проверяем, что пользователь не оставлял отзыв на это произведение
#         if Review.objects.filter(title=title,
#                                   author=self.request.user).exists():
#             # Если пользователь уже оставлял отзыв, то возвращаем ошибку
#             raise ValidationError('Вы уже оставляли отзыв на это произведение')
#         serializer.save(author=self.request.user)


# class CommentViewSet(viewsets.ModelViewSet):
#     """Вьюсет для комментариев"""

#     queryset = Comments.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = (
#         IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly | IsAdminOrModerator)

#     def perform_create(self, serializer):
#         """Создание комментария с автоматическим созданием автора."""
#         serializer.save(author=self.request.user)
