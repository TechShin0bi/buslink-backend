from rest_framework import serializers
from ..models import AgencyBranch
from utils.base_serializers import BaseModelSerializer
from .travel_agency import TravelAgencyListSerializer

class AgencyBranchSerializer(BaseModelSerializer):
    """Serializer for AgencyBranch model with detailed information"""
    agency_details = TravelAgencyListSerializer(source='agency', read_only=True)
    
    class Meta(BaseModelSerializer.Meta):
        model = AgencyBranch
        fields = BaseModelSerializer.Meta.fields + (
            'name', 'agency', 'agency_details'
        )

class AgencyBranchListSerializer(BaseModelSerializer):
    """Lightweight serializer for listing AgencyBranches"""
    agency_name = serializers.CharField(source='agency.name', read_only=True)
    
    class Meta(BaseModelSerializer.Meta):
        model = AgencyBranch
        fields = ('id', 'name', 'agency', 'agency_name')
