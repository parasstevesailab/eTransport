from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('vehicle-owners/', VehicleOwnerListView.as_view(), name='vehicle-owner-list'),
    path('vehicle-owners/<uuid:user_id>/', VehicleOwnerDetailView.as_view(), name='vehicle-owner-detail'),
    path('vehicle-owners/update/', VehicleOwnerUpdateView.as_view(), name='vehicle-owner-update'),
    path('vehicle-owners/approve/<uuid:user_id>/', ApproveVehicleOwnerView.as_view(), name='approve-vehicle-owner'),
]
