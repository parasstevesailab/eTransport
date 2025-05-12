# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from .serializers import (
#     VehicleOwnerDocumentSerializer, IndustrialOwnerDocumentSerializer,
#     BulkVehicleDocumentSerializer, BulkIndustrialDocumentSerializer,
#     CustomUserSerializer, UserProfileSerializer, VehicleOwnerSerializer,
#     ApproveVehicleOwnerSerializer, IndustrialOwnerSerializer, PostSerializer,
#     InitialRegistrationSerializer, UserDetailsSerializer, OTPVerificationSerializer,
#     LanguagePreferenceSerializer, UserTypeSelectionSerializer,
#     VehicleOwnerRegistrationSerializer, IndustrialOwnerRegistrationSerializer,
#     LoginSerializer, VehicleListSerializer, DeliveryStatusSerializer
# )
# from django.core.exceptions import ObjectDoesNotExist
# from .models import CustomUser, VehicleOwnerDocument, IndustrialOwnerDocument, Post, Delivery, DeliveryStatus, VehicleOwner, IndustrialOwner
# from .utils import sendMail
# import random
# import re
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.core.exceptions import ValidationError
# import imghdr
# from django.shortcuts import get_object_or_404
# from datetime import datetime
# from rest_framework.permissions import AllowAny
# from rest_framework.permissions import BasePermission

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             otp = random.randint(1000, 9999)
#             user.verification_code = otp
#             user.is_verified = False
#             user.save()
#             success, message = sendMail(emailid=user.email, otp=otp)
#             if success:
#                 return Response(
#                     {"message": f"{user.get_user_type_display()} registered successfully. {message}"},
#                     status=status.HTTP_201_CREATED
#                 )
#             else:
#                 return Response(
#                     {"error": f"Failed to send verification email: {message}"},
#                     status=status.HTTP_500_INTERNAL_SERVER_ERROR
#                 )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = CustomUser.objects.get(email=serializer.validated_data['email'])
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'message': 'Login successful',
#                 'access_token': str(refresh.access_token),
#                 'refresh_token': str(refresh),
#                 'user_type': user.user_type
#             })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VerifyEmailView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         otp = request.data.get("otp")
#         if not email or not otp:
#             return Response(
#                 {"error": "Email and OTP are required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         try:
#             user = CustomUser.objects.get(email=email)
#             if user.is_verified:
#                 return Response(
#                     {"message": "Email is already verified"},
#                     status=status.HTTP_200_OK
#                 )
#             if str(user.verification_code) == str(otp):
#                 user.is_verified = True
#                 user.verification_code = None
#                 user.save()
#                 return Response(
#                     {"message": "Email verified successfully"},
#                     status=status.HTTP_200_OK
#                 )
#             else:
#                 return Response(
#                     {"error": "Invalid OTP"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         except CustomUser.DoesNotExist:
#             return Response(
#                 {"error": "No user found with this email"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request):
#         serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VehicleOwnerListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         vehicle_owners = VehicleOwner.objects.filter(doc_is_approved=True)
#         serializer = VehicleOwnerSerializer(vehicle_owners, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class VehicleOwnerDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, user_id):
#         try:
#             vehicle_owner = VehicleOwner.objects.filter(user__user_id=user_id).first()
#             if not vehicle_owner:
#                 return Response({"error": "Vehicle Owner not found."}, status=status.HTTP_404_NOT_FOUND)
#             serializer = VehicleOwnerSerializer(vehicle_owner)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "Vehicle Owner not found."}, status=status.HTTP_404_NOT_FOUND)

# class VehicleOwnerUpdateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, vehicle_id):
#         try:
#             vehicle_owner = VehicleOwner.objects.get(id=vehicle_id, user=request.user)
#             serializer = VehicleOwnerSerializer(vehicle_owner, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except VehicleOwner.DoesNotExist:
#             return Response({"error": "Vehicle not found or you are not authorized."}, status=status.HTTP_404_NOT_FOUND)

# class IndustrialOwnerUpdateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request):
#         user = request.user
#         try:
#             industrial_owner = IndustrialOwner.objects.get(user=user)
#             serializer = IndustrialOwnerSerializer(industrial_owner, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except IndustrialOwner.DoesNotExist:
#             return Response({"error": "You are not a registered industrial owner."}, status=status.HTTP_403_FORBIDDEN)

# class IsAppAdminOrSuperUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and (request.user.is_superuser or request.user.is_admin)

# class ApproveVehicleOwnerView(APIView):
#     permission_classes = [IsAppAdminOrSuperUser]

#     def put(self, request, user_id):
#         try:
#             vehicle_owner = CustomUser.objects.get(user_id=user_id, user_type='vehicle_owner')
#             serializer = ApproveVehicleOwnerSerializer(vehicle_owner, data={'is_approved': True}, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({"message": "Vehicle Owner approved successfully."}, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "Vehicle Owner not found."}, status=status.HTTP_404_NOT_FOUND)

# class VehicleDocumentUploadView(APIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def validate_image(self, file_obj):
#         valid_image_types = ['jpeg', 'png', 'gif', 'bmp']
#         file_type = imghdr.what(file_obj)
#         if file_type not in valid_image_types:
#             raise ValidationError("File must be an image (JPEG, PNG, GIF, or BMP)")
#         if file_obj.size > 5 * 1024 * 1024:
#             raise ValidationError("Image file too large (max 5MB)")

#     def post(self, request):
#         user = request.user
#         if user.user_type != 'vehicle_owner':
#             return Response({"error": "Only vehicle owners can upload these documents"}, status=status.HTTP_403_FORBIDDEN)
        
