from rest_framework import permissions


class Admin(permissions.BasePermission):
    '''Кастомный пермишен, который расширит возможности встроенных пермишенов
    и разрешит полный доступ к объекту только админу(суперюзеру)'''

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )


class AdminOrReadOnly(permissions.BasePermission):
    '''Кастомный пермишен, который даст доступ на уровне админа'''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class AdminOrModeratorOrAuthor(permissions.BasePermission):
    '''Кастомный пермишен, который даст доступ на уровне
    админа, модератора или автора'''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )