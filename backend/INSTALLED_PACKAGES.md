# Installed Python Packages for Matrimonial Website

## Complete Package List

### Core Django Packages
1. **Django** (v4.2.25)
   - Purpose: Main web framework
   - Usage: Backend application framework, ORM, admin panel

2. **djangorestframework** (v3.16.1)
   - Purpose: REST API framework
   - Usage: Building RESTful APIs for React frontend

3. **django-cors-headers** (v4.9.0)
   - Purpose: Handle CORS (Cross-Origin Resource Sharing)
   - Usage: Allow React frontend (localhost:3000) to communicate with Django backend (localhost:8000)

### Authentication & Security
4. **djangorestframework-simplejwt** (v5.5.1)
   - Purpose: JSON Web Token (JWT) authentication
   - Usage: Secure token-based authentication for API endpoints
   - Includes: PyJWT (v2.10.1)

### Image Processing
5. **Pillow** (v11.3.0)
   - Purpose: Python Imaging Library
   - Usage: Handle profile pictures, photo uploads, image processing

### Data Processing & Excel Support
6. **pandas** (v2.3.3)
   - Purpose: Data analysis and manipulation
   - Usage: Export user data, generate reports, data analytics
   - Dependencies: numpy (v2.3.3), python-dateutil (v2.9.0.post0), pytz (v2025.2)

7. **openpyxl** (v3.1.5)
   - Purpose: Read/write Excel 2010 xlsx/xlsm files
   - Usage: Export user profiles to Excel, import bulk data
   - Dependencies: et-xmlfile (v2.0.0)

### PDF Generation
8. **reportlab** (v4.4.4)
   - Purpose: PDF generation library
   - Usage: Generate profile PDFs, reports, invoices
   - Dependencies: charset-normalizer (v3.4.3)

### Database Client
9. **mysqlclient** (v2.2.7)
   - Purpose: MySQL database adapter
   - Usage: Connect Django to MySQL database (production-ready)

## Installation Commands

### All Packages at Once
```bash
cd d:\Matrimonial_Site\backend
.\venv\Scripts\pip.exe install -r requirements.txt
```

### Individual Package Installation
```bash
# Core Django packages
.\venv\Scripts\pip.exe install Django djangorestframework django-cors-headers

# JWT Authentication
.\venv\Scripts\pip.exe install djangorestframework-simplejwt

# Image handling
.\venv\Scripts\pip.exe install Pillow

# Data processing
.\venv\Scripts\pip.exe install pandas openpyxl

# PDF generation
.\venv\Scripts\pip.exe install reportlab

# MySQL client
.\venv\Scripts\pip.exe install mysqlclient
```

## Package Usage in Matrimonial Website

### 1. User Authentication (SimpleJWT)
- Login/Logout with JWT tokens
- Secure API endpoints
- Token refresh mechanism
- User session management

### 2. Profile Pictures (Pillow)
- Upload user photos
- Resize and optimize images
- Generate thumbnails
- Image format conversion

### 3. Data Export/Import (Pandas + OpenPyXL)
- Export user profiles to Excel
- Import bulk user data
- Generate statistical reports
- Data analysis and insights

### 4. PDF Reports (ReportLab)
- Generate user profile PDFs
- Create matrimonial bio-data
- Export search results
- Print-ready documents

### 5. MySQL Database (mysqlclient)
- Production database support
- Better performance than SQLite
- Concurrent user handling
- Data integrity and reliability

## Configuration Updates

### Django Settings (settings.py)
```python
INSTALLED_APPS = [
    # ...
    'rest_framework_simplejwt',  # JWT authentication
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Media files for images
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### URL Configuration (urls.py)
```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
```

## API Endpoints Added

### JWT Authentication
- `POST /api/token/` - Obtain JWT token (login)
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity

## Next Steps

1. **Configure MySQL Database** (when ready for production)
2. **Add image fields** to UserProfile model
3. **Create Excel export views** for user data
4. **Implement PDF generation** for profiles
5. **Test JWT authentication** with frontend

## Verification

To verify all packages are installed:
```bash
.\venv\Scripts\pip.exe list
```

Expected output includes all packages listed above with their versions.
