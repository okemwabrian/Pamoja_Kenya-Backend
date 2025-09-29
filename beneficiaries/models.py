from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Beneficiary(models.Model):
    RELATIONSHIP_CHOICES = [
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('sibling', 'Sibling'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beneficiaries')
    
    # Beneficiary Information
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    
    # Address Information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='USA')
    
    # Beneficiary Details
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Additional Information
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_primary', 'name']
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name} ({self.relationship}) - {self.user.get_full_name()}"


class BeneficiaryChangeRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beneficiary_change_requests')
    
    # Request Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    current_names = models.TextField()
    new_names = models.TextField()
    
    # Address Information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    
    # Request Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_beneficiary_requests'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Change Request by {self.full_name} ({self.status})"