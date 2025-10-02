from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Application(models.Model):
    APPLICATION_TYPES = [
        ('single', 'Single Family'),
        ('double', 'Double Family'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    application_type = models.CharField(max_length=10, choices=APPLICATION_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Address Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    
    # Spouse Information
    spouse_name = models.CharField(max_length=200, blank=True)
    spouse_phone = models.CharField(max_length=20, blank=True)
    
    # Children Information
    child_1 = models.CharField(max_length=200, blank=True)
    child_2 = models.CharField(max_length=200, blank=True)
    child_3 = models.CharField(max_length=200, blank=True)
    child_4 = models.CharField(max_length=200, blank=True)
    child_5 = models.CharField(max_length=200, blank=True)
    
    # Parents Information (Both sides)
    parent_1 = models.CharField(max_length=200, blank=True)
    parent_2 = models.CharField(max_length=200, blank=True)
    spouse_parent_1 = models.CharField(max_length=200, blank=True)
    spouse_parent_2 = models.CharField(max_length=200, blank=True)
    
    # Siblings Information
    sibling_1 = models.CharField(max_length=200, blank=True)
    sibling_2 = models.CharField(max_length=200, blank=True)
    sibling_3 = models.CharField(max_length=200, blank=True)
    
    # Authorized Representative
    authorized_rep = models.CharField(max_length=200, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=100, blank=True)
    
    # Additional Information
    occupation = models.CharField(max_length=200, blank=True)
    employer = models.CharField(max_length=200, blank=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Document Uploads
    identity_document = models.FileField(upload_to='applications/identity/', blank=True, null=True, help_text='Upload ID card, passport, or driver\'s license')
    supporting_document_1 = models.FileField(upload_to='applications/supporting/', blank=True, null=True, help_text='Additional supporting document')
    supporting_document_2 = models.FileField(upload_to='applications/supporting/', blank=True, null=True, help_text='Additional supporting document')
    supporting_document_3 = models.FileField(upload_to='applications/supporting/', blank=True, null=True, help_text='Additional supporting document')
    
    # Document Review Status
    identity_document_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected - Resubmit Required')
        ],
        default='pending'
    )
    documents_review_notes = models.TextField(blank=True, null=True, help_text='Admin notes on document review')
    documents_reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_documents'
    )
    documents_reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Application Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # $200 single, $400 double
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    constitution_agreed = models.BooleanField(default=False)
    
    # Approval Information
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_applications'
    )
    rejection_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.application_type} ({self.status})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()