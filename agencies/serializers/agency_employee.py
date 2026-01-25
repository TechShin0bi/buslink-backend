from rest_framework import serializers
from ..models import AgencyEmployee
from utils.base_serializers import BaseModelSerializer

class AgencyEmployeeSerializer(BaseModelSerializer):
    """Serializer for AgencyEmployee model with detailed information"""
    # user_details = UserSerializer(source='user', read_only=True)
    branch_details = serializers.SerializerMethodField()
    role_details = serializers.SerializerMethodField()
    
    class Meta(BaseModelSerializer.Meta):
        model = AgencyEmployee
        fields = BaseModelSerializer.Meta.fields + (
            'user', 'branch', 'branch_details', 
            'role', 'role_details', 'is_active', 'date_joined'
        )
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ('date_joined',)
    
    def get_branch_details(self, obj):
        from .agency_branch import AgencyBranchListSerializer
        return AgencyBranchListSerializer(obj.branch).data
    
    def get_role_details(self, obj):
        if obj.role:
            return {
                'id': obj.role.id,
                'name': obj.role.name,
                'code': obj.role.code
            }
        return None

class AgencyEmployeeListSerializer(BaseModelSerializer):
    """Lightweight serializer for listing AgencyEmployees"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta(BaseModelSerializer.Meta):
        model = AgencyEmployee
        fields = (
            'id', 'user', 'user_name', 'user_email', 'branch', 'branch_name',
            'role', 'role_name', 'is_active', 'date_joined'
        )
