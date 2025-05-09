
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
    
    
    
import random
from django.db import models
from accounts.models import CustomUser  # Adjust import based on your app

class Post(models.Model):
    post_id = models.CharField(max_length=5, unique=True)
    industrial_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    accepted_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_posts')  # Vehicle owner who accepted
    source_location = models.CharField(max_length=255)
    destination_location = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=50, default='open')  # e.g., 'open', 'accepted', 'completed'
    delivery_deadline = models.DateTimeField(null=True, blank=True)
    first_payment_made = models.BooleanField(default=False)  # Half payment after items loaded
    second_payment_made = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.post_id:
            while True:
                new_id = str(random.randint(0, 99999)).zfill(5)
                if not Post.objects.filter(post_id=new_id).exists():
                    self.post_id = new_id
                    break
        if self.distance_km:
            self.price = self.distance_km * 10
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post {self.post_id} from {self.source_location} to {self.destination_location} ({self.weight} tons)"
    
    
    
class Delivery(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='delivery')
    vehicle_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='deliveries')
    pickup_time = models.DateTimeField(null=True, blank=True)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')  # e.g., 'pending', 'picked_up', 'in_transit', 'delivered'
    
    
    
from django.db import models
from accounts.models import CustomUser
from .models import Post

class DeliveryStatus(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='status_updates')
    vehicle_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=100)  # e.g., "reached_pickup", "items_loaded", "en_route", "reached_destination", "items_dropped"
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)  # Optional notes

    def __str__(self):
        return f"Status: {self.status} for Post {self.post.post_id} at {self.timestamp}"