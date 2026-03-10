import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile
from django.contrib.auth.hashers import make_password

def create_users():
    """Create 10 professional users with realistic data"""
    
    users_data = [
        {
            'username': 'priya_sharma',
            'email': 'priya.sharma@email.com',
            'first_name': 'Priya',
            'last_name': 'Sharma',
            'profile': {
                'name': 'Priya Sharma',
                'gender': 'female',
                'age': 27,
                'location': 'Mumbai, Maharashtra',
                'occupation': 'Software Engineer',
                'education': 'B.Tech in Computer Science',
                'mobile_number': '+91-9876543210',
                'about': 'Tech professional working at a leading IT company. Looking for a life partner who values family and career.',
                'height': 5.5,
                'desired_partner_traits': 'Looking for someone who is well-educated, family-oriented, and supportive.'
            }
        },
        {
            'username': 'rahul_verma',
            'email': 'rahul.verma@email.com',
            'first_name': 'Rahul',
            'last_name': 'Verma',
            'profile': {
                'name': 'Rahul Verma',
                'gender': 'male',
                'age': 30,
                'location': 'Delhi, India',
                'occupation': 'Business Analyst',
                'education': 'MBA in Finance',
                'mobile_number': '+91-9876543211',
                'about': 'MBA graduate working in corporate sector. Family-oriented and looking for a caring partner.',
                'height': 5.10,
                'desired_partner_traits': 'Seeking a caring and understanding partner who values family traditions.'
            }
        },
        {
            'username': 'anjali_patel',
            'email': 'anjali.patel@email.com',
            'first_name': 'Anjali',
            'last_name': 'Patel',
            'profile': {
                'name': 'Anjali Patel',
                'gender': 'female',
                'age': 26,
                'location': 'Bangalore, Karnataka',
                'occupation': 'Data Scientist',
                'education': 'M.Tech in Data Science',
                'mobile_number': '+91-9876543212',
                'about': 'Data science professional passionate about AI/ML. Looking for an understanding life partner.',
                'height': 5.4,
                'desired_partner_traits': 'Seeking a partner who is intellectually curious and supportive of career goals.'
            }
        },
        {
            'username': 'vikram_singh',
            'email': 'vikram.singh@email.com',
            'first_name': 'Vikram',
            'last_name': 'Singh',
            'profile': {
                'name': 'Vikram Singh',
                'gender': 'male',
                'age': 32,
                'location': 'Pune, Maharashtra',
                'occupation': 'Senior Manager',
                'education': 'MBA from IIM',
                'mobile_number': '+91-9876543213',
                'about': 'Senior management professional. Believe in traditional values with modern outlook.',
                'height': 6.0,
                'desired_partner_traits': 'Looking for an educated and independent partner with strong family values.'
            }
        },
        {
            'username': 'neha_kapoor',
            'email': 'neha.kapoor@email.com',
            'first_name': 'Neha',
            'last_name': 'Kapoor',
            'profile': {
                'name': 'Neha Kapoor',
                'gender': 'female',
                'age': 28,
                'location': 'Chennai, Tamil Nadu',
                'occupation': 'Product Manager',
                'education': 'B.Tech + MBA',
                'mobile_number': '+91-9876543214',
                'about': 'Product manager at tech startup. Looking for someone who shares similar values and ambitions.',
                'height': 5.6,
                'desired_partner_traits': 'Seeking an ambitious and caring partner who values mutual growth.'
            }
        },
        {
            'username': 'amit_gupta',
            'email': 'amit.gupta@email.com',
            'first_name': 'Amit',
            'last_name': 'Gupta',
            'profile': {
                'name': 'Amit Gupta',
                'gender': 'male',
                'age': 29,
                'location': 'Mumbai, Maharashtra',
                'occupation': 'Chartered Accountant',
                'education': 'CA + B.Com',
                'mobile_number': '+91-9876543215',
                'about': 'CA by profession. Family values are important to me. Looking for a supportive life partner.',
                'height': 5.8,
                'desired_partner_traits': 'Looking for a well-educated and family-oriented partner.'
            }
        },
        {
            'username': 'kavya_reddy',
            'email': 'kavya.reddy@email.com',
            'first_name': 'Kavya',
            'last_name': 'Reddy',
            'profile': {
                'name': 'Kavya Reddy',
                'gender': 'female',
                'age': 25,
                'location': 'Hyderabad, Telangana',
                'occupation': 'HR Manager',
                'education': 'MBA in HR',
                'mobile_number': '+91-9876543216',
                'about': 'HR professional with people skills. Believe in building strong relationships and mutual respect.',
                'height': 5.5,
                'desired_partner_traits': 'Seeking someone who values communication and mutual respect in relationships.'
            }
        },
        {
            'username': 'rohan_mehta',
            'email': 'rohan.mehta@email.com',
            'first_name': 'Rohan',
            'last_name': 'Mehta',
            'profile': {
                'name': 'Rohan Mehta',
                'gender': 'male',
                'age': 31,
                'location': 'Bangalore, Karnataka',
                'occupation': 'Software Architect',
                'education': 'M.S. in Computer Science',
                'mobile_number': '+91-9876543217',
                'about': 'Senior tech professional. Enjoy traveling and exploring new places. Looking for a compatible partner.',
                'height': 5.11,
                'desired_partner_traits': 'Looking for someone who enjoys adventure and values work-life balance.'
            }
        },
        {
            'username': 'sneha_joshi',
            'email': 'sneha.joshi@email.com',
            'first_name': 'Sneha',
            'last_name': 'Joshi',
            'profile': {
                'name': 'Sneha Joshi',
                'gender': 'female',
                'age': 27,
                'location': 'Delhi, India',
                'occupation': 'Doctor (MBBS)',
                'education': 'MBBS',
                'mobile_number': '+91-9876543218',
                'about': 'Medical professional dedicated to healthcare. Looking for an understanding and supportive partner.',
                'height': 5.4,
                'desired_partner_traits': 'Seeking a supportive partner who understands the demands of medical profession.'
            }
        },
        {
            'username': 'arjun_nair',
            'email': 'arjun.nair@email.com',
            'first_name': 'Arjun',
            'last_name': 'Nair',
            'profile': {
                'name': 'Arjun Nair',
                'gender': 'male',
                'age': 28,
                'location': 'Kochi, Kerala',
                'occupation': 'Marketing Manager',
                'education': 'MBA in Marketing',
                'mobile_number': '+91-9876543219',
                'about': 'Marketing professional with creative mindset. Believe in balanced life and strong family bonds.',
                'height': 5.9,
                'desired_partner_traits': 'Looking for a creative and family-oriented partner who values traditions.'
            }
        }
    ]
    
    created_count = 0
    
    for user_data in users_data:
        try:
            # Check if user already exists
            if User.objects.filter(username=user_data['username']).exists():
                print(f"❌ User {user_data['username']} already exists, skipping...")
                continue
            
            # Create user
            user = User.objects.create(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password=make_password('password123'),  # Default password
                is_active=True
            )
            
            # Create profile
            profile = Profile.objects.create(
                user=user,
                **user_data['profile']
            )
            
            created_count += 1
            print(f"✅ Created: {user_data['profile']['name']} ({user_data['profile']['gender']}, {user_data['profile']['age']}, {user_data['profile']['location']})")
            
        except Exception as e:
            print(f"❌ Error creating {user_data['username']}: {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully created {created_count} new users!")
    print(f"{'='*60}")
    
    # Show summary statistics
    total_users = User.objects.count()
    total_profiles = Profile.objects.count()
    male_count = Profile.objects.filter(gender='M').count()
    female_count = Profile.objects.filter(gender='F').count()
    
    print(f"\n📊 DATABASE SUMMARY:")
    print(f"Total Users: {total_users}")
    print(f"Total Profiles: {total_profiles}")
    print(f"Male: {male_count} ({male_count/total_profiles*100:.1f}%)")
    print(f"Female: {female_count} ({female_count/total_profiles*100:.1f}%)")
    
    # Location distribution
    print(f"\n📍 TOP LOCATIONS:")
    from django.db.models import Count
    locations = Profile.objects.values('location').annotate(count=Count('id')).order_by('-count')[:5]
    for loc in locations:
        print(f"  {loc['location']}: {loc['count']} users")

if __name__ == '__main__':
    print("🚀 Starting user population script...\n")
    create_users()
    print("\n✅ Script completed!")
    print("\n💡 Default password for all users: password123")
    print("🔐 Admin credentials: admin / admin123")
