# Frontend Connection Information

## ✅ Backend Status: READY FOR CONNECTION

**Backend URL:** `http://127.0.0.1:8000`

## 🔑 Working Endpoints (Verified)

### Public Endpoints (No Auth Required)
```
GET http://127.0.0.1:8000/api/notifications/announcements/
GET http://127.0.0.1:8000/api/notifications/events/
GET http://127.0.0.1:8000/api/beneficiaries/list/
```

### Authentication Endpoints
```
POST http://127.0.0.1:8000/api/auth/login/
POST http://127.0.0.1:8000/api/auth/register/
GET http://127.0.0.1:8000/api/auth/profile/
```

### Admin Endpoints (Admin Token Required)
```
GET http://127.0.0.1:8000/api/admin/stats/
GET http://127.0.0.1:8000/api/admin/users/
GET http://127.0.0.1:8000/api/admin/applications/
```

## 🔐 Test Credentials
```
Username: admin
Password: admin123
```

## 📊 Sample Data Available
- **3 Announcements** (including welcome message)
- **2 Events** (Community Picnic, Cultural Night)
- **Dashboard Statistics** (13 users, 8 applications, $2,800 revenue)

## 🧪 Quick Test
```bash
# Test public content (should return 3 announcements)
curl http://127.0.0.1:8000/api/notifications/announcements/

# Test login (should return JWT tokens)
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

## ✅ CORS Configuration
- Allows `http://localhost:4200`
- Allows `http://127.0.0.1:4200`
- All necessary headers configured

## 🎯 Expected Frontend Results
When connected properly, your frontend should show:
- ✅ **Green connection indicator**
- ✅ **Real announcements on home page**
- ✅ **Real events displayed**
- ✅ **Working login functionality**
- ✅ **Admin dashboard with real statistics**

---

**The backend is fully operational and ready for frontend connection!**