from datetime import time
from django.utils import timezone
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Attendance
from .serializers import AttendanceSerializer
from accounts.permissions import IsManagerOrAbove

OFFICE_START_TIME = time(9, 30)  # 9:30 AM cutoff for "late" marking


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    Employees check in/out for themselves; managers/HR/admin can view all records
    with ?employee=<id>&date_after=&date_before= filters.
    """
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["employee", "date"]
    ordering_fields = ["date"]

    def get_queryset(self):
        user = self.request.user
        qs = Attendance.objects.select_related("employee").all()
        if user.role in ("SUPER_ADMIN", "HR", "MANAGER", "TEAM_LEAD"):
            return qs
        return qs.filter(employee=user)

    def get_permissions(self):
        if self.action in ("destroy",):
            return [permissions.IsAuthenticated(), IsManagerOrAbove()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=["post"])
    def check_in(self, request):
        today = timezone.localdate()
        now = timezone.localtime().time()
        record, created = Attendance.objects.get_or_create(employee=request.user, date=today)
        if record.check_in:
            return Response({"detail": "Already checked in today."}, status=status.HTTP_400_BAD_REQUEST)
        record.check_in = now
        record.is_late = now > OFFICE_START_TIME
        record.save()
        return Response(AttendanceSerializer(record).data)

    @action(detail=False, methods=["post"])
    def check_out(self, request):
        today = timezone.localdate()
        now = timezone.localtime().time()
        try:
            record = Attendance.objects.get(employee=request.user, date=today)
        except Attendance.DoesNotExist:
            return Response({"detail": "You haven't checked in today."}, status=status.HTTP_400_BAD_REQUEST)
        record.check_out = now
        record.save()
        return Response(AttendanceSerializer(record).data)

    @action(detail=False, methods=["get"])
    def monthly(self, request):
        """?employee=<id>&year=YYYY&month=MM -> all records for that employee/month."""
        year = request.query_params.get("year", timezone.localdate().year)
        month = request.query_params.get("month", timezone.localdate().month)
        qs = self.get_queryset().filter(date__year=year, date__month=month)
        emp = request.query_params.get("employee")
        if emp:
            qs = qs.filter(employee_id=emp)
        return Response(AttendanceSerializer(qs, many=True).data)
