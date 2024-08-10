from rest_framework import permissions


class IsUnauthenticated(permissions.BasePermission):
    """
    Custom permission to only allow access only to unauthenticated users.
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated
