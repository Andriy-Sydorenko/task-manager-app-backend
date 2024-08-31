from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User
from user.utils import validate_password_length


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "nickname",
            "profile_picture",
            "date_joined",
        )


class MeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "nickname",
            "profile_picture",
            "password",
        )

    @staticmethod
    def validate_password(value):
        validate_password_length(value)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("password", "")
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["email"] = instance.email
        representation["date_joined"] = instance.date_joined
        return representation


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "nickname", "password")

    @staticmethod
    def validate_password(value):
        validate_password_length(value)
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            nickname=validated_data["nickname"],
        )
        user.set_password(validated_data["password"])
        user.save()


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


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    @staticmethod
    def validate_email(value):
        if not get_user_model().objects.filter(email=value).exists():
            raise ValidationError("User with this email does not exist.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
