# JWT Authentication Architecture
## System Architecture & Flow Diagram

**Date:** October 14, 2025  
**Status:** ✅ Production Ready

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                             │
│                     http://localhost:3000                            │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Authentication Context / Hooks                             │   │
│  │  - useAuth()                                                │   │
│  │  - login(), logout(), getCurrentUser()                      │   │
│  │  - Token storage (localStorage)                             │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Axios Instance with Interceptors                           │   │
│  │  - Request: Add "Bearer <token>" header                     │   │
│  │  - Response: Auto-refresh on 401 error                      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                       │
└──────────────────────────────┼───────────────────────────────────────┘
                               │
                               │ HTTP Requests
                               │ Authorization: Bearer <token>
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│                         DJANGO BACKEND                               │
│                     http://localhost:8000                            │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  CORS Middleware                                            │   │
│  │  - Allow: localhost:3000, 127.0.0.1:3000                    │   │
│  │  - Allow credentials: True                                  │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  URL Router                                                  │   │
│  │  /api/token/          → TokenObtainPairView                 │   │
│  │  /api/token/refresh/  → TokenRefreshView                    │   │
│  │  /api/token/verify/   → TokenVerifyView                     │   │
│  │  /api/profiles/       → ProfileViewSet                      │   │
│  │  /api/interests/      → InterestViewSet                     │   │
│  │  /api/reports/        → ReportViewSet                       │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  JWT Authentication (JWTAuthentication)                     │   │
│  │  1. Extract token from Authorization header                 │   │
│  │  2. Verify token signature with SECRET_KEY                  │   │
│  │  3. Check expiration time                                   │   │
│  │  4. Load user from database (user_id claim)                 │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Custom Permission Classes                                   │   │
│  │  - IsAuthenticated (built-in)                               │   │
│  │  - IsProfileOwner                                           │   │
│  │  - IsInterestParticipant                                    │   │
│  │  - IsReportOwnerOrAdmin                                     │   │
│  │  - IsAdminUser                                              │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  ViewSets / Views                                            │   │
│  │  - ProfileViewSet (CRUD operations)                          │   │
│  │  - InterestViewSet (Send/respond to interests)              │   │
│  │  - ReportViewSet (Create/review reports)                    │   │
│  │  - ExportLogViewSet (Admin exports)                         │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Database (SQLite / MySQL)                                   │   │
│  │  - User (auth.User)                                         │   │
│  │  - Profile                                                  │   │
│  │  - Interest                                                 │   │
│  │  - Report                                                   │   │
│  │  - OTPVerification                                          │   │
│  │  - OutstandingToken (JWT blacklist)                        │   │
│  │  - BlacklistedToken (JWT blacklist)                        │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Authentication Flow

### 1. User Login Flow

```
┌──────────┐                  ┌──────────┐                  ┌──────────┐
│          │  POST /api/token/  │          │                  │          │
│  Client  │  ─────────────────>│  Django  │                  │ Database │
│          │  username/password │          │                  │          │
│          │                    │          │  Verify User     │          │
│          │                    │          │  ────────────────>│          │
│          │                    │          │                  │          │
│          │                    │          │  User Found      │          │
│          │                    │          │  <────────────────│          │
│          │                    │          │                  │          │
│          │                    │  Generate JWT Tokens:       │          │
│          │                    │  - Access (60 min)          │          │
│          │                    │  - Refresh (7 days)         │          │
│          │                    │                             │          │
│          │  Return Tokens     │          │                  │          │
│          │  <─────────────────│          │                  │          │
│          │  {access, refresh} │          │                  │          │
└──────────┘                  └──────────┘                  └──────────┘

Client stores tokens in localStorage or cookies
```

### 2. Authenticated Request Flow

