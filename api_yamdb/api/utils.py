"""Утилита для отправки кода подтверждения пользователю модели User."""

from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_email(user, confirmation_code):
    """Отправка кода подтверждения."""
    subject = 'Код подтверждения для YaMDB'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
