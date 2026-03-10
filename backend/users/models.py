from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Adds is_admin field for admin privileges and is_blocked for account blocking.
    """
    is_admin = models.BooleanField(
        default=False,
        help_text='Designates whether the user is an admin.'
    )
    is_blocked = models.BooleanField(
        default=False,
        help_text='Designates whether the user account is blocked by admin.'
    )
    blocked_reason = models.TextField(
        blank=True,
        null=True,
        help_text='Reason for blocking the account'
    )
    blocked_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Timestamp when the account was blocked'
    )
    blocked_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blocked_users',
        help_text='Admin who blocked this user'
    )
    
    class Meta:
        db_table = 'users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username


class Profile(models.Model):
    """
    User Profile model for matrimonial website.
    Contains all personal and preference information.
    """
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    name = models.CharField(max_length=255, help_text='Full name')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text='Date of birth (must be 18+ years old)'
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)],
        help_text='Age in years (calculated from date of birth)'
    )
    occupation = models.CharField(max_length=255, blank=True)
    education = models.CharField(max_length=255, blank=True)
    height = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text='Height in feet (e.g., 5.6)',
        null=True,
        blank=True
    )
    location = models.CharField(max_length=255, help_text='City, State, Country')
    about = models.TextField(blank=True, help_text='About yourself')
    desired_partner_traits = models.TextField(
        blank=True,
        help_text='Desired partner characteristics'
    )
    photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
        help_text='Profile photo'
    )
    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        help_text='Mobile number with country code'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_profile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-created_at']
    
    def calculate_age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            age = today.year - self.date_of_birth.year
            # Adjust if birthday hasn't occurred this year
            if today.month < self.date_of_birth.month or \
               (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                age -= 1
            return age
        return self.age  # Fallback to manual age if DOB not set
    
    def save(self, *args, **kwargs):
        """Auto-calculate age from date_of_birth before saving"""
        if self.date_of_birth:
            self.age = self.calculate_age()
        # Normalize gender to lowercase
        if self.gender:
            self.gender = self.gender.lower()
        # Normalize name to Title Case
        if self.name:
            self.name = self.name.strip().title()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}'s Profile ({self.user.username})"


class OTPVerification(models.Model):
    """
    OTP Verification model for mobile number verification.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='otp_verifications'
    )
    otp = models.CharField(max_length=6, help_text='6-digit OTP code')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        help_text='OTP expiration time (typically 10 minutes from creation)'
    )
    
    class Meta:
        db_table = 'users_otpverification'
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'
        ordering = ['-created_at']
    
    def __str__(self):
        status = "Verified" if self.is_verified else "Pending"
        return f"OTP for {self.user.username} - {status}"
    
    def is_expired(self):
        """Check if OTP has expired"""
        from django.utils import timezone
        return timezone.now() > self.expires_at


class Interest(models.Model):
    """
    Interest/Connection Request model.
    Tracks interest sent between users.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interests_sent'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interests_received'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    message = models.TextField(
        blank=True,
        help_text='Optional message with interest request'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'users_interest'
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'
        ordering = ['-created_at']
        unique_together = ['sender', 'receiver']  # Prevent duplicate interests
    
    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username} ({self.status})"


class Favorite(models.Model):
    """
    Favorite model for users to save profiles they're interested in.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users_favorite'
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        ordering = ['-created_at']
        unique_together = ['user', 'profile']  # Prevent duplicate favorites
    
    def __str__(self):
        return f"{self.user.username} favorited {self.profile.name}"


class Report(models.Model):
    """
    Report model for users to report inappropriate profiles or behavior.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]
    
    REASON_CHOICES = [
        ('fake_profile', 'Fake Profile'),
        ('inappropriate_content', 'Inappropriate Content'),
        ('harassment', 'Harassment'),
        ('spam', 'Spam'),
        ('other', 'Other'),
    ]
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made'
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_received'
    )
    reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES,
        help_text='Reason for reporting'
    )
    description = models.TextField(
        blank=True,
        help_text='Detailed description of the issue'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_reviewed'
    )
    admin_notes = models.TextField(blank=True, help_text='Admin notes on the report')
    
    class Meta:
        db_table = 'users_report'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report by {self.reporter.username} against {self.reported_user.username} - {self.status}"


class ExportLog(models.Model):
    """
    Export Log model to track data exports by admins.
    """
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]
    
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='export_logs',
        limit_choices_to={'is_admin': True}
    )
    file_type = models.CharField(
        max_length=10,
        choices=FILE_TYPE_CHOICES,
        help_text='Type of exported file'
    )
    file_name = models.CharField(max_length=255, help_text='Name of exported file')
    export_type = models.CharField(
        max_length=50,
        help_text='Type of data exported (e.g., users, profiles, reports)'
    )
    record_count = models.PositiveIntegerField(
        default=0,
        help_text='Number of records exported'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users_exportlog'
        verbose_name = 'Export Log'
        verbose_name_plural = 'Export Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.admin.username} exported {self.export_type} as {self.file_type} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Feedback(models.Model):
    """
    Feedback model for users to send feedback to admin.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]
    
    CATEGORY_CHOICES = [
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('general', 'General Feedback'),
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        help_text='User who submitted the feedback'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general',
        help_text='Category of feedback'
    )
    subject = models.CharField(
        max_length=200,
        help_text='Brief subject of feedback'
    )
    message = models.TextField(
        help_text='Detailed feedback message'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Current status of feedback'
    )
    admin_response = models.TextField(
        blank=True,
        null=True,
        help_text='Admin response to feedback'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_feedback'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.subject}"


class PasswordResetRequest(models.Model):
    """
    Model for password reset requests.
    Users submit requests, admins approve and send new passwords via email.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_reset_requests',
        help_text='User requesting password reset'
    )
    email = models.EmailField(
        help_text='Email address where new password will be sent'
    )
    reason = models.TextField(
        blank=True,
        null=True,
        help_text='Reason for password reset request'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Status of the request'
    )
    admin_notes = models.TextField(
        blank=True,
        null=True,
        help_text='Admin notes regarding the request'
    )
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_reset_requests',
        help_text='Admin who processed this request'
    )
    new_password = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text='Temporary password generated by admin'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the request was processed'
    )
    
    class Meta:
        db_table = 'users_passwordresetrequest'
        verbose_name = 'Password Reset Request'
        verbose_name_plural = 'Password Reset Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.status} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
