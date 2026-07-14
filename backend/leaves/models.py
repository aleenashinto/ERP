from django.db import models
from django.conf import settings


class LeaveType(models.TextChoices):
    CASUAL = "CASUAL", "Casual Leave"
    SICK = "SICK", "Sick Leave"
    PAID = "PAID", "Paid Leave"
    WFH = "WFH", "Work From Home"


class LeaveStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED", "Cancelled"


class LeaveBalance(models.Model):
    employee = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leave_balance")
    casual_leave = models.PositiveIntegerField(default=12)
    sick_leave = models.PositiveIntegerField(default=10)
    paid_leave = models.PositiveIntegerField(default=15)

    def __str__(self):
        return f"Leave balance for {self.employee.username}"


class LeaveRequest(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=10, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=LeaveStatus.choices, default=LeaveStatus.PENDING)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_leaves"
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    manager_comment = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.start_date} to {self.end_date})"

    @property
    def days_requested(self):
        return (self.end_date - self.start_date).days + 1
