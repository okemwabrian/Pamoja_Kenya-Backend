from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Sum
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer
from notifications.email_service import send_payment_confirmation_email

class PaymentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentCreateSerializer
        return PaymentSerializer

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

@api_view(['GET'])
def payment_stats_view(request):
    user_payments = Payment.objects.filter(user=request.user)
    total_paid = user_payments.filter(status='completed').aggregate(
        total=Sum('amount'))['total'] or 0
    
    stats = {
        'total_payments': user_payments.count(),
        'completed_payments': user_payments.filter(status='completed').count(),
        'pending_payments': user_payments.filter(status='pending').count(),
        'total_amount_paid': float(total_paid),
    }
    return Response(stats)

@api_view(['POST'])
@permission_classes([AllowAny])
def record_paypal_payment(request):
    """Record PayPal payment from frontend"""
    data = request.data
    
    # Get user or create test user
    from accounts.models import User
    from applications.models import Application
    
    user = request.user if request.user.is_authenticated else User.objects.first()
    if not user:
        user = User.objects.create_user(username='testuser', email='test@example.com')
    
    # Get application if provided
    application = None
    if data.get('application'):
        try:
            application = Application.objects.get(id=data.get('application'))
        except Application.DoesNotExist:
            pass
    
    payment = Payment.objects.create(
        user=user,
        application=application,
        amount=data.get('amount'),
        currency=data.get('currency', 'USD'),
        payment_method='paypal',
        payer_name=data.get('payer_name'),
        payer_email=data.get('payer_email'),
        paypal_order_id=data.get('paypal_order_id'),
        transaction_id=data.get('paypal_order_id'),
        description=data.get('description', ''),
        status='completed'
    )
    
    # Send payment confirmation email
    send_payment_confirmation_email(user, payment)
    
    return Response({
        'id': payment.id,
        'message': 'Payment recorded successfully',
        'status': payment.status
    }, status=status.HTTP_201_CREATED)