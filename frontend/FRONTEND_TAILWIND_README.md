# Matrimonial Site - React Frontend with TailwindCSS

## 🎨 Features

### Completed Pages:
1. **Login Page** - Beautiful gradient design with form validation
2. **Register Page** - Multi-section registration form with comprehensive fields
3. **OTP Verification** - 6-digit OTP input with auto-focus and resend functionality
4. **Home Page** - Profile browsing with advanced filters (gender, age, location)
5. **Profile Details** - Detailed profile view with Send Interest & Report Profile
6. **Edit Profile** - Comprehensive profile editing with image upload
7. **Report Profile** - Report inappropriate profiles with reason selection
8. **Admin Dashboard** - Manage users, reports, and export data (PDF/Excel)

### Design Highlights:
- 🎨 **TailwindCSS** styling throughout
- 📱 **Fully Responsive** design
- 🌈 **Gradient Accents** (red to pink theme)
- ✨ **Smooth Animations** (fadeIn, hover effects, loading spinners)
- 🎯 **Intuitive UI/UX** with icons and visual feedback
- 🔔 **Toast Notifications** for user actions
- 🎭 **Professional Cards** with hover effects

## 📦 Installation

### Prerequisites
- Node.js 14+ and npm
- Django backend running on `http://localhost:8000`

### Step 1: Install Dependencies

```bash
cd frontend
npm install react-router-dom axios tailwindcss postcss autoprefixer
```

### Step 2: Initialize Tailwind (Already Done)

The following files have been created:
- `tailwind.config.js` - Tailwind configuration with custom colors
- `postcss.config.js` - PostCSS configuration
- `src/index.css` - Tailwind directives and custom animations

### Step 3: Update package.json

Your `package.json` should include:

```json
{
  "dependencies": {
    "axios": "^1.6.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0"
  },
  "devDependencies": {
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.31",
    "autoprefixer": "^10.4.16"
  }
}
```

### Step 4: Start Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

## 🗂️ Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── api.js                 # Axios instance + API functions
│   ├── components/
│   │   ├── Navbar.jsx             # Navigation with user menu
│   │   └── ProtectedRoute.jsx     # Route protection wrapper
│   ├── pages/
│   │   ├── LoginPage.jsx          # Login with JWT authentication
│   │   ├── RegisterPage.jsx       # Registration form
│   │   ├── OTPVerification.jsx    # OTP verification
│   │   ├── HomePage.jsx           # Browse profiles with filters
│   │   ├── ProfileDetails.jsx     # Detailed profile view
│   │   ├── EditProfile.jsx        # Edit profile with image upload
│   │   ├── ReportProfile.jsx      # Report inappropriate profiles
│   │   └── AdminDashboard.jsx     # Admin panel (users, reports, exports)
│   ├── App.jsx                    # Main app with routing
│   ├── index.css                  # Tailwind + custom styles
│   └── index.js                   # Entry point
├── public/
├── tailwind.config.js             # Tailwind configuration
├── postcss.config.js              # PostCSS configuration
├── package.json
└── .env                           # Environment variables

