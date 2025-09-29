# Pamoja Kenya Backend API

A comprehensive Django REST API backend for the Pamoja Kenya membership management system.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone and navigate to backend directory**
```bash
cd pamoja_backend
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create admin user (already done)**
```bash
python create_admin.py
```

6. **Start server**
```bash
python start_server.py
# OR
python manage.py runserver
```

## 🔐 Default Credentials

### Admin User
- **Username**: `admin`
- **Email**: `admin@pamojakenyamn.com`
- **Password**: `admin123`
- **Role**: Admin

### Test User
- **Username**: `testuser`
- **Email**: `test@example.com`
- **Password**: `test123`
- **Role**: User

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile
- `GET /api/auth/stats/` - Get user statistics

### Applications
- `GET /api/applications/` - List user applications
- `POST /api/applications/` - Create new application
- `GET /api/applications/<id>/` - Get application details
- `PUT /api/applications/<id>/` - Update application
- `DELETE /api/applications/<id>/` - Delete application
- `GET /api/applications/stats/` - Get application statistics

### Payments
- `GET /api/payments/` - List user payments
- `POST /api/payments/` - Create new payment
- `GET /api/payments/<id>/` - Get payment details
- `PUT /api/payments/<id>/` - Update payment
- `DELETE /api/payments/<id>/` - Delete payment
- `GET /api/payments/stats/` - Get payment statistics

### Beneficiaries
- `GET /api/beneficiaries/` - List user beneficiaries
- `POST /api/beneficiaries/` - Create new beneficiary
- `GET /api/beneficiaries/<id>/` - Get beneficiary details
- `PUT /api/beneficiaries/<id>/` - Update beneficiary
- `DELETE /api/beneficiaries/<id>/` - Delete beneficiary
- `GET /api/beneficiaries/list/` - Public beneficiary list (masked)
- `POST /api/beneficiaries/request/` - Submit change request

### Admin API (Admin Only)
- `GET /api/admin/stats/` - Get admin dashboard statistics
- `GET /api/admin/users/` - List all users
- `GET /api/admin/users/<id>/` - Get user details
- `PUT /api/admin/users/<id>/` - Update user
- `DELETE /api/admin/users/<id>/delete/` - Delete user
- `GET /api/admin/applications/` - List all applications
- `GET /api/admin/applications/<id>/` - Get application details
- `PUT /api/admin/applications/<id>/` - Update application
- `DELETE /api/admin/applications/<id>/delete/` - Delete application
- `GET /api/admin/payments/` - List all payments

## 🔧 Features

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (User/Admin)
- Custom user model with extended fields
- Secure password validation

### User Management
- User registration and login
- Profile management
- Membership status tracking
- Admin user management

### Application System
- Single and Double family applications
- Application status workflow (Pending/Approved/Rejected)
- Comprehensive application data collection
- Admin application management

### Payment Processing
- Multiple payment method support (PayPal, Stripe, M-Pesa)
- Payment status tracking
- Payment history and statistics
- Admin payment oversight

### Beneficiary Management
- Beneficiary CRUD operations
- Change request system
- Masked public beneficiary display
- Relationship tracking

### Admin Features
- Comprehensive admin dashboard
- User management with role controls
- Application approval workflow
- Payment monitoring
- Statistics and reporting

## 🛠️ Technology Stack

- **Framework**: Django 5.0.1
- **API**: Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development) / PostgreSQL (production)
- **CORS**: django-cors-headers
- **Environment**: python-decouple

## 🔒 Security Features

- JWT token authentication
- CORS protection
- Password validation
- Role-based permissions
- Admin-only endpoints protection
- Input validation and sanitization

## 📱 Frontend Integration

This backend is designed to work seamlessly with the Angular frontend:
- CORS configured for `http://localhost:4200`
- JWT tokens for authentication
- RESTful API design
- Consistent error handling
- Pagination support

## 🚀 Production Deployment

For production deployment:
1. Set `DEBUG=False` in environment
2. Configure PostgreSQL database
3. Set up proper SECRET_KEY and JWT_SECRET_KEY
4. Configure allowed hosts
5. Set up static file serving
6. Use gunicorn or similar WSGI server

## 📞 Support

For support and questions, contact the development team or refer to the API documentation.

---

**Pamoja Kenya Backend API** - Powering community membership management with Django & DRF