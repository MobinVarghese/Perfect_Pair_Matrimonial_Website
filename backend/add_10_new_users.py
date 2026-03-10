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
    """Create 10 new professional users with realistic data"""
    
    users_data = [
        {
            'username': 'divya_krishnan',
            'email': 'divya.krishnan@email.com',
            'first_name': 'Divya',
            'last_name': 'Krishnan',
            'profile': {
                'name': 'Divya Krishnan',
                'gender': 'female',
                'age': 26,
                'location': 'Coimbatore, Tamil Nadu',
                'occupation': 'UI/UX Designer',
                'education': 'B.Des in Design',
                'mobile_number': '+91-9876543220',
                'about': 'Creative designer passionate about user experience. Looking for a partner who appreciates art and creativity.',
                'height': 5.3,
                'desired_partner_traits': 'Seeking someone creative, understanding, and supportive of artistic pursuits.'
            }
        },
        {
            'username': 'karan_malhotra',
            'email': 'karan.malhotra@email.com',
            'first_name': 'Karan',
            'last_name': 'Malhotra',
            'profile': {
                'name': 'Karan Malhotra',
                'gender': 'male',
                'age': 33,
                'location': 'Chandigarh, Punjab',
                'occupation': 'Civil Engineer',
                'education': 'B.Tech in Civil Engineering',
                'mobile_number': '+91-9876543221',
                'about': 'Civil engineer working on infrastructure projects. Value honesty and commitment in relationships.',
                'height': 6.1,
                'desired_partner_traits': 'Looking for a caring and family-oriented partner who values stability.'
            }
        },
        {
            'username': 'pooja_agarwal',
            'email': 'pooja.agarwal@email.com',
            'first_name': 'Pooja',
            'last_name': 'Agarwal',
            'profile': {
                'name': 'Pooja Agarwal',
                'gender': 'female',
                'age': 29,
                'location': 'Jaipur, Rajasthan',
                'occupation': 'Fashion Designer',
                'education': 'Diploma in Fashion Design',
                'mobile_number': '+91-9876543222',
                'about': 'Fashion designer with my own boutique. Looking for someone who respects my passion and career.',
                'height': 5.5,
                'desired_partner_traits': 'Seeking a supportive partner who appreciates creativity and entrepreneurship.'
            }
        },
        {
            'username': 'siddharth_rao',
            'email': 'siddharth.rao@email.com',
            'first_name': 'Siddharth',
            'last_name': 'Rao',
            'profile': {
                'name': 'Siddharth Rao',
                'gender': 'male',
                'age': 30,
                'location': 'Visakhapatnam, Andhra Pradesh',
                'occupation': 'Marine Engineer',
                'education': 'B.Tech in Marine Engineering',
                'mobile_number': '+91-9876543223',
                'about': 'Marine engineer working in shipping industry. Love to travel and explore different cultures.',
                'height': 5.10,
                'desired_partner_traits': 'Looking for an understanding partner who can adapt to my travel schedule.'
            }
        },
        {
            'username': 'ritu_saxena',
            'email': 'ritu.saxena@email.com',
            'first_name': 'Ritu',
            'last_name': 'Saxena',
            'profile': {
                'name': 'Ritu Saxena',
                'gender': 'female',
                'age': 24,
                'location': 'Lucknow, Uttar Pradesh',
                'occupation': 'Teacher',
                'education': 'B.Ed + M.A. in English',
                'mobile_number': '+91-9876543224',
                'about': 'School teacher passionate about education. Believe in traditional values and joint family system.',
                'height': 5.4,
                'desired_partner_traits': 'Seeking a well-educated partner who values family and education.'
            }
        },
        {
            'username': 'manish_kumar',
            'email': 'manish.kumar@email.com',
            'first_name': 'Manish',
            'last_name': 'Kumar',
            'profile': {
                'name': 'Manish Kumar',
                'gender': 'male',
                'age': 35,
                'location': 'Patna, Bihar',
                'occupation': 'Government Officer (IAS)',
                'education': 'M.A. in Public Administration',
                'mobile_number': '+91-9876543225',
                'about': 'Civil services officer dedicated to public service. Looking for a life partner who shares similar values.',
                'height': 5.9,
                'desired_partner_traits': 'Seeking an educated and socially conscious partner.'
            }
        },
        {
            'username': 'meera_iyer',
            'email': 'meera.iyer@email.com',
            'first_name': 'Meera',
            'last_name': 'Iyer',
            'profile': {
                'name': 'Meera Iyer',
                'gender': 'female',
                'age': 27,
                'location': 'Mysore, Karnataka',
                'occupation': 'Pharmacist',
                'education': 'B.Pharm',
                'mobile_number': '+91-9876543226',
                'about': 'Pharmacist working at a reputed hospital. Value health, wellness, and family bonding.',
                'height': 5.5,
                'desired_partner_traits': 'Looking for a health-conscious and family-oriented partner.'
            }
        },
        {
            'username': 'aditya_bhatt',
            'email': 'aditya.bhatt@email.com',
            'first_name': 'Aditya',
            'last_name': 'Bhatt',
            'profile': {
                'name': 'Aditya Bhatt',
                'gender': 'male',
                'age': 28,
                'location': 'Indore, Madhya Pradesh',
                'occupation': 'Mechanical Engineer',
                'education': 'B.Tech in Mechanical Engineering',
                'mobile_number': '+91-9876543227',
                'about': 'Mechanical engineer in automobile industry. Enjoy reading and sports. Looking for compatible match.',
                'height': 5.11,
                'desired_partner_traits': 'Seeking someone who is independent yet values family traditions.'
            }
        },
        {
            'username': 'sakshi_chauhan',
            'email': 'sakshi.chauhan@email.com',
            'first_name': 'Sakshi',
            'last_name': 'Chauhan',
            'profile': {
                'name': 'Sakshi Chauhan',
                'gender': 'female',
                'age': 25,
                'location': 'Dehradun, Uttarakhand',
                'occupation': 'Content Writer',
                'education': 'M.A. in Journalism',
                'mobile_number': '+91-9876543228',
                'about': 'Freelance content writer and blogger. Love reading, writing, and nature. Looking for intellectual companionship.',
                'height': 5.6,
                'desired_partner_traits': 'Seeking an intellectual partner who enjoys meaningful conversations.'
            }
        },
        {
            'username': 'varun_pillai',
            'email': 'varun.pillai@email.com',
            'first_name': 'Varun',
            'last_name': 'Pillai',
            'profile': {
                'name': 'Varun Pillai',
                'gender': 'male',
                'age': 31,
                'location': 'Thiruvananthapuram, Kerala',
                'occupation': 'Bank Manager',
                'education': 'MBA in Banking & Finance',
                'mobile_number': '+91-9876543229',
                'about': 'Banking professional with stable career. Believe in work-life balance and quality time with family.',
                'height': 5.8,
                'desired_partner_traits': 'Looking for a well-educated partner who values financial stability and family life.'
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
    male_count = Profile.objects.filter(gender='male').count()
    female_count = Profile.objects.filter(gender='female').count()
    
    print(f"\n📊 DATABASE SUMMARY:")
    print(f"Total Users: {total_users}")
    print(f"Total Profiles: {total_profiles}")
    print(f"Male: {male_count} ({male_count/total_profiles*100:.1f}%)")
    print(f"Female: {female_count} ({female_count/total_profiles*100:.1f}%)")
    
    # Location distribution
    print(f"\n📍 TOP LOCATIONS:")
    from django.db.models import Count
    locations = Profile.objects.values('location').annotate(count=Count('id')).order_by('-count')[:8]
    for loc in locations:
        print(f"  {loc['location']}: {loc['count']} users")

if __name__ == '__main__':
    print("🚀 Starting user population script...\n")
    create_users()
    print("\n✅ Script completed!")
    print("\n💡 Default password for all users: password123")
    print("🔐 Admin credentials: admin / admin123")
