"""Валидаторы для reviews и users."""

import re
from datetime import datetime

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


def validate_year(value):
    """Валидатор года выпуска произведения."""
    current_year = datetime.now().year
    if value > current_year:
        raise ValidationError(
            f'Год {value} не может быть больше {current_year}.'
        )
