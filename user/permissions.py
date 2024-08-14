from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class IsUnauthenticated(permissions.BasePermission):
    """
    Custom permission to only allow access only to unauthenticated users.
    If a valid access JWT token is provided, the user is considered authenticated.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False

        # Check if a valid JWT token is provided
        jwt_authenticator = JWTAuthentication()
        try:
            raw_token = request.headers.get("Authorization", "Bearer null").split()[1]
            jwt_authenticator.get_validated_token(raw_token=raw_token)
            return False
        except InvalidToken:
            return True
