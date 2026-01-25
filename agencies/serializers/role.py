from rest_framework import serializers
from ..models import Role
from utils.base_serializers import BaseModelSerializer

class RoleSerializer(BaseModelSerializer):
    """Serializer for Role model"""
    class Meta(BaseModelSerializer.Meta):
        model = Role
        fields = BaseModelSerializer.Meta.fields + ('name', 'code', 'description')
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ('code',)
        extra_kwargs = {
            'code': {'read_only': True},
            **BaseModelSerializer.Meta.extra_kwargs
        }
        
    def validate_name(self, value):
        """Validate that role name is unique (case-insensitive)"""
        if self.instance:
            if Role.objects.filter(name__iexact=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A role with this name already exists.")
        elif Role.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A role with this name already exists.")
        return value
