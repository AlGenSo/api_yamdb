from django.db import models


class Genre(models.Model):
    """Модель жанра произведения."""
    
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
