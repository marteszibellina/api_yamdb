"""Валидаторы для reviews и users."""

import re
from datetime import datetime

from django.core.exceptions import ValidationError

from api.constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH

# Тесты на проверку количества символов в username и email по длине по адресу:
# tests\test_00_user_registration.py:
# 90: def test_00_singup_length_and_simbols_validation():
# ссылаются на файл tests\utils.py:
# 39: invalid_data_for_username_and_email_fields
# которые не отображаются в VS Code Testing.
# Поэтому проверка осталась неизменённой.


def validate_username(value):
    """Проверка username."""
    if len(value) > NAME_MAX_LENGTH:
        raise ValidationError('Длина имени не должна превышать 150 символов.')
    if value.lower() == 'me':
        raise ValidationError('Имя "me" запрещено.')
    # Работа с недопустимыми символами
    invalid_chars = re.sub(r'[\w.@+-]', '', value)
    if invalid_chars:
        raise ValidationError(
            f'Имя пользователя содержит недопустимые символы {invalid_chars}.'
        )
    return value


def validate_email(value):
    """Проверка email."""
    if len(value) > EMAIL_MAX_LENGTH:
        raise ValidationError('Длина почты не должна превышать 254 символов.')
    if '@' not in value:
        raise ValidationError('Некорректная почта.')
    return value


def validate_year(value):
    """Валидатор года выпуска произведения."""
    current_year = datetime.now().year
    if value > current_year:
        raise ValidationError(
            f'Год {value} не может быть больше {current_year}.'
        )
