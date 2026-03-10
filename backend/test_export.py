"""
Export Functionality Test Script
Tests PDF and Excel export endpoints

Usage:
    python test_export.py

Requirements:
    - Django server running on http://localhost:8000
    - Admin user created (username: admin, password: admin123)
    - Test profiles in database
"""

import requests
import os
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    """Print success message"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"✗ {text}")

def test_export_functionality():
    """Main test function"""
    print_header("EXPORT FUNCTIONALITY TESTS")
    
    # Test 1: Login as admin
    print("Test 1: Admin Login")
    try:
        response = requests.post(
            f"{BASE_URL}/api/token/",
            json={"username": "admin", "password": "admin123"}
        )
        
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens["access"]
            print_success(f"Admin login successful")
            print(f"  Access Token: {access_token[:50]}...")
        else:
            print_error(f"Admin login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test 2: Export profiles as PDF
    print("\nTest 2: Export Profiles as PDF")
    try:
        response = requests.post(
            f"{BASE_URL}/api/export/profiles/pdf/",
            headers=headers,
            json={}
        )
        
        if response.status_code == 200:
            filename = f"profiles_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filename)
            print_success(f"PDF exported successfully")
            print(f"  File: {filename}")
            print(f"  Size: {file_size:,} bytes")
        else:
            print_error(f"PDF export failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print_error(f"PDF export error: {str(e)}")
    
    # Test 3: Export profiles as Excel
    print("\nTest 3: Export Profiles as Excel")
    try:
        response = requests.post(
            f"{BASE_URL}/api/export/profiles/excel/",
            headers=headers,
            json={}
        )
        
        if response.status_code == 200:
            filename = f"profiles_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filename)
            print_success(f"Excel exported successfully")
            print(f"  File: {filename}")
            print(f"  Size: {file_size:,} bytes")
        else:
            print_error(f"Excel export failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print_error(f"Excel export error: {str(e)}")
    
    # Test 4: Export with date filter
    print("\nTest 4: Export with Date Filter")
    try:
        response = requests.post(
            f"{BASE_URL}/api/export/profiles/pdf/",
            headers=headers,
            json={
                "date_from": "2025-01-01",
                "date_to": "2025-12-31"
            }
        )
        
        if response.status_code == 200:
            filename = f"profiles_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filename)
            print_success(f"Filtered PDF exported successfully")
            print(f"  File: {filename}")
            print(f"  Size: {file_size:,} bytes")
            print(f"  Date Range: 2025-01-01 to 2025-12-31")
        else:
            print_error(f"Filtered export failed: {response.status_code}")
    except Exception as e:
        print_error(f"Filtered export error: {str(e)}")
    
    # Test 5: Export users as PDF
    print("\nTest 5: Export Users as PDF")
    try:
        response = requests.post(
            f"{BASE_URL}/api/export/users/pdf/",
            headers=headers,
            json={}
        )
        
        if response.status_code == 200:
            filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filename)
            print_success(f"Users PDF exported successfully")
            print(f"  File: {filename}")
            print(f"  Size: {file_size:,} bytes")
        else:
            print_error(f"Users export failed: {response.status_code}")
    except Exception as e:
        print_error(f"Users export error: {str(e)}")
    
    # Test 6: Export users as Excel
    print("\nTest 6: Export Users as Excel")
    try:
        response = requests.post(
            f"{BASE_URL}/api/export/users/excel/",
            headers=headers,
            json={}
        )
        
        if response.status_code == 200:
            filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filename)
            print_success(f"Users Excel exported successfully")
            print(f"  File: {filename}")
            print(f"  Size: {file_size:,} bytes")
        else:
            print_error(f"Users Excel export failed: {response.status_code}")
    except Exception as e:
        print_error(f"Users Excel export error: {str(e)}")
    
    # Test 7: View export logs
    print("\nTest 7: View Export Logs")
    try:
        response = requests.get(
            f"{BASE_URL}/api/export-logs/",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Export logs retrieved: {data['count']} total entries")
            
            if data['results']:
                print("\n  Recent Exports:")
                for i, log in enumerate(data['results'][:5], 1):
                    print(f"  {i}. {log['file_name']}")
                    print(f"     Type: {log['export_type']} | Format: {log['file_type']}")
                    print(f"     Records: {log['record_count']} | Admin: {log['admin']}")
                    print(f"     Date: {log['created_at']}")
                    print()
            else:
                print("  No export logs found")
        else:
            print_error(f"Failed to retrieve logs: {response.status_code}")
    except Exception as e:
        print_error(f"Export logs error: {str(e)}")
    
    # Test 8: Test non-admin access (should fail)
    print("\nTest 8: Test Non-Admin Access (Should Fail)")
    try:
        # Try to login as regular user
        response = requests.post(
            f"{BASE_URL}/api/token/",
            json={"username": "testuser", "password": "test123"}
        )
        
        if response.status_code == 200:
            non_admin_token = response.json()["access"]
            non_admin_headers = {"Authorization": f"Bearer {non_admin_token}"}
            
            # Try to export (should fail)
            response = requests.post(
                f"{BASE_URL}/api/export/profiles/pdf/",
                headers=non_admin_headers,
                json={}
            )
            
            if response.status_code == 403:
                print_success("Non-admin access correctly denied (403 Forbidden)")
            else:
                print_error(f"Unexpected status code: {response.status_code}")
        else:
            print("  (Skipped - no regular user found)")
    except Exception as e:
        print("  (Skipped - regular user test)")
    
    # Summary
    print_header("TEST SUMMARY")
    print("All export functionality tests completed!")
    print("\nGenerated Files:")
    for file in os.listdir('.'):
        if file.startswith(('profiles_', 'users_')) and file.endswith(('.pdf', '.xlsx')):
            size = os.path.getsize(file)
            print(f"  - {file} ({size:,} bytes)")
    
    print("\nNext Steps:")
    print("  1. Check generated PDF files")
    print("  2. Check generated Excel files")
    print("  3. Verify export logs in admin panel")
    print("  4. Test with different date ranges")

if __name__ == "__main__":
    try:
        test_export_functionality()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\nFatal error: {str(e)}")
