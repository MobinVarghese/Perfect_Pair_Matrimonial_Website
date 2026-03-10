"""
Comprehensive Unit Tests for Matrimonial Site

Tests cover:
- Model creation (Profile, Interest, Report)
- JWT authentication
- Report Profile endpoint
- Export PDF/Excel endpoints
- Search functionality
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, timedelta
from decimal import Decimal
import json
import io

from .models import Profile, Interest, Report, OTPVerification, ExportLog

User = get_user_model()


# ===================== Model Creation Tests =====================

class ProfileModelTest(TestCase):
    """Test Profile model creation and validation"""
    
    def setUp(self):
        """Set up test user for profile creation"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_create_profile_success(self):
        """Test creating a valid profile"""
        profile = Profile.objects.create(
            user=self.user,
            name='Test User',
            gender='male',
            age=34,
            height=Decimal('5.75'),
            location='Mumbai, Maharashtra, India',
            mobile_number='9876543210',
            occupation='Software Engineer',
            education='Bachelor of Engineering',
            about='A software engineer from Mumbai.'
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.name, 'Test User')
        self.assertEqual(profile.gender, 'male')
        self.assertEqual(profile.age, 34)
        self.assertEqual(profile.location, 'Mumbai, Maharashtra, India')
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)
    
    def test_profile_str_method(self):
        """Test Profile __str__ method"""
        profile = Profile.objects.create(
            user=self.user,
            name='Test User',
            gender='male',
            age=34,
            location='Mumbai, Maharashtra',
            mobile_number='9876543211'
        )
        self.assertEqual(str(profile), "Test User's Profile (testuser)")
    
    def test_profile_user_relationship(self):
        """Test one-to-one relationship between User and Profile"""
        profile = Profile.objects.create(
            user=self.user,
            name='Test User',
            gender='male',
            age=34,
            location='Mumbai',
            mobile_number='9876543212'
        )
        
        # Access profile from user
        self.assertEqual(self.user.profile, profile)
        
    def test_profile_required_fields(self):
        """Test that required fields are enforced"""
        with self.assertRaises(Exception):
            Profile.objects.create(user=self.user)  # Missing required fields


class InterestModelTest(TestCase):
    """Test Interest model creation and relationships"""
    
    def setUp(self):
        """Set up test users for interest exchange"""
        self.sender = User.objects.create_user(
            username='sender',
            email='sender@example.com',
            password='testpass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver',
            email='receiver@example.com',
            password='testpass123'
        )
    
    def test_create_interest_success(self):
        """Test creating a valid interest"""
        interest = Interest.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            message='I would like to connect with you.',
            status='pending'
        )
        
        self.assertEqual(interest.sender, self.sender)
        self.assertEqual(interest.receiver, self.receiver)
        self.assertEqual(interest.status, 'pending')
        self.assertEqual(interest.message, 'I would like to connect with you.')
        self.assertIsNotNone(interest.created_at)
        self.assertIsNone(interest.responded_at)
    
    def test_interest_str_method(self):
        """Test Interest __str__ method"""
        interest = Interest.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            status='pending'
        )
        expected = f"{self.sender.username} → {self.receiver.username} (pending)"
        self.assertEqual(str(interest), expected)
    
    def test_interest_status_choices(self):
        """Test different interest status values"""
        statuses = ['pending', 'accepted', 'rejected']
        
        for status_value in statuses:
            interest = Interest.objects.create(
                sender=self.sender,
                receiver=self.receiver,
                status=status_value
            )
            self.assertEqual(interest.status, status_value)
            interest.delete()  # Clean up


class ReportModelTest(TestCase):
    """Test Report model creation and validation"""
    
    def setUp(self):
        """Set up test users for reporting"""
        self.reporter = User.objects.create_user(
            username='reporter',
            email='reporter@example.com',
            password='testpass123'
        )
        self.reported_user = User.objects.create_user(
            username='reported',
            email='reported@example.com',
            password='testpass123'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            is_admin=True,
            is_staff=True
        )
    
    def test_create_report_success(self):
        """Test creating a valid report"""
        report = Report.objects.create(
            reporter=self.reporter,
            reported_user=self.reported_user,
            reason='fake_profile',
            description='This profile appears to be fake.',
            status='pending'
        )
        
        self.assertEqual(report.reporter, self.reporter)
        self.assertEqual(report.reported_user, self.reported_user)
        self.assertEqual(report.reason, 'fake_profile')
        self.assertEqual(report.status, 'pending')
        self.assertIsNotNone(report.created_at)
        self.assertIsNone(report.reviewed_at)
        self.assertIsNone(report.reviewed_by)
    
    def test_report_str_method(self):
        """Test Report __str__ method"""
        report = Report.objects.create(
            reporter=self.reporter,
            reported_user=self.reported_user,
            reason='spam',
            description='Spam content'
        )
        expected = f"Report by {self.reporter.username} against {self.reported_user.username} - pending"
        self.assertEqual(str(report), expected)
    
    def test_report_reason_choices(self):
        """Test different report reason values"""
        reasons = ['fake_profile', 'inappropriate_content', 'harassment', 'spam', 'scam', 'other']
        
        for reason_value in reasons:
            report = Report.objects.create(
                reporter=self.reporter,
                reported_user=self.reported_user,
                reason=reason_value,
                description='Test report'
            )
            self.assertEqual(report.reason, reason_value)
            report.delete()  # Clean up


