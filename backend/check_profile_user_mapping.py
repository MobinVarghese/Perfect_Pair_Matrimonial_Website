import os
import django
import sys

sys.path.insert(0, 'D:/Matrimonial_Site/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile

print("Profile ID → User ID Mapping:")
print("=" * 60)

profiles = Profile.objects.all().order_by('id')
for profile in profiles:
    print(f"Profile ID: {profile.id:2d} | User ID: {profile.user.id:2d} | Username: {profile.user.username:20s} | Name: {profile.user.first_name} {profile.user.last_name}")

print("\n" + "=" * 60)
print("\nProblem: When frontend sends Profile ID 12, backend receives it as User ID 12")
print("This causes interest to be sent to the WRONG person!")
print("\nProfile ID 12 should map to User:", Profile.objects.get(id=12).user.username)
print("But User ID 12 is:", User.objects.get(id=12).username)
