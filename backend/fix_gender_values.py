import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import Profile

print("\n" + "="*60)
print("FIXING GENDER INCONSISTENCIES")
print("="*60)

# Check current gender values
print("\n📊 Current Gender Distribution:")
all_profiles = Profile.objects.all()
for profile in all_profiles:
    print(f"  {profile.name}: '{profile.gender}'")

# Fix inconsistent gender values
print("\n🔧 Fixing gender values...")
fixed_count = 0

for profile in all_profiles:
    old_gender = profile.gender
    
    # Normalize to lowercase
    if profile.gender in ['Male', 'MALE', 'M']:
        profile.gender = 'male'
        profile.save()
        fixed_count += 1
        print(f"  ✅ Fixed {profile.name}: '{old_gender}' → 'male'")
    elif profile.gender in ['Female', 'FEMALE', 'F']:
        profile.gender = 'female'
        profile.save()
        fixed_count += 1
        print(f"  ✅ Fixed {profile.name}: '{old_gender}' → 'female'")

print(f"\n✅ Fixed {fixed_count} profiles")

# Verify the fix
print("\n📊 Updated Gender Distribution:")
male_count = Profile.objects.filter(gender='male').count()
female_count = Profile.objects.filter(gender='female').count()
print(f"  Male: {male_count}")
print(f"  Female: {female_count}")

# Check what Sarah can now see
sarah = Profile.objects.filter(name__icontains='sarah').first()
if sarah:
    print(f"\n👤 SARAH can now see:")
    opposite_gender = 'male' if sarah.gender == 'female' else 'female'
    print(f"   Her gender: {sarah.gender}")
    print(f"   Looking for: {opposite_gender}")
    
    available = Profile.objects.filter(gender=opposite_gender).exclude(user=sarah.user)
    print(f"   Available profiles: {available.count()}")
    
    # Check if John is in the list
    john = Profile.objects.filter(name__icontains='john').first()
    if john and john in available:
        print(f"   ✅ John Doe IS NOW visible to Sarah!")
    elif john:
        print(f"   ❌ John Doe is still not visible (Gender: {john.gender})")
    
    for profile in available[:5]:
        print(f"   - {profile.name} (Gender: {profile.gender})")

print("\n✅ All done!")
