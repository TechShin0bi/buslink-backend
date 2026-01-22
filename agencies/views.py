from rest_framework import viewsets, permissions
from .models import Country, TravelAgency, AgencyLocation
from .serializers import CountrySerializer, TravelAgencySerializer, AgencyLocationSerializer
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
        agency_id = self.request.data.get('agency')
        if agency_id:
            agency = TravelAgency.objects.get(id=agency_id)
            if agency.owner != self.request.user and not self.request.user.is_staff:
                raise permissions.PermissionDenied("You don't have permission to add locations to this agency.")
        serializer.save()