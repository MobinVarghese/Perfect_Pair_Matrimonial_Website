"""
Professional User Population Script
Generates realistic, diverse user profiles for impressive data exports
"""

import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Profile, Interest
from django.contrib.auth.hashers import make_password
from django.utils import timezone

# Professional data sets
INDIAN_CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 
    'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat',
    'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane',
    'Bhopal', 'Visakhapatnam', 'Pimpri-Chinchwad', 'Patna', 'Vadodara'
]

OCCUPATIONS = [
    'Software Engineer', 'Data Scientist', 'Product Manager', 'Business Analyst',
    'Marketing Manager', 'Financial Analyst', 'HR Manager', 'Consultant',
    'Architect', 'Civil Engineer', 'Mechanical Engineer', 'Doctor',
    'Chartered Accountant', 'Bank Manager', 'Teacher', 'Professor',
    'Graphic Designer', 'Content Writer', 'Sales Manager', 'Operations Manager',
    'Project Manager', 'Quality Analyst', 'Research Scientist', 'Pharmacist',
    'Lawyer', 'Journalist', 'Chef', 'Interior Designer', 'Fashion Designer',
    'Digital Marketing Specialist', 'Cloud Architect', 'DevOps Engineer'
]

EDUCATION_LEVELS = [
    'B.Tech', 'M.Tech', 'MBA', 'BBA', 'MCA', 'B.Sc', 'M.Sc',
    'B.Com', 'M.Com', 'B.A', 'M.A', 'BCA', 'PhD',
    'MBBS', 'B.Pharm', 'M.Pharm', 'LLB', 'CA', 'B.E', 'M.E'
]

MALE_FIRST_NAMES = [
    'Arjun', 'Rohan', 'Aditya', 'Vikas', 'Rahul', 'Amit', 'Karan', 'Siddharth',
    'Rajesh', 'Vikram', 'Aakash', 'Nikhil', 'Ankit', 'Varun', 'Harsh',
    'Prateek', 'Akshay', 'Abhishek', 'Suresh', 'Ravi', 'Deepak', 'Manoj',
    'Gaurav', 'Sandeep', 'Ajay', 'Vishal', 'Ashish', 'Naveen', 'Pankaj', 'Sanjay',
    'Dev', 'Kunal', 'Sahil', 'Mohit', 'Neel', 'Pranav', 'Ritesh', 'Shubham'
]

FEMALE_FIRST_NAMES = [
    'Priya', 'Ananya', 'Sneha', 'Neha', 'Pooja', 'Kavya', 'Riya', 'Simran',
    'Anjali', 'Divya', 'Shruti', 'Isha', 'Meera', 'Sakshi', 'Ritika',
    'Nikita', 'Swati', 'Preeti', 'Deepika', 'Komal', 'Manisha', 'Sonal',
    'Rekha', 'Pallavi', 'Nisha', 'Srishti', 'Aditi', 'Tanvi', 'Aarti', 'Shweta',
    'Megha', 'Radhika', 'Aishwarya', 'Shreya', 'Tanya', 'Vidya', 'Jyoti', 'Sapna'
]

LAST_NAMES = [
    'Sharma', 'Verma', 'Singh', 'Kumar', 'Patel', 'Gupta', 'Reddy', 'Rao',
    'Krishnan', 'Iyer', 'Nair', 'Menon', 'Pillai', 'Agarwal', 'Jain',
    'Chopra', 'Kapoor', 'Malhotra', 'Bhatia', 'Khanna', 'Arora', 'Sethi',
    'Mehta', 'Shah', 'Desai', 'Kulkarni', 'Joshi', 'Deshpande', 'Patil',
    'Naik', 'Sinha', 'Mishra', 'Pandey', 'Tiwari', 'Dubey', 'Yadav'
]

HOBBIES = [
    'Reading, Traveling, Photography',
    'Music, Dancing, Cooking',
    'Sports, Fitness, Yoga',
    'Painting, Art, Crafts',
    'Gaming, Technology, Gadgets',
    'Movies, Series, Theater',
    'Hiking, Adventure Sports, Trekking',
    'Writing, Blogging, Poetry',
    'Gardening, Nature, Environment',
    'Volunteering, Social Work, NGO Activities'
]

