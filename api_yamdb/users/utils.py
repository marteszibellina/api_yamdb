"""Модуль для отправки кода подтверждения."""
import secrets

from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_email(user):  # Меняем email на user
    """Отправка кода подтверждения."""
    confirmation_code = secrets.token_hex(16)
    subject = 'Код подтверждения для YaMDB'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = settings.DEFAULT_FROM_EMAIL  # settings.py
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    return confirmation_code
