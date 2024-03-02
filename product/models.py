from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    start = models.DateTimeField(
        'Дата и время старта',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название',
        unique=True,
        max_length=200,
        help_text='Введите название',
    )
    minValue = models.PositiveIntegerField(
        'Минимальное количество юзеров в группе',
        null=False,
        default=0,
    )
    maxValue = models.PositiveIntegerField(
        'Максимальное количество юзеров в группе',
        null=False,
        default=10,
    )
    price = models.DecimalField(
        'Цена',
        help_text='Введите цену',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        ordering = ('-start',)

    def __str__(self):
        return (
            f'Автор: {str(self.author)} Название: {self.name[:15]}'
        )
