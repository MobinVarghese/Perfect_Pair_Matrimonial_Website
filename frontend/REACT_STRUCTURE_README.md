# React Frontend - Matrimonial Site

## 📁 Project Structure

```
src/
├── api/
│   └── api.js                      # API service with axios interceptors
├── components/
│   ├── Navbar.jsx                  # Navigation bar component
│   ├── ProfileCard.jsx             # Profile card component
│   └── ProtectedRoute.jsx          # Route protection wrapper
├── pages/
│   ├── LoginPage.jsx               # User login
│   ├── RegisterPage.jsx            # User registration
│   ├── OTPVerification.jsx         # OTP verification
│   ├── HomePage.jsx                # Browse profiles with search
│   ├── ProfileDetails.jsx          # View detailed profile
│   ├── EditProfile.jsx             # Edit user profile
│   ├── AdminDashboard.jsx          # Admin panel
│   └── ReportProfile.jsx           # Report inappropriate profiles
├── App.jsx                         # Main app with routing
└── App.css                         # Global styles
```

---

## 🚀 Features Implemented

### 🔐 Authentication
- **JWT-based authentication** with token refresh
- Login, Register, and OTP Verification
- Protected routes for authenticated users
- Admin-only routes

### 👤 User Features
- Browse and search profiles
- View detailed profile information
- Edit own profile with image upload
- Send interests to other profiles
- Report inappropriate profiles

### 👨‍💼 Admin Features
- View all users
- Manage reports (approve/reject)
- Export profiles to PDF/Excel
- View export history

### 🎨 Components
- **Navbar**: Responsive navigation with user menu
- **ProfileCard**: Reusable profile display card
- **ProtectedRoute**: Authentication wrapper for routes

---

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

**Required packages:**
```bash
npm install react-router-dom axios
```

### 2. Configure Environment

Create `.env` file in `frontend/` directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

### 3. Start Development Server

```bash
npm start
```

The app will run on `http://localhost:3000`

---

## 📡 API Integration

### API Service (`api/api.js`)

Centralized API calls with:
- **Axios instance** with base URL
- **Request interceptor** - Adds JWT token to requests
- **Response interceptor** - Handles token refresh on 401 errors
- **Utility functions** for all backend endpoints

### Available API Functions

#### Authentication
```javascript
import { login, register, logout, verifyToken } from './api/api';

// Login
await login({ username: 'user', password: 'pass' });

// Register
await register(userData);

// Logout
logout();
```

#### Profiles
```javascript
import { getProfiles, getProfileById, searchProfiles } from './api/api';

// Get all profiles
const profiles = await getProfiles();

// Search profiles
const results = await searchProfiles({ gender: 'female', min_age: 25 });

// Get specific profile
const profile = await getProfileById(123);
```

#### Interests
```javascript
import { sendInterest, getSentInterests, getReceivedInterests } from './api/api';

// Send interest
await sendInterest(userId, 'I am interested!');

// Get sent interests
const sent = await getSentInterests();
```

#### Admin
```javascript
import { getAllUsers, exportProfilesPDF, exportProfilesExcel } from './api/api';

// Get all users (admin only)
const users = await getAllUsers();

// Export to PDF (admin only)
await exportProfilesPDF({ gender: 'female' });
```

---

## 🎨 Styling Guide

### CSS Organization

Each page/component has its own CSS file:
- `AuthPages.css` - Login, Register, OTP
- `HomePage.css` - Home page styles
- `ProfileDetails.css` - Profile detail page
- `EditProfile.css` - Edit profile form
- `AdminDashboard.css` - Admin panel
- `Navbar.css` - Navigation bar
- `ProfileCard.css` - Profile card component

### Global Styles (`App.css`)

Create `App.css` with common styles:

