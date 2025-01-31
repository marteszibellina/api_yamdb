from random import randint

from django.core.mail import send_mail


def send_confirmation_email(email):
    """Отправка кода подтверждения."""
    code = str(randint(111111, 999999))
    subject = 'Код подтверждения для YaMDB'
    message = f'Ваш код подтверждения: {code}'
    from_email = 'noreply@yamdb.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return code
