from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.exceptions import ObjectDoesNotExist
from .serializers import CustomUserSerializer, UserProfileSerializer, VehicleOwnerSerializer, ApproveVehicleOwnerSerializer
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .utils import sendMail
import random
import re
from rest_framework.permissions import BasePermission

class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            otp = random.randint(1000, 9999)
            user.verification_code = otp
            user.is_verified = False  
            user.save()

            sendMail(
                emailid=user.email,
                otp=otp,
            )

            return Response(
                {"message": f"{user.get_user_type_display()} registered successfully. Verification email sent."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        identifier = request.data.get('email')
        password = request.data.get('password')

        if not identifier or not password:
            return Response({"error": "Both identifier (email/phone) and password are required."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            if '@' in identifier: 
                user = CustomUser.objects.get(email=identifier)
            elif re.match(r'^\+?1?\d{9,15}$', identifier): 
                user = CustomUser.objects.get(contact_no=identifier)
            else:
                return Response({"error": "Invalid identifier. Please provide a valid email or phone number."}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Print debugging info (remove in production)
            print(f"User found: {user.email}, Authenticating with: {user.email}")
            
            # Authenticate the user
            authenticated_user = authenticate(username=user.email, password=password)
            
            if authenticated_user is not None:
                refresh = RefreshToken.for_user(authenticated_user)
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "message": "Login successful!",
                    "user_type": authenticated_user.user_type
                }, status=status.HTTP_200_OK)
            else:
                # More detailed error for debugging (simplify for production)
                return Response({
                    "error": "Invalid credentials.",
                    "detail": "User found but authentication failed. Check password or authentication backends."
                }, status=status.HTTP_401_UNAUTHORIZED)

        except ObjectDoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response(
                {"error": "Email and OTP are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(email=email)

            if str(user.verification_code) == str(otp):
                user.is_verified = True
                user.verification_code = None  
                user.save()
                return Response(
                    {"message": "Email verified successfully!"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid OTP."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "No user found with this email."},
                status=status.HTTP_404_NOT_FOUND
            )
        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve user profile"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update user profile"""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VehicleOwnerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get list of all approved vehicle owners"""
        vehicle_owners = CustomUser.objects.filter(is_vehicle_owner=True, is_approved=True)
        serializer = VehicleOwnerSerializer(vehicle_owners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VehicleOwnerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        """Get details of a specific vehicle owner"""
        try:
            vehicle_owner = CustomUser.objects.get(user_id=user_id, is_vehicle_owner=True)
            serializer = VehicleOwnerSerializer(vehicle_owner)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Vehicle Owner not found."}, status=status.HTTP_404_NOT_FOUND)

class VehicleOwnerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """Update Vehicle Owner details"""
        user = request.user
        if not user.is_vehicle_owner:
            return Response({"error": "You are not a registered vehicle owner."}, status=status.HTTP_403_FORBIDDEN)

        serializer = VehicleOwnerSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class IsAppAdminOrSuperUser(BasePermission):
    """
    Custom permission to allow only superusers or app admins to approve vehicle owners.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_admin)

# class ApproveVehicleOwnerView(APIView):
#     permission_classes = [IsAdminUser]

#     def put(self, request, user_id):
#         """Admin approves a vehicle owner"""
#         try:
#             vehicle_owner = CustomUser.objects.get(user_id=user_id, user_type='vehicle_owner')
            
#             if vehicle_owner.is_approved:
#                 return Response({"message": "Vehicle Owner is already approved."}, status=status.HTTP_400_BAD_REQUEST)

#             serializer = ApproveVehicleOwnerSerializer(vehicle_owner, data={'is_approved': True}, partial=True)

#             if serializer.is_valid():
#                 serializer.save(approved_by=request.user)  # Track which admin approved
#                 return Response({"message": "Vehicle Owner approved successfully."}, status=status.HTTP_200_OK)
            
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         except CustomUser.DoesNotExist:
#             return Response({"error": "Vehicle Owner not found."}, status=status.HTTP_404_NOT_FOUND)


class ApproveVehicleOwnerView(APIView):
    permission_classes = [IsAppAdminOrSuperUser]  # Allow both superuser & app admins

    def put(self, request, user_id):
        """Admin approves a vehicle owner"""
        try:
            vehicle_owner = CustomUser.objects.get(user_id=user_id, user_type='vehicle_owner')
            
            serializer = ApproveVehicleOwnerSerializer(vehicle_owner, data={'is_approved': True}, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Vehicle Owner approved successfully."}, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except CustomUser.DoesNotExist:
            return Response({"error": "Vehicle Owner not found."}, status=status.HTTP_404_NOT_FOUND)
