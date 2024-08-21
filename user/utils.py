from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, Token

from user.models import User


def invalidate_refresh_token(refresh_token: Token) -> None:
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except TokenError as e:
        raise ValidationError(detail=e)


def create_reset_password_url(user: User) -> str:
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.FRONTEND_URL}/reset-password/?uid={uid}&token={token}"
    return reset_link


def set_new_user_password(uid: str, token: str, new_password: str) -> Response:
    if not uid or not token or not new_password:
        raise ValidationError("uid, token and new_password are required")

    try:
        decoded_id = force_str(urlsafe_base64_decode(uid))
        user = get_user_model().objects.get(pk=decoded_id)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        raise ValidationError({"error": "Invalid uid"})

    if user and default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    else:
        raise ValidationError("Reset password link is expired!")


def validate_password_length(password: str) -> str:
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    return password
