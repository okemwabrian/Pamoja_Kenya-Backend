from django.contrib import admin
from django.contrib.auth import get_user_model
from applications.models import Application
from payments.models import Payment
from claims.models import Claim
from beneficiaries.models import Beneficiary

User = get_user_model()

# Admin dashboard views - these models are already registered in their respective apps
# This admin.py file is for admin_api app which provides API endpoints for admin functionality

class AdminDashboard:
    """Admin dashboard statistics and management"""
    
    @staticmethod
    def get_stats():
        return {
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'total_applications': Application.objects.count(),
            'pending_applications': Application.objects.filter(status='pending').count(),
            'total_payments': Payment.objects.count(),
            'completed_payments': Payment.objects.filter(status='completed').count(),
            'total_claims': Claim.objects.count(),
            'pending_claims': Claim.objects.filter(status='pending').count(),
            'total_beneficiaries': Beneficiary.objects.count(),
        }

# No models to register here as this app only provides API endpoints
