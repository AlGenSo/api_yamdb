from django.db import models

from users.models import User
from .title import Title


class Review(models.Model):
    """Модель отзыва на произведение."""
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

    def __str__(self):
        
        return self.text
