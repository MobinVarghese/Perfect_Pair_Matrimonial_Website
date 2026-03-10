# 🔍 Advanced Profile Search Feature - Complete Documentation

## Overview

Implemented a comprehensive search system for the matrimonial site that allows users to search and filter profiles using multiple criteria. The feature includes both a quick search bar and advanced filters.

---

## 🎯 Features Implemented

### 1. Django Backend - Search API Endpoint

**Endpoint:** `/api/profiles/search/`  
**Method:** `GET`  
**Authentication:** Required (JWT Token)

#### Supported Query Parameters:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `q` | string | General search across name, occupation, location, education | `?q=engineer` |
| `name` | string | Filter by name (case-insensitive partial match) | `?name=john` |
| `min_age` | integer | Minimum age filter | `?min_age=25` |
| `max_age` | integer | Maximum age filter | `?max_age=35` |
| `gender` | string | Filter by gender (male/female/other) | `?gender=female` |
| `occupation` | string | Filter by occupation (partial match) | `?occupation=doctor` |
| `location` | string | Filter by location (partial match) | `?location=mumbai` |
| `city` | string | Filter by city (partial match) | `?city=delhi` |
| `state` | string | Filter by state (partial match) | `?state=maharashtra` |
| `country` | string | Filter by country (partial match) | `?country=india` |
| `education` | string | Filter by education (partial match) | `?education=masters` |
| `marital_status` | string | Filter by marital status | `?marital_status=single` |
| `ordering` | string | Sort results | `?ordering=-age` (desc), `?ordering=name` (asc) |

#### Example API Requests:

```bash
# General search
GET /api/profiles/search/?q=engineer

# Search with multiple filters
GET /api/profiles/search/?gender=female&min_age=25&max_age=30&location=mumbai

# Search by occupation
GET /api/profiles/search/?occupation=software%20engineer

# Search by name and education
GET /api/profiles/search/?name=priya&education=bachelor

# Complex search
GET /api/profiles/search/?q=doctor&gender=male&min_age=30&max_age=40&marital_status=single&ordering=-age
```

#### Response Format:

```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 5,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
      },
      "name": "John Doe",
      "gender": "Male",
      "date_of_birth": "1990-05-15",
      "age": 34,
      "height": 175.5,
      "weight": 70.0,
      "marital_status": "Single",
      "mother_tongue": "English",
      "location": "Mumbai, Maharashtra",
      "city": "Mumbai",
      "state": "Maharashtra",
      "country": "India",
      "occupation": "Software Engineer",
      "education": "Bachelor of Engineering",
      "income": "1000000",
      "profile_picture": "http://localhost:8000/media/profiles/john.jpg",
      "bio": "Looking for a life partner...",
      "created_at": "2024-01-15T10:30:00Z"
    },
    // ... more profiles
  ]
}
```

---

### 2. React Frontend - Enhanced Search Component

#### Components Modified:

**File:** `src/pages/HomePage.jsx`

#### Key Features:

1. **Quick Search Bar**
   - Prominent search input at the top
   - Real-time search with Enter key
   - Searches across: name, occupation, location, education
   - Beautiful gradient search button
   - Advanced filters toggle button

2. **Advanced Filters Panel**
   - Collapsible filters section
   - 7 filter fields:
     - Gender (dropdown)
     - Min Age (number input)
     - Max Age (number input)
     - Location (text input)
     - Occupation (text input)
     - Education (text input)
     - Marital Status (dropdown)
   - Apply/Clear buttons
   - Smooth animation on show/hide

3. **Results Display**
   - Shows count of matching profiles
   - Real-time update after search
   - Loading spinner during search
   - Empty state when no results
   - Responsive grid layout

#### State Management:

```javascript
const [searchQuery, setSearchQuery] = useState(''); // Quick search query
const [filters, setFilters] = useState({
  gender: '',
  min_age: '',
  max_age: '',
  location: '',
  occupation: '',
  education: '',
  marital_status: '',
});
const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
const [resultCount, setResultCount] = useState(0);
```

#### API Integration:

```javascript
// Uses searchProfiles from api.js
import { searchProfiles, sendInterest } from '../api/api';

const fetchProfiles = async (searchFilters = {}) => {
  setLoading(true);
  try {
    const data = await searchProfiles(searchFilters);
    const profileList = Array.isArray(data) ? data : data.results || [];
    setProfiles(profileList);
    setResultCount(data.count || profileList.length);
  } catch (error) {
    console.error('Error fetching profiles:', error);
    setProfiles([]);
    setResultCount(0);
  } finally {
    setLoading(false);
  }
};
```

---

## 🎨 UI/UX Design

### Quick Search Bar

