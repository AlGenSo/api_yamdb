from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import category, comment, genre, review, title

from .permissions import AdminOrReadOnly, UserIsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


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
