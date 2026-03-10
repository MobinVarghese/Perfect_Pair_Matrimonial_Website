# JWT Authentication Testing Guide
## Quick Tests for Token Endpoints

**Created:** October 14, 2025  
**Purpose:** Verify JWT authentication integration

---

## Prerequisites

1. **Start Django Server:**
   ```bash
   cd d:\Matrimonial_Site\backend
   python manage.py runserver
   ```

2. **Create Test User (if not exists):**
   ```bash
   python manage.py createsuperuser
   ```
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: `admin123`

---

## Test 1: Login - Primary Endpoint

### Request
```bash
curl -X POST http://localhost:8000/api/token/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

### Expected Response
```json
{
    "access": "eyJ0eXAiOiJKV1QiLC...",
    "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

**Status Code:** 200 OK

---

## Test 2: Login - Alternative Endpoint

### Request
```bash
curl -X POST http://localhost:8000/api/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

### Expected Response
Same as Test 1 (both endpoints use the same view)

---

## Test 3: Access Protected Endpoint

### Without Token (Should Fail)
```bash
curl -X GET http://localhost:8000/api/profiles/
```

**Expected Response:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```
**Status Code:** 401 Unauthorized

### With Token (Should Succeed)
```bash
curl -X GET http://localhost:8000/api/profiles/ ^
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

**Replace `<YOUR_ACCESS_TOKEN>` with actual token from Test 1**

**Expected Response:**
```json
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
```
**Status Code:** 200 OK

---

## Test 4: Refresh Token - Primary Endpoint

### Request
```bash
curl -X POST http://localhost:8000/api/token/refresh/ ^
  -H "Content-Type: application/json" ^
  -d "{\"refresh\":\"<YOUR_REFRESH_TOKEN>\"}"
```

**Replace `<YOUR_REFRESH_TOKEN>` with actual refresh token from Test 1**

### Expected Response
```json
{
    "access": "eyJ0eXAiOiJKV1QiLC...",
    "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

**Note:** Both access AND refresh tokens are returned (token rotation enabled)

**Status Code:** 200 OK

---

## Test 5: Refresh Token - Alternative Endpoint

### Request
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ ^
  -H "Content-Type: application/json" ^
  -d "{\"refresh\":\"<YOUR_REFRESH_TOKEN>\"}"
```

**Expected Response:** Same as Test 4

---

## Test 6: Verify Token - Primary Endpoint

### Request
```bash
curl -X POST http://localhost:8000/api/token/verify/ ^
  -H "Content-Type: application/json" ^
  -d "{\"token\":\"<YOUR_ACCESS_TOKEN>\"}"
```

### Expected Response (Valid Token)
```json
{}
```
**Status Code:** 200 OK  
**Note:** Empty response = valid token

### Expected Response (Invalid Token)
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```
**Status Code:** 401 Unauthorized

---

## Test 7: Verify Token - Alternative Endpoint

### Request
```bash
curl -X POST http://localhost:8000/api/auth/verify/ ^
  -H "Content-Type: application/json" ^
  -d "{\"token\":\"<YOUR_ACCESS_TOKEN>\"}"
```

**Expected Response:** Same as Test 6

---

## Test 8: User Registration

### Request
```bash
curl -X POST http://localhost:8000/api/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"Test123!@#\",\"password2\":\"Test123!@#\",\"first_name\":\"Test\",\"last_name\":\"User\"}"
```

### Expected Response
```json
{
    "id": 2,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "is_admin": false,
    "is_active": true,
    "date_joined": "2025-10-14T10:30:00Z"
}
```

**Status Code:** 201 Created

---

## Test 9: Get Current User

### Request
```bash
curl -X GET http://localhost:8000/api/users/me/ ^
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

### Expected Response
```json
{
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": "",
    "is_admin": true,
    "is_active": true,
    "date_joined": "2025-10-14T10:00:00Z"
}
```

**Status Code:** 200 OK

---

## Test 10: Change Password

### Request
```bash
curl -X PUT http://localhost:8000/api/users/change-password/ ^
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"old_password\":\"admin123\",\"new_password\":\"NewPass123!@#\",\"new_password2\":\"NewPass123!@#\"}"
```

### Expected Response
```json
{
    "message": "Password changed successfully"
}
```

**Status Code:** 200 OK

---

## PowerShell Testing Script

Save as `test_jwt.ps1`:

```powershell
# JWT Authentication Testing Script
# Run from: d:\Matrimonial_Site\backend

$BASE_URL = "http://localhost:8000"

Write-Host "=== JWT Authentication Tests ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Login
Write-Host "Test 1: Login (Primary Endpoint)" -ForegroundColor Yellow
$loginResponse = Invoke-RestMethod -Uri "$BASE_URL/api/token/" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"username":"admin","password":"admin123"}' `
    -ErrorAction SilentlyContinue

if ($loginResponse.access) {
    Write-Host "✓ Login successful" -ForegroundColor Green
    $accessToken = $loginResponse.access
    $refreshToken = $loginResponse.refresh
    Write-Host "Access Token: $($accessToken.Substring(0, 50))..." -ForegroundColor Gray
    Write-Host "Refresh Token: $($refreshToken.Substring(0, 50))..." -ForegroundColor Gray
} else {
    Write-Host "✗ Login failed" -ForegroundColor Red
    exit
}
Write-Host ""

# Test 2: Access Protected Endpoint
Write-Host "Test 2: Access Protected Endpoint" -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $accessToken"
    }
    $profiles = Invoke-RestMethod -Uri "$BASE_URL/api/profiles/" `
        -Method Get `
        -Headers $headers
    
    Write-Host "✓ Protected endpoint accessible" -ForegroundColor Green
    Write-Host "Profile count: $($profiles.count)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Failed to access protected endpoint" -ForegroundColor Red
}
Write-Host ""

# Test 3: Refresh Token
Write-Host "Test 3: Refresh Token (Primary Endpoint)" -ForegroundColor Yellow
try {
    $refreshResponse = Invoke-RestMethod -Uri "$BASE_URL/api/token/refresh/" `
        -Method Post `
        -ContentType "application/json" `
        -Body "{`"refresh`":`"$refreshToken`"}"
    
    Write-Host "✓ Token refresh successful" -ForegroundColor Green
    Write-Host "New Access Token: $($refreshResponse.access.Substring(0, 50))..." -ForegroundColor Gray
    Write-Host "New Refresh Token: $($refreshResponse.refresh.Substring(0, 50))..." -ForegroundColor Gray
} catch {
    Write-Host "✗ Token refresh failed" -ForegroundColor Red
}
Write-Host ""

# Test 4: Verify Token
Write-Host "Test 4: Verify Token (Primary Endpoint)" -ForegroundColor Yellow
try {
    $verifyResponse = Invoke-RestMethod -Uri "$BASE_URL/api/token/verify/" `
        -Method Post `
        -ContentType "application/json" `
        -Body "{`"token`":`"$accessToken`"}"
    
    Write-Host "✓ Token is valid" -ForegroundColor Green
} catch {
    Write-Host "✗ Token is invalid" -ForegroundColor Red
}
Write-Host ""

# Test 5: Get Current User
Write-Host "Test 5: Get Current User" -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $accessToken"
    }
    $currentUser = Invoke-RestMethod -Uri "$BASE_URL/api/users/me/" `
        -Method Get `
        -Headers $headers
    
    Write-Host "✓ Current user retrieved" -ForegroundColor Green
    Write-Host "Username: $($currentUser.username)" -ForegroundColor Gray
    Write-Host "Email: $($currentUser.email)" -ForegroundColor Gray
    Write-Host "Is Admin: $($currentUser.is_admin)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Failed to get current user" -ForegroundColor Red
}
Write-Host ""

Write-Host "=== All Tests Complete ===" -ForegroundColor Cyan
```

**Run the script:**
```powershell
cd d:\Matrimonial_Site\backend
.\test_jwt.ps1
```

---

## Python Testing Script

Save as `test_jwt.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def print_test(name, success, details=""):
    status = "✓" if success else "✗"
    color = "\033[92m" if success else "\033[91m"
    print(f"{color}{status}\033[0m {name}")
    if details:
        print(f"  {details}")

print("\n=== JWT Authentication Tests ===\n")

# Test 1: Login
print("Test 1: Login (Primary Endpoint)")
try:
    response = requests.post(
        f"{BASE_URL}/api/token/",
        json={"username": "admin", "password": "admin123"}
    )
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens["access"]
        refresh_token = tokens["refresh"]
        print_test("Login successful", True)
        print(f"  Access Token: {access_token[:50]}...")
        print(f"  Refresh Token: {refresh_token[:50]}...")
    else:
        print_test("Login failed", False, f"Status: {response.status_code}")
        exit()
except Exception as e:
    print_test("Login failed", False, str(e))
    exit()

print()

# Test 2: Access Protected Endpoint
print("Test 2: Access Protected Endpoint")
try:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/api/profiles/", headers=headers)
    
    if response.status_code == 200:
        profiles = response.json()
        print_test("Protected endpoint accessible", True)
        print(f"  Profile count: {profiles['count']}")
    else:
        print_test("Failed to access protected endpoint", False)
except Exception as e:
    print_test("Failed to access protected endpoint", False, str(e))

print()

# Test 3: Refresh Token
print("Test 3: Refresh Token (Primary Endpoint)")
try:
    response = requests.post(
        f"{BASE_URL}/api/token/refresh/",
        json={"refresh": refresh_token}
    )
    
    if response.status_code == 200:
        new_tokens = response.json()
        print_test("Token refresh successful", True)
        print(f"  New Access Token: {new_tokens['access'][:50]}...")
        print(f"  New Refresh Token: {new_tokens['refresh'][:50]}...")
    else:
        print_test("Token refresh failed", False)
except Exception as e:
    print_test("Token refresh failed", False, str(e))

print()

# Test 4: Verify Token
print("Test 4: Verify Token (Primary Endpoint)")
try:
    response = requests.post(
        f"{BASE_URL}/api/token/verify/",
        json={"token": access_token}
    )
    
    if response.status_code == 200:
        print_test("Token is valid", True)
    else:
        print_test("Token is invalid", False)
except Exception as e:
    print_test("Token verification failed", False, str(e))

print()

# Test 5: Get Current User
print("Test 5: Get Current User")
try:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/api/users/me/", headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        print_test("Current user retrieved", True)
        print(f"  Username: {user['username']}")
        print(f"  Email: {user['email']}")
        print(f"  Is Admin: {user['is_admin']}")
    else:
        print_test("Failed to get current user", False)
except Exception as e:
    print_test("Failed to get current user", False, str(e))

print()
print("=== All Tests Complete ===\n")
```

**Run the script:**
```bash
cd d:\Matrimonial_Site\backend
python test_jwt.py
```

---

## Postman/Thunder Client Collection

### Import into Postman

Create a new collection with these requests:

**1. Login**
- Method: POST
- URL: `http://localhost:8000/api/token/`
- Body (JSON):
  ```json
  {
      "username": "admin",
      "password": "admin123"
  }
  ```

**2. Refresh Token**
- Method: POST
- URL: `http://localhost:8000/api/token/refresh/`
- Body (JSON):
  ```json
  {
      "refresh": "{{refresh_token}}"
  }
  ```

**3. Verify Token**
- Method: POST
- URL: `http://localhost:8000/api/token/verify/`
- Body (JSON):
  ```json
  {
      "token": "{{access_token}}"
  }
  ```

**4. Get Profiles (Protected)**
- Method: GET
- URL: `http://localhost:8000/api/profiles/`
- Headers:
  - Authorization: `Bearer {{access_token}}`

**5. Get Current User**
- Method: GET
- URL: `http://localhost:8000/api/users/me/`
- Headers:
  - Authorization: `Bearer {{access_token}}`

---

## Expected Behavior Summary

| Test | Endpoint | Method | Auth Required | Expected Status |
|------|----------|--------|---------------|-----------------|
| Login | `/api/token/` | POST | No | 200 OK |
| Login Alt | `/api/auth/login/` | POST | No | 200 OK |
| Refresh | `/api/token/refresh/` | POST | No | 200 OK |
| Refresh Alt | `/api/auth/refresh/` | POST | No | 200 OK |
| Verify | `/api/token/verify/` | POST | No | 200 OK |
| Verify Alt | `/api/auth/verify/` | POST | No | 200 OK |
| Profiles | `/api/profiles/` | GET | Yes | 200 OK |
| Current User | `/api/users/me/` | GET | Yes | 200 OK |
| Register | `/api/register/` | POST | No | 201 Created |
| Change Password | `/api/users/change-password/` | PUT | Yes | 200 OK |

---

## Troubleshooting

### Issue: "No active account found"
**Solution:** Verify username and password, check user is active

### Issue: "Authentication credentials were not provided"
**Solution:** Add `Authorization: Bearer <token>` header

### Issue: "Token is invalid or expired"
**Solution:** Use refresh token to get new access token

### Issue: "Token is blacklisted"
**Solution:** Login again to get new token pair

---

**Last Updated:** October 14, 2025  
**Version:** 1.0