```css
/* Global Variables */
:root {
  --primary-color: #3498db;
  --secondary-color: #e91e63;
  --success-color: #27ae60;
  --danger-color: #e74c3c;
  --warning-color: #f39c12;
  --dark-color: #2c3e50;
  --light-color: #ecf0f1;
  --border-radius: 8px;
  --box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: var(--dark-color);
  background-color: #f5f5f5;
}

/* Container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Buttons */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: var(--secondary-color);
  color: white;
}

.btn-success {
  background-color: var(--success-color);
  color: white;
}

.btn-danger {
  background-color: var(--danger-color);
  color: white;
}

/* Alerts */
.alert {
  padding: 15px;
  border-radius: var(--border-radius);
  margin-bottom: 20px;
}

.alert-error {
  background-color: #fadbd8;
  color: #c0392b;
  border: 1px solid #e74c3c;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #27ae60;
}

/* Loading Spinner */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

---

## 🔒 Authentication Flow

### 1. Registration
```
RegisterPage → API (register) → OTPVerification → LoginPage
```

### 2. Login
```
LoginPage → API (login) → Store tokens → Redirect to HomePage
```

### 3. Token Refresh
```
Request → 401 Error → Interceptor → Refresh token → Retry request
```

### 4. Protected Routes
```
Route → ProtectedRoute wrapper → Check auth → Allow/Deny access
```

---

## 📱 Responsive Design

All components are mobile-responsive:
- **Navbar**: Hamburger menu on mobile
- **ProfileCard**: Grid layout adjusts for screen size
- **Forms**: Stack vertically on small screens
- **Tables**: Horizontal scroll on mobile

---

## 🧪 Testing

### Manual Testing Checklist

#### Authentication
- [ ] Register new user
- [ ] Verify OTP
- [ ] Login with credentials
- [ ] Logout
- [ ] Access protected routes without login (should redirect)

#### Profile Features
- [ ] Browse profiles on home page
- [ ] Search profiles with filters
- [ ] View profile details
- [ ] Send interest
- [ ] Edit own profile
- [ ] Upload profile picture
- [ ] Report a profile

#### Admin Features
- [ ] Access admin dashboard (admin user only)
- [ ] View all users
- [ ] View reports
- [ ] Review reports (approve/reject)
- [ ] Export profiles to PDF
- [ ] Export profiles to Excel
- [ ] View export history

---

## 🔧 Configuration

### API Base URL

Update in `.env`:
```env
REACT_APP_API_URL=http://localhost:8000/api
```

For production:
```env
REACT_APP_API_URL=https://your-domain.com/api
```

### Token Storage

Tokens are stored in `localStorage`:
- `access_token` - JWT access token
- `refresh_token` - JWT refresh token

To clear tokens:
```javascript
localStorage.removeItem('access_token');
localStorage.removeItem('refresh_token');
```

---

## 🐛 Troubleshooting

### Issue: CORS Errors

**Solution:** Configure Django backend CORS settings:

```python
# backend/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### Issue: 401 Unauthorized

**Solutions:**
1. Check if token is expired
2. Try logging in again
3. Verify API URL in `.env`

### Issue: Token Refresh Loop

**Solution:** Check refresh token validity and backend `/api/token/refresh/` endpoint

### Issue: Images Not Loading

**Solutions:**
1. Verify `MEDIA_URL` in Django settings
2. Check CORS headers for media files
3. Use absolute URLs for images

---

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized production build in `build/` folder.

### Serve Build

```bash
npm install -g serve
serve -s build -p 3000
```

### Deploy to Netlify/Vercel

1. Connect your Git repository
2. Set build command: `npm run build`
3. Set publish directory: `build`
4. Add environment variable: `REACT_APP_API_URL`

---

## 📚 Additional Resources

### React Router Documentation
https://reactrouter.com/

### Axios Documentation
https://axios-http.com/

### React Best Practices
- Use functional components with hooks
- Keep components small and focused
- Use PropTypes for type checking
- Implement error boundaries
- Lazy load routes for better performance

---

## 🔐 Security Best Practices

1. **Never commit `.env` file**
   ```bash
   # Add to .gitignore
   .env
   .env.local
   ```

2. **Validate user input** on both frontend and backend

3. **Sanitize user-generated content** before display

4. **Use HTTPS** in production

5. **Implement CSRF protection** for sensitive operations

6. **Rate limit** API requests

---

## 📝 Next Steps

### Suggested Enhancements

1. **Add More Features:**
   - Chat/messaging system
   - Notifications
   - Advanced search filters
   - Profile verification badges
   - Photo gallery
   - Video profiles

2. **Improve UX:**
   - Loading skeletons
   - Toast notifications
   - Infinite scroll
   - Image lazy loading
   - Dark mode

3. **Performance:**
   - Code splitting
   - Memoization
   - Virtual scrolling for large lists
   - Service worker for offline support

4. **Testing:**
   - Unit tests with Jest
   - Integration tests with React Testing Library
   - E2E tests with Cypress

---

## 👥 Contributing

When adding new features:

1. Create component in appropriate folder
2. Add route in `App.jsx`
3. Create corresponding CSS file
4. Add API function in `api/api.js`
5. Update this README

---

## 📄 License

[Your License Here]

---

## 🎉 You're All Set!

Your React frontend is now ready with:

✅ Complete folder structure
✅ All pages and components
✅ API integration with JWT auth
✅ Protected routes
✅ Admin dashboard
✅ Responsive design
✅ Error handling

**Start the development server and begin building your matrimonial platform!** 🚀

