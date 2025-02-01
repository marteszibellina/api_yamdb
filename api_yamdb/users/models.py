"""Модель пользователя."""

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models

from api.constants import (CONFIRMATION_CODE_LENGTH, EMAIL_MAX_LENGTH,
                           NAME_MAX_LENGTH, Role)
from api.validators import validate_email, validate_username


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        'username',
        max_length=NAME_MAX_LENGTH,
        unique=True,
        validators=[validate_username],
        help_text='Укажите никнейм пользователя'
    )
    email = models.EmailField(
        'email',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        validators=[validate_email],
        help_text='Укажите e-mail'
    )
    bio = models.TextField('bio', blank=True)
    role = models.CharField(
        'role',
        max_length=max(len(Role.name) for Role in Role),  # Автодлина
        choices=Role.choices,  # Выбор из кортежа
        default=Role.USER)  # Значение по умолчанию
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True,
        null=True)

    # Метод для генерации confirmation_code
    @property
    def generate_confirmation_code(self):
        """Генерирует код с использованием default_token_generator."""
        return default_token_generator.make_token(self)  # было сложно

    # Метод для проверки confirmation_code
    def check_confirmation_code(self, code):
        """Проверяет код с использованием default_token_generator."""
        return default_token_generator.check_token(self, code)  # было проще

    # Методы для проверки ролей
    # Добавим is_superuser и is_staff, а Role.ADMIN возьмём из модели Roles
    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.role == Role.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.role == Role.MODERATOR

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'],
                                    name='unique_username_email')
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
