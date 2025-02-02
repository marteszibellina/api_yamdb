"""Валидаторы приложения users."""

import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверка username."""
    if value.lower() == 'me':
        raise ValidationError('Имя "me" запрещено.')
    # Работа с недопустимыми символами
    invalid_chars = re.sub(r'[\w.@+-]', '', value)
    if invalid_chars:
        raise ValidationError(
            f'Имя пользователя содержит недопустимые символы {invalid_chars}.'
        )
    return value
