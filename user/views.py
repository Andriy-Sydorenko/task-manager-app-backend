from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user import documentation, utils
from user.permissions import IsUnauthenticated
from user.serializers import (
    CustomTokenObtainPairSerializer,
    ForgotPasswordSerializer,
    LogoutSerializer,
    MeSerializer,
    MeUpdateSerializer,
    RegistrationSerializer,
    ResetPasswordSerializer,
)


@extend_schema_view(**documentation.ME_DOCS)
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = MeUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@extend_schema_view(**documentation.USER_REGISTRATION_DOCS)
class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            if get_user_model().objects.filter(email=serializer.validated_data["email"]).exists():
                raise ValidationError({"email": "User with this email already exists."})
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(**documentation.USER_LOGIN_DOCS)
class LoginView(TokenObtainPairView):
    permission_classes = [
        IsUnauthenticated,
    ]
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(**documentation.USER_LOGOUT_DOCS)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            utils.invalidate_refresh_token(refresh_token)
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except KeyError:
            raise ValidationError(detail="Refresh token wasn't sent with logout request!")


@extend_schema_view(**documentation.FORGOT_PASSWORD_DOCS)
class ForgotPasswordView(APIView):
    permission_classes = [
        IsUnauthenticated,
    ]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        if not email:
            raise ValidationError({"error": "Email is required"})

        user = get_user_model().objects.get(email=email)
        reset_link = utils.create_reset_password_url(user)
        subject = "Password Reset Request"
        message = render_to_string(
            "password_reset_email.html",
            {
                "user": user,
                "reset_link": reset_link,
            },
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                email,
            ],
            html_message=message,
        )

        return Response(
            {"detail": "Password reset link has been sent to your email. Please, check your spam folder."},
            status=status.HTTP_200_OK,
        )


@extend_schema_view(**documentation.RESET_PASSWORD_DOCS)
class ResetPasswordView(APIView):
    permission_classes = [IsUnauthenticated]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        return utils.set_new_user_password(uid, token, new_password)
