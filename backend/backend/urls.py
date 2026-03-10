"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ============================================
    # Admin Site
    # ============================================
    path('admin/', admin.site.urls),
    
    # ============================================
    # API Routes
    # ============================================
    # All users app routes are prefixed with /api/
    # This includes:
    # - Authentication (login, refresh, verify)
    # - User management (register, list, update, etc.)
    # - Profiles (/api/profiles/)
    # - Interests (/api/interests/)
    # - Reports (/api/reports/)
    # - OTP (/api/otp/)
    # - Exports (/api/export/profiles/pdf/, /api/export/profiles/excel/)
    path('api/', include('users.urls', namespace='users')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

"""
Available API Endpoints:

BASE URL: http://localhost:8000

AUTHENTICATION (Primary):
    POST   /api/token/                      - Login and get JWT tokens
    POST   /api/token/refresh/              - Refresh access token
    POST   /api/token/verify/               - Verify token validity

AUTHENTICATION (Alternative - same functionality):
    POST   /api/auth/login/                 - Login and get JWT tokens
    POST   /api/auth/refresh/               - Refresh access token
    POST   /api/auth/verify/                - Verify token validity

USER MANAGEMENT:
    POST   /api/register/                   - Register new user
    GET    /api/users/                      - List all users
    GET    /api/users/me/                   - Get current user
    PUT    /api/users/me/update/            - Update current user
    PUT    /api/users/change-password/      - Change password

PROFILES:
    GET    /api/profiles/                   - List all profiles (with filters)
    POST   /api/profiles/                   - Create profile
    GET    /api/profiles/{id}/              - Get profile by ID
    PUT    /api/profiles/{id}/              - Update profile
    DELETE /api/profiles/{id}/              - Delete profile
    GET    /api/profiles/me/                - Get my profile
    POST   /api/profiles/create-mine/       - Create my profile

INTERESTS:
    GET    /api/interests/                  - List interests (sent/received)
    POST   /api/interests/                  - Send interest
    GET    /api/interests/{id}/             - Get interest by ID
    PUT    /api/interests/{id}/             - Update interest
    DELETE /api/interests/{id}/             - Delete interest
    GET    /api/interests/sent/             - Get sent interests
    GET    /api/interests/received/         - Get received interests
    GET    /api/interests/pending/          - Get pending interests
    POST   /api/interests/{id}/respond/     - Accept/reject interest
    POST   /api/interests/{id}/cancel/      - Cancel interest

REPORTS:
    GET    /api/reports/                    - List reports
    POST   /api/reports/                    - Create report
    GET    /api/reports/{id}/               - Get report by ID
    GET    /api/reports/my-reports/         - Get my reports
    GET    /api/reports/pending/            - Get pending reports (Admin)
    POST   /api/reports/{id}/review/        - Review report (Admin)
    GET    /api/reports/statistics/         - Get statistics (Admin)

OTP VERIFICATION:
    GET    /api/otp/                        - List OTP history
    POST   /api/otp/generate/               - Generate OTP
    POST   /api/otp/verify/                 - Verify OTP
    POST   /api/otp/resend/                 - Resend OTP

EXPORTS (Admin Only):
    POST   /api/export/profiles/pdf/        - Export profiles as PDF
    POST   /api/export/profiles/excel/      - Export profiles as Excel
    POST   /api/export/{type}/{format}/     - Generic export endpoint
    GET    /api/export-logs/                - List export logs

ADMIN:
    GET    /admin/                          - Django admin interface

Usage Examples:
    
    # Login (Primary endpoint)
    curl -X POST http://localhost:8000/api/token/ \\
         -H "Content-Type: application/json" \\
         -d '{"username":"john","password":"pass"}'
    
    # Refresh Token
    curl -X POST http://localhost:8000/api/token/refresh/ \\
         -H "Content-Type: application/json" \\
         -d '{"refresh":"<refresh_token>"}'
    
    # List Profiles (with authentication)
    curl -X GET http://localhost:8000/api/profiles/ \\
         -H "Authorization: Bearer <access_token>"
    
    # Send Interest
    curl -X POST http://localhost:8000/api/interests/ \\
         -H "Authorization: Bearer <access_token>" \\
         -H "Content-Type: application/json" \\
         -d '{"receiver":5,"message":"Hello!"}'
    
    # Export Profiles as PDF (Admin)
    curl -X POST http://localhost:8000/api/export/profiles/pdf/ \\
         -H "Authorization: Bearer <admin_token>" \\
         -H "Content-Type: application/json" \\
         -d '{"date_from":"2025-01-01","date_to":"2025-10-14"}'
"""
