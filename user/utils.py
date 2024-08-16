from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, Token


def invalidate_refresh_token(refresh_token: Token) -> None:
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except TokenError as e:
        raise ValidationError(detail=e)
