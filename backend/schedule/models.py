from django.db import models
from users.models import User


# Create your models here.

class Slot(models.Model):
    CHOICE_STATUS = (
        ('free', 'свободна'),
        ('reserved', 'зарезервирована'),
        ('agreement', 'на согласовании'),
        ('completed', 'завершена')
    )

    specialist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='time_slots_specialist',
        verbose_name='Специалист'
    )
    start_time = models.DateTimeField(
        verbose_name='Дата и время начала консультации'
    )
    end_time = models.DateTimeField(
        verbose_name='Дата и время окончания консультации'
    )
    context = models.CharField(
        verbose_name='Описание услуги',
        max_length=255,
        null=True,
        blank=True
    )
    cost = models.DecimalField(
        verbose_name='Стоимость услуги',
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=50,
        choices=CHOICE_STATUS,
        default='free'
    )
    client = models.ForeignKey(
        User,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        related_name='time_slots_client',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Cлот'
        verbose_name_plural = 'Слоты'
        # ordering = ('-start_time',)

    def __str__(self):
        return f'Консультация {self.start_time.strftime("%d.%m.%Y")} с {self.start_time.strftime("%H:%M")} по {self.end_time.strftime("%H:%M")} | Спец - {self.specialist}'

    def change_status(self, status='free'):
        if status not in dict(self.CHOICE_STATUS):
            raise ValueError(f"Неверный статус. Возможные значения: {', '.join(dict(self.CHOICE_STATUS).keys())}")
        if status == 'free':
            self.client = None

        self.status = status


class Comment(models.Model):
    CHOICE_REASON = (
        ('None', 'Нет причины'),
        ('force majeure', 'Форс-мажор'),
        ('got sick', 'Заболел'),
        ('schedule conflict', 'Конфликт расписания')
    )

    reason = models.CharField(
        verbose_name='Причина',
        max_length=50,
        choices=CHOICE_REASON,
        default='force majeure'
    )

    text = models.CharField(
        verbose_name='Текст комментария',
        max_length=255,
        null=True,
        blank=True
    )

    client = models.ForeignKey(
        User,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        related_name='comment_client',
        null=True,
        blank=True
    )

    slot = models.ForeignKey(
        Slot,
        verbose_name='Слот',
        on_delete=models.CASCADE,
        related_name='comments_slot'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        # ordering = ('-id',)

    def __str__(self):
        return f'{self.reason}| {self.text}| клиент - {self.client}'
