# PerfectPair â€” Project Structure

## Repository Layout

```
Matrimonial_Site/                  â† Repository root
â”œâ”€â”€ README.md                      â† Project overview & feature summary
â”œâ”€â”€ PROJECT_STRUCTURE.md           â† This file
â”œâ”€â”€ exports/                       â† Admin-generated export files (saved to disk)
â””â”€â”€ backend/                       â† Django project root (run manage.py from here)
    â”œâ”€â”€ manage.py
    â”œâ”€â”€ requirements.txt
    â”œâ”€â”€ db.sqlite3                  â† SQLite database (dev)
    â”‚
    â”œâ”€â”€ config/                    â† Django project configuration package
    â”‚   â”œâ”€â”€ __init__.py
    â”‚   â”œâ”€â”€ settings.py
    â”‚   â”œâ”€â”€ urls.py
    â”‚   â”œâ”€â”€ asgi.py
    â”‚   â””â”€â”€ wsgi.py
    â”‚
    â”œâ”€â”€ apps/                      â† All Django apps
    â”‚   â”œâ”€â”€ __init__.py
    â”‚   â”œâ”€â”€ accounts/              â† Auth: User model, login, register, password reset
    â”‚   â”‚   â”œâ”€â”€ models.py          #   User, OTPVerification, PasswordResetRequest
    â”‚   â”‚   â”œâ”€â”€ views.py
    â”‚   â”‚   â”œâ”€â”€ urls.py            #   namespace: accounts
    â”‚   â”‚   â”œâ”€â”€ admin.py
    â”‚   â”‚   â”œâ”€â”€ apps.py
    â”‚   â”‚   â””â”€â”€ migrations/
    â”‚   â”œâ”€â”€ profiles/              â† Profile management & browsing
    â”‚   â”‚   â”œâ”€â”€ models.py          #   Profile
    â”‚   â”‚   â”œâ”€â”€ views.py
    â”‚   â”‚   â”œâ”€â”€ urls.py            #   namespace: profiles
    â”‚   â”‚   â”œâ”€â”€ admin.py
    â”‚   â”‚   â”œâ”€â”€ apps.py
    â”‚   â”‚   â””â”€â”€ migrations/
    â”‚   â”œâ”€â”€ matchmaking/           â† Interest / connection requests
    â”‚   â”‚   â”œâ”€â”€ models.py          #   Interest
    â”‚   â”‚   â”œâ”€â”€ views.py
    â”‚   â”‚   â”œâ”€â”€ urls.py            #   namespace: matchmaking
    â”‚   â”‚   â”œâ”€â”€ admin.py
    â”‚   â”‚   â”œâ”€â”€ apps.py
    â”‚   â”‚   â””â”€â”€ migrations/
    â”‚   â”œâ”€â”€ messaging/             â† HTMX real-time chat
    â”‚   â”‚   â”œâ”€â”€ models.py          #   Conversation, Message
    â”‚   â”‚   â”œâ”€â”€ views.py
    â”‚   â”‚   â”œâ”€â”€ urls.py            #   namespace: messaging
    â”‚   â”‚   â”œâ”€â”€ admin.py
    â”‚   â”‚   â”œâ”€â”€ apps.py
    â”‚   â”‚   â””â”€â”€ migrations/
    â”‚   â”œâ”€â”€ interactions/          â† Favorites
    â”‚   â”‚   â”œâ”€â”€ models.py          #   Favorite
    â”‚   â”‚   â”œâ”€â”€ views.py
    â”‚   â”‚   â”œâ”€â”€ urls.py            #   namespace: interactions
    â”‚   â”‚   â”œâ”€â”€ admin.py
    â”‚   â”‚   â”œâ”€â”€ apps.py
    â”‚   â”‚   â””â”€â”€ migrations/
    â”‚   â”œâ”€â”€ moderation/            â† Reports, blocking, admin dashboard, exports
    â”‚   â”‚   â”œâ”€â”€ models.py          #   Report, ExportLog
    â”‚   â”‚   â”œâ”€â”€ views.py
    â”‚   â”‚   â”œâ”€â”€ urls.py            #   namespace: moderation
    â”‚   â”‚   â”œâ”€â”€ admin.py
    â”‚   â”‚   â”œâ”€â”€ apps.py
    â”‚   â”‚   â””â”€â”€ migrations/
    â”‚   â”œâ”€â”€ feedback/              â† User feedback & admin responses
    â”‚   â”‚   â”œâ”€â”€ models.py          #   Feedback
    â”‚   â”‚   â”œâ”€â”€ views.py
    â”‚   â”‚   â”œâ”€â”€ urls.py            #   namespace: feedback
    â”‚   â”‚   â”œâ”€â”€ admin.py
    â”‚   â”‚   â”œâ”€â”€ apps.py
    â”‚   â”‚   â””â”€â”€ migrations/
    â”‚   â””â”€â”€ core/                  â† Shared utilities (no models/DB)
    â”‚       â”œâ”€â”€ __init__.py
    â”‚       â”œâ”€â”€ apps.py
    â”‚       â”œâ”€â”€ decorators.py      #   @admin_required
    â”‚       â”œâ”€â”€ middleware.py      #   NoCacheMiddleware
    â”‚       â””â”€â”€ context_processors.py  # pending_interests_count, unread_messages_count
    â”‚
    â”œâ”€â”€ templates/                 â† All HTML templates
    â”‚   â”œâ”€â”€ base/
    â”‚   â”‚   â”œâ”€â”€ base.html          â† Main layout (navbar, flash messages, footer)
    â”‚   â”‚   â””â”€â”€ base_auth.html     â† Minimal layout for login/register pages
    â”‚   â”œâ”€â”€ accounts/
    â”‚   â”‚   â”œâ”€â”€ login.html
    â”‚   â”‚   â”œâ”€â”€ register.html
    â”‚   â”‚   â””â”€â”€ forgot_password.html
    â”‚   â”œâ”€â”€ profiles/
    â”‚   â”‚   â”œâ”€â”€ home.html          â† Browse / search profiles (paginated)
    â”‚   â”‚   â”œâ”€â”€ detail.html        â† Single profile view
    â”‚   â”‚   â””â”€â”€ edit.html          â† Edit profile + change password
    â”‚   â”œâ”€â”€ matchmaking/
    â”‚   â”‚   â””â”€â”€ notifications.html â† Interests received / sent
    â”‚   â”œâ”€â”€ messaging/
    â”‚   â”‚   â”œâ”€â”€ inbox.html         â† Conversation list
    â”‚   â”‚   â”œâ”€â”€ conversation.html  â† Chat view (HTMX polling)
    â”‚   â”‚   â””â”€â”€ partials/
    â”‚   â”‚       â”œâ”€â”€ message_bubble.html  â† HTMX: single message fragment
    â”‚   â”‚       â””â”€â”€ new_messages.html    â† HTMX: new messages poll response
    â”‚   â”œâ”€â”€ interactions/
    â”‚   â”‚   â””â”€â”€ favorites.html     â† Saved profiles grid
    â”‚   â”œâ”€â”€ feedback/
    â”‚   â”‚   â””â”€â”€ feedback.html      â† Submit feedback & view history
    â”‚   â””â”€â”€ admin_panel/
    â”‚       â””â”€â”€ dashboard.html     â† Admin dashboard (5 tabs)
    â”‚
    â”œâ”€â”€ media/                     â† User-uploaded files (gitignored except .gitkeep)
    â”‚   â”œâ”€â”€ profile_photos/
    â”‚   â””â”€â”€ documents/
    â””â”€â”€ staticfiles/               â† Output of collectstatic
```

