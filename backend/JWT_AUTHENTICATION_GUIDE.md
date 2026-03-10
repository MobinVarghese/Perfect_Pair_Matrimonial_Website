# JWT Authentication Integration Guide
## djangorestframework-simplejwt - Complete Setup & Usage

**Created:** October 14, 2025  
**Package:** djangorestframework-simplejwt 5.5.1  
**Status:** ✅ FULLY INTEGRATED

---

## Table of Contents
1. [Overview](#overview)
2. [Configuration](#configuration)
3. [Authentication Endpoints](#authentication-endpoints)
4. [Permissions System](#permissions-system)
5. [Usage Examples](#usage-examples)
6. [Testing Authentication](#testing-authentication)
7. [Frontend Integration](#frontend-integration)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### What is JWT?
JSON Web Token (JWT) is an open standard for securely transmitting information between parties as a JSON object. It's commonly used for authentication and information exchange.

### Implementation Details
- **Package:** `djangorestframework-simplejwt`
- **Version:** 5.5.1
- **Access Token Lifetime:** 60 minutes
- **Refresh Token Lifetime:** 7 days
- **Token Rotation:** Enabled (new refresh token on each refresh)
- **Blacklisting:** Enabled (old tokens invalidated after rotation)

### Key Features
✅ Stateless authentication (no server-side session storage)  
✅ Automatic token rotation for security  
✅ Token blacklisting to prevent token reuse  
✅ Custom permission classes for role-based access  
✅ Integration with Django REST Framework  
✅ Support for multiple authentication methods

---

## Configuration

### 1. Installed Apps (`settings.py`)

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',  # ← JWT support
    'rest_framework_simplejwt.token_blacklist',  # ← Optional: Token blacklisting
    'corsheaders',
    
    # Local apps
    'users',
]
```

### 2. REST Framework Settings

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Default: Public access
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # ← Primary auth
        'rest_framework.authentication.SessionAuthentication',  # ← Fallback for admin
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

**Key Points:**
- `DEFAULT_PERMISSION_CLASSES` is `AllowAny` - Override per view/viewset
- `JWTAuthentication` is the primary authentication method
- `SessionAuthentication` allows Django admin to work normally

### 3. JWT Settings

```python
from datetime import timedelta

SIMPLE_JWT = {
    # Token lifetimes
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),   # 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # 7 days
    
    # Token rotation & security
    'ROTATE_REFRESH_TOKENS': True,                    # Generate new refresh token
    'BLACKLIST_AFTER_ROTATION': True,                 # Invalidate old tokens
    'UPDATE_LAST_LOGIN': True,                        # Update User.last_login
    
    # Algorithm & signing
    'ALGORITHM': 'HS256',                             # HMAC SHA-256
    'SIGNING_KEY': SECRET_KEY,                        # Use Django's secret key
    
    # Authorization header
    'AUTH_HEADER_TYPES': ('Bearer',),                 # "Bearer <token>"
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',         # Header name
    
    # Token claims
    'USER_ID_FIELD': 'id',                           # User model field
    'USER_ID_CLAIM': 'user_id',                      # JWT claim name
    'TOKEN_TYPE_CLAIM': 'token_type',                # Token type claim
    
    # Token classes
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}
```

### 4. CORS Configuration

```python
# Allow requests from React frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # React dev server
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True     # Allow cookies/auth headers
```

---

## Authentication Endpoints

### Base URL
```
http://localhost:8000/api/
```

### 1. Login (Obtain Token Pair)

#### Primary Endpoint
```http
POST /api/token/
```

#### Alternative Endpoint (same functionality)
```http
POST /api/auth/login/
```

#### Request
```json
{
    "username": "johndoe",
    "password": "SecurePass123!"
}
```

#### Response (Success)
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4OTE5MjAwLCJpYXQiOjE3Mjg5MTU2MDAsImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoxfQ.signature",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyOTUyMDQwMCwiaWF0IjoxNzI4OTE1NjAwLCJqdGkiOiI5ODc2NTQzMjEwIiwidXNlcl9pZCI6MX0.signature"
}
```

#### Response (Failure)
```json
{
    "detail": "No active account found with the given credentials"
}
```
**Status Code:** 401 Unauthorized

#### Token Payload (Decoded)
```json
{
    "token_type": "access",
    "exp": 1728919200,        // Expiration timestamp
    "iat": 1728915600,        // Issued at timestamp
    "jti": "1234567890",      // JWT ID (unique)
    "user_id": 1              // User ID from database
}
```

---

### 2. Refresh Token

#### Primary Endpoint
```http
POST /api/token/refresh/
```

#### Alternative Endpoint
```http
POST /api/auth/refresh/
```

#### Request
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Response (Success)
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  // New refresh token
}
```

**Note:** Both `access` and `refresh` tokens are returned due to `ROTATE_REFRESH_TOKENS: True`

#### Response (Failure)
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```
**Status Code:** 401 Unauthorized

---

### 3. Verify Token

#### Primary Endpoint
```http
POST /api/token/verify/
```

#### Alternative Endpoint
```http
POST /api/auth/verify/
```

#### Request
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Response (Success)
```json
{}
```
**Status Code:** 200 OK  
**Note:** Empty response body indicates valid token

#### Response (Failure)
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```
**Status Code:** 401 Unauthorized

---

## Permissions System

### Overview
The project implements **role-based access control (RBAC)** using custom permission classes. Each ViewSet/View specifies which permission classes to use.

### Permission Classes

#### 1. `IsOwnerOrReadOnly`
**Location:** `users/permissions.py`

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    - Read: Allowed for any authenticated user
    - Write/Delete: Only allowed for the owner
    """
```

**Use Case:** Profiles, user data where users can view all but edit only their own

**Example:**
```python
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
```

---

#### 2. `IsAdminOrReadOnly`
**Location:** `users/permissions.py`

```python
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    - Read: Allowed for any authenticated user
    - Write/Delete: Only allowed for admins
    """
```

**Use Case:** Data that all users can view but only admins can modify

**Example:**
```python
class SystemSettingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
```

---

#### 3. `IsReportOwnerOrAdmin`
**Location:** `users/permissions.py`

```python
class IsReportOwnerOrAdmin(permissions.BasePermission):
    """
    - Reporter: Can view their own reports
    - Admin: Can view and manage all reports
    """
```

**Use Case:** Report management system

**Example:**
```python
class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsReportOwnerOrAdmin]
```

---

#### 4. `IsProfileOwner`
**Location:** `users/permissions.py`

```python
class IsProfileOwner(permissions.BasePermission):
    """
    - Read: Allowed for any authenticated user
    - Write/Delete: Only allowed to the profile owner
    """
```

**Use Case:** User profiles with strict ownership

**Example:**
```python
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProfileOwner]
```

---

#### 5. `IsInterestParticipant`
**Location:** `users/permissions.py`

```python
class IsInterestParticipant(permissions.BasePermission):
    """
    - Sender: Can view and cancel (DELETE)
    - Receiver: Can view and respond (UPDATE)
    - Both: Can view (GET)
    """
```

**Use Case:** Interest/match system in matrimonial app

**Example:**
```python
class InterestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsInterestParticipant]
```

---

#### 6. `IsAdminUser`
**Location:** `users/permissions.py`

```python
class IsAdminUser(permissions.BasePermission):
    """
    Only admin users can access
    Checks the custom User.is_admin field
    """
```

**Use Case:** Admin-only endpoints (exports, statistics, user management)

**Example:**
```python
class ExportLogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
```

---

#### 7. `IsOwner`
**Location:** `users/permissions.py`

```python
class IsOwner(permissions.BasePermission):
    """
    Only the owner can access the object
    No read permissions for others
    """
```

**Use Case:** Private data (OTP, personal settings)

**Example:**
```python
class OTPVerificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
```

---

### Permission Matrix

| Endpoint | Method | Permission | Who Can Access |
|----------|--------|------------|----------------|
| `/api/register/` | POST | AllowAny | Anyone (Public) |
| `/api/token/` | POST | AllowAny | Anyone (Public) |
| `/api/users/` | GET | IsAuthenticated | All authenticated users |
| `/api/users/me/` | GET | IsAuthenticated | Current user only |
| `/api/profiles/` | GET | IsAuthenticated | All authenticated users |
| `/api/profiles/` | POST | IsAuthenticated | All authenticated users |
| `/api/profiles/{id}/` | GET | IsAuthenticated | All authenticated users |
| `/api/profiles/{id}/` | PUT/PATCH | IsProfileOwner | Profile owner only |
| `/api/profiles/{id}/` | DELETE | IsProfileOwner | Profile owner only |
| `/api/interests/` | GET | IsAuthenticated | All authenticated users |
| `/api/interests/` | POST | IsAuthenticated | All authenticated users |
| `/api/interests/{id}/` | GET | IsInterestParticipant | Sender or Receiver |
| `/api/interests/{id}/` | PUT/PATCH | IsInterestParticipant | Receiver only |
| `/api/interests/{id}/` | DELETE | IsInterestParticipant | Sender only |
| `/api/reports/` | GET | IsAuthenticated | User (own) / Admin (all) |
| `/api/reports/` | POST | IsAuthenticated | All authenticated users |
| `/api/reports/{id}/` | GET | IsReportOwnerOrAdmin | Reporter or Admin |
| `/api/reports/{id}/review/` | POST | IsAdminUser | Admins only |
| `/api/reports/statistics/` | GET | IsAdminUser | Admins only |
| `/api/otp/` | GET | IsAuthenticated + IsOwner | Own OTP records only |
| `/api/otp/generate/` | POST | IsAuthenticated | All authenticated users |
| `/api/export/profiles/pdf/` | POST | IsAdminUser | Admins only |
| `/api/export-logs/` | GET | IsAdminUser | Admins only |

---

## Usage Examples

### 1. Complete Authentication Flow

```python
import requests

BASE_URL = "http://localhost:8000"

# Step 1: Login
login_response = requests.post(
    f"{BASE_URL}/api/token/",
    json={
        "username": "johndoe",
        "password": "SecurePass123!"
    }
)

tokens = login_response.json()
access_token = tokens["access"]
refresh_token = tokens["refresh"]

print(f"Access Token: {access_token}")
print(f"Refresh Token: {refresh_token}")

# Step 2: Make authenticated request
headers = {
    "Authorization": f"Bearer {access_token}"
}

profiles_response = requests.get(
    f"{BASE_URL}/api/profiles/",
    headers=headers
)

profiles = profiles_response.json()
print(f"Profiles: {profiles}")

# Step 3: Refresh token (when access token expires)
refresh_response = requests.post(
    f"{BASE_URL}/api/token/refresh/",
    json={
        "refresh": refresh_token
    }
)

new_tokens = refresh_response.json()
new_access_token = new_tokens["access"]
new_refresh_token = new_tokens["refresh"]  # New refresh token due to rotation

print(f"New Access Token: {new_access_token}")
print(f"New Refresh Token: {new_refresh_token}")
```

---

### 2. JavaScript (Axios) Implementation

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

// Axios instance with interceptor
const api = axios.create({
    baseURL: BASE_URL
});

let accessToken = null;
let refreshToken = null;

// Request interceptor - Add token to headers
api.interceptors.request.use(
    config => {
        if (accessToken) {
            config.headers.Authorization = `Bearer ${accessToken}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

// Response interceptor - Handle token refresh
api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        // If 401 and we haven't retried yet
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Refresh the token
                const response = await axios.post(
                    `${BASE_URL}/api/token/refresh/`,
                    { refresh: refreshToken }
                );

                accessToken = response.data.access;
                refreshToken = response.data.refresh;

                // Update authorization header
                originalRequest.headers.Authorization = `Bearer ${accessToken}`;

                // Retry original request
                return api(originalRequest);
            } catch (refreshError) {
                // Refresh failed - redirect to login
                console.error('Token refresh failed:', refreshError);
                // Redirect to login page
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

// Login function
async function login(username, password) {
    try {
        const response = await axios.post(`${BASE_URL}/api/token/`, {
            username,
            password
        });

        accessToken = response.data.access;
        refreshToken = response.data.refresh;

        // Store in localStorage
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);

        return { success: true, tokens: response.data };
    } catch (error) {
        console.error('Login failed:', error.response.data);
        return { success: false, error: error.response.data };
    }
}

// Get profiles (authenticated)
async function getProfiles() {
    try {
        const response = await api.get('/api/profiles/');
        return response.data;
    } catch (error) {
        console.error('Get profiles failed:', error);
        throw error;
    }
}

// Example usage
(async () => {
    // Login
    const loginResult = await login('johndoe', 'SecurePass123!');
    console.log('Login result:', loginResult);

    // Get profiles
    const profiles = await getProfiles();
    console.log('Profiles:', profiles);
})();
```

---

### 3. cURL Examples

#### Login
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

#### Make Authenticated Request
```bash
curl -X GET http://localhost:8000/api/profiles/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Refresh Token
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

#### Verify Token
```bash
curl -X POST http://localhost:8000/api/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

---

### 4. React Hook Implementation

```javascript
// useAuth.js
import { useState, useEffect, createContext, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [accessToken, setAccessToken] = useState(
        localStorage.getItem('access_token')
    );
    const [refreshToken, setRefreshToken] = useState(
        localStorage.getItem('refresh_token')
    );
    const [loading, setLoading] = useState(true);

    const api = axios.create({
        baseURL: 'http://localhost:8000'
    });

    // Request interceptor
    api.interceptors.request.use(
        config => {
            if (accessToken) {
                config.headers.Authorization = `Bearer ${accessToken}`;
            }
            return config;
        },
        error => Promise.reject(error)
    );

    // Response interceptor
    api.interceptors.response.use(
        response => response,
        async error => {
            const originalRequest = error.config;

            if (error.response.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true;

                try {
                    const response = await axios.post(
                        'http://localhost:8000/api/token/refresh/',
                        { refresh: refreshToken }
                    );

                    const newAccessToken = response.data.access;
                    const newRefreshToken = response.data.refresh;

                    setAccessToken(newAccessToken);
                    setRefreshToken(newRefreshToken);
                    localStorage.setItem('access_token', newAccessToken);
                    localStorage.setItem('refresh_token', newRefreshToken);

                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                    return api(originalRequest);
                } catch (refreshError) {
                    logout();
                    return Promise.reject(refreshError);
                }
            }

            return Promise.reject(error);
        }
    );

    const login = async (username, password) => {
        try {
            const response = await axios.post('http://localhost:8000/api/token/', {
                username,
                password
            });

            const { access, refresh } = response.data;

            setAccessToken(access);
            setRefreshToken(refresh);
            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);

            // Get user details
            const userResponse = await api.get('/api/users/me/');
            setUser(userResponse.data);

            return { success: true };
        } catch (error) {
            return { success: false, error: error.response.data };
        }
    };

    const logout = () => {
        setUser(null);
        setAccessToken(null);
        setRefreshToken(null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    };

    useEffect(() => {
        const initAuth = async () => {
            if (accessToken) {
                try {
                    const response = await api.get('/api/users/me/');
                    setUser(response.data);
                } catch (error) {
                    logout();
                }
            }
            setLoading(false);
        };

        initAuth();
    }, []);

    return (
        <AuthContext.Provider value={{ user, login, logout, api, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
```

**Usage in React Component:**

```javascript
import { useAuth } from './useAuth';

function ProfilesList() {
    const { api, user } = useAuth();
    const [profiles, setProfiles] = useState([]);

    useEffect(() => {
        const fetchProfiles = async () => {
            try {
                const response = await api.get('/api/profiles/');
                setProfiles(response.data.results);
            } catch (error) {
                console.error('Failed to fetch profiles:', error);
            }
        };

        if (user) {
            fetchProfiles();
        }
    }, [user]);

    return (
        <div>
            {profiles.map(profile => (
                <div key={profile.id}>{profile.name}</div>
            ))}
        </div>
    );
}
```

---

## Testing Authentication

### 1. Create Test User

```bash
cd backend
python manage.py createsuperuser
```

Enter:
- Username: `testuser`
- Email: `test@example.com`
- Password: `Test123!@#`

### 2. Test Login

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test123!@#"
  }'
```

**Expected Response:**
```json
{
    "access": "eyJ0eXAiOi...",
    "refresh": "eyJ0eXAiOi..."
}
```

### 3. Test Protected Endpoint

```bash
# Without token (should fail)
curl -X GET http://localhost:8000/api/profiles/

# With token (should succeed)
curl -X GET http://localhost:8000/api/profiles/ \
  -H "Authorization: Bearer eyJ0eXAiOi..."
```

### 4. Test Token Refresh

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOi..."
  }'
```

### 5. Test Token Verify

```bash
curl -X POST http://localhost:8000/api/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJ0eXAiOi..."
  }'
```

---

## Frontend Integration

### Setting Up Axios Interceptors

Create `src/api/axios.js`:

```javascript
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const refreshToken = localStorage.getItem('refresh_token');

            if (refreshToken) {
                try {
                    const response = await axios.post(
                        `${BASE_URL}/api/token/refresh/`,
                        { refresh: refreshToken }
                    );

                    const { access, refresh } = response.data;

                    localStorage.setItem('access_token', access);
                    localStorage.setItem('refresh_token', refresh);

                    originalRequest.headers.Authorization = `Bearer ${access}`;

                    return api(originalRequest);
                } catch (refreshError) {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    window.location.href = '/login';
                    return Promise.reject(refreshError);
                }
            }
        }

        return Promise.reject(error);
    }
);

export default api;
```

### Authentication Service

Create `src/services/authService.js`:

```javascript
import api from '../api/axios';

const authService = {
    login: async (username, password) => {
        try {
            const response = await api.post('/api/token/', {
                username,
                password,
            });

            const { access, refresh } = response.data;

            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);

            return { success: true, data: response.data };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || 'Login failed',
            };
        }
    },

    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    getCurrentUser: async () => {
        try {
            const response = await api.get('/api/users/me/');
            return { success: true, data: response.data };
        } catch (error) {
            return { success: false, error: error.response?.data };
        }
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('access_token');
    },
};

export default authService;
```

---

## Troubleshooting

### Common Issues

#### 1. "Token is invalid or expired"
**Cause:** Access token has expired (after 60 minutes)  
**Solution:** Use refresh token to get new access token

```javascript
const response = await axios.post('/api/token/refresh/', {
    refresh: refreshToken
});
```

#### 2. "No active account found with the given credentials"
**Cause:** Incorrect username/password or inactive account  
**Solution:** 
- Verify credentials
- Check if user account is active: `User.is_active = True`

#### 3. "Authentication credentials were not provided"
**Cause:** Missing Authorization header  
**Solution:** Add header to request

```javascript
headers: {
    'Authorization': `Bearer ${accessToken}`
}
```

#### 4. "Token is blacklisted"
**Cause:** Refresh token has been used and blacklisted  
**Solution:** User must login again to get new token pair

#### 5. CORS Error
**Cause:** Frontend domain not in `CORS_ALLOWED_ORIGINS`  
**Solution:** Add domain to settings.py

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://your-frontend-domain.com",
]
```

---

### Debugging Tips

#### 1. Decode JWT Token
Visit https://jwt.io/ and paste your token to see the payload

#### 2. Check Token Expiration
```python
import jwt
from datetime import datetime

token = "your_token_here"
decoded = jwt.decode(token, options={"verify_signature": False})
exp_timestamp = decoded['exp']
exp_datetime = datetime.fromtimestamp(exp_timestamp)
print(f"Token expires at: {exp_datetime}")
```

#### 3. Test with Django Shell
```python
python manage.py shell

from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

user = User.objects.get(username='testuser')
refresh = RefreshToken.for_user(user)

print(f"Access: {refresh.access_token}")
print(f"Refresh: {refresh}")
```

#### 4. Check Token Blacklist
```python
python manage.py shell

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

# View all outstanding tokens
OutstandingToken.objects.all()

# View blacklisted tokens
BlacklistedToken.objects.all()
```

---

## Security Best Practices

### 1. Token Storage
✅ **Do:** Store tokens in `httpOnly` cookies (server-side)  
✅ **Do:** Use `localStorage` for prototypes/development  
❌ **Don't:** Store tokens in regular cookies (XSS vulnerable)  
❌ **Don't:** Expose tokens in URLs

### 2. HTTPS in Production
✅ **Always use HTTPS** in production to prevent token interception

```python
# settings.py (Production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 3. Token Rotation
✅ **Enabled by default** in this project  
✅ Old refresh tokens are blacklisted after use

### 4. Short Token Lifetimes
✅ Access token: 60 minutes (current)  
✅ Refresh token: 7 days (current)

### 5. Environment Variables
```python
# Use environment variables for secrets
import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
```

### 6. Rate Limiting
Consider adding rate limiting for auth endpoints:

```bash
pip install django-ratelimit
```

---

## Summary

### ✅ What's Integrated

1. **djangorestframework-simplejwt 5.5.1** - Fully configured
2. **JWT Authentication Endpoints:**
   - Primary: `/api/token/`, `/api/token/refresh/`, `/api/token/verify/`
   - Alternative: `/api/auth/login/`, `/api/auth/refresh/`, `/api/auth/verify/`
3. **Custom Permission Classes:**
   - `IsOwnerOrReadOnly`
   - `IsAdminOrReadOnly`
   - `IsReportOwnerOrAdmin`
   - `IsProfileOwner`
   - `IsInterestParticipant`
   - `IsAdminUser`
   - `IsOwner`
4. **Token Configuration:**
   - 60-minute access token lifetime
   - 7-day refresh token lifetime
   - Automatic token rotation
   - Token blacklisting
5. **CORS Configuration** - Ready for React frontend

### 📋 Next Steps

1. **Test all endpoints** with Postman/Thunder Client
2. **Integrate frontend** with authentication service
3. **Add rate limiting** for security (optional)
4. **Set up HTTPS** for production deployment
5. **Configure environment variables** for secrets

---

**Last Updated:** October 14, 2025  
**Version:** 1.0  
**Status:** ✅ Production Ready
