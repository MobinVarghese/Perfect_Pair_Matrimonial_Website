import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile
from datetime import date

def create_sample_profiles():
    # Sample male profiles
    male_profiles = [
        {
            'username': 'john_doe', 'email': 'john@example.com', 'password': 'pass123',
            'first_name': 'John', 'last_name': 'Doe',
            'name': 'John Doe', 'gender': 'male', 'age': 28,
            'occupation': 'Software Engineer', 'education': "Bachelor's in Computer Science",
            'height': 5.10, 'location': 'Mumbai, India', 'mobile_number': '+911234567801',
            'about': 'Passionate about technology and traveling. Looking for a life partner who shares similar interests.'
        },
        {
            'username': 'alex_smith', 'email': 'alex@example.com', 'password': 'pass123',
            'first_name': 'Alex', 'last_name': 'Smith',
            'name': 'Alex Smith', 'gender': 'male', 'age': 32,
            'occupation': 'Doctor', 'education': 'MBBS, MD',
            'height': 6.00, 'location': 'Delhi, India', 'mobile_number': '+911234567802',
            'about': 'Medical professional with a caring nature. Love reading and music.'
        },
        {
            'username': 'mike_brown', 'email': 'mike@example.com', 'password': 'pass123',
            'first_name': 'Mike', 'last_name': 'Brown',
            'name': 'Mike Brown', 'gender': 'male', 'age': 30,
            'occupation': 'Business Analyst', 'education': 'MBA',
            'height': 5.09, 'location': 'Bangalore, India', 'mobile_number': '+911234567803',
            'about': 'Ambitious professional seeking a supportive and understanding partner.'
        },
        {
            'username': 'david_wilson', 'email': 'david@example.com', 'password': 'pass123',
            'first_name': 'David', 'last_name': 'Wilson',
            'name': 'David Wilson', 'gender': 'male', 'age': 27,
            'occupation': 'Civil Engineer', 'education': 'B.Tech in Civil Engineering',
            'height': 5.11, 'location': 'Pune, India', 'mobile_number': '+911234567804',
            'about': 'Love outdoors and adventure sports. Looking for someone with positive energy.'
        },
        {
            'username': 'james_taylor', 'email': 'james@example.com', 'password': 'pass123',
            'first_name': 'James', 'last_name': 'Taylor',
            'name': 'James Taylor', 'gender': 'male', 'age': 35,
            'occupation': 'Architect', 'education': "Master's in Architecture",
            'height': 6.01, 'location': 'Chennai, India', 'mobile_number': '+911234567805',
            'about': 'Creative thinker with a passion for design. Family oriented person.'
        }
    ]

    # Sample female profiles
    female_profiles = [
        {
            'username': 'sarah_jones', 'email': 'sarah@example.com', 'password': 'pass123',
            'first_name': 'Sarah', 'last_name': 'Jones',
            'name': 'Sarah Jones', 'gender': 'female', 'age': 26,
            'occupation': 'Teacher', 'education': 'B.Ed, M.A. in English',
            'height': 5.05, 'location': 'Mumbai, India', 'mobile_number': '+911234567806',
            'about': 'Passionate about education and helping others. Love reading and cooking.'
        },
        {
            'username': 'emily_davis', 'email': 'emily@example.com', 'password': 'pass123',
            'first_name': 'Emily', 'last_name': 'Davis',
            'name': 'Emily Davis', 'gender': 'female', 'age': 29,
            'occupation': 'Software Developer', 'education': "Bachelor's in IT",
            'height': 5.04, 'location': 'Bangalore, India', 'mobile_number': '+911234567807',
            'about': 'Tech enthusiast who loves coding and yoga. Seeking a understanding partner.'
        },
        {
            'username': 'jessica_miller', 'email': 'jessica@example.com', 'password': 'pass123',
            'first_name': 'Jessica', 'last_name': 'Miller',
            'name': 'Jessica Miller', 'gender': 'female', 'age': 31,
            'occupation': 'Marketing Manager', 'education': 'MBA in Marketing',
            'height': 5.06, 'location': 'Delhi, India', 'mobile_number': '+911234567808',
            'about': 'Creative and outgoing personality. Love traveling and photography.'
        },
        {
            'username': 'rachel_white', 'email': 'rachel@example.com', 'password': 'pass123',
            'first_name': 'Rachel', 'last_name': 'White',
            'name': 'Rachel White', 'gender': 'female', 'age': 28,
            'occupation': 'Graphic Designer', 'education': "Bachelor's in Design",
            'height': 5.03, 'location': 'Pune, India', 'mobile_number': '+911234567809',
            'about': 'Artistic soul who loves painting and music. Family is everything to me.'
        },
        {
            'username': 'lisa_anderson', 'email': 'lisa@example.com', 'password': 'pass123',
            'first_name': 'Lisa', 'last_name': 'Anderson',
            'name': 'Lisa Anderson', 'gender': 'female', 'age': 27,
            'occupation': 'HR Manager', 'education': 'MBA in HR',
            'height': 5.05, 'location': 'Hyderabad, India', 'mobile_number': '+911234567810',
            'about': 'People person with good communication skills. Love dancing and fitness.'
        }
    ]

    all_profiles = male_profiles + female_profiles
    created_count = 0

    for profile_data in all_profiles:
        # Check if user already exists
        if User.objects.filter(username=profile_data['username']).exists():
            print(f"⚠️  User {profile_data['username']} already exists, skipping...")
            continue

        try:
            # Create user
            user = User.objects.create_user(
                username=profile_data['username'],
                email=profile_data['email'],
                password=profile_data['password'],
                first_name=profile_data['first_name'],
                last_name=profile_data['last_name']
            )

            # Create profile
            Profile.objects.create(
                user=user,
                name=profile_data['name'],
                gender=profile_data['gender'],
                age=profile_data['age'],
                occupation=profile_data['occupation'],
                education=profile_data['education'],
                height=profile_data['height'],
                location=profile_data['location'],
                mobile_number=profile_data['mobile_number'],
                about=profile_data['about']
            )

            print(f"✅ Created profile for {profile_data['name']} ({profile_data['gender']})")
            created_count += 1

        except Exception as e:
            print(f"❌ Error creating {profile_data['username']}: {str(e)}")

    print(f"\n🎉 Successfully created {created_count} sample profiles!")
    print("\n📝 Profile Summary:")
    print(f"   Male profiles: {Profile.objects.filter(gender='male').count()}")
    print(f"   Female profiles: {Profile.objects.filter(gender='female').count()}")
    print(f"   Total profiles: {Profile.objects.count()}")

if __name__ == '__main__':
    create_sample_profiles()
