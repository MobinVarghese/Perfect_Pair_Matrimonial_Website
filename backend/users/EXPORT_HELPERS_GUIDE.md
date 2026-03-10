# Export Helper Functions Guide

## Overview

This guide covers the use of reusable export helper functions located in `users/export_utils.py`. These functions provide a clean, maintainable way to export profile data to PDF, Excel, and CSV formats.

## Available Functions

### 1. `export_profiles_to_pdf()`

Generates a professionally formatted PDF document with profile data using reportlab.

**Signature:**
```python
def export_profiles_to_pdf(profiles_queryset, title="User Profiles Export", filters=None)
```

**Parameters:**
- `profiles_queryset` (QuerySet): Django QuerySet of Profile objects to export
- `title` (str, optional): Document title. Default: "User Profiles Export"
- `filters` (dict, optional): Dictionary of applied filters to display in metadata

**Returns:**
- `HttpResponse` object with PDF file as downloadable attachment

**Features:**
- Professional table layout with colored headers (navy blue #1a237e)
- Alternating row colors (beige/light grey) for readability
- Document metadata (generation time, record count, filters)
- Auto-paginated for large datasets
- Footer with confidentiality notice
- Responsive column widths

**PDF Styling:**
- **Page Size:** A4
- **Margins:** 30 points on all sides
- **Header:** Bold navy blue text
- **Data Rows:** Alternating beige and light grey backgrounds
- **Grid:** Black borders with navy blue outer box
- **Font:** Helvetica (9-10pt for data, 24pt for title)

---

### 2. `export_profiles_to_excel()`

Generates a formatted Excel spreadsheet with profile data using pandas and openpyxl.

**Signature:**
```python
def export_profiles_to_excel(profiles_queryset, sheet_name="Profiles", filters=None)
```

**Parameters:**
- `profiles_queryset` (QuerySet): Django QuerySet of Profile objects to export
- `sheet_name` (str, optional): Excel sheet name. Default: "Profiles"
- `filters` (dict, optional): Dictionary of applied filters to display in metadata

**Returns:**
- `HttpResponse` object with Excel file (.xlsx) as downloadable attachment

**Features:**
- Report title and metadata at the top of the sheet
- Styled header row (navy blue background, white bold text)
- Auto-adjusted column widths (10-50 characters)
- Alternating row colors for readability
- Frozen header row for easy scrolling
- Wrap text in cells for better visibility
- Filter information displayed at top

**Excel Columns:**
1. Profile ID
2. Name
3. Username
4. Email
5. Gender
6. Age
7. Location
8. Occupation
9. Education
10. Height (ft)
11. Mobile Number
12. About (first 100 characters)
13. Desired Partner Traits (first 100 characters)
14. Profile Created
15. Last Updated
16. User Active

---

### 3. `export_profiles_to_csv()`

Generates a simple CSV file with profile data using pandas.

**Signature:**
```python
def export_profiles_to_csv(profiles_queryset, filename_prefix="profiles")
```

**Parameters:**
- `profiles_queryset` (QuerySet): Django QuerySet of Profile objects to export
- `filename_prefix` (str, optional): Prefix for CSV filename. Default: "profiles"

**Returns:**
- `HttpResponse` object with CSV file as downloadable attachment

**Features:**
- Simple, clean CSV format
- UTF-8 encoding
- Timestamp in filename
- Compatible with all spreadsheet software

---

## Usage Examples

### Basic Usage in Django Views

#### Example 1: Simple PDF Export
```python
from django.shortcuts import render
from users.models import Profile
from users.export_utils import export_profiles_to_pdf

def export_all_profiles_pdf(request):
    """Export all profiles to PDF"""
    profiles = Profile.objects.all()
    return export_profiles_to_pdf(profiles)
```

#### Example 2: Filtered Excel Export
```python
from django.shortcuts import render
from users.models import Profile
from users.export_utils import export_profiles_to_excel

def export_female_profiles_excel(request):
    """Export female profiles to Excel"""
    profiles = Profile.objects.filter(gender='female')
    
    filters = {
        'gender': 'female'
    }
    
    return export_profiles_to_excel(
        profiles, 
        sheet_name="Female Profiles",
        filters=filters
    )
```

#### Example 3: Date Range Export with Custom Title
```python
from django.utils import timezone
from datetime import timedelta
from users.models import Profile
from users.export_utils import export_profiles_to_pdf

def export_recent_profiles_pdf(request):
    """Export profiles created in last 30 days"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    profiles = Profile.objects.filter(created_at__gte=thirty_days_ago)
    
    filters = {
        'date_from': thirty_days_ago.strftime('%Y-%m-%d')
    }
    
    return export_profiles_to_pdf(
        profiles,
        title="Recent Profiles (Last 30 Days)",
        filters=filters
    )
```

---

### ViewSet Integration

#### Example: DRF ViewSet with Export Actions

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from users.models import Profile
from users.serializers import ProfileSerializer
from users.export_utils import (
    export_profiles_to_pdf,
    export_profiles_to_excel,
    export_profiles_to_csv
)


class ProfileExportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for profile exports with PDF, Excel, and CSV options.
    Only accessible by admin users.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]
    
    def get_filtered_queryset(self, request):
        """Apply filters from request parameters"""
        queryset = self.get_queryset()
        
        # Filter by gender
        gender = request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)
        
        # Filter by location
        location = request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by age range
        min_age = request.query_params.get('min_age')
        max_age = request.query_params.get('max_age')
        if min_age:
            queryset = queryset.filter(age__gte=int(min_age))
        if max_age:
            queryset = queryset.filter(age__lte=int(max_age))
        
        # Filter by date range
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        return queryset
    
    def get_filter_dict(self, request):
        """Extract filters from request for metadata"""
        filters = {}
        
        if request.query_params.get('gender'):
            filters['gender'] = request.query_params.get('gender')
        if request.query_params.get('location'):
            filters['location'] = request.query_params.get('location')
        if request.query_params.get('min_age'):
            filters['min_age'] = request.query_params.get('min_age')
        if request.query_params.get('max_age'):
            filters['max_age'] = request.query_params.get('max_age')
        if request.query_params.get('date_from'):
            filters['date_from'] = request.query_params.get('date_from')
        if request.query_params.get('date_to'):
            filters['date_to'] = request.query_params.get('date_to')
        
        return filters
    
    @action(detail=False, methods=['get'], url_path='pdf')
    def export_pdf(self, request):
        """
        Export profiles to PDF
        
        Query Parameters:
        - gender: Filter by gender (male/female)
        - location: Filter by location (case-insensitive)
        - min_age: Minimum age
        - max_age: Maximum age
        - date_from: Start date (YYYY-MM-DD)
        - date_to: End date (YYYY-MM-DD)
        """
        profiles = self.get_filtered_queryset(request)
        filters = self.get_filter_dict(request)
        
        # Get custom title from query params
        title = request.query_params.get('title', 'User Profiles Export')
        
        return export_profiles_to_pdf(profiles, title=title, filters=filters)
    
    @action(detail=False, methods=['get'], url_path='excel')
    def export_excel(self, request):
        """
        Export profiles to Excel
        
        Query Parameters: Same as PDF export
        """
        profiles = self.get_filtered_queryset(request)
        filters = self.get_filter_dict(request)
        
        # Get custom sheet name from query params
        sheet_name = request.query_params.get('sheet_name', 'Profiles')
        
        return export_profiles_to_excel(profiles, sheet_name=sheet_name, filters=filters)
    
    @action(detail=False, methods=['get'], url_path='csv')
    def export_csv(self, request):
        """
        Export profiles to CSV
        
        Query Parameters: Same as PDF export
        """
        profiles = self.get_filtered_queryset(request)
        
        return export_profiles_to_csv(profiles)