```

## 🎯 API Integration

All pages consume Django REST APIs via Axios:

### Authentication APIs
- `POST /api/token/` - Login (get JWT tokens)
- `POST /api/register/` - User registration
- `POST /api/otp/verify/` - OTP verification
- `POST /api/token/refresh/` - Refresh JWT token

### Profile APIs
- `GET /api/profiles/` - Get all profiles (with filters)
- `GET /api/profiles/{id}/` - Get profile by ID
- `GET /api/users/me/` - Get current user profile
- `PATCH /api/users/me/` - Update profile (with FormData for images)

### Interest APIs
- `POST /api/interests/` - Send interest to a profile
- `GET /api/interests/sent/` - Get sent interests
- `GET /api/interests/received/` - Get received interests

### Report APIs
- `POST /api/reports/` - Report a profile
- `GET /api/reports/` - Get all reports (admin)
- `POST /api/reports/{id}/review/` - Review report (admin)

### Admin APIs
- `GET /api/users/` - Get all users (admin)
- `GET /api/profile-exports/pdf/` - Export profiles to PDF
- `GET /api/profile-exports/excel/` - Export profiles to Excel
- `GET /api/export-logs/` - Get export history

## 🔐 Authentication Flow

1. User enters username/password on Login page
2. JWT tokens (access + refresh) stored in `localStorage`
3. Axios interceptor automatically adds `Authorization: Bearer <token>` to all requests
4. On 401 error, refresh token is used to get new access token
5. If refresh fails, user is redirected to login

## 🎨 TailwindCSS Classes Used

### Layout
- `min-h-screen` - Full viewport height
- `max-w-7xl mx-auto` - Centered container
- `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6` - Responsive grid

### Colors
- `bg-gradient-to-r from-red-600 to-pink-600` - Gradient backgrounds
- `text-red-600` - Primary text color
- `hover:bg-red-50` - Hover states

### Effects
- `rounded-xl` - Rounded corners
- `shadow-md` - Drop shadows
- `transition duration-150` - Smooth transitions
- `animate-fadeIn` - Custom fade-in animation

### Forms
- `focus:ring-2 focus:ring-red-500` - Focus states
- `border border-gray-300` - Input borders
- `disabled:opacity-50` - Disabled states

## 📱 Responsive Design

All pages are fully responsive:
- Mobile: Single column layout
- Tablet: 2 columns
- Desktop: 3 columns for profile grids

Hamburger menu on mobile devices with slide-down navigation.

## ✨ Key Features by Page

### Login Page
- Gradient background
- Username/password fields with icons
- Remember me checkbox
- Loading spinner on submit
- Error handling with styled alerts
- Link to registration

### Register Page
- Multi-section form (Personal, Contact, Credentials)
- Field validation (age, mobile, passwords match)
- Gender and date picker
- Password confirmation
- Terms acceptance checkbox

### OTP Verification
- 6-digit OTP input with auto-focus
- Resend OTP with countdown timer
- Success message
- Back to registration button

### Home Page
- Profile cards with images
- Search filters (gender, age range, location)
- "Send Interest" button on each card
- "View Profile" link
- Empty state for no results
- Loading spinner

### Profile Details
- Large profile image
- Detailed information sections
- "Send Interest" and "Report Profile" buttons
- "Edit Profile" for own profile
- Sticky sidebar on desktop

### Edit Profile
- Profile picture upload with preview
- All user fields editable
- Organized sections (Personal, Professional, Location, Family)
- Save/Cancel buttons
- Success notification

### Report Profile
- Reason dropdown (Fake Profile, Harassment, etc.)
- Detailed description textarea
- Important notice about false reports
- Cancel/Submit buttons

### Admin Dashboard
- Tabbed interface (Users, Reports, Exports)
- Stats cards (Total Users, Pending Reports, Total Exports)
- Users table with View/Delete actions
- Reports cards with Resolve/Dismiss actions
- Export buttons (PDF/Excel)
- Export history table

## 🚀 Next Steps

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Django Backend**:
   ```bash
   cd backend
   python manage.py runserver
   ```

3. **Start React Frontend**:
   ```bash
   cd frontend
   npm start
   ```

4. **Access the App**:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

## 🎯 Environment Variables

Create a `.env` file in the `frontend` directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

This is already configured in your `.env` file.

## 🐛 Troubleshooting

### Tailwind styles not working
1. Make sure `tailwind.config.js` and `postcss.config.js` exist
2. Restart the dev server: `npm start`
3. Clear cache: Delete `node_modules/.cache`

### API errors
1. Check Django backend is running on port 8000
2. Check CORS settings in Django
3. Open browser console for detailed errors

### Authentication issues
1. Check JWT tokens in localStorage (F12 → Application → Local Storage)
2. Check Axios interceptor is adding Authorization header
3. Verify Django `SIMPLE_JWT` settings

## 📝 Notes

- All forms have client-side validation
- Images are handled with FormData for proper multipart uploads
- JWT tokens automatically refresh on 401 errors
- All API calls use Axios interceptors for token injection
- Loading states prevent multiple submissions
- Error messages are user-friendly and styled

## 🎉 Complete Feature List

✅ Beautiful TailwindCSS design
✅ JWT authentication with automatic token refresh
✅ Profile browsing with filters
✅ Profile details with all information
✅ Send interest to profiles
✅ Report inappropriate profiles
✅ Edit own profile with image upload
✅ Admin dashboard for management
✅ Export data to PDF/Excel
✅ Responsive design for all devices
✅ Loading spinners and animations
✅ Toast notifications
✅ Form validation
✅ Protected routes
✅ 404 page

Your matrimonial site frontend is now complete with professional, production-ready React pages! 🚀
