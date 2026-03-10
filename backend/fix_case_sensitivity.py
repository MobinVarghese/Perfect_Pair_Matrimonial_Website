import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile

print("\n" + "="*80)
print("COMPREHENSIVE CASE SENSITIVITY CHECK")
print("="*80)

# ============================================================================
# 1. CHECK AND FIX USER DATA
# ============================================================================
print("\n📋 PART 1: CHECKING USER DATA")
print("-" * 80)

users = User.objects.all()
user_fixes = []

for user in users:
    issues = []
    fixes = {}
    
    # Check username (should be lowercase)
    if user.username != user.username.lower():
        issues.append(f"Username has uppercase: '{user.username}'")
        fixes['username'] = user.username.lower()
    
    # Check email (should be lowercase)
    if user.email != user.email.lower():
        issues.append(f"Email has uppercase: '{user.email}'")
        fixes['email'] = user.email.lower()
    
    # Check first_name (should be Title Case)
    if user.first_name and user.first_name != user.first_name.title():
        issues.append(f"First name not Title Case: '{user.first_name}'")
        fixes['first_name'] = user.first_name.title()
    
    # Check last_name (should be Title Case)
    if user.last_name and user.last_name != user.last_name.title():
        issues.append(f"Last name not Title Case: '{user.last_name}'")
        fixes['last_name'] = user.last_name.title()
    
    if issues:
        user_fixes.append({
            'user': user,
            'issues': issues,
            'fixes': fixes
        })
        print(f"\n❌ User ID {user.id}: {user.username}")
        for issue in issues:
            print(f"   - {issue}")

if not user_fixes:
    print("\n✅ All users have correct case sensitivity!")
else:
    print(f"\n⚠️  Found {len(user_fixes)} users with case issues")

# ============================================================================
# 2. CHECK AND FIX PROFILE DATA
# ============================================================================
print("\n" + "="*80)
print("📋 PART 2: CHECKING PROFILE DATA")
print("-" * 80)

profiles = Profile.objects.all()
profile_fixes = []

for profile in profiles:
    issues = []
    fixes = {}
    
    # Check gender (MUST be lowercase: 'male' or 'female')
    if profile.gender not in ['male', 'female']:
        issues.append(f"Gender not lowercase: '{profile.gender}'")
        if profile.gender.lower() in ['male', 'm']:
            fixes['gender'] = 'male'
        elif profile.gender.lower() in ['female', 'f']:
            fixes['gender'] = 'female'
    
    # Check name (should be Title Case)
    if profile.name and profile.name != profile.name.title():
        issues.append(f"Name not Title Case: '{profile.name}'")
        fixes['name'] = profile.name.title()
    
    # Check location (should be Title Case for cities)
    if profile.location:
        # Split by comma and title case each part
        location_parts = [part.strip().title() for part in profile.location.split(',')]
        correct_location = ', '.join(location_parts)
        if profile.location != correct_location:
            issues.append(f"Location case: '{profile.location}'")
            fixes['location'] = correct_location
    
    # Check occupation (should be Title Case)
    if profile.occupation and profile.occupation != profile.occupation.title():
        # Special handling for abbreviations like MBA, IAS, CA
        occupation = profile.occupation
        if not any(abbr in occupation for abbr in ['MBA', 'IAS', 'CA', 'MBBS', 'PhD', 'B.Tech', 'M.Tech']):
            if occupation != occupation.title():
                issues.append(f"Occupation not Title Case: '{occupation}'")
                fixes['occupation'] = occupation.title()
    
    # Check education (should be Title Case with abbreviations preserved)
    if profile.education:
        # Preserve common abbreviations
        education = profile.education
        # This is complex, we'll just flag it
        if education.islower() or education.isupper():
            if len(education) > 10:  # Not an abbreviation
                issues.append(f"Education case needs review: '{education}'")
    
    if issues:
        profile_fixes.append({
            'profile': profile,
            'issues': issues,
            'fixes': fixes
        })
        print(f"\n❌ Profile: {profile.name} (User: {profile.user.username})")
        for issue in issues:
            print(f"   - {issue}")

if not profile_fixes:
    print("\n✅ All profiles have correct case sensitivity!")
else:
    print(f"\n⚠️  Found {len(profile_fixes)} profiles with case issues")

# ============================================================================
# 3. APPLY FIXES
# ============================================================================
print("\n" + "="*80)
print("🔧 APPLYING FIXES")
print("-" * 80)

# Fix users
user_fixed_count = 0
for item in user_fixes:
    user = item['user']
    fixes = item['fixes']
    
    for field, value in fixes.items():
        setattr(user, field, value)
        print(f"✅ Fixed User {user.id} - {field}: {value}")
    
    user.save()
    user_fixed_count += 1

# Fix profiles
profile_fixed_count = 0
for item in profile_fixes:
    profile = item['profile']
    fixes = item['fixes']
    
    for field, value in fixes.items():
        setattr(profile, field, value)
        print(f"✅ Fixed Profile {profile.id} ({profile.name}) - {field}: {value}")
    
    profile.save()
    profile_fixed_count += 1

print(f"\n{'='*80}")
print(f"✅ SUMMARY")
print(f"{'='*80}")
print(f"Users fixed: {user_fixed_count}")
print(f"Profiles fixed: {profile_fixed_count}")

# ============================================================================
# 4. FINAL VERIFICATION
# ============================================================================
print("\n" + "="*80)
print("📊 FINAL VERIFICATION")
print("-" * 80)

print("\n✅ GENDER VALUES (All should be lowercase 'male' or 'female'):")
gender_check = Profile.objects.values_list('gender', flat=True).distinct()
for gender in gender_check:
    count = Profile.objects.filter(gender=gender).count()
    status = "✅" if gender in ['male', 'female'] else "❌"
    print(f"  {status} '{gender}': {count} profiles")

print("\n📋 SAMPLE USERS:")
for user in User.objects.all()[:10]:
    print(f"  ID: {user.id:2} | Username: {user.username:20} | Email: {user.email:30} | Name: {user.first_name} {user.last_name}")

print("\n📋 SAMPLE PROFILES:")
for profile in Profile.objects.all()[:10]:
    print(f"  {profile.name:25} | Gender: {profile.gender:6} | Age: {profile.age:2} | Location: {profile.location}")

print("\n" + "="*80)
print("✅ CASE SENSITIVITY CHECK COMPLETE!")
print("="*80)
