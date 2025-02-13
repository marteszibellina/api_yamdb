"""Модель пользователя."""

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models

from users.constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH, Role
from users.validators import validate_username


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
        help_text='Укажите e-mail'
    )
    bio = models.TextField('bio', blank=True)
    role = models.CharField(
        'role',
        max_length=max(len(Role.name) for Role in Role),  # Автодлина
        choices=Role.choices,  # Выбор из кортежа
        default=Role.USER)  # Значение по умолчанию

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'user: {self.username} email: {self.email}'

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

    # Метод для генерации confirmation_code
    @property
    def generate_confirmation_code(self):
        """Генерирует код с использованием default_token_generator."""
        return default_token_generator.make_token(self)  # было сложно

    # Метод для проверки confirmation_code
    def check_confirmation_code(self, code):
        """Проверяет код с использованием default_token_generator."""
        return default_token_generator.check_token(self, code)  # было проще