```

**URL Configuration:**
```python
# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import ProfileExportViewSet

router = DefaultRouter()
router.register(r'profile-exports', ProfileExportViewSet, basename='profile-export')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

---

## API Endpoints

### PDF Export
```
GET /api/profile-exports/pdf/
```

**Query Parameters:**
- `gender` - Filter by gender (male/female)
- `location` - Filter by location (partial match)
- `min_age` - Minimum age
- `max_age` - Maximum age
- `date_from` - Start date (YYYY-MM-DD)
- `date_to` - End date (YYYY-MM-DD)
- `title` - Custom PDF title

**Example Requests:**
```bash
# Export all profiles
curl -X GET "http://localhost:8000/api/profile-exports/pdf/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Export female profiles from Mumbai
curl -X GET "http://localhost:8000/api/profile-exports/pdf/?gender=female&location=Mumbai" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Export profiles with age range
curl -X GET "http://localhost:8000/api/profile-exports/pdf/?min_age=25&max_age=35" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Export with custom title
curl -X GET "http://localhost:8000/api/profile-exports/pdf/?title=Premium%20Profiles%20Report" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### Excel Export
```
GET /api/profile-exports/excel/
```

**Query Parameters:** Same as PDF export, plus:
- `sheet_name` - Custom Excel sheet name

**Example Requests:**
```bash
# Export all profiles
curl -X GET "http://localhost:8000/api/profile-exports/excel/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Export with custom sheet name
curl -X GET "http://localhost:8000/api/profile-exports/excel/?sheet_name=Active%20Profiles" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Export profiles created in date range
curl -X GET "http://localhost:8000/api/profile-exports/excel/?date_from=2025-01-01&date_to=2025-12-31" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### CSV Export
```
GET /api/profile-exports/csv/
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/profile-exports/csv/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -o profiles.csv
```

