import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection

print("\n" + "="*80)
print("DATABASE MIGRATION: ADD DATE_OF_BIRTH TO PROFILE")
print("="*80)

# Add date_of_birth column to Profile table
with connection.cursor() as cursor:
    # Check if column already exists
    cursor.execute("PRAGMA table_info(users_profile)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'date_of_birth' in columns:
        print("\n✅ Column 'date_of_birth' already exists in users_profile table")
    else:
        print("\n🔧 Adding 'date_of_birth' column to users_profile table...")
        cursor.execute("""
            ALTER TABLE users_profile 
            ADD COLUMN date_of_birth DATE NULL
        """)
        print("✅ Column 'date_of_birth' added successfully!")

    # Verify
    cursor.execute("PRAGMA table_info(users_profile)")
    columns_info = cursor.fetchall()
    print("\n📋 Current Profile table structure:")
    for col in columns_info:
        print(f"  - {col[1]}: {col[2]}")

print("\n" + "="*80)
print("✅ DATABASE MIGRATION COMPLETE!")
print("="*80)
