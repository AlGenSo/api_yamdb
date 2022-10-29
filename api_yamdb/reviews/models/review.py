from django.db import models
from users.models import User

from .title import Title


class Review(models.Model):
    """Модель отзыва на произведение."""
    
    RATE_CHOICES = zip(range(1, 11), range(1, 11))
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'

    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Отзыв'
    )
    pub_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    score = models.IntegerField(choices=RATE_CHOICES, default=1)

    def __str__(self):

        return self.text
