from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from datetime import timedelta
import random
import io

# PDF and Excel export libraries
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import pandas as pd

from .models import Profile, OTPVerification, Interest, Favorite, Report, ExportLog, Feedback, PasswordResetRequest
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    ProfileSerializer,
    OTPVerificationSerializer,
    PasswordResetRequestSerializer,
    OTPVerifySerializer,
    InterestSerializer,
    InterestResponseSerializer,
    FavoriteSerializer,
    ReportSerializer,
    ReportReviewSerializer,
    ExportLogSerializer,
    ExportRequestSerializer,
    FeedbackSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsReportOwnerOrAdmin

User = get_user_model()


# ======================== User Views ========================

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Public endpoint - no authentication required.
    User must login after registration.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response(
            {
                'message': 'Registration successful! Please login to continue.',
                'username': user.username
            },
            status=status.HTTP_201_CREATED
        )


class UserListView(generics.ListAPIView):
    """
    API endpoint to list all users.
    Authenticated users can view all users for matchmaking.
    """
    queryset = User.objects.filter(is_active=True).select_related('profile')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']
    ordering = ['-date_joined']


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a user.
    Users can only update/delete their own account.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        # Users can only access their own account
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False  # Soft delete
        user.save()
        return Response(
            {'message': 'Account deactivated successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


class CurrentUserView(APIView):
    """
    API endpoint to get current authenticated user with profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    """
    API endpoint for changing user password.
    Requires old password for verification.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Password changed successfully'},
            status=status.HTTP_200_OK
        )


# ======================== Profile ViewSet ========================

class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Profile model with full CRUD operations.
    
    Features:
    - List: View all profiles (authenticated users)
    - Retrieve: View single profile
    - Create: Create profile for authenticated user
    - Update: Update own profile
    - Delete: Delete own profile
    - Search: Filter by gender, age, location
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location', 'occupation', 'education']
    ordering_fields = ['created_at', 'age', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Filter profiles based on user role and query parameters.
        """
        queryset = Profile.objects.select_related('user').all()
        
        # Filter by gender (case-insensitive)
        gender = self.request.query_params.get('gender', None)
        if gender:
            queryset = queryset.filter(gender__iexact=gender)
        
        # Filter by age range
        min_age = self.request.query_params.get('min_age', None)
        max_age = self.request.query_params.get('max_age', None)
        if min_age:
            queryset = queryset.filter(age__gte=min_age)
        if max_age:
            queryset = queryset.filter(age__lte=max_age)
        
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        return queryset

    def perform_create(self, serializer):
        """
        Create profile for the authenticated user.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Update profile and track modification time.
        """
        serializer.save()

    @action(detail=False, methods=['get'], url_path='me')
    def my_profile(self, request):
        """
        Get current user's profile.
        """
        try:
            profile = request.user.profile
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found. Please create your profile.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], url_path='create-mine')
    def create_my_profile(self, request):
        """
        Create profile for current user.
        """
        if hasattr(request.user, 'profile'):
            return Response(
                {'error': 'Profile already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='view')
    def view_profile(self, request, pk=None):
        """
        View another user's profile with detailed information.
        """
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search')
    def search_profiles(self, request):
        """
        Advanced search endpoint for profiles.
        Supports filtering by: name, age range, gender, occupation, location, education, marital_status.
        
        Query Parameters:
        - q: General search query (searches name, occupation, location)
        - name: Filter by name (case-insensitive partial match)
        - min_age: Minimum age filter
        - max_age: Maximum age filter
        - gender: Filter by gender (male/female/other)
        - occupation: Filter by occupation (case-insensitive partial match)
        - location: Filter by location (case-insensitive partial match)
        - education: Filter by education level (case-insensitive partial match)
        - marital_status: Filter by marital status (single/married/divorced/widowed)
        - city: Filter by city (case-insensitive partial match)
        - state: Filter by state (case-insensitive partial match)
        - country: Filter by country (case-insensitive partial match)
        """
        queryset = Profile.objects.select_related('user').all()
        
        # General search query (searches across multiple fields)
        q = request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(occupation__icontains=q) |
                Q(location__icontains=q) |
                Q(education__icontains=q)
            )
        
        # Name filter
        name = request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        # Age range filters
        min_age = request.query_params.get('min_age', None)
        max_age = request.query_params.get('max_age', None)
        if min_age:
            try:
                queryset = queryset.filter(age__gte=int(min_age))
            except (ValueError, TypeError):
                pass
        if max_age:
            try:
                queryset = queryset.filter(age__lte=int(max_age))
            except (ValueError, TypeError):
                pass
        
        # Gender filter
        gender = request.query_params.get('gender', None)
        if gender and gender.lower() in ['male', 'female']:
            queryset = queryset.filter(gender__iexact=gender)
        
        # Occupation filter
        occupation = request.query_params.get('occupation', None)
        if occupation:
            queryset = queryset.filter(occupation__icontains=occupation)
        
        # Location filter
        location = request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # City filter
        city = request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # State filter
        state = request.query_params.get('state', None)
        if state:
            queryset = queryset.filter(state__icontains=state)
        
        # Country filter
        country = request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        # Education filter
        education = request.query_params.get('education', None)
        if education:
            queryset = queryset.filter(education__icontains=education)
        
        # Marital status filter
        marital_status = request.query_params.get('marital_status', None)
        if marital_status:
            queryset = queryset.filter(marital_status__iexact=marital_status)
        
        # Order by (default: most recent first)
        ordering = request.query_params.get('ordering', '-created_at')
        valid_orderings = ['created_at', '-created_at', 'age', '-age', 'name', '-name']
        if ordering in valid_orderings:
            queryset = queryset.order_by(ordering)
        
        # Serialize and return
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })


# ======================== OTP Verification ViewSet ========================

class OTPVerificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for OTP Verification with full CRUD operations.
    
    Features:
    - Generate OTP for mobile verification
    - Verify OTP code
    - Resend OTP
    - List user's OTP history (own only)
    """
    serializer_class = OTPVerificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Users can only see their own OTP records.
        """
        return OTPVerification.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['post'], url_path='generate')
    def generate_otp(self, request):
        """
        Generate new OTP for current user.
        """
        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        
        # Set expiration time (10 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Create OTP record
        otp_verification = OTPVerification.objects.create(
            user=request.user,
            otp=otp_code,
            expires_at=expires_at
        )
        
        # TODO: Send OTP via SMS service (Twilio, AWS SNS, etc.)
        # For now, return OTP in response (ONLY FOR DEVELOPMENT)
        
        serializer = self.get_serializer(otp_verification)
        return Response({
            'message': 'OTP generated successfully',
            'otp': otp_code,  # Remove in production
            'expires_at': expires_at,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='verify')
    def verify_otp(self, request):
        """
        Verify OTP code submitted by user.
        """
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        otp_code = serializer.validated_data['otp']
        
        # Find OTP record
        try:
            otp_verification = OTPVerification.objects.filter(
                user=request.user,
                otp=otp_code,
                is_verified=False
            ).latest('created_at')
            
            # Check if expired
            if otp_verification.is_expired():
                return Response(
                    {'error': 'OTP has expired. Please request a new one.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Mark as verified
            otp_verification.is_verified = True
            otp_verification.save()
            
            return Response({
                'message': 'OTP verified successfully',
                'verified': True
            }, status=status.HTTP_200_OK)
            
        except OTPVerification.DoesNotExist:
            return Response(
                {'error': 'Invalid OTP code'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='resend')
    def resend_otp(self, request):
        """
        Resend OTP to user.
        """
        return self.generate_otp(request)


# ======================== Interest ViewSet ========================

class InterestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Interest/Connection Requests with full CRUD operations.
    
    Features:
    - Send interest to another user
    - View sent interests
    - View received interests
    - Accept/reject interests
    - Delete interest
    """
    serializer_class = InterestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter interests based on query parameters.
        """
        queryset = Interest.objects.select_related(
            'sender', 'receiver', 'sender__profile', 'receiver__profile'
        )
        
        # Filter by type
        interest_type = self.request.query_params.get('type', None)
        if interest_type == 'sent':
            queryset = queryset.filter(sender=self.request.user)
        elif interest_type == 'received':
            queryset = queryset.filter(receiver=self.request.user)
        else:
            # Show both sent and received
            queryset = queryset.filter(
                Q(sender=self.request.user) | Q(receiver=self.request.user)
            )
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """
        Create interest with current user as sender.
        """
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['get'], url_path='sent')
    def sent_interests(self, request):
        """
        Get all interests sent by current user.
        """
        interests = Interest.objects.filter(sender=request.user).select_related(
            'receiver', 'receiver__profile'
        ).order_by('-created_at')
        serializer = self.get_serializer(interests, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='received')
    def received_interests(self, request):
        """
        Get all interests received by current user.
        """
        interests = Interest.objects.filter(receiver=request.user).select_related(
            'sender', 'sender__profile'
        ).order_by('-created_at')
        serializer = self.get_serializer(interests, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='pending')
    def pending_interests(self, request):
        """
        Get pending interests received by current user.
        """
        interests = Interest.objects.filter(
            receiver=request.user,
            status='pending'
        ).select_related('sender', 'sender__profile').order_by('-created_at')
        serializer = self.get_serializer(interests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='respond')
    def respond_to_interest(self, request, pk=None):
        """
        Accept or reject an interest request.
        Only the receiver can respond.
        """
        interest = self.get_object()
        
        # Check if user is the receiver
        if interest.receiver != request.user:
            return Response(
                {'error': 'Only the receiver can respond to this interest'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if already responded
        if interest.status != 'pending':
            return Response(
                {'error': f'Interest already {interest.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate response
        serializer = InterestResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Update interest
        interest.status = serializer.validated_data['status']
        interest.responded_at = timezone.now()
        interest.save()
        
        return Response({
            'message': f'Interest {interest.status} successfully',
            'data': InterestSerializer(interest, context={'request': request}).data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_interest(self, request, pk=None):
        """
        Cancel a sent interest (only if pending).
        Only sender can cancel.
        """
        interest = self.get_object()
        
        # Check if user is the sender
        if interest.sender != request.user:
            return Response(
                {'error': 'Only the sender can cancel this interest'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if pending
        if interest.status != 'pending':
            return Response(
                {'error': 'Can only cancel pending interests'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        interest.delete()
        return Response(
            {'message': 'Interest cancelled successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'], url_path='check/(?P<profile_id>[^/.]+)')
    def check_interest_status(self, request, profile_id=None):
        """
        Check if there's an accepted interest between current user and the specified profile.
        Returns the interest status if exists.
        """
        try:
            target_profile = Profile.objects.get(id=profile_id)
            target_user = target_profile.user
            
            # Check for interest from either direction
            interest = Interest.objects.filter(
                Q(sender=request.user, receiver=target_user) |
                Q(sender=target_user, receiver=request.user)
            ).first()
            
            if interest:
                return Response({
                    'has_interest': True,
                    'status': interest.status,
                    'is_sender': interest.sender == request.user,
                    'can_view_contact': interest.status == 'accepted'
                })
            else:
                return Response({
                    'has_interest': False,
                    'status': None,
                    'is_sender': False,
                    'can_view_contact': False
                })
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ======================== Favorite ViewSet ========================

class FavoriteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Favorite model with full CRUD operations.
    
    Features:
    - Users can add profiles to favorites
    - Users can view their favorite profiles
    - Users can remove profiles from favorites
    - Check if a profile is favorited
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Users see only their own favorites.
        """
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('profile', 'profile__user').order_by('-created_at')

    def perform_create(self, serializer):
        """
        Create favorite with current user.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='toggle/(?P<profile_id>[^/.]+)')
    def toggle_favorite(self, request, profile_id=None):
        """
        Toggle favorite status for a profile.
        If favorited, remove it. If not favorited, add it.
        """
        try:
            profile = Profile.objects.get(id=profile_id)
            
            # Check if already favorited
            favorite = Favorite.objects.filter(
                user=request.user,
                profile=profile
            ).first()
            
            if favorite:
                # Remove from favorites
                favorite.delete()
                return Response({
                    'message': 'Removed from favorites',
                    'is_favorited': False
                }, status=status.HTTP_200_OK)
            else:
                # Add to favorites
                favorite = Favorite.objects.create(
                    user=request.user,
                    profile=profile
                )
                serializer = self.get_serializer(favorite, context={'request': request})
                return Response({
                    'message': 'Added to favorites',
                    'is_favorited': True,
                    'favorite': serializer.data
                }, status=status.HTTP_201_CREATED)
                
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], url_path='check/(?P<profile_id>[^/.]+)')
    def check_favorite_status(self, request, profile_id=None):
        """
        Check if a profile is in user's favorites.
        """
        try:
            profile = Profile.objects.get(id=profile_id)
            is_favorited = Favorite.objects.filter(
                user=request.user,
                profile=profile
            ).exists()
            
            return Response({
                'is_favorited': is_favorited
            })
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], url_path='my-favorites')
    def my_favorites(self, request):
        """
        Get all favorites for the current user.
        """
        favorites = self.get_queryset()
        serializer = self.get_serializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)


# ======================== Report ViewSet ========================

class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Report model with full CRUD operations.
    
    Features:
    - Users can report other users
    - Users can view their own reports
    - Admins can view all reports
    - Admins can review and resolve reports
    """
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Users see their own reports, admins see all.
        """
        if self.request.user.is_admin:
            return Report.objects.select_related(
                'reporter', 'reported_user', 'reviewed_by'
            ).all().order_by('-created_at')
        return Report.objects.filter(
            reporter=self.request.user
        ).select_related('reported_user').order_by('-created_at')

    def perform_create(self, serializer):
        """
        Create report with current user as reporter.
        """
        serializer.save(reporter=self.request.user)

    @action(detail=False, methods=['get'], url_path='my-reports')
    def my_reports(self, request):
        """
        Get all reports made by current user.
        """
        reports = Report.objects.filter(reporter=request.user).select_related(
            'reported_user', 'reported_user__profile'
        ).order_by('-created_at')
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='pending', permission_classes=[IsAdminUser])
    def pending_reports(self, request):
        """
        Get all pending reports (Admin only).
        """
        reports = Report.objects.filter(status='pending').select_related(
            'reporter', 'reported_user'
        ).order_by('-created_at')
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='review', permission_classes=[IsAdminUser])
    def review_report(self, request, pk=None):
        """
        Review and update report status (Admin only).
        """
        report = self.get_object()
        
        serializer = ReportReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Update report
        report.status = serializer.validated_data['status']
        report.admin_notes = serializer.validated_data.get('admin_notes', '')
        report.reviewed_by = request.user
        report.reviewed_at = timezone.now()
        report.save()
        
        return Response({
            'message': f'Report marked as {report.status}',
            'data': ReportSerializer(report, context={'request': request}).data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='statistics', permission_classes=[IsAdminUser])
    def report_statistics(self, request):
        """
        Get report statistics (Admin only).
        """
        total_reports = Report.objects.count()
        pending_reports = Report.objects.filter(status='pending').count()
        reviewed_reports = Report.objects.filter(status='reviewed').count()
        resolved_reports = Report.objects.filter(status='resolved').count()
        
        return Response({
            'total': total_reports,
            'pending': pending_reports,
            'reviewed': reviewed_reports,
            'resolved': resolved_reports
        })


# ======================== Export Log ViewSet ========================

class ExportLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Export Log (Admin only, read-only).
    
    Features:
    - Admins can view export history
    - Track who exported what and when
    """
    serializer_class = ExportLogSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """
        Get all export logs, optionally filtered.
        """
        queryset = ExportLog.objects.select_related('admin').all().order_by('-created_at')
        
        # Filter by admin
        admin_id = self.request.query_params.get('admin_id', None)
        if admin_id:
            queryset = queryset.filter(admin_id=admin_id)
        
        # Filter by file type
        file_type = self.request.query_params.get('file_type', None)
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        
        # Filter by export type
        export_type = self.request.query_params.get('export_type', None)
        if export_type:
            queryset = queryset.filter(export_type=export_type)
        
        return queryset

    @action(detail=False, methods=['post'], url_path='export-data')
    def export_data(self, request):
        """
        Export data as PDF or Excel and create log entry (Admin only).
        
        Supports:
        - PDF export using reportlab
        - Excel export using pandas and openpyxl
        - Date range filtering
        """
        serializer = ExportRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file_type = serializer.validated_data['file_type']
        export_type = serializer.validated_data['export_type']
        date_from = serializer.validated_data.get('date_from')
        date_to = serializer.validated_data.get('date_to')
        
        # Get data based on export type
        if export_type == 'profiles':
            queryset = Profile.objects.select_related('user').all()
            if date_from:
                queryset = queryset.filter(created_at__gte=date_from)
            if date_to:
                queryset = queryset.filter(created_at__lte=date_to)
            data = queryset
            record_count = data.count()
        elif export_type == 'users':
            queryset = User.objects.all()
            if date_from:
                queryset = queryset.filter(date_joined__gte=date_from)
            if date_to:
                queryset = queryset.filter(date_joined__lte=date_to)
            data = queryset
            record_count = data.count()
        elif export_type == 'reports':
            queryset = Report.objects.select_related('reporter', 'reported_user').all()
            if date_from:
                queryset = queryset.filter(created_at__gte=date_from)
            if date_to:
                queryset = queryset.filter(created_at__lte=date_to)
            data = queryset
            record_count = data.count()
        elif export_type == 'interests':
            queryset = Interest.objects.select_related('sender', 'receiver').all()
            if date_from:
                queryset = queryset.filter(created_at__gte=date_from)
            if date_to:
                queryset = queryset.filter(created_at__lte=date_to)
            data = queryset
            record_count = data.count()
        else:
            return Response(
                {'error': 'Invalid export type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate file name
        file_name = f"{export_type}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{file_type}"
        
        # Create export log
        export_log = ExportLog.objects.create(
            admin=request.user,
            file_type=file_type,
            file_name=file_name,
            export_type=export_type,
            record_count=record_count
        )
        
        # Generate export file
        if file_type == 'pdf':
            return self._export_pdf(data, export_type, file_name, record_count)
        elif file_type == 'excel':
            return self._export_excel(data, export_type, file_name, record_count)
        else:
            return Response({
                'message': 'Export log created successfully',
                'file_name': file_name,
                'record_count': record_count,
                'data': ExportLogSerializer(export_log, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
    
    def _export_pdf(self, data, export_type, file_name, record_count):
        """
        Generate PDF export using reportlab.
        """
        # Create buffer
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        
        # Container for elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Add title
        title = Paragraph(f"{export_type.upper()} Export Report", title_style)
        elements.append(title)
        
        # Add metadata
        metadata = [
            f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Records: {record_count}",
            f"Export Type: {export_type}"
        ]
        for line in metadata:
            elements.append(Paragraph(line, styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Prepare table data based on export type
        if export_type == 'profiles':
            table_data = [['Name', 'Gender', 'Age', 'Location', 'Occupation', 'Mobile']]
            for profile in data:
                table_data.append([
                    profile.name[:20],
                    profile.gender,
                    str(profile.age),
                    profile.location[:25],
                    profile.occupation[:20],
                    profile.mobile_number
                ])
        elif export_type == 'users':
            table_data = [['Username', 'Email', 'Name', 'Admin', 'Active', 'Joined']]
            for user in data:
                table_data.append([
                    user.username,
                    user.email[:25],
                    f"{user.first_name} {user.last_name}",
                    'Yes' if user.is_admin else 'No',
                    'Yes' if user.is_active else 'No',
                    user.date_joined.strftime('%Y-%m-%d')
                ])
        elif export_type == 'reports':
            table_data = [['Reporter', 'Reported User', 'Reason', 'Status', 'Date']]
            for report in data:
                table_data.append([
                    report.reporter.username,
                    report.reported_user.username,
                    report.get_reason_display()[:20],
                    report.get_status_display(),
                    report.created_at.strftime('%Y-%m-%d')
                ])
        elif export_type == 'interests':
            table_data = [['Sender', 'Receiver', 'Status', 'Message', 'Date']]
            for interest in data:
                table_data.append([
                    interest.sender.username,
                    interest.receiver.username,
                    interest.get_status_display(),
                    interest.message[:30] if interest.message else '-',
                    interest.created_at.strftime('%Y-%m-%d')
                ])
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        
        # Add footer
        elements.append(Spacer(1, 0.5*inch))
        footer_text = Paragraph(
            "Generated by Matrimonial Website Admin Panel",
            styles['Normal']
        )
        elements.append(footer_text)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Create HTTP response
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        
        return response
    
    def _export_excel(self, data, export_type, file_name, record_count):
        """
        Generate Excel export using pandas and openpyxl.
        """
        # Prepare DataFrame based on export type
        if export_type == 'profiles':
            data_list = []
            for profile in data:
                data_list.append({
                    'ID': profile.id,
                    'Name': profile.name,
                    'Username': profile.user.username,
                    'Gender': profile.gender,
                    'Age': profile.age,
                    'Location': profile.location,
                    'Occupation': profile.occupation,
                    'Education': profile.education,
                    'Height': float(profile.height) if profile.height else None,
                    'Mobile': profile.mobile_number,
                    'Created': profile.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                })
            df = pd.DataFrame(data_list)
        
        elif export_type == 'users':
            data_list = []
            for user in data:
                data_list.append({
                    'ID': user.id,
                    'Username': user.username,
                    'Email': user.email,
                    'First Name': user.first_name,
                    'Last Name': user.last_name,
                    'Is Admin': user.is_admin,
                    'Is Active': user.is_active,
                    'Date Joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                    'Last Login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else None,
                })
            df = pd.DataFrame(data_list)
        
        elif export_type == 'reports':
            data_list = []
            for report in data:
                data_list.append({
                    'ID': report.id,
                    'Reporter': report.reporter.username,
                    'Reported User': report.reported_user.username,
                    'Reason': report.get_reason_display(),
                    'Description': report.description,
                    'Status': report.get_status_display(),
                    'Created': report.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'Reviewed At': report.reviewed_at.strftime('%Y-%m-%d %H:%M:%S') if report.reviewed_at else None,
                    'Reviewed By': report.reviewed_by.username if report.reviewed_by else None,
                    'Admin Notes': report.admin_notes,
                })
            df = pd.DataFrame(data_list)
        
        elif export_type == 'interests':
            data_list = []
            for interest in data:
                data_list.append({
                    'ID': interest.id,
                    'Sender': interest.sender.username,
                    'Receiver': interest.receiver.username,
                    'Status': interest.get_status_display(),
                    'Message': interest.message,
                    'Created': interest.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'Responded At': interest.responded_at.strftime('%Y-%m-%d %H:%M:%S') if interest.responded_at else None,
                })
            df = pd.DataFrame(data_list)
        
        # Create Excel file in memory
        buffer = io.BytesIO()
        
        # Write to Excel with formatting
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=export_type.upper(), index=False)
            
            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets[export_type.upper()]
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Style header row
            from openpyxl.styles import Font, PatternFill, Alignment
            
            header_fill = PatternFill(start_color='1a237e', end_color='1a237e', fill_type='solid')
            header_font = Font(bold=True, color='FFFFFF')
            
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Get Excel data
        excel_data = buffer.getvalue()
        buffer.close()
        
        # Create HTTP response
        response = HttpResponse(
            excel_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        
        return response


# ======================== Password Reset Views ========================

class PasswordResetRequestView(APIView):
    """
    Request password reset - generates OTP and sends to user's email
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists or not (security)
            return Response(
                {'message': 'If this email exists, a password reset code has been sent.'},
                status=status.HTTP_200_OK
            )
        
        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        
        # Delete any existing OTP for this user
        OTPVerification.objects.filter(user=user, verification_type='password_reset').delete()
        
        # Create new OTP
        OTPVerification.objects.create(
            user=user,
            otp=otp_code,
            verification_type='password_reset'
        )
        
        # In production, send email here
        # For development, we'll just return the OTP
        return Response({
            'message': 'Password reset code sent to your email',
            'otp': otp_code,  # Remove this in production!
            'email': email
        }, status=status.HTTP_200_OK)


class PasswordResetVerifyView(APIView):
    """
    Verify OTP and reset password
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        
        if not all([email, otp, new_password]):
            return Response(
                {'error': 'Email, OTP, and new password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(new_password) < 8:
            return Response(
                {'error': 'Password must be at least 8 characters long'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify OTP
        try:
            otp_obj = OTPVerification.objects.get(
                user=user,
                otp=otp,
                verification_type='password_reset',
                is_verified=False
            )
            
            # Check if OTP is expired (10 minutes)
            if timezone.now() > otp_obj.created_at + timedelta(minutes=10):
                otp_obj.delete()
                return Response(
                    {'error': 'OTP has expired. Please request a new one.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # OTP is valid - reset password
            user.set_password(new_password)
            user.save()
            
            # Mark OTP as verified and delete it
            otp_obj.is_verified = True
            otp_obj.save()
            otp_obj.delete()
            
            return Response({
                'message': 'Password reset successful. You can now login with your new password.'
            }, status=status.HTTP_200_OK)
            
        except OTPVerification.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired OTP'},
                status=status.HTTP_400_BAD_REQUEST
            )


# ======================== Feedback ViewSet ========================

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Feedback management.
    - Users can create and view their own feedback
    - Admins can view all feedback and add responses
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return user's own feedback or all feedback for admins"""
        if self.request.user.is_admin or self.request.user.is_staff:
            return Feedback.objects.select_related('user').all().order_by('-created_at')
        return Feedback.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Automatically set the user when creating feedback"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def respond(self, request, pk=None):
        """Admin can add response to feedback"""
        if not (request.user.is_admin or request.user.is_staff):
            return Response(
                {'error': 'Only admins can respond to feedback'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        feedback = self.get_object()
        admin_response = request.data.get('admin_response')
        new_status = request.data.get('status', 'reviewed')
        
        if not admin_response:
            return Response(
                {'error': 'Admin response is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        feedback.admin_response = admin_response
        feedback.status = new_status
        feedback.save()
        
        serializer = self.get_serializer(feedback)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        """Admin can update feedback status"""
        if not (request.user.is_admin or request.user.is_staff):
            return Response(
                {'error': 'Only admins can update feedback status'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        feedback = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Feedback.STATUS_CHOICES).keys():
            return Response(
                {'error': f'Invalid status. Must be one of: {", ".join(dict(Feedback.STATUS_CHOICES).keys())}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        feedback.status = new_status
        feedback.save()
        
        serializer = self.get_serializer(feedback)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ======================== Custom Login View ========================

class CustomTokenObtainPairView(APIView):
    """
    Custom login view that checks if user is blocked before issuing tokens.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if user is blocked
        if user.is_blocked:
            blocked_info = {
                'error': 'Your account has been blocked by the admin.',
                'is_blocked': True,
                'blocked_reason': user.blocked_reason or 'No reason provided',
                'blocked_at': user.blocked_at.isoformat() if user.blocked_at else None
            }
            return Response(blocked_info, status=status.HTTP_403_FORBIDDEN)
        
        # Check if user is active
        if not user.is_active:
            return Response(
                {'error': 'Your account is inactive. Please contact support.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verify password
        if not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens using Simple JWT
        from rest_framework_simplejwt.tokens import RefreshToken
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin,
                'is_staff': user.is_staff,
            }
        }, status=status.HTTP_200_OK)


# ======================== User Blocking View ========================

class BlockUserView(APIView):
    """
    Admin-only view to block/unblock users.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        # Check if requester is admin
        if not (request.user.is_admin or request.user.is_staff):
            return Response(
                {'error': 'Only admins can block/unblock users'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get user to block
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Prevent blocking self
        if user.id == request.user.id:
            return Response(
                {'error': 'You cannot block yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prevent blocking other admins
        if user.is_admin or user.is_staff:
            return Response(
                {'error': 'You cannot block admin users'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        action = request.data.get('action', 'block')  # 'block' or 'unblock'
        reason = request.data.get('reason', '')
        
        if action == 'block':
            user.is_blocked = True
            user.blocked_reason = reason
            user.blocked_at = timezone.now()
            user.blocked_by = request.user
            user.save()
            
            return Response({
                'message': f'User {user.username} has been blocked successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'is_blocked': user.is_blocked,
                    'blocked_reason': user.blocked_reason,
                    'blocked_at': user.blocked_at
                }
            }, status=status.HTTP_200_OK)
        
        elif action == 'unblock':
            user.is_blocked = False
            user.blocked_reason = None
            user.blocked_at = None
            user.blocked_by = None
            user.save()
            
            return Response({
                'message': f'User {user.username} has been unblocked successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'is_blocked': user.is_blocked
                }
            }, status=status.HTTP_200_OK)
        
        else:
            return Response(
                {'error': 'Invalid action. Use "block" or "unblock"'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Password Reset Requests.
    Users can create requests, admins can view and process them.
    """
    serializer_class = PasswordResetRequestSerializer
    
    def get_permissions(self):
        """
        Allow unauthenticated users to create requests.
        Require authentication for other operations.
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """
        Admins see all requests.
        Regular users see only their own requests.
        """
        user = self.request.user
        if user.is_authenticated and (user.is_admin or user.is_staff):
            return PasswordResetRequest.objects.all()
        elif user.is_authenticated:
            return PasswordResetRequest.objects.filter(user=user)
        return PasswordResetRequest.objects.none()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """
        Admin approves password reset request and sends new password via email.
        """
        if not (request.user.is_admin or request.user.is_staff):
            return Response(
                {'error': 'Only admins can approve password reset requests'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reset_request = self.get_object()
        
        if reset_request.status != 'pending':
            return Response(
                {'error': f'Request is already {reset_request.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate random password
        import random
        import string
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        # Update user password
        user = reset_request.user
        user.set_password(new_password)
        user.save()
        
        # Update reset request
        reset_request.status = 'approved'
        reset_request.processed_by = request.user
        reset_request.processed_at = timezone.now()
        reset_request.new_password = new_password  # Store temporarily for admin reference
        reset_request.admin_notes = request.data.get('admin_notes', '')
        reset_request.save()
        
        # Send email with new password
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            subject = 'Password Reset - PerfectPair Matrimonial'
            message = f"""
Hello {user.first_name or user.username},

Your password reset request has been approved by our admin team.

Your new temporary password is: {new_password}

Please login with this password and change it immediately from your profile settings.

Login URL: http://localhost:3000/login

If you did not request this password reset, please contact us immediately.

Best regards,
PerfectPair Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [reset_request.email],
                fail_silently=False,
            )
            
            return Response({
                'message': 'Password reset approved and email sent successfully',
                'new_password': new_password,  # Return to admin for reference
                'email_sent_to': reset_request.email,
                'request_id': reset_request.id
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Even if email fails, password is changed
            return Response({
                'message': 'Password reset approved but email sending failed',
                'new_password': new_password,  # Return to admin so they can manually share
                'email_error': str(e),
                'request_id': reset_request.id
            }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        """
        Admin rejects password reset request.
        """
        if not (request.user.is_admin or request.user.is_staff):
            return Response(
                {'error': 'Only admins can reject password reset requests'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reset_request = self.get_object()
        
        if reset_request.status != 'pending':
            return Response(
                {'error': f'Request is already {reset_request.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reset_request.status = 'rejected'
        reset_request.processed_by = request.user
        reset_request.processed_at = timezone.now()
        reset_request.admin_notes = request.data.get('admin_notes', 'Request rejected')
        reset_request.save()
        
        return Response({
            'message': 'Password reset request rejected',
            'request_id': reset_request.id
        }, status=status.HTTP_200_OK)
