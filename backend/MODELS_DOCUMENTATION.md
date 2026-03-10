# Django Models Documentation - Matrimonial Website

## Overview
Complete Django models implementation for a matrimonial website with user management, profiles, OTP verification, interest/connection system, reporting, and export logging.

---

## 📋 Models Summary

### 1. **User Model**
Custom user model extending Django's AbstractUser

### 2. **Profile Model**
Detailed matrimonial profile information

### 3. **OTPVerification Model**
Mobile number verification via OTP

### 4. **Interest Model**
Connection requests between users

### 5. **Report Model**
User reporting system for inappropriate content

### 6. **ExportLog Model**
Track data exports by admins

---

## 🔧 Model Definitions

### 1. User Model

**Extends:** `AbstractUser`

**Purpose:** Custom user authentication with admin privileges

**Fields:**
- All fields from AbstractUser (username, email, password, first_name, last_name, etc.)
- `is_admin` (Boolean) - Designates admin users

**Database Table:** `users_user`

**Methods:**
- `__str__()` - Returns username

**Example:**
```python
user = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='securepass123',
    is_admin=False
)
```

---

### 2. Profile Model

**Purpose:** Store detailed matrimonial profile information

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | Link to User model |
| `name` | CharField(255) | Full name |
| `gender` | CharField(10) | Male/Female/Other |
| `age` | PositiveIntegerField | Age (18-100) |
| `occupation` | CharField(255) | Job/profession |
| `education` | CharField(255) | Educational qualification |
| `height` | DecimalField(4,2) | Height in feet (e.g., 5.6) |
| `location` | CharField(255) | City, State, Country |
| `about` | TextField | About section |
| `desired_partner_traits` | TextField | Partner preferences |
| `photo` | ImageField | Profile photo |
| `mobile_number` | CharField(15) | Unique mobile number |
| `created_at` | DateTimeField | Auto-generated |
| `updated_at` | DateTimeField | Auto-updated |

**Database Table:** `users_profile`

**Relationships:**
- OneToOne with User (CASCADE delete)

**Validators:**
- Age: 18-100 years
- Mobile number: Unique

**Methods:**
- `__str__()` - Returns "Name's Profile (username)"

**Example:**
```python
profile = Profile.objects.create(
    user=user,
    name='John Doe',
    gender='male',
    age=28,
    occupation='Software Engineer',
    education='Bachelor in Computer Science',
    height=5.10,
    location='New York, NY, USA',
    about='Looking for a life partner...',
    desired_partner_traits='Kind, educated, family-oriented',
    mobile_number='+1234567890'
)
```

---

### 3. OTPVerification Model

**Purpose:** Verify user mobile numbers via OTP

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | Link to User |
| `otp` | CharField(6) | 6-digit OTP code |
| `is_verified` | BooleanField | Verification status |
| `created_at` | DateTimeField | Auto-generated |
| `expires_at` | DateTimeField | OTP expiration time |

**Database Table:** `users_otpverification`

**Relationships:**
- ForeignKey to User (CASCADE delete)

**Methods:**
- `__str__()` - Returns "OTP for username - Status"
- `is_expired()` - Check if OTP has expired

**Example:**
```python
from django.utils import timezone
from datetime import timedelta

otp = OTPVerification.objects.create(
    user=user,
    otp='123456',
    is_verified=False,
    expires_at=timezone.now() + timedelta(minutes=10)
)

# Check if expired
if otp.is_expired():
    print("OTP has expired")
```

---

### 4. Interest Model

**Purpose:** Manage connection requests between users

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `sender` | ForeignKey | User sending interest |
| `receiver` | ForeignKey | User receiving interest |
| `status` | CharField(10) | pending/accepted/rejected |
| `message` | TextField | Optional message |
| `created_at` | DateTimeField | Auto-generated |
| `responded_at` | DateTimeField | Response timestamp |

**Database Table:** `users_interest`

**Relationships:**
- ForeignKey to User as sender (CASCADE delete)
- ForeignKey to User as receiver (CASCADE delete)

**Constraints:**
- Unique together: (sender, receiver) - Prevents duplicate interests

**Methods:**
- `__str__()` - Returns "sender → receiver (status)"

**Example:**
```python
interest = Interest.objects.create(
    sender=user1,
    receiver=user2,
    status='pending',
    message='I would like to connect with you.'
)

# Accept interest
interest.status = 'accepted'
interest.responded_at = timezone.now()
interest.save()
```

---

### 5. Report Model

**Purpose:** Allow users to report inappropriate profiles/behavior

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `reporter` | ForeignKey | User making the report |
| `reported_user` | ForeignKey | User being reported |
| `reason` | CharField(50) | Report category |
| `description` | TextField | Detailed description |
| `status` | CharField(10) | pending/reviewed/resolved |
| `created_at` | DateTimeField | Auto-generated |
| `reviewed_at` | DateTimeField | Review timestamp |
| `reviewed_by` | ForeignKey | Admin who reviewed |
| `admin_notes` | TextField | Admin's notes |

**Database Table:** `users_report`

**Relationships:**
- ForeignKey to User as reporter (CASCADE delete)
- ForeignKey to User as reported_user (CASCADE delete)
- ForeignKey to User as reviewed_by (SET_NULL on delete)

**Reason Choices:**
- fake_profile
- inappropriate_content
- harassment
- spam
- other

**Status Choices:**
- pending
- reviewed
- resolved

**Methods:**
- `__str__()` - Returns "Report by reporter against reported_user - status"

