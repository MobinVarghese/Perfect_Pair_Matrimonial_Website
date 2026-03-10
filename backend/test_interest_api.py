import os
import django
import sys

sys.path.insert(0, 'D:/Matrimonial_Site/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile
from users.serializers import InterestSerializer
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser

# Get Sarah's user
sarah = User.objects.filter(username='sarah_jones').first()
print(f"Sarah User ID: {sarah.id}")

# Get a profile to send interest to (Mike Brown - Profile ID 12)
mike_profile = Profile.objects.get(id=12)
print(f"Mike Profile ID: {mike_profile.id}")
print(f"Mike User ID: {mike_profile.user.id}")

# Test the serializer with Profile ID (wrong - should fail)
print("\n--- Test 1: Sending Profile ID (12) - WRONG ---")
factory = APIRequestFactory()
request = factory.post('/api/interests/')
request.user = sarah

data = {
    'receiver': mike_profile.id,  # Profile ID (wrong)
    'message': ''
}

serializer = InterestSerializer(data=data, context={'request': request})
print(f"Is Valid: {serializer.is_valid()}")
if not serializer.is_valid():
    print(f"Errors: {serializer.errors}")

# Test the serializer with User ID (correct - should work)
print("\n--- Test 2: Sending User ID (10) - CORRECT ---")
data = {
    'receiver': mike_profile.user.id,  # User ID (correct)
    'message': ''
}

serializer = InterestSerializer(data=data, context={'request': request})
print(f"Is Valid: {serializer.is_valid()}")
if not serializer.is_valid():
    print(f"Errors: {serializer.errors}")
else:
    print(f"Validated Data: {serializer.validated_data}")
