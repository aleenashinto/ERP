from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    HR = "HR", "HR"
    MANAGER = "MANAGER", "Manager"
    TEAM_LEAD = "TEAM_LEAD", "Team Lead"
    EMPLOYEE = "EMPLOYEE", "Employee"
    ACCOUNTANT = "ACCOUNTANT", "Accountant"


class User(AbstractUser):
    """Custom user model used across the ERP for authentication and RBAC."""

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to="employee_photos/", blank=True, null=True)
    is_active_employee = models.BooleanField(default=True)  # Active/Inactive status
    date_joined_company = models.DateField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    # --- RBAC helpers ---
    @property
    def is_super_admin(self):
        return self.role == Role.SUPER_ADMIN

    @property
    def is_hr(self):
        return self.role == Role.HR

    @property
    def is_manager(self):
        return self.role in (Role.MANAGER, Role.TEAM_LEAD)


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reset_tokens")
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset token for {self.user.username}"
