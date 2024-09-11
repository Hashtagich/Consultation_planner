from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from backend.settings import EMAIL_HOST_USER


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
