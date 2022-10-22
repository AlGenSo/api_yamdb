from django.db import models


class Category(models.Model):
    """Модель категории произведения."""
    
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
