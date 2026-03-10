# PerfectPair - Matrimonial Website

A comprehensive full-stack matrimonial web application built with Django REST Framework backend and React frontend.

## 🌟 Project Overview

PerfectPair is a modern matrimonial platform that helps users find their perfect life partner through an intuitive interface with advanced matching features, interest management, and comprehensive admin controls.

## 📁 Project Structure

```
Matrimonial_Site/
├── backend/                    # Django REST Framework Backend
│   ├── backend/               # Main Django project configuration
│   │   ├── settings.py       # Project settings
│   │   ├── urls.py           # Root URL configuration
│   │   └── wsgi.py           # WSGI configuration
│   ├── users/                 # Main users app
│   │   ├── models.py         # Database models (User, Profile, Interest, etc.)
│   │   ├── serializers.py    # DRF serializers
│   │   ├── views.py          # API views and ViewSets
│   │   ├── urls.py           # App URL patterns
│   │   └── admin.py          # Django admin configuration
│   ├── media/                 # User uploaded files
│   │   ├── profile_photos/   # Profile pictures
│   │   └── documents/        # Document uploads
│   ├── db.sqlite3            # SQLite database
│   ├── manage.py             # Django management script
│   └── requirements.txt      # Python dependencies
└── frontend/                  # React Frontend
    ├── public/               # Static public files
    ├── src/
    │   ├── pages/           # Page components
    │   │   ├── LoginPage.jsx
    │   │   ├── RegisterPage.jsx
    │   │   ├── HomePage.jsx
    │   │   ├── ProfilePage.jsx
    │   │   ├── ProfileDetails.jsx
    │   │   ├── Notifications.jsx
    │   │   ├── Favorites.jsx
    │   │   ├── Feedback.jsx
    │   │   ├── AdminDashboard.jsx
    │   │   └── ForgotPasswordPage.jsx
    │   ├── components/      # Reusable components
    │   │   └── Navbar.jsx
    │   ├── api/             # API integration
    │   │   └── api.js
    │   ├── App.jsx          # Main App component
    │   └── index.js         # React entry point
    ├── package.json         # Node dependencies
    └── tailwind.config.js   # TailwindCSS configuration
```

## ✨ Features

### 👤 User Features
- **Authentication System**
  - User registration with email validation
  - Secure JWT-based login/logout
  - Password change functionality
  - Admin-approved password reset system

- **Profile Management**
  - Detailed profile creation and editing
  - Profile photo upload
  - Personal information (age, height, education, occupation, etc.)
  - Location and contact details
  - Bio and preferences

- **Profile Discovery**
  - Advanced search with 10+ filters
  - Browse profiles by gender, age, location, occupation, education
  - Height, marital status, and religion filters
  - Pagination support

- **Interest Management**
  - Send interest to profiles with optional message
  - View sent interests
  - Receive and manage interest requests
  - Accept or reject interests
  - Cancel sent interests
  - Interest status tracking

- **Favorites System**
  - Add/remove profiles to favorites
  - View all favorited profiles
  - Quick access to saved profiles

- **Notifications**
  - Real-time interest request notifications
  - Interest acceptance/rejection alerts
  - Status updates

- **Reporting System**
  - Report inappropriate profiles
  - Multiple report reasons (spam, fake, inappropriate, harassment, other)
  - Admin review workflow

- **Feedback System**
  - Submit feedback to admin
  - Multiple categories (Bug Report, Feature Request, General Feedback, Complaint)
  - Admin response system
  - Feedback status tracking

### 🔐 Admin Features
- **Comprehensive Admin Dashboard**
  - User statistics and analytics
  - Total users, profiles, interests, reports overview
  - Recent activity monitoring

- **User Management**
  - View all registered users
  - Block/unblock users with reason
  - View user profiles and activity
  - Delete users

- **Report Management**
  - Review reported profiles
  - Approve or reject reports
  - Take action on reported users
  - Report statistics

- **Password Reset Management**
  - Review password reset requests
  - Approve/reject requests
  - Auto-generate secure passwords
  - Send new passwords to users

- **Feedback Management**
  - View all user feedback
  - Respond to feedback
  - Update feedback status (Pending, In Progress, Resolved, Closed)
  - Filter by category and status

- **Data Export**
  - Export profiles to PDF/Excel
  - Export users data
  - Export reports and interests
  - Formatted export with comprehensive data

### 🎨 UI/UX Features
- **Modern Design**
  - Beautiful gradient color schemes (pink/red theme)
  - Responsive layout (mobile, tablet, desktop)
  - TailwindCSS styling
  - Smooth animations and transitions

- **User Experience**
  - Intuitive navigation
  - Loading states and spinners
  - Success/error notifications
  - Empty state designs
  - Confirmation dialogs for critical actions

### 🔒 Security Features
- JWT token authentication
- Automatic token refresh
- Password hashing (PBKDF2)
- Permission-based access control
- User blocking system
- CORS protection
- Input validation (frontend + backend)
- Protected routes

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```cmd
     venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

   ✅ Backend will be available at `http://localhost:8000`
   
   🔧 Admin panel: `http://localhost:8000/admin`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   ✅ Frontend will be available at `http://localhost:3000`

   The browser should automatically open. If not, navigate to the URL manually.

