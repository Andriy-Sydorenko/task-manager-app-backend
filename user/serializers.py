from rest_framework import serializers

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
