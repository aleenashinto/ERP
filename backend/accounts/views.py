import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, PasswordResetToken
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


class LoginView(TokenObtainPairView):
    """POST username & password -> access + refresh tokens + user profile."""
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    """POST refresh token -> blacklists it (requires token_blacklist app if enabled)."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return Response({"detail": "Logged out."}, status=status.HTTP_205_RESET_CONTENT)


class RegisterView(generics.CreateAPIView):
    """HR/Admin registers a new employee account."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH the logged-in user's own profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Password changed successfully."})


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
            token = secrets.token_urlsafe(32)
            PasswordResetToken.objects.create(user=user, token=token)
            reset_link = f"{settings.CORS_ALLOWED_ORIGINS[0]}/reset-password?token={token}"
            send_mail(
                "Reset your Office ERP password",
                f"Click the link to reset your password: {reset_link}\nThis link expires in 1 hour.",
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, "DEFAULT_FROM_EMAIL") else "no-reply@officeerp.local",
                [email],
                fail_silently=True,
            )
        except User.DoesNotExist:
            pass  # Don't reveal whether the email exists
        return Response({"detail": "If that email exists, a reset link has been sent."})


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_value = serializer.validated_data["token"]
        try:
            reset_token = PasswordResetToken.objects.get(token=token_value, used=False)
        except PasswordResetToken.DoesNotExist:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        if reset_token.created_at < timezone.now() - timedelta(hours=1):
            return Response({"detail": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_token.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        reset_token.used = True
        reset_token.save()
        return Response({"detail": "Password reset successfully."})