---

## Key Files Explained

### `config/` â€” Project Config

| File | Purpose |
|------|---------|
| `settings.py` | All Django config: SQLite (dev) / MySQL (prod), INSTALLED_APPS, MEDIA, STATIC, AUTH_USER_MODEL |
| `urls.py` | Root URL router â€” includes all 7 app URL configs and Django admin at `/admin/` |
| `asgi.py` | ASGI entrypoint (for async servers like Daphne/Uvicorn) |
| `wsgi.py` | WSGI entrypoint (for Gunicorn / Apache mod_wsgi) |

### `apps/` â€” Business Logic

| App | Models | Key Views |
|-----|--------|-----------|
| `accounts` | User, OTPVerification, PasswordResetRequest | login, logout, register, forgot_password, change_password, approve/reject_password_reset |
| `profiles` | Profile | home (browse), profile_detail, edit_profile, export_pdf, export_excel |
| `matchmaking` | Interest | send_interest, respond_interest, notifications |
| `messaging` | Conversation, Message | inbox, conversation, send_message, fetch_new_messages, start_conversation |
| `interactions` | Favorite | favorites, toggle_favorite |
| `moderation` | Report, ExportLog | report_profile, admin_dashboard, block_user, review_report |
| `feedback` | Feedback | feedback |
| `core` | *(none)* | decorators, middleware, context processors |

