from django.db import models
from django.contrib.auth import get_user_model
from applications.models import Application

User = get_user_model()

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHODS = [
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer'),
        ('mpesa', 'M-Pesa'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name='payments',
        null=True,
        blank=True
    )
    
    # Payment Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Payer Information
    payer_name = models.CharField(max_length=200)
    payer_email = models.EmailField()
    
    # External Payment IDs
    paypal_order_id = models.CharField(max_length=100, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    
    # Additional Information
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.payer_name} - ${self.amount} ({self.status})"

    @property
    def is_completed(self):
        return self.status == 'completed'