---

## Advanced Usage Patterns

### 1. Export with Logging

```python
from users.models import Profile, ExportLog
from users.export_utils import export_profiles_to_pdf

def export_with_logging(request, export_type='pdf'):
    """Export profiles and log the activity"""
    profiles = Profile.objects.all()
    record_count = profiles.count()
    
    # Generate filename
    filename = f"profiles_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{export_type}"
    
    # Create export log
    export_log = ExportLog.objects.create(
        admin=request.user,
        file_type=export_type,
        file_name=filename,
        export_type='profiles',
        record_count=record_count
    )
    
    # Generate export
    if export_type == 'pdf':
        response = export_profiles_to_pdf(profiles)
    elif export_type == 'excel':
        response = export_profiles_to_excel(profiles)
    else:
        response = export_profiles_to_csv(profiles)
    
    return response
```

### 2. Scheduled Exports with Celery

```python
from celery import shared_task
from django.core.mail import EmailMessage
from users.models import Profile
from users.export_utils import export_profiles_to_excel

@shared_task
def send_weekly_profile_report(admin_email):
    """Send weekly profile report via email"""
    # Get profiles created in last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    profiles = Profile.objects.filter(created_at__gte=seven_days_ago)
    
    # Generate Excel report
    response = export_profiles_to_excel(
        profiles,
        sheet_name="Weekly Report",
        filters={'date_from': seven_days_ago.strftime('%Y-%m-%d')}
    )
    
    # Create email with attachment
    email = EmailMessage(
        subject='Weekly Profile Report',
        body='Please find attached the weekly profile report.',
        from_email='admin@matrimonial.com',
        to=[admin_email]
    )
    
    # Attach Excel file
    email.attach(
        f"weekly_report_{timezone.now().strftime('%Y%m%d')}.xlsx",
        response.content,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    email.send()
```

### 3. Export with Annotations

```python
from django.db.models import Count, Q
from users.models import Profile
from users.export_utils import export_profiles_to_pdf

def export_profiles_with_stats(request):
    """Export profiles with additional statistics"""
    profiles = Profile.objects.annotate(
        interests_sent=Count('interests_sent'),
        interests_received=Count('interests_received'),
        matches_count=Count(
            'interests_sent',
            filter=Q(interests_sent__status='accepted')
        )
    ).select_related('user')
    
    return export_profiles_to_pdf(
        profiles,
        title="Profile Statistics Report"
    )
```

### 4. Multi-Format Export

```python
from django.http import JsonResponse
from users.models import Profile
from users.export_utils import (
    export_profiles_to_pdf,
    export_profiles_to_excel,
    export_profiles_to_csv
)

def export_profiles_multi(request):
    """Export profiles in requested format"""
    export_format = request.GET.get('format', 'pdf').lower()
    profiles = Profile.objects.all()
    
    # Route to appropriate export function
    export_functions = {
        'pdf': export_profiles_to_pdf,
        'excel': export_profiles_to_excel,
        'xlsx': export_profiles_to_excel,
        'csv': export_profiles_to_csv,
    }
    
    export_func = export_functions.get(export_format)
    
    if not export_func:
        return JsonResponse(
            {'error': f'Unsupported format: {export_format}'},
            status=400
        )
    
    return export_func(profiles)
```

---

## Frontend Integration

### JavaScript/React Example

```javascript
// Download PDF export
const exportProfilesPDF = async (filters = {}) => {
  try {
    const token = localStorage.getItem('access_token');
    
    // Build query string
    const params = new URLSearchParams(filters);
    
    const response = await fetch(
      `http://localhost:8000/api/profile-exports/pdf/?${params}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    if (!response.ok) {
      throw new Error('Export failed');
    }
    
    // Get filename from response header
    const contentDisposition = response.headers.get('Content-Disposition');
    const filename = contentDisposition
      ? contentDisposition.split('filename=')[1].replace(/"/g, '')
      : 'profiles_export.pdf';
    
    // Create blob and download
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    
    console.log('PDF downloaded successfully');
  } catch (error) {
    console.error('Export error:', error);
  }
};

