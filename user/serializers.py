from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "nickname",
            "profile_picture",
            "date_joined",
        )


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "nickname", "password")

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            nickname=validated_data["nickname"],
        )
        user.set_password(validated_data["password"])
        user.save()
        user_data = self.to_representation(user)
        user_data.pop("password", None)
        return user_data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except AuthenticationFailed:
            raise ValidationError(
                {"email": "No active account found with the given credentials"}, code=status.HTTP_400_BAD_REQUEST
            )


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
