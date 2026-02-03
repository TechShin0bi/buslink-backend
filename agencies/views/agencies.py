from agencies.models.agency_branch import AgencyBranch
from rest_framework import generics
from agencies.serializers import AgencyBranchSerializer
from rest_framework.permissions import IsAuthenticated


class GetTravelAgencyBranches(generics.ListAPIView):
    serializer_class = AgencyBranchSerializer
    queryset = AgencyBranch.objects.all()

    def get_queryset(self):
        agency_id = self.kwargs.get('agency_id')
        return self.queryset.filter(agency__id=agency_id)


class CreateAgencyBranchWithLocation(generics.CreateAPIView):
    """
    Create a new agency branch with its location and optional image.
    
    Expected payload (multipart/form-data):
    {
        "name": "Branch Name",
        "contact": "0712345678",
        "address": "123 Main St",
        "agency": 1,
        "image": <file>,  # Optional
        "latitude": "4.053544519648043",
        "longitude": "9.738178249055299",
        "is_active": true
    }
    """
    serializer_class = AgencyBranchSerializer
    permission_classes = [IsAuthenticated]