# Django REST Framework Serializers - Quick Reference
## Matrimonial Website API

---

## 📋 All Serializers Overview

| Serializer | Purpose | Key Fields | Validations |
|------------|---------|------------|-------------|
| **ProfileSerializer** | Profile CRUD | name, age, gender, mobile, photo | Age 18-100, phone format, photo 5MB max |
| **UserSerializer** | User display | username, email, profile (nested) | Email required |
| **UserRegistrationSerializer** | User signup | username, email, password, password2 | Password hashing, confirmation |
| **UserUpdateSerializer** | Update user info | email, first_name, last_name | Email uniqueness |
| **PasswordChangeSerializer** | Change password | old_password, new_password | Old password check, strength validation |
| **OTPVerificationSerializer** | OTP records | user, otp, expires_at | 6 digits, future expiry |
| **OTPVerifySerializer** | Verify OTP | otp | 6 digits numeric |
| **InterestSerializer** | Send/view interests | sender, receiver, message, status | No self-interest, no duplicates |
| **InterestResponseSerializer** | Accept/reject | status | accepted/rejected only |
| **ReportSerializer** | Report users | reported_user, reason, description | Min 20 chars, no self-report |
| **ReportReviewSerializer** | Admin review | status, admin_notes | reviewed/resolved only |
| **ExportLogSerializer** | Export tracking | file_type, export_type, record_count | Admin only, valid filename |
| **ExportRequestSerializer** | Request export | file_type, export_type, date_from, date_to | Max 1 year range |

---

## 🔐 Password Security Implementation

### Registration (UserRegistrationSerializer)
```python
def create(self, validated_data):
    validated_data.pop('password2')
    user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password'],  # ✅ Automatically hashed
        first_name=validated_data.get('first_name', ''),
        last_name=validated_data.get('last_name', '')
    )
    return user
```

### Password Change (PasswordChangeSerializer)
```python
def save(self, **kwargs):
    user = self.context['request'].user
    user.set_password(self.validated_data['new_password'])  # ✅ Properly hashed
    user.save()
    return user
```

**✅ Security Features:**
- Uses Django's `create_user()` for automatic hashing
- Uses `set_password()` for password updates
- Never stores plain text passwords
- Password validation with Django validators
- Password confirmation required

---

## ✅ Validation Rules Quick Reference

### Profile Validations
```python
# Name: Letters and spaces only
validate_name() -> "John Doe" ✅  "John123" ❌

# Age: 18-100 years
validate_age() -> 25 ✅  17 ❌  101 ❌

# Height: 3.0-8.0 feet
validate_height() -> 5.6 ✅  2.5 ❌  9.0 ❌

# Mobile: 10-15 digits
validate_mobile_number() -> "+91 9876543210" ✅  "123" ❌

# Photo: Max 5MB, jpg/jpeg/png/gif
validate_photo() -> 3MB JPG ✅  10MB BMP ❌
```

### User Validations
```python
# Username: Alphanumeric + underscore, 3-150 chars
validate_username() -> "john_doe" ✅  "john-doe" ❌  "ab" ❌

# Email: Unique, case-insensitive
validate_email() -> Checks uniqueness ✅

# Password: Django validation
- Minimum 8 characters ✅
- Cannot be too common ✅
- Cannot be entirely numeric ✅
- Must match confirmation ✅
```

### Interest Validations
```python
# Message: Min 10 chars if provided
validate_message() -> "Hello! Let's connect." ✅  "Hi" ❌

# Cross-field validation
validate() -> {
    Cannot send to yourself ❌
    Cannot send duplicate ❌
    Cannot change receiver ❌
}
```

### Report Validations
```python
# Description: Min 20 chars required
validate_description() -> "Detailed report text..." ✅  "Short" ❌

# Cross-field validation
validate() -> {
    Cannot report yourself ❌
    No duplicate reports in 24 hours ❌
}
```

---

## 🚀 Common Usage Patterns

### 1. User Registration + Profile Creation
```python
# Step 1: Register user
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
    user = user_serializer.save()  # ✅ Password automatically hashed

# Step 2: Create profile
profile_data = {
    'user': user.id,
    'name': 'John Doe',
    'gender': 'male',
    'age': 28,
    'location': 'Mumbai, India',
    'mobile_number': '+91 9876543210'
}
profile_serializer = ProfileSerializer(data=profile_data, context={'request': request})
if profile_serializer.is_valid():
    profile = profile_serializer.save()
```

### 2. Send Interest
```python
data = {
    'receiver': receiver_user_id,
    'message': 'Hello! I would like to connect with you.'
}
serializer = InterestSerializer(data=data, context={'request': request})
if serializer.is_valid():
    interest = serializer.save(sender=request.user)
```

### 3. Respond to Interest
```python
response_data = {'status': 'accepted'}  # or 'rejected'
serializer = InterestResponseSerializer(data=response_data)
if serializer.is_valid():
    interest.status = response_data['status']
    interest.responded_at = timezone.now()
    interest.save()
```

