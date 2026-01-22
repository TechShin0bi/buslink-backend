from rest_framework import viewsets, permissions
from .models import Country, TravelAgency, AgencyLocation
from .serializers import (
    CountrySerializer,
    TravelAgencySerializer,
    AgencyLocationSerializer,
)
from .permissions import IsAgencyOwnerOrAdmin


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]


class TravelAgencyViewSet(viewsets.ModelViewSet):
    serializer_class = TravelAgencySerializer
    permission_classes = [permissions.IsAuthenticated, IsAgencyOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TravelAgency.objects.all()
        return TravelAgency.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AgencyLocationViewSet(viewsets.ModelViewSet):
    serializer_class = AgencyLocationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAgencyOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return AgencyLocation.objects.all()
        return AgencyLocation.objects.filter(agency__owner=user)

    def perform_create(self, serializer):
        agency_id = self.request.data.get("agency")
        if agency_id:
            agency = TravelAgency.objects.get(id=agency_id)
            if agency.owner != self.request.user and not self.request.user.is_staff:
                raise permissions.PermissionDenied(
                    "You don't have permission to add locations to this agency."
                )
        serializer.save()

        # agencies/views.py


# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import AgencyEmployee, Role
# from .serializers import AgencyEmployeeSerializer, RoleSerializer
# from .permissions import IsAgencyOwnerOrAdmin

# class RoleViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class AgencyEmployeeViewSet(viewsets.ModelViewSet):
#     serializer_class = AgencyEmployeeSerializer
#     permission_classes = [permissions.IsAuthenticated, IsAgencyOwnerOrAdmin]

#     def get_queryset(self):
#         user = self.request.user
#         queryset = AgencyEmployee.objects.all()

#         # Agency admins can see their agency's employees
#         if not user.is_staff:
#             queryset = queryset.filter(agency__owner=user)

#         return queryset.select_related('user', 'agency', 'role')

#     @action(detail=False, methods=['get'])
#     def my_roles(self, request):
#         """Get all agencies and roles for the current user"""
#         employments = AgencyEmployee.objects.filter(
#             user=request.user,
#             is_active=True
#         ).select_related('agency', 'role')

#         data = [{
#             'agency_id': emp.agency.id,
#             'agency_name': emp.agency.name,
#             'role': emp.role.name,
#             'role_code': emp.role.code,
#             'permissions': list(emp.role.permissions.values_list('codename', flat=True))
#         } for emp in employments]

#         return Response(data)
