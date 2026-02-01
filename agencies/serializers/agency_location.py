from rest_framework import serializers
from ..models import AgencyLocation
from .agency_branch import AgencyBranchListSerializer
from utils.base_serializers import BaseModelSerializer

class AgencyLocationSerializer(BaseModelSerializer):
    """Serializer for AgencyLocation model with detailed information"""
    # branch_details = AgencyBranchListSerializer(source='branch', read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = AgencyLocation
        fields = BaseModelSerializer.Meta.fields + (
            'latitude', 'longitude', 'is_active'
        )