#         serializer = BulkVehicleDocumentSerializer(data=request.FILES)
#         if serializer.is_valid():
#             try:
#                 for file in serializer.validated_data.values():
#                     self.validate_image(file)
                
#                 VehicleOwnerDocument.objects.bulk_create([
#                     VehicleOwnerDocument(
#                         user=user,
#                         document_type='vehicle_registration',
#                         document_image=serializer.validated_data['vehicle_registration']
#                     ),
#                     VehicleOwnerDocument(
#                         user=user,
#                         document_type='driving_license',
#                         document_image=serializer.validated_data['driving_license']
#                     ),
#                     VehicleOwnerDocument(
#                         user=user,
#                         document_type='identity_proof',
#                         document_image=serializer.validated_data['identity_proof']
#                     )
#                 ])
                
#                 user.has_submitted_vehicle_docs = True
#                 user.save()
                
#                 documents = user.vehicle_documents.all()
#                 return Response(VehicleOwnerDocumentSerializer(documents, many=True).data, status=status.HTTP_201_CREATED)
#             except ValidationError as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class IndustrialDocumentUploadView(APIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def validate_image(self, file_obj):
#         valid_image_types = ['jpeg', 'png', 'gif', 'bmp']
#         file_type = imghdr.what(file_obj)
#         if file_type not in valid_image_types:
#             raise ValidationError("File must be an image (JPEG, PNG, GIF, or BMP)")
#         if file_obj.size > 5 * 1024 * 1024:
#             raise ValidationError("Image file too large (max 5MB)")

#     def post(self, request):
#         user = request.user
#         if user.user_type != 'industrial_owner':
#             return Response({"error": "Only industrial owners can upload these documents"}, status=status.HTTP_403_FORBIDDEN)
        
#         if user.industrial_documents.exists():
#             return Response({"error": "Documents already submitted"}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = BulkIndustrialDocumentSerializer(data=request.FILES)
#         if serializer.is_valid():
#             try:
#                 for file in serializer.validated_data.values():
#                     self.validate_image(file)
                
#                 IndustrialOwnerDocument.objects.bulk_create([
#                     IndustrialOwnerDocument(
#                         user=user,
#                         document_type='industrial_certificate',
#                         document_image=serializer.validated_data['industrial_certificate']
#                     ),
#                     IndustrialOwnerDocument(
#                         user=user,
#                         document_type='industrial_license',
#                         document_image=serializer.validated_data['industrial_license']
#                     ),
#                     IndustrialOwnerDocument(
#                         user=user,
#                         document_type='identity_proof',
#                         document_image=serializer.validated_data['identity_proof']
#                     )
#                 ])
                
#                 user.has_submitted_industrial_docs = True
#                 user.save()
                
#                 documents = user.industrial_documents.all()
#                 return Response(IndustrialOwnerDocumentSerializer(documents, many=True).data, status=status.HTTP_201_CREATED)
#             except ValidationError as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VehicleDocumentListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         if user.user_type != 'vehicle_owner' and not user.is_admin:
#             return Response({"error": "Only vehicle owners or admins can view these documents"}, status=status.HTTP_403_FORBIDDEN)
        
#         user_id = request.query_params.get('user_id')
#         if user.is_admin and user_id:
#             try:
#                 target_user = CustomUser.objects.get(id=user_id)
#                 if target_user.user_type != 'vehicle_owner':
#                     return Response({"error": "Specified user is not a vehicle owner"}, status=status.HTTP_400_BAD_REQUEST)
#                 documents = target_user.vehicle_documents.all()
#             except CustomUser.DoesNotExist:
#                 return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             documents = user.vehicle_documents.all()
            
#         serializer = VehicleOwnerDocumentSerializer(documents, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class IndustrialDocumentListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         if user.user_type != 'industrial_owner' and not user.is_admin:
#             return Response({"error": "Only industrial owners or admins can view these documents"}, status=status.HTTP_403_FORBIDDEN)
        
#         user_id = request.query_params.get('user_id')
#         if user.is_admin and user_id:
#             try:
#                 target_user = CustomUser.objects.get(id=user_id)
#                 if target_user.user_type != 'industrial_owner':
#                     return Response({"error": "Specified user is not an industrial owner"}, status=status.HTTP_400_BAD_REQUEST)
#                 documents = target_user.industrial_documents.all()
#             except CustomUser.DoesNotExist:
#                 return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             documents = user.industrial_documents.all()
            
#         serializer = IndustrialOwnerDocumentSerializer(documents, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class DocumentApprovalView(APIView):
#     permission_classes = [IsAdminUser]

#     def post(self, request, doc_type, doc_id):
#         try:
#             if doc_type == 'vehicle':
#                 document = VehicleOwnerDocument.objects.get(id=doc_id)
#                 model = VehicleOwnerDocument
#                 flag = 'has_submitted_vehicle_docs'
#             elif doc_type == 'industrial':
#                 document = IndustrialOwnerDocument.objects.get(id=doc_id)
#                 model = IndustrialOwnerDocument
#                 flag = 'has_submitted_industrial_docs'
#             else:
#                 return Response({"error": "Invalid document type"}, status=status.HTTP_400_BAD_REQUEST)
                
#             document.is_verified = True
#             document.save()
            
#             user = document.user
#             all_docs_verified = not model.objects.filter(user=user, is_verified=False).exists()
#             required_docs = {'vehicle_registration', 'driving_license', 'identity_proof'} \
#                           if doc_type == 'vehicle' else \
#                           {'industrial_certificate', 'industrial_license', 'identity_proof'}
                          
#             if all_docs_verified and getattr(user, flag):
#                 user.is_approved = True
#                 user.doc_is_approved = True
#                 user.save()
                
