"""
Test the check interest status endpoint as Sarah checking Mike's profile
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile, Interest
from django.db.models import Q

# Get users
sarah = User.objects.get(username='sarah_jones')
mike = User.objects.get(username='mike_brown')

print(f"\n=== Users ===")
print(f"Sarah: User ID {sarah.id}, Profile ID {sarah.profile.id}")
print(f"Mike: User ID {mike.id}, Profile ID {mike.profile.id}")

# Get Mike's profile
mike_profile_id = mike.profile.id

# Simulate the check_interest_status endpoint
try:
    target_profile = Profile.objects.get(id=mike_profile_id)
    target_user = target_profile.user
    
    print(f"\n=== Target Profile ===")
    print(f"Target Profile ID: {target_profile.id}")
    print(f"Target User ID: {target_user.id}, Username: {target_user.username}")
    
    # Check for interest from either direction (as Sarah)
    interest = Interest.objects.filter(
        Q(sender=sarah, receiver=target_user) |
        Q(sender=target_user, receiver=sarah)
    ).first()
    
    print(f"\n=== Interest Query ===")
    print(f"Looking for interest between Sarah (ID: {sarah.id}) and Mike (ID: {target_user.id})")
    print(f"Query: (sender=Sarah AND receiver=Mike) OR (sender=Mike AND receiver=Sarah)")
    
    if interest:
        print(f"\n✅ Interest Found!")
        print(f"  - Interest ID: {interest.id}")
        print(f"  - Sender: {interest.sender.username} (ID: {interest.sender.id})")
        print(f"  - Receiver: {interest.receiver.username} (ID: {interest.receiver.id})")
        print(f"  - Status: {interest.status}")
        print(f"  - Is Sarah the sender? {interest.sender == sarah}")
    else:
        print(f"\n❌ No Interest Found")
        print(f"\nChecking all interests involving Sarah or Mike:")
        all_interests = Interest.objects.filter(
            Q(sender=sarah) | Q(receiver=sarah) |
            Q(sender=mike) | Q(receiver=mike)
        )
        print(f"  Found {all_interests.count()} interests:")
        for i in all_interests:
            print(f"    - {i.sender.username} → {i.receiver.username} (Status: {i.status})")
            
except Profile.DoesNotExist:
    print("❌ Profile not found")
