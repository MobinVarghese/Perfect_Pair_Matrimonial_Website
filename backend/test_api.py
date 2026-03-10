#!/usr/bin/env python
"""
Comprehensive Backend API Testing Script
Tests all major API endpoints and functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(test_name, status, message=""):
    """Print formatted test result"""
    symbol = "✓" if status else "✗"
    color = Colors.GREEN if status else Colors.RED
    print(f"{color}{symbol} {test_name}{Colors.END}")
    if message:
        print(f"  {message}")

def print_section(title):
    """Print section header"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.END}\n")

# Test data
test_user = {
    "username": "testuser_" + datetime.now().strftime("%H%M%S"),
    "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
}

admin_credentials = {
    "username": "adminuser",
    "password": "admin123"
}

tokens = {}
test_profile_id = None
test_interest_id = None

def test_registration():
    """Test user registration"""
    print_section("1. USER REGISTRATION")
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=test_user)
        if response.status_code == 201:
            print_test("User Registration", True, f"User {test_user['username']} created")
            return True
        else:
            print_test("User Registration", False, f"Status: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print_test("User Registration", False, str(e))
        return False

def test_login():
    """Test user login"""
    print_section("2. USER LOGIN")
    
    try:
        # Test user login
        response = requests.post(f"{BASE_URL}/api/token/", json={
            "username": test_user["username"],
            "password": test_user["password"]
        })
        
        if response.status_code == 200:
            data = response.json()
            if 'access' in data and 'refresh' in data:
                tokens['user_access'] = data['access']
                tokens['user_refresh'] = data['refresh']
                print_test("User Login", True, "JWT tokens received")
            else:
                print_test("User Login", False, "No tokens in response")
                return False
        else:
            print_test("User Login", False, f"Status: {response.status_code}")
            return False
        
        # Test admin login
        response = requests.post(f"{BASE_URL}/api/token/", json=admin_credentials)
        
        if response.status_code == 200:
            data = response.json()
            tokens['admin_access'] = data['access']
            tokens['admin_refresh'] = data['refresh']
            print_test("Admin Login", True, "Admin tokens received")
            return True
        else:
            print_test("Admin Login", False, f"Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test("Login", False, str(e))
        return False

def test_get_current_user():
    """Test get current user endpoint"""
    print_section("3. GET CURRENT USER")
    
    try:
        headers = {"Authorization": f"Bearer {tokens['user_access']}"}
        response = requests.get(f"{BASE_URL}/api/users/me/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print_test("Get Current User", True, f"Username: {data.get('username')}")
            return True
        else:
            print_test("Get Current User", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Get Current User", False, str(e))
        return False

def test_profile_creation():
    """Test profile creation"""
    print_section("4. PROFILE CREATION")
    
    global test_profile_id
    
    try:
        headers = {"Authorization": f"Bearer {tokens['user_access']}"}
        profile_data = {
            "name": "Test User Profile",
            "gender": "male",
            "age": 25,
            "date_of_birth": "1999-01-15",
            "occupation": "Software Engineer",
            "education": "B.Tech Computer Science",
            "height": "5.8",
            "location": "Mumbai, Maharashtra, India",
            "about": "Test profile for API testing",
            "mobile_number": "+91987654" + datetime.now().strftime("%H%M")
        }
        
        response = requests.post(f"{BASE_URL}/api/profiles/", json=profile_data, headers=headers)
        
        if response.status_code == 201:
            data = response.json()
            test_profile_id = data.get('id')
            print_test("Profile Creation", True, f"Profile ID: {test_profile_id}")
            return True
        else:
            print_test("Profile Creation", False, f"Status: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print_test("Profile Creation", False, str(e))
        return False

def test_profile_search():
    """Test profile search"""
    print_section("5. PROFILE SEARCH")
    
    try:
        headers = {"Authorization": f"Bearer {tokens['user_access']}"}
        
        # Test search by gender
        response = requests.get(f"{BASE_URL}/api/profiles/?gender=female", headers=headers)
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', len(data) if isinstance(data, list) else 0)
            print_test("Search by Gender", True, f"Found {count} female profiles")
        else:
            print_test("Search by Gender", False, f"Status: {response.status_code}")
            return False
        
        # Test search by age range
        response = requests.get(f"{BASE_URL}/api/profiles/?min_age=21&max_age=30", headers=headers)
        if response.status_code == 200:
            print_test("Search by Age Range", True)
        else:
            print_test("Search by Age Range", False)
            return False
        
        # Test search by location
        response = requests.get(f"{BASE_URL}/api/profiles/?location=Mumbai", headers=headers)
        if response.status_code == 200:
            print_test("Search by Location", True)
            return True
        else:
            print_test("Search by Location", False)
            return False
            
    except Exception as e:
        print_test("Profile Search", False, str(e))
        return False

def test_interest_system():
    """Test interest sending and receiving"""
    print_section("6. INTEREST SYSTEM")
    
    global test_interest_id
    
    try:
        headers = {"Authorization": f"Bearer {tokens['admin_access']}"}
        
        # Admin sends interest to test user
        interest_data = {
            "receiver": test_profile_id,
            "message": "Hi! I'd like to connect with you."
        }
        
        response = requests.post(f"{BASE_URL}/api/interests/", json=interest_data, headers=headers)
        
        if response.status_code == 201:
            data = response.json()
            test_interest_id = data.get('id')
            print_test("Send Interest", True, f"Interest ID: {test_interest_id}")
        else:
            print_test("Send Interest", False, f"Status: {response.status_code}")
            return False
        
        # Get received interests
        user_headers = {"Authorization": f"Bearer {tokens['user_access']}"}
        response = requests.get(f"{BASE_URL}/api/interests/received/", headers=user_headers)
        
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get('count', 0)
            print_test("Get Received Interests", True, f"Count: {count}")
            return True
        else:
            print_test("Get Received Interests", False)
            return False
            
    except Exception as e:
        print_test("Interest System", False, str(e))
        return False

def test_favorites():
    """Test favorites functionality"""
    print_section("7. FAVORITES SYSTEM")
    
    try:
        headers = {"Authorization": f"Bearer {tokens['user_access']}"}
        
        # Toggle favorite (add)
        response = requests.post(f"{BASE_URL}/api/favorites/toggle/{test_profile_id}/", headers=headers)
        
        if response.status_code in [200, 201]:
            data = response.json()
            is_favorited = data.get('is_favorited', False)
            print_test("Add to Favorites", True, f"Favorited: {is_favorited}")
        else:
            print_test("Add to Favorites", False, f"Status: {response.status_code}")
            return False
        
        # Check favorite status
        response = requests.get(f"{BASE_URL}/api/favorites/check/{test_profile_id}/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print_test("Check Favorite Status", True, f"Is Favorited: {data.get('is_favorited')}")
            return True
        else:
            print_test("Check Favorite Status", False)
            return False
            
    except Exception as e:
        print_test("Favorites", False, str(e))
        return False

def test_password_reset_request():
    """Test password reset request"""
    print_section("8. PASSWORD RESET SYSTEM")
    
    try:
        # Create password reset request
        reset_data = {
            "email": test_user["email"],
            "reason": "Forgot my password - testing"
        }
        
        response = requests.post(f"{BASE_URL}/api/password-reset-requests/", json=reset_data)
        
        if response.status_code in [200, 201]:
            print_test("Password Reset Request", True)
        else:
            print_test("Password Reset Request", False, f"Status: {response.status_code}")
            return False
        
        # Admin views password reset requests
        headers = {"Authorization": f"Bearer {tokens['admin_access']}"}
        response = requests.get(f"{BASE_URL}/api/password-reset-requests/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get('count', 0)
            print_test("View Password Resets (Admin)", True, f"Count: {count}")
            return True
        else:
            print_test("View Password Resets (Admin)", False)
            return False
            
    except Exception as e:
        print_test("Password Reset", False, str(e))
        return False

def test_feedback_system():
    """Test feedback submission"""
    print_section("9. FEEDBACK SYSTEM")
    
    try:
        headers = {"Authorization": f"Bearer {tokens['user_access']}"}
        
        feedback_data = {
            "category": "suggestion",
            "subject": "Great platform!",
            "message": "This is a test feedback for API testing."
        }
        
        response = requests.post(f"{BASE_URL}/api/feedback/", json=feedback_data, headers=headers)
        
        if response.status_code == 201:
            print_test("Submit Feedback", True)
            return True
        else:
            print_test("Submit Feedback", False, f"Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test("Feedback", False, str(e))
        return False

def test_user_list():
    """Test user list endpoint"""
    print_section("10. USER LIST")
    
    try:
        headers = {"Authorization": f"Bearer {tokens['user_access']}"}
        response = requests.get(f"{BASE_URL}/api/users/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get('count', 0)
            print_test("Get User List", True, f"Total users: {count}")
            return True
        else:
            print_test("Get User List", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("User List", False, str(e))
        return False

def test_token_refresh():
    """Test token refresh"""
    print_section("11. TOKEN REFRESH")
    
    try:
        refresh_data = {"refresh": tokens['user_refresh']}
        response = requests.post(f"{BASE_URL}/api/token/refresh/", json=refresh_data)
        
        if response.status_code == 200:
            data = response.json()
            if 'access' in data:
                tokens['user_access'] = data['access']
                print_test("Token Refresh", True, "New access token received")
                return True
            else:
                print_test("Token Refresh", False, "No access token in response")
                return False
        else:
            print_test("Token Refresh", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Token Refresh", False, str(e))
        return False

def main():
    """Run all tests"""
    print(f"\n{Colors.YELLOW}{'='*60}")
    print("  MATRIMONIAL WEBSITE - API TEST SUITE")
    print(f"  Testing Backend: {BASE_URL}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}{Colors.END}\n")
    
    tests = [
        ("Registration", test_registration),
        ("Login", test_login),
        ("Current User", test_get_current_user),
        ("Profile Creation", test_profile_creation),
        ("Profile Search", test_profile_search),
        ("Interest System", test_interest_system),
        ("Favorites", test_favorites),
        ("Password Reset", test_password_reset_request),
        ("Feedback", test_feedback_system),
        ("User List", test_user_list),
        ("Token Refresh", test_token_refresh),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_test(test_name, False, f"Exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {total - passed}{Colors.END}")
    print(f"Success Rate: {(passed/total)*100:.1f}%\n")
    
    if passed == total:
        print(f"{Colors.GREEN}✓ ALL TESTS PASSED! ✓{Colors.END}\n")
    else:
        print(f"{Colors.RED}✗ SOME TESTS FAILED ✗{Colors.END}\n")
        print("Failed tests:")
        for test_name, result in results:
            if not result:
                print(f"  - {test_name}")
        print()

if __name__ == "__main__":
    main()