#             return Response({"message": "Document approved"}, status=status.HTTP_200_OK)
#         except (VehicleOwnerDocument.DoesNotExist, IndustrialOwnerDocument.DoesNotExist):
#             return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

# class ResendOTPView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         if not email:
#             return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             user = CustomUser.objects.get(email=email)
#             if user.is_verified:
#                 return Response({"message": "Email is already verified"}, status=status.HTTP_200_OK)
            
#             otp = random.randint(1000, 9999)
#             user.verification_code = otp
#             user.save()
            
#             success, message = sendMail(emailid=user.email, otp=otp)
#             if success:
#                 return Response({"message": f"OTP resent successfully to {email}"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": f"Failed to resend OTP: {message}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "No user found with this email"}, status=status.HTTP_404_NOT_FOUND)

# class IndustrialOwnerCreatePostView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         if not user.user_type == 'industrial_owner':
#             return Response({"error": "You are not a registered industrial owner."}, status=status.HTTP_403_FORBIDDEN)
#         if not user.doc_is_approved:
#             return Response({"error": "Your documents are not verified. Please contact admin."}, status=status.HTTP_403_FORBIDDEN)

#         serializer = PostSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             post = serializer.save(industrial_owner=user)
#             return Response({
#                 "message": "Post created successfully",
#                 "post": serializer.data,
#                 "post_id": post.post_id,
#                 "price": post.price,
#                 "delivery_deadline": post.delivery_deadline
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VehicleOwnerPostListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         if not user.user_type == 'vehicle_owner' or not user.doc_is_approved:
#             return Response({"error": "You are not authorized to view posts."}, status=status.HTTP_403_FORBIDDEN)

#         posts = Post.objects.filter(is_active=True, status='open').select_related('industrial_owner')
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class PostDeleteView(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, post_id):
#         post = get_object_or_404(Post, post_id=post_id)
#         user = request.user
#         if not (user.is_staff or user == post.industrial_owner):
#             return Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
#         post.delete()
#         return Response({"message": f"Post {post_id} deleted successfully"}, status=status.HTTP_200_OK)

# class PostAcceptView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, post_id):
#         user = request.user
#         if not user.user_type == 'vehicle_owner' or not user.doc_is_approved:
#             return Response({"error": "You are not authorized to accept posts."}, status=status.HTTP_403_FORBIDDEN)

#         post = get_object_or_404(Post, post_id=post_id, is_active=True, status='open')
#         post.accepted_by = user
#         post.status = 'accepted'
#         post.is_active = False
#         post.save()

#         Delivery.objects.create(post=post, vehicle_owner=user)
#         return Response({
#             "message": f"Post {post_id} accepted successfully",
#             "industrial_owner_contact": {
#                 "email": post.industrial_owner.email,
#                 "contact_no": post.industrial_owner.contact_no
#             }
#         }, status=status.HTTP_200_OK)

# class DeliveryScheduleView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, post_id):
#         user = request.user
#         post = Post.objects.filter(post_id=post_id).first()
#         if not post:
#             return Response({"detail": f"No post found with ID {post_id}."}, status=status.HTTP_404_NOT_FOUND)
#         if post.accepted_by != user:
#             return Response({"detail": "You did not accept this post."}, status=status.HTTP_403_FORBIDDEN)
#         if post.status != 'accepted':
#             return Response({"detail": f"Post status is '{post.status}', not 'accepted'."}, status=status.HTTP_400_BAD_REQUEST)
#         if not post.delivery_deadline:
#             return Response({"error": "No delivery deadline set by industrial owner."}, status=status.HTTP_400_BAD_REQUEST)

#         delivery_data = request.data
#         pickup_time = delivery_data.get('pickup_time')
#         estimated_delivery_time = delivery_data.get('estimated_delivery_time')
#         if not pickup_time or not estimated_delivery_time:
#             return Response({"error": "Pick-up and delivery times are required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             pickup_time = datetime.fromisoformat(pickup_time.replace('Z', '+00:00'))
#             estimated_delivery_time = datetime.fromisoformat(estimated_delivery_time.replace('Z', '+00:00'))
#         except ValueError:
#             return Response({"error": "Invalid datetime format. Use ISO format (e.g., '2024-04-13T10:00:00Z')."}, status=status.HTTP_400_BAD_REQUEST)

#         if pickup_time > post.delivery_deadline or estimated_delivery_time > post.delivery_deadline:
#             return Response({"error": "Pick-up and delivery times must be before the deadline."}, status=status.HTTP_400_BAD_REQUEST)
#         if pickup_time >= estimated_delivery_time:
#             return Response({"error": "Pick-up time must be before estimated delivery time."}, status=status.HTTP_400_BAD_REQUEST)

#         delivery, created = Delivery.objects.get_or_create(post=post)
#         delivery.pickup_time = pickup_time
#         delivery.estimated_delivery_time = estimated_delivery_time
#         delivery.save()
#         return Response({"message": "Delivery schedule set successfully"}, status=status.HTTP_200_OK)

# class PostCancelAcceptView(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, post_id):
#         user = request.user
#         post = Post.objects.filter(post_id=post_id).first()
#         if not post:
#             return Response({"detail": f"No post found with ID {post_id}."}, status=status.HTTP_404_NOT_FOUND)
#         if not user.user_type == 'vehicle_owner' or not user.doc_is_approved:
#             return Response({"error": "You are not authorized to cancel this acceptance."}, status=status.HTTP_403_FORBIDDEN)
#         if post.accepted_by != user:
#             return Response({"error": "You did not accept this post, so you cannot cancel it."}, status=status.HTTP_403_FORBIDDEN)
#         if post.status != 'accepted':
#             return Response({"error": f"Post status is '{post.status}', not 'accepted'. Cannot cancel."}, status=status.HTTP_400_BAD_REQUEST)

