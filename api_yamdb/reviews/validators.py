from datetime import datetime

from rest_framework.serializers import ValidationError


def validate_year(value):
    """Валидатор года выпуска произведения."""
    current_year = datetime.now().year
    if value > current_year:
        raise ValidationError(
            f'Год {value} не может быть больше {current_year}.'
        )
