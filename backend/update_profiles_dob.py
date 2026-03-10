import os
import django
import sys
from datetime import date, timedelta

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import Profile

print("\n" + "="*80)
print("UPDATING EXISTING PROFILES WITH DATE_OF_BIRTH")
print("="*80)

profiles = Profile.objects.all()
updated_count = 0

print(f"\n📋 Processing {profiles.count()} profiles...\n")

for profile in profiles:
    if not profile.date_of_birth and profile.age:
        # Calculate approximate date of birth from age
        current_year = date.today().year
        birth_year = current_year - profile.age
        
        # Use January 1st as default DOB
        profile.date_of_birth = date(birth_year, 1, 1)
        profile.save()
        
        updated_count += 1
        print(f"✅ {profile.name}: Age {profile.age} → DOB {profile.date_of_birth}")
    elif profile.date_of_birth:
        print(f"ℹ️  {profile.name}: Already has DOB {profile.date_of_birth}")
    else:
        print(f"⚠️  {profile.name}: No age or DOB found")

print(f"\n{'='*80}")
print(f"✅ Updated {updated_count} profiles with calculated date_of_birth")
print(f"{'='*80}")

# Verify all profiles
print("\n📊 VERIFICATION:")
profiles_with_dob = Profile.objects.filter(date_of_birth__isnull=False).count()
profiles_without_dob = Profile.objects.filter(date_of_birth__isnull=True).count()

print(f"Profiles with DOB: {profiles_with_dob}")
print(f"Profiles without DOB: {profiles_without_dob}")

print("\n✅ All done!")
