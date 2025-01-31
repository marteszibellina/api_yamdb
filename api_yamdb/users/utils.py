from django.core.mail import send_mail

from .models import User


def send_confirmation_email(email):
    """Отправка кода подтверждения."""
    subject = 'Код подтверждения для YaMDB'
    message = f'Ваш код подтверждения: {User.confirmation_code}'
    from_email = 'noreply@yamdb.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