## 📡 API Endpoints

### Authentication Endpoints

**JWT Authentication:**
- `POST /api/token/` - Login and get JWT tokens
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity

**Alternative Auth Routes:**
- `POST /api/auth/login/` - Login (alternative)
- `POST /api/auth/refresh/` - Refresh token (alternative)
- `POST /api/auth/verify/` - Verify token (alternative)

### User Management Endpoints

- `POST /api/register/` - Register new user
- `GET /api/users/` - List all users (Admin only)
- `GET /api/users/me/` - Get current user
- `PUT /api/users/me/update/` - Update current user
- `PUT /api/users/change-password/` - Change password
- `GET /api/users/<id>/` - Get user by ID
- `POST /api/users/<user_id>/block/` - Block user (Admin only)

### Profile Endpoints

- `GET /api/profiles/` - List all profiles (with filters)
- `POST /api/profiles/` - Create profile
- `GET /api/profiles/<id>/` - Get profile by ID
- `PUT /api/profiles/<id>/` - Update profile
- `DELETE /api/profiles/<id>/` - Delete profile
- `GET /api/profiles/search/` - Search profiles with filters

**Available Search Filters:**
- `gender` - Filter by gender (Male/Female)
- `min_age`, `max_age` - Age range
- `location` - Location search
- `occupation` - Occupation filter
- `education` - Education level
- `min_height`, `max_height` - Height range (in cm)
- `marital_status` - Marital status filter
- `religion` - Religion filter

### Interest Endpoints

- `GET /api/interests/` - List all interests
- `POST /api/interests/` - Send interest
- `GET /api/interests/<id>/` - Get interest details
- `DELETE /api/interests/<id>/` - Delete interest
- `GET /api/interests/sent/` - Get sent interests
- `GET /api/interests/received/` - Get received interests
- `GET /api/interests/pending/` - Get pending interests
- `POST /api/interests/<id>/respond/` - Respond to interest (accept/reject)
- `POST /api/interests/<id>/cancel/` - Cancel sent interest
- `GET /api/interests/check/<profile_id>/` - Check interest status

### Favorites Endpoints

- `GET /api/favorites/` - List all favorites
- `POST /api/favorites/toggle/<profile_id>/` - Add/remove favorite
- `GET /api/favorites/check/<profile_id>/` - Check if favorited
- `GET /api/favorites/my-favorites/` - Get my favorites

### Report Endpoints

- `GET /api/reports/` - List all reports (Admin only)
- `POST /api/reports/` - Report a profile
- `GET /api/reports/<id>/` - Get report details
- `GET /api/reports/my-reports/` - Get my reports
- `GET /api/reports/pending/` - Get pending reports (Admin only)
- `POST /api/reports/<id>/review/` - Review report (Admin only)
- `GET /api/reports/statistics/` - Get report statistics (Admin only)

### Feedback Endpoints

- `GET /api/feedback/` - List all feedback (Admin only)
- `POST /api/feedback/` - Submit feedback
- `GET /api/feedback/<id>/` - Get feedback details
- `PUT /api/feedback/<id>/` - Update feedback
- `DELETE /api/feedback/<id>/` - Delete feedback
- `POST /api/feedback/<id>/respond/` - Respond to feedback (Admin only)
- `POST /api/feedback/<id>/update_status/` - Update feedback status (Admin only)

### Password Reset Endpoints

- `POST /api/password-reset-requests/` - Submit password reset request
- `GET /api/password-reset-requests/` - List all requests (Admin only)
- `GET /api/password-reset-requests/<id>/` - Get request details (Admin only)
- `POST /api/password-reset-requests/<id>/approve/` - Approve request (Admin only)
- `POST /api/password-reset-requests/<id>/reject/` - Reject request (Admin only)

### Export Endpoints (Admin Only)

- `POST /api/export/profiles/pdf/` - Export profiles as PDF
- `POST /api/export/profiles/excel/` - Export profiles as Excel
- `POST /api/export/users/pdf/` - Export users as PDF
- `POST /api/export/users/excel/` - Export users as Excel
- `POST /api/export/reports/pdf/` - Export reports as PDF
- `POST /api/export/interests/pdf/` - Export interests as PDF

### Admin Panel

Access the Django admin panel at `http://localhost:8000/admin` with your superuser credentials.

## 🛠️ Technologies Used

### Backend
- **Python 3.8+**
- **Django 4.2.25** - Web framework
- **Django REST Framework 3.16.1** - API framework
- **djangorestframework-simplejwt 5.3.0** - JWT authentication
- **django-cors-headers 4.3.1** - CORS handling
- **Pillow 11.0.0** - Image processing
- **reportlab 4.2.5** - PDF generation
- **pandas 2.2.3** - Excel export
- **openpyxl 3.1.5** - Excel file handling
- **SQLite** - Database (default for development)

