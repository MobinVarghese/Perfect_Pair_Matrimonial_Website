# Example: Refactoring Export ViewSet to Use Helper Functions

## Original Implementation
The current `ExportLogViewSet.export_data()` method in `users/views.py` contains all export logic inline (~280 lines).

## Refactored Implementation
Using the helper functions from `users/export_utils.py`, the code becomes much cleaner and maintainable.

---

## OPTION 1: Direct Replacement (Simplest)

Replace the `_export_pdf()` and `_export_excel()` methods in `ExportLogViewSet` with imports from the helper module:

```python
# At the top of users/views.py
from .export_utils import export_profiles_to_pdf, export_profiles_to_excel

# In ExportLogViewSet class
class ExportLogViewSet(viewsets.ReadOnlyModelViewSet):
    # ... existing code ...
    
    @action(detail=False, methods=['post'], url_path='export-data')
    def export_data(self, request):
        """Export data as PDF or Excel with logging"""
        serializer = ExportRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file_type = serializer.validated_data['file_type']
        export_type = serializer.validated_data['export_type']
        date_from = serializer.validated_data.get('date_from')
        date_to = serializer.validated_data.get('date_to')
        
        # Get data based on export type
        if export_type == 'profiles':
            queryset = Profile.objects.select_related('user').all()
            if date_from:
                queryset = queryset.filter(created_at__gte=date_from)
            if date_to:
                queryset = queryset.filter(created_at__lte=date_to)
            data = queryset
            record_count = data.count()
        # ... other export types ...
        
        # Generate file name
        file_name = f"{export_type}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{file_type}"
        
        # Create export log
        export_log = ExportLog.objects.create(
            admin=request.user,
            file_type=file_type,
            file_name=file_name,
            export_type=export_type,
            record_count=record_count
        )
        
        # Build filters dict for metadata
        filters = {}
        if date_from:
            filters['date_from'] = date_from.strftime('%Y-%m-%d')
        if date_to:
            filters['date_to'] = date_to.strftime('%Y-%m-%d')
        
        # Use helper functions
        if file_type == 'pdf':
            title = f"{export_type.title()} Export"
            return export_profiles_to_pdf(data, title=title, filters=filters)
        elif file_type == 'excel':
            sheet_name = export_type.title()
            return export_profiles_to_excel(data, sheet_name=sheet_name, filters=filters)
        else:
            return Response(
                {'error': 'Unsupported file type'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # REMOVE the _export_pdf() and _export_excel() methods entirely!
```

**Benefits:**
- ✅ Reduces ViewSet code by ~250 lines
- ✅ Reusable functions can be called from anywhere
- ✅ Easier to test independently
- ✅ Single source of truth for export logic
- ✅ Maintains ExportLog integration

---

## OPTION 2: Dedicated Export ViewSet (Recommended)

Create a separate ViewSet specifically for profile exports using the helper functions:

```python
# In users/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from .models import Profile
from .export_utils import (
    export_profiles_to_pdf,
    export_profiles_to_excel,
    export_profiles_to_csv
)


class ProfileExportViewSet(viewsets.ViewSet):
    """
    ViewSet for exporting profile data in various formats.
    
    Admin-only access.
    
    Endpoints:
    - GET /api/profile-exports/pdf/ - Export to PDF
    - GET /api/profile-exports/excel/ - Export to Excel
    - GET /api/profile-exports/csv/ - Export to CSV
    """
    permission_classes = [IsAdminUser]
    
    def get_filtered_profiles(self, request):
        """
        Apply filters from query parameters.
        
        Supported filters:
        - gender: male/female
        - location: partial match
        - min_age: minimum age
        - max_age: maximum age
        - date_from: created after date (YYYY-MM-DD)
        - date_to: created before date (YYYY-MM-DD)
        """
        queryset = Profile.objects.select_related('user').all()
        
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
        """Extract filters for metadata display"""
        filters = {}
        params = ['gender', 'location', 'min_age', 'max_age', 'date_from', 'date_to']
        
        for param in params:
            value = request.query_params.get(param)
            if value:
                filters[param] = value
        
        return filters
    
    @action(detail=False, methods=['get'])
    def pdf(self, request):
        """
        Export profiles to PDF.
        
        Query Parameters:
        - title: Custom PDF title (optional)
        - gender, location, min_age, max_age, date_from, date_to (filters)
        
        Example:
            GET /api/profile-exports/pdf/?gender=female&location=Mumbai
        """
        profiles = self.get_filtered_profiles(request)
        filters = self.get_filter_dict(request)
        title = request.query_params.get('title', 'User Profiles Export')
        
        return export_profiles_to_pdf(profiles, title=title, filters=filters)
    
    @action(detail=False, methods=['get'])
    def excel(self, request):
        """
        Export profiles to Excel.
        
        Query Parameters:
        - sheet_name: Custom sheet name (optional)
        - Filters: same as PDF
        
        Example:
            GET /api/profile-exports/excel/?min_age=25&max_age=35
        """
        profiles = self.get_filtered_profiles(request)
        filters = self.get_filter_dict(request)
        sheet_name = request.query_params.get('sheet_name', 'Profiles')
        
        return export_profiles_to_excel(profiles, sheet_name=sheet_name, filters=filters)
    
    @action(detail=False, methods=['get'])
    def csv(self, request):
        """
        Export profiles to CSV.
        
        Query Parameters: Same filters as PDF/Excel
        
        Example:
            GET /api/profile-exports/csv/?date_from=2025-01-01
        """
        profiles = self.get_filtered_profiles(request)
        
        return export_profiles_to_csv(profiles)
```

