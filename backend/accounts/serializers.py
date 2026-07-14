from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds user profile info (including role) to the JWT login response."""

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "full_name": self.user.get_full_name(),
            "role": self.user.role,
            "photo": self.user.photo.url if self.user.photo else None,
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name", "full_name",
            "role", "phone", "photo", "is_active_employee", "date_joined_company",
            "email_verified", "is_staff", "date_joined",
        ]
        read_only_fields = ["id", "date_joined", "is_staff"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[password_validation.validate_password])

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "role", "phone"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[password_validation.validate_password])

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[password_validation.validate_password])
