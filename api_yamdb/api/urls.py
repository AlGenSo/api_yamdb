from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UsersViewSet, GetApiToken, ApiSignup,
                    CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet)

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(
    r'titles/(?P<title>\d+)/reviews',
    ReviewViewSet, basename='review')
router.register('users', UsersViewSet, basename='user')
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', GetApiToken.as_view(), name='get_token'),
    path('v1/auth/signup/', ApiSignup.as_view(), name='signup')
]
