# Django REST Framework ViewSets Documentation
## Matrimonial Website - Complete API Guide

**Created:** October 14, 2025  
**File:** `backend/users/views.py`  
**Total ViewSets:** 5 + 5 User Management Views

---

## Table of Contents
1. [Authentication & JWT Setup](#authentication--jwt-setup)
2. [User Management Views](#user-management-views)
3. [Profile ViewSet](#profile-viewset)
4. [OTP Verification ViewSet](#otp-verification-viewset)
5. [Interest ViewSet](#interest-viewset)
6. [Report ViewSet](#report-viewset)
7. [Export Log ViewSet](#export-log-viewset)
8. [Permissions](#permissions)
9. [API Endpoints Reference](#api-endpoints-reference)

---

## Authentication & JWT Setup

### JWT Token Endpoints

#### 1. Login (Obtain Token)
```
POST /api/users/auth/login/
```
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

#### 2. Refresh Token
```
POST /api/users/auth/refresh/
```
**Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 3. Verify Token
```
POST /api/users/auth/verify/
```
**Body:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using JWT in Requests
Add Authorization header to all protected endpoints:
```
Authorization: Bearer <access_token>
```

---

## User Management Views

### 1. UserRegistrationView
**Endpoint:** `POST /api/users/register/`  
**Permission:** AllowAny (Public)  
**Purpose:** Register new user account

**Request:**
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

**Response:**
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe"
    },
    "message": "User registered successfully. Please create your profile."
}
```

### 2. UserListView
**Endpoint:** `GET /api/users/users/`  
**Permission:** IsAuthenticated  
**Purpose:** List all active users

**Query Parameters:**
- `search` - Search by username, email, name
- `ordering` - Sort by date_joined, username

**Response:**
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/users/users/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "johndoe",
            "email": "john@example.com",
            "profile": {...}
        }
    ]
}
```

### 3. CurrentUserView
**Endpoint:** `GET /api/users/users/me/`  
**Permission:** IsAuthenticated  
**Purpose:** Get current authenticated user

**Response:**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "profile": {
        "name": "John Doe",
        "age": 28,
        "gender": "male",
        ...
    }
}
```

### 4. UserDetailView
**Endpoint:** `GET/PUT/PATCH/DELETE /api/users/users/me/update/`  
**Permission:** IsAuthenticated (Own account only)  
**Purpose:** Update or delete user account

**Update Request:**
```json
{
    "email": "newemail@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Delete:** Performs soft delete (sets is_active=False)

### 5. ChangePasswordView
**Endpoint:** `PUT /api/users/users/change-password/`  
**Permission:** IsAuthenticated  
**Purpose:** Change user password securely

**Request:**
```json
{
    "old_password": "OldPass123!",
    "new_password": "NewPass456!",
    "new_password2": "NewPass456!"
}
```

**Response:**
```json
{
    "message": "Password changed successfully"
}
```

---

## Profile ViewSet

**Base URL:** `/api/users/profiles/`  
**Permission:** IsAuthenticated  
**Model:** Profile

### CRUD Operations

#### 1. List Profiles
```
GET /api/users/profiles/
```
**Query Parameters:**
- `gender` - Filter by gender (male/female/other)
- `min_age` - Minimum age filter
- `max_age` - Maximum age filter
- `location` - Filter by location (contains)
- `search` - Search name, location, occupation, education
- `ordering` - Sort by created_at, age, name

**Example:**
```
GET /api/users/profiles/?gender=female&min_age=25&max_age=30&location=Mumbai
```

**Response:**
```json
{
    "count": 15,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user_username": "johndoe",
            "name": "John Doe",
            "gender": "male",
            "age": 28,
            "location": "Mumbai, India",
            "photo_url": "http://localhost:8000/media/profile_photos/john.jpg",
            ...
        }
    ]
}
```

#### 2. Retrieve Profile
```
GET /api/users/profiles/{id}/
```

#### 3. Create Profile
```
POST /api/users/profiles/
```
**Content-Type:** multipart/form-data (for photo upload)

**Request:**
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
    "photo": <file>
}
```

#### 4. Update Profile
```
PUT/PATCH /api/users/profiles/{id}/
```
**Note:** Users can only update their own profile

#### 5. Delete Profile
```
DELETE /api/users/profiles/{id}/
```

### Custom Actions

#### Get My Profile
```
GET /api/users/profiles/me/
```
**Response:** Current user's profile or 404 if not created

#### Create My Profile
```
POST /api/users/profiles/create-mine/
```
**Purpose:** Simplified endpoint to create profile for current user

#### View Profile Details
```
GET /api/users/profiles/{id}/view/
```
**Purpose:** View detailed profile information

---

## OTP Verification ViewSet

**Base URL:** `/api/users/otp/`  
**Permission:** IsAuthenticated  
**Model:** OTPVerification

### CRUD Operations

#### 1. List OTP History
```
GET /api/users/otp/
```
**Response:** List of user's own OTP records

### Custom Actions

#### Generate OTP
```
POST /api/users/otp/generate/
```
**Request:** No body required

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

#### Verify OTP
```
POST /api/users/otp/verify/
```
**Request:**
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

**Response (Error):**
```json
{
    "error": "OTP has expired. Please request a new one."
}
```

#### Resend OTP
```
POST /api/users/otp/resend/
```
**Purpose:** Generate and send new OTP

---

## Interest ViewSet

**Base URL:** `/api/users/interests/`  
**Permission:** IsAuthenticated  
**Model:** Interest

### CRUD Operations

#### 1. List Interests
```
GET /api/users/interests/
```
**Query Parameters:**
- `type` - Filter by sent/received (default: both)
- `status` - Filter by pending/accepted/rejected

**Example:**
```
GET /api/users/interests/?type=received&status=pending
```

**Response:**
```json
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "sender": 2,
            "sender_username": "janedoe",
            "sender_name": "Jane Doe",
            "receiver": 1,
            "receiver_username": "johndoe",
            "receiver_name": "John Doe",
            "status": "pending",
            "message": "Hello! I'd like to connect.",
            "created_at": "2025-10-14T10:00:00Z",
            "responded_at": null
        }
    ]
}
```

#### 2. Retrieve Interest
```
GET /api/users/interests/{id}/
```

#### 3. Send Interest
```
POST /api/users/interests/
```
**Request:**
```json
{
    "receiver": 5,
    "message": "Hello! I would like to connect with you."
}
```

**Validations:**
- Cannot send to yourself
- Cannot send duplicate interest
- Message must be at least 10 characters

#### 4. Update Interest
```
PUT/PATCH /api/users/interests/{id}/
```
**Note:** Only receiver can update (respond)

#### 5. Delete Interest
```
DELETE /api/users/interests/{id}/
```
**Note:** Only sender can delete (cancel)

### Custom Actions

#### Get Sent Interests
```
GET /api/users/interests/sent/
```
**Response:** All interests sent by current user

#### Get Received Interests
```
GET /api/users/interests/received/
```
**Response:** All interests received by current user

#### Get Pending Interests
```
GET /api/users/interests/pending/
```
**Response:** Pending interests received by current user

#### Respond to Interest
```
POST /api/users/interests/{id}/respond/
```
**Request:**
```json
{
    "status": "accepted"
}
```
**Valid status:** accepted, rejected

**Response:**
```json
{
    "message": "Interest accepted successfully",
    "data": {
        "id": 1,
        "status": "accepted",
        "responded_at": "2025-10-14T11:00:00Z",
        ...
    }
}
```

**Permissions:**
- Only receiver can respond
- Can only respond to pending interests

#### Cancel Interest
```
POST /api/users/interests/{id}/cancel/
```
**Purpose:** Cancel a sent interest (pending only)

**Response:**
```json
{
    "message": "Interest cancelled successfully"
}
```

**Permissions:**
- Only sender can cancel
- Can only cancel pending interests

---

## Report ViewSet

**Base URL:** `/api/users/reports/`  
**Permission:** IsAuthenticated (Users), IsAdminUser (Admin actions)  
**Model:** Report

### CRUD Operations

#### 1. List Reports
```
GET /api/users/reports/
```
**Behavior:**
- Regular users: See their own reports
- Admins: See all reports

**Response:**
```json
{
    "count": 3,
    "results": [
        {
            "id": 1,
            "reporter_username": "johndoe",
            "reported_user_username": "spammer",
            "reason": "spam",
            "reason_display": "Spam",
            "description": "This user is sending spam messages...",
            "status": "pending",
            "status_display": "Pending",
            "created_at": "2025-10-14T10:00:00Z"
        }
    ]
}
```

#### 2. Retrieve Report
```
GET /api/users/reports/{id}/
```

#### 3. Create Report
```
POST /api/users/reports/
```
**Request:**
```json
{
    "reported_user": 5,
    "reason": "fake_profile",
    "description": "This profile appears to be using fake photos and information. The person claims to be someone they are not."
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
- Description must be at least 20 characters

#### 4. Update Report
```
PUT/PATCH /api/users/reports/{id}/
```
**Note:** Regular users cannot update reports

#### 5. Delete Report
```
DELETE /api/users/reports/{id}/
```
**Permission:** Reporter or Admin

### Custom Actions (Admin Only)

#### Get My Reports
```
GET /api/users/reports/my-reports/
```
**Response:** All reports made by current user

#### Get Pending Reports (Admin)
```
GET /api/users/reports/pending/
```
**Permission:** IsAdminUser  
**Response:** All pending reports

#### Review Report (Admin)
```
POST /api/users/reports/{id}/review/
```
**Permission:** IsAdminUser

**Request:**
```json
{
    "status": "reviewed",
    "admin_notes": "Investigated and found the report to be valid. User has been warned."
}
```

**Valid status:** reviewed, resolved

**Response:**
```json
{
    "message": "Report marked as reviewed",
    "data": {
        "id": 1,
        "status": "reviewed",
        "reviewed_by_username": "admin",
        "reviewed_at": "2025-10-14T11:00:00Z",
        "admin_notes": "Investigated and found..."
    }
}
```

#### Report Statistics (Admin)
```
GET /api/users/reports/statistics/
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

## Export Log ViewSet

**Base URL:** `/api/users/export-logs/`  
**Permission:** IsAdminUser (Admin only)  
**Model:** ExportLog

### CRUD Operations

#### 1. List Export Logs
```
GET /api/users/export-logs/
```
**Query Parameters:**
- `admin_id` - Filter by admin who exported
- `file_type` - Filter by pdf/excel/csv
- `export_type` - Filter by users/profiles/reports/interests

**Response:**
```json
{
    "count": 10,
    "results": [
        {
            "id": 1,
            "admin_username": "admin",
            "admin_full_name": "Admin User",
            "file_type": "excel",
            "file_type_display": "Excel",
            "file_name": "users_20251014_103000.excel",
            "export_type": "users",
            "record_count": 150,
            "created_at": "2025-10-14T10:30:00Z"
        }
    ]
}
```

#### 2. Retrieve Export Log
```
GET /api/users/export-logs/{id}/
```

**Note:** Create, Update, Delete not allowed (read-only)

### Custom Actions

#### Export Data
```
POST /api/users/export-logs/export-data/
```
**Permission:** IsAdminUser

**Request:**
```json
{
    "file_type": "excel",
    "export_type": "users",
    "date_from": "2025-01-01",
    "date_to": "2025-10-14"
}
```

**File Type Choices:** pdf, excel, csv  
**Export Type Choices:** users, profiles, reports, interests, all_data

**Response:**
```json
{
    "message": "Export initiated successfully",
    "file_name": "users_20251014_103000.excel",
    "record_count": 150,
    "data": {
        "id": 1,
        "file_name": "users_20251014_103000.excel",
        ...
    }
}
```

**Validations:**
- Date range max 1 year
- date_to must be after date_from

---

## Permissions

### Built-in Permissions
- **AllowAny** - Public access (registration, login)
- **IsAuthenticated** - Requires valid JWT token
- **IsAdminUser** - Requires is_admin=True

### Custom Permissions

#### IsOwnerOrReadOnly
- Allows read to all authenticated users
- Allows write only to owner
- Used for: Profiles, Interests

#### IsAdminOrReadOnly
- Allows read to all authenticated users
- Allows write only to admins
- Used for: Admin-managed content

#### IsReportOwnerOrAdmin
- Reporter can view their own reports
- Admins can view and manage all reports
- Used for: Reports

#### IsProfileOwner
- Allows read to all authenticated users
- Allows write only to profile owner
- Used for: Profile updates

#### IsInterestParticipant
- Both sender and receiver can view
- Sender can cancel (delete)
- Receiver can respond (update)
- Used for: Interests

---

## API Endpoints Reference

### Authentication
| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| POST | `/api/users/auth/login/` | AllowAny | Login and get JWT tokens |
| POST | `/api/users/auth/refresh/` | AllowAny | Refresh access token |
| POST | `/api/users/auth/verify/` | AllowAny | Verify token validity |

### User Management
| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| POST | `/api/users/register/` | AllowAny | Register new user |
| GET | `/api/users/users/` | IsAuthenticated | List all users |
| GET | `/api/users/users/me/` | IsAuthenticated | Get current user |
| PUT/PATCH | `/api/users/users/me/update/` | IsAuthenticated | Update current user |
| DELETE | `/api/users/users/me/update/` | IsAuthenticated | Delete (deactivate) account |
| PUT | `/api/users/users/change-password/` | IsAuthenticated | Change password |

### Profiles
| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/users/profiles/` | IsAuthenticated | List profiles (with filters) |
| POST | `/api/users/profiles/` | IsAuthenticated | Create profile |
| GET | `/api/users/profiles/{id}/` | IsAuthenticated | Get profile details |
| PUT/PATCH | `/api/users/profiles/{id}/` | IsOwner | Update profile |
| DELETE | `/api/users/profiles/{id}/` | IsOwner | Delete profile |
| GET | `/api/users/profiles/me/` | IsAuthenticated | Get my profile |
| POST | `/api/users/profiles/create-mine/` | IsAuthenticated | Create my profile |
| GET | `/api/users/profiles/{id}/view/` | IsAuthenticated | View profile |

### OTP Verification
| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/users/otp/` | IsAuthenticated | List OTP history |
| POST | `/api/users/otp/generate/` | IsAuthenticated | Generate new OTP |
| POST | `/api/users/otp/verify/` | IsAuthenticated | Verify OTP code |
| POST | `/api/users/otp/resend/` | IsAuthenticated | Resend OTP |

### Interests
| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/users/interests/` | IsAuthenticated | List interests |
| POST | `/api/users/interests/` | IsAuthenticated | Send interest |
| GET | `/api/users/interests/{id}/` | IsParticipant | Get interest details |
| PUT/PATCH | `/api/users/interests/{id}/` | IsReceiver | Update interest |
| DELETE | `/api/users/interests/{id}/` | IsSender | Cancel interest |
| GET | `/api/users/interests/sent/` | IsAuthenticated | Get sent interests |
| GET | `/api/users/interests/received/` | IsAuthenticated | Get received interests |
| GET | `/api/users/interests/pending/` | IsAuthenticated | Get pending interests |
| POST | `/api/users/interests/{id}/respond/` | IsReceiver | Accept/reject interest |
| POST | `/api/users/interests/{id}/cancel/` | IsSender | Cancel interest |

### Reports
| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/users/reports/` | IsAuthenticated | List reports |
| POST | `/api/users/reports/` | IsAuthenticated | Create report |
| GET | `/api/users/reports/{id}/` | IsOwnerOrAdmin | Get report details |
| GET | `/api/users/reports/my-reports/` | IsAuthenticated | Get my reports |
| GET | `/api/users/reports/pending/` | IsAdminUser | Get pending reports |
| POST | `/api/users/reports/{id}/review/` | IsAdminUser | Review report |
| GET | `/api/users/reports/statistics/` | IsAdminUser | Get statistics |

### Export Logs
| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | `/api/users/export-logs/` | IsAdminUser | List export logs |
| GET | `/api/users/export-logs/{id}/` | IsAdminUser | Get export log details |
| POST | `/api/users/export-logs/export-data/` | IsAdminUser | Export data |

---

## Request/Response Examples

### Complete User Flow

#### 1. Register
```bash
POST /api/users/register/
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### 2. Login
```bash
POST /api/users/auth/login/
{
    "username": "johndoe",
    "password": "SecurePass123!"
}
# Returns: {"access": "...", "refresh": "..."}
```

#### 3. Create Profile
```bash
POST /api/users/profiles/create-mine/
Authorization: Bearer <access_token>
{
    "name": "John Doe",
    "gender": "male",
    "age": 28,
    "location": "Mumbai, India",
    "mobile_number": "+91 9876543210",
    "occupation": "Software Engineer"
}
```

#### 4. Search Profiles
```bash
GET /api/users/profiles/?gender=female&min_age=25&max_age=30&location=Mumbai
Authorization: Bearer <access_token>
```

#### 5. Send Interest
```bash
POST /api/users/interests/
Authorization: Bearer <access_token>
{
    "receiver": 5,
    "message": "Hello! I'd like to connect."
}
```

#### 6. Respond to Interest
```bash
POST /api/users/interests/3/respond/
Authorization: Bearer <access_token>
{
    "status": "accepted"
}
```

---

## Error Responses

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "error": "Only the receiver can respond to this interest"
}
```

### 400 Bad Request
```json
{
    "receiver": ["You cannot send interest to yourself."],
    "message": ["Message should be at least 10 characters long."]
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

---

## Testing with cURL

### Get JWT Token
```bash
curl -X POST http://localhost:8000/api/users/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"SecurePass123!"}'
```

### Make Authenticated Request
```bash
curl -X GET http://localhost:8000/api/users/profiles/ \
  -H "Authorization: Bearer <access_token>"
```

### Upload Photo
```bash
curl -X POST http://localhost:8000/api/users/profiles/ \
  -H "Authorization: Bearer <access_token>" \
  -F "name=John Doe" \
  -F "gender=male" \
  -F "age=28" \
  -F "location=Mumbai" \
  -F "mobile_number=+919876543210" \
  -F "photo=@/path/to/photo.jpg"
```

---

## Conclusion

This comprehensive API implementation provides:
- ✅ **Full CRUD operations** for all models
- ✅ **JWT authentication** on all protected endpoints
- ✅ **Role-based permissions** (User vs Admin)
- ✅ **Custom actions** for specific use cases
- ✅ **Filtering & search** capabilities
- ✅ **Pagination** for list views
- ✅ **File upload** support (profile photos)
- ✅ **Business logic validation** (no self-interest, etc.)

**Total Endpoints:** 35+  
**ViewSets:** 5  
**Custom Actions:** 15+  
**Permissions:** 6 custom classes

**Last Updated:** October 14, 2025  
**Version:** 1.0
