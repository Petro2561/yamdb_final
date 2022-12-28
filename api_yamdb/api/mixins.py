from django.http.response import Http404
from rest_framework import exceptions, mixins, status, viewsets
from rest_framework.response import Response


class GetPostDeleteViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Класс для получения, создания и удаления."""

    def handle_exception(self, exc):
        if isinstance(exc, (exceptions.AuthenticationFailed,
                            exceptions.NotAuthenticated)):
            return Response(
                exc.detail,
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
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return Response(
            {'detail': f'{exc}'},
            status=status.HTTP_403_FORBIDDEN
        )


class CustomHandlerModelViewSet(viewsets.ModelViewSet):
    """Модель класс с кастомным обработчиком исключений."""

    def handle_exception(self, exc):
        if isinstance(exc, (exceptions.AuthenticationFailed,
                            exceptions.NotAuthenticated)):
            return Response(
                exc.detail,
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
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        if isinstance(exc, Http404):
            return Response(
                {'detail': 'No found object'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {'detail': f'{exc}'},
            status=status.HTTP_403_FORBIDDEN
        )
