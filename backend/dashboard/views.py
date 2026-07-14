from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User
from attendance.models import Attendance
from leaves.models import LeaveRequest, LeaveStatus
from departments.models import Department
from .models import Announcement
from .serializers import AnnouncementSerializer
from accounts.permissions import IsHR


class DashboardSummaryView(APIView):
    """
    GET /api/dashboard/summary/
    Powers the dashboard cards: total employees, today's attendance,
    pending leaves, upcoming birthdays, department distribution, etc.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        upcoming_window = today + timedelta(days=7)

        total_employees = User.objects.filter(is_active_employee=True).count()
        today_attendance = Attendance.objects.filter(date=today, check_in__isnull=False).count()
        pending_leaves = LeaveRequest.objects.filter(status=LeaveStatus.PENDING).count()

        # Birthdays in the next 7 days (month/day comparison, ignoring year)
        upcoming_birthdays = []
        for user in User.objects.exclude(employee_profile__date_of_birth__isnull=True).select_related("employee_profile"):
            dob = user.employee_profile.date_of_birth
            if not dob:
                continue
            this_year_bday = dob.replace(year=today.year)
            if today <= this_year_bday <= upcoming_window:
                upcoming_birthdays.append({
                    "name": user.get_full_name(),
                    "date": this_year_bday.isoformat(),
                })

        department_distribution = list(
            Department.objects.annotate(count=Count("employees")).values("name", "count")
        )

        leave_statistics = {
            "pending": LeaveRequest.objects.filter(status=LeaveStatus.PENDING).count(),
            "approved": LeaveRequest.objects.filter(status=LeaveStatus.APPROVED).count(),
            "rejected": LeaveRequest.objects.filter(status=LeaveStatus.REJECTED).count(),
        }

        return Response({
            "total_employees": total_employees,
            "today_attendance": today_attendance,
            "pending_leaves": pending_leaves,
            "upcoming_birthdays": upcoming_birthdays,
            "department_distribution": department_distribution,
            "leave_statistics": leave_statistics,
        })


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsHR()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
