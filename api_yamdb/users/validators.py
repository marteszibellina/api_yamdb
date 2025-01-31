import re

from django.core.exceptions import ValidationError

from .constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH


def validate_username(value):
    """Проверка username."""
    if len(value) > NAME_MAX_LENGTH:
        raise ValidationError('Имя пользователя слишком длинное.')
    if value.lower() == 'me':
        raise ValidationError('Имя "me" запрещено.')
    if not re.match(r'^[\w.@+-]+$', value):
        raise ValidationError(
            'Имя пользователя содержит недопустимые символы.')
    return value


def validate_email(value):
    """Проверка email."""
    from .models import User  # ленивый импорт

    if len(value) > EMAIL_MAX_LENGTH:
        raise ValidationError('Email слишком длинный.')
    return value
