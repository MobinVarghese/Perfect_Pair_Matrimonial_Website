# API Routes Documentation
## Matrimonial Website - Complete URL Guide

**Created:** October 14, 2025  
**Base URL:** `http://localhost:8000`  
**Total Endpoints:** 40+

---

## Table of Contents
1. [URL Structure](#url-structure)
2. [Authentication Endpoints](#authentication-endpoints)
3. [User Management Endpoints](#user-management-endpoints)
4. [Profile Endpoints](#profile-endpoints)
5. [Interest Endpoints](#interest-endpoints)
6. [Report Endpoints](#report-endpoints)
7. [OTP Verification Endpoints](#otp-verification-endpoints)
8. [Export Endpoints](#export-endpoints)
9. [URL Patterns Summary](#url-patterns-summary)
10. [Testing URLs](#testing-urls)

---

## URL Structure

### Files
- **`backend/urls.py`** - Main URL configuration
- **`users/urls.py`** - Users app URL configuration
- **Router:** DefaultRouter for ViewSets

### Base URL Prefix
All API endpoints are prefixed with `/api/`

```
http://localhost:8000/api/
```

### URL Namespacing
```python
path('api/', include('users.urls', namespace='users'))
```

---

## Authentication Endpoints

### 1. Login (Obtain JWT Token)

#### Primary Endpoint (Recommended)
```
POST /api/token/
```

#### Alternative Endpoint
```
POST /api/auth/login/
```

**Permission:** AllowAny (Public)  
**Body:**
```json
{
    "username": "johndoe",
    "password": "SecurePass123!"
}
```
**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Note:** Both endpoints work identically - use whichever you prefer!

---

### 2. Refresh Token

#### Primary Endpoint (Recommended)
```
POST /api/token/refresh/
```

#### Alternative Endpoint
```
POST /api/auth/refresh/
```

**Permission:** AllowAny  
**Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Note:** Both `access` and `refresh` tokens are returned due to token rotation enabled.

---

### 3. Verify Token

#### Primary Endpoint (Recommended)
```
POST /api/token/verify/
```

#### Alternative Endpoint
```
POST /api/auth/verify/
```

**Permission:** AllowAny  
**Body:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Response (Success):**
```json
{}
```
(Empty response = valid token)

**Response (Failure):**
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```
**Status Code:** 401 Unauthorized

---

## User Management Endpoints

### 1. Register New User
```
POST /api/register/
```
**Permission:** AllowAny (Public)  
**Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
}
```

### 2. List All Users
```
GET /api/users/
```
**Permission:** IsAuthenticated  
**Query Parameters:**
- `search` - Search username, email, name
- `ordering` - Sort by date_joined, username

### 3. Get Current User
```
GET /api/users/me/
```
**Permission:** IsAuthenticated

### 4. Update Current User
```
PUT /api/users/me/update/
PATCH /api/users/me/update/
```
**Permission:** IsAuthenticated

### 5. Delete Current User (Soft Delete)
```
DELETE /api/users/me/update/
```
**Permission:** IsAuthenticated

### 6. Change Password
```
PUT /api/users/change-password/
```
**Permission:** IsAuthenticated  
**Body:**
```json
{
    "old_password": "OldPass123!",
    "new_password": "NewPass456!",
    "new_password2": "NewPass456!"
}
```

### 7. Get User by ID
```
GET /api/users/{id}/
```
**Permission:** IsAuthenticated

---

## Profile Endpoints

Base URL: `/api/profiles/`

### CRUD Operations

#### 1. List All Profiles
```
GET /api/profiles/
```
**Permission:** IsAuthenticated  
**Query Parameters:**
- `gender` - Filter by male/female/other
- `min_age` - Minimum age (18-100)
- `max_age` - Maximum age (18-100)
- `location` - Filter by location (contains)
- `search` - Search name, occupation, education, location
- `ordering` - Sort by created_at, age, name
- `page` - Page number (pagination)

**Example:**
```
GET /api/profiles/?gender=female&min_age=25&max_age=30&location=Mumbai&page=1
```

#### 2. Get Profile by ID
```
GET /api/profiles/{id}/
```
**Permission:** IsAuthenticated

#### 3. Create Profile
```
POST /api/profiles/
```
**Permission:** IsAuthenticated  
**Content-Type:** multipart/form-data  
**Body:**
```json
{
    "name": "John Doe",
    "gender": "male",
    "age": 28,
    "location": "Mumbai, India",
    "mobile_number": "+91 9876543210",
    "occupation": "Software Engineer",
    "education": "B.Tech Computer Science",
    "about": "Looking for a life partner...",
    "desired_partner_traits": "Looking for someone who...",
    "photo": <file>,
    "height": 5.8
}
```

#### 4. Update Profile
```
PUT /api/profiles/{id}/
PATCH /api/profiles/{id}/
```
**Permission:** IsAuthenticated (Own profile only)

#### 5. Delete Profile
```
DELETE /api/profiles/{id}/
```
**Permission:** IsAuthenticated (Own profile only)

### Custom Actions

#### 6. Get My Profile
```
GET /api/profiles/me/
```
**Permission:** IsAuthenticated

#### 7. Create My Profile
```
POST /api/profiles/create-mine/
```
**Permission:** IsAuthenticated

#### 8. View Profile Details
```
GET /api/profiles/{id}/view/
```
**Permission:** IsAuthenticated

---

## Interest Endpoints

Base URL: `/api/interests/`

### CRUD Operations

#### 1. List Interests
```
GET /api/interests/
```
**Permission:** IsAuthenticated  
**Query Parameters:**
- `type` - Filter by sent/received
- `status` - Filter by pending/accepted/rejected

**Example:**
```
GET /api/interests/?type=received&status=pending
```

#### 2. Get Interest by ID
```
GET /api/interests/{id}/
```
**Permission:** IsAuthenticated (Sender or Receiver)

#### 3. Send Interest
```
POST /api/interests/
```
**Permission:** IsAuthenticated  
**Body:**
```json
{
    "receiver": 5,
    "message": "Hello! I would like to connect with you. I found your profile interesting..."
}
```

**Validations:**
- Cannot send to yourself
- Cannot send duplicate interest
- Message minimum 10 characters

#### 4. Update Interest
```
PUT /api/interests/{id}/
PATCH /api/interests/{id}/
```
**Permission:** IsAuthenticated (Receiver only)

#### 5. Delete Interest
```
DELETE /api/interests/{id}/
```
**Permission:** IsAuthenticated (Sender only)

### Custom Actions

#### 6. Get Sent Interests
```
GET /api/interests/sent/
```
**Permission:** IsAuthenticated

#### 7. Get Received Interests
```
GET /api/interests/received/
```
**Permission:** IsAuthenticated

#### 8. Get Pending Interests
```
GET /api/interests/pending/
```
**Permission:** IsAuthenticated

#### 9. Respond to Interest
```
POST /api/interests/{id}/respond/
```
**Permission:** IsAuthenticated (Receiver only)  
**Body:**
```json
{
    "status": "accepted"
}
```
**Valid status:** accepted, rejected

#### 10. Cancel Interest
```
POST /api/interests/{id}/cancel/
```
**Permission:** IsAuthenticated (Sender only)  
**Note:** Can only cancel pending interests

---

## Report Endpoints

Base URL: `/api/reports/`

### CRUD Operations

#### 1. List Reports
```
GET /api/reports/
```
**Permission:** IsAuthenticated  
**Behavior:**
- Regular users: See their own reports
- Admins: See all reports

#### 2. Get Report by ID
```
GET /api/reports/{id}/
```
**Permission:** IsAuthenticated (Reporter or Admin)

#### 3. Create Report
```
POST /api/reports/
```
**Permission:** IsAuthenticated  
**Body:**
```json
{
    "reported_user": 5,
    "reason": "fake_profile",
    "description": "This profile appears to be using fake photos and information. The person claims to be..."
}
```

**Reason Choices:**
- fake_profile
- inappropriate_content
- harassment
- spam
- other

**Validations:**
- Cannot report yourself
- Cannot report same user within 24 hours
- Description minimum 20 characters

#### 4. Update Report
```
PUT /api/reports/{id}/
PATCH /api/reports/{id}/
```
**Permission:** IsAdminUser

#### 5. Delete Report
```
DELETE /api/reports/{id}/
```
**Permission:** IsAuthenticated (Reporter or Admin)

### Custom Actions

#### 6. Get My Reports
```
GET /api/reports/my-reports/
```
**Permission:** IsAuthenticated

#### 7. Get Pending Reports (Admin Only)
```
GET /api/reports/pending/
```
**Permission:** IsAdminUser

#### 8. Review Report (Admin Only)
```
POST /api/reports/{id}/review/
```
**Permission:** IsAdminUser  
**Body:**
```json
{
    "status": "reviewed",
    "admin_notes": "Investigated and found the report to be valid. User has been warned."
}
```
**Valid status:** reviewed, resolved

#### 9. Get Report Statistics (Admin Only)
```
GET /api/reports/statistics/
```
**Permission:** IsAdminUser  
**Response:**
```json
{
    "total": 25,
    "pending": 10,
    "reviewed": 8,
    "resolved": 7
}
```

---

## OTP Verification Endpoints

Base URL: `/api/otp/`

### CRUD Operations

#### 1. List OTP History
```
GET /api/otp/
```
**Permission:** IsAuthenticated  
**Note:** Users can only see their own OTP records

#### 2. Get OTP by ID
```
GET /api/otp/{id}/
```
**Permission:** IsAuthenticated (Own OTP only)

### Custom Actions

#### 3. Generate OTP
```
POST /api/otp/generate/
```
**Permission:** IsAuthenticated  
**Response:**
```json
{
    "message": "OTP generated successfully",
    "otp": "123456",
    "expires_at": "2025-10-14T11:00:00Z",
    "data": {
        "id": 1,
        "user_username": "johndoe",
        "otp": "123456",
        "is_verified": false,
        "created_at": "2025-10-14T10:50:00Z",
        "expires_at": "2025-10-14T11:00:00Z"
    }
}
```
**Note:** OTP expires in 10 minutes

#### 4. Verify OTP
```
POST /api/otp/verify/
```
**Permission:** IsAuthenticated  
**Body:**
```json
{
    "otp": "123456"
}
```
**Response (Success):**
```json
{
    "message": "OTP verified successfully",
    "verified": true
}
```

#### 5. Resend OTP
```
POST /api/otp/resend/
```
**Permission:** IsAuthenticated

---

## Export Endpoints

Base URL: `/api/export/`

### Specific Export Endpoints

#### 1. Export Profiles as PDF
```
POST /api/export/profiles/pdf/
```
**Permission:** IsAdminUser  
**Body (Optional):**
```json
{
    "date_from": "2025-01-01",
    "date_to": "2025-10-14"
}
```
**Response:**
```json
{
    "message": "Export initiated successfully",
    "file_name": "profiles_20251014_103000.pdf",
    "record_count": 150,
    "data": {
        "id": 1,
        "file_name": "profiles_20251014_103000.pdf",
        "file_type": "pdf",
        "export_type": "profiles",
        "record_count": 150
    }
}
```

#### 2. Export Profiles as Excel
```
POST /api/export/profiles/excel/
```
**Permission:** IsAdminUser  
**Body (Optional):**
```json
{
    "date_from": "2025-01-01",
    "date_to": "2025-10-14"
}
```

### Generic Export Endpoint

#### 3. Export Any Data Type
```
POST /api/export/{export_type}/{file_type}/
```
**Permission:** IsAdminUser

**Export Types:**
- users
- profiles
- reports
- interests
- all_data

**File Types:**
- pdf
- excel
- csv

**Examples:**
```
POST /api/export/users/pdf/
POST /api/export/reports/excel/
POST /api/export/interests/csv/
```

### Export Logs

#### 4. List Export Logs
```
GET /api/export-logs/
```
**Permission:** IsAdminUser  
**Query Parameters:**
- `admin_id` - Filter by admin who exported
- `file_type` - Filter by pdf/excel/csv
- `export_type` - Filter by users/profiles/reports/interests

#### 5. Get Export Log by ID
```
GET /api/export-logs/{id}/
```
**Permission:** IsAdminUser

#### 6. Export Data (Generic)
```
POST /api/export-logs/export-data/
```
**Permission:** IsAdminUser  
**Body:**
```json
{
    "file_type": "excel",
    "export_type": "users",
    "date_from": "2025-01-01",
    "date_to": "2025-10-14"
}
```

---

## URL Patterns Summary

### Complete Endpoint List

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| **AUTHENTICATION (Primary)** |
| POST | `/api/token/` | AllowAny | Login and get JWT tokens |
| POST | `/api/token/refresh/` | AllowAny | Refresh access token |
| POST | `/api/token/verify/` | AllowAny | Verify token validity |
| **AUTHENTICATION (Alternative - same functionality)** |
| POST | `/api/auth/login/` | AllowAny | Login and get JWT tokens |
| POST | `/api/auth/refresh/` | AllowAny | Refresh access token |
| POST | `/api/auth/verify/` | AllowAny | Verify token validity |
| **USER MANAGEMENT** |
| POST | `/api/register/` | AllowAny | Register new user |
| GET | `/api/users/` | IsAuthenticated | List all users |
| GET | `/api/users/me/` | IsAuthenticated | Get current user |
| PUT/PATCH | `/api/users/me/update/` | IsAuthenticated | Update current user |
| DELETE | `/api/users/me/update/` | IsAuthenticated | Delete current user |
| PUT | `/api/users/change-password/` | IsAuthenticated | Change password |
| GET | `/api/users/{id}/` | IsAuthenticated | Get user by ID |
| **PROFILES** |
| GET | `/api/profiles/` | IsAuthenticated | List profiles (with filters) |
| POST | `/api/profiles/` | IsAuthenticated | Create profile |
| GET | `/api/profiles/{id}/` | IsAuthenticated | Get profile by ID |
| PUT/PATCH | `/api/profiles/{id}/` | IsOwner | Update profile |
| DELETE | `/api/profiles/{id}/` | IsOwner | Delete profile |
| GET | `/api/profiles/me/` | IsAuthenticated | Get my profile |
| POST | `/api/profiles/create-mine/` | IsAuthenticated | Create my profile |
| GET | `/api/profiles/{id}/view/` | IsAuthenticated | View profile details |
| **INTERESTS** |
| GET | `/api/interests/` | IsAuthenticated | List interests |
| POST | `/api/interests/` | IsAuthenticated | Send interest |
| GET | `/api/interests/{id}/` | IsParticipant | Get interest by ID |
| PUT/PATCH | `/api/interests/{id}/` | IsReceiver | Update interest |
| DELETE | `/api/interests/{id}/` | IsSender | Delete interest |
| GET | `/api/interests/sent/` | IsAuthenticated | Get sent interests |
| GET | `/api/interests/received/` | IsAuthenticated | Get received interests |
| GET | `/api/interests/pending/` | IsAuthenticated | Get pending interests |
| POST | `/api/interests/{id}/respond/` | IsReceiver | Accept/reject interest |
| POST | `/api/interests/{id}/cancel/` | IsSender | Cancel interest |
| **REPORTS** |
| GET | `/api/reports/` | IsAuthenticated | List reports |
| POST | `/api/reports/` | IsAuthenticated | Create report |
| GET | `/api/reports/{id}/` | IsOwnerOrAdmin | Get report by ID |
| GET | `/api/reports/my-reports/` | IsAuthenticated | Get my reports |
| GET | `/api/reports/pending/` | IsAdminUser | Get pending reports |
| POST | `/api/reports/{id}/review/` | IsAdminUser | Review report |
| GET | `/api/reports/statistics/` | IsAdminUser | Get statistics |
| **OTP VERIFICATION** |
| GET | `/api/otp/` | IsAuthenticated | List OTP history |
| POST | `/api/otp/generate/` | IsAuthenticated | Generate OTP |
| POST | `/api/otp/verify/` | IsAuthenticated | Verify OTP |
| POST | `/api/otp/resend/` | IsAuthenticated | Resend OTP |
| **EXPORTS** |
| POST | `/api/export/profiles/pdf/` | IsAdminUser | Export profiles as PDF |
| POST | `/api/export/profiles/excel/` | IsAdminUser | Export profiles as Excel |
| POST | `/api/export/{type}/{format}/` | IsAdminUser | Generic export |
| GET | `/api/export-logs/` | IsAdminUser | List export logs |
| POST | `/api/export-logs/export-data/` | IsAdminUser | Export data |

**Total Endpoints:** 46 (43 unique + 3 alternative auth endpoints)

---

## Testing URLs

### Using cURL

#### 1. Login (Primary Endpoint)
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"SecurePass123!"}'
```

#### 1b. Login (Alternative Endpoint)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"SecurePass123!"}'
```

#### 2. List Profiles (with filters)
```bash
curl -X GET "http://localhost:8000/api/profiles/?gender=female&min_age=25&max_age=30" \
  -H "Authorization: Bearer <access_token>"
```

#### 3. Send Interest
```bash
curl -X POST http://localhost:8000/api/interests/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"receiver":5,"message":"Hello! I would like to connect."}'
```

#### 4. Export Profiles as PDF (Admin)
```bash
curl -X POST http://localhost:8000/api/export/profiles/pdf/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"date_from":"2025-01-01","date_to":"2025-10-14"}'
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Login
response = requests.post(
    f"{BASE_URL}/api/auth/login/",
    json={"username": "johndoe", "password": "SecurePass123!"}
)
token = response.json()["access"]

# Headers with authentication
headers = {"Authorization": f"Bearer {token}"}

# List Profiles
response = requests.get(
    f"{BASE_URL}/api/profiles/",
    headers=headers,
    params={"gender": "female", "min_age": 25, "max_age": 30}
)
profiles = response.json()

# Send Interest
response = requests.post(
    f"{BASE_URL}/api/interests/",
    headers=headers,
    json={"receiver": 5, "message": "Hello!"}
)
```

### Using JavaScript (Axios)

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

// Login
const login = async () => {
  const response = await axios.post(`${BASE_URL}/api/auth/login/`, {
    username: 'johndoe',
    password: 'SecurePass123!'
  });
  return response.data.access;
};

// List Profiles
const listProfiles = async (token) => {
  const response = await axios.get(`${BASE_URL}/api/profiles/`, {
    headers: { Authorization: `Bearer ${token}` },
    params: { gender: 'female', min_age: 25, max_age: 30 }
  });
  return response.data;
};

// Send Interest
const sendInterest = async (token, receiverId, message) => {
  const response = await axios.post(
    `${BASE_URL}/api/interests/`,
    { receiver: receiverId, message },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};
```

---

## URL Naming Conventions

### Reverse URL Lookup

Using Django's `reverse()` function:

```python
from django.urls import reverse

# Authentication
reverse('users:token_obtain_pair')  # /api/auth/login/
reverse('users:token_refresh')      # /api/auth/refresh/

# User Management
reverse('users:user-register')      # /api/register/
reverse('users:current-user')       # /api/users/me/

# ViewSet URLs
reverse('users:profile-list')       # /api/profiles/
reverse('users:profile-detail', kwargs={'pk': 1})  # /api/profiles/1/
reverse('users:interest-list')      # /api/interests/
reverse('users:report-list')        # /api/reports/
reverse('users:otp-list')          # /api/otp/

# Custom Actions
reverse('users:profile-me')         # /api/profiles/me/
reverse('users:interest-sent')      # /api/interests/sent/
reverse('users:report-pending')     # /api/reports/pending/
reverse('users:otp-generate')       # /api/otp/generate/

# Export URLs
reverse('users:export-profiles-pdf')   # /api/export/profiles/pdf/
reverse('users:export-profiles-excel') # /api/export/profiles/excel/
```

---

## Router Configuration

### DefaultRouter Auto-generated URLs

The DefaultRouter automatically creates these URL patterns for each ViewSet:

| URL Pattern | Name | Method | Action |
|-------------|------|--------|--------|
| `{prefix}/` | `{basename}-list` | GET | list |
| `{prefix}/` | `{basename}-list` | POST | create |
| `{prefix}/{pk}/` | `{basename}-detail` | GET | retrieve |
| `{prefix}/{pk}/` | `{basename}-detail` | PUT | update |
| `{prefix}/{pk}/` | `{basename}-detail` | PATCH | partial_update |
| `{prefix}/{pk}/` | `{basename}-detail` | DELETE | destroy |
| `{prefix}/{custom}/` | `{basename}-{action}` | * | custom action |

### Custom Actions

Custom actions are added with `@action` decorator:

```python
@action(detail=False, methods=['get'], url_path='me')
def my_profile(self, request):
    # Creates: /api/profiles/me/
    pass

@action(detail=True, methods=['post'], url_path='respond')
def respond_to_interest(self, request, pk=None):
    # Creates: /api/interests/{id}/respond/
    pass
```

---

## Conclusion

This URL configuration provides:
- ✅ **Clear structure** with /api/ prefix
- ✅ **RESTful design** following best practices
- ✅ **43 endpoints** covering all functionality
- ✅ **JWT authentication** on protected routes
- ✅ **Role-based access** (User vs Admin)
- ✅ **Filtering & search** capabilities
- ✅ **Custom actions** for specific use cases
- ✅ **Export functionality** (PDF, Excel)

**Files:**
- `backend/urls.py` - Main URL configuration
- `users/urls.py` - Users app URLs (with router)

**Last Updated:** October 14, 2025  
**Version:** 1.0
