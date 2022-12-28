from api.views import (AdminViewSet, CategoryViewSet, CommentViewSet,
                       GenreViewSet, ReviewViewSet, SignUpViewSet,
                       TitleViewSet, TokenObtainViewSet)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users',
                AdminViewSet,
                basename='admin-rights')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('api/v1/auth/signup/', SignUpViewSet.as_view()),
    path('api/v1/auth/token/', TokenObtainViewSet.as_view()),
    path('api/v1/', include(router.urls)),
]
