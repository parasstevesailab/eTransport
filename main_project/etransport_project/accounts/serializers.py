from rest_framework import serializers
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import CustomUser, VehicleOwnerDocument, IndustrialOwnerDocument
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
import imghdr

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



class IndustrialOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'first_name', 'last_name', 'email', 'contact_no', 'company_name', 'company_address', 'company_reg_no', 'designation','is_vehicle_owner', 'is_approved']
        read_only_fields = ['user_id', 'email', 'is_vehicle_owner', 'is_approved']  # Optional: Prevent updates to these fields

class ApproveVehicleOwnerSerializer(serializers.ModelSerializer):
    approved_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CustomUser
        fields = ['is_approved', 'approved_by']

    def update(self, instance, validated_data):
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()
        return instance


class VehicleOwnerDocumentSerializer(serializers.ModelSerializer):
    document_image = serializers.ImageField(max_length=None, use_url=True)
    
    class Meta:
        model = VehicleOwnerDocument
        fields = ['id', 'document_type', 'document_image', 'uploaded_at', 'is_verified']

class IndustrialOwnerDocumentSerializer(serializers.ModelSerializer):
    document_image = serializers.ImageField(max_length=None, use_url=True)
    
    class Meta:
        model = IndustrialOwnerDocument
        fields = ['id', 'document_type', 'document_image', 'uploaded_at', 'is_verified']

class BulkVehicleDocumentSerializer(serializers.Serializer):
    vehicle_registration = serializers.ImageField()
    driving_license = serializers.ImageField()
    identity_proof = serializers.ImageField()

class BulkIndustrialDocumentSerializer(serializers.Serializer):
    industrial_certificate = serializers.ImageField()
    industrial_license = serializers.ImageField()
    identity_proof = serializers.ImageField()
    
    
    
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_id', 'source_location', 'destination_location', 'weight', 'distance_km']
        read_only_fields = ['post_id']  # post_id is generated, not provided by the user

    def validate(self, data):
        # Ensure distance_km is positive
        if data['distance_km'] <= 0:
            raise serializers.ValidationError("Distance must be greater than 0.")
        return data
    
    
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'contact_no']  # Adjust fields as needed
        
from datetime import timedelta       
class PostSerializer(serializers.ModelSerializer):
    industrial_owner = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['post_id', 'industrial_owner', 'source_location', 'destination_location', 'weight', 'distance_km', 'price', 'created_at', 'is_active', 'status', 'delivery_deadline']
        read_only_fields = ['post_id', 'industrial_owner', 'price', 'created_at', 'is_active', 'status']

    def validate(self, data):
        if data.get('distance_km', 0) <= 0:
            raise serializers.ValidationError("Distance must be greater than 0.")
        
        # Validate delivery deadline if provided as days
        if 'delivery_deadline_days' in self.context['request'].data:  # Assuming days are passed
            days = int(self.context['request'].data['delivery_deadline_days'])
            if days <= 0:
                raise serializers.ValidationError("Delivery deadline must be positive days.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        days = request.data.get('delivery_deadline_days')  # Get days from request
        post = Post.objects.create(
            industrial_owner=request.user,
            source_location=validated_data['source_location'],
            destination_location=validated_data['destination_location'],
            weight=validated_data['weight'],
            distance_km=validated_data['distance_km'],
            delivery_deadline=None if not days else (Post.objects.first().created_at + timedelta(days=int(days)))  # Set deadline
        )
        return post
    
from .models import Post, DeliveryStatus

class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = ['status', 'timestamp', 'notes']