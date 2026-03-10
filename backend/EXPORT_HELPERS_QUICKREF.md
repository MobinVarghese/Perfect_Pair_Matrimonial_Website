# Export Helper Functions - Quick Reference

## 🚀 Quick Start

### Import Functions
```python
from users.export_utils import (
    export_profiles_to_pdf,
    export_profiles_to_excel,
    export_profiles_to_csv
)
```

---

## 📋 Function Signatures

### PDF Export
```python
export_profiles_to_pdf(
    profiles_queryset,              # Required: QuerySet of Profile objects
    title="User Profiles Export",   # Optional: PDF title
    filters=None                    # Optional: Dict of applied filters
)
# Returns: HttpResponse with PDF attachment
```

### Excel Export
```python
export_profiles_to_excel(
    profiles_queryset,              # Required: QuerySet of Profile objects
    sheet_name="Profiles",          # Optional: Excel sheet name
    filters=None                    # Optional: Dict of applied filters
)
# Returns: HttpResponse with Excel (.xlsx) attachment
```

### CSV Export
```python
export_profiles_to_csv(
    profiles_queryset,              # Required: QuerySet of Profile objects
    filename_prefix="profiles"      # Optional: Filename prefix
)
# Returns: HttpResponse with CSV attachment
```

---

## 💡 Common Use Cases

### 1. Export All Profiles
```python
from users.models import Profile

profiles = Profile.objects.all()
return export_profiles_to_pdf(profiles)
```

### 2. Export with Filters
```python
profiles = Profile.objects.filter(gender='female', location='Mumbai')
filters = {'gender': 'female', 'location': 'Mumbai'}

return export_profiles_to_excel(profiles, filters=filters)
```

### 3. Export with Custom Title
```python
profiles = Profile.objects.filter(age__gte=25, age__lte=35)

return export_profiles_to_pdf(
    profiles,
    title="Profiles Age 25-35"
)
```

### 4. Export Date Range
```python
from django.utils import timezone
from datetime import timedelta

thirty_days_ago = timezone.now() - timedelta(days=30)
profiles = Profile.objects.filter(created_at__gte=thirty_days_ago)

filters = {'date_from': thirty_days_ago.strftime('%Y-%m-%d')}

return export_profiles_to_pdf(profiles, filters=filters)
```

---

## 🔌 ViewSet Integration

### Basic ViewSet
```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

class ProfileExportViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def pdf(self, request):
        profiles = Profile.objects.all()
        return export_profiles_to_pdf(profiles)
    
    @action(detail=False, methods=['get'])
    def excel(self, request):
        profiles = Profile.objects.all()
        return export_profiles_to_excel(profiles)
```

### With Query Parameters
```python
@action(detail=False, methods=['get'])
def pdf(self, request):
    profiles = Profile.objects.all()
    
    # Apply filters from query params
    gender = request.query_params.get('gender')
    if gender:
        profiles = profiles.filter(gender=gender)
    
    location = request.query_params.get('location')
    if location:
        profiles = profiles.filter(location__icontains=location)
    
    # Build filters dict
    filters = {}
    if gender:
        filters['gender'] = gender
    if location:
        filters['location'] = location
    
    return export_profiles_to_pdf(profiles, filters=filters)
```

---

## 🌐 API Endpoints

### URL Configuration
```python
# users/urls.py
from rest_framework.routers import DefaultRouter
from .views import ProfileExportViewSet

router = DefaultRouter()
router.register(r'profile-exports', ProfileExportViewSet, basename='profile-export')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### Generated URLs
```
GET /api/profile-exports/pdf/
GET /api/profile-exports/excel/
GET /api/profile-exports/csv/
```

### cURL Examples
```bash
# Export all profiles to PDF
curl -X GET "http://localhost:8000/api/profile-exports/pdf/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o profiles.pdf

# Export with filters
curl -X GET "http://localhost:8000/api/profile-exports/excel/?gender=female&location=Mumbai" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o profiles.xlsx
```

---

## 🎨 Customization

### PDF Styling
Modify in `export_utils.py`:
```python
# Change page size
from reportlab.lib.pagesizes import letter
doc = SimpleDocTemplate(buffer, pagesize=letter, ...)

# Change colors
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF0000')),  # Red header
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
]))

# Change title style
title_style = ParagraphStyle(
    'CustomTitle',
    fontSize=28,  # Larger title
    textColor=colors.HexColor('#000000'),  # Black text
)
```

### Excel Styling
```python
# Change column width limits
adjusted_width = min(max(max_length + 2, 15), 60)  # Min 15, max 60

