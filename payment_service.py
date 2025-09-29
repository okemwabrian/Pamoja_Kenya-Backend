import paypalrestsdk
import stripe
from django.conf import settings
from django.utils import timezone
import logging
import uuid

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self):
        # PayPal Configuration
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,  # sandbox or live
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
        
        # Stripe Configuration
        stripe.api_key = settings.STRIPE_SECRET_KEY
    
    def create_paypal_payment(self, amount, currency='USD', description='Pamoja Kenya MN Payment'):
        """Create PayPal payment"""
        try:
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": f"{settings.FRONTEND_URL}/payment/success",
                    "cancel_url": f"{settings.FRONTEND_URL}/payment/cancel"
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": description,
                            "sku": "pamoja-payment",
                            "price": str(amount),
                            "currency": currency,
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(amount),
                        "currency": currency
                    },
                    "description": description
                }]
            })
            
            if payment.create():
                logger.info(f"PayPal payment created: {payment.id}")
                return {
                    'success': True,
                    'payment_id': payment.id,
                    'approval_url': next(link.href for link in payment.links if link.rel == "approval_url"),
                    'method': 'paypal'
                }
            else:
                logger.error(f"PayPal payment creation failed: {payment.error}")
                return {'success': False, 'error': payment.error}
                
        except Exception as e:
            logger.error(f"PayPal payment error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def execute_paypal_payment(self, payment_id, payer_id):
        """Execute PayPal payment after approval"""
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                logger.info(f"PayPal payment executed: {payment_id}")
                return {
                    'success': True,
                    'transaction_id': payment.transactions[0].related_resources[0].sale.id,
                    'amount': payment.transactions[0].amount.total,
                    'currency': payment.transactions[0].amount.currency,
                    'status': 'completed'
                }
            else:
                logger.error(f"PayPal payment execution failed: {payment.error}")
                return {'success': False, 'error': payment.error}
                
        except Exception as e:
            logger.error(f"PayPal execution error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_stripe_payment_intent(self, amount, currency='usd', description='Pamoja Kenya MN Payment'):
        """Create Stripe payment intent"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Stripe uses cents
                currency=currency,
                description=description,
                metadata={
                    'organization': 'Pamoja Kenya MN',
                    'timestamp': str(timezone.now())
                }
            )
            
            logger.info(f"Stripe payment intent created: {intent.id}")
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'method': 'stripe'
            }
            
        except Exception as e:
            logger.error(f"Stripe payment error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_bank_transfer_reference(self, amount, currency='USD', description='Pamoja Kenya MN Payment'):
        """Create bank transfer reference"""
        try:
            reference_id = f"PMJ-{uuid.uuid4().hex[:8].upper()}"
            
            bank_details = {
                'success': True,
                'reference_id': reference_id,
                'method': 'bank_transfer',
                'amount': amount,
                'currency': currency,
                'bank_details': {
                    'bank_name': 'Wells Fargo Bank',
                    'account_name': 'Pamoja Kenya MN',
                    'account_number': '****1234',  # Masked for security
                    'routing_number': '121000248',
                    'swift_code': 'WFBIUS6S',
                    'reference': reference_id
                },
                'instructions': [
                    f'Use reference number: {reference_id}',
                    'Include your full name in the transfer description',
                    'Email payment confirmation to payments@pamojakenyamn.com',
                    'Processing time: 1-3 business days'
                ]
            }
            
            logger.info(f"Bank transfer reference created: {reference_id}")
            return bank_details
            
        except Exception as e:
            logger.error(f"Bank transfer error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def verify_payment_status(self, payment_id, method):
        """Verify payment status across different methods"""
        try:
            if method == 'paypal':
                payment = paypalrestsdk.Payment.find(payment_id)
                return {
                    'status': payment.state,
                    'amount': payment.transactions[0].amount.total if payment.transactions else None,
                    'currency': payment.transactions[0].amount.currency if payment.transactions else None
                }
            
            elif method == 'stripe':
                intent = stripe.PaymentIntent.retrieve(payment_id)
                return {
                    'status': intent.status,
                    'amount': intent.amount / 100,  # Convert from cents
                    'currency': intent.currency
                }
            
            elif method == 'bank_transfer':
                # For bank transfers, status would be manually updated
                return {
                    'status': 'pending',
                    'message': 'Bank transfer verification pending'
                }
                
        except Exception as e:
            logger.error(f"Payment verification error: {str(e)}")
            return {'error': str(e)}