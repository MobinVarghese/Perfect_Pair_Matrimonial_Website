# Export Logs Feature - Testing Guide

## Overview
The Export Logs feature allows admins to export user data in PDF or Excel format and track all export operations.

---

## ✅ Feature Status: **FULLY IMPLEMENTED**

### Backend Implementation
- ✅ `ExportLogViewSet` - View and manage export history
- ✅ PDF Export using ReportLab
- ✅ Excel Export using Pandas & OpenPyXL
- ✅ Export logging system
- ✅ Admin-only permissions

### Frontend Implementation
- ✅ Admin Dashboard with Exports tab
- ✅ Export buttons (PDF & Excel)
- ✅ Export history display
- ✅ Loading states & notifications

---

## 📋 How to Test Export Logs

### Step 1: Login as Admin

1. Open browser and go to: **http://localhost:3000/login**
2. Login with admin credentials:
   ```
   Username: adminuser
   Password: admin123
   ```
3. You'll be redirected to the home page

### Step 2: Access Admin Dashboard

1. Navigate to: **http://localhost:3000/admin**
2. Or click on your profile menu and select "Admin Dashboard" (if available)
3. You should see the admin dashboard with three tabs:
   - Users
   - Reports
   - **Exports** ← Click this tab

### Step 3: Test Export Functionality

#### A. Export to PDF

1. Click the **"Export to PDF"** button (red/pink gradient)
2. You should see:
   - ✅ Loading spinner appears
   - ✅ PDF file downloads automatically
   - ✅ Success notification: "PDF exported successfully!"
   - ✅ Export history table updates with new entry

**Expected PDF Output:**
- File name: `profiles_YYYYMMDD_HHMMSS.pdf`
- Contains: User profiles in a formatted table
- Includes: Name, Gender, Age, Location, Education, Occupation

#### B. Export to Excel

1. Click the **"Export to Excel"** button (green gradient)
2. You should see:
   - ✅ Loading spinner appears
   - ✅ Excel file (.xlsx) downloads automatically
   - ✅ Success notification: "Excel exported successfully!"
   - ✅ Export history table updates with new entry

**Expected Excel Output:**
- File name: `profiles_YYYYMMDD_HHMMSS.xlsx`
- Contains: User profiles in spreadsheet format
- Columns: Username, First Name, Last Name, Email, Gender, Age, Location, Education, Occupation, Mobile

### Step 4: Verify Export History

After exporting, check the **Export History** table:

| Column | Description | Expected Value |
|--------|-------------|----------------|
| **Date** | When export was created | Current date/time |
| **Format** | File type | PDF (red badge) or Excel (green badge) |
| **Records** | Number of profiles exported | Count of profiles (e.g., 24) |
| **Exported By** | Admin username | adminuser |

---

## 🔧 API Endpoints

### 1. Get Export Logs
```http
GET http://127.0.0.1:8000/api/exports/
Authorization: Bearer <access_token>
```

