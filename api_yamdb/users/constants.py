"""Константы."""

from django.db import models

NAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254
CONFIRMATION_CODE_LENGTH = 100


class Role(models.TextChoices):
    """Роли пользователей."""

    ADMIN = 'admin', 'Администратор'
    MODERATOR = 'moderator', 'Модератор'
    USER = 'user', 'Пользователь'
