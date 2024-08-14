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
    serializer_class = ForgotPasswordSerializer
    permission_classes = [
        IsUnauthenticated,
    ]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{request.build_absolute_uri('/reset-password/')}?uid={uid}&token={token}"

        # Send email
        subject = "Password Reset Request"
        message = render_to_string(
            "password_reset_email.html",
            {
                "user": user,
                "reset_link": reset_link,
            },
        )
        send_mail(subject, message, None, [user.email])

        return Response({"detail": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        pass