```
┌──────────┐                  ┌──────────┐                  ┌──────────┐
│          │  GET /api/profiles/ │          │                  │          │
│  Client  │  ─────────────────>│  Django  │                  │ Database │
│          │  Authorization:    │          │                  │          │
│          │  Bearer <token>    │          │                  │          │
│          │                    │          │                  │          │
│          │                    │  1. Extract token           │          │
│          │                    │  2. Verify signature        │          │
│          │                    │  3. Check expiration        │          │
│          │                    │  4. Get user_id from claims │          │
│          │                    │                             │          │
│          │                    │          │  Load User       │          │
│          │                    │          │  ────────────────>│          │
│          │                    │          │                  │          │
│          │                    │          │  User Data       │          │
│          │                    │          │  <────────────────│          │
│          │                    │          │                  │          │
│          │                    │  5. Check permissions       │          │
│          │                    │     (IsAuthenticated, etc.) │          │
│          │                    │                             │          │
│          │                    │  6. Execute view logic      │          │
│          │                    │                             │          │
│          │                    │          │  Query Profiles  │          │
│          │                    │          │  ────────────────>│          │
│          │                    │          │                  │          │
│          │                    │          │  Profile Data    │          │
│          │                    │          │  <────────────────│          │
│          │                    │          │                  │          │
│          │  Return Data       │          │                  │          │
│          │  <─────────────────│          │                  │          │
│          │  {profiles list}   │          │                  │          │
└──────────┘                  └──────────┘                  └──────────┘
```

### 3. Token Refresh Flow

```
┌──────────┐                  ┌──────────┐                  ┌──────────┐
│          │  POST              │          │                  │          │
│  Client  │  /api/token/refresh/│ Django  │                  │ Database │
│          │  ─────────────────>│          │                  │          │
│          │  {refresh: "..."}  │          │                  │          │
│          │                    │          │                  │          │
│          │                    │  1. Verify refresh token    │          │
│          │                    │  2. Check not blacklisted   │          │
│          │                    │                             │          │
│          │                    │          │  Check Blacklist │          │
│          │                    │          │  ────────────────>│          │
│          │                    │          │                  │          │
│          │                    │          │  Not Blacklisted │          │
│          │                    │          │  <────────────────│          │
│          │                    │          │                  │          │
│          │                    │  3. Generate NEW tokens:    │          │
│          │                    │     - New access token      │          │
│          │                    │     - New refresh token     │          │
│          │                    │                             │          │
│          │                    │  4. Blacklist old refresh   │          │
│          │                    │                             │          │
│          │                    │          │  Add to Blacklist│          │
│          │                    │          │  ────────────────>│          │
│          │                    │          │                  │          │
│          │  Return New Tokens │          │                  │          │
│          │  <─────────────────│          │                  │          │
│          │  {access, refresh} │          │                  │          │
└──────────┘                  └──────────┘                  └──────────┘

Client updates tokens in storage
```

### 4. Token Expiration & Auto-Refresh

```
┌──────────┐                  ┌──────────┐
│          │  GET /api/profiles/ │          │
│  Client  │  ─────────────────>│  Django  │
│          │  Bearer <expired>  │          │
│          │                    │          │
│          │  401 Unauthorized  │  Token expired!
│          │  <─────────────────│          │
│          │                    └──────────┘
│          │
│  Axios   │  Intercepts 401
│ Intercep-│
│   tor    │
│          │                  ┌──────────┐
│          │  POST              │          │
│          │  /api/token/refresh/│ Django  │
│          │  ─────────────────>│          │
│          │                    │          │
│          │  New Tokens        │          │
│          │  <─────────────────│          │
│          │                    └──────────┘
│          │
│  Update  │  Store new tokens
│  tokens  │
│          │
│          │                  ┌──────────┐
│          │  GET /api/profiles/ │          │
│  Retry   │  ─────────────────>│  Django  │
│ Original │  Bearer <new>      │          │
│ Request  │                    │          │
│          │  200 OK            │          │
│          │  <─────────────────│          │
│          │  {profiles}        │          │
└──────────┘                  └──────────┘
```

---

## 🔐 Token Structure

### Access Token (JWT)

