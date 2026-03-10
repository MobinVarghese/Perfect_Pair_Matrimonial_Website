# Export Functionality Documentation
## PDF & Excel Export for Admin Users

**Created:** October 14, 2025  
**Status:** ✅ FULLY IMPLEMENTED

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [API Endpoints](#api-endpoints)
4. [ExportLog Model](#exportlog-model)
5. [Implementation Details](#implementation-details)
6. [Usage Examples](#usage-examples)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The export functionality allows **admin users only** to export user data in PDF or Excel format. This feature uses:

- **reportlab** - PDF generation with professional formatting
- **pandas** - Data processing and structuring
- **openpyxl** - Excel file generation with styling

### Key Features

✅ **Admin-Only Access** - Only users with `is_admin=True` can export  
✅ **PDF Export** - Professional PDF reports with tables and formatting  
✅ **Excel Export** - Structured Excel files with auto-sized columns  
✅ **Date Range Filtering** - Export data within specific date ranges  
✅ **Export Logging** - All exports are tracked in `ExportLog` model  
✅ **Multiple Export Types** - Profiles, Users, Reports, Interests

---

## Features

### 1. Export Types Supported

| Export Type | Description | Records Exported |
|------------|-------------|------------------|
| `profiles` | User profiles | Name, gender, age, location, occupation, mobile |
| `users` | User accounts | Username, email, admin status, join date |
| `reports` | User reports | Reporter, reported user, reason, status |
| `interests` | Interest requests | Sender, receiver, status, message |

### 2. File Formats

#### PDF Export
- Professional table layout
- Color-coded headers
- Metadata (generation time, record count)
- Page formatting with margins
- Auto-wrapped text

#### Excel Export
- Structured data in sheets
- Auto-sized columns
- Styled header row (blue background, white text)
- Date formatting
- Easy to import/analyze

### 3. Filtering Options

- **Date Range:** Export only records created within specified dates
- **date_from:** Start date (inclusive)
- **date_to:** End date (inclusive)

### 4. Export Tracking

Every export creates an `ExportLog` entry recording:
- Admin who performed export
- File type (PDF/Excel)
- Export type (profiles/users/reports/interests)
- File name
- Record count
- Timestamp

---

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### 1. Export Profiles as PDF

#### Endpoint
```
POST /api/export/profiles/pdf/
```

#### Permission
**Admin Only** (`IsAdminUser`)

#### Request Headers
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

#### Request Body (Optional)
```json
{
    "date_from": "2025-01-01",
    "date_to": "2025-10-14"
}
```

#### Response
**Content-Type:** `application/pdf`  
**Content-Disposition:** `attachment; filename="profiles_20251014_103000.pdf"`

Downloads PDF file directly.

---

### 2. Export Profiles as Excel

#### Endpoint
```
POST /api/export/profiles/excel/
```

#### Permission
**Admin Only** (`IsAdminUser`)

#### Request Headers
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

#### Request Body (Optional)
```json
{
    "date_from": "2025-01-01",
    "date_to": "2025-10-14"
}
```

#### Response
**Content-Type:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`  
**Content-Disposition:** `attachment; filename="profiles_20251014_103000.excel"`

Downloads Excel file directly.

---

### 3. Generic Export Endpoint

#### Endpoint
```
POST /api/export/<export_type>/<file_type>/
```

**Parameters:**
- `export_type`: `users`, `profiles`, `reports`, `interests`
- `file_type`: `pdf`, `excel`

#### Examples
```
POST /api/export/users/pdf/
POST /api/export/reports/excel/
POST /api/export/interests/pdf/
```

---

### 4. View Export Logs

#### Endpoint
```
GET /api/export-logs/
```

#### Permission
**Admin Only** (`IsAdminUser`)

#### Query Parameters
- `admin_id` - Filter by admin user ID
- `file_type` - Filter by file type (pdf/excel)
- `export_type` - Filter by export type (users/profiles/reports/interests)

#### Example
```
GET /api/export-logs/?file_type=pdf&export_type=profiles
```

#### Response
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "admin": "admin",
            "admin_email": "admin@example.com",
            "file_type": "pdf",
            "file_name": "profiles_20251014_103000.pdf",
            "export_type": "profiles",
            "record_count": 150,
            "created_at": "2025-10-14T10:30:00Z"
        }
    ]
}
```

---

## ExportLog Model

### Model Definition

```python
class ExportLog(models.Model):
    """
    Export Log model to track data exports by admins.
    """
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]
    
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='export_logs',
        limit_choices_to={'is_admin': True}
    )
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    file_name = models.CharField(max_length=255)
    export_type = models.CharField(max_length=50)
    record_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `admin` | ForeignKey | Admin who performed export |
| `file_type` | CharField | Type of file (pdf/excel/csv) |
| `file_name` | CharField | Generated file name |
| `export_type` | CharField | Type of data exported |
| `record_count` | PositiveIntegerField | Number of records exported |
| `created_at` | DateTimeField | When export was created |

### Purpose

1. **Audit Trail** - Track who exported what and when
2. **Compliance** - Meet data export regulations
3. **Analytics** - Analyze export patterns
4. **Security** - Monitor admin activities

---

## Implementation Details

### PDF Generation (reportlab)

#### Process Flow

```python
1. Create BytesIO buffer
2. Initialize SimpleDocTemplate (A4 page)
3. Add title and metadata
4. Prepare table data from queryset
5. Create Table with TableStyle
   - Blue header background (#1a237e)
   - White header text
   - Beige alternating rows
   - Borders and grid lines
6. Build PDF document
7. Return as HTTP response
```

#### Table Styling

```python
TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),  # Header
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
])
```

#### Profiles PDF Structure

| Column | Data |
|--------|------|
| Name | First 20 characters |
| Gender | male/female/other |
| Age | Numeric age |
| Location | First 25 characters |
| Occupation | First 20 characters |
| Mobile | Full mobile number |

---

### Excel Generation (pandas + openpyxl)

#### Process Flow

```python
1. Prepare data list from queryset
2. Create pandas DataFrame
3. Create BytesIO buffer
4. Initialize ExcelWriter with openpyxl engine
5. Write DataFrame to Excel
6. Auto-adjust column widths
7. Style header row
   - Blue background (#1a237e)
   - White bold font
   - Center alignment
8. Return as HTTP response
```

#### Column Auto-Sizing

```python
for column in worksheet.columns:
    max_length = max(len(str(cell.value)) for cell in column)
    adjusted_width = min(max_length + 2, 50)  # Max 50 chars
    worksheet.column_dimensions[column_letter].width = adjusted_width
```

#### Profiles Excel Columns

| Column | Description |
|--------|-------------|
| ID | Profile ID |
| Name | Full name |
| Username | User's username |
| Gender | Gender choice |
| Age | Age in years |
| Location | Full location |
| Occupation | Occupation field |
| Education | Education field |
| Height | Height in feet |
| Mobile | Mobile number |
| Created | Creation timestamp |

---

## Usage Examples

### 1. Export Profiles as PDF (cURL)

```bash
curl -X POST http://localhost:8000/api/export/profiles/pdf/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"date_from":"2025-01-01","date_to":"2025-10-14"}' \
  --output profiles_export.pdf
```

### 2. Export Profiles as Excel (cURL)

```bash
curl -X POST http://localhost:8000/api/export/profiles/excel/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"date_from":"2025-01-01","date_to":"2025-10-14"}' \
  --output profiles_export.xlsx
```

### 3. Export Users as PDF (Python)

```python
import requests

BASE_URL = "http://localhost:8000"

# Login as admin
response = requests.post(
    f"{BASE_URL}/api/token/",
    json={"username": "admin", "password": "admin123"}
)
access_token = response.json()["access"]

# Export users as PDF
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.post(
    f"{BASE_URL}/api/export/users/pdf/",
    headers=headers,
    json={"date_from": "2025-01-01", "date_to": "2025-10-14"}
)

# Save PDF file
with open("users_export.pdf", "wb") as f:
    f.write(response.content)

print("PDF exported successfully!")
```

### 4. Export Reports as Excel (Python)

```python
import requests

BASE_URL = "http://localhost:8000"
access_token = "<your_admin_token>"

headers = {"Authorization": f"Bearer {access_token}"}
response = requests.post(
    f"{BASE_URL}/api/export/reports/excel/",
    headers=headers,
    json={}  # No date filter - export all
)

# Save Excel file
with open("reports_export.xlsx", "wb") as f:
    f.write(response.content)

print("Excel exported successfully!")
```

### 5. View Export Logs (JavaScript/Axios)

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';
const accessToken = '<your_admin_token>';

const api = axios.create({
    baseURL: BASE_URL,
    headers: { Authorization: `Bearer ${accessToken}` }
});

// Get all export logs
const response = await api.get('/api/export-logs/');
console.log('Export Logs:', response.data.results);

// Filter by PDF exports
const pdfExports = await api.get('/api/export-logs/?file_type=pdf');
console.log('PDF Exports:', pdfExports.data.results);
```

### 6. Download Export (React)

```javascript
import axios from 'axios';

const exportProfilesPDF = async () => {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await axios.post(
            'http://localhost:8000/api/export/profiles/pdf/',
            {
                date_from: '2025-01-01',
                date_to: '2025-10-14'
            },
            {
                headers: { Authorization: `Bearer ${token}` },
                responseType: 'blob'  // Important for file download
            }
        );
        
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'profiles_export.pdf');
        document.body.appendChild(link);
        link.click();
        link.remove();
        
        console.log('PDF downloaded successfully!');
    } catch (error) {
        console.error('Export failed:', error);
    }
};

// Usage in component
<button onClick={exportProfilesPDF}>
    Export Profiles as PDF
</button>
```

---

## Testing

### Prerequisites

1. **Create Admin User:**
   ```bash
   cd d:\Matrimonial_Site\backend
   python manage.py createsuperuser
   ```
   - Username: `admin`
   - Password: `admin123`

2. **Create Test Data:**
   ```bash
   python manage.py shell
   ```
   ```python
   from users.models import User, Profile
   
   # Create test user
   user = User.objects.create_user(
       username='testuser',
       email='test@example.com',
       password='test123'
   )
   
   # Create test profile
   Profile.objects.create(
       user=user,
       name='Test User',
       gender='male',
       age=28,
       location='Mumbai, India',
       occupation='Engineer',
       mobile_number='+919876543210'
   )
   ```

### Test Cases

#### Test 1: Export Profiles as PDF

```bash
# 1. Login as admin
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Save access token

# 2. Export profiles
curl -X POST http://localhost:8000/api/export/profiles/pdf/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  --output test_profiles.pdf

# 3. Verify PDF created
ls -la test_profiles.pdf
```

**Expected Result:** PDF file downloaded successfully

---

#### Test 2: Export Profiles as Excel

```bash
curl -X POST http://localhost:8000/api/export/profiles/excel/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  --output test_profiles.xlsx

# Verify Excel file
ls -la test_profiles.xlsx
```

**Expected Result:** Excel file downloaded successfully

---

#### Test 3: Non-Admin Access (Should Fail)

```bash
# Login as regular user
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}'

# Try to export (should fail with 403)
curl -X POST http://localhost:8000/api/export/profiles/pdf/ \
  -H "Authorization: Bearer <non_admin_token>"
```

**Expected Result:** 403 Forbidden

---

#### Test 4: Date Range Filtering

```bash
curl -X POST http://localhost:8000/api/export/profiles/pdf/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "date_from": "2025-01-01",
    "date_to": "2025-10-14"
  }' \
  --output filtered_profiles.pdf
```

**Expected Result:** PDF with only profiles created in date range

---

#### Test 5: View Export Logs

```bash
curl -X GET http://localhost:8000/api/export-logs/ \
  -H "Authorization: Bearer <admin_token>"
```

**Expected Response:**
```json
{
    "count": 1,
    "results": [
        {
            "id": 1,
            "admin": "admin",
            "file_type": "pdf",
            "file_name": "profiles_20251014_103000.pdf",
            "export_type": "profiles",
            "record_count": 5,
            "created_at": "2025-10-14T10:30:00Z"
        }
    ]
}
```

---

### Python Testing Script

Save as `test_export.py`:

```python
import requests
import os

BASE_URL = "http://localhost:8000"

def test_export_functionality():
    print("=== Export Functionality Tests ===\n")
    
    # Test 1: Login as admin
    print("Test 1: Login as admin...")
    response = requests.post(
        f"{BASE_URL}/api/token/",
        json={"username": "admin", "password": "admin123"}
    )
    
    if response.status_code == 200:
        print("✓ Admin login successful")
        access_token = response.json()["access"]
    else:
        print("✗ Admin login failed")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test 2: Export profiles as PDF
    print("\nTest 2: Export profiles as PDF...")
    response = requests.post(
        f"{BASE_URL}/api/export/profiles/pdf/",
        headers=headers,
        json={}
    )
    
    if response.status_code == 200:
        with open("test_profiles.pdf", "wb") as f:
            f.write(response.content)
        file_size = os.path.getsize("test_profiles.pdf")
        print(f"✓ PDF exported successfully ({file_size} bytes)")
    else:
        print(f"✗ PDF export failed: {response.status_code}")
    
    # Test 3: Export profiles as Excel
    print("\nTest 3: Export profiles as Excel...")
    response = requests.post(
        f"{BASE_URL}/api/export/profiles/excel/",
        headers=headers,
        json={}
    )
    
    if response.status_code == 200:
        with open("test_profiles.xlsx", "wb") as f:
            f.write(response.content)
        file_size = os.path.getsize("test_profiles.xlsx")
        print(f"✓ Excel exported successfully ({file_size} bytes)")
    else:
        print(f"✗ Excel export failed: {response.status_code}")
    
    # Test 4: View export logs
    print("\nTest 4: View export logs...")
    response = requests.get(
        f"{BASE_URL}/api/export-logs/",
        headers=headers
    )
    
    if response.status_code == 200:
        logs = response.json()
        print(f"✓ Export logs retrieved: {logs['count']} entries")
        for log in logs['results'][:3]:
            print(f"  - {log['file_name']} ({log['record_count']} records)")
    else:
        print(f"✗ Failed to retrieve logs: {response.status_code}")
    
    print("\n=== Tests Complete ===")

if __name__ == "__main__":
    test_export_functionality()
```

**Run:**
```bash
cd d:\Matrimonial_Site\backend
python test_export.py
```

---

## Troubleshooting

### Issue 1: "You do not have permission to perform this action"

**Cause:** User is not an admin  
**Solution:** Ensure user has `is_admin=True`

```python
# In Django shell
from users.models import User
user = User.objects.get(username='admin')
user.is_admin = True
user.save()
```

---

### Issue 2: PDF Download Fails / Corrupt File

**Cause:** Missing `responseType: 'blob'` in frontend request  
**Solution:** Add responseType to axios request

```javascript
axios.post(url, data, {
    headers: { Authorization: `Bearer ${token}` },
    responseType: 'blob'  // Important!
})
```

---

### Issue 3: Excel File Won't Open

**Cause:** Incorrect content-type in response  
**Solution:** Backend automatically sets correct content-type

```python
# Already handled in code
content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
```

---

### Issue 4: "No records found" / Empty Export

**Cause:** Date filter too restrictive or no data  
**Solution:** 
1. Check data exists: `Profile.objects.count()`
2. Remove date filters
3. Adjust date range

---

### Issue 5: PDF Formatting Issues

**Cause:** Text too long for table cells  
**Solution:** Text is automatically truncated in code

```python
profile.name[:20]  # First 20 characters
profile.location[:25]  # First 25 characters
```

---

### Issue 6: Memory Issues with Large Exports

**Cause:** Too many records  
**Solution:** 
1. Use date range filtering
2. Export in batches
3. Add pagination to export

---

## Summary

### ✅ What's Implemented

1. **PDF Export** - Using reportlab with professional formatting
2. **Excel Export** - Using pandas and openpyxl with styling
3. **Admin-Only Access** - Protected by `IsAdminUser` permission
4. **ExportLog Model** - Tracks all export activity
5. **Date Range Filtering** - Export specific time periods
6. **Multiple Export Types** - Profiles, Users, Reports, Interests
7. **Comprehensive API** - RESTful endpoints with full CRUD

### 📊 Export Statistics

- **Export Types:** 4 (profiles, users, reports, interests)
- **File Formats:** 2 (PDF, Excel)
- **Endpoints:** 3 main + 1 generic + 1 logs view
- **Permission:** Admin only (`IsAdminUser`)
- **Logging:** Every export logged in database

### 🔐 Security Features

- ✅ Admin-only access enforced
- ✅ JWT authentication required
- ✅ Export activity tracked
- ✅ Audit trail in ExportLog
- ✅ No direct file storage (memory buffer)

---

**Last Updated:** October 14, 2025  
**Version:** 1.0  
**Status:** ✅ PRODUCTION READY
