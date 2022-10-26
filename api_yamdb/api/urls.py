from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router = DefaultRouter()
router.register(r'title', TitleViewSet, basename='title')
router.register(r'category', CategoryViewSet, basename='category')
router.register(
    r'review/(?P<review_id>\d+)/comments', CommentViewSet, basename='comment'
)
router.register(r'genre', GenreViewSet, basename='genre')
router.register(r'review', ReviewViewSet, basename='review')

urlpatterns = [
    path('v1/', include(router.urls))
]
