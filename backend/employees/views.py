from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeCreateSerializer
from accounts.permissions import IsHR


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Employee directory: list/search/filter, view details, and HR/Admin CRUD.
    Supports:
      ?search=<name or employee_id>
      ?department=<id>  ?status=Active|Inactive  ?designation=<text>
    """
    queryset = Employee.objects.select_related("user", "department", "manager__user").all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["department", "designation"]
    search_fields = ["employee_id", "user__first_name", "user__last_name", "user__email", "designation"]
    ordering_fields = ["employee_id", "date_of_joining"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return EmployeeCreateSerializer
        return EmployeeSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsHR()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get("status")
        if status_param == "Active":
            qs = qs.filter(user__is_active_employee=True)
        elif status_param == "Inactive":
            qs = qs.filter(user__is_active_employee=False)
        return qs
