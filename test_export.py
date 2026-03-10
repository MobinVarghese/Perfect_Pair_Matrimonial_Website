"""
Test script to verify export functionality
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "username": "adminuser",
    "password": "admin123"
}

def test_export():
    """Test PDF and Excel export functionality"""
    
    print("=" * 60)
    print("Testing Export Functionality")
    print("=" * 60)
    
    # Step 1: Login as admin
    print("\n1. Logging in as admin...")
    login_response = requests.post(
        f"{BASE_URL}/token/",
        json=ADMIN_CREDENTIALS
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    tokens = login_response.json()
    access_token = tokens.get('access')
    print(f"✅ Login successful! Token received.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Test PDF Export
    print("\n2. Testing PDF Export (Profiles)...")
    pdf_response = requests.post(
        f"{BASE_URL}/export/profiles/pdf/",
        headers=headers
    )
    
    print(f"Status Code: {pdf_response.status_code}")
    print(f"Content-Type: {pdf_response.headers.get('Content-Type')}")
    print(f"Content-Disposition: {pdf_response.headers.get('Content-Disposition')}")
    
    if pdf_response.status_code == 200:
        if pdf_response.headers.get('Content-Type') == 'application/pdf':
            pdf_size = len(pdf_response.content)
            print(f"✅ PDF Export successful! Size: {pdf_size} bytes ({pdf_size/1024:.2f} KB)")
            
            # Save PDF to test
            filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            with open(filename, 'wb') as f:
                f.write(pdf_response.content)
            print(f"✅ PDF saved as: {filename}")
        else:
            print(f"❌ Wrong content type: {pdf_response.headers.get('Content-Type')}")
            print(f"Response: {pdf_response.text[:500]}")
    else:
        print(f"❌ PDF Export failed!")
        print(f"Response: {pdf_response.text}")
    
    # Step 3: Test Excel Export
    print("\n3. Testing Excel Export (Profiles)...")
    excel_response = requests.post(
        f"{BASE_URL}/export/profiles/excel/",
        headers=headers
    )
    
    print(f"Status Code: {excel_response.status_code}")
    print(f"Content-Type: {excel_response.headers.get('Content-Type')}")
    print(f"Content-Disposition: {excel_response.headers.get('Content-Disposition')}")
    
    if excel_response.status_code == 200:
        expected_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        if expected_type in excel_response.headers.get('Content-Type', ''):
            excel_size = len(excel_response.content)
            print(f"✅ Excel Export successful! Size: {excel_size} bytes ({excel_size/1024:.2f} KB)")
            
            # Save Excel to test
            filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(excel_response.content)
            print(f"✅ Excel saved as: {filename}")
        else:
            print(f"❌ Wrong content type: {excel_response.headers.get('Content-Type')}")
            print(f"Response: {excel_response.text[:500]}")
    else:
        print(f"❌ Excel Export failed!")
        print(f"Response: {excel_response.text}")
    
    # Step 4: Test other export types
    print("\n4. Testing Other Export Types...")
    
    export_types = ['users', 'reports', 'interests']
    
    for export_type in export_types:
        print(f"\n   Testing {export_type.upper()} PDF export...")
        response = requests.post(
            f"{BASE_URL}/export/{export_type}/pdf/",
            headers=headers
        )
        
        if response.status_code == 200:
            size = len(response.content)
            print(f"   ✅ {export_type.upper()} PDF: {size} bytes ({size/1024:.2f} KB)")
        else:
            print(f"   ❌ {export_type.upper()} PDF failed: {response.status_code}")
            if response.status_code != 200:
                print(f"      Error: {response.text[:200]}")
    
    print("\n" + "=" * 60)
    print("Export Functionality Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_export()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server at http://127.0.0.1:8000")
        print("   Make sure the backend server is running!")
    except Exception as e:
        print(f"❌ Error: {e}")