### `apps/core/` â€” Shared Utilities

| File | Purpose |
|------|---------|
| `decorators.py` | `@admin_required` â€” redirects non-admins; imported by accounts, profiles, moderation views |
| `middleware.py` | `NoCacheMiddleware` â€” sets `Cache-Control: no-store` on every response |
| `context_processors.py` | Injects `pending_interests_count` and `unread_messages_count` into every template |

### `backend/requirements.txt`

```
Django>=4.2,<5.0
Pillow>=10.0.0           # Image handling for profile photos
pandas>=2.0.0            # Data export to Excel/CSV
openpyxl>=3.1.0          # Excel file writing
reportlab>=4.0.0         # PDF generation
mysqlclient>=2.2.0       # MySQL driver (for production)
```

---

## Database Tables (`db.sqlite3`)

All custom tables retain their original `db_table` names (prefixed `users_*`) for schema compatibility.

| Table | App | Model | Description |
|-------|-----|-------|-------------|
| `users_user` | accounts | `User` | Custom auth user (extends AbstractUser) + blocking fields |
| `users_otpverification` | accounts | `OTPVerification` | OTP codes (10-min expiry) |
| `users_passwordresetrequest` | accounts | `PasswordResetRequest` | Admin-managed reset requests |
| `users_profile` | profiles | `Profile` | Matrimonial info: gender, DOB, age, religion, height, photo, etc. |
| `users_interest` | matchmaking | `Interest` | Connection requests (pending/accepted/rejected) |
| `users_conversation` | messaging | `Conversation` | Unique chat thread between two users |
| `users_message` | messaging | `Message` | Individual chat messages (with read status) |
| `users_favorite` | interactions | `Favorite` | Saved/bookmarked profiles |
| `users_report` | moderation | `Report` | Abuse/spam reports with admin review workflow |
| `users_exportlog` | moderation | `ExportLog` | Audit trail of admin PDF/Excel exports |
| `users_feedback` | feedback | `Feedback` | User feedback with admin response |

Plus standard Django tables: `auth_*`, `django_*`, `admin_*`, `sessions_*`

---

## URL Routes

Each app has its own namespace. All routes are at the root (`/`) â€” no prefix.

### `accounts:` namespace

| URL | View | Name |
|-----|------|------|
| `/login/` | `login_view` | `accounts:login` |
| `/logout/` | `logout_view` | `accounts:logout` |
| `/register/` | `register_view` | `accounts:register` |
| `/forgot-password/` | `forgot_password_view` | `accounts:forgot_password` |
| `/profile/change-password/` | `change_password_view` | `accounts:change_password` |
| `/admin/reset/<id>/approve/` | `approve_password_reset_view` | `accounts:approve_password_reset` |
| `/admin/reset/<id>/reject/` | `reject_password_reset_view` | `accounts:reject_password_reset` |

