"""
Seeds the database with a demo super admin, departments, and a couple of employees
so you can log in and explore the ERP immediately.

Usage: python manage.py seed_demo_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User, Role
from departments.models import Department
from employees.models import Employee


class Command(BaseCommand):
    help = "Seed demo data: super admin, departments, and sample employees."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser(
                username="admin", email="admin@officeerp.local", password="Admin@12345",
                first_name="System", last_name="Admin", role=Role.SUPER_ADMIN,
            )
            self.stdout.write(self.style.SUCCESS("Created super admin -> username: admin / password: Admin@12345"))
        else:
            admin = User.objects.get(username="admin")

        dept, _ = Department.objects.get_or_create(name="Engineering", defaults={"description": "Product engineering team"})
        dept2, _ = Department.objects.get_or_create(name="Human Resources", defaults={"description": "HR & recruitment"})

        if not User.objects.filter(username="hr_jane").exists():
            hr_user = User.objects.create_user(
                username="hr_jane", email="hr.jane@officeerp.local", password="Hr@12345",
                first_name="Jane", last_name="HR", role=Role.HR,
            )
            Employee.objects.create(user=hr_user, employee_id="EMP002", department=dept2, designation="HR Manager", date_of_joining=timezone.now().date())
            self.stdout.write(self.style.SUCCESS("Created HR user -> username: hr_jane / password: Hr@12345"))

        if not User.objects.filter(username="john_dev").exists():
            emp_user = User.objects.create_user(
                username="john_dev", email="john.dev@officeerp.local", password="John@12345",
                first_name="John", last_name="Developer", role=Role.EMPLOYEE,
            )
            Employee.objects.create(user=emp_user, employee_id="EMP001", department=dept, designation="Software Engineer", date_of_joining=timezone.now().date())
            self.stdout.write(self.style.SUCCESS("Created Employee user -> username: john_dev / password: John@12345"))

        self.stdout.write(self.style.SUCCESS("Demo data seeding complete."))
