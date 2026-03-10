"""
Script to check interest status between Sarah and Mike
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile, Interest

try:
    sarah = User.objects.get(username='sarah_jones')
    mike = User.objects.get(username='mike_brown')
    
    print(f"\n=== User Information ===")
    print(f"Sarah: ID {sarah.id}, Profile ID {sarah.profile.id}")
    print(f"Mike: ID {mike.id}, Profile ID {mike.profile.id}")
    
    # Check interests from Sarah to Mike
    interests_sarah_to_mike = Interest.objects.filter(sender=sarah, receiver=mike)
    print(f"\n=== Interests from Sarah to Mike ===")
    print(f"Count: {interests_sarah_to_mike.count()}")
    for interest in interests_sarah_to_mike:
        print(f"  - Interest ID: {interest.id}")
        print(f"    Status: {interest.status}")
        print(f"    Created: {interest.created_at}")
        print(f"    Message: {interest.message}")
    
    # Check interests from Mike to Sarah
    interests_mike_to_sarah = Interest.objects.filter(sender=mike, receiver=sarah)
    print(f"\n=== Interests from Mike to Sarah ===")
    print(f"Count: {interests_mike_to_sarah.count()}")
    for interest in interests_mike_to_sarah:
        print(f"  - Interest ID: {interest.id}")
        print(f"    Status: {interest.status}")
        print(f"    Created: {interest.created_at}")
    
    # Check all interests in database
    all_interests = Interest.objects.all()
    print(f"\n=== All Interests in Database ===")
    print(f"Total: {all_interests.count()}")
    for interest in all_interests:
        sender_name = interest.sender.username if interest.sender else "None"
        receiver_name = interest.receiver.username if interest.receiver else "None"
        print(f"  - {sender_name} → {receiver_name} (Status: {interest.status})")
    
except User.DoesNotExist as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Error: {e}")
