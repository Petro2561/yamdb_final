from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USERS_ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    role = models.CharField(
        choices=USERS_ROLES,
        default='user',
        max_length=15
    )
    bio = models.TextField(
        'Биография',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'auth_user'
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def token(self):
        return self.__get_jwt_token()

    def __get_jwt_token(self):
        try:
            timedelta = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        except Exception:
            raise KeyError(
                'Check settings SIMPLE_JWT access_token_lifetime'
            )
        expired_time = (datetime.now() + timedelta)
        token = jwt.encode(
            {'id': self.pk,
             'exp': expired_time},
            settings.SECRET_KEY,
            algorithm=settings.SIMPLE_JWT.get('ALGORITHM')
        )
        return token
