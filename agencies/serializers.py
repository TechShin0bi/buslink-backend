from rest_framework import serializers
from .models import Country, TravelAgency, AgencyLocation

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class TravelAgencySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source='country',
        write_only=True
    )
    
    class Meta:
        model = TravelAgency
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'updated_at')

class AgencyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyLocation
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')