BIO_TEMPLATES = [
    "Looking for a life partner who shares similar values and interests. Believe in mutual respect and understanding.",
    "Family-oriented professional seeking meaningful connection. Value honesty, loyalty, and communication.",
    "Ambitious and driven, yet grounded in traditions. Looking for someone to share life's journey.",
    "Passionate about career and personal growth. Seeking a partner who values both independence and togetherness.",
    "Believer in balancing modern outlook with traditional values. Looking for a compatible life partner.",
    "Down-to-earth professional with strong family values. Seeking genuine connection and companionship.",
    "Optimistic and positive person looking for someone special to build a future together.",
    "Career-focused yet family-oriented. Seeking a supportive and understanding life partner."
]

def generate_phone_number():
    """Generate realistic Indian mobile number"""
    prefixes = ['98', '97', '96', '95', '94', '93', '92', '91', '90', '89', '88', '87', '86', '85']
    return f"+91{random.choice(prefixes)}{random.randint(10000000, 99999999)}"

def generate_email(first_name, last_name):
    """Generate professional email"""
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
    patterns = [
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name.lower()}{last_name.lower()}",
        f"{first_name.lower()}{random.randint(1, 999)}",
        f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 99)}"
    ]
    return f"{random.choice(patterns)}@{random.choice(domains)}"

def create_professional_users(count=50):
    """Create professional user profiles"""
    
    print(f"🚀 Starting to create {count} professional users...")
    print("=" * 60)
    
    created_users = []
    created_profiles = []
    
    for i in range(count):
        # Randomly choose gender (balanced distribution)
        gender = 'M' if i % 2 == 0 else 'F'
        
        # Select names
        first_name = random.choice(MALE_FIRST_NAMES if gender == 'M' else FEMALE_FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"
        
        # Generate username
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            username = f"{username}{random.randint(1000, 9999)}"
        
        # Generate email
        email = generate_email(first_name, last_name)
        
        # Check if email exists
        if User.objects.filter(email=email).exists():
            email = f"{first_name.lower()}{random.randint(1000, 9999)}@gmail.com"
        
        try:
            # Create User
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password('password123'),  # Default password
                is_active=True,
                date_joined=timezone.now() - timedelta(days=random.randint(1, 365))
            )
            
            # Generate realistic age (23-40 for professionals)
            age = random.randint(23, 40)
            
            # Select education and occupation that make sense
            education = random.choice(EDUCATION_LEVELS)
            occupation = random.choice(OCCUPATIONS)
            
            # Location (weighted towards major cities)
            location = random.choices(
                INDIAN_CITIES,
                weights=[15, 12, 12, 10, 10, 8, 8, 6, 5, 5, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2],
                k=1
            )[0]
            
            # Create Profile (using actual model fields)
            profile = Profile.objects.create(
                user=user,
                name=full_name,
                age=age,
                gender='male' if gender == 'M' else 'female',  # Use lowercase
                location=location,
                occupation=occupation,
                education=education,
                mobile_number=generate_phone_number(),
                about=random.choice(BIO_TEMPLATES),
                desired_partner_traits=random.choice([
                    "Looking for educated, family-oriented partner with similar values",
                    "Seeking understanding and supportive life partner",
                    "Want partner who respects both traditions and modern outlook",
                    "Looking for someone with good values and career goals"
                ]),
                height=round(random.uniform(5.2, 6.2), 2) if gender == 'M' else round(random.uniform(4.10, 5.8), 2)
            )
            
            created_users.append(user)
            created_profiles.append(profile)
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"✅ Created {i + 1}/{count} users...")
                
        except Exception as e:
            print(f"❌ Error creating user {i+1}: {str(e)}")
            continue
    
    print("=" * 60)
    print(f"✅ Successfully created {len(created_users)} users and profiles!")
    
    # Create some realistic interests
    print("\n🔗 Creating realistic interests between users...")
    create_interests(created_profiles)
    
    # Print statistics
    print_statistics()

