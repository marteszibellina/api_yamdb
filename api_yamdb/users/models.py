import re
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from .constants import (ADMIN,
                        MODERATOR,
                        USER,
                        ROLES,
                        NAME_MAX_LENGTH,
                        EMAIL_MAX_LENGTH)
# from .validators import validate_username


class User(AbstractUser):
    """Модель пользователя."""

    ROLE_CHOICES = ROLES

    username = models.CharField(
        'username',
        max_length=NAME_MAX_LENGTH,
        unique=True,
        db_index=True,
        # validators=[validate_username],
        help_text='Укажите никнейм пользователя',)
    email = models.EmailField(
        'email',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        db_index=True,
        help_text='Укажите e-mail',)
    first_name = models.CharField(
        'first name',
        max_length=NAME_MAX_LENGTH,
        blank=True,
        help_text='Укажите имя пользователя',)
    last_name = models.CharField(
        'last name',
        max_length=NAME_MAX_LENGTH,
        blank=True,
        help_text='Укажите фамилию пользователя',)
    bio = models.TextField(
        'bio',
        blank=True,
        null=True,
        help_text='Укажите биографию пользователя',)
    role = models.CharField(
        'role',
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,)
    confirmation_code = models.CharField(max_length=100, blank=True, null=True)

    def validate_username(self, value):
        """Проверка на уникальность username."""
        if self.username == 'me':
            raise ValidationError('Нельзя использовать имя "me".')
        pattern = r'^[\w.@+-]+$'
        if not re.match(pattern, value):
            raise ValidationError(
                'Имя пользователя содержит недопустимые символы.')
        return value

    def validate_email(self, value):
        """Проверка на уникальность email."""
        if User.objects.filter(email=value).exists():
            raise ValidationError(
                'Пользователь с таким email уже существует')
        return value

    def __str__(self):
        """Возвращает username."""
        return self.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
