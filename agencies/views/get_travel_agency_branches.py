from agencies.models.agency_branch import AgencyBranch
from rest_framework import generics
from agencies.serializers import AgencyBranchSerializer

class GetTravelAgencyBranches(generics.ListAPIView):
    serializer_class = AgencyBranchSerializer
    queryset = AgencyBranch.objects.all()

    def get_queryset(self):
        agency_id = self.kwargs.get('agency_id')
        return self.queryset.filter(agency__id=agency_id)