from random import randint

from django.core.mail import send_mail


def send_code(user):
    """Функция отправки кода подтверждения на почту пользователя."""
    code = str(randint(111111, 999999))
    send_mail(
        subject='Код подтверждения',
        message=f'Вы получили код подтверждения: {code}',
        from_email=['admin@yamdb.ru'],
        recipient_list=[user.email],
        fail_silently=True,
    )