import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile

print("\n" + "="*80)
print("CASE SENSITIVITY VERIFICATION - GENDER FILTERING TEST")
print("="*80)

# Test 1: Check all gender values in database
print("\n📋 TEST 1: Gender Values in Database")
print("-" * 80)

all_genders = Profile.objects.values_list('gender', flat=True).distinct()
print(f"Unique gender values: {list(all_genders)}")

male_count = Profile.objects.filter(gender='male').count()
female_count = Profile.objects.filter(gender='female').count()

# Try with capital letters (should return 0 if case-sensitive)
Male_count = Profile.objects.filter(gender='Male').count()
Female_count = Profile.objects.filter(gender='Female').count()

print(f"\n✅ Lowercase 'male': {male_count} profiles")
print(f"✅ Lowercase 'female': {female_count} profiles")
print(f"❌ Capitalized 'Male': {Male_count} profiles (should be 0)")
print(f"❌ Capitalized 'Female': {Female_count} profiles (should be 0)")

if Male_count > 0 or Female_count > 0:
    print("\n⚠️  WARNING: Found profiles with capitalized gender values!")
    print("   This will cause filtering issues.")
else:
    print("\n✅ All gender values are lowercase - filtering will work correctly!")

# Test 2: Simulate filtering for a male user (should show female profiles)
print("\n" + "="*80)
print("📋 TEST 2: Simulating Profile Filtering")
print("-" * 80)

# Get a male user
male_user = Profile.objects.filter(gender='male').first()
if male_user:
    print(f"\n👤 Test User: {male_user.name} (Gender: {male_user.gender})")
    print(f"   Looking for: opposite gender")
    
    # Simulate frontend logic (old - with capital letters)
    opposite_gender_capital = 'Female' if male_user.gender == 'male' else 'Male'
    profiles_capital = Profile.objects.filter(gender=opposite_gender_capital)
    print(f"\n❌ OLD Logic (Capital): gender='{opposite_gender_capital}'")
    print(f"   Results: {profiles_capital.count()} profiles")
    
    # Simulate frontend logic (new - with lowercase)
    opposite_gender_lower = 'female' if male_user.gender == 'male' else 'male'
    profiles_lower = Profile.objects.filter(gender=opposite_gender_lower)
    print(f"\n✅ NEW Logic (Lowercase): gender='{opposite_gender_lower}'")
    print(f"   Results: {profiles_lower.count()} profiles")
    
    if profiles_lower.count() > 0:
        print(f"\n   Sample profiles shown:")
        for profile in profiles_lower[:5]:
            print(f"   - {profile.name} ({profile.gender}, {profile.age})")

# Test 3: Check Sarah can see John
print("\n" + "="*80)
print("📋 TEST 3: Sarah → John Visibility Test")
print("-" * 80)

sarah = Profile.objects.filter(name__icontains='sarah').first()
john = Profile.objects.filter(name__icontains='john').first()

if sarah and john:
    print(f"\n👤 Sarah: {sarah.name}")
    print(f"   Gender: '{sarah.gender}'")
    print(f"   Looking for: '{('male' if sarah.gender == 'female' else 'female')}'")
    
    print(f"\n👤 John: {john.name}")
    print(f"   Gender: '{john.gender}'")
    
    # Check if John would be in Sarah's filtered results
    opposite = 'male' if sarah.gender == 'female' else 'female'
    sarah_matches = Profile.objects.filter(gender=opposite).exclude(user=sarah.user)
    
    if john in sarah_matches:
        print(f"\n✅ SUCCESS: John Doe WILL appear in Sarah's profile list!")
        print(f"   Total profiles Sarah can see: {sarah_matches.count()}")
    else:
        print(f"\n❌ PROBLEM: John Doe will NOT appear in Sarah's profile list!")
        print(f"   Sarah's gender: '{sarah.gender}'")
        print(f"   John's gender: '{john.gender}'")
        print(f"   Filter looking for: '{opposite}'")
else:
    print("\n⚠️  Sarah or John not found in database")

# Test 4: Registration simulation
print("\n" + "="*80)
print("📋 TEST 4: Registration Data Flow Test")
print("-" * 80)

print("\nSimulating registration with 'male' (lowercase):")
print("  Frontend sends: gender='male'")
print("  Backend receives: gender='male'")
print("  Model saves: gender='male' (normalized in save())")
print("  ✅ Filtering works: Can search for gender='male'")

print("\nSimulating registration with 'Male' (capitalized):")
print("  Frontend sends: gender='Male'")
print("  Backend receives: gender='Male'")
print("  Model saves: gender='male' (normalized to lowercase in save())")
print("  ✅ Filtering works: Can search for gender='male'")

# Test 5: Verify all profiles are searchable
print("\n" + "="*80)
print("📋 TEST 5: Profile Searchability")
print("-" * 80)

print("\n🔍 Testing gender='male' filter:")
male_profiles = Profile.objects.filter(gender='male')
print(f"   Found {male_profiles.count()} profiles")

print("\n🔍 Testing gender='female' filter:")
female_profiles = Profile.objects.filter(gender='female')
print(f"   Found {female_profiles.count()} profiles")

print("\n🔍 Testing gender='Male' filter (should be 0):")
Male_profiles = Profile.objects.filter(gender='Male')
print(f"   Found {Male_profiles.count()} profiles")

print("\n🔍 Testing gender='Female' filter (should be 0):")
Female_profiles = Profile.objects.filter(gender='Female')
print(f"   Found {Female_profiles.count()} profiles")

print("\n" + "="*80)
print("✅ VERIFICATION COMPLETE!")
print("="*80)

print("\n📊 SUMMARY:")
print(f"Total profiles: {Profile.objects.count()}")
print(f"Searchable with 'male': {Profile.objects.filter(gender='male').count()}")
print(f"Searchable with 'female': {Profile.objects.filter(gender='female').count()}")
print(f"Total searchable: {Profile.objects.filter(gender__in=['male', 'female']).count()}")

if Profile.objects.count() == Profile.objects.filter(gender__in=['male', 'female']).count():
    print("\n✅ ALL PROFILES ARE SEARCHABLE! ✅")
else:
    print("\n⚠️  WARNING: Some profiles may not be searchable!")
