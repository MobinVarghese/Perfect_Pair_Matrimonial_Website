# Django REST Framework ViewSets - Quick Reference
## Matrimonial Website API

---

## 🚀 Quick Start

### 1. Get JWT Token
```bash
POST /api/users/auth/login/
Body: {"username": "johndoe", "password": "pass"}
Response: {"access": "token...", "refresh": "token..."}
```

### 2. Use Token in Requests
```
Authorization: Bearer <access_token>
```

---

## 📋 All ViewSets & Endpoints

| ViewSet | Base URL | Permission | CRUD | Custom Actions |
|---------|----------|------------|------|----------------|
| **ProfileViewSet** | `/api/users/profiles/` | IsAuthenticated | ✅ Full | me, create-mine, view |
| **OTPVerificationViewSet** | `/api/users/otp/` | IsAuthenticated | List only | generate, verify, resend |
| **InterestViewSet** | `/api/users/interests/` | IsAuthenticated | ✅ Full | sent, received, pending, respond, cancel |
| **ReportViewSet** | `/api/users/reports/` | IsAuthenticated | ✅ Full | my-reports, pending (admin), review (admin), statistics (admin) |
| **ExportLogViewSet** | `/api/users/export-logs/` | IsAdminUser | Read-only | export-data |

---

## 🔐 Authentication Endpoints

```bash
# Login
POST /api/users/auth/login/
{"username": "user", "password": "pass"}

# Refresh Token
POST /api/users/auth/refresh/
{"refresh": "refresh_token"}

# Verify Token
POST /api/users/auth/verify/
{"token": "access_token"}
```

---

## 👤 User Management

```bash
# Register
POST /api/users/register/
{"username": "user", "email": "email", "password": "pass", "password2": "pass", ...}

# List Users
GET /api/users/users/

# Get Current User
GET /api/users/users/me/

# Update User
PUT /api/users/users/me/update/
{"email": "new@email.com", "first_name": "John"}

# Change Password
PUT /api/users/users/change-password/
{"old_password": "old", "new_password": "new", "new_password2": "new"}

# Delete Account (Soft Delete)
DELETE /api/users/users/me/update/
```

---

## 👥 Profile Operations

### Standard CRUD
```bash
# List Profiles (with filters)
GET /api/users/profiles/?gender=male&min_age=25&max_age=35&location=Mumbai

# Get Profile
GET /api/users/profiles/{id}/

# Create Profile
POST /api/users/profiles/
{
  "name": "John Doe",
  "gender": "male",
  "age": 28,
  "location": "Mumbai",
  "mobile_number": "+919876543210",
  "photo": <file>
}

# Update Profile
PUT/PATCH /api/users/profiles/{id}/

# Delete Profile
DELETE /api/users/profiles/{id}/
```

### Custom Actions
```bash
# Get My Profile
GET /api/users/profiles/me/

# Create My Profile
POST /api/users/profiles/create-mine/

# View Profile Details
GET /api/users/profiles/{id}/view/
```

### Query Parameters
- `gender` - male/female/other
- `min_age`, `max_age` - Age range
- `location` - Location contains
- `search` - Search name, occupation, education
- `ordering` - Sort by created_at, age, name

---

## 📱 OTP Verification

```bash
# Generate OTP
POST /api/users/otp/generate/
Response: {"otp": "123456", "expires_at": "..."}

# Verify OTP
POST /api/users/otp/verify/
{"otp": "123456"}

# Resend OTP
POST /api/users/otp/resend/

# List OTP History
GET /api/users/otp/
```

**OTP Expiry:** 10 minutes

---

## 💝 Interest/Connection Requests

### Standard CRUD
```bash
# List Interests
GET /api/users/interests/?type=received&status=pending

# Send Interest
POST /api/users/interests/
{"receiver": 5, "message": "Hello! I'd like to connect."}

# Get Interest
GET /api/users/interests/{id}/

# Update Interest (Receiver only)
PUT /api/users/interests/{id}/

# Delete Interest (Sender only)
DELETE /api/users/interests/{id}/
```

### Custom Actions
```bash
# Get Sent Interests
GET /api/users/interests/sent/

# Get Received Interests
GET /api/users/interests/received/

# Get Pending Interests
GET /api/users/interests/pending/

# Respond to Interest (Accept/Reject)
POST /api/users/interests/{id}/respond/
{"status": "accepted"}  # or "rejected"

# Cancel Interest (Sender only)
POST /api/users/interests/{id}/cancel/
```

### Query Parameters
- `type` - sent/received
- `status` - pending/accepted/rejected

### Business Rules
- ❌ Cannot send to yourself
- ❌ Cannot send duplicate interest
- ❌ Message min 10 characters
- ✅ Only receiver can respond
- ✅ Only sender can cancel
- ✅ Can only respond/cancel pending

---

## 🚨 Report System

### User Operations
```bash
# Create Report
POST /api/users/reports/
{
  "reported_user": 5,
  "reason": "fake_profile",
  "description": "Detailed description (min 20 chars)..."
}

# List My Reports
GET /api/users/reports/my-reports/

# Get Report
GET /api/users/reports/{id}/
```

### Admin Operations
```bash
# List All Reports
GET /api/users/reports/

# Get Pending Reports
GET /api/users/reports/pending/

# Review Report
POST /api/users/reports/{id}/review/
{
  "status": "reviewed",
  "admin_notes": "Investigated and..."
}

# Get Statistics
GET /api/users/reports/statistics/
Response: {"total": 25, "pending": 10, "reviewed": 8, "resolved": 7}
```

### Reason Choices
- `fake_profile`
- `inappropriate_content`
- `harassment`
- `spam`
- `other`

### Status Flow
```
pending → reviewed → resolved
```

### Business Rules
- ❌ Cannot report yourself
- ❌ Cannot report same user in 24 hours
- ✅ Description min 20 characters
- ✅ Only admins can review

---

## 📊 Export Logs (Admin Only)

```bash
# List Export Logs
GET /api/users/export-logs/?file_type=excel&export_type=users

# Get Export Log
GET /api/users/export-logs/{id}/

# Export Data
POST /api/users/export-logs/export-data/
{
  "file_type": "excel",
  "export_type": "users",
  "date_from": "2025-01-01",
  "date_to": "2025-10-14"
}
```

### File Type Choices
- `pdf`
- `excel`
- `csv`

### Export Type Choices
- `users`
- `profiles`
- `reports`
- `interests`
- `all_data`

### Query Parameters
- `admin_id` - Filter by admin
- `file_type` - Filter by type
- `export_type` - Filter by data type

---

## 🔒 Permissions Matrix

| Endpoint | User | Admin | Note |
|----------|------|-------|------|
| Register/Login | ✅ | ✅ | Public |
| List Users | ✅ | ✅ | Authenticated |
| Update User | ✅ Own | ✅ Own | Own account only |
| List Profiles | ✅ | ✅ | With filters |
| Update Profile | ✅ Own | ✅ Own | Own profile only |
| Send Interest | ✅ | ✅ | To others |
| Respond Interest | ✅ Receiver | ✅ Receiver | Receiver only |
| Cancel Interest | ✅ Sender | ✅ Sender | Sender only |
| Create Report | ✅ | ✅ | Not self |
| Review Report | ❌ | ✅ | Admin only |
| Export Data | ❌ | ✅ | Admin only |

---

## 🎯 Common Use Cases

### Complete Registration Flow
```bash
# 1. Register
POST /api/users/register/
{"username": "john", "email": "john@ex.com", "password": "pass", ...}

# 2. Login
POST /api/users/auth/login/
{"username": "john", "password": "pass"}

# 3. Create Profile
POST /api/users/profiles/create-mine/
Authorization: Bearer <token>
{"name": "John Doe", "gender": "male", "age": 28, ...}

# 4. Generate OTP
POST /api/users/otp/generate/
Authorization: Bearer <token>

# 5. Verify OTP
POST /api/users/otp/verify/
Authorization: Bearer <token>
{"otp": "123456"}
```

