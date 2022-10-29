from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from xml.dom import ValidationErr
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import permissions, filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from reviews.models import category, comment, genre, review, title
from users.models import User

from .permissions import Admin, AdminOrReadOnly, UserIsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer, UserSerializer,
                          RoleSerializer, SignUpSerializer, TokenSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = title.Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [AdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = genre.Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = category.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [UserIsAuthorOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        get_title = get_object_or_404(
            title.Title, pk=self.kwargs.get('title')
        )
        return review.Review.objects.filter(title=get_title)

    def perform_create(self, serializer):
        get_title = get_object_or_404(
            title.Title, pk=self.kwargs.get('title')
        )
        serializer.save(author=self.request.user, title=get_title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        get_review = get_object_or_404(
            review.Review, pk=self.kwargs.get('review')
        )
        return comment.Comment.objects.filter(review=get_review)

    def perform_create(self, serializer):
        get_review = get_object_or_404(
            review.Review, pk=self.kwargs.get('review')
        )
        serializer.save(author=self.request.user, review=get_review)


class UsersViewSet(viewsets.ModelViewSet):
    '''view-класс реализующий операции модели Users'''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (Admin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def about_user(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = RoleSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class GetApiToken(APIView):
    '''Получение JWT-токена'''

    def post(self, request):
        serializer = TokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class ApiSignup(APIView):
    '''Получение кода подтверждения на email.'''

    permission_classes = (permissions.AllowAny,)

    validators = [
        UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username'),
            message=('Такой Никнейм уже зарегистрирован!'),
        ),
        RegexValidator(
            regex=r'^[\w.@+-]+\\z',
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

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        user = serializer.save()

        email = request.data.get('email')
        user = User.objects.filter(email=email)

        if user.exists():
            user = user.get(email=email)

            return Response(
                {'message': 'Пользователь с такой электронной почтой уже '
                            'существует.'
                            'Код подтверждения отправлен повторно. '
                 },
                status=status.HTTP_400_BAD_REQUEST
            )

        email_body = (
            f'Код подтверждения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
