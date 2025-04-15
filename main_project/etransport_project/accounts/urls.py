from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('profile/', UserProfileView.as_view(), name='user-profile_get_user_profile_display'),
    
    path('vehicle-owners/', VehicleOwnerListView.as_view(), name='vehicle-owner-list'),
    path('vehicle-owners/<uuid:user_id>/', VehicleOwnerDetailView.as_view(), name='vehicle-owner-detail'),
    
    path('vehicle-owners/update/', VehicleOwnerUpdateView.as_view(), name='vehicle-owner-update'),
    path('industrial-owners/update/', IndustrialOwnerUpdateView.as_view(), name='industrial_owner_update'),
    
    path('vehicle-owners/approve/<uuid:user_id>/', ApproveVehicleOwnerView.as_view(), name='approve-vehicle-owner'),
    
    
    path('documents/vehicle/', VehicleDocumentListView.as_view(), name='vehicle-document-list'),
    path('documents/industrial/', IndustrialDocumentListView.as_view(), name='industrial-document-list'),
    
    
    path('documents/approve/<str:doc_type>/<int:doc_id>/', DocumentApprovalView.as_view(), name='document-approve'),
    
    
    path('documents/vehicle/upload/',VehicleDocumentUploadView.as_view(),name='vehicle-document-upload'),
    
    # Endpoint for industrial owners to upload all three required documents
    path('documents/industrial/upload/', IndustrialDocumentUploadView.as_view(), name='industrial-document-upload'),
    
    path('post_create/', IndustrialOwnerCreatePostView.as_view(), name='industrial_owner_create_post'),
    
    path('api/posts/',VehicleOwnerPostListView.as_view(), name='post_list'),
    path('posts/<str:post_id>/delete/', PostDeleteView.as_view(), name='post_delete'),  # New endpoint
    
    
    path('api/posts/<str:post_id>/accept/', PostAcceptView.as_view(), name='post_accept'),
    path('api/posts/<str:post_id>/schedule/', DeliveryScheduleView.as_view(), name='delivery_schedule'),
    path('api/posts/<str:post_id>/cancel/', PostCancelAcceptView.as_view(), name='post_cancel'),  # New endpoint
    
    path('api/posts/<str:post_id>/status/', DeliveryStatusListView.as_view(), name='delivery_status_list'),
    path('api/posts/<str:post_id>/update_status/', UpdateDeliveryStatusView.as_view(), name='update_delivery_status'),
]
