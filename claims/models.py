from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Claim(models.Model):
    CLAIM_TYPES = [
        ('death', 'Death Benefit'),
        ('medical', 'Medical Benefit'),
        ('education', 'Education Benefit'),
        ('emergency', 'Emergency Benefit'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    claim_type = models.CharField(max_length=20, choices=CLAIM_TYPES)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    supporting_documents = models.FileField(upload_to='claims/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Admin fields
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_claims')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_claim_type_display()} - ${self.amount_requested}"

class Beneficiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_beneficiaries')
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Benefit tracking
    total_benefits_received = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_benefit_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"

class BenefitPayment(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='benefit_payments')
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='benefit_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='bank_transfer')
    payment_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    paid_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-paid_at']
    
    def __str__(self):
        return f"{self.beneficiary.name} - ${self.amount}"