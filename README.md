# PerfectPair - Matrimonial Site

A full-featured matrimonial platform built with Django, HTMX, and Tailwind CSS.

---

## Tech Stack

| Layer      | Technology                              |
|------------|-----------------------------------------|
| Backend    | Django 4.2+                             |
| Frontend   | Django Templates, Tailwind CSS, HTMX    |
| Database   | SQLite (dev) / MySQL (production-ready) |
| Libraries  | Pillow, pandas, openpyxl, reportlab     |

---

## Features

### User Authentication
- Session-based login and registration
- Auto-profile creation on signup
- Password change for logged-in users
- Admin-managed password reset flow (user submits request → admin approves and generates temporary password)

### Profile Management
- Personal details: name, gender, date of birth, age (auto-calculated), religion, height, location, occupation, education, mobile number
- Photo upload (5 MB limit; jpg/jpeg/png/gif)
- Desired partner traits description
- Gender choices: Male / Female
- Religion choices: Hindu, Muslim, Christian, Sikh, Buddhist, Jain, Other
- Age validation: 18–100 (derived from DOB)
- Mobile validation: 10–15 digits, unique per profile

### Browse & Search
- Profile grid on home page with pagination (12 per page)
- Filters: gender, age range, location, occupation, education, religion
- Advanced search API endpoint

### Interest / Matching System
- Send interest to another user with an optional message
- Recipient can accept or reject the interest
- Notification badges for pending interests
- Blocked users cannot send interests

### Direct Messaging
- HTMX-powered real-time chat interface
- Conversation list (inbox) with unread message indicators
- Messaging is only enabled after both users have mutually accepted an interest
- Start a new conversation or continue an existing one

### Favorites
- Save / unsave profiles to a personal favorites list
- Toggle favorite from profile detail or browse pages

### Reporting & Safety
- Report a profile for: fake profile, inappropriate content, harassment, spam
- Report workflow: pending → reviewed → resolved
- User blocking with reason tracking and audit trail (who blocked, when, why)

### Feedback System
- Users can submit feedback with a category and subject
- View personal feedback history
- Admin can respond to feedback from the dashboard

### Notifications
- Badge counters for pending interests (received/sent)
- Unread message indicators in the inbox

---

## Admin Dashboard

Accessible at `/admin-dashboard/` for admin users.

### Dashboard Tabs

| Tab              | Capabilities                                                            |
|------------------|-------------------------------------------------------------------------|
| Users            | List all users, block/unblock with reason                               |
| Reports          | Review abuse reports, add admin notes, change status                    |
| Password Resets  | Approve reset requests, generate temporary passwords                    |
| Exports          | View export history (PDF/Excel)                                         |
| Feedback         | Read user feedback, send admin responses                                |

### Summary Cards
- Total users and profiles
- Pending reports, password reset requests, and feedback

### Data Exports (Admin Only)
- **PDF** — Profile listing with demographic stats (location distribution, age groups, interest/report metrics)
- **Excel** — Spreadsheet export with the same data and stats
- Export audit log tracks every export (admin, file type, record count)

---

## Routes

### Authentication
| Method | Endpoint                        | Description                |
|--------|---------------------------------|----------------------------|
| GET/POST | `/login/`                     | Log in                     |
| GET/POST | `/register/`                  | Register new user          |
| GET    | `/logout/`                      | Log out                    |
| GET/POST | `/forgot-password/`           | Request password reset     |

### Profiles
| Method | Endpoint                        | Description                |
|--------|---------------------------------|----------------------------|
| GET    | `/home/`                        | Browse profiles (filtered) |
| GET/POST | `/profile/edit/`              | Edit own profile           |
| GET    | `/profile/<id>/`                | View a profile             |
| POST   | `/profile/change-password/`     | Change password            |

### Interests
| Method | Endpoint                              | Description              |
|--------|---------------------------------------|--------------------------|
| POST   | `/interest/send/<user_id>/`           | Send interest            |
| POST   | `/interest/<interest_id>/respond/`    | Accept or reject         |
| GET    | `/notifications/`                     | View sent/received       |

### Messaging
| Method | Endpoint                                  | Description              |
|--------|-------------------------------------------|--------------------------|
| GET    | `/messages/`                              | Inbox                    |
| GET    | `/messages/<conversation_id>/`            | View conversation        |
| POST   | `/messages/<conversation_id>/send/`       | Send message (HTMX)      |
| POST   | `/messages/start/<user_id>/`              | Start new conversation   |

### Favorites
| Method | Endpoint                            | Description              |
|--------|-------------------------------------|--------------------------|
| GET    | `/favorites/`                       | View favorites           |
| POST   | `/favorites/toggle/<profile_id>/`   | Add / remove favorite    |

### Reporting
| Method | Endpoint                            | Description              |
|--------|-------------------------------------|--------------------------|
| POST   | `/profile/<profile_id>/report/`     | Report a user            |