### Search and Connect
```bash
# 1. Search Profiles
GET /api/users/profiles/?gender=female&min_age=25&max_age=30
Authorization: Bearer <token>

# 2. Send Interest
POST /api/users/interests/
Authorization: Bearer <token>
{"receiver": 5, "message": "Hello!"}

# 3. Check Pending Interests
GET /api/users/interests/pending/
Authorization: Bearer <token>

# 4. Respond to Interest
POST /api/users/interests/3/respond/
Authorization: Bearer <token>
{"status": "accepted"}
```

### Report User (Admin Review)
```bash
# 1. User Reports
POST /api/users/reports/
Authorization: Bearer <user_token>
{"reported_user": 5, "reason": "spam", "description": "..."}

# 2. Admin Views Pending
GET /api/users/reports/pending/
Authorization: Bearer <admin_token>

# 3. Admin Reviews
POST /api/users/reports/1/review/
Authorization: Bearer <admin_token>
{"status": "reviewed", "admin_notes": "..."}
```

---

## 🛠️ Testing Commands

### Using cURL

```bash
# Login
curl -X POST http://localhost:8000/api/users/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass"}'

# List Profiles (Authenticated)
curl -X GET http://localhost:8000/api/users/profiles/ \
  -H "Authorization: Bearer <token>"

# Send Interest
curl -X POST http://localhost:8000/api/users/interests/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"receiver":5,"message":"Hello!"}'

# Upload Photo
curl -X POST http://localhost:8000/api/users/profiles/ \
  -H "Authorization: Bearer <token>" \
  -F "name=John Doe" \
  -F "gender=male" \
  -F "age=28" \
  -F "photo=@photo.jpg"
```

### Using Python Requests

```python
import requests

# Login
response = requests.post(
    'http://localhost:8000/api/users/auth/login/',
    json={'username': 'john', 'password': 'pass'}
)
token = response.json()['access']

# Headers
headers = {'Authorization': f'Bearer {token}'}

# List Profiles
response = requests.get(
    'http://localhost:8000/api/users/profiles/',
    headers=headers
)
profiles = response.json()

# Send Interest
response = requests.post(
    'http://localhost:8000/api/users/interests/',
    headers=headers,
    json={'receiver': 5, 'message': 'Hello!'}
)
```

---

## 📝 Response Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | GET request successful |
| 201 | Created | POST created successfully |
| 204 | No Content | DELETE successful |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | No/invalid token |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal error |

---

## ⚡ Performance Tips

### Filtering
```bash
# Good: Use filters
GET /api/users/profiles/?gender=male&min_age=25&max_age=35

# Bad: Get all and filter client-side
GET /api/users/profiles/
```

### Pagination
```bash
# Use page parameter
GET /api/users/profiles/?page=2

# Set page size (max 100)
GET /api/users/profiles/?page_size=20
```

### Search
```bash
# Use search parameter
GET /api/users/profiles/?search=Mumbai+Engineer
```

---

## 🐛 Common Errors

### 401 Unauthorized
```json
{"detail": "Authentication credentials were not provided."}
```
**Fix:** Add Authorization header

### 403 Forbidden
```json
{"error": "Only the receiver can respond to this interest"}
```
**Fix:** Check permissions and user role

### 400 Bad Request
```json
{"receiver": ["You cannot send interest to yourself."]}
```
**Fix:** Follow business rules

### Token Expired
```json
{"detail": "Token is invalid or expired"}
```
**Fix:** Refresh token or login again

---

## 📚 Resources

### Files
- `backend/users/views.py` - ViewSets implementation (~700 lines)
- `backend/users/permissions.py` - Custom permissions (6 classes)
- `backend/users/urls.py` - URL configuration
- `backend/users/serializers.py` - Serializers (13 classes)

### Documentation
- `VIEWSETS_DOCUMENTATION.md` - Complete API guide
- `SERIALIZERS_DOCUMENTATION.md` - Serializers reference
- `PERMISSIONS_DOCUMENTATION.md` - Permissions guide

---

**Total Endpoints:** 35+  
**ViewSets:** 5  
**Custom Actions:** 15+  
**Permissions:** 6 custom classes  
**Authentication:** JWT (Simple JWT)

**Last Updated:** October 14, 2025
