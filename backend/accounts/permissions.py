from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_super_admin)


class IsHR(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ("HR", "SUPER_ADMIN")
        )


class IsManagerOrAbove(BasePermission):
    """Managers, Team Leads, HR and Super Admins."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ("MANAGER", "TEAM_LEAD", "HR", "SUPER_ADMIN")
        )


class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ("ACCOUNTANT", "SUPER_ADMIN")
        )


class IsSelfOrManagerOrAbove(BasePermission):
    """Object-level permission: owner of the record, or a manager/HR/admin."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role in ("SUPER_ADMIN", "HR", "MANAGER", "TEAM_LEAD"):
            return True
        owner = getattr(obj, "employee", None) or getattr(obj, "user", None)
        return owner == user
