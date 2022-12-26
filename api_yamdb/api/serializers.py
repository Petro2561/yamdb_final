from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации."""

    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                '"me" is unusable in usernamefield'
            )
        elif User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'User exist'
            )
        elif User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'one email can use only one user'
            )
        return data


class TokenObtainSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения JWT токена."""

    confirmation_code = serializers.CharField(source='password',
                                              required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = get_object_or_404(User, username=username)
        if not (user.password == password
           or user.check_password(password)):
            raise serializers.ValidationError(
                'Not Correct password for this user.'
            )
        return data


class UsersSerializer(serializers.ModelSerializer):
    """Пользовательский сериалайзер."""

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role',
        )
        read_only_fields = ['username', 'email', 'role']


class AdminRightsSerializer(serializers.ModelSerializer):
    """Административный сериалайзер."""

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Duplicated email.'
            )
        return data


class AdminPatchSerializer(serializers.ModelSerializer):
    """Админ класс для сериализации методов PATCH и PUT."""

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role',
        )


class CurrentTitleDefault:
    """Получение текущего тайтла."""

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['title']


class ReviewSerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Review."""

    author = SlugRelatedField(read_only=True, slug_field='username',
                              default=serializers.CurrentUserDefault())
    title = serializers.HiddenField(default=CurrentTitleDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Comment."""
    author = SlugRelatedField(read_only=True, slug_field='username',
                              default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GetTitleSerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Title: метод GET."""

    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            'id', 'name', 'rating',
            'year', 'description',
            'genre', 'category',
        )
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Title."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name',
            'year', 'description',
            'genre', 'category',
        )
        model = Title

    def validate_year(self, value):
        year = datetime.today().year + 1
        if year < value:
            raise serializers.ValidationError(
                'Год произведения должен быть не больше текущего года.'
            )
        return value
