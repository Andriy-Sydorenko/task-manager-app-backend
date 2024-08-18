from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user import utils
from user.documentation import USER_LOGOUT_DOCS, USER_REGISTRATION_DOCS
from user.permissions import IsUnauthenticated
from user.serializers import (
    CustomTokenObtainPairSerializer,
    ForgotPasswordSerializer,
    RegistrationSerializer,
    ResetPasswordSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(email=self.request.user.email)

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


@extend_schema_view(**USER_REGISTRATION_DOCS)
class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = [
        IsUnauthenticated,
    ]
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(**USER_LOGOUT_DOCS)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            utils.invalidate_refresh_token(refresh_token)
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except KeyError:
            raise ValidationError(detail="Refresh token wasn't sent with logout request!")


class ForgotPasswordView(APIView):
    permission_classes = [
        IsUnauthenticated,
    ]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        if not email:
            raise ValidationError({"error": "Email is required"})

        user = get_user_model().objects.get(email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # TODO: here should be frontend URL
        reset_link = f"{settings.FRONTEND_URL}/reset-password/?uid={uid}&token={token}"
        print(reset_link)

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


class ResetPasswordView(APIView):
    permission_classes = [IsUnauthenticated]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        if not uidb64 or not token or not new_password:
            raise ValidationError("uid, token and new_password are required")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise ValidationError({"error": "Invalid uid"})

        if user and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            raise ValidationError("Reset password link is expired!")
