from rest_framework import serializers
from django.contrib.auth import get_user_model
from reviews.models import category, comment, genre, review, title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''Преобразование данных класса User'''

    class Meta:
        model = User
        lookup_field = 'username'
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class RoleSerializer(serializers.ModelSerializer):
    '''Преобразование данных класса Role'''
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class SignUpSerializer(serializers.ModelSerializer):
    '''Преобразование данных класса SignUp.
    Проверка на допустимые символы и запрещённый ник'''

    username = serializers.CharField(max_length=150,)
    email = serializers.EmailField(max_length=254,)

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    '''Преобразование данных Tokena.'''

    username = serializers.CharField(max_length=150, required=True,)
    confirmation_code = serializers.CharField(required=True,)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class TitleSerializer(serializers.ModelSerializer):
    '''Преобразование данных Title.'''

    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = title.Title
        fields = (
            'id',
            'name',
            'year',
            'genre',
            'category',
            'description',
            'rating'
        )
        read_only_fields = ('rating',)


class CategorySerializer(serializers.ModelSerializer):
    '''Преобразование данных Category.'''

    class Meta:
        model = category.Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    '''Преобразование данных Genre.'''

    class Meta:
        model = genre.Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    '''Преобразование данных Title при чтении.'''

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = title.Title
        fields = (
            'id',
            'name',
            'year',
            'genre',
            'category',
            'description',
            'rating'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    '''Преобразование данных Title при создании.'''
    genre = serializers.SlugRelatedField(
        queryset=genre.Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=category.Category.objects.all(),
        slug_field='slug'
    )
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = title.Title
        fields = (
            'id',
            'name',
            'year',
            'genre',
            'category',
            'description',
            'rating'
        )
        read_only_fields = ('rating',)


class ReviewSerializer(serializers.ModelSerializer):
    '''Преобразование данных Review.'''

    class Meta:
        model = review.Review
        fields = ('id', 'title', 'author', 'text', 'pub_date', 'score')


class CommentSerializer(serializers.ModelSerializer):
    '''Преобразование данных Comment.'''

    class Meta:
        model = comment.Comment
        fields = ('review', 'author', 'pub_date', 'text')
