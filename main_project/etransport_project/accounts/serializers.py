# from rest_framework import serializers
# from .models import CustomUser, VehicleOwner, IndustrialOwner, VehicleOwnerDocument, IndustrialOwnerDocument, Post, DeliveryStatus
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework import status
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.core.exceptions import ValidationError
# import imghdr
# from django.contrib.auth import get_user_model
# import random
# from datetime import timedelta

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = [
#             'username', 'password', 'email', 'first_name', 'last_name', 'contact_no',
#             'user_type', 'company_name', 'company_address', 'company_reg_no',
#             'vehicle_name', 'vehicle_no', 'address', 'is_verified'
#         ]
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'is_verified': {'read_only': True},
#         }

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#             email=validated_data.get('email'),
#             first_name=validated_data.get('first_name'),
#             last_name=validated_data.get('last_name'),
#             contact_no=validated_data.get('contact_no'),
#             user_type=validated_data.get('user_type'),
#             company_name=validated_data.get('company_name', ''),
#             company_address=validated_data.get('company_address', ''),
#             company_reg_no=validated_data.get('company_reg_no', ''),
#             vehicle_name=validated_data.get('vehicle_name', ''),
#             vehicle_no=validated_data.get('vehicle_no', ''),
#             address=validated_data.get('address', ''),
#         )
#         return user

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = [
#             'username', 'email', 'first_name', 'last_name', 'contact_no',
#             'user_type', 'company_name', 'company_address', 'company_reg_no',
#             'vehicle_name', 'vehicle_no', 'address', 'is_verified'
#         ]
#         read_only_fields = ['email', 'user_type', 'is_verified']
    
#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance

# class VehicleOwnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VehicleOwner
#         fields = [
#             'id', 'user', 'vehicle_name', 'vehicle_no', 'vehicle_model', 'vehicle_image',
#             'services_offered', 'driving_license_photo', 'aadhar_photo', 'rc_document',
#             'insurance_document', 'kyc_document', 'insurance_number', 'insurance_expiry_date',
#             'rc_number', 'rc_expiry_date', 'kyc_number', 'kyc_expiry_date',
#             'has_submitted_vehicle_docs', 'doc_is_approved'
#         ]
#         read_only_fields = ['id', 'user', 'has_submitted_vehicle_docs', 'doc_is_approved']

# class VehicleListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VehicleOwner
#         fields = ['id', 'vehicle_name', 'vehicle_no', 'vehicle_model', 'doc_is_approved']

# class IndustrialOwnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = IndustrialOwner
#         fields = ['user', 'company_name', 'company_address', 'company_reg_no', 'designation']
#         read_only_fields = ['user']

# class ApproveVehicleOwnerSerializer(serializers.ModelSerializer):
#     approved_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = CustomUser
#         fields = ['is_approved', 'approved_by']

#     def update(self, instance, validated_data):
#         instance.is_approved = validated_data.get('is_approved', instance.is_approved)
#         instance.save()
#         return instance

# class VehicleOwnerDocumentSerializer(serializers.ModelSerializer):
#     document_image = serializers.ImageField(max_length=None, use_url=True)
    
#     class Meta:
#         model = VehicleOwnerDocument
#         fields = ['id', 'document_type', 'document_image', 'uploaded_at', 'is_verified']

# class IndustrialOwnerDocumentSerializer(serializers.ModelSerializer):
#     document_image = serializers.ImageField(max_length=None, use_url=True)
    
#     class Meta:
#         model = IndustrialOwnerDocument
#         fields = ['id', 'document_type', 'document_image', 'uploaded_at', 'is_verified']

# class BulkVehicleDocumentSerializer(serializers.Serializer):
#     vehicle_registration = serializers.ImageField()
#     driving_license = serializers.ImageField()
#     identity_proof = serializers.ImageField()

# class BulkIndustrialDocumentSerializer(serializers.Serializer):
#     industrial_certificate = serializers.ImageField()
#     industrial_license = serializers.ImageField()
#     identity_proof = serializers.ImageField()

# class PostSerializer(serializers.ModelSerializer):
#     industrial_owner = serializers.SerializerMethodField()

#     class Meta:
#         model = Post
#         fields = ['post_id', 'industrial_owner', 'source_location', 'destination_location', 'weight', 'distance_km', 'price', 'created_at', 'is_active', 'status', 'delivery_deadline']
#         read_only_fields = ['post_id', 'industrial_owner', 'price', 'created_at', 'is_active', 'status']

#     def get_industrial_owner(self, obj):
#         return {
#             'username': obj.industrial_owner.username,
#             'email': obj.industrial_owner.email,
#             'contact_no': obj.industrial_owner.contact_no
#         }

#     def validate(self, data):
#         if data.get('distance_km', 0) <= 0:
#             raise serializers.ValidationError("Distance must be greater than 0.")
#         if 'delivery_deadline_days' in self.context['request'].data:
#             days = int(self.context['request'].data['delivery_deadline_days'])
#             if days <= 0:
#                 raise serializers.ValidationError("Delivery deadline must be positive days.")
#         return data

#     def create(self, validated_data):
#         request = self.context['request']
#         days = request.data.get('delivery_deadline_days')
#         post = Post.objects.create(
#             industrial_owner=request.user,
#             source_location=validated_data['source_location'],
#             destination_location=validated_data['destination_location'],
#             weight=validated_data['weight'],
#             distance_km=validated_data['distance_km'],
#             delivery_deadline=None if not days else (Post.objects.first().created_at + timedelta(days=int(days)))
#         )
#         return post

# class DeliveryStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DeliveryStatus
#         fields = ['status', 'timestamp', 'notes']

# class InitialRegistrationSerializer(serializers.Serializer):
#     mobile_number = serializers.CharField(max_length=15)
    
#     def validate_mobile_number(self, value):
#         if CustomUser.objects.filter(contact_no=value).exists():
#             raise serializers.ValidationError("Mobile number already registered")
#         return value

# class UserDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             username=validated_data['email'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             contact_no=self.context['mobile_number']
#         )
#         return user

# class OTPVerificationSerializer(serializers.Serializer):
#     otp = serializers.CharField(max_length=6)

# class LanguagePreferenceSerializer(serializers.Serializer):
#     language = serializers.ChoiceField(choices=[('en', 'English'), ('hi', 'Hindi')])

# class UserTypeSelectionSerializer(serializers.Serializer):
#     user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

# class VehicleOwnerRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VehicleOwner
#         fields = [
#             'vehicle_name', 'vehicle_no', 'vehicle_model', 'vehicle_image',
#             'services_offered', 'driving_license_photo', 'aadhar_photo',
#             'rc_document', 'insurance_document', 'kyc_document',
#             'insurance_number', 'insurance_expiry_date',
#             'rc_number', 'rc_expiry_date',
#             'kyc_number', 'kyc_expiry_date'
#         ]

#     def validate_vehicle_no(self, value):
#         if VehicleOwner.objects.filter(vehicle_no=value).exists():
#             raise serializers.ValidationError("Vehicle number already registered")
#         return value

# class IndustrialOwnerRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = IndustrialOwner
#         fields = [
#             'company_name', 'company_address', 'company_reg_no',
#             'designation'
#         ]

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         try:
#             user = CustomUser.objects.get(email=data['email'])
#             if not user.check_password(data['password']):
#                 raise serializers.ValidationError("Invalid credentials")
#             return data
#         except CustomUser.DoesNotExist:
#             raise serializers.ValidationError("User not found")


from rest_framework import serializers
from .models import CustomUser, VehicleOwner, IndustrialOwner, VehicleOwnerDocument, IndustrialOwnerDocument, Post, DeliveryStatus
from django.core.exceptions import ValidationError
import imghdr
from datetime import timedelta

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name', 'contact_no',
            'user_type', 'address', 'is_verified'
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
            address=validated_data.get('address', ''),
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    company_address = serializers.SerializerMethodField()
    company_reg_no = serializers.SerializerMethodField()
    vehicles = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'contact_no',
            'user_type', 'company_name', 'company_address', 'company_reg_no',
            'vehicles', 'address', 'is_verified'
        ]
        read_only_fields = ['email', 'user_type', 'is_verified']

    def get_company_name(self, obj):
        if obj.user_type == 'industrial_owner' and hasattr(obj, 'industrial_profile'):
            return obj.industrial_profile.company_name
        return ''

    def get_company_address(self, obj):
        if obj.user_type == 'industrial_owner' and hasattr(obj, 'industrial_profile'):
            return obj.industrial_profile.company_address
        return ''

    def get_company_reg_no(self, obj):
        if obj.user_type == 'industrial_owner' and hasattr(obj, 'industrial_profile'):
            return obj.industrial_profile.company_reg_no
        return ''

    def get_vehicles(self, obj):
        if obj.user_type == 'vehicle_owner':
            vehicles = obj.vehicle_profiles.all()
            return VehicleListSerializer(vehicles, many=True).data
        return []

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class VehicleOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleOwner
        fields = [
            'id', 'vehicle_name', 'vehicle_no', 'vehicle_model', 'vehicle_image',
            'services_offered', 'driving_license_photo', 'aadhar_photo', 'rc_document',
            'insurance_document', 'kyc_document', 'insurance_number', 'insurance_expiry_date',
            'rc_number', 'rc_expiry_date', 'kyc_number', 'kyc_expiry_date',
            'has_submitted_vehicle_docs', 'doc_is_approved'
        ]
        read_only_fields = ['id', 'has_submitted_vehicle_docs', 'doc_is_approved']

class VehicleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleOwner
        fields = ['id', 'vehicle_name', 'vehicle_no', 'vehicle_model', 'doc_is_approved']

class IndustrialOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrialOwner
        fields = ['company_name', 'company_address', 'company_reg_no', 'designation']
        read_only_fields = ['user']

class ApproveVehicleOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleOwner
        fields = ['doc_is_approved']

    def update(self, instance, validated_data):
        instance.doc_is_approved = validated_data.get('doc_is_approved', instance.doc_is_approved)
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

class PostSerializer(serializers.ModelSerializer):
    industrial_owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['post_id', 'industrial_owner', 'source_location', 'destination_location', 'weight', 'distance_km', 'price', 'created_at', 'is_active', 'status', 'delivery_deadline']
        read_only_fields = ['post_id', 'industrial_owner', 'price', 'created_at', 'is_active', 'status']

    def get_industrial_owner(self, obj):
        return {
            'username': obj.industrial_owner.username,
            'email': obj.industrial_owner.email,
            'contact_no': obj.industrial_owner.contact_no
        }

    def validate(self, data):
        if data.get('distance_km', 0) <= 0:
            raise serializers.ValidationError("Distance must be greater than 0.")
        if 'delivery_deadline_days' in self.context['request'].data:
            days = int(self.context['request'].data['delivery_deadline_days'])
            if days <= 0:
                raise serializers.ValidationError("Delivery deadline must be positive days.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        days = request.data.get('delivery_deadline_days')
        post = Post.objects.create(
            industrial_owner=request.user,
            source_location=validated_data['source_location'],
            destination_location=validated_data['destination_location'],
            weight=validated_data['weight'],
            distance_km=validated_data['distance_km'],
            delivery_deadline=None if not days else (Post.objects.first().created_at + timedelta(days=int(days)))
        )
        return post

class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = ['status', 'timestamp', 'notes']

class InitialRegistrationSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    
    def validate_mobile_number(self, value):
        if CustomUser.objects.filter(contact_no=value).exists():
            raise serializers.ValidationError("Mobile number already registered")
        return value

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            contact_no=self.context['mobile_number']
        )
        return user

class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

class LanguagePreferenceSerializer(serializers.Serializer):
    language = serializers.ChoiceField(choices=[('en', 'English'), ('hi', 'Hindi')])

class UserTypeSelectionSerializer(serializers.Serializer):
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

class VehicleOwnerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleOwner
        fields = [
            'vehicle_name', 'vehicle_no', 'vehicle_model', 'vehicle_image',
            'services_offered', 'driving_license_photo', 'aadhar_photo',
            'rc_document', 'insurance_document', 'kyc_document',
            'insurance_number', 'insurance_expiry_date',
            'rc_number', 'rc_expiry_date',
            'kyc_number', 'kyc_expiry_date'
        ]

    def validate_vehicle_no(self, value):
        if VehicleOwner.objects.filter(vehicle_no=value).exists():
            raise serializers.ValidationError("Vehicle number already registered")
        return value

    def create(self, validated_data):
        user = self.context['user']
        vehicle_owner = VehicleOwner.objects.create(user=user, **validated_data)
        return vehicle_owner

class IndustrialOwnerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrialOwner
        fields = [
            'company_name', 'company_address', 'company_reg_no',
            'designation'
        ]

    def create(self, validated_data):
        user = self.context['user']
        industrial_owner = IndustrialOwner.objects.create(user=user, **validated_data)
        return industrial_owner

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            if not user.check_password(data['password']):
                raise serializers.ValidationError("Invalid credentials")
            return data
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found")