"""Константы приложений revews и users."""

from django.db import models

MAX_NAME_LENGTH = 256
MAX_SLUG_LENGTH = 50
MAX_TEXT_LENGTH = 5000
MAX_COMMENT_LENGTH = 200
MAX_SCORE = 10
MIN_SCORE = 1
TEXT_SLICE = 10
NAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254
CONFIRMATION_CODE_LENGTH = 100


class Role(models.TextChoices):
    """Роли пользователей."""

    ADMIN = 'admin', 'Администратор'
    MODERATOR = 'moderator', 'Модератор'
    USER = 'user', 'Пользователь'
