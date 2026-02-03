from rest_framework import serializers
from ..models import AgencyBranch
from utils.base_serializers import BaseModelSerializer
from django.db import transaction

class AgencyBranchSerializer(BaseModelSerializer):
    """Serializer for AgencyBranch model with location data included"""
    latitude = serializers.DecimalField(max_digits=15, decimal_places=8, required=False, allow_null=True , write_only=True)
    longitude = serializers.DecimalField(max_digits=15, decimal_places=8, required=False, allow_null=True , write_only=True)
    is_active = serializers.BooleanField(required=False, default=True , write_only=True)
    location = serializers.SerializerMethodField(read_only=True)
    
    class Meta(BaseModelSerializer.Meta):
        model = AgencyBranch
        fields = BaseModelSerializer.Meta.fields + (
            'name', 'contact', 'address', 'image', 'agency' , 'latitude', 'longitude', 'is_active', 'location',
        )
    
    def get_location(self, obj):
        """Return location details if it exists"""
        from .agency_location import AgencyLocationSerializer
        locations = obj.branch_location.all() if hasattr(obj, 'branch_location') else []
        if locations:
            return AgencyLocationSerializer(locations[0]).data
        return None
    
    @transaction.atomic
    def create(self, validated_data):
        """Override create to handle location data"""
        from agencies.models.agency_location import AgencyLocation
        
        # Extract location fields
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        is_active = validated_data.pop('is_active', True)
        
        # Create the branch
        branch = AgencyBranch.objects.create(**validated_data)
        
        # Create location if latitude and longitude are provided
        if latitude is not None and longitude is not None:
            AgencyLocation.objects.create(
                branch=branch,
                latitude=latitude,
                longitude=longitude,
                is_active=is_active
            )
        
        return branch

class AgencyBranchListSerializer(BaseModelSerializer):
    """Lightweight serializer for listing AgencyBranches"""
    agency_name = serializers.CharField(source='agency.name', read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = AgencyBranch
        fields = ('id', 'name', 'agency', 'agency_name', 'image')
