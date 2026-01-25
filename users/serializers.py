from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    agency_details = serializers.SerializerMethodField("get_agency_details")
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name','profile_picture', 
                 'phone_number', 'is_active', 'is_staff', 'date_joined' ,'agency_details')
        read_only_fields = ('id', 'is_active', 'is_staff', 'date_joined')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True, 'allow_blank': False},
        }
    
    def create(self, validated_data):
        """Create and return a new user with encrypted password"""
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
            
        return user
    
    def get_agency_details(self, obj):
        from agencies.serializers import AgencyEmployeeSerializer
        # Since agency_employments is a related manager, we need to use .all()
        employments = obj.agency_employments.all()
        if employments.exists():
            # Return the first employment details if exists
            return AgencyEmployeeSerializer(employments.first()).data
        return None