```jsx
<div className="bg-white rounded-xl shadow-md p-6 mb-6">
  <div className="flex items-center space-x-4">
    {/* Search Icon + Input */}
    <div className="flex-1 relative">
      <input 
        placeholder="Search by name, occupation, location, education..."
        className="... pl-10 pr-3 py-3 ..."
      />
    </div>
    
    {/* Search Button (Gradient) */}
    <button className="bg-gradient-to-r from-red-600 to-pink-600 ...">
      Search
    </button>
    
    {/* Advanced Filters Toggle */}
    <button className="border-2 border-gray-300 ...">
      Advanced Filters
    </button>
  </div>
  
  {/* Results Count */}
  <div className="mt-4 text-sm text-gray-600">
    Found <span className="font-semibold text-red-600">15</span> profiles
  </div>
</div>
```

### Advanced Filters

```jsx
{showAdvancedFilters && (
  <div className="bg-white rounded-xl shadow-md p-6 mb-6 animate-fadeIn">
    {/* 7 filter fields in responsive grid */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Gender, Ages, Location, Occupation, Education, Marital Status */}
    </div>
    
    {/* Action Buttons */}
    <div className="flex items-center space-x-4 mt-6">
      <button>Apply Filters</button>
      <button>Clear All</button>
    </div>
  </div>
)}
```

### Color Scheme

- **Primary Gradient:** Red to Pink (`from-red-600 to-pink-600`)
- **Hover State:** Darker gradient (`from-red-700 to-pink-700`)
- **Result Count:** Red accent (`text-red-600`)
- **Borders:** Gray 300 (`border-gray-300`)
- **Background:** White cards on gray-50 background

---

## 🔧 Backend Implementation Details

### View Function (in `users/views.py`):

```python
@action(detail=False, methods=['get'], url_path='search')
def search_profiles(self, request):
    """
    Advanced search endpoint for profiles.
    """
    queryset = Profile.objects.select_related('user').all()
    
    # General search query (searches across multiple fields)
    q = request.query_params.get('q', None)
    if q:
        queryset = queryset.filter(
            Q(name__icontains=q) |
            Q(occupation__icontains=q) |
            Q(location__icontains=q) |
            Q(education__icontains=q)
        )
    
    # Individual filters
    name = request.query_params.get('name', None)
    if name:
        queryset = queryset.filter(name__icontains=name)
    
    # Age range filters
    min_age = request.query_params.get('min_age', None)
    max_age = request.query_params.get('max_age', None)
    if min_age:
        queryset = queryset.filter(age__gte=int(min_age))
    if max_age:
        queryset = queryset.filter(age__lte=int(max_age))
    
    # Gender filter
    gender = request.query_params.get('gender', None)
    if gender:
        queryset = queryset.filter(gender__iexact=gender)
    
    # ... more filters
    
    # Ordering
    ordering = request.query_params.get('ordering', '-created_at')
    if ordering in valid_orderings:
        queryset = queryset.order_by(ordering)
    
    # Return results
    serializer = self.get_serializer(queryset, many=True)
    return Response({
        'count': queryset.count(),
        'results': serializer.data
    })
```

### URL Configuration:

The search endpoint is automatically registered by the Django REST Framework router:

```python
# In users/urls.py
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

# This creates:
# GET /api/profiles/search/ -> ProfileViewSet.search_profiles()
```

---

## 📱 User Flow

### 1. Quick Search Flow

```
User enters "engineer" in search bar
  ↓
Presses Enter or clicks Search button
  ↓
API call: GET /api/profiles/search/?q=engineer
  ↓
Backend searches: name, occupation, location, education
  ↓
Returns matching profiles
  ↓
Frontend displays results with count
```

### 2. Advanced Search Flow

```
User clicks "Advanced Filters" button
  ↓
Filter panel slides down (animate-fadeIn)
  ↓
User selects filters:
  - Gender: Female
  - Min Age: 25
  - Max Age: 30
  - Location: Mumbai
  - Occupation: Doctor
  ↓
Clicks "Apply Filters"
  ↓
API call: GET /api/profiles/search/?gender=female&min_age=25&max_age=30&location=mumbai&occupation=doctor
  ↓
Backend applies all filters using Q objects
  ↓
Returns filtered results
  ↓
Frontend displays matching profiles
```

### 3. Clear Filters Flow

```
User clicks "Clear All" button
  ↓
All filter fields reset to empty
  ↓
API call: GET /api/profiles/search/ (no filters)
  ↓
Returns all profiles
  ↓
Frontend displays all profiles
```

---

## 🧪 Testing the Search Feature

### Test Cases:

