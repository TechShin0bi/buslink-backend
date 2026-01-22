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
        
        
        # agencies/serializers.py
# from .models import AgencyEmployee, Role

# # ... existing serializers ...

# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = '__all__'

# class AgencyEmployeeSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     agency = serializers.PrimaryKeyRelatedField(queryset=TravelAgency.objects.all())
#     role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    
#     user_details = serializers.SerializerMethodField()
#     role_details = serializers.SerializerMethodField()
    
#     class Meta:
#         model = AgencyEmployee
#         fields = '__all__'
#         read_only_fields = ('date_joined',)
    
#     def get_user_details(self, obj):
#         from users.serializers import UserSerializer
#         return UserSerializer(obj.user).data
    
#     def get_role_details(self, obj):
#         return {
#             'name': obj.role.name,
#             'code': obj.role.code
#         }