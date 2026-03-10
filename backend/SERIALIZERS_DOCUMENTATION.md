# Django REST Framework Serializers Documentation
## Matrimonial Website - Complete Serializer Guide

**Created:** October 14, 2025  
**File:** `backend/users/serializers.py`  
**Total Serializers:** 13

---

## Table of Contents
1. [Profile Serializers](#profile-serializers)
2. [User Serializers](#user-serializers)
3. [OTP Verification Serializers](#otp-verification-serializers)
4. [Interest Serializers](#interest-serializers)
5. [Report Serializers](#report-serializers)
6. [Export Log Serializers](#export-log-serializers)
7. [Validation Rules Summary](#validation-rules-summary)

---

## Profile Serializers

### 1. ProfileSerializer
**Purpose:** Main serializer for Profile model with comprehensive validation

**Fields:**
- `id` (read-only) - Profile ID
- `user` (write-only) - Foreign key to User
- `user_username` (read-only) - Associated user's username
- `user_email` (read-only) - Associated user's email
- `name` (required) - Full name (2-255 chars, letters and spaces only)
- `gender` (required) - Choice: male/female/other
- `age` (required) - Age in years (18-100)
- `occupation` (optional) - Occupation
- `education` (optional) - Education details
- `height` (optional) - Height in feet (3.0-8.0)
- `location` (required) - City, State, Country (min 3 chars)
- `about` (optional) - About yourself
- `desired_partner_traits` (optional) - Partner preferences
- `photo` (optional) - Profile photo (max 5MB, jpg/jpeg/png/gif)
- `photo_url` (read-only) - Absolute URL to photo
- `mobile_number` (required) - 10-15 digits with country code
- `created_at` (read-only) - Creation timestamp
- `updated_at` (read-only) - Last update timestamp

**Validation Rules:**
1. **Name Validation:**
   - Cannot be empty or just spaces
   - Only letters and spaces allowed
   - Automatically trimmed

2. **Age Validation:**
   - Must be at least 18 years old
   - Maximum age 100 years

3. **Height Validation:**
   - If provided, must be between 3.0 and 8.0 feet

4. **Mobile Number Validation:**
   - Allows digits, spaces, +, -, (, )
   - Must contain 10-15 digits (after removing special chars)

5. **Photo Validation:**
   - Maximum file size: 5MB
   - Allowed formats: jpg, jpeg, png, gif

6. **Cross-field Validation:**
   - Ensures one profile per user

**Example Usage:**
```python
# Create profile
data = {
    'user': user_id,
    'name': 'John Doe',
    'gender': 'male',
    'age': 28,
    'location': 'Mumbai, Maharashtra, India',
    'mobile_number': '+91 9876543210'
}
serializer = ProfileSerializer(data=data, context={'request': request})
if serializer.is_valid():
    profile = serializer.save()
```

---

## User Serializers

### 2. UserSerializer
**Purpose:** Display user information with nested profile

**Fields:**
- `id` (read-only) - User ID
- `username` (required) - Username
- `email` (required) - Email address
- `first_name` - First name
- `last_name` - Last name
- `full_name` (read-only) - Computed full name
- `is_admin` (read-only) - Admin status
- `is_active` - Account active status
- `profile` (read-only) - Nested profile data
- `date_joined` (read-only) - Registration date

**Example Response:**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "is_admin": false,
    "is_active": true,
    "profile": {
        "name": "John Doe",
        "age": 28,
        "gender": "male",
        ...
    },
    "date_joined": "2025-10-14T10:30:00Z"
}
```

### 3. UserRegistrationSerializer
**Purpose:** Handle user registration with password validation

**Fields:**
- `username` (required) - 3-150 chars, letters/numbers/underscores only
- `email` (required) - Must be unique
- `password` (required) - Write-only, validated for strength
- `password2` (required) - Write-only, must match password
- `first_name` (required) - First name
- `last_name` (required) - Last name

**Validation Rules:**
1. **Username:**
   - Only alphanumeric and underscores
   - Converted to lowercase
   - Minimum 3 characters

2. **Email:**
   - Must be unique (case-insensitive)
   - Converted to lowercase

3. **Password:**
   - Uses Django's validate_password
   - Minimum 8 characters (Django default)
   - Must not be too common
   - Must not be entirely numeric
   - Passwords must match

4. **Password Hashing:**
   - Uses `User.objects.create_user()` for proper hashing
   - Never stores plain text passwords

**Example Usage:**
```python
data = {
    'username': 'johndoe',
    'email': 'john@example.com',
    'password': 'SecurePass123!',
    'password2': 'SecurePass123!',
    'first_name': 'John',
    'last_name': 'Doe'
}
serializer = UserRegistrationSerializer(data=data)
if serializer.is_valid():
    user = serializer.save()
```

### 4. UserUpdateSerializer
**Purpose:** Update user information (excluding password)

**Fields:**
- `email` (optional) - Must be unique
- `first_name` (optional)
- `last_name` (optional)

**Validation:**
- Email uniqueness checked excluding current user

### 5. PasswordChangeSerializer
**Purpose:** Handle password changes securely

**Fields:**
- `old_password` (required) - Current password
- `new_password` (required) - New password with validation
- `new_password2` (required) - Confirm new password

**Validation Rules:**
1. Old password must be correct
2. New passwords must match
3. New password must be different from old password
4. New password must meet strength requirements

**Password Hashing:**
- Uses `user.set_password()` for proper hashing

---

## OTP Verification Serializers

### 6. OTPVerificationSerializer
**Purpose:** Manage OTP records

**Fields:**
- `id` (read-only)
- `user` (write-only) - Foreign key to User
- `user_username` (read-only)
- `otp` (required) - 6-digit code
- `is_verified` (read-only)
- `created_at` (read-only)
- `expires_at` (required)
- `is_expired` (read-only) - Computed expiration status

**Validation Rules:**
1. **OTP:**
   - Must be exactly 6 digits
   - Only numeric characters

2. **Expires At:**
   - Must be in the future

### 7. OTPVerifySerializer
**Purpose:** Verify OTP submission

**Fields:**
- `otp` (required) - 6-digit code

**Validation:**
- Must be 6 digits
- Only numeric characters

---

## Interest Serializers

### 8. InterestSerializer
**Purpose:** Handle interest/connection requests

**Fields:**
- `id` (read-only)
- `sender` (read-only) - Set automatically from request.user
- `sender_username` (read-only)
- `sender_name` (read-only)
- `receiver` (required) - User receiving interest
- `receiver_username` (read-only)
- `receiver_name` (read-only)
- `status` - pending/accepted/rejected
- `message` (optional) - Message with interest (max 500 chars)
- `created_at` (read-only)
- `responded_at` (read-only) - Set when status changes

**Validation Rules:**
1. **Message:**
   - If provided, minimum 10 characters
   - Automatically trimmed

2. **Cross-field Validation:**
   - Cannot send interest to yourself
   - Cannot send duplicate interest (unique sender-receiver pair)
   - Cannot change receiver after creation

3. **Status Updates:**
   - `responded_at` automatically set when status changes from pending

**Example Usage:**
```python
# Send interest
data = {
    'receiver': receiver_user_id,
    'message': 'Hello! I would like to connect with you.'
}
serializer = InterestSerializer(data=data, context={'request': request})
if serializer.is_valid():
    serializer.save(sender=request.user)
```

### 9. InterestResponseSerializer
**Purpose:** Accept or reject interest

**Fields:**
- `status` (required) - accepted/rejected

**Validation:**
- Only 'accepted' or 'rejected' allowed

---

## Report Serializers

### 10. ReportSerializer
**Purpose:** Handle user reports

**Fields:**
- `id` (read-only)
- `reporter` (read-only) - Set from request.user
- `reporter_username` (read-only)
- `reporter_name` (read-only)
- `reported_user` (required) - User being reported
- `reported_user_username` (read-only)
- `reported_user_name` (read-only)
- `reason` (required) - fake_profile/inappropriate_content/harassment/spam/other
- `reason_display` (read-only) - Human-readable reason
- `description` (required) - Detailed description (min 20 chars)
- `status` - pending/reviewed/resolved
- `status_display` (read-only)
- `created_at` (read-only)
- `reviewed_at` (read-only)
- `reviewed_by` (read-only) - Admin who reviewed
- `reviewed_by_username` (read-only)
- `admin_notes` (read-only)

**Validation Rules:**
1. **Description:**
   - Minimum 20 characters
   - Automatically trimmed

2. **Cross-field Validation:**
   - Cannot report yourself
   - Cannot report same user twice in 24 hours

**Example Usage:**
```python
data = {
    'reported_user': user_id,
    'reason': 'fake_profile',
    'description': 'This profile appears to be using fake photos and information...'
}
serializer = ReportSerializer(data=data, context={'request': request})
if serializer.is_valid():
    serializer.save(reporter=request.user)
```

### 11. ReportReviewSerializer
**Purpose:** Admin review of reports

**Fields:**
- `status` (required) - reviewed/resolved
- `admin_notes` (optional) - Admin comments (max 1000 chars)

**Validation:**
- Only 'reviewed' or 'resolved' statuses allowed

---

## Export Log Serializers

### 12. ExportLogSerializer
**Purpose:** Track admin data exports

**Fields:**
- `id` (read-only)
- `admin` (read-only) - Set from request.user
- `admin_username` (read-only)
- `admin_full_name` (read-only)
- `file_type` (required) - pdf/excel/csv
- `file_type_display` (read-only)
- `file_name` (required) - Name of exported file
- `export_type` (required) - users/profiles/reports/interests/all_data
- `record_count` (required) - Number of records (min 0)
- `created_at` (read-only)

**Validation Rules:**
1. **File Name:**
   - Cannot be empty
   - Cannot contain: < > : " / \ | ? *

2. **Export Type:**
   - Must be: users/profiles/reports/interests/all_data
   - Converted to lowercase

3. **Permission:**
   - Only admins can create export logs

### 13. ExportRequestSerializer
**Purpose:** Request data export with filters

**Fields:**
- `file_type` (required) - pdf/excel/csv
- `export_type` (required) - users/profiles/reports/interests/all_data
- `date_from` (optional) - Start date for filtering
- `date_to` (optional) - End date for filtering

**Validation Rules:**
1. **Date Range:**
   - End date must be after start date
   - Maximum range: 1 year

---

## Validation Rules Summary

### Password Security
✅ **Proper Password Hashing:**
- Registration: `User.objects.create_user()` with password parameter
- Password Change: `user.set_password()` method
- Never stores plain text passwords
- Uses Django's built-in password hashing (PBKDF2 by default)

✅ **Password Validation:**
- Minimum 8 characters
- Cannot be too common
- Cannot be entirely numeric
- Cannot be too similar to user information
- Must be confirmed with matching field

### Field Validations

| Field Type | Validation Rules |
|------------|------------------|
| **Name** | Letters and spaces only, 2-255 chars, trimmed |
| **Age** | 18-100 years |
| **Height** | 3.0-8.0 feet (if provided) |
| **Mobile** | 10-15 digits, allows +, -, (, ), spaces |
| **Email** | Must be unique, case-insensitive, lowercase |
| **Username** | 3-150 chars, alphanumeric + underscore, lowercase |
| **OTP** | Exactly 6 digits, numeric only |
| **Photo** | Max 5MB, jpg/jpeg/png/gif only |
| **Message** | Min 10 chars (if provided) |
| **Description** | Min 20 chars, required for reports |

### Business Logic Validations

✅ **Profile:**
- One profile per user
- Photo size and format restrictions

✅ **Interest:**
- Cannot send to yourself
- Cannot send duplicate interest
- Cannot change receiver after creation
- Responded_at auto-set on status change

✅ **Report:**
- Cannot report yourself
- Cannot report same user within 24 hours
- Detailed description required

✅ **Export Log:**
- Admin-only access
- Valid file name format
- Date range validation (max 1 year)

---

## Usage Examples

### Complete User Registration Flow
```python
# 1. Register user
registration_data = {
    'username': 'johndoe',
    'email': 'john@example.com',
    'password': 'SecurePass123!',
    'password2': 'SecurePass123!',
    'first_name': 'John',
    'last_name': 'Doe'
}
user_serializer = UserRegistrationSerializer(data=registration_data)
if user_serializer.is_valid():
    user = user_serializer.save()

# 2. Create profile
profile_data = {
    'user': user.id,
    'name': 'John Doe',
    'gender': 'male',
    'age': 28,
    'location': 'Mumbai, India',
    'mobile_number': '+91 9876543210',
    'occupation': 'Software Engineer',
    'education': 'B.Tech in Computer Science'
}
profile_serializer = ProfileSerializer(data=profile_data, context={'request': request})
if profile_serializer.is_valid():
    profile = profile_serializer.save()
```

### Send and Respond to Interest
```python
# Send interest
interest_data = {
    'receiver': receiver_id,
    'message': 'Hello! I would like to connect with you.'
}
interest_serializer = InterestSerializer(data=interest_data, context={'request': request})
if interest_serializer.is_valid():
    interest = interest_serializer.save(sender=request.user)

# Respond to interest
response_data = {'status': 'accepted'}
response_serializer = InterestResponseSerializer(data=response_data)
if response_serializer.is_valid():
    interest.status = response_data['status']
    interest.responded_at = timezone.now()
    interest.save()
```

### Change Password
```python
password_data = {
    'old_password': 'OldPass123!',
    'new_password': 'NewPass456!',
    'new_password2': 'NewPass456!'
}
password_serializer = PasswordChangeSerializer(
    data=password_data,
    context={'request': request}
)
if password_serializer.is_valid():
    password_serializer.save()
```

---

## Integration with Views

### Recommended View Structure
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InterestViewSet(viewsets.ModelViewSet):
    serializer_class = InterestSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        interest = self.get_object()
        if interest.receiver != request.user:
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = InterestResponseSerializer(data=request.data)
        if serializer.is_valid():
            interest.status = serializer.validated_data['status']
            interest.responded_at = timezone.now()
            interest.save()
            return Response(InterestSerializer(interest).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---

## Security Features

### 1. Password Security
- ✅ Automatic password hashing using Django's create_user()
- ✅ set_password() for password changes
- ✅ Password validation with Django validators
- ✅ Password confirmation required
- ✅ Old password verification for changes

### 2. Input Validation
- ✅ Field-level validation (name, email, phone, etc.)
- ✅ Cross-field validation (password match, age limits)
- ✅ Business logic validation (no self-interest, no duplicates)
- ✅ File upload validation (size, type)

### 3. Data Integrity
- ✅ Read-only fields for system-generated data
- ✅ Write-only fields for sensitive data (passwords)
- ✅ Automatic timestamp management
- ✅ Unique constraints enforcement

### 4. Permission Control
- ✅ Admin-only operations (export logs)
- ✅ User-specific data access
- ✅ Authorization checks in views

---

## Testing Recommendations

### Unit Tests
```python
from django.test import TestCase
from users.serializers import ProfileSerializer, UserRegistrationSerializer

class ProfileSerializerTest(TestCase):
    def test_valid_profile_creation(self):
        data = {
            'user': self.user.id,
            'name': 'John Doe',
            'gender': 'male',
            'age': 28,
            'location': 'Mumbai',
            'mobile_number': '+919876543210'
        }
        serializer = ProfileSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_invalid_age(self):
        data = {..., 'age': 15}
        serializer = ProfileSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('age', serializer.errors)
```

---

## Performance Considerations

### Optimizations
1. **Select Related:** Use `select_related()` for foreign keys
2. **Prefetch Related:** Use `prefetch_related()` for reverse relations
3. **Read-only Fields:** Minimize database queries
4. **SerializerMethodField:** Cache results when possible

### Best Practices
- Use `write_only=True` for sensitive fields
- Use `read_only=True` for computed fields
- Implement proper `get_queryset()` in views
- Use `context` to pass request data

---

## Conclusion

This comprehensive serializer implementation provides:
- ✅ **Security:** Proper password hashing and validation
- ✅ **Validation:** Comprehensive field and business logic validation
- ✅ **Flexibility:** Multiple serializers for different use cases
- ✅ **Maintainability:** Well-documented and organized code
- ✅ **User Experience:** Clear error messages and validation feedback
- ✅ **Data Integrity:** Automatic timestamp and status management

**Total Lines of Code:** ~630 lines  
**Total Serializers:** 13  
**Total Validation Methods:** 25+  
**Security Features:** Password hashing, validation, permission checks

---

**Last Updated:** October 14, 2025  
**Version:** 1.0  
**Author:** GitHub Copilot
