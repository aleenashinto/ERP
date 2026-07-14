from django.db import models
from django.conf import settings
from departments.models import Department


class Employee(models.Model):
    """Extended HR profile linked one-to-one with the auth User."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employee_profile")
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    designation = models.CharField(max_length=100, blank=True)
    manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="team_members")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["employee_id"]

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"

    @property
    def status(self):
        return "Active" if self.user.is_active_employee else "Inactive"