// Download Excel export
const exportProfilesExcel = async (filters = {}) => {
  try {
    const token = localStorage.getItem('access_token');
    const params = new URLSearchParams(filters);
    
    const response = await fetch(
      `http://localhost:8000/api/profile-exports/excel/?${params}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    if (!response.ok) {
      throw new Error('Export failed');
    }
    
    const contentDisposition = response.headers.get('Content-Disposition');
    const filename = contentDisposition
      ? contentDisposition.split('filename=')[1].replace(/"/g, '')
      : 'profiles_export.xlsx';
    
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    
    console.log('Excel downloaded successfully');
  } catch (error) {
    console.error('Export error:', error);
  }
};

// Usage examples
exportProfilesPDF({ gender: 'female', location: 'Mumbai' });
exportProfilesExcel({ min_age: 25, max_age: 35 });
```

---

### React Component Example

```jsx
import React, { useState } from 'react';

const ProfileExportComponent = () => {
  const [filters, setFilters] = useState({
    gender: '',
    location: '',
    min_age: '',
    max_age: '',
    date_from: '',
    date_to: ''
  });
  
  const [loading, setLoading] = useState(false);
  
  const handleExport = async (format) => {
    setLoading(true);
    
    try {
      const token = localStorage.getItem('access_token');
      
      // Remove empty filters
      const cleanFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== '')
      );
      
      const params = new URLSearchParams(cleanFilters);
      
      const response = await fetch(
        `http://localhost:8000/api/profile-exports/${format}/?${params}`,
        {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      if (!response.ok) {
        throw new Error('Export failed');
      }
      
      // Download file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `profiles_export.${format === 'excel' ? 'xlsx' : format}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      
      alert(`${format.toUpperCase()} exported successfully!`);
    } catch (error) {
      console.error('Export error:', error);
      alert('Export failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="export-component">
      <h2>Export Profiles</h2>
      
      <div className="filters">
        <label>
          Gender:
          <select
            value={filters.gender}
            onChange={(e) => setFilters({...filters, gender: e.target.value})}
          >
            <option value="">All</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </label>
        
        <label>
          Location:
          <input
            type="text"
            value={filters.location}
            onChange={(e) => setFilters({...filters, location: e.target.value})}
            placeholder="Enter location"
          />
        </label>
        
        <label>
          Min Age:
          <input
            type="number"
            value={filters.min_age}
            onChange={(e) => setFilters({...filters, min_age: e.target.value})}
          />
        </label>
        
        <label>
          Max Age:
          <input
            type="number"
            value={filters.max_age}
            onChange={(e) => setFilters({...filters, max_age: e.target.value})}
          />
        </label>
        
        <label>
          Date From:
          <input
            type="date"
            value={filters.date_from}
            onChange={(e) => setFilters({...filters, date_from: e.target.value})}
          />
        </label>
        
        <label>
          Date To:
          <input
            type="date"
            value={filters.date_to}
            onChange={(e) => setFilters({...filters, date_to: e.target.value})}
          />
        </label>
      </div>
      
      <div className="export-buttons">
        <button
          onClick={() => handleExport('pdf')}
          disabled={loading}
        >
          {loading ? 'Exporting...' : 'Export PDF'}
        </button>
        
        <button
          onClick={() => handleExport('excel')}
          disabled={loading}
        >
          {loading ? 'Exporting...' : 'Export Excel'}
        </button>
        
        <button
          onClick={() => handleExport('csv')}
          disabled={loading}
        >
          {loading ? 'Exporting...' : 'Export CSV'}
        </button>
      </div>
    </div>
  );
};

export default ProfileExportComponent;
```

---

## Testing

### Test Script

```python
# test_export_helpers.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import Profile
from users.export_utils import (
    export_profiles_to_pdf,
    export_profiles_to_excel,
    export_profiles_to_csv
)

def test_pdf_export():
    """Test PDF export"""
    print("Testing PDF export...")
    profiles = Profile.objects.all()[:10]  # Test with 10 profiles
    
    response = export_profiles_to_pdf(profiles, title="Test PDF Export")
    
    # Save to file for inspection
    with open('test_export.pdf', 'wb') as f:
        f.write(response.content)
    
    print(f"✓ PDF generated: {len(response.content)} bytes")
    print(f"✓ Content-Type: {response['Content-Type']}")
    print(f"✓ Saved as: test_export.pdf")

def test_excel_export():
    """Test Excel export"""
    print("\nTesting Excel export...")
    profiles = Profile.objects.all()[:10]
    
    filters = {'gender': 'female', 'location': 'Mumbai'}
    response = export_profiles_to_excel(
        profiles,
        sheet_name="Test Sheet",
        filters=filters
    )
    
    # Save to file for inspection
    with open('test_export.xlsx', 'wb') as f:
        f.write(response.content)
    
    print(f"✓ Excel generated: {len(response.content)} bytes")
    print(f"✓ Content-Type: {response['Content-Type']}")
    print(f"✓ Saved as: test_export.xlsx")

def test_csv_export():
    """Test CSV export"""
    print("\nTesting CSV export...")
    profiles = Profile.objects.all()[:10]
    
    response = export_profiles_to_csv(profiles)
    
    # Save to file for inspection
    with open('test_export.csv', 'wb') as f:
        f.write(response.content)
    
    print(f"✓ CSV generated: {len(response.content)} bytes")
    print(f"✓ Content-Type: {response['Content-Type']}")
    print(f"✓ Saved as: test_export.csv")

if __name__ == '__main__':
    test_pdf_export()
    test_excel_export()
    test_csv_export()
    print("\n✅ All export tests completed!")
```

**Run tests:**
```bash
cd backend
python test_export_helpers.py
```

---

## Performance Considerations

### Large Dataset Handling

For very large datasets (10,000+ records), consider:

1. **Pagination in Queries:**
```python
from django.core.paginator import Paginator

def export_large_dataset_pdf(request):
    profiles = Profile.objects.all()
    
    # Limit to first 5000 records
    profiles = profiles[:5000]
    
    return export_profiles_to_pdf(profiles)
```

2. **Async/Celery Tasks:**
```python
from celery import shared_task

@shared_task
def async_export_profiles(admin_id, filters):
    """Generate export in background"""
    profiles = Profile.objects.filter(**filters)
    response = export_profiles_to_pdf(profiles)
    
    # Save to file storage or send via email
    # ... implementation ...
```

3. **Database Query Optimization:**
```python
def optimized_export(request):
    """Use select_related to reduce queries"""
    profiles = Profile.objects.select_related('user').all()
    return export_profiles_to_excel(profiles)
```

---

## Troubleshooting

### Common Issues

**1. Memory Error with Large Datasets**
- **Solution:** Limit queryset size or use pagination
- **Code:**
  ```python
  profiles = Profile.objects.all()[:1000]  # Limit to 1000
  ```

**2. Unicode Characters Not Displaying**
- **Solution:** Already handled in functions (UTF-8 encoding)
- **Verify:** Check CSV export uses `encoding='utf-8'`

**3. Excel Column Width Issues**
- **Solution:** Adjust max width in `export_profiles_to_excel()`
- **Code:** Change `min(max_length + 2, 50)` to desired max

**4. PDF Page Overflow**
- **Solution:** reportlab auto-paginates, but you can adjust page size
- **Code:**
  ```python
  from reportlab.lib.pagesizes import letter  # Use letter instead of A4
  ```

---

## Best Practices

1. **Always Use Filters:** Provide filter information for better context
2. **Limit Data:** Don't export entire database at once
3. **Add Logging:** Track export activity with ExportLog model
4. **Error Handling:** Wrap exports in try-except blocks
5. **Permission Checks:** Ensure only admins can export
6. **Optimize Queries:** Use select_related/prefetch_related
7. **Cache Results:** For repeated exports, consider caching
8. **Clean Filenames:** Use timestamps and descriptive names
9. **Test Locally:** Always test with sample data first
10. **Monitor Performance:** Track export times and sizes

---

## Summary

The export helper functions provide:

✅ **Reusable** - Call from anywhere in your Django project
✅ **Customizable** - Pass filters and custom titles
✅ **Professional** - High-quality formatting out of the box
✅ **Efficient** - Optimized for performance
✅ **Maintainable** - Single source of truth for export logic
✅ **Flexible** - Support for PDF, Excel, and CSV formats

For more information, see:
- `backend/users/export_utils.py` - Source code
- `EXPORT_FUNCTIONALITY_GUIDE.md` - Complete export documentation
- `test_export_helpers.py` - Test scripts

