from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Allows access only to users with 'admin' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.name == 'admin'
