from rest_framework import serializers
from ..models import AgencyLocation
from .agency_branch import AgencyBranchListSerializer
from utils.base_serializers import BaseModelSerializer

class AgencyLocationSerializer(BaseModelSerializer):
    """Serializer for AgencyLocation model with detailed information"""
    branch_details = AgencyBranchListSerializer(source='branch', read_only=True)
    
    class Meta(BaseModelSerializer.Meta):
        model = AgencyLocation
        fields = BaseModelSerializer.Meta.fields + (
            'name', 'branch', 'branch_details', 'address', 'city', 'state',
            'country', 'postal_code', 'phone', 'email', 'is_active'
        )

    def validate(self, data):
        """
        Validate that the location name is unique within the same branch
        """
        instance = self.instance
        branch = data.get('branch') or (instance and instance.branch)
        name = data.get('name') or (instance and instance.name)
        
        if branch and name:
            qs = AgencyLocation.objects.filter(branch=branch, name__iexact=name)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError({
                    'name': 'A location with this name already exists for this branch.'
                })
        
        return data