**URL Configuration:**

```python
# In users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileExportViewSet

router = DefaultRouter()
router.register(r'profile-exports', ProfileExportViewSet, basename='profile-export')

urlpatterns = [
    path('api/', include(router.urls)),
    # ... other patterns ...
]
```

**Benefits:**
- ✅ Clean separation of concerns
- ✅ Simple, readable code (~100 lines vs 400+)
- ✅ Easy to extend with new export types
- ✅ Standard REST patterns
- ✅ Can coexist with existing ExportLogViewSet

---

## OPTION 3: Simple Function-Based Views

For even simpler implementation, use function-based views:

```python
# In users/views.py

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .models import Profile
from .export_utils import export_profiles_to_pdf, export_profiles_to_excel


@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_profiles_pdf_view(request):
    """Export all profiles to PDF"""
    # Get filters from query params
    profiles = Profile.objects.all()
    
    gender = request.GET.get('gender')
    if gender:
        profiles = profiles.filter(gender=gender)
    
    location = request.GET.get('location')
    if location:
        profiles = profiles.filter(location__icontains=location)
    
    # Build filters dict
    filters = {}
    if gender:
        filters['gender'] = gender
    if location:
        filters['location'] = location
    
    return export_profiles_to_pdf(profiles, filters=filters)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_profiles_excel_view(request):
    """Export all profiles to Excel"""
    profiles = Profile.objects.all()
    
    # Apply filters (same as PDF)
    gender = request.GET.get('gender')
    if gender:
        profiles = profiles.filter(gender=gender)
    
    filters = {}
    if gender:
        filters['gender'] = gender
    
    return export_profiles_to_excel(profiles, filters=filters)
```

**URL Configuration:**

```python
# In users/urls.py
from django.urls import path
from .views import export_profiles_pdf_view, export_profiles_excel_view

urlpatterns = [
    path('api/export/profiles/pdf/', export_profiles_pdf_view, name='export-profiles-pdf'),
    path('api/export/profiles/excel/', export_profiles_excel_view, name='export-profiles-excel'),
    # ... other patterns ...
]
```

**Benefits:**
- ✅ Simplest implementation (20-30 lines per view)
- ✅ Direct and explicit
- ✅ Easy for beginners to understand
- ✅ No complex class structures

---

## Comparison Table

| Approach | Lines of Code | Complexity | Flexibility | Recommended For |
|----------|---------------|------------|-------------|-----------------|
| **Option 1: Direct Replacement** | ~150 lines | Medium | Medium | Minimal changes to existing code |
| **Option 2: Dedicated ViewSet** | ~100 lines | Low | High | New projects or clean refactoring |
| **Option 3: Function Views** | ~50 lines | Very Low | Low | Simple exports without many features |
| **Current Implementation** | ~400 lines | High | High | Already implemented |

---

## Migration Guide

### Step 1: Verify Helper Functions Work
```bash
cd backend
python test_export_helpers.py
```

### Step 2: Choose Implementation Option
Pick Option 1, 2, or 3 based on your needs.

### Step 3: Update Views
Replace existing code with chosen option.

### Step 4: Update URLs (if needed)
If using Option 2 or 3, update `users/urls.py`.

### Step 5: Test Endpoints
```bash
# Test PDF export
curl -X GET "http://localhost:8000/api/profile-exports/pdf/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test Excel export
curl -X GET "http://localhost:8000/api/profile-exports/excel/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Step 6: Update Documentation
Point to the new endpoints and usage patterns.

---

## Recommendation

**For your project, I recommend Option 2 (Dedicated ViewSet):**

1. ✅ Cleanest separation from ExportLog functionality
2. ✅ Simplest code to maintain (~100 lines)
3. ✅ Easy to extend with new features
4. ✅ Follows REST best practices
5. ✅ Can coexist with existing ExportLogViewSet
6. ✅ No need to refactor existing working code

**Keep the existing `ExportLogViewSet` for:**
- Tracking export history
- Viewing export logs
- Admin audit trail

**Use the new `ProfileExportViewSet` for:**
- Actual export operations
- User-facing export endpoints
- Filtered exports with query parameters

This gives you the best of both worlds: a clean, maintainable export system with full audit logging capabilities.

---

## Next Steps

1. ✅ Test helper functions: `python test_export_helpers.py`
2. ✅ Review the guide: `EXPORT_HELPERS_GUIDE.md`
3. ⏳ Choose implementation option (1, 2, or 3)
4. ⏳ Implement in your views.py
5. ⏳ Update URLs if needed
6. ⏳ Test with your frontend
7. ⏳ Deploy!

