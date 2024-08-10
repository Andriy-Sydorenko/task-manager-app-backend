from drf_spectacular.utils import OpenApiExample, extend_schema

USER_REGISTRATION_DOCS = {
    "post": extend_schema(
        summary="Register a new user",
        description="Register a new user with the provided email, nickname, and password.",
        examples=[
            OpenApiExample(
                "Example for registration",
                value={"email": "user@example.com", "nickname": "user123", "password": "password123"},
            )
        ],
    )
}

USER_LOGOUT_DOCS = {
    "post": extend_schema(
        summary="Logout a user",
        description="Logout a user by blacklisting the provided refresh token.",
        examples=[OpenApiExample("Example for logout", value={"refresh": "your_refresh_token_here"})],
    )
}
