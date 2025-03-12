from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name', 'contact_no',
            'user_type', 'company_name', 'company_address', 'company_reg_no',
            'vehicle_name', 'vehicle_no', 'address', 'is_verified'
        ]
        
        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'read_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            contact_no=validated_data.get('contact_no'),
            user_type=validated_data.get('user_type'),
            company_name=validated_data.get('company_name', ''),
            company_address=validated_data.get('company_address', ''),
            company_reg_no=validated_data.get('company_reg_no', ''),
            vehicle_name=validated_data.get('vehicle_name', ''),
            vehicle_no=validated_data.get('vehicle_no', ''),
            address=validated_data.get('address', ''),
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'contact_no',
            'user_type', 'company_name', 'company_address', 'company_reg_no',
            'vehicle_name', 'vehicle_no', 'address', 'is_verified'
        ]
        read_only_fields = ['email', 'user_type', 'is_verified'] 
    def update(self, instance, validated_data):
        """Update user profile fields"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class VehicleOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 'contact_no',
            'vehicle_name', 'vehicle_no', 'fleet_size', 'services_offered',
            'is_vehicle_owner', 'is_approved'
        ]
        read_only_fields = ['user_id', 'email', 'is_vehicle_owner', 'is_approved']

class ApproveVehicleOwnerSerializer(serializers.ModelSerializer):
    approved_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CustomUser
        fields = ['is_approved', 'approved_by']

    def update(self, instance, validated_data):
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()
        return instance