```
Header:
{
  "alg": "HS256",           # Algorithm: HMAC SHA-256
  "typ": "JWT"              # Type: JSON Web Token
}

Payload:
{
  "token_type": "access",   # Token type
  "exp": 1728919200,        # Expiration timestamp (60 min from issue)
  "iat": 1728915600,        # Issued at timestamp
  "jti": "abc123...",       # JWT ID (unique identifier)
  "user_id": 1              # User ID from database
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  SECRET_KEY
)
```

**Lifetime:** 60 minutes  
**Purpose:** Authenticate API requests  
**Storage:** Client-side (localStorage / cookies)

### Refresh Token (JWT)

```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "token_type": "refresh",  # Token type
  "exp": 1729520400,        # Expiration timestamp (7 days from issue)
  "iat": 1728915600,        # Issued at timestamp
  "jti": "xyz789...",       # JWT ID (unique identifier)
  "user_id": 1              # User ID from database
}

Signature:
HMACSHA256(...)
```

**Lifetime:** 7 days  
**Purpose:** Obtain new access tokens  
**Storage:** Client-side (localStorage / cookies)  
**Note:** Blacklisted after use (token rotation)

---

## 🛡️ Permission System

### Permission Hierarchy

```
┌───────────────────────────────────────────────────────────┐
│                     Public Access                          │
│  - Registration (/api/register/)                          │
│  - Login (/api/token/)                                    │
│  - Token Refresh (/api/token/refresh/)                   │
└───────────────────────────────────────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────────────────┐
│                  IsAuthenticated                           │
│  Base requirement for all protected endpoints             │
│                                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │            View All (Read-Only)                     │  │
│  │  - List all profiles                                │  │
│  │  - List all users                                   │  │
│  │  - View profile details                             │  │
│  └────────────────────────────────────────────────────┘  │
│                       │                                    │
│                       ▼                                    │
│  ┌────────────────────────────────────────────────────┐  │
│  │         Manage Own Resources                        │  │
│  │  IsOwner / IsProfileOwner                          │  │
│  │  - Edit own profile                                 │  │
│  │  - Delete own account                               │  │
│  │  - Change own password                              │  │
│  │  - View own OTP records                             │  │
│  └────────────────────────────────────────────────────┘  │
│                       │                                    │
│                       ▼                                    │
│  ┌────────────────────────────────────────────────────┐  │
│  │      Interact with Others                           │  │
│  │  IsInterestParticipant                             │  │
│  │  - Send interests                                   │  │
│  │  - Respond to interests                             │  │
│  │  - Cancel sent interests                            │  │
│  │  - Create reports                                   │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────────────────┐
│                    IsAdminUser                             │
│  Additional privileges for administrators                 │
│                                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │           Admin-Only Actions                        │  │
│  │  - View all reports (not just own)                  │  │
│  │  - Review and resolve reports                       │  │
│  │  - View report statistics                           │  │
│  │  - Export data (PDF, Excel)                         │  │
│  │  - View export logs                                 │  │
│  │  - Manage all users                                 │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

### Permission Logic Flow

```
                    ┌───────────────────┐
                    │  Incoming Request  │
                    └─────────┬─────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │ Check Authentication    │
                │ (JWT Token Valid?)      │
                └─────────┬───────────────┘
                          │
                   ┌──────┴──────┐
                   │             │
                  Yes           No
                   │             │
                   │             ▼
                   │    ┌──────────────┐
                   │    │ Return 401   │
                   │    │ Unauthorized │
                   │    └──────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Check View-Level     │
        │ Permissions          │
        │ (permission_classes) │
        └──────────┬───────────┘
                   │
            ┌──────┴──────┐
            │             │
          Pass          Fail
            │             │
            │             ▼
            │    ┌──────────────┐
            │    │ Return 403   │
            │    │ Forbidden    │
            │    └──────────────┘
            │
            ▼
   ┌──────────────────────┐
   │ Check Object-Level   │
   │ Permissions          │
   │ (has_object_perm)    │
   └──────────┬───────────┘
              │
       ┌──────┴──────┐
       │             │
     Pass          Fail
       │             │
       │             ▼
       │    ┌──────────────┐
       │    │ Return 403   │
       │    │ Forbidden    │
       │    └──────────────┘
       │
       ▼
