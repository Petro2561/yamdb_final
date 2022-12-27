import jwt

from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header
from django.conf import settings

from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """Класс авторицаяя пользователя по токену."""

    def authenticate(self, request):
        CORRECT_AUTH_HEADER_LENGTH = 2
        auth = get_authorization_header(request).split()
        auth_header_prefix = settings.SIMPLE_JWT.get('AUTH_HEADER_TYPES')
        if not auth:
            return None
        if len(auth) != CORRECT_AUTH_HEADER_LENGTH:
            return None
        prefix_key = auth[0].decode('utf8')
        token = auth[1].decode('utf8')
        if prefix_key not in auth_header_prefix:
            return None
        return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.SIMPLE_JWT.get('ALGORITHM')]
            )
        except Exception:
            raise exceptions.AuthenticationFailed('Wrong token')
        user_id = payload.get('user_id') or payload.get('id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            message = 'User does not exist Check Token.'
            raise exceptions.AuthenticationFailed(message)
        if not user.is_active:
            message = 'User deactivated.'
            raise exceptions.AuthenticationFailed(message)
        return user, token
