from rest_framework import serializers

class BaseModelSerializer(serializers.ModelSerializer):
    """Base serializer for all models with common fields"""
    
    class Meta:
        fields = ('id', 'created_at', 'updated_at',)
        read_only_fields = ('id', 'created_at', 'updated_at') 
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
