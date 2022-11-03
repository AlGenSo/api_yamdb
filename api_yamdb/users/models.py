from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    '''Кастомная модель User'''

    ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    )

    username = models.CharField(
        verbose_name='Ник пользователя',
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.TextField(
        verbose_name='Роль пользователя',
        blank=True,
        choices=ROLES,
        default='user'
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=6
    )

    class Meta:

        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):

        return str(self.username)

    @property
    def is_admin(self):

        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):

        return self.role == 'moderator'
