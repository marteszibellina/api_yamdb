from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models

from .constants import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH


ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLES = [
    (ADMIN, 'администратор'),
    (MODERATOR, 'модератор'),
    (USER, 'пользователь')
]


def validate_username(username):
    """Проверяем юзернейм на соответствие правилам."""
    if username == 'me':
        raise ValidationError(
            'Невозможно использовать "me" в качестве никнейма.'
        )
    if len(username) > NAME_MAX_LENGTH:
        raise ValidationError(
            f'Никнейм не может превышать {NAME_MAX_LENGTH} символов.'
        )
    # Позже здесь будет еще одна проверка
    # на соответствие паттерну ^[\\w.@+-]+\\Z'
    return username


def validate_email(email):
    """Проверяем email на количество символов."""
    if len(email) > EMAIL_MAX_LENGTH:
        raise ValidationError(
            f'Email не может превышать {EMAIL_MAX_LENGTH} символов.'
        )
    return email


class CustomUser(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        unique=True,
        max_length=NAME_MAX_LENGTH,
        validators=(
            MaxLengthValidator, validate_username
        ),
        verbose_name='Никнейм пользователя',
        help_text='Укажите никнейм пользователя',
    )
    email = models.EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        validators=(
            MaxLengthValidator, validate_email
        ),
        verbose_name='Электронная почта пользователя',
        help_text='Укажите e-mail'
    )
    first_name = models.CharField(
        blank=True,
        max_length=NAME_MAX_LENGTH,
        validators=(MaxLengthValidator,),
        verbose_name='Имя пользователя',
        help_text='Укажите имя'
    )
    last_name = models.CharField(
        blank=True,
        max_length=NAME_MAX_LENGTH,
        validators=(MaxLengthValidator,),
        verbose_name='Фамилия пользователя',
        help_text='Укажите фамилию'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Био пользователя',
        help_text='Расскажите о себе',
    )
    role = models.TextField(
        max_length=max(len(role[0]) for role in ROLES),
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя',
        help_text='Укажите роль',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin_or_superuser(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR
