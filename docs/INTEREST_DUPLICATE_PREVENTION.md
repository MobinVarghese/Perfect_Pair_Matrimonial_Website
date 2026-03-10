# Interest Duplicate Prevention - Error Messages

## Overview
Added clear error messages when users attempt to send an interest request to someone they've already sent one to. The system now prevents duplicate interest requests and shows user-friendly error messages based on the current status.

## Changes Made

### Backend Changes

#### 1. **backend/users/serializers.py** (Lines 543-562)

**Updated `InterestSerializer.validate()` method:**

**Before:**
```python
if existing_interest:
    raise serializers.ValidationError({
        'receiver': f"You have already sent an interest to this user. Status: {existing_interest.status}"
    })
```

**After:**
```python
if existing_interest:
    if existing_interest.status == 'accepted':
        raise serializers.ValidationError({
            'error': "Request already sent once. Your interest has been accepted by this user."
        })
    elif existing_interest.status == 'rejected':
        raise serializers.ValidationError({
            'error': "Request already sent once. You cannot send interest again to this user."
        })
    else:  # pending
        raise serializers.ValidationError({
            'error': "Request already sent once. Your interest is pending approval."
        })
```

**Improvements:**
- ✅ More specific error messages based on interest status
- ✅ Uses 'error' key instead of 'receiver' for consistent frontend handling
- ✅ Clear "Request already sent once" prefix for all scenarios
- ✅ Prevents accidental duplicate submissions

### Frontend Changes

#### 2. **frontend/src/pages/HomePage.jsx** (Lines 336-339)

**Updated error handling in `handleSendInterest` function:**

**Before:**
```javascript
catch (error) {
  console.error('Error sending interest:', error);
  setNotification('Failed to send interest. Try again.');
  setTimeout(() => setNotification(''), 3000);
}
```

**After:**
```javascript
catch (error) {
  console.error('Error sending interest:', error);
  // Show backend error message if available
  if (error.response?.data?.error) {
    setNotification(error.response.data.error);
  } else {
    setNotification('Failed to send interest. Try again.');
  }
  setTimeout(() => setNotification(''), 3000);
}
```

**Improvements:**
- ✅ Shows backend error message when available
- ✅ Falls back to generic message for other errors
- ✅ Consistent with ProfileDetails error handling

#### 3. **frontend/src/pages/ProfileDetails.jsx** (Already Correct)

**Existing error handling (Lines 77-80):**
```javascript
if (error.response?.data?.error) {
  setNotification(error.response.data.error);
} else {
  setNotification('Failed to send interest. Try again.');
}
```

**Status:** ✅ Already handles backend error messages correctly

## Error Messages

### User Experience

| Status | Previous Message | New Message |
|--------|-----------------|-------------|
| **Pending** | "You have already sent an interest to this user. Status: pending" | "Request already sent once. Your interest is pending approval." |
| **Rejected** | "You have already sent an interest to this user. Status: rejected" | "Request already sent once. You cannot send interest again to this user." |
| **Accepted** | "You have already sent an interest to this user. Status: accepted" | "Request already sent once. Your interest has been accepted by this user." |

### Why These Changes?

1. **"Request already sent once"** - Matches your exact requirement
2. **Status-specific guidance** - Users understand what happened
3. **Prevents confusion** - Clear why they can't send again
4. **Consistent format** - All messages follow same pattern

## How It Works

### Scenario 1: Trying to Resend to Pending Interest
```
User: Clicks "Send Interest" (button shows as enabled due to page reload)
Backend: Checks database → Finds pending interest
Backend: Returns 400 error with message
Frontend: Shows notification: "Request already sent once. Your interest is pending approval."
```

### Scenario 2: Trying to Resend After Rejection
```
User: Clicks "Send Interest"
Backend: Checks database → Finds rejected interest
Backend: Returns 400 error with message
Frontend: Shows notification: "Request already sent once. You cannot send interest again to this user."
Button: Should be gray "Request Sent" (prevented by frontend state)
```

