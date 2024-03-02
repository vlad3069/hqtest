from django.db import models

from product.models import Product


class Lesson(models.Model):
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
    videoUrl = models.URLField(
        'Ссылка на видео',
        null=False,
        unique=True,
        help_text='Введите ссылку на видео',
    )

    def __str__(self):
        return (f'Название: {self.name[:15]}')
