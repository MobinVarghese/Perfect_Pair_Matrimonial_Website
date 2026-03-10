import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile

print("\n" + "="*60)
print("CHECKING JOHN DOE AND SARAH")
print("="*60)

# Find Sarah
sarah_users = User.objects.filter(username__icontains='sarah')
print(f"\n🔍 Users with 'sarah' in username: {sarah_users.count()}")
for user in sarah_users:
    print(f"  - ID: {user.id}, Username: {user.username}")
    try:
        profile = user.profile
        print(f"    ✅ Has Profile: {profile.name}, Gender: {profile.gender}, Age: {profile.age}")
    except:
        print(f"    ❌ No Profile")

# Find John Doe
john_users = User.objects.filter(username__icontains='john')
print(f"\n🔍 Users with 'john' in username: {john_users.count()}")
for user in john_users:
    print(f"  - ID: {user.id}, Username: {user.username}")
    try:
        profile = user.profile
        print(f"    ✅ Has Profile: {profile.name}, Gender: {profile.gender}, Age: {profile.age}")
    except:
        print(f"    ❌ No Profile")

# Check all profiles
print(f"\n📊 TOTAL STATISTICS:")
print(f"Total Users: {User.objects.count()}")
print(f"Total Profiles: {Profile.objects.count()}")
print(f"Users without profiles: {User.objects.count() - Profile.objects.count()}")

# List users without profiles
users_without_profiles = []
for user in User.objects.all():
    try:
        profile = user.profile
    except:
        users_without_profiles.append(user)

if users_without_profiles:
    print(f"\n❌ Users without profiles ({len(users_without_profiles)}):")
    for user in users_without_profiles:
        print(f"  - ID: {user.id}, Username: {user.username}, Email: {user.email}")
else:
    print(f"\n✅ All users have profiles!")

# Check if john_doe profile exists by name
john_profiles = Profile.objects.filter(name__icontains='john')
print(f"\n🔍 Profiles with 'john' in name: {john_profiles.count()}")
for profile in john_profiles:
    print(f"  - Profile ID: {profile.id}, Name: {profile.name}, User ID: {profile.user.id}, Username: {profile.user.username}")

# Check if sarah can see john (gender filtering)
if sarah_users.exists():
    sarah = sarah_users.first()
    try:
        sarah_profile = sarah.profile
        print(f"\n👤 SARAH'S PROFILE:")
        print(f"   Gender: {sarah_profile.gender}")
        print(f"   Looking for: {'male' if sarah_profile.gender == 'female' else 'female'}")
        
        # Get opposite gender profiles
        opposite_gender = 'male' if sarah_profile.gender == 'female' else 'female'
        available_profiles = Profile.objects.filter(gender=opposite_gender).exclude(user=sarah)
        
        print(f"\n📋 Available profiles for Sarah ({opposite_gender}): {available_profiles.count()}")
        for profile in available_profiles[:10]:
            print(f"   - {profile.name} (Age: {profile.age}, Location: {profile.location})")
            
    except Exception as e:
        print(f"\n❌ Sarah has no profile: {e}")
