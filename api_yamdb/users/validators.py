"""Валидаторы. Созданы отдельно на всякий случай"""
import re
from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверка на уникальность username."""

    pattern = r'^[\w.@+-]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Имя пользователя содержит недопустимые символы.')

    return value