**Expected Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "admin": 92,
      "file_type": "pdf",
      "file_name": "profiles_20251117_110030.pdf",
      "export_type": "profiles",
      "record_count": 24,
      "created_at": "2025-11-17T11:00:30Z"
    }
  ]
}
```

### 2. Export Data (PDF)
```http
POST http://127.0.0.1:8000/api/exports/export-data/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "file_type": "pdf",
  "export_type": "profiles"
}
```

**Expected Response:**
- HTTP 200
- Content-Type: application/pdf
- File downloads automatically

### 3. Export Data (Excel)
```http
POST http://127.0.0.1:8000/api/exports/export-data/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "file_type": "excel",
  "export_type": "profiles"
}
```

**Expected Response:**
- HTTP 200
- Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
- File downloads automatically

---

## 🧪 Manual API Testing with PowerShell

### Test 1: Get Export Logs

```powershell
# First, login to get token
$loginBody = @{
    username = "adminuser"
    password = "admin123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/login/" -Method POST -Body $loginBody -ContentType "application/json"
$token = $loginResponse.access

# Get export logs
$headers = @{
    Authorization = "Bearer $token"
}

$exportLogs = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/exports/" -Method GET -Headers $headers
$exportLogs | ConvertTo-Json -Depth 5
```

### Test 2: Export to PDF

```powershell
# Login and get token (same as above)
$loginBody = @{
    username = "adminuser"
    password = "admin123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/login/" -Method POST -Body $loginBody -ContentType "application/json"
$token = $loginResponse.access

# Export to PDF
$headers = @{
    Authorization = "Bearer $token"
}

$exportBody = @{
    file_type = "pdf"
    export_type = "profiles"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/exports/export-data/" -Method POST -Headers $headers -Body $exportBody -ContentType "application/json" -OutFile "profiles_export.pdf"

Write-Host "PDF exported successfully to: profiles_export.pdf"
```

### Test 3: Export to Excel

```powershell
# Login and get token
$loginBody = @{
    username = "adminuser"
    password = "admin123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/login/" -Method POST -Body $loginBody -ContentType "application/json"
$token = $loginResponse.access

# Export to Excel
$headers = @{
    Authorization = "Bearer $token"
}

$exportBody = @{
    file_type = "excel"
    export_type = "profiles"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/exports/export-data/" -Method POST -Headers $headers -Body $exportBody -ContentType "application/json" -OutFile "profiles_export.xlsx"

Write-Host "Excel exported successfully to: profiles_export.xlsx"
```

---

## ✅ Verification Checklist

### Frontend Checks
- [ ] Admin dashboard loads without errors
- [ ] Exports tab is visible and clickable
- [ ] Export buttons are properly styled and responsive
- [ ] Loading spinner appears during export
- [ ] Success notification shows after export
- [ ] Export history table displays correctly
- [ ] Export history updates after each export
- [ ] Date formatting is correct
- [ ] Format badges (PDF/Excel) display correctly

### Backend Checks
- [ ] Export logs endpoint returns data
- [ ] PDF export generates valid PDF file
- [ ] Excel export generates valid .xlsx file
- [ ] Export log entry is created in database
- [ ] Record count is accurate
- [ ] File name includes timestamp
- [ ] Only admins can access export endpoints
- [ ] Non-admin users get 403 Forbidden

### Database Checks
Run this to verify export logs in database:

```powershell
cd D:\Matrimonial_Site\backend
.\venv\Scripts\Activate.ps1
python manage.py shell
```

Then in Python shell:
```python
from users.models import ExportLog

# View all export logs
logs = ExportLog.objects.all()
for log in logs:
    print(f"ID: {log.id}, Type: {log.file_type}, Records: {log.record_count}, Admin: {log.admin.username}, Date: {log.created_at}")

# Count total exports
print(f"\nTotal exports: {logs.count()}")
```

---

## 🐛 Troubleshooting

### Issue 1: "Export buttons not working"

**Solution:**
1. Check browser console for JavaScript errors (F12)
2. Verify both servers are running:
   - Backend: http://127.0.0.1:8000/
   - Frontend: http://localhost:3000/
3. Ensure you're logged in as admin

### Issue 2: "403 Forbidden error"

**Solution:**
1. Verify you're logged in with admin account
2. Check token is valid:
   ```javascript
   console.log(localStorage.getItem('access_token'))
   ```
3. Re-login if token expired

### Issue 3: "PDF/Excel not downloading"

**Solution:**
1. Check browser download settings
2. Allow pop-ups for localhost:3000
3. Check browser's download folder
4. Try right-click → Save As on export button

### Issue 4: "Export history empty"

**Solution:**
1. Click export buttons to create exports first
2. Refresh the page
3. Check network tab (F12) for API responses
4. Verify backend endpoint: http://127.0.0.1:8000/api/exports/

---

## 📊 Expected Test Results

### Successful Export Flow:

1. **Before Export:**
   - Export history table shows existing exports (or empty)
   - Export buttons are enabled
   - No loading indicators

2. **During Export:**
   - Loading spinner appears on clicked button
   - Button is disabled temporarily
   - No errors in console

3. **After Export:**
   - File downloads to browser's download folder
   - Success notification appears
   - Export history table updates with new row
   - New entry shows:
     - Current date/time
     - Correct format badge (PDF or Excel)
     - Record count (number of profiles)
     - Admin username
   - Button re-enables
   - Loading spinner disappears

---

## 🎯 Testing Scenarios

### Scenario 1: First-time Export
- Navigate to Exports tab
- Table should be empty or show "No export history found"
- Click "Export to PDF"
- Wait for download
- Table should now show 1 entry

### Scenario 2: Multiple Exports
- Export to PDF (1st export)
- Export to Excel (2nd export)
- Export to PDF again (3rd export)
- Table should show 3 entries in chronological order
- Most recent at the top

### Scenario 3: File Validation
- Open downloaded PDF
- Should display profile data in table format
- Should be readable and properly formatted
- Open downloaded Excel
- Should open in Excel/LibreOffice
- Should contain profile data in columns
- Should have proper headers

---

## 🔐 Security Notes

1. **Admin-Only Access:**
   - Only users with `is_staff=True` or `is_admin=True` can access exports
   - Regular users get 403 Forbidden

2. **Authentication Required:**
   - Must be logged in with valid JWT token
   - Expired tokens are rejected

3. **Audit Trail:**
   - All exports are logged with:
     - Admin user who performed export
     - Timestamp
     - Export type and format
     - Record count

---

## 📝 Summary

**Feature Status:** ✅ **FULLY FUNCTIONAL**

The export logs feature is complete and working. Follow the steps above to test:

1. Login as admin: `adminuser` / `admin123`
2. Go to: http://localhost:3000/admin
3. Click "Exports" tab
4. Click "Export to PDF" or "Export to Excel"
5. Verify file downloads
6. Check export history table updates

**Expected Outcome:** Files download successfully, and export history is tracked in the database and displayed in the admin dashboard.

---

**Last Updated:** November 17, 2025
**Status:** Working and tested
**Version:** 1.0