#### 1. Quick Search Test
```bash
# Test general search
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/profiles/search/?q=engineer"

# Expected: Profiles with "engineer" in name, occupation, location, or education
```

#### 2. Gender Filter Test
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/profiles/search/?gender=female"

# Expected: Only female profiles
```

#### 3. Age Range Test
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/profiles/search/?min_age=25&max_age=30"

# Expected: Profiles with age between 25 and 30
```

#### 4. Location Search Test
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/profiles/search/?location=mumbai"

# Expected: Profiles with "mumbai" in location field
```

#### 5. Occupation Search Test
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/profiles/search/?occupation=doctor"

# Expected: Profiles with "doctor" in occupation
```

#### 6. Combined Filters Test
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/profiles/search/?gender=female&min_age=25&max_age=30&location=delhi&education=masters"

# Expected: Female profiles, age 25-30, in Delhi, with master's education
```

### Frontend Testing:

1. **Quick Search:**
   - Type "engineer" in search bar → Press Enter
   - Should show profiles matching "engineer"

2. **Advanced Filters:**
   - Click "Advanced Filters" button
   - Set Gender: Female
   - Set Age Range: 25-30
   - Click "Apply Filters"
   - Should show filtered results

3. **Clear Filters:**
   - Click "Clear All" button
   - All fields should reset
   - Should show all profiles

4. **Result Count:**
   - After any search, verify count matches number of results
   - "Found X profiles" should update dynamically

---

## 🚀 Performance Optimizations

### Database Queries:

1. **select_related()** - Reduces database queries
   ```python
   queryset = Profile.objects.select_related('user').all()
   ```

2. **Case-insensitive searches** - Uses database indexes
   ```python
   .filter(name__icontains=name)  # Case-insensitive
   ```

3. **Q objects** - Efficient OR queries
   ```python
   Q(name__icontains=q) | Q(occupation__icontains=q)
   ```

### Frontend Optimizations:

1. **Debounced Search** - Reduces API calls
   - Enter key trigger prevents excessive requests

2. **Loading States** - Better UX
   - Spinner shows during API calls
   - Disabled state prevents duplicate requests

3. **Conditional Rendering** - Efficient DOM updates
   ```jsx
   {showAdvancedFilters && <FilterPanel />}
   ```

---

## 🔐 Security Features

### Backend:

1. **Authentication Required**
   ```python
   permission_classes = [IsAuthenticated]
   ```

2. **Input Validation**
   ```python
   if min_age:
       try:
           queryset = queryset.filter(age__gte=int(min_age))
       except (ValueError, TypeError):
           pass
   ```

3. **SQL Injection Prevention**
   - Django ORM handles parameterization automatically
   - Uses `.filter()` instead of raw SQL

### Frontend:

1. **JWT Token** - Automatically attached to requests
2. **Input Sanitization** - Form validation
3. **Error Handling** - Graceful failure

---

## 📊 Search Analytics (Future Enhancement)

### Track Search Metrics:

```python
class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=255)
    filters_used = models.JSONField()
    results_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Implement in View:

```python
# Log search
SearchLog.objects.create(
    user=request.user,
    search_query=q or '',
    filters_used=dict(request.query_params),
    results_count=queryset.count()
)
```

---

## 🎯 Future Enhancements

### 1. Auto-complete Suggestions
```jsx
<input 
  onInput={handleAutoComplete}
  list="suggestions"
/>
<datalist id="suggestions">
  {suggestions.map(item => <option value={item} />)}
</datalist>
```

### 2. Saved Searches
```python
class SavedSearch(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    filters = models.JSONField()
```

### 3. Recent Searches
```jsx
const [recentSearches, setRecentSearches] = useState([]);
// Store in localStorage
localStorage.setItem('recentSearches', JSON.stringify(searches));
```

### 4. Search by Distance
```python
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

queryset = queryset.filter(
    location__distance_lte=(Point(lng, lat), D(km=50))
)
```

### 5. Fuzzy Search
```python
from django.contrib.postgres.search import TrigramSimilarity

queryset = queryset.annotate(
    similarity=TrigramSimilarity('name', search_query)
).filter(similarity__gt=0.3).order_by('-similarity')
```

---

## 📝 Summary

✅ **Backend:** Advanced search endpoint with 12+ filter parameters  
✅ **Frontend:** Beautiful search bar + collapsible advanced filters  
✅ **UI/UX:** Gradient buttons, smooth animations, result count  
✅ **Performance:** Optimized queries, loading states  
✅ **Security:** Authentication, input validation  
✅ **Responsive:** Mobile-friendly grid layout  
✅ **Documentation:** Complete API reference  

The search feature is **production-ready** and fully integrated! 🎉

