import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models

from .category import Category
from .genre import Genre

year_now = dt.datetime.now().year()


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=100,
        help_text='Название произведения'
    )
    year = models.IntegerField(
        validators=[
            MaxValueValidator(year_now)
        ],
        help_text='Дата'
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text='Описание'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        verbose_name='Произведение',
        related_name='genre',
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='category'
    )

    def __str__(self):

        return self.name
