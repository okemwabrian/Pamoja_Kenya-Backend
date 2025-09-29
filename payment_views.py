from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from payment_service import PaymentService
from email_service import EmailService
import logging

logger = logging.getLogger(__name__)
payment_service = PaymentService()

@api_view(['POST'])
def create_payment(request):
    """Create payment based on method"""
    try:
        amount = float(request.data.get('amount', 0))
        method = request.data.get('method', 'paypal')
        description = request.data.get('description', 'Pamoja Kenya MN Payment')
        
        if amount <= 0:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)
        
        if method == 'paypal':
            result = payment_service.create_paypal_payment(amount, description=description)
        elif method == 'stripe':
            result = payment_service.create_stripe_payment_intent(amount, description=description)
        elif method == 'bank_transfer':
            result = payment_service.create_bank_transfer_reference(amount, description=description)
        else:
            return Response({'error': 'Invalid payment method'}, status=status.HTTP_400_BAD_REQUEST)
        
        if result.get('success'):
            return Response(result)
        else:
            return Response({'error': result.get('error', 'Payment creation failed')}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Payment creation error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def execute_paypal_payment(request):
    """Execute PayPal payment after user approval"""
    try:
        payment_id = request.data.get('payment_id')
        payer_id = request.data.get('payer_id')
        user_email = request.data.get('user_email', '')
        user_name = request.data.get('user_name', '')
        
        if not payment_id or not payer_id:
            return Response({'error': 'Missing payment_id or payer_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        result = payment_service.execute_paypal_payment(payment_id, payer_id)
        
        if result.get('success'):
            # Send confirmation email
            if user_email:
                payment_details = {
                    'amount': result.get('amount'),
                    'method': 'PayPal',
                    'transaction_id': result.get('transaction_id'),
                    'date': 'Today'
                }
                EmailService.send_payment_confirmation(user_email, user_name, payment_details)
            
            return Response(result)
        else:
            return Response({'error': result.get('error', 'Payment execution failed')}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"PayPal execution error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def confirm_stripe_payment(request):
    """Confirm Stripe payment"""
    try:
        payment_intent_id = request.data.get('payment_intent_id')
        user_email = request.data.get('user_email', '')
        user_name = request.data.get('user_name', '')
        
        if not payment_intent_id:
            return Response({'error': 'Missing payment_intent_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Verify payment with Stripe
        result = payment_service.verify_payment_status(payment_intent_id, 'stripe')
        
        if result.get('status') == 'succeeded':
            # Send confirmation email
            if user_email:
                payment_details = {
                    'amount': result.get('amount'),
                    'method': 'Credit Card (Stripe)',
                    'transaction_id': payment_intent_id,
                    'date': 'Today'
                }
                EmailService.send_payment_confirmation(user_email, user_name, payment_details)
            
            return Response({'success': True, 'message': 'Payment confirmed'})
        else:
            return Response({'error': 'Payment not completed'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Stripe confirmation error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def verify_bank_transfer(request):
    """Verify bank transfer (manual process)"""
    try:
        reference_id = request.data.get('reference_id')
        user_email = request.data.get('user_email', '')
        user_name = request.data.get('user_name', '')
        
        if not reference_id:
            return Response({'error': 'Missing reference_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # In real implementation, this would check against bank records
        # For now, return pending status
        
        # Send acknowledgment email
        if user_email:
            EmailService.send_welcome_email(user_email, user_name)
        
        return Response({
            'success': True,
            'status': 'pending',
            'message': 'Bank transfer received. Processing within 1-3 business days.',
            'reference_id': reference_id
        })
        
    except Exception as e:
        logger.error(f"Bank transfer verification error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def payment_methods(request):
    """Get available payment methods"""
    return Response({
        'methods': [
            {
                'id': 'paypal',
                'name': 'PayPal',
                'description': 'Pay securely with PayPal',
                'icon': '💳',
                'processing_time': 'Instant'
            },
            {
                'id': 'stripe',
                'name': 'Credit/Debit Card',
                'description': 'Pay with Visa, MasterCard, or American Express',
                'icon': '💳',
                'processing_time': 'Instant'
            },
            {
                'id': 'bank_transfer',
                'name': 'Bank Transfer',
                'description': 'Direct bank transfer (ACH)',
                'icon': '🏦',
                'processing_time': '1-3 business days'
            }
        ]
    })