from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('industrial_owner', 'Industrial Owner'),
        ('vehicle_owner', 'Vehicle Owner'),
        ('admin', 'Admin'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=4, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    # Industrial Owner Fields
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    company_reg_no = models.CharField(max_length=30, blank=True, null=True)
    designation = models.CharField(max_length=30, blank=True, null=True)

    # Vehicle Owner Fields
    is_vehicle_owner = models.BooleanField(default=False)  # Explicitly mark vehicle owners
    is_approved = models.BooleanField(default=False)  # Admin approval for vehicle owners
    vehicle_name = models.CharField(max_length=100, blank=True, null=True)
    vehicle_no = models.CharField(max_length=30, blank=True, null=True)
    fleet_size = models.PositiveIntegerField(default=1)  # Number of vehicles owned
    services_offered = models.TextField(blank=True, null=True)  # e.g., "Goods transport, refrigerated transport"

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"
