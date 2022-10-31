from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from reviews.models import category, comment, genre, review, title
from users.models import User

from .filters import TitleFilter
from .permissions import Admin, AdminOrReadOnly, UserIsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleWriteSerializer, TitleReadSerializer,
                          UserSerializer, TokenSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = title.Title.objects.all()
    permission_classes = [AdminOrReadOnly, ]
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, )
    search_fields = ('name',)
    filterset_class = TitleFilter

    # def get_queryset(self):
    #     queryset = title.Title.objects.all()
    #     genre = self.request.query_params.get('genre__slug')
    #     return queryset.filter(genre__slug=genre)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer

        return TitleWriteSerializer


class CreateListDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class GenreViewSet(CreateListDeleteViewSet):
    queryset = genre.Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly, ]
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoryViewSet(CreateListDeleteViewSet):
    queryset = category.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly, ]
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [UserIsAuthorOrReadOnly, ]
    # pagination_class = PageNumberPagination

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
    permission_classes = [UserIsAuthorOrReadOnly, ]
    # pagination_class = PageNumberPagination

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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class GetApiToken(APIView):
    '''Получение JWT-токена и кода подтверждения'''

    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        serializer = TokenSerializer(data=request.data)

        if serializer.is_valid():
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiSignup(APIView):
    '''Регистрация и получение кода подтверждения на email.'''

    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )

        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()

        send_mail(
            subject="Код подтверждения",
            message=(
                f'Код подтверждения'
                f'для доступа регистрации: {confirmation_code}'
            ),
            from_email=None,
            recipient_list=[user.email],
        )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)