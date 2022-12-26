from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Пермишен только суперюзеры."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.is_staff
                     or request.user.is_admin))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.is_staff
                     or request.user.is_admin))


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, дающее возможность редактирования только владельцам объекта.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user
                    or request.user.is_superuser
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator')
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user == obj.author
                    or request.user.is_superuser
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator')
        return request.method in permissions.SAFE_METHODS


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешение, администратор либо чтение."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_superuser
                    or request.user.is_admin
                    )
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.is_superuser
                    or request.user.is_admin
                    )
        return request.method in permissions.SAFE_METHODS
