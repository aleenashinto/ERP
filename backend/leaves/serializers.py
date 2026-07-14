from rest_framework import serializers
from .models import LeaveRequest, LeaveBalance


class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = ["casual_leave", "sick_leave", "paid_leave"]


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.get_full_name", read_only=True)
    days_requested = serializers.IntegerField(read_only=True)
    approved_by_name = serializers.CharField(source="approved_by.get_full_name", read_only=True, default="")

    class Meta:
        model = LeaveRequest
        fields = [
            "id", "employee", "employee_name", "leave_type", "start_date", "end_date",
            "reason", "status", "approved_by", "approved_by_name", "applied_at",
            "decided_at", "manager_comment", "days_requested",
        ]
        read_only_fields = ["employee", "status", "approved_by", "decided_at"]

    def validate(self, data):
        if data["end_date"] < data["start_date"]:
            raise serializers.ValidationError("End date cannot be before start date.")
        return data