### Feedback
| Method | Endpoint                            | Description              |
|--------|-------------------------------------|--------------------------|
| GET    | `/feedback/`                        | Submit & view feedback   |

### Account
| Method | Endpoint                            | Description              |
|--------|-------------------------------------|--------------------------|
| POST   | `/profile/change-password/`         | Change password          |

### Admin
| Method | Endpoint                                    | Description                    |
|--------|---------------------------------------------|--------------------------------|
| GET    | `/admin-dashboard/`                         | Dashboard                      |
| POST   | `/admin/user/<user_id>/block/`              | Block / unblock user           |
| POST   | `/admin/report/<report_id>/review/`         | Review a report                |
| GET    | `/admin/export/pdf/`                        | Export profiles as PDF         |
| GET    | `/admin/export/excel/`                      | Export profiles as Excel       |

---

## Data Models

| Model                | Description                                         |
|----------------------|-----------------------------------------------------|
| User                 | Custom user with admin and blocking fields           |
| Profile              | Matrimonial profile (personal info, photo, partner prefs) |
| Interest             | Connection request (pending / accepted / rejected)   |
| Favorite             | Saved profile bookmark                               |
| Conversation         | Chat between two users (unique pair)                 |
| Message              | Individual chat message with read status             |
| Report               | Abuse/spam report with admin review workflow         |
| OTPVerification      | OTP codes for mobile/email verification              |
| PasswordResetRequest | Admin-managed password reset workflow                |
| Feedback             | User feedback with admin response                    |
| ExportLog            | Audit trail for admin data exports                   |

---

## Security & Permissions

- **Access control**: `@login_required` for all authenticated pages, custom `@admin_required` for admin views
- **User blocking**: blocked users cannot send interests; full audit trail
- **Report moderation**: admin review workflow for flagged profiles
- **No-cache middleware**: prevents browser caching of authenticated pages
- **Input validation**: age 18+, mobile format, file size/type limits, Django password validators (8+ characters)

---

## User Workflow

```
Register (mobile + gender + DOB)
  └─► Profile auto-created
        └─► Browse & filter profiles
              └─► Send interest (optional message)
                    └─► Recipient accepts
                          └─► Both can message each other
```

### Admin Password Reset Flow

```
User submits forgot-password request
  └─► Admin sees request in dashboard
        └─► Admin approves & generates temporary password
              └─► User logs in with temp password → changes password
```

---

## Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── config/                        # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                          # All Django apps
│   ├── accounts/                  # Auth: User model, login, register, password reset
│   │   ├── models.py              #   User, OTPVerification, PasswordResetRequest
│   │   ├── views.py
│   │   ├── urls.py                #   namespace: accounts
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── profiles/                  # Profile management & browsing
│   │   ├── models.py              #   Profile
│   │   ├── views.py
│   │   ├── urls.py                #   namespace: profiles
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── matchmaking/               # Interest / connection requests
│   │   ├── models.py              #   Interest
│   │   ├── views.py
│   │   ├── urls.py                #   namespace: matchmaking
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── messaging/                 # HTMX real-time chat
│   │   ├── models.py              #   Conversation, Message
│   │   ├── views.py
│   │   ├── urls.py                #   namespace: messaging
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── interactions/              # Favorites
│   │   ├── models.py              #   Favorite
│   │   ├── views.py
│   │   ├── urls.py                #   namespace: interactions
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── moderation/                # Reports, user blocking, admin dashboard, exports
│   │   ├── models.py              #   Report, ExportLog
│   │   ├── views.py
│   │   ├── urls.py                #   namespace: moderation
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── feedback/                  # User feedback & admin responses
│   │   ├── models.py              #   Feedback
│   │   ├── views.py
│   │   ├── urls.py                #   namespace: feedback
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   └── core/                      # Shared utilities (no models/migrations)
│       ├── decorators.py          #   @admin_required
│       ├── middleware.py          #   NoCacheMiddleware
│       └── context_processors.py #   pending_interests_count, unread_messages_count
│
├── templates/                     # HTML templates (Django template engine)
│   ├── base/
│   │   ├── base.html              #   Main layout (navbar, flash messages, footer)
│   │   └── base_auth.html         #   Minimal layout for login/register pages
│   ├── accounts/                  #   login.html, register.html, forgot_password.html
│   ├── profiles/                  #   home.html, detail.html, edit.html
│   ├── matchmaking/               #   notifications.html
│   ├── messaging/                 #   inbox.html, conversation.html
│   │   └── partials/              #   HTMX fragments: message_bubble.html, new_messages.html
│   ├── interactions/              #   favorites.html
│   ├── feedback/                  #   feedback.html
│   └── admin_panel/               #   dashboard.html
│
├── media/                         # Uploaded files
│   ├── profile_photos/
│   └── documents/
└── staticfiles/
```

---

## Getting Started

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
