from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.get_full_name", read_only=True)
    hours_worked = serializers.FloatField(read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "id", "employee", "employee_name", "date", "check_in", "check_out",
            "is_late", "overtime_minutes", "notes", "hours_worked",
        ]
        read_only_fields = ["employee", "is_late"]
