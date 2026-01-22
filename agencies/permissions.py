# agencies/permissions.py
from rest_framework import permissions

class IsAgencyOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an agency or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the agency or admin.
        return obj.owner == request.user or request.user.is_staff
    

# agencies/permissions.py
from rest_framework import permissions

class IsAgencyEmployee(permissions.BasePermission):
    """
    Permission to check if a user is an employee of a specific agency.
    """
    def has_permission(self, request, view):
        # This will be checked at the view level
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # For object-level permission, check if user is an employee of the agency
        if hasattr(obj, 'agency'):
            agency = obj.agency
        elif hasattr(obj, 'agencies'):  # For agency itself
            agency = obj
        else:
            return False

        return agency.employees.filter(
            user=request.user,
            is_active=True
        ).exists()

class HasAgencyRole(permissions.BasePermission):
    """
    Permission to check if a user has a specific role in an agency.
    """
    def __init__(self, role_codes=None):
        self.role_codes = role_codes if isinstance(role_codes, (list, tuple)) else [role_codes]

    def has_permission(self, request, view):
        # This will be checked at the view level
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'agency'):
            agency = obj.agency
        elif hasattr(obj, 'agencies'):
            agency = obj
        else:
            return False

        return AgencyEmployee.objects.filter(
            user=request.user,
            agency=agency,
            role__code__in=self.role_codes,
            is_active=True
        ).exists()

# Update the existing permission to use the new employee system
class IsAgencyOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is an admin
        if request.user.is_staff:
            return True

        # For agency owners
        if hasattr(obj, 'owner'):
            return obj.owner == request.user

        # For agency employees with appropriate permissions
        if hasattr(obj, 'agency'):
            return obj.agency.employees.filter(
                user=request.user,
                is_active=True
            ).exists()

        return False