### 4. Change Password
```python
data = {
    'old_password': 'OldPass123!',
    'new_password': 'NewPass456!',
    'new_password2': 'NewPass456!'
}
serializer = PasswordChangeSerializer(data=data, context={'request': request})
if serializer.is_valid():
    serializer.save()  # ✅ Password properly hashed
```

### 5. Report User
```python
data = {
    'reported_user': user_id,
    'reason': 'fake_profile',
    'description': 'This profile appears to be using fake photos and information...'
}
serializer = ReportSerializer(data=data, context={'request': request})
if serializer.is_valid():
    report = serializer.save(reporter=request.user)
```

---

## 📊 Field Types Summary

### Read-Only Fields (Computed/System)
```python
- id
- created_at, updated_at
- date_joined
- photo_url
- full_name
- is_expired
- reason_display, status_display
- responded_at (auto-set)
- reviewed_at (auto-set)
```

### Write-Only Fields (Sensitive)
```python
- user (in ProfileSerializer)
- password, password2
- old_password, new_password, new_password2
```

### Required Fields
```python
ProfileSerializer: name, gender, age, location, mobile_number
UserRegistrationSerializer: username, email, password, password2, first_name, last_name
InterestSerializer: receiver
ReportSerializer: reported_user, reason, description
```

---

## 🔒 Business Logic Validations

### Profile
- ✅ One profile per user
- ✅ Photo size and format restrictions
- ✅ Age restrictions (18+)

### Interest
- ❌ Cannot send interest to yourself
- ❌ Cannot send duplicate interest
- ❌ Cannot change receiver after creation
- ✅ Auto-set responded_at on status change

### Report
- ❌ Cannot report yourself
- ❌ Cannot report same user within 24 hours
- ✅ Detailed description required (20+ chars)

### Export Log
- ❌ Admin-only access
- ✅ Valid file name format
- ✅ Date range validation (max 1 year)

---

## 🎯 API Response Examples

### Successful Registration
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Validation Error
```json
{
    "age": ["You must be at least 18 years old."],
    "mobile_number": ["Mobile number should contain between 10 and 15 digits."]
}
```

### User with Profile
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "profile": {
        "name": "John Doe",
        "age": 28,
        "gender": "male",
        "location": "Mumbai, India",
        "photo_url": "http://localhost:8000/media/profile_photos/john.jpg"
    }
}
```

### Interest with Names
```json
{
    "id": 1,
    "sender": 1,
    "sender_username": "johndoe",
    "sender_name": "John Doe",
    "receiver": 2,
    "receiver_username": "janedoe",
    "receiver_name": "Jane Doe",
    "status": "pending",
    "message": "Hello! I would like to connect.",
    "created_at": "2025-10-14T10:30:00Z",
    "responded_at": null
}
```

---

## 🛠️ Integration Checklist

### View Setup
- [ ] Import serializers
- [ ] Set serializer_class
- [ ] Add permission_classes
- [ ] Implement get_queryset()
- [ ] Override perform_create() if needed
- [ ] Pass context={'request': request}

### URL Configuration
- [ ] Add URL patterns
- [ ] Configure router for ViewSets
- [ ] Set basename if needed

### Testing
- [ ] Test valid data
- [ ] Test validation errors
- [ ] Test business logic validations
- [ ] Test password hashing
- [ ] Test permission checks

---

## 📝 Error Handling

### Common Validation Errors
```python
# Age validation
{"age": ["You must be at least 18 years old."]}

# Password mismatch
{"password2": ["Password fields didn't match."]}

# Duplicate interest
{"receiver": ["You have already sent an interest to this user. Status: pending"]}

# Self-interest
{"receiver": ["You cannot send interest to yourself."]}

# Self-report
{"reported_user": ["You cannot report yourself."]}

# Photo size
{"photo": ["Photo size should not exceed 5MB."]}

# Email exists
{"email": ["A user with this email already exists."]}
```

---

## 🎓 Best Practices

### 1. Always Use Context
```python
serializer = ProfileSerializer(data=data, context={'request': request})
```

### 2. Set User in View
```python
def perform_create(self, serializer):
    serializer.save(user=self.request.user)
```

### 3. Handle Validation Errors
```python
if serializer.is_valid():
    serializer.save()
else:
    return Response(serializer.errors, status=400)
```

### 4. Use Read-Only for Computed Fields
```python
full_name = serializers.SerializerMethodField()
```

### 5. Use Write-Only for Sensitive Data
```python
password = serializers.CharField(write_only=True)
```

---

## 📚 Quick Commands

### Check Serializers
```bash
# Syntax check
python -m py_compile users/serializers.py

# Django check
python manage.py check

# Test in shell
python manage.py shell
>>> from users.serializers import ProfileSerializer
>>> serializer = ProfileSerializer()
>>> serializer.fields
```

### Import in Views
```python
from users.serializers import (
    ProfileSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    InterestSerializer,
    ReportSerializer,
    # ... others
)
```

---

**Total Serializers:** 13  
**Total Validations:** 25+  
**Lines of Code:** ~630  
**Security:** ✅ Password hashing implemented  
**Documentation:** Complete

**Last Updated:** October 14, 2025
