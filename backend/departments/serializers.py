from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.CharField(source="head.get_full_name", read_only=True, default="")
    employee_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "description", "head", "head_name", "employee_count", "created_at", "updated_at"]
