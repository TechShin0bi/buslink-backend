from rest_framework import serializers
from ..models import TravelAgency
from utils.base_serializers import BaseModelSerializer

class TravelAgencySerializer(BaseModelSerializer):
    """Serializer for TravelAgency model with detailed information"""
    class Meta(BaseModelSerializer.Meta):
        model = TravelAgency
        fields = BaseModelSerializer.Meta.fields + ('name', 'description', 'is_active')
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ('is_active',)

class TravelAgencyListSerializer(BaseModelSerializer):
    """Lightweight serializer for listing TravelAgencies"""
    class Meta(BaseModelSerializer.Meta):
        model = TravelAgency
        fields = ('id', 'name', 'is_active')