# Change header colors
header_fill = PatternFill(
    start_color='FF0000',  # Red background
    end_color='FF0000',
    fill_type='solid'
)
```

---

## 🧪 Testing

### Run Tests
```bash
cd backend
python test_export_helpers.py
```

### Test Individual Functions
```python
# test_manual.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import Profile
from users.export_utils import export_profiles_to_pdf

# Test
profiles = Profile.objects.all()[:10]
response = export_profiles_to_pdf(profiles)

# Save to file
with open('test.pdf', 'wb') as f:
    f.write(response.content)

print(f"PDF saved: {len(response.content)} bytes")
```

---

## ⚡ Performance Tips

### 1. Limit Queryset Size
```python
profiles = Profile.objects.all()[:1000]  # Max 1000 records
```

### 2. Use select_related()
```python
profiles = Profile.objects.select_related('user').all()
```

### 3. Add Pagination
```python
from django.core.paginator import Paginator

paginator = Paginator(Profile.objects.all(), 500)
page = paginator.get_page(1)
return export_profiles_to_pdf(page.object_list)
```

---

## 📊 Output Formats

### PDF Features
- ✅ Professional table layout
- ✅ Navy blue headers
- ✅ Alternating row colors
- ✅ Auto-pagination
- ✅ Document metadata
- ✅ A4 page size

### Excel Features
- ✅ Styled header row
- ✅ Auto-sized columns
- ✅ Frozen header
- ✅ Report metadata
- ✅ Alternating rows
- ✅ 16 detailed columns

### CSV Features
- ✅ Simple format
- ✅ UTF-8 encoding
- ✅ Universal compatibility

---

## 🔍 Filter Options

### Supported Filters
```python
filters = {
    'gender': 'female',              # Gender filter
    'location': 'Mumbai',            # Location filter
    'min_age': 25,                   # Minimum age
    'max_age': 35,                   # Maximum age
    'date_from': '2025-01-01',       # Start date
    'date_to': '2025-12-31',         # End date
}
```

### Applying Filters
```python
# In queryset
profiles = Profile.objects.filter(
    gender='female',
    location__icontains='Mumbai',
    age__gte=25,
    age__lte=35,
    created_at__gte='2025-01-01'
)

# In function call (for metadata display)
filters = {'gender': 'female', 'location': 'Mumbai'}
return export_profiles_to_pdf(profiles, filters=filters)
```

---

## 📚 Documentation

- **Complete Guide:** `EXPORT_HELPERS_GUIDE.md` (1,500+ lines)
- **Refactoring Guide:** `REFACTORING_EXPORT_VIEWSET.md` (450+ lines)
- **Implementation Summary:** `EXPORT_HELPERS_SUMMARY.md` (800+ lines)
- **Test Script:** `test_export_helpers.py` (350+ lines)

---

## 🐛 Troubleshooting

### Import Error
```bash
# Install dependencies
pip install reportlab>=4.0.0 pandas>=2.0.0 openpyxl>=3.1.0
```

### Empty PDF/Excel
```python
# Check if queryset has data
profiles = Profile.objects.all()
print(f"Profile count: {profiles.count()}")
```

### Memory Error
```python
# Limit dataset size
profiles = Profile.objects.all()[:500]
```

### Unicode Issues
```python
# Already handled - UTF-8 encoding used
# No action needed
```

---

## ✅ Checklist

Before using in production:

- [ ] Dependencies installed (`reportlab`, `pandas`, `openpyxl`)
- [ ] Functions imported successfully
- [ ] Test script runs without errors
- [ ] Sample exports generated and reviewed
- [ ] Admin permissions configured
- [ ] URLs configured (if using ViewSet)
- [ ] Frontend integration tested
- [ ] Error handling tested
- [ ] Large dataset tested (100+ records)
- [ ] Filter functionality tested

---

## 🎯 One-Liners

```python
# Export all profiles to PDF
return export_profiles_to_pdf(Profile.objects.all())

# Export female profiles to Excel
return export_profiles_to_excel(Profile.objects.filter(gender='female'))

# Export to CSV
return export_profiles_to_csv(Profile.objects.all())

# Export with custom title
return export_profiles_to_pdf(Profile.objects.all(), title="My Report")

# Export with filters metadata
return export_profiles_to_excel(
    Profile.objects.filter(gender='male'),
    filters={'gender': 'male'}
)
```

---

## 📞 Need Help?

1. Check `EXPORT_HELPERS_GUIDE.md` for detailed examples
2. Run `test_export_helpers.py` to verify setup
3. Review `REFACTORING_EXPORT_VIEWSET.md` for integration options
4. Inspect generated test files (PDF/Excel/CSV) for output format

---

**Location:** `backend/users/export_utils.py`

**Functions Available:**
- ✅ `export_profiles_to_pdf()`
- ✅ `export_profiles_to_excel()`
- ✅ `export_profiles_to_csv()`

**Status:** Production Ready 🚀

