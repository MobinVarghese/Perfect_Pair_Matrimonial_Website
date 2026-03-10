"""
Script to delete cyril user and all dependencies
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile, Interest, Favorite, Report

try:
    # Find the user
    user = User.objects.get(username__iexact='cyril')
    print(f"\n=== Found User: {user.username} (ID: {user.id}) ===\n")
    
    # Check dependencies
    profile = Profile.objects.filter(user=user).first()
    sent_interests = Interest.objects.filter(sender=user)
    received_interests = Interest.objects.filter(receiver=user)
    favorites = Favorite.objects.filter(user=user)
    reports_by = Report.objects.filter(reporter=user)
    reports_against = Report.objects.filter(reported_user=user)
    
    print("Dependencies found:")
    print(f"  - Profile: {profile.id if profile else 'None'}")
    print(f"  - Sent Interests: {sent_interests.count()}")
    print(f"  - Received Interests: {received_interests.count()}")
    print(f"  - Favorites: {favorites.count()}")
    print(f"  - Reports By User: {reports_by.count()}")
    print(f"  - Reports Against User: {reports_against.count()}")
    
    # Delete all dependencies (Django cascade delete should handle this)
    print("\nDeleting user and all dependencies...")
    
    # Manual deletion for clarity
    if profile:
        print(f"  ✓ Deleting profile (ID: {profile.id})")
        profile.delete()
    
    sent_count = sent_interests.count()
    if sent_count > 0:
        print(f"  ✓ Deleting {sent_count} sent interests")
        sent_interests.delete()
    
    received_count = received_interests.count()
    if received_count > 0:
        print(f"  ✓ Deleting {received_count} received interests")
        received_interests.delete()
    
    fav_count = favorites.count()
    if fav_count > 0:
        print(f"  ✓ Deleting {fav_count} favorites")
        favorites.delete()
    
    reports_by_count = reports_by.count()
    if reports_by_count > 0:
        print(f"  ✓ Deleting {reports_by_count} reports by user")
        reports_by.delete()
    
    reports_against_count = reports_against.count()
    if reports_against_count > 0:
        print(f"  ✓ Deleting {reports_against_count} reports against user")
        reports_against.delete()
    
    # Finally delete the user
    print(f"  ✓ Deleting user: {user.username}")
    user.delete()
    
    print("\n✅ Successfully deleted cyril user and all dependencies!")
    
except User.DoesNotExist:
    print("❌ User 'cyril' not found in database")
except Exception as e:
    print(f"❌ Error: {e}")