#         post.accepted_by = None
#         post.status = 'open'
#         post.is_active = True
#         post.save()
#         Delivery.objects.filter(post=post).delete()
#         return Response({"message": f"Acceptance of post {post_id} cancelled successfully. Post is now open again."}, status=status.HTTP_200_OK)

# class DeliveryStatusListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, post_id):
#         post = get_object_or_404(Post, post_id=post_id, status='accepted')
#         user = request.user
#         if not (user == post.accepted_by or user == post.industrial_owner):
#             return Response({"error": "You are not authorized to view this status."}, status=status.HTTP_403_FORBIDDEN)

#         status_updates = DeliveryStatus.objects.filter(post=post).order_by('timestamp')
#         serializer = DeliveryStatusSerializer(status_updates, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class UpdateDeliveryStatusView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, post_id):
#         user = request.user
#         post = get_object_or_404(Post, post_id=post_id, accepted_by=user, status='accepted')
#         if not user.user_type == 'vehicle_owner' or not user.doc_is_approved:
#             return Response({"error": "You are not authorized to update this status."}, status=status.HTTP_403_FORBIDDEN)

#         delivery_status = request.data.get('status')
#         notes = request.data.get('notes', '')
#         valid_statuses = ['reached_pickup', 'items_loaded', 'en_route', 'reached_destination', 'items_dropped']
#         if not delivery_status or delivery_status not in valid_statuses:
#             return Response({"error": f"Invalid status. Use: {', '.join(valid_statuses)}."}, status=status.HTTP_400_BAD_REQUEST)

#         DeliveryStatus.objects.create(post=post, vehicle_owner=user, status=delivery_status, notes=notes)
#         if delivery_status == 'items_loaded':
#             post.first_payment_made = False
#             post.save()
#             return Response({
#                 "message": "Status updated. Industrial owner needs to make first payment.",
#                 "payment_due": "half"
#             }, status=status.HTTP_200_OK)
#         if delivery_status == 'items_dropped':
#             post.second_payment_made = False
#             post.save()
#             return Response({
#                 "message": "Status updated. Industrial owner needs to make second payment.",
#                 "payment_due": "half"
#             }, status=status.HTTP_200_OK)
#         return Response({"message": f"Status updated to {delivery_status}."}, status=status.HTTP_200_OK)

# class InitialRegistrationView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = InitialRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             request.session['mobile_number'] = serializer.validated_data['mobile_number']
#             return Response({'message': 'Mobile number verified successfully'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserDetailsRegistrationView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         mobile_number = request.session.get('mobile_number')
#         if not mobile_number:
#             return Response({'error': 'Please provide mobile number first'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = UserDetailsSerializer(data=request.data, context={'mobile_number': mobile_number})
#         if serializer.is_valid():
#             user = serializer.save()
#             email_otp = str(random.randint(100000, 999999))
#             user.verification_code = email_otp
#             user.save()
#             success, message = sendMail(emailid=user.email, otp=email_otp)
#             if not success:
#                 return Response({'error': f'Failed to send OTP: {message}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             return Response({
#                 'message': 'User details saved. Please check your email for OTP verification.',
#                 'user_id': user.id
#             })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class OTPVerificationView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = OTPVerificationSerializer(data=request.data)
#         if serializer.is_valid():
#             mobile_number = request.session.get('mobile_number')
#             if not mobile_number:
#                 return Response({'error': 'Mobile number not found in session'}, status=status.HTTP_400_BAD_REQUEST)
            
#             try:
#                 user = CustomUser.objects.get(contact_no=mobile_number)
#                 if not user.verification_code:
#                     return Response({'error': 'No OTP found for this user'}, status=status.HTTP_400_BAD_REQUEST)
                
#                 if str(user.verification_code) != str(serializer.validated_data['otp']):
#                     return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
                
#                 user.is_verified = True
#                 user.verification_code = None
#                 user.save()
#                 return Response({'message': 'OTP verified successfully'})
#             except CustomUser.DoesNotExist:
#                 return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LanguagePreferenceView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LanguagePreferenceSerializer(data=request.data)
#         if serializer.is_valid():
#             mobile_number = request.session.get('mobile_number')
#             if not mobile_number:
#                 return Response({'error': 'Mobile number not found in session'}, status=status.HTTP_400_BAD_REQUEST)
            
#             request.session['language'] = serializer.validated_data['language']
#             return Response({'message': 'Language preference saved'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserTypeSelectionView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = UserTypeSelectionSerializer(data=request.data)
#         if serializer.is_valid():
#             mobile_number = request.session.get('mobile_number')
#             if not mobile_number:
#                 return Response({'error': 'Mobile number not found in session'}, status=status.HTTP_400_BAD_REQUEST)
            
#             try:
#                 user = CustomUser.objects.get(contact_no=mobile_number)
#                 user.user_type = serializer.validated_data['user_type']
#                 user.save()
#                 return Response({'message': 'User type selected successfully'})
#             except CustomUser.DoesNotExist:
#                 return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VehicleOwnerRegistrationView(APIView):
#     permission_classes = [AllowAny]
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request):
#         mobile_number = request.session.get('mobile_number')
#         if not mobile_number:
#             return Response({'error': 'Please provide mobile number first'}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             user = CustomUser.objects.get(contact_no=mobile_number)
#             if user.user_type != 'vehicle_owner':
#                 return Response({'error': 'User is not registered as a vehicle owner'}, status=status.HTTP_400_BAD_REQUEST)
            
