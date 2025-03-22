
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

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
    contact_no = models.CharField(max_length=30, unique=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=4, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    # Industrial Owner Fields
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    company_reg_no = models.CharField(max_length=30, blank=True, null=True)
    designation = models.CharField(max_length=30, blank=True, null=True)
    
    has_submitted_vehicle_docs = models.BooleanField(default=False)
    has_submitted_industrial_docs = models.BooleanField(default=False)
    
    # Vehicle Owner Fields
    is_vehicle_owner = models.BooleanField(default=False)  # Explicitly mark vehicle owners
    is_industrial_owner = models.BooleanField(default=False)  # Explicitly mark industrial owners
    doc_is_approved = models.BooleanField(default=False)  # Admin approval for vehicle owners
    vehicle_name = models.CharField(max_length=100, blank=True, null=True)
    vehicle_no = models.CharField(max_length=30, blank=True, null=True)
    fleet_size = models.PositiveIntegerField(default=1)  # Number of vehicles owned
    services_offered = models.TextField(blank=True, null=True)  # e.g., "Goods transport, refrigerated transport"

    def save(self, *args, **kwargs):
        # Reset both flags to False before setting the appropriate one
        self.is_vehicle_owner = False
        self.is_industrial_owner = False
        
        # Set the appropriate flag based on user_type
        if self.user_type == 'vehicle_owner':
            self.is_vehicle_owner = True
        elif self.user_type == 'industrial_owner':
            self.is_industrial_owner = True
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"
    
    
    
    
    
class VehicleOwnerDocument(models.Model):
    DOCUMENT_TYPES = (
        ('vehicle_registration', 'Vehicle Registration'),
        ('driving_license', 'Driving License'),
        ('identity_proof', 'Identity Proof'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vehicle_documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_image = models.ImageField(upload_to='vehicle_documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'document_type')
    
    def __str__(self):
        return f"{self.user.email} - {self.get_document_type_display()}"

class IndustrialOwnerDocument(models.Model):
    DOCUMENT_TYPES = (
        ('industrial_certificate', 'Industrial Certificate'),
        ('industrial_license', 'Industrial License'),
        ('identity_proof', 'Identity Proof'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='industrial_documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_image = models.ImageField(upload_to='industrial_documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'document_type')
    
    def __str__(self):
        return f"{self.user.email} - {self.get_document_type_display()}"