from django.db import models
from django.conf import settings
from django.utils import timezone


class Attendance(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(default=timezone.localdate)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    is_late = models.BooleanField(default=False)
    overtime_minutes = models.PositiveIntegerField(default=0)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("employee", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.employee.username} - {self.date}"

    @property
    def hours_worked(self):
        if self.check_in and self.check_out:
            from datetime import datetime, date
            dt_in = datetime.combine(date.today(), self.check_in)
            dt_out = datetime.combine(date.today(), self.check_out)
            return round((dt_out - dt_in).seconds / 3600, 2)
        return None