#             serializer = VehicleOwnerRegistrationSerializer(data=request.data)
#             if serializer.is_valid():
#                 vehicle_owner = serializer.save(user=user)
#                 vehicle_owner.has_submitted_vehicle_docs = True
#                 vehicle_owner.save()
#                 return Response({
#                     'message': 'Vehicle owner registration completed',
#                     'vehicle_owner_id': vehicle_owner.id
#                 }, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# class AddVehicleView(APIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request):
#         user = request.user
#         if user.user_type != 'vehicle_owner':
#             return Response({'error': 'Only vehicle owners can add vehicles'}, status=status.HTTP_403_FORBIDDEN)
        
#         serializer = VehicleOwnerRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             vehicle_owner = serializer.save(user=user)
#             vehicle_owner.has_submitted_vehicle_docs = True
#             vehicle_owner.save()
#             return Response({
#                 'message': 'Vehicle added successfully',
#                 'vehicle_owner_id': vehicle_owner.id
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VehicleListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         if user.user_type != 'vehicle_owner':
#             return Response({'error': 'Only vehicle owners can view their vehicles'}, status=status.HTTP_403_FORBIDDEN)
        
#         vehicles = VehicleOwner.objects.filter(user=user)
#         serializer = VehicleListSerializer(vehicles, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class IndustrialOwnerRegistrationView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         mobile_number = request.session.get('mobile_number')
#         if not mobile_number:
#             return Response({'error': 'Please provide mobile number first'}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             user = CustomUser.objects.get(contact_no=mobile_number)
#             if user.user_type != 'industrial_owner':
#                 return Response({'error': 'User is not registered as an industrial owner'}, status=status.HTTP_400_BAD_REQUEST)
            
