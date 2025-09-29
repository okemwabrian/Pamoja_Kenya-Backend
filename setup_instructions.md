# Backend Setup Instructions

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Environment Configuration

1. Copy `.env.example` to `.env`
2. Fill in your configuration values:

### Email Setup (Gmail Example)
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # Generate from Google Account settings
```

### PayPal Setup
1. Create PayPal Developer account: https://developer.paypal.com/
2. Create a sandbox application
3. Get Client ID and Secret:
```
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
```

### Stripe Setup
1. Create Stripe account: https://stripe.com/
2. Get API keys from dashboard:
```
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

## 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 4. Redis Setup (for Celery)

### Windows:
1. Download Redis from: https://github.com/microsoftarchive/redis/releases
2. Install and start Redis server

### Linux/Mac:
```bash
# Install Redis
sudo apt-get install redis-server  # Ubuntu
brew install redis                 # Mac

# Start Redis
redis-server
```

## 5. Start Services

### Terminal 1 - Django Server:
```bash
python manage.py runserver
```

### Terminal 2 - Celery Worker:
```bash
celery -A pamoja_kenya worker --loglevel=info
```

### Terminal 3 - Celery Beat (for scheduled tasks):
```bash
celery -A pamoja_kenya beat --loglevel=info
```

## 6. Test Email Functionality

```python
# In Django shell (python manage.py shell)
from email_service import EmailService
EmailService.send_welcome_email('test@example.com', 'Test User')
```

## 7. Test Payment Integration

### PayPal Test Cards:
- Use PayPal sandbox accounts for testing
- Create buyer and seller accounts in PayPal Developer Console

### Stripe Test Cards:
- 4242424242424242 (Visa)
- 4000000000000002 (Card declined)
- 4000000000009995 (Insufficient funds)

## 8. API Endpoints

### Authentication:
- POST `/api/simple-login/` - User login
- POST `/api/profile/update/` - Update profile
- POST `/api/profile/change-password/` - Change password

### Payments:
- GET `/api/payments/methods/` - Get payment methods
- POST `/api/payments/create/` - Create payment
- POST `/api/payments/paypal/execute/` - Execute PayPal payment
- POST `/api/payments/stripe/confirm/` - Confirm Stripe payment
- POST `/api/payments/bank/verify/` - Verify bank transfer

## 9. Frontend Integration

Update your frontend environment:
```typescript
// environment.ts
export const environment = {
  apiUrl: 'http://localhost:8000/api',
  stripePublishableKey: 'pk_test_your-key',
  paypalClientId: 'your-paypal-client-id'
};
```

## 10. Production Deployment

1. Set `DEBUG=False` in production
2. Use proper email service (SendGrid, AWS SES)
3. Use production PayPal/Stripe keys
4. Set up proper Redis instance
5. Use production database (PostgreSQL)
6. Configure proper CORS settings