from itertools import chain
from random import shuffle
from secrets import choice
from string import ascii_lowercase, digits, punctuation, ascii_uppercase

from backend.settings import EMAIL_HOST_USER
from celery import shared_task
from django.core.mail import EmailMultiAlternatives


def generate_temporary_password():
    lower = (choice(ascii_lowercase) for _ in range(4))
    upper = (choice(ascii_uppercase) for _ in range(1))
    digit = (choice(digits) for _ in range(1))
    special = (choice(punctuation) for _ in range(1))
    result = list(chain(lower, upper, digit, special))
    shuffle(result)
    password = ''.join(result)

    return password


def send_slot_notification(slot, user, action):
    title = f'{action} консультации на {slot.start_time.strftime("%d.%m.%Y")} в {slot.start_time.strftime("%H:%M")}'
    message = f'Специалист {user} {"не согласовал" if action == "Отмена" else "согласовал"} консультацию на {slot.start_time.strftime("%d.%m.%Y")} {slot.start_time.strftime("%H:%M")} - {slot.end_time.strftime("%H:%M")}'
    send_email(title, message, sub_list=slot.client.email)


@shared_task
def send_notifications(title, message, sub_list):
    try:
        if isinstance(sub_list, str):
            sub_list = [sub_list]

        msg = EmailMultiAlternatives(
            subject=title,
            body=message,
            from_email=EMAIL_HOST_USER,
            to=sub_list,
        )
        msg.send()
    except Exception as e:
        print(f'Произошла ошибка при отправке письма: {e}')


def send_email(title, message, sub_list):
    try:
        if isinstance(sub_list, str):
            sub_list = [sub_list]

        msg = EmailMultiAlternatives(
            subject=title,
            body=message,
            from_email=EMAIL_HOST_USER,
            to=sub_list,
        )
        msg.send()
    except Exception as e:
        print(f'Произошла ошибка при отправке письма: {e}')
