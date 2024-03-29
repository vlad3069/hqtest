from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class Group(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        'Название',
        unique=True,
        max_length=100,
        help_text='Введите название',
    )
    usersInGroup = models.ManyToManyField(
        User,
        related_name='group_users',
    )

    def __str__(self):
        return (f'Группа {self.name} - '
                f'Количество участников {self.usersInGroup.count()}')