def create_interests(profiles, interest_count=80):
    """Create realistic interest connections"""
    
    created = 0
    attempts = 0
    max_attempts = interest_count * 3
    
    while created < interest_count and attempts < max_attempts:
        attempts += 1
        
        # Pick random sender and receiver
        sender_profile = random.choice(profiles)
        receiver_profile = random.choice(profiles)
        
        # Ensure different users and opposite gender (realistic for matrimonial)
        if (sender_profile.user.id != receiver_profile.user.id and 
            sender_profile.gender != receiver_profile.gender):
            
            # Check if interest already exists
            if not Interest.objects.filter(
                sender=sender_profile.user,
                receiver=receiver_profile.user
            ).exists():
                
                # Random status (60% pending, 25% accepted, 15% rejected)
                status_choice = random.choices(
                    ['pending', 'accepted', 'rejected'],
                    weights=[60, 25, 15],
                    k=1
                )[0]
                
                # Create interest
                interest = Interest.objects.create(
                    sender=sender_profile.user,
                    receiver=receiver_profile.user,
                    status=status_choice,
                    created_at=timezone.now() - timedelta(days=random.randint(1, 180))
                )
                
                # If accepted or rejected, set response date
                if status_choice in ['accepted', 'rejected']:
                    interest.responded_at = interest.created_at + timedelta(days=random.randint(1, 30))
                    interest.save()
                
                created += 1
                
                if created % 20 == 0:
                    print(f"✅ Created {created}/{interest_count} interests...")
    
    print(f"✅ Successfully created {created} interests!")

def print_statistics():
    """Print database statistics"""
    
    print("\n" + "=" * 60)
    print("📊 DATABASE STATISTICS")
    print("=" * 60)
    
    # User statistics
    total_users = User.objects.count()
    male_users = Profile.objects.filter(gender='M').count()
    female_users = Profile.objects.filter(gender='F').count()
    
    print(f"\n👥 USERS:")
    print(f"   Total Users: {total_users}")
    print(f"   Male: {male_users} ({male_users/total_users*100:.1f}%)")
    print(f"   Female: {female_users} ({female_users/total_users*100:.1f}%)")
    
    # Location statistics
    print(f"\n📍 TOP 5 LOCATIONS:")
    locations = Profile.objects.values('location').annotate(
        count=django.db.models.Count('id')
    ).order_by('-count')[:5]
    for loc in locations:
        print(f"   {loc['location']}: {loc['count']} users")
    
    # Age statistics
    print(f"\n📅 AGE DISTRIBUTION:")
    age_ranges = [
        ('23-25', 23, 25),
        ('26-30', 26, 30),
        ('31-35', 31, 35),
        ('36-40', 36, 40)
    ]
    for label, min_age, max_age in age_ranges:
        count = Profile.objects.filter(age__gte=min_age, age__lte=max_age).count()
        print(f"   {label}: {count} users")
    
    # Interest statistics
    total_interests = Interest.objects.count()
    pending = Interest.objects.filter(status='pending').count()
    accepted = Interest.objects.filter(status='accepted').count()
    rejected = Interest.objects.filter(status='rejected').count()
    
    print(f"\n💕 INTERESTS:")
    print(f"   Total: {total_interests}")
    print(f"   Pending: {pending}")
    print(f"   Accepted: {accepted} ({accepted/total_interests*100:.1f}% acceptance rate)" if total_interests > 0 else "   Accepted: 0")
    print(f"   Rejected: {rejected}")
    
    print("\n" + "=" * 60)
    print("✨ Data population complete! Ready for impressive exports!")
    print("=" * 60)

if __name__ == '__main__':
    import django.db.models
    
    print("\n" + "🎓 PROFESSIONAL USER POPULATION SCRIPT".center(60))
    print("For Impressive Mini Project Data Exports\n")
    
    # Ask for confirmation
    response = input("This will create 50 professional users. Continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        create_professional_users(50)
        print("\n✅ All done! Now you can export impressive statistics from admin panel!")
        print("🔗 Visit: http://127.0.0.1:8000/admin/users/profile/")
        print("📊 Use 'Export platform statistics' action for your mini project!")
    else:
        print("❌ Operation cancelled.")