### Frontend
- **React 18.2.0** - UI library
- **React Router 6.20.0** - Client-side routing
- **Axios 1.6.0** - HTTP client
- **TailwindCSS 3.4.18** - Utility-first CSS framework
- **PostCSS 8.4.35** - CSS processing

## 📝 Database Models

### User Model (Extended Django User)
- Username, email, password
- First name, last name
- Admin status
- Active status
- Date joined
- Blocking fields (blocked status, reason, timestamp, blocked_by)

### Profile Model
- User (OneToOne with User)
- Personal details (name, age, date of birth, gender, height)
- Contact info (mobile number, location)
- Professional info (occupation, education)
- Bio and preferences
- Profile picture
- Marital status, religion
- Timestamps (created_at, updated_at)

### Interest Model
- Sender (ForeignKey to User)
- Receiver (ForeignKey to User)
- Status (pending, accepted, rejected, cancelled)
- Message (optional)
- Timestamps (created_at, updated_at)

### Favorite Model
- User (ForeignKey to User)
- Profile (ForeignKey to Profile)
- Timestamp (created_at)

### Report Model
- Reporter (ForeignKey to User)
- Reported user (ForeignKey to User)
- Reason (spam, fake, inappropriate, harassment, other)
- Description
- Status (pending, reviewed, action_taken, dismissed)
- Admin notes
- Timestamps (created_at, updated_at)

### Feedback Model
- User (ForeignKey to User)
- Category (bug_report, feature_request, general, complaint)
- Subject
- Message
- Status (pending, in_progress, resolved, closed)
- Admin response
- Timestamps (created_at, updated_at)

### PasswordResetRequest Model
- User (ForeignKey to User)
- Email
- Reason
- Status (pending, approved, rejected)
- New password (encrypted)
- Timestamps (created_at, updated_at)

### OTPVerification Model
- User (ForeignKey to User)
- OTP code
- Expiry timestamp
- Verified status
- Timestamp (created_at)

### ExportLog Model
- User (ForeignKey to User)
- Export type (profiles, users, reports, interests)
- File type (pdf, excel)
- Record count
- File name
- Timestamp (created_at)

## 🎯 Key Features Implementation

### JWT Authentication Flow
1. User logs in with credentials
2. Backend validates and returns access + refresh tokens
3. Frontend stores tokens in localStorage
4. Access token included in API request headers
5. Automatic token refresh on 401 responses
6. Logout clears tokens

### Interest Management Flow
1. User A sends interest to User B (with optional message)
2. User B receives notification
3. User B can accept or reject
4. User A gets status update
5. Both users can view interest history

### Admin Password Reset Flow
1. User submits password reset request
2. Admin reviews request in dashboard
3. Admin approves and auto-generates secure password
4. New password sent to user (simulated)
5. User logs in and changes password

### Report System Flow
1. User reports a profile with reason
2. Admin views report in dashboard
3. Admin reviews and can take action
4. Options: Approve (block user) or Dismiss
5. Reporting user notified of outcome

## 🔧 Configuration

### Backend Configuration (settings.py)

**CORS Settings:**
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ALLOW_CREDENTIALS = True
```

**JWT Settings:**
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

**Media Files:**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Frontend Configuration (api.js)

**Base URL:**
```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' }
});
```

**Token Management:**
- Automatic token injection in requests
- Automatic token refresh on 401
- Token stored in localStorage

## 📊 Test Credentials

### Admin Account
```
Username: adminuser
Password: admin123
Email: admin@example.com
```

### Regular Users
**User 1:**
```
Username: gautham
Password: password123
Email: gautham@example.com
```

**User 2:**
```
Username: sakshi_chauhan
Password: password123
Email: sakshi@example.com
```

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000
# Kill the process
Stop-Process -Id <PID> -Force
```

**Database locked error:**
```bash
# Delete database and recreate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Port 3000 already in use:**
```powershell
# Find and kill process
$p = (Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue).OwningProcess
Stop-Process -Id $p -Force
```

**Module not found:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
# Clear cache
npm cache clean --force
npm install
```

## 🚀 Deployment

### Backend Deployment (Production)

1. **Update settings.py:**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use PostgreSQL instead of SQLite
   - Set secure `SECRET_KEY`
   - Configure static/media file serving

2. **Install production server:**
   ```bash
   pip install gunicorn
   gunicorn backend.wsgi:application
   ```

3. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

### Frontend Deployment

1. **Build production bundle:**
   ```bash
   npm run build
   ```

2. **Deploy build folder** to hosting service (Netlify, Vercel, etc.)

3. **Update API base URL** in `api.js` to production backend URL

## 📚 Documentation

Additional documentation files in the project:
- `PROJECT_REVIEW_CHECKLIST.md` - Complete feature checklist
- `FINAL_REVIEW_SUMMARY.md` - Project completion summary
- `DEMO_GUIDE.md` - Step-by-step demo walkthrough
- `backend/test_api.py` - API testing script

## 🤝 Contributing

This is an educational project. Feel free to fork and modify for your learning purposes.

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

Created as part of a full-stack development learning project.

---

**Happy Coding! 💝**
