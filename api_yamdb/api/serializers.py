from xml.dom import ValidationErr

from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api_yamdb.users.models import User


class UserSerializer(serializers.ModelSerializer):
    '''Преобразование данных класса User'''

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SignUpSerializer(serializers.Serializer):
    '''Преобразование данных класса SignUp.
    Проверка на допустимые символы и запрещённый ник'''

    validators = [
        UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username'),
            message=('Такой Никнейм уже зарегистрирован!'),
        ),
        RegexValidator(
            queryset=User.objects.all(),
            fields=('username'),
            regex=r'^[\w.@+-]+$',
            message='Недопустимые символы! Только @/./+/-/_',
            code='invalid_username',
        ),
    ]

    def validate_username(self, username):
        '''Проверка ограничения для username:
        заперт на использование 'me'.'''

        if username == 'me':
            raise ValidationErr(
                'Нельзя использовать <me>!'
            )

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    '''Преобразование данных Tokena.'''

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
