from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from .models import Department
from .serializers import DepartmentSerializer
from accounts.permissions import IsHR


class DepartmentViewSet(viewsets.ModelViewSet):
    """Full CRUD for departments. HR/Admin can write, everyone authenticated can read."""
    queryset = Department.objects.select_related("head").all()
    serializer_class = DepartmentSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsHR()]
        return [permissions.IsAuthenticated()]