### Scenario 3: Trying to Resend After Acceptance
```
User: Clicks "Send Interest"
Backend: Checks database → Finds accepted interest
Backend: Returns 400 error with message
Frontend: Shows notification: "Request already sent once. Your interest has been accepted by this user."
Button: Should be green "Interest Accepted" (prevented by frontend state)
```

## Technical Flow

```
Frontend (HomePage/ProfileDetails)
    ↓
    User clicks "Send Interest"
    ↓
    Call sendInterest(profile.user)
    ↓
Backend (InterestSerializer.validate)
    ↓
    Check for existing interest
    ↓
    If exists → Raise ValidationError with 'error' key
    ↓
Frontend (catch block)
    ↓
    Check error.response.data.error
    ↓
    Display message in notification banner
    ↓
    Auto-hide after 3 seconds
```

## API Response Format

### Success Response (201 Created)
```json
{
  "id": 7,
  "sender": 8,
  "receiver": 5,
  "status": "pending",
  "message": "",
  "created_at": "2025-10-15T22:15:30Z"
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "Request already sent once. Your interest is pending approval."
}
```

## Testing

### Manual Test Steps

1. **Test Pending Status:**
   - Login as Sarah
   - Send interest to Mike
   - Try to send interest again (bypass frontend)
   - Should see: "Request already sent once. Your interest is pending approval."

2. **Test Rejected Status:**
   - Have Mike reject Sarah's interest
   - Login as Sarah
   - Try to send interest to Mike again
   - Should see: "Request already sent once. You cannot send interest again to this user."

3. **Test Accepted Status:**
   - Have Mike accept Sarah's interest
   - Login as Sarah
   - Try to send interest to Mike again
   - Should see: "Request already sent once. Your interest has been accepted by this user."

### Database Verification

Check existing interest:
```python
from users.models import Interest, User
sarah = User.objects.get(username='sarah_jones')
mike = User.objects.get(username='mike_brown')
interest = Interest.objects.filter(sender=sarah, receiver=mike).first()
print(f"Status: {interest.status if interest else 'None'}")
```

### API Test (curl)

```bash
# Send interest (first time - should succeed)
curl -X POST http://localhost:8000/api/interests/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receiver": 5, "message": ""}'

# Try to send again (should fail with error)
curl -X POST http://localhost:8000/api/interests/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receiver": 5, "message": ""}'
```

Expected second response:
```json
{
  "error": "Request already sent once. Your interest is pending approval."
}
```

## Files Modified

### Backend
- ✅ `backend/users/serializers.py` (Lines 543-562) - Enhanced error messages

### Frontend  
- ✅ `frontend/src/pages/HomePage.jsx` (Lines 336-342) - Added error.response.data.error handling
- ✅ `frontend/src/pages/ProfileDetails.jsx` (Already correct) - Confirmed error handling

**Total:** 2 files modified, 1 file verified

## Benefits

1. **Clear Communication** - Users know exactly why they can't resend
2. **Matches Requirement** - "Request already sent once" message as requested
3. **Status Awareness** - Different messages for pending/rejected/accepted
4. **Prevents Confusion** - No generic "Failed" messages
5. **Backend Validation** - Can't bypass even if frontend fails
6. **Consistent UX** - Same error handling on both HomePage and ProfileDetails

## Related Features

This works together with:
- ✅ Three-state button system (prevents UI-level duplicates)
- ✅ Interest status tracking (checks before showing button)
- ✅ Database constraints (prevents actual duplicates)
- ✅ API validation (backend-level protection)

## Notes

- Error messages auto-hide after 3 seconds
- Button state should prevent most duplicate attempts (frontend)
- Backend validation is the final safety net
- Messages are user-friendly and actionable
- Consistent across HomePage and ProfileDetails pages
