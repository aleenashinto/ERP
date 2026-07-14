from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordResetToken


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "is_active_employee", "is_staff")
    list_filter = ("role", "is_active_employee", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("ERP Info", {"fields": ("role", "phone", "photo", "is_active_employee", "date_joined_company", "email_verified")}),
    )


admin.site.register(PasswordResetToken)
