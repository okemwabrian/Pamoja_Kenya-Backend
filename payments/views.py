from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer

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