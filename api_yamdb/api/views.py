from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework import exceptions
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from .serializers import (
    SignUpSerializer, TokenObtainSerializer,
    UsersSerializer, AdminRightsSerializer,
    AdminPatchSerializer, ReviewSerializer,
    CommentSerializer, CategorySerializer,
    GenreSerializer, TitleSerializer,
    GetTitleSerializer
)
from users.models import User
from reviews.models import Review, Title, Genre, Category
from .permissions import (
    AdminOnly, AdminOrReadOnly,
    IsAuthorOrReadOnly
)
from .mixins import CustomHandlerModelViewSet, GetPostDeleteViewset
from .filters import TitlesFilter


class SignUpViewSet(APIView):
    """Класс для регистрации."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        password = BaseUserManager().make_random_password()
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            password=make_password(password)
        )
        send_mail(
            'confirmation_code',
            str(password),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[serializer.data['email']],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainViewSet(APIView):
    """Класс для получения токена."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.data['username']
        )
        return Response(
            {'token': user.token},
            status=status.HTTP_200_OK
        )


class AdminViewSet(ModelViewSet):
    """Класс для администратора."""

    serializer_class = AdminRightsSerializer
    permission_classes = [AdminOnly]
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['=username']

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return AdminPatchSerializer
        return AdminRightsSerializer

    @action(methods=['GET', 'PATCH'],
            detail=False,
            name='me',
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = UsersSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def handle_exception(self, exc):
        if isinstance(exc, (exceptions.AuthenticationFailed,
                            exceptions.NotAuthenticated)):
            return Response(
                {'detail': 'permissions denied.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if isinstance(exc, exceptions.ValidationError):
            return Response(
                exc.detail,
                status=status.HTTP_400_BAD_REQUEST
            )
        if isinstance(exc, exceptions.MethodNotAllowed):
            return Response(
                exc.detail,
                status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return Response(
            {'detail': f'{exc}'},
            status=status.HTTP_403_FORBIDDEN
        )


class ReviewViewSet(CustomHandlerModelViewSet):
    """Описание вьюсета для работы с моделью Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_serializer_context(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return {'title': title,
                'request': self.request}

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(CustomHandlerModelViewSet):
    """Описание вьюсета для работы с моделью Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    @staticmethod
    def __get_review(kwargs):
        review = get_object_or_404(
            Review,
            pk=kwargs.get('review_id'),
            title=kwargs.get('title_id')
        )
        return review

    def get_queryset(self):
        review = self.__get_review(self.kwargs)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = self.__get_review(self.kwargs)
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(CustomHandlerModelViewSet):
    """Описание вьюсета для работы с моделью Title."""

    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('GET', 'LIST'):
            return GetTitleSerializer
        return TitleSerializer


class GenreViewSet(GetPostDeleteViewset):
    """Описание вьюсета для работы с моделью Genre"""

    serializer_class = GenreSerializer
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)


class CategoryViewSet(GetPostDeleteViewset):
    """Описание вьюсета для работы с моделью Category"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)