### `profiles:` namespace

| URL | View | Name |
|-----|------|------|
| `/home/` | `home_view` | `profiles:home` |
| `/profile/edit/` | `edit_profile_view` | `profiles:edit_profile` |
| `/profile/<pk>/` | `profile_detail_view` | `profiles:profile_detail` |
| `/admin/export/pdf/` | `export_pdf_view` | `profiles:export_pdf` |
| `/admin/export/excel/` | `export_excel_view` | `profiles:export_excel` |

### `matchmaking:` namespace

| URL | View | Name |
|-----|------|------|
| `/interest/send/<user_id>/` | `send_interest_view` | `matchmaking:send_interest` |
| `/interest/<id>/respond/` | `respond_interest_view` | `matchmaking:respond_interest` |
| `/notifications/` | `notifications_view` | `matchmaking:notifications` |

### `messaging:` namespace

| URL | View | Name |
|-----|------|------|
| `/messages/` | `inbox_view` | `messaging:inbox` |
| `/messages/<id>/` | `conversation_view` | `messaging:conversation` |
| `/messages/<id>/send/` | `send_message_view` | `messaging:send_message` |
| `/messages/<id>/new/` | `fetch_new_messages_view` | `messaging:fetch_new_messages` |
| `/messages/start/<user_id>/` | `start_conversation_view` | `messaging:start_conversation` |

### `interactions:` namespace

| URL | View | Name |
|-----|------|------|
| `/favorites/` | `favorites_view` | `interactions:favorites` |
| `/favorites/toggle/<profile_id>/` | `toggle_favorite_view` | `interactions:toggle_favorite` |

### `moderation:` namespace

| URL | View | Name |
|-----|------|------|
| `/admin-dashboard/` | `admin_dashboard_view` | `moderation:admin_dashboard` |
| `/profile/<id>/report/` | `report_profile_view` | `moderation:report_profile` |
| `/admin/user/<id>/block/` | `block_user_view` | `moderation:block_user` |
| `/admin/report/<id>/review/` | `review_report_view` | `moderation:review_report` |

### `feedback:` namespace

| URL | View | Name |
|-----|------|------|
| `/feedback/` | `feedback_view` | `feedback:feedback` |

---

## Templates Structure

### Base Templates

| Template | Used by |
|----------|---------|
| `base/base.html` | All authenticated pages (navbar, flash messages, footer, Tailwind + HTMX CDN) |
| `base/base_auth.html` | Login, register, forgot-password pages (minimal layout) |

### Template Groups

```
accounts/       login, register, forgot_password
profiles/       home (browse), detail, edit
matchmaking/    notifications
messaging/      inbox, conversation + 2 HTMX partials
interactions/   favorites
feedback/       feedback
admin_panel/    dashboard (5-tab admin UI)
```

---

## Media & Static Files

| Directory | Contents |
|-----------|---------|
| `media/profile_photos/` | User-uploaded profile pictures (served at `/media/profile_photos/`) |
| `media/documents/` | Reserved for future document uploads |
| `staticfiles/` | Output of `python manage.py collectstatic` |
| `exports/` | PDF and Excel files generated by admin export feature |

---

## Getting Started

```bash
# 1. Create & activate virtual environment
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. Create a superuser (admin)
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` â€” redirects to `/login/`.  
Django admin: `http://127.0.0.1:8000/admin/`  
Custom admin dashboard: `http://127.0.0.1:8000/admin-dashboard/` (requires `is_admin=True`)

### Promote a user to site admin

```bash
python manage.py shell
>>> from apps.accounts.models import User
>>> u = User.objects.get(username='yourusername')
>>> u.is_admin = True
>>> u.save()
```
