# Frontend Connection Guide

## ✅ Backend Status: READY FOR FRONTEND CONNECTION

### 🚀 Quick Start

1. **Start the Backend Server**:
```bash
cd pamoja_backend
python start_backend_for_frontend.py
```

2. **Backend will be available at**:
- **Development**: `http://localhost:8000`
- **Production**: `https://okemwabrianny.pythonanywhere.com`

### 🔗 API Endpoints Ready

#### Authentication Endpoints ✅
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/token/refresh/` - Refresh JWT token

#### User Data Endpoints ✅
- `GET /api/applications/my-applications/` - User's applications
- `GET /api/claims/` - User's claims
- `GET /api/payments/` - User's payments
- `GET /api/notifications/list/` - User notifications

#### Admin Endpoints ✅
- `GET /api/admin/stats/` - Dashboard statistics
- `GET /api/admin/users/` - All users
- `GET /api/admin/applications/` - All applications
- `GET /api/admin/claims/` - All claims
- `GET /api/admin/payments/` - All payments
- `POST /api/admin/announcements/create/` - Create announcement
- `POST /api/admin/events/create/` - Create event
- `POST /api/admin/meetings/create/` - Create meeting

### 🔧 CORS Configuration ✅
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Angular dev server
    "http://127.0.0.1:4200",
    "https://okemwabrianny.pythonanywhere.com",
]
```

### 🔑 Authentication
- **JWT Tokens**: All endpoints use Bearer token authentication
- **Admin User**: username=`admin`, password=`admin123`
- **Token Format**: `Authorization: Bearer <jwt_token>`

### 📊 Sample API Responses

#### Login Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@pamojakenyamn.com",
    "role": "admin"
  }
}
```

#### Admin Stats Response:
```json
{
  "total_users": 13,
  "total_applications": 6,
  "pending_applications": 0,
  "approved_applications": 5,
  "rejected_applications": 1,
  "total_claims": 6,
  "pending_claims": 2,
  "approved_claims": 2,
  "rejected_claims": 1,
  "total_payments": 3,
  "total_revenue": 2400.0
}
```

### 🧪 Test Connection

Run this command to test all endpoints:
```bash
python test_frontend_endpoints.py
```

### 🌐 Frontend Configuration

Update your Angular environment files:

**environment.ts**:
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

**environment.prod.ts**:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://okemwabrianny.pythonanywhere.com/api'
};
```

### 🔄 Connection Flow

1. **Frontend starts** → `ng serve` (http://localhost:4200)
2. **Backend starts** → `python start_backend_for_frontend.py` (http://localhost:8000)
3. **Frontend calls** → `http://localhost:8000/api/auth/login/`
4. **Backend responds** → JWT tokens + user data
5. **Frontend stores** → JWT tokens in localStorage/sessionStorage
6. **Frontend makes authenticated calls** → All other API endpoints

### ⚡ Status Summary

| Component | Status | Details |
|-----------|--------|---------|
| Database | ✅ Ready | PostgreSQL with test data |
| Authentication | ✅ Ready | JWT tokens working |
| User Endpoints | ✅ Ready | All CRUD operations |
| Admin Endpoints | ✅ Ready | Full admin functionality |
| CORS | ✅ Ready | Frontend domains allowed |
| File Uploads | ✅ Ready | Document upload support |

### 🚨 Important Notes

1. **Backend must be running** before starting frontend
2. **CORS is configured** for localhost:4200 and production domain
3. **JWT tokens expire** after 60 minutes (configurable)
4. **Admin user exists** with username `admin` and password `admin123`
5. **All endpoints tested** and returning proper JSON responses

### 🎯 Next Steps

1. Start backend server: `python start_backend_for_frontend.py`
2. Start frontend: `ng serve`
3. Navigate to `http://localhost:4200`
4. Login with admin credentials
5. All features should work with real backend data!

---

**Backend is 100% ready for frontend connection! 🚀**