**Example:**
```python
report = Report.objects.create(
    reporter=user1,
    reported_user=user2,
    reason='fake_profile',
    description='This profile seems to be using fake photos.',
    status='pending'
)

# Admin reviews
report.status = 'reviewed'
report.reviewed_by = admin_user
report.reviewed_at = timezone.now()
report.admin_notes = 'Investigated and confirmed fake profile'
report.save()
```

---

### 6. ExportLog Model

**Purpose:** Track data exports by administrators

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `admin` | ForeignKey | Admin performing export |
| `file_type` | CharField(10) | pdf/excel/csv |
| `file_name` | CharField(255) | Name of exported file |
| `export_type` | CharField(50) | Type of data exported |
| `record_count` | PositiveIntegerField | Number of records |
| `created_at` | DateTimeField | Auto-generated |

**Database Table:** `users_exportlog`

**Relationships:**
- ForeignKey to User as admin (CASCADE delete, limited to is_admin=True)

**File Type Choices:**
- pdf
- excel
- csv

**Methods:**
- `__str__()` - Returns "admin exported export_type as file_type on date"

**Example:**
```python
export_log = ExportLog.objects.create(
    admin=admin_user,
    file_type='excel',
    file_name='users_export_2025_10_14.xlsx',
    export_type='users',
    record_count=150
)
```

---

## 🗃️ Database Schema

```
users_user (Custom User)
├── id (PK)
├── username
├── email
├── password
├── first_name
├── last_name
├── is_admin
└── ... (other AbstractUser fields)

users_profile
├── id (PK)
├── user_id (FK → users_user)
├── name
├── gender
├── age
├── occupation
├── education
├── height
├── location
├── about
├── desired_partner_traits
├── photo
├── mobile_number (Unique)
├── created_at
└── updated_at

users_otpverification
├── id (PK)
├── user_id (FK → users_user)
├── otp
├── is_verified
├── created_at
└── expires_at

users_interest
├── id (PK)
├── sender_id (FK → users_user)
├── receiver_id (FK → users_user)
├── status
├── message
├── created_at
└── responded_at

users_report
├── id (PK)
├── reporter_id (FK → users_user)
├── reported_user_id (FK → users_user)
├── reason
├── description
├── status
├── created_at
├── reviewed_at
├── reviewed_by_id (FK → users_user)
└── admin_notes

users_exportlog
├── id (PK)
├── admin_id (FK → users_user)
├── file_type
├── file_name
├── export_type
├── record_count
└── created_at
```

---

## 🔄 Relationships

```
User (1) ←→ (1) Profile
User (1) ←→ (*) OTPVerification
User (1) ←→ (*) Interest (as sender)
User (1) ←→ (*) Interest (as receiver)
User (1) ←→ (*) Report (as reporter)
User (1) ←→ (*) Report (as reported_user)
User (1) ←→ (*) Report (as reviewed_by)
User (1) ←→ (*) ExportLog (as admin)
```

---

## ⚙️ Configuration

### settings.py
```python
# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Installed Apps
INSTALLED_APPS = [
    ...
    'users',
]
```

---

## 🚀 Usage Examples

### Creating a Complete User Profile
```python
from users.models import User, Profile

# Create user
user = User.objects.create_user(
    username='jane_doe',
    email='jane@example.com',
    password='securepass123'
)

# Create profile
profile = Profile.objects.create(
    user=user,
    name='Jane Doe',
    gender='female',
    age=26,
    occupation='Doctor',
    education='MBBS',
    height=5.6,
    location='San Francisco, CA, USA',
    mobile_number='+19876543210',
    about='Medical professional seeking educated partner',
    desired_partner_traits='Educated, caring, supportive'
)
```

### Sending Interest
```python
from users.models import Interest

interest = Interest.objects.create(
    sender=user1,
    receiver=user2,
    message='Hi, I found your profile interesting!'
)
```

### OTP Workflow
```python
import random
from django.utils import timezone
from datetime import timedelta

# Generate OTP
otp_code = str(random.randint(100000, 999999))

# Create OTP record
otp = OTPVerification.objects.create(
    user=user,
    otp=otp_code,
    expires_at=timezone.now() + timedelta(minutes=10)
)

# Verify OTP
user_input_otp = '123456'
if otp.otp == user_input_otp and not otp.is_expired():
    otp.is_verified = True
    otp.save()
```

---

## ✅ Migrations Applied

All models have been successfully migrated to the database.

**Migration File:** `users/migrations/0001_initial.py`

**Tables Created:**
- ✅ users_user
- ✅ users_profile
- ✅ users_otpverification
- ✅ users_interest
- ✅ users_report
- ✅ users_exportlog

---

## 📊 Admin Interface

All models are registered in the Django admin with custom configurations:
- Custom list displays
- Search and filter options
- Readonly fields
- Organized fieldsets

Access at: `http://localhost:8000/admin/`

---

## 🎯 Features

✅ Custom User model with admin flag  
✅ Comprehensive matrimonial profiles  
✅ Mobile OTP verification system  
✅ Interest/connection management  
✅ User reporting with admin review  
✅ Export tracking for auditing  
✅ All models include created_at timestamps  
✅ Proper string representations (__str__)  
✅ Validation and constraints  
✅ Foreign key relationships with proper delete behavior  

---

**Status:** All models created and migrated successfully! ✅  
**Date:** October 14, 2025  
**Location:** `d:\Matrimonial_Site\backend\users\models.py`