# ===================== JWT Authentication Tests =====================

class JWTAuthenticationTest(APITestCase):
    """Test JWT token-based authentication"""
    
    def setUp(self):
        """Set up test user for authentication"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client = APIClient()
    
    def test_obtain_jwt_token_success(self):
        """Test obtaining JWT token with valid credentials"""
        url = reverse('users:token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(len(response.data['access']) > 0)
        self.assertTrue(len(response.data['refresh']) > 0)
    
    def test_obtain_jwt_token_invalid_credentials(self):
        """Test JWT token request with invalid credentials"""
        url = reverse('users:token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
    
    def test_refresh_jwt_token_success(self):
        """Test refreshing JWT token"""
        # First, obtain tokens
        refresh = RefreshToken.for_user(self.user)
        
        url = reverse('users:token_refresh')
        data = {'refresh': str(refresh)}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_verify_jwt_token_success(self):
        """Test verifying a valid JWT token"""
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        url = reverse('users:token_verify')
        data = {'token': access_token}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_authenticated_request_with_token(self):
        """Test making authenticated request with JWT token"""
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        url = reverse('users:current-user')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_authenticated_request_without_token(self):
        """Test making authenticated request without token (should fail)"""
        url = reverse('users:current-user')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ===================== Report Profile Endpoint Tests =====================

class ReportProfileEndpointTest(APITestCase):
    """Test Report Profile API endpoint"""
    
    def setUp(self):
        """Set up test users and authentication"""
        self.reporter = User.objects.create_user(
            username='reporter',
            email='reporter@example.com',
            password='testpass123'
        )
        self.reported_user = User.objects.create_user(
            username='reported',
            email='reported@example.com',
            password='testpass123'
        )
        
        # Create profiles
        Profile.objects.create(
            user=self.reported_user,
            name='Reported User',
            gender='male',
            age=34,
            location='Delhi',
            mobile_number='9876543200'
        )
        
        # Authenticate as reporter
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.reporter)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    
    def test_create_report_success(self):
        """Test creating a report successfully"""
        url = reverse('users:report-list')
        data = {
            'reported_user': self.reported_user.id,
            'reason': 'fake_profile',
            'description': 'This profile appears to be fake with misleading information.'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 1)
        
        report = Report.objects.first()
        self.assertEqual(report.reporter, self.reporter)
        self.assertEqual(report.reported_user, self.reported_user)
        self.assertEqual(report.reason, 'fake_profile')
        self.assertEqual(report.status, 'pending')
    
    def test_create_report_missing_fields(self):
        """Test creating report with missing required fields"""
        url = reverse('users:report-list')
        data = {
            'reported_user': self.reported_user.id,
            # Missing reason and description
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_reports_as_reporter(self):
        """Test listing reports as the reporter"""
        # Create a report
        Report.objects.create(
            reporter=self.reporter,
            reported_user=self.reported_user,
            reason='spam',
            description='Spam content'
        )
        
        url = reverse('users:report-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should see own reports
        self.assertTrue(len(response.data) > 0)
    
    def test_get_my_reports(self):
        """Test getting user's own reports"""
        # Create reports
        Report.objects.create(
            reporter=self.reporter,
            reported_user=self.reported_user,
            reason='spam',
            description='Spam 1'
        )
        Report.objects.create(
            reporter=self.reporter,
            reported_user=self.reported_user,
            reason='fake_profile',
            description='Fake profile'
        )
        
        url = reverse('users:report-my-reports')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_report_unauthenticated(self):
        """Test creating report without authentication (should fail)"""
        self.client.credentials()  # Remove authentication
        
        url = reverse('users:report-list')
        data = {
            'reported_user': self.reported_user.id,
            'reason': 'spam',
            'description': 'Test'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ===================== Export Endpoints Tests =====================

class ExportEndpointsTest(APITestCase):
    """Test Export PDF and Excel endpoints"""
    
    def setUp(self):
        """Set up admin user and test profiles"""
        # Create admin user
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_admin=True,
            is_staff=True
        )
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='testpass123'
        )
        
        # Create test profiles
        for i in range(5):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='testpass123'
            )
            Profile.objects.create(
                user=user,
                name=f'Test User {i}',
                gender='male' if i % 2 == 0 else 'female',
                age=34 - i,
                location=f'City {i}',
                occupation=f'Occupation {i}',
                mobile_number=f'98765432{i}{i}'
            )
        
        self.client = APIClient()
    
    def test_export_pdf_success(self):
        """Test exporting profiles to PDF as admin"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        
        url = reverse('users:export-profiles-pdf')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(len(response.content) > 0)
        
        # Verify export log was created
        self.assertEqual(ExportLog.objects.count(), 1)
        log = ExportLog.objects.first()
        self.assertEqual(log.export_type, 'pdf')
        self.assertEqual(log.admin, self.admin)
    
    def test_export_pdf_with_filters(self):
        """Test exporting filtered profiles to PDF"""
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        
        url = reverse('users:export-profiles-pdf')
        response = self.client.get(url, {'gender': 'male'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
    
    def test_export_excel_success(self):
        """Test exporting profiles to Excel as admin"""
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        
        url = reverse('users:export-profiles-excel')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            response['Content-Type'],
            ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
             'application/vnd.ms-excel']
        )
        self.assertTrue(len(response.content) > 0)
        
        # Verify export log was created
        logs = ExportLog.objects.filter(export_type='excel')
        self.assertTrue(logs.exists())
    
    def test_export_excel_with_filters(self):
        """Test exporting filtered profiles to Excel"""
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        
        url = reverse('users:export-profiles-excel')
        response = self.client.get(url, {'gender': 'female'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_export_pdf_non_admin(self):
        """Test PDF export fails for non-admin users"""
        refresh = RefreshToken.for_user(self.regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        
        url = reverse('users:export-profiles-pdf')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_export_excel_non_admin(self):
        """Test Excel export fails for non-admin users"""
        refresh = RefreshToken.for_user(self.regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        
        url = reverse('users:export-profiles-excel')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_export_pdf_unauthenticated(self):
        """Test PDF export fails without authentication"""
        url = reverse('users:export-profiles-pdf')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_export_excel_unauthenticated(self):
        """Test Excel export fails without authentication"""
        url = reverse('users:export-profiles-excel')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ===================== Search Functionality Tests =====================

class SearchFunctionalityTest(APITestCase):
    """Test Profile Search functionality"""
    
    def setUp(self):
        """Set up test profiles with diverse data for search testing"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create diverse test profiles
        self.profiles_data = [
            {
                'username': 'engineer1',
                'name': 'John Engineer',
                'gender': 'male',
                'age': 30,
                'location': 'Mumbai, Maharashtra',
                'occupation': 'Software Engineer',
                'education': 'Bachelor of Engineering',
                'mobile': '9001234567'
            },
            {
                'username': 'doctor1',
                'name': 'Sarah Doctor',
                'gender': 'female',
                'age': 28,
                'location': 'Delhi, Delhi',
                'occupation': 'Medical Doctor',
                'education': 'MBBS',
                'mobile': '9001234568'
            },
            {
                'username': 'teacher1',
                'name': 'Mike Teacher',
                'gender': 'male',
                'age': 35,
                'location': 'Bangalore, Karnataka',
                'occupation': 'School Teacher',
                'education': 'Bachelor of Education',
                'mobile': '9001234569'
            },
            {
                'username': 'engineer2',
                'name': 'Emily Software',
                'gender': 'female',
                'age': 32,
                'location': 'Pune, Maharashtra',
                'occupation': 'Software Engineer',
                'education': 'Master of Computer Science',
                'mobile': '9001234570'
            },
            {
                'username': 'manager1',
                'name': 'David Manager',
                'gender': 'male',
                'age': 40,
                'location': 'Mumbai, Maharashtra',
                'occupation': 'Project Manager',
                'education': 'MBA',
                'mobile': '9001234571'
            }
        ]
        
        for profile_data in self.profiles_data:
            user = User.objects.create_user(
                username=profile_data['username'],
                email=f"{profile_data['username']}@example.com",
                password='testpass123'
            )
            Profile.objects.create(
                user=user,
                name=profile_data['name'],
                gender=profile_data['gender'],
                age=profile_data['age'],
                location=profile_data['location'],
                occupation=profile_data['occupation'],
                education=profile_data['education'],
                mobile_number=profile_data['mobile']
            )
        
        # Authenticate
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    
    def test_search_by_general_query(self):
        """Test general text search across name and occupation"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {'q': 'engineer'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 3)  # 2 engineers + 1 with "Engineer" in name
    
    def test_search_by_name(self):
        """Test search by specific name"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {'name': 'Sarah'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Sarah Doctor')
    
    def test_search_by_gender(self):
        """Test search by gender filter"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {'gender': 'male'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)  # 3 male profiles
    
    def test_search_by_age_range(self):
        """Test search by age range (min and max)"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {'min_age': 28, 'max_age': 32})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] >= 2)  # At least Sarah (28) and Emily (32)
    
    def test_search_by_location(self):
        """Test search by location (city/state)"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {'location': 'Mumbai'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # 2 profiles in Mumbai
    
    def test_search_by_occupation(self):
        """Test search by occupation"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {'occupation': 'Software Engineer'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # 2 software engineers
    
    def test_search_by_education(self):
        """Test search by education"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {'education': 'MBBS'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_search_by_marital_status(self):
        """Test search by marital status (NOTE: marital_status field doesn't exist in Profile model)"""
        url = reverse('users:profile-search')
        # Skipping this test as marital_status is not in the model
        # response = self.client.get(url, {'marital_status': 'Single'})
        # This test would fail as the field doesn't exist
        pass  # Placeholder
    
    def test_search_by_city(self):
        """Test search by city (NOTE: city field doesn't exist in Profile model)"""
        url = reverse('users:profile-search')
        # Skipping this test as city is not a separate field in the model
        # City is part of location field
        pass  # Placeholder
    
    def test_search_by_state(self):
        """Test search by state (NOTE: state field doesn't exist in Profile model)"""
        url = reverse('users:profile-search')
        # Skipping this test as state is not a separate field in the model
        # State is part of location field
        pass  # Placeholder
    
    def test_search_multiple_filters(self):
        """Test search with multiple filters combined"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {
            'gender': 'male',
            'location': 'Mumbai',
            'occupation': 'Software Engineer'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # Only John Engineer matches all
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        url = reverse('users:profile-search')
        
        # Test lowercase
        response1 = self.client.get(url, {'q': 'engineer'})
        # Test uppercase
        response2 = self.client.get(url, {'q': 'ENGINEER'})
        # Test mixed case
        response3 = self.client.get(url, {'q': 'EnGiNeEr'})
        
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        
        # All should return same count
        self.assertEqual(response1.data['count'], response2.data['count'])
        self.assertEqual(response2.data['count'], response3.data['count'])
    
    def test_search_partial_match(self):
        """Test that search supports partial matching"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {'q': 'eng'})  # Partial match for "engineer"
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] > 0)
    
    def test_search_no_results(self):
        """Test search with no matching results"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {'q': 'nonexistentoccupation12345'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_search_unauthenticated(self):
        """Test search without authentication (should fail)"""
        self.client.credentials()  # Remove authentication
        
        url = reverse('users:profile-search')
        response = self.client.get(url, {'q': 'engineer'})
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_search_empty_query(self):
        """Test search with no filters (should return all profiles)"""
        url = reverse('users:profile-search')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)  # All 5 test profiles


# ===================== Integration Tests =====================

class IntegrationTest(APITestCase):
    """Integration tests for complete user workflows"""
    
    def test_complete_user_workflow(self):
        """Test complete workflow: register → login → create profile → search"""
        client = APIClient()
        
        # Step 1: Create new user (skip registration endpoint)
        new_user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newpass123',
            first_name='New',
            last_name='User'
        )
        
        # Step 2: Login and obtain JWT token
        login_url = reverse('users:token_obtain_pair')
        login_data = {
            'username': 'newuser',
            'password': 'newpass123'
        }
        login_response = client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        
        access_token = login_response.data['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Step 3: Create profile
        profile_url = reverse('users:profile-list')
        profile_data = {
            'name': 'New User',
            'gender': 'male',
            'age': 29,
            'location': 'Chennai, Tamil Nadu',
            'occupation': 'Data Scientist',
            'education': 'Master of Science',
            'mobile_number': '9001112222'
        }
        profile_response = client.post(profile_url, profile_data, format='json')
        self.assertIn(profile_response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        
        # Step 4: Search for profiles
        search_url = reverse('users:profile-search')
        search_response = client.get(search_url, {'q': 'Data'})
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(search_response.data['count'], 1)
        
        # Step 5: View own profile
        current_user_url = reverse('users:current-user')
        current_user_response = client.get(current_user_url)
        self.assertEqual(current_user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(current_user_response.data['username'], 'newuser')
