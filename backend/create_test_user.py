#!/usr/bin/env python
"""Script to create a test user for login testing"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create test user
username = 'testuser'
email = 'test@example.com'
password = 'testpass123'

if User.objects.filter(username=username).exists():
    print(f'✅ User "{username}" already exists!')
else:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='Test',
        last_name='User'
    )
    print(f'✅ User created successfully!')

print(f'\n📝 Test Credentials:')
print(f'   Username: {username}')
print(f'   Password: {password}')
print(f'\nUse these credentials to test login at http://localhost:3000/login')
