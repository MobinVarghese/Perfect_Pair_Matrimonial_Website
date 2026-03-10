"""
Test script for Password Reset functionality
Run this script to test the password reset feature
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import OTPVerification
import requests

User = get_user_model()

print("=" * 60)
print("PASSWORD RESET FEATURE TEST")
print("=" * 60)

# Test with a known user
test_email = "sarah_jones@example.com"  # One of the female users

print(f"\n1. Testing password reset request for: {test_email}")
print("-" * 60)

# Request password reset
response = requests.post('http://localhost:8000/api/password-reset/request/', json={
    'email': test_email
})

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    otp_code = response.json().get('otp')
    print(f"\n✓ OTP Generated: {otp_code}")
    
    print(f"\n2. Testing password reset verification")
    print("-" * 60)
    
    # Verify OTP and reset password
    new_password = "newpassword123"
    verify_response = requests.post('http://localhost:8000/api/password-reset/verify/', json={
        'email': test_email,
        'otp': otp_code,
        'new_password': new_password
    })
    
    print(f"Status Code: {verify_response.status_code}")
    print(f"Response: {verify_response.json()}")
    
    if verify_response.status_code == 200:
        print(f"\n✓ Password reset successful!")
        print(f"\n3. Testing login with new password")
        print("-" * 60)
        
        # Try logging in with new password
        login_response = requests.post('http://localhost:8000/api/token/', json={
            'username': 'sarah_jones',
            'password': new_password
        })
        
        if login_response.status_code == 200:
            print(f"✓ Login successful with new password!")
            print(f"Access Token: {login_response.json().get('access')[:50]}...")
            
            # Reset password back to original
            print(f"\n4. Resetting password back to original")
            print("-" * 60)
            user = User.objects.get(email=test_email)
            user.set_password('password123')
            user.save()
            print(f"✓ Password reset back to 'password123'")
        else:
            print(f"✗ Login failed with new password")
            print(f"Response: {login_response.json()}")
    else:
        print(f"✗ Password reset verification failed")
else:
    print(f"✗ Password reset request failed")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
