from drf_spectacular.utils import extend_schema

from user.serializers import (
    CustomTokenObtainPairSerializer,
    LogoutSerializer,
    MeSerializer,
    MeUpdateSerializer,
    ResetPasswordSerializer,
)

USER_REGISTRATION_DOCS = {
    "post": extend_schema(
        summary="Register a new user",
        description="Register a new user with the provided email, nickname, and password.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "example": "test@email.com"},
                    "nickname": {"type": "string", "example": "test_nickname"},
                },
                "additionalProperties": False,
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Enter a valid email address."},
                },
                "additionalProperties": False,
            },
        },
    )
}

USER_LOGIN_DOCS = {
    "post": extend_schema(
        summary="Login a user",
        description="Authenticate a user and return a pair of access and refresh tokens.",
        request=CustomTokenObtainPairSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {"refresh": {"type": "string"}, "access": {"type": "string"}},
                "additionalProperties": False,
            },
            400: {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "example": "No active account found with the given credentials."},
                },
                "additionalProperties": False,
            },
        },
    )
}

# TODO: EXAMPLE FOR DOCS
USER_LOGOUT_DOCS = {
    "post": extend_schema(
        summary="Logout a user",
        description="Logout a user by blacklisting the provided refresh token.",
        request=LogoutSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {"detail": {"type": "string", "example": "Successfully logged out."}},
                "additionalProperties": False,
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Refresh token wasn't sent with logout request"},
                },
                "additionalProperties": False,
            },
        },
    )
}

ME_DOCS = {
    "get": extend_schema(
        summary="Retrieve the authenticated user's profile",
        description="Retrieve the authenticated user's profile.",
        responses={200: MeSerializer},
    ),
    "patch": extend_schema(
        summary="Update the authenticated user's profile",
        description="Update the authenticated user's profile.",
        request=MeUpdateSerializer,
        responses={200: MeUpdateSerializer},
    ),
}

RESET_PASSWORD_DOCS = {
    "post": extend_schema(
        summary="Reset user password",
        description="Reset the user's password using the provided uid, token, and new password.",
        request=ResetPasswordSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {"detail": {"type": "string", "example": "Password has been reset successfully."}},
                "additionalProperties": False,
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Reset password link is expired!"},
                },
                "additionalProperties": False,
            },
        },
    )
}

FORGOT_PASSWORD_DOCS = {
    "post": extend_schema(
        summary="Send a password reset link",
        description="Send a password reset link to the user's email.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Password reset link has been sent to your email. Please, check your spam folder.",
                    }
                },
                "additionalProperties": False,
            },
            400: {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "example": "User with this email does not exist."},
                },
                "additionalProperties": False,
            },
        },
    )
}
