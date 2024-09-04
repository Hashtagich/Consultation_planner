from django.db import models
from users.models import User


# Create your models here.

class Slot(models.Model):
    CHOICE_STATUS = (
        ('free', 'свободна'),
        ('reserved', 'зарезервирована'),
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
    client = models.OneToOneField(
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
        return f'{self.start_time} {self.end_time} {self.context}'
