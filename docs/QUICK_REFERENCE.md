# 🚀 Quick Reference - Installed Packages

## Package Summary
| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2.25 | Web Framework |
| djangorestframework | 3.16.1 | REST API |
| django-cors-headers | 4.9.0 | CORS Support |
| djangorestframework-simplejwt | 5.5.1 | JWT Authentication |
| Pillow | 11.3.0 | Image Processing |
| pandas | 2.3.3 | Data Analysis |
| openpyxl | 3.1.5 | Excel Files |
| reportlab | 4.4.4 | PDF Generation |
| mysqlclient | 2.2.7 | MySQL Database |

## Quick Commands

### Install All Packages
```bash
cd d:\Matrimonial_Site\backend
.\venv\Scripts\pip.exe install -r requirements.txt
```

### List Installed Packages
```bash
.\venv\Scripts\pip.exe list
```

### Upgrade a Package
```bash
.\venv\Scripts\pip.exe install --upgrade package-name
```

## JWT API Endpoints
- **Login**: `POST /api/token/`
- **Refresh**: `POST /api/token/refresh/`
- **Verify**: `POST /api/token/verify/`

## Usage Examples

### JWT Login Request
```json
POST /api/token/
{
  "username": "user123",
  "password": "password123"
}
```

### JWT Response
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using JWT Token
```javascript
headers: {
  'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
}
```

## File Locations
- **Requirements**: `backend/requirements.txt`
- **Settings**: `backend/backend/settings.py`
- **URLs**: `backend/backend/urls.py`
- **Installed List**: `backend/installed_packages.txt`

## Status: ✅ ALL INSTALLED & CONFIGURED
