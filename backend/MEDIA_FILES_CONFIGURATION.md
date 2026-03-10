# Media Files Configuration Guide

## Overview
Media files configuration for handling user-uploaded content including profile photos, documents, and other files in the Matrimonial Website.

---

## 📁 Directory Structure

```
backend/
├── media/                          # Root media directory
│   ├── profile_photos/            # User profile pictures
│   │   └── .gitkeep
│   └── documents/                 # User documents (ID proof, etc.)
│       └── .gitkeep
├── staticfiles/                   # Collected static files (for production)
└── backend/
    └── settings.py                # Configuration file
```

---

## ⚙️ Settings Configuration

### In `settings.py`:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Specific media subdirectories
MEDIA_PROFILE_PHOTOS = os.path.join(MEDIA_ROOT, 'profile_photos')
MEDIA_DOCUMENTS = os.path.join(MEDIA_ROOT, 'documents')

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### In `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your url patterns
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📝 Configuration Details

### MEDIA_URL
- **Value**: `/media/`
- **Purpose**: URL prefix for serving media files
- **Example**: User profile photo accessible at `http://localhost:8000/media/profile_photos/user_123.jpg`

### MEDIA_ROOT
- **Value**: `BASE_DIR / 'media'`
- **Purpose**: Filesystem path where uploaded files are stored
- **Location**: `d:\Matrimonial_Site\backend\media\`

### Subdirectories:
1. **profile_photos/**: Store user profile pictures
2. **documents/**: Store user documents (ID proofs, certificates, etc.)

---

## 🖼️ Using Media Files in Models

### Update UserProfile Model

Edit `users/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile photo field
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
        help_text='Profile picture'
    )
    
    # Additional document field
    id_proof = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True,
        help_text='ID proof document'
    )
    
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True
    )
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        ordering = ['-created_at']
```

### Run Migrations

```bash
cd d:\Matrimonial_Site\backend
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate
```

---

## 🔄 Update Serializers

Edit `users/serializers.py`:

```python
class UserProfileSerializer(serializers.ModelSerializer):
    profile_photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'phone_number', 'date_of_birth', 'gender', 'bio',
            'profile_photo', 'profile_photo_url', 'id_proof',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_profile_photo_url(self, obj):
        if obj.profile_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_photo.url)
        return None
```

---

## 📤 File Upload API

### Create Upload View

Edit `users/views.py`:

```python
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_profile_photo(request):
    """Upload or update user profile photo"""
    if not request.user.is_authenticated:
        return Response(
            {'error': 'Authentication required'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    profile = request.user.profile
    
    if 'profile_photo' in request.FILES:
        # Delete old photo if exists
        if profile.profile_photo:
            profile.profile_photo.delete()
        
        # Save new photo
        profile.profile_photo = request.FILES['profile_photo']
        profile.save()
        
        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(
        {'error': 'No file provided'},
        status=status.HTTP_400_BAD_REQUEST
    )
```

### Add URL Route

Edit `users/urls.py`:

```python
from .views import upload_profile_photo

urlpatterns = [
    # ... existing patterns
    path('upload-photo/', upload_profile_photo, name='upload-profile-photo'),
]
```

---

## 🌐 Frontend Integration (React)

### Upload Component Example

```javascript
import axios from 'axios';

const uploadProfilePhoto = async (file, token) => {
  const formData = new FormData();
  formData.append('profile_photo', file);
  
  try {
    const response = await axios.post(
      'http://localhost:8000/api/users/upload-photo/',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      }
    );
    console.log('Upload successful:', response.data);
    return response.data;
  } catch (error) {
    console.error('Upload failed:', error);
    throw error;
  }
};

// Usage in component
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    uploadProfilePhoto(file, userToken);
  }
};
```

### Display Profile Photo

```javascript
const ProfilePhoto = ({ photoUrl }) => {
  const defaultPhoto = '/default-avatar.png';
  
  return (
    <img
      src={photoUrl || defaultPhoto}
      alt="Profile"
      style={{ width: '150px', height: '150px', borderRadius: '50%' }}
    />
  );
};
```

---

## 🔒 Security Considerations

### 1. File Size Limits

Add to `settings.py`:

```python
# Maximum upload file size (in bytes)
# 5MB = 5 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

### 2. File Type Validation

```python
from django.core.exceptions import ValidationError

def validate_image(image):
    """Validate uploaded image file"""
    # Check file size (2MB)
    if image.size > 2 * 1024 * 1024:
        raise ValidationError("Image file too large ( > 2MB )")
    
    # Check file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed: {', '.join(valid_extensions)}")
    
    return image

# Use in model
class UserProfile(models.Model):
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        validators=[validate_image],
        blank=True,
        null=True
    )
```

### 3. Image Processing with Pillow

```python
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

def compress_image(image, max_size=(800, 800), quality=85):
    """Compress and resize image"""
    img = Image.open(image)
    
    # Convert RGBA to RGB if necessary
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    
    # Resize if larger than max_size
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Save to BytesIO
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    return ContentFile(output.read())
```

---

## 🗂️ File Organization Best Practices

### 1. Organize by User ID

```python
def user_directory_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/profile_photos/user_<id>/<filename>"""
    return f'profile_photos/user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    profile_photo = models.ImageField(upload_to=user_directory_path)
```

### 2. Generate Unique Filenames

```python
import uuid
from django.utils.text import slugify

def unique_filename(instance, filename):
    """Generate unique filename"""
    ext = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex[:8]
    username = slugify(instance.user.username)
    new_filename = f"{username}_{unique_id}.{ext}"
    return f'profile_photos/{new_filename}'
```

---

## 🚀 Production Configuration

### Use Cloud Storage (AWS S3, Azure, etc.)

Install django-storages:
```bash
pip install django-storages boto3
```

Configure in `settings.py`:
```python
# AWS S3 Configuration (example)
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
```

---

## ✅ Testing Media Upload

### Using cURL:

```bash
curl -X POST http://localhost:8000/api/users/upload-photo/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "profile_photo=@/path/to/photo.jpg"
```

### Using Postman:
1. Set method to POST
2. URL: `http://localhost:8000/api/users/upload-photo/`
3. Headers: `Authorization: Bearer YOUR_TOKEN`
4. Body: form-data, key: `profile_photo`, type: File

---

## 📊 Directory Permissions

### Windows:
Directories created automatically have proper permissions.

### Linux/Mac:
```bash
chmod 755 media/
chmod 755 media/profile_photos/
chmod 755 media/documents/
```

---

## 🎯 Summary

**Configured Settings:**
- ✅ MEDIA_URL = `/media/`
- ✅ MEDIA_ROOT = `d:\Matrimonial_Site\backend\media`
- ✅ STATIC_URL = `/static/`
- ✅ STATIC_ROOT = `d:\Matrimonial_Site\backend\staticfiles`

**Created Directories:**
- ✅ `media/profile_photos/`
- ✅ `media/documents/`
- ✅ `staticfiles/`

**Status:** All media file configurations are complete and ready for use! 🎉
