from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (ADMIN, MODERATOR, USER, ROLES, NAME_MAX_LENGTH,
                        EMAIL_MAX_LENGTH)
from .validators import validate_username, validate_email


class User(AbstractUser):
    """Модель пользователя."""

    ROLE_CHOICES = ROLES

    username = models.CharField(
        'username', max_length=NAME_MAX_LENGTH, unique=True, db_index=True,
        validators=[validate_username],
        help_text='Укажите никнейм пользователя'
    )
    email = models.EmailField(
        'email', max_length=EMAIL_MAX_LENGTH, unique=True, db_index=True,
        validators=[validate_email], help_text='Укажите e-mail'
    )
    first_name = models.CharField('first name',
                                  max_length=NAME_MAX_LENGTH, blank=True)
    last_name = models.CharField('last name',
                                 max_length=NAME_MAX_LENGTH, blank=True)
    bio = models.TextField('bio', blank=True, null=True)
    role = models.CharField('role', max_length=10,
                            choices=ROLE_CHOICES, default=USER)
    confirmation_code = models.CharField(max_length=100, blank=True, null=True)

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.role == MODERATOR

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'],
                                    name='unique_username_email')
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
