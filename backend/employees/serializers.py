from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True, default="")
    manager_name = serializers.CharField(source="manager.user.get_full_name", read_only=True, default="")
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id", "user", "employee_id", "department", "department_name", "designation",
            "manager", "manager_name", "date_of_birth", "gender", "address",
            "emergency_contact_name", "emergency_contact_phone", "date_of_joining", "status",
        ]


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """Used for creating an Employee profile for an existing User (created via /api/auth/register/)."""

    class Meta:
        model = Employee
        fields = [
            "id", "user", "employee_id", "department", "designation", "manager",
            "date_of_birth", "gender", "address", "emergency_contact_name",
            "emergency_contact_phone", "date_of_joining",
        ]