#             serializer = IndustrialOwnerRegistrationSerializer(data=request.data)
#             if serializer.is_valid():
#                 industrial_owner = serializer.save(user=user)
#                 return Response({
#                     'message': 'Industrial owner registration completed',
#                     'industrial_owner_id': industrial_owner.id
#                 }, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import (
    VehicleOwnerDocumentSerializer, IndustrialOwnerDocumentSerializer,
    BulkVehicleDocumentSerializer, BulkIndustrialDocumentSerializer,
    CustomUserSerializer, UserProfileSerializer, VehicleOwnerSerializer,
    ApproveVehicleOwnerSerializer, IndustrialOwnerSerializer, PostSerializer,
    InitialRegistrationSerializer, UserDetailsSerializer, OTPVerificationSerializer,
    LanguagePreferenceSerializer, UserTypeSelectionSerializer,
    VehicleOwnerRegistrationSerializer, IndustrialOwnerRegistrationSerializer,
    LoginSerializer, VehicleListSerializer, DeliveryStatusSerializer
)
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser, VehicleOwnerDocument, IndustrialOwnerDocument, Post, Delivery, DeliveryStatus, VehicleOwner, IndustrialOwner
from .utils import sendMail
import random
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
import imghdr
from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework.permissions import AllowAny
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
            success, message = sendMail(emailid=user.email, otp=otp)
            if success:
                return Response(
                    {"message": f"{user.get_user_type_display()} registered successfully. {message}"},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"error": f"Failed to send verification email: {message}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.validated_data['email'])
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user_type': user.user_type
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        if not email or not otp:
            return Response(
                {"error": "Email and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_verified:
                return Response(
                    {"message": "Email is already verified"},
                    status=status.HTTP_200_OK
                )
            if str(user.verification_code) == str(otp):
                user.is_verified = True
                user.verification_code = None
                user.save()
                return Response(
                    {"message": "Email verified successfully"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid OTP"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "No user found with this email"},
                status=status.HTTP_404_NOT_FOUND
            )

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehicleOwnerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vehicle_owners = VehicleOwner.objects.filter(doc_is_approved=True)
        serializer = VehicleOwnerSerializer(vehicle_owners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VehicleOwnerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        vehicles = VehicleOwner.objects.filter(user__user_id=user_id)
        if not vehicles.exists():
            return Response({"error": "No vehicles found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleOwnerSerializer(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VehicleOwnerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, vehicle_id):
        try:
            vehicle_owner = VehicleOwner.objects.get(id=vehicle_id, user=request.user)
            serializer = VehicleOwnerSerializer(vehicle_owner, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except VehicleOwner.DoesNotExist:
            return Response({"error": "Vehicle not found or you are not authorized."}, status=status.HTTP_404_NOT_FOUND)

class IndustrialOwnerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        try:
            industrial_owner = IndustrialOwner.objects.get(user=user)
            serializer = IndustrialOwnerSerializer(industrial_owner, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IndustrialOwner.DoesNotExist:
            return Response({"error": "You are not a registered industrial owner."}, status=status.HTTP_403_FORBIDDEN)

class IsAppAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_admin)

class ApproveVehicleOwnerView(APIView):
    permission_classes = [IsAppAdminOrSuperUser]

    def put(self, request, vehicle_id):
        try:
            vehicle = VehicleOwner.objects.get(id=vehicle_id)
            serializer = ApproveVehicleOwnerSerializer(vehicle, data={'doc_is_approved': True}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Vehicle approved successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except VehicleOwner.DoesNotExist:
            return Response({"error": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)

class VehicleDocumentUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def validate_image(self, file_obj):
        valid_image_types = ['jpeg', 'png', 'gif', 'bmp']
        file_type = imghdr.what(file_obj)
        if file_type not in valid_image_types:
            raise ValidationError("File must be an image (JPEG, PNG, GIF, or BMP)")
        if file_obj.size > 5 * 1024 * 1024:
            raise ValidationError("Image file too large (max 5MB)")

    def post(self, request):
        user = request.user
        if user.user_type != 'vehicle_owner':
            return Response({"error": "Only vehicle owners can upload these documents"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BulkVehicleDocumentSerializer(data=request.FILES)
        if serializer.is_valid():
            try:
                for file in serializer.validated_data.values():
                    self.validate_image(file)
                
                VehicleOwnerDocument.objects.bulk_create([
                    VehicleOwnerDocument(
                        user=user,
                        document_type='vehicle_registration',
                        document_image=serializer.validated_data['vehicle_registration']
                    ),
                    VehicleOwnerDocument(
                        user=user,
                        document_type='driving_license',
                        document_image=serializer.validated_data['driving_license']
                    ),
                    VehicleOwnerDocument(
                        user=user,
                        document_type='identity_proof',
                        document_image=serializer.validated_data['identity_proof']
                    )
                ])
                
                vehicle = VehicleOwner.objects.filter(user=user).first()
                if vehicle:
                    vehicle.has_submitted_vehicle_docs = True
                    vehicle.save()
                
                documents = user.vehicle_documents.all()
                return Response(VehicleOwnerDocumentSerializer(documents, many=True).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IndustrialDocumentUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def validate_image(self, file_obj):
        valid_image_types = ['jpeg', 'png', 'gif', 'bmp']
        file_type = imghdr.what(file_obj)
        if file_type not in valid_image_types:
            raise ValidationError("File must be an image (JPEG, PNG, GIF, or BMP)")
        if file_obj.size > 5 * 1024 * 1024:
            raise ValidationError("Image file too large (max 5MB)")

    def post(self, request):
        user = request.user
        if user.user_type != 'industrial_owner':
            return Response({"error": "Only industrial owners can upload these documents"}, status=status.HTTP_403_FORBIDDEN)
        
        if user.industrial_documents.exists():
            return Response({"error": "Documents already submitted"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BulkIndustrialDocumentSerializer(data=request.FILES)
        if serializer.is_valid():
            try:
                for file in serializer.validated_data.values():
                    self.validate_image(file)
                
                IndustrialOwnerDocument.objects.bulk_create([
                    IndustrialOwnerDocument(
                        user=user,
                        document_type='industrial_certificate',
                        document_image=serializer.validated_data['industrial_certificate']
                    ),
                    IndustrialOwnerDocument(
                        user=user,
                        document_type='industrial_license',
                        document_image=serializer.validated_data['industrial_license']
                    ),
                    IndustrialOwnerDocument(
                        user=user,
                        document_type='identity_proof',
                        document_image=serializer.validated_data['identity_proof']
                    )
                ])
                
                industrial_owner = IndustrialOwner.objects.get(user=user)
                industrial_owner.has_submitted_industrial_docs = True
                industrial_owner.save()
                
                documents = user.industrial_documents.all()
                return Response(IndustrialOwnerDocumentSerializer(documents, many=True).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehicleDocumentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'vehicle_owner' and not user.is_admin:
            return Response({"error": "Only vehicle owners or admins can view these documents"}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.query_params.get('user_id')
        if user.is_admin and user_id:
            try:
                target_user = CustomUser.objects.get(id=user_id)
                if target_user.user_type != 'vehicle_owner':
                    return Response({"error": "Specified user is not a vehicle owner"}, status=status.HTTP_400_BAD_REQUEST)
                documents = target_user.vehicle_documents.all()
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            documents = user.vehicle_documents.all()
            
        serializer = VehicleOwnerDocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class IndustrialDocumentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'industrial_owner' and not user.is_admin:
            return Response({"error": "Only industrial owners or admins can view these documents"}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.query_params.get('user_id')
        if user.is_admin and user_id:
            try:
                target_user = CustomUser.objects.get(id=user_id)
                if target_user.user_type != 'industrial_owner':
                    return Response({"error": "Specified user is not an industrial owner"}, status=status.HTTP_400_BAD_REQUEST)
                documents = target_user.industrial_documents.all()
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            documents = user.industrial_documents.all()
            
        serializer = IndustrialOwnerDocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DocumentApprovalView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, doc_type, doc_id):
        try:
            if doc_type == 'vehicle':
                document = VehicleOwnerDocument.objects.get(id=doc_id)
                model = VehicleOwnerDocument
                flag = 'has_submitted_vehicle_docs'
            elif doc_type == 'industrial':
                document = IndustrialOwnerDocument.objects.get(id=doc_id)
                model = IndustrialOwnerDocument
                flag = 'has_submitted_industrial_docs'
            else:
                return Response({"error": "Invalid document type"}, status=status.HTTP_400_BAD_REQUEST)
                
            document.is_verified = True
            document.save()
            
            user = document.user
            all_docs_verified = not model.objects.filter(user=user, is_verified=False).exists()
            required_docs = {'vehicle_registration', 'driving_license', 'identity_proof'} \
                          if doc_type == 'vehicle' else \
                          {'industrial_certificate', 'industrial_license', 'identity_proof'}
                          
            if all_docs_verified and getattr(user.vehicle_profiles.first() if doc_type == 'vehicle' else user.industrial_profile, flag):
                if doc_type == 'vehicle':
                    vehicle = VehicleOwner.objects.filter(user=user).first()
                    if vehicle:
                        vehicle.doc_is_approved = True
                        vehicle.save()
                else:
                    industrial_owner = IndustrialOwner.objects.get(user=user)
                    industrial_owner.doc_is_approved = True
                    industrial_owner.save()
                
            return Response({"message": "Document approved"}, status=status.HTTP_200_OK)
        except (VehicleOwnerDocument.DoesNotExist, IndustrialOwnerDocument.DoesNotExist):
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_verified:
                return Response({"message": "Email is already verified"}, status=status.HTTP_200_OK)
            
            otp = random.randint(1000, 9999)
            user.verification_code = otp
            user.save()
            
            success, message = sendMail(emailid=user.email, otp=otp)
            if success:
                return Response({"message": f"OTP resent successfully to {email}"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": f"Failed to resend OTP: {message}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except CustomUser.DoesNotExist:
            return Response({"error": "No user found with this email"}, status=status.HTTP_404_NOT_FOUND)

class IndustrialOwnerCreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.user_type == 'industrial_owner':
            return Response({"error": "You are not a registered industrial owner."}, status=status.HTTP_403_FORBIDDEN)
        try:
            if not user.industrial_profile.doc_is_approved:
                return Response({"error": "Your documents are not verified. Please contact admin."}, status=status.HTTP_403_FORBIDDEN)
        except IndustrialOwner.DoesNotExist:
            return Response({"error": "You are not a registered industrial owner."}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save(industrial_owner=user)
            return Response({
                "message": "Post created successfully",
                "post": serializer.data,
                "post_id": post.post_id,
                "price": post.price,
                "delivery_deadline": post.delivery_deadline
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehicleOwnerPostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.user_type == 'vehicle_owner' or not user.vehicle_profiles.filter(doc_is_approved=True).exists():
            return Response({"error": "You are not authorized to view posts."}, status=status.HTTP_403_FORBIDDEN)

        posts = Post.objects.filter(is_active=True, status='open').select_related('industrial_owner')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        user = request.user
        if not (user.is_admin or user == post.industrial_owner):
            return Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"message": f"Post {post_id} deleted successfully"}, status=status.HTTP_200_OK)

class PostAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        if not user.user_type == 'vehicle_owner' or not user.vehicle_profiles.filter(doc_is_approved=True).exists():
            return Response({"error": "You are not authorized to accept posts."}, status=status.HTTP_403_FORBIDDEN)

        post = get_object_or_404(Post, post_id=post_id, is_active=True, status='open')
        post.accepted_by = user
        post.status = 'accepted'
        post.is_active = False
        post.save()

        Delivery.objects.create(post=post, vehicle_owner=user)
        return Response({
            "message": f"Post {post_id} accepted successfully",
            "industrial_owner_contact": {
                "email": post.industrial_owner.email,
                "contact_no": post.industrial_owner.contact_no
            }
        }, status=status.HTTP_200_OK)

class DeliveryScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        post = Post.objects.filter(post_id=post_id).first()
        if not post:
            return Response({"detail": f"No post found with ID {post_id}."}, status=status.HTTP_404_NOT_FOUND)
        if post.accepted_by != user:
            return Response({"detail": "You did not accept this post."}, status=status.HTTP_403_FORBIDDEN)
        if post.status != 'accepted':
            return Response({"detail": f"Post status is '{post.status}', not 'accepted'."}, status=status.HTTP_400_BAD_REQUEST)
        if not post.delivery_deadline:
            return Response({"error": "No delivery deadline set by industrial owner."}, status=status.HTTP_400_BAD_REQUEST)

        delivery_data = request.data
        pickup_time = delivery_data.get('pickup_time')
        estimated_delivery_time = delivery_data.get('estimated_delivery_time')
        if not pickup_time or not estimated_delivery_time:
            return Response({"error": "Pick-up and delivery times are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pickup_time = datetime.fromisoformat(pickup_time.replace('Z', '+00:00'))
            estimated_delivery_time = datetime.fromisoformat(estimated_delivery_time.replace('Z', '+00:00'))
        except ValueError:
            return Response({"error": "Invalid datetime format. Use ISO format (e.g., '2024-04-13T10:00:00Z')."}, status=status.HTTP_400_BAD_REQUEST)

        if pickup_time > post.delivery_deadline or estimated_delivery_time > post.delivery_deadline:
            return Response({"error": "Pick-up and delivery times must be before the deadline."}, status=status.HTTP_400_BAD_REQUEST)
        if pickup_time >= estimated_delivery_time:
            return Response({"error": "Pick-up time must be before estimated delivery time."}, status=status.HTTP_400_BAD_REQUEST)

        delivery, created = Delivery.objects.get_or_create(post=post)
        delivery.pickup_time = pickup_time
        delivery.estimated_delivery_time = estimated_delivery_time
        delivery.save()
        return Response({"message": "Delivery schedule set successfully"}, status=status.HTTP_200_OK)

class PostCancelAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        user = request.user
        post = Post.objects.filter(post_id=post_id).first()
        if not post:
            return Response({"detail": f"No post found with ID {post_id}."}, status=status.HTTP_404_NOT_FOUND)
        if not user.user_type == 'vehicle_owner' or not user.vehicle_profiles.filter(doc_is_approved=True).exists():
            return Response({"error": "You are not authorized to cancel this acceptance."}, status=status.HTTP_403_FORBIDDEN)
        if post.accepted_by != user:
            return Response({"error": "You did not accept this post, so you cannot cancel it."}, status=status.HTTP_403_FORBIDDEN)
        if post.status != 'accepted':
            return Response({"error": f"Post status is '{post.status}', not 'accepted'. Cannot cancel."}, status=status.HTTP_400_BAD_REQUEST)

        post.accepted_by = None
        post.status = 'open'
        post.is_active = True
        post.save()
        Delivery.objects.filter(post=post).delete()
        return Response({"message": f"Acceptance of post {post_id} cancelled successfully. Post is now open again."}, status=status.HTTP_200_OK)

class DeliveryStatusListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id, status='accepted')
        user = request.user
        if not (user == post.accepted_by or user == post.industrial_owner):
            return Response({"error": "You are not authorized to view this status."}, status=status.HTTP_403_FORBIDDEN)

        status_updates = DeliveryStatus.objects.filter(post=post).order_by('timestamp')
        serializer = DeliveryStatusSerializer(status_updates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateDeliveryStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, post_id=post_id, accepted_by=user, status='accepted')
        if not user.user_type == 'vehicle_owner' or not user.vehicle_profiles.filter(doc_is_approved=True).exists():
            return Response({"error": "You are not authorized to update this status."}, status=status.HTTP_403_FORBIDDEN)

        delivery_status = request.data.get('status')
        notes = request.data.get('notes', '')
        valid_statuses = ['reached_pickup', 'items_loaded', 'en_route', 'reached_destination', 'items_dropped']
        if not delivery_status or delivery_status not in valid_statuses:
            return Response({"error": f"Invalid status. Use: {', '.join(valid_statuses)}."}, status=status.HTTP_400_BAD_REQUEST)

        DeliveryStatus.objects.create(post=post, vehicle_owner=user, status=delivery_status, notes=notes)
        if delivery_status == 'items_loaded':
            post.first_payment_made = False
            post.save()
            return Response({
                "message": "Status updated. Industrial owner needs to make first payment.",
                "payment_due": "half"
            }, status=status.HTTP_200_OK)
        if delivery_status == 'items_dropped':
            post.second_payment_made = False
            post.save()
            return Response({
                "message": "Status updated. Industrial owner needs to make second payment.",
                "payment_due": "half"
            }, status=status.HTTP_200_OK)
        return Response({"message": f"Status updated to {delivery_status}."}, status=status.HTTP_200_OK)

class InitialRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InitialRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            request.session['mobile_number'] = serializer.validated_data['mobile_number']
            return Response({'message': 'Mobile number verified successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile_number = request.session.get('mobile_number')
        if not mobile_number:
            return Response({'error': 'Please provide mobile number first'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserDetailsSerializer(data=request.data, context={'mobile_number': mobile_number})
        if serializer.is_valid():
            user = serializer.save()
            email_otp = str(random.randint(100000, 999999))
            user.verification_code = email_otp
            user.save()
            success, message = sendMail(emailid=user.email, otp=email_otp)
            if not success:
                return Response({'error': f'Failed to send OTP: {message}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({
                'message': 'User details saved. Please check your email for OTP verification.',
                'user_id': user.id
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = request.session.get('mobile_number')
            if not mobile_number:
                return Response({'error': 'Mobile number not found in session'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = CustomUser.objects.get(contact_no=mobile_number)
                if not user.verification_code:
                    return Response({'error': 'No OTP found for this user'}, status=status.HTTP_400_BAD_REQUEST)
                
                if str(user.verification_code) != str(serializer.validated_data['otp']):
                    return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
                
                user.is_verified = True
                user.verification_code = None
                user.save()
                return Response({'message': 'OTP verified successfully'})
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LanguagePreferenceView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LanguagePreferenceSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = request.session.get('mobile_number')
            if not mobile_number:
                return Response({'error': 'Mobile number not found in session'}, status=status.HTTP_400_BAD_REQUEST)
            
            request.session['language'] = serializer.validated_data['language']
            return Response({'message': 'Language preference saved'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserTypeSelectionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserTypeSelectionSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = request.session.get('mobile_number')
            if not mobile_number:
                return Response({'error': 'Mobile number not found in session'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = CustomUser.objects.get(contact_no=mobile_number)
                user.user_type = serializer.validated_data['user_type']
                user.save()
                return Response({'message': 'User type selected successfully'})
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehicleOwnerRegistrationView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        mobile_number = request.session.get('mobile_number')
        if not mobile_number:
            return Response({'error': 'Please provide mobile number first'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(contact_no=mobile_number)
            if user.user_type != 'vehicle_owner':
                return Response({'error': 'User is not registered as a vehicle owner'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = VehicleOwnerRegistrationSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                vehicle_owner = serializer.save()
                vehicle_owner.has_submitted_vehicle_docs = True
                vehicle_owner.save()
                return Response({
                    'message': 'Vehicle owner registration completed',
                    'vehicle_owner_id': vehicle_owner.id
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class AddVehicleView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user
        if user.user_type != 'vehicle_owner':
            return Response({'error': 'Only vehicle owners can add vehicles'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = VehicleOwnerRegistrationSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            vehicle_owner = serializer.save()
            vehicle_owner.has_submitted_vehicle_docs = True
            vehicle_owner.save()
            return Response({
                'message': 'Vehicle added successfully',
                'vehicle_owner_id': vehicle_owner.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehicleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'vehicle_owner':
            return Response({'error': 'Only vehicle owners can view their vehicles'}, status=status.HTTP_403_FORBIDDEN)
        
        vehicles = VehicleOwner.objects.filter(user=user)
        serializer = VehicleListSerializer(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class IndustrialOwnerRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile_number = request.session.get('mobile_number')
        if not mobile_number:
            return Response({'error': 'Please provide mobile number first'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(contact_no=mobile_number)
            if user.user_type != 'industrial_owner':
                return Response({'error': 'User is not registered as an industrial owner'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = IndustrialOwnerRegistrationSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                industrial_owner = serializer.save()
                return Response({
                    'message': 'Industrial owner registration completed',
                    'industrial_owner_id': industrial_owner.id
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)