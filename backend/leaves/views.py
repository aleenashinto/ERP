from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LeaveRequest, LeaveBalance, LeaveStatus
from .serializers import LeaveRequestSerializer, LeaveBalanceSerializer
from accounts.permissions import IsManagerOrAbove


class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    Employees: apply / cancel / view own history.
    Managers/HR: approve / reject / view all, plus leave reports.
    """
    serializer_class = LeaveRequestSerializer

    def get_queryset(self):
        user = self.request.user
        qs = LeaveRequest.objects.select_related("employee", "approved_by").all()
        if user.role in ("SUPER_ADMIN", "HR", "MANAGER", "TEAM_LEAD"):
            return qs
        return qs.filter(employee=user)

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        leave = self.get_object()
        if leave.employee != request.user:
            return Response({"detail": "Not your leave request."}, status=status.HTTP_403_FORBIDDEN)
        if leave.status != LeaveStatus.PENDING:
            return Response({"detail": "Only pending requests can be cancelled."}, status=status.HTTP_400_BAD_REQUEST)
        leave.status = LeaveStatus.CANCELLED
        leave.decided_at = timezone.now()
        leave.save()
        return Response(LeaveRequestSerializer(leave).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, IsManagerOrAbove])
    def approve(self, request, pk=None):
        leave = self.get_object()
        leave.status = LeaveStatus.APPROVED
        leave.approved_by = request.user
        leave.decided_at = timezone.now()
        leave.manager_comment = request.data.get("comment", "")
        leave.save()
        return Response(LeaveRequestSerializer(leave).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, IsManagerOrAbove])
    def reject(self, request, pk=None):
        leave = self.get_object()
        leave.status = LeaveStatus.REJECTED
        leave.approved_by = request.user
        leave.decided_at = timezone.now()
        leave.manager_comment = request.data.get("comment", "")
        leave.save()
        return Response(LeaveRequestSerializer(leave).data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated, IsManagerOrAbove])
    def reports(self, request):
        """Aggregate counts by status, for HR leave reports."""
        qs = self.get_queryset()
        summary = {
            "total": qs.count(),
            "pending": qs.filter(status=LeaveStatus.PENDING).count(),
            "approved": qs.filter(status=LeaveStatus.APPROVED).count(),
            "rejected": qs.filter(status=LeaveStatus.REJECTED).count(),
            "cancelled": qs.filter(status=LeaveStatus.CANCELLED).count(),
        }
        return Response(summary)


class LeaveBalanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaveBalanceSerializer

    def get_queryset(self):
        return LeaveBalance.objects.filter(employee=self.request.user)

    @action(detail=False, methods=["get"])
    def mine(self, request):
        balance, _ = LeaveBalance.objects.get_or_create(employee=request.user)
        return Response(LeaveBalanceSerializer(balance).data)
