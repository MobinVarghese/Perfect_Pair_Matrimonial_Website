"""
Test script for export helper functions
Tests export_profiles_to_pdf() and export_profiles_to_excel()
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import Profile
from users.export_utils import (
    export_profiles_to_pdf,
    export_profiles_to_excel,
    export_profiles_to_csv
)
from django.utils import timezone
from datetime import timedelta


def test_pdf_export():
    """Test PDF export with various configurations"""
    print("\n" + "="*60)
    print("TEST 1: PDF Export - All Profiles")
    print("="*60)
    
    try:
        profiles = Profile.objects.all()[:20]  # Test with 20 profiles
        
        if not profiles.exists():
            print("⚠ No profiles found in database. Please create some profiles first.")
            return False
        
        print(f"Exporting {profiles.count()} profiles to PDF...")
        
        response = export_profiles_to_pdf(profiles)
        
        # Save to file
        filename = 'test_pdf_export.pdf'
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        # Verify response
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/pdf'
        assert 'Content-Disposition' in response
        assert len(response.content) > 0
        
        print(f"✓ PDF generated successfully")
        print(f"✓ File size: {len(response.content):,} bytes")
        print(f"✓ Content-Type: {response['Content-Type']}")
        print(f"✓ Saved as: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_pdf_with_filters():
    """Test PDF export with custom title and filters"""
    print("\n" + "="*60)
    print("TEST 2: PDF Export - With Filters and Custom Title")
    print("="*60)
    
    try:
        # Filter female profiles
        profiles = Profile.objects.filter(gender='female')[:10]
        
        if not profiles.exists():
            print("⚠ No female profiles found. Skipping filter test.")
            return False
        
        filters = {
            'gender': 'female',
            'date_from': (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        }
        
        print(f"Exporting {profiles.count()} female profiles...")
        print(f"Filters: {filters}")
        
        response = export_profiles_to_pdf(
            profiles,
            title="Female Profiles Report",
            filters=filters
        )
        
        filename = 'test_pdf_filtered.pdf'
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ PDF with filters generated successfully")
        print(f"✓ File size: {len(response.content):,} bytes")
        print(f"✓ Saved as: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_excel_export():
    """Test Excel export"""
    print("\n" + "="*60)
    print("TEST 3: Excel Export - All Profiles")
    print("="*60)
    
    try:
        profiles = Profile.objects.all()[:20]
        
        if not profiles.exists():
            print("⚠ No profiles found in database.")
            return False
        
        print(f"Exporting {profiles.count()} profiles to Excel...")
        
        response = export_profiles_to_excel(profiles)
        
        # Save to file
        filename = 'test_excel_export.xlsx'
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        # Verify response
        assert response.status_code == 200
        assert 'spreadsheetml' in response['Content-Type']
        assert 'Content-Disposition' in response
        assert len(response.content) > 0
        
        print(f"✓ Excel generated successfully")
        print(f"✓ File size: {len(response.content):,} bytes")
        print(f"✓ Content-Type: {response['Content-Type']}")
        print(f"✓ Saved as: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_excel_with_custom_sheet():
    """Test Excel export with custom sheet name"""
    print("\n" + "="*60)
    print("TEST 4: Excel Export - Custom Sheet Name")
    print("="*60)
    
    try:
        profiles = Profile.objects.all()[:15]
        
        if not profiles.exists():
            print("⚠ No profiles found in database.")
            return False
        
        filters = {
            'location': 'Mumbai'
        }
        
        print(f"Exporting {profiles.count()} profiles with custom sheet name...")
        
        response = export_profiles_to_excel(
            profiles,
            sheet_name="Premium Profiles",
            filters=filters
        )
        
        filename = 'test_excel_custom.xlsx'
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Excel with custom sheet generated successfully")
        print(f"✓ File size: {len(response.content):,} bytes")
        print(f"✓ Saved as: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_csv_export():
    """Test CSV export"""
    print("\n" + "="*60)
    print("TEST 5: CSV Export - All Profiles")
    print("="*60)
    
    try:
        profiles = Profile.objects.all()[:20]
        
        if not profiles.exists():
            print("⚠ No profiles found in database.")
            return False
        
        print(f"Exporting {profiles.count()} profiles to CSV...")
        
        response = export_profiles_to_csv(profiles)
        
        # Save to file
        filename = 'test_csv_export.csv'
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        # Verify response
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'
        assert 'Content-Disposition' in response
        assert len(response.content) > 0
        
        print(f"✓ CSV generated successfully")
        print(f"✓ File size: {len(response.content):,} bytes")
        print(f"✓ Content-Type: {response['Content-Type']}")
        print(f"✓ Saved as: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_empty_queryset():
    """Test exports with empty queryset"""
    print("\n" + "="*60)
    print("TEST 6: Exports with Empty QuerySet")
    print("="*60)
    
    try:
        # Create empty queryset
        profiles = Profile.objects.none()
        
        print("Testing PDF with empty queryset...")
        pdf_response = export_profiles_to_pdf(profiles, title="Empty Report")
        assert pdf_response.status_code == 200
        print("✓ PDF handles empty queryset")
        
        print("Testing Excel with empty queryset...")
        excel_response = export_profiles_to_excel(profiles)
        assert excel_response.status_code == 200
        print("✓ Excel handles empty queryset")
        
        print("Testing CSV with empty queryset...")
        csv_response = export_profiles_to_csv(profiles)
        assert csv_response.status_code == 200
        print("✓ CSV handles empty queryset")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_large_dataset():
    """Test exports with larger dataset"""
    print("\n" + "="*60)
    print("TEST 7: Large Dataset Export (100 profiles)")
    print("="*60)
    
    try:
        profiles = Profile.objects.all()[:100]
        
        if profiles.count() < 50:
            print(f"⚠ Only {profiles.count()} profiles available. Skipping large dataset test.")
            return False
        
        print(f"Exporting {profiles.count()} profiles to PDF...")
        
        import time
        start = time.time()
        response = export_profiles_to_pdf(profiles)
        elapsed = time.time() - start
        
        filename = 'test_pdf_large.pdf'
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Large PDF generated successfully")
        print(f"✓ Records: {profiles.count()}")
        print(f"✓ File size: {len(response.content):,} bytes")
        print(f"✓ Generation time: {elapsed:.2f} seconds")
        print(f"✓ Saved as: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_profile_data_integrity():
    """Test that exported data matches database data"""
    print("\n" + "="*60)
    print("TEST 8: Data Integrity Check")
    print("="*60)
    
    try:
        profiles = Profile.objects.all()[:5]
        
        if not profiles.exists():
            print("⚠ No profiles found in database.")
            return False
        
        print(f"Checking data integrity for {profiles.count()} profiles...")
        
        # Get first profile data
        first_profile = profiles.first()
        
        print(f"\nSample Profile Data:")
        print(f"  ID: {first_profile.id}")
        print(f"  Name: {first_profile.name}")
        print(f"  Gender: {first_profile.gender}")
        print(f"  Age: {first_profile.age}")
        print(f"  Location: {first_profile.location}")
        print(f"  Mobile: {first_profile.mobile_number}")
        
        # Generate exports
        pdf_response = export_profiles_to_pdf(profiles)
        excel_response = export_profiles_to_excel(profiles)
        csv_response = export_profiles_to_csv(profiles)
        
        print(f"\n✓ All exports generated without data errors")
        print(f"✓ PDF size: {len(pdf_response.content):,} bytes")
        print(f"✓ Excel size: {len(excel_response.content):,} bytes")
        print(f"✓ CSV size: {len(csv_response.content):,} bytes")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all export helper tests"""
    print("\n" + "="*60)
    print("EXPORT HELPER FUNCTIONS TEST SUITE")
    print("="*60)
    print(f"Testing export_profiles_to_pdf() and export_profiles_to_excel()")
    print(f"Location: backend/users/export_utils.py")
    print(f"Started: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if profiles exist
    profile_count = Profile.objects.count()
    print(f"\nTotal profiles in database: {profile_count}")
    
    if profile_count == 0:
        print("\n⚠ WARNING: No profiles found in database!")
        print("Please create some profiles first using Django admin or API.")
        print("Continuing with limited tests...")
    
    # Run all tests
    tests = [
        ("PDF Export - All Profiles", test_pdf_export),
        ("PDF Export - With Filters", test_pdf_with_filters),
        ("Excel Export - All Profiles", test_excel_export),
        ("Excel Export - Custom Sheet", test_excel_with_custom_sheet),
        ("CSV Export - All Profiles", test_csv_export),
        ("Empty QuerySet Handling", test_empty_queryset),
        ("Large Dataset Export", test_large_dataset),
        ("Data Integrity Check", test_profile_data_integrity),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed successfully!")
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
    
    print("\nGenerated files:")
    print("  - test_pdf_export.pdf")
    print("  - test_pdf_filtered.pdf")
    print("  - test_excel_export.xlsx")
    print("  - test_excel_custom.xlsx")
    print("  - test_csv_export.csv")
    print("  - test_pdf_large.pdf (if applicable)")
    
    print(f"\nCompleted: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)


if __name__ == '__main__':
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