┌──────────────────┐
│ Execute View     │
│ Return Response  │
└──────────────────┘
```

---

## 🔧 Configuration Files

### settings.py

```python
# JWT Authentication
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',  # Token rotation
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### urls.py

```python
# Primary endpoints (recommended)
path('token/', TokenObtainPairView.as_view()),
path('token/refresh/', TokenRefreshView.as_view()),
path('token/verify/', TokenVerifyView.as_view()),

# Alternative endpoints (same functionality)
path('auth/login/', TokenObtainPairView.as_view()),
path('auth/refresh/', TokenRefreshView.as_view()),
path('auth/verify/', TokenVerifyView.as_view()),
```

### views.py

```python
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProfileOwner]
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

---

## 📊 Database Schema

### Token-Related Tables

```
┌─────────────────────────────────────────────────────────────┐
│  OutstandingToken                                            │
├─────────────────────────────────────────────────────────────┤
│  id            INTEGER PRIMARY KEY                           │
│  user_id       INTEGER FOREIGN KEY → auth_user.id          │
│  jti           VARCHAR(255) UNIQUE                          │
│  token         TEXT                                         │
│  created_at    DATETIME                                     │
│  expires_at    DATETIME                                     │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ One-to-One
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  BlacklistedToken                                            │
├─────────────────────────────────────────────────────────────┤
│  id            INTEGER PRIMARY KEY                           │
│  token_id      INTEGER FOREIGN KEY → OutstandingToken.id   │
│  blacklisted_at DATETIME                                    │
└─────────────────────────────────────────────────────────────┘
```

**How it works:**
1. When refresh token is used, it's moved to `BlacklistedToken`
2. Future requests with blacklisted token are rejected
3. Ensures each refresh token can only be used once

---

## 🎯 Endpoint Summary

### Authentication Endpoints (6 total)

| Endpoint (Primary) | Endpoint (Alternative) | Method | Auth | Description |
|-------------------|----------------------|--------|------|-------------|
| `/api/token/` | `/api/auth/login/` | POST | No | Login |
| `/api/token/refresh/` | `/api/auth/refresh/` | POST | No | Refresh |
| `/api/token/verify/` | `/api/auth/verify/` | POST | No | Verify |

### Protected Endpoints by Permission

| Permission | Endpoints | Count | Who Can Access |
|-----------|-----------|-------|----------------|
| Public | Register, Login, Refresh | 4 | Everyone |
| IsAuthenticated | Profiles (view), Users (view), Interests | 15+ | All authenticated users |
| IsOwner | Profile (edit own), Users (edit own) | 8 | Resource owner only |
| IsInterestParticipant | Interests (edit/delete) | 6 | Sender/Receiver |
| IsReportOwnerOrAdmin | Reports (view/edit) | 5 | Reporter or Admin |
| IsAdminUser | Exports, Statistics, Admin reports | 8 | Admins only |

**Total:** 46 endpoints (43 unique + 3 alternative auth endpoints)

---

## ✅ Security Features

### 1. Token Security
- ✅ HMAC SHA-256 signature
- ✅ Short access token lifetime (60 min)
- ✅ Token rotation on refresh
- ✅ Automatic blacklisting
- ✅ Unique JWT ID (jti) for each token

### 2. API Security
- ✅ CORS configuration
- ✅ Permission-based access control
- ✅ Object-level permissions
- ✅ User ownership validation

### 3. Database Security
- ✅ Password hashing (PBKDF2)
- ✅ Token blacklist tracking
- ✅ Soft delete for users

### 4. Production Recommendations
- ⚠️ Use HTTPS in production
- ⚠️ Move SECRET_KEY to environment variables
- ⚠️ Add rate limiting to auth endpoints
- ⚠️ Enable token blacklist cleanup (periodic task)

---

**Last Updated:** October 14, 2025  
**Version:** 1.0  
**Status:** ✅ Production Ready
