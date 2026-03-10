from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django.utils import timezone
from .models import Profile, OTPVerification, Interest, Favorite, Report, ExportLog, Feedback, PasswordResetRequest
import re

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model with comprehensive validation.
    Handles profile creation, updates, and nested user data display.
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    photo_url = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'user_username', 'user_email', 'first_name', 'last_name',
            'name', 'gender', 'date_of_birth', 'age', 'occupation', 'education', 'height', 'location',
            'about', 'desired_partner_traits', 'photo', 'photo_url', 'profile_picture',
            'mobile_number', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user', 'age', 'gender', 'date_of_birth']
        extra_kwargs = {
            'name': {'required': True, 'min_length': 2, 'max_length': 255},
            'location': {'required': True, 'min_length': 3},
            'mobile_number': {'required': True},
        }
    
    def get_photo_url(self, obj):
        """Return absolute URL for profile photo"""
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
        return None
    
    def get_profile_picture(self, obj):
        """Return absolute URL for profile photo (alias for photo_url)"""
        return self.get_photo_url(obj)
    
    def validate_name(self, value):
        """Validate name contains only letters and spaces"""
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty or just spaces.")
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("Name should only contain letters and spaces.")
        return value.strip()
    
    def validate_age(self, value):
        """Validate age is between 18 and 100"""
        if value < 18:
            raise serializers.ValidationError("You must be at least 18 years old.")
        if value > 100:
            raise serializers.ValidationError("Age must be less than 100.")
        return value
    
    def validate_height(self, value):
        """Validate height is reasonable (3.0 to 8.0 feet)"""
        if value is not None:
            if value < 3.0 or value > 8.0:
                raise serializers.ValidationError("Height must be between 3.0 and 8.0 feet.")
        return value
    
    def validate_mobile_number(self, value):
        """Validate mobile number format and uniqueness"""
        if not re.match(r'^[\d\s\+\-\(\)]+$', value):
            raise serializers.ValidationError(
                "Mobile number should only contain digits, spaces, +, -, (, )."
            )
        # Remove spaces and special characters to check digit count
        digits_only = re.sub(r'[^\d]', '', value)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise serializers.ValidationError(
                "Mobile number should contain between 10 and 15 digits."
            )
        
        # Check uniqueness - exclude current profile if updating
        if self.instance:
            if Profile.objects.filter(mobile_number=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "A profile with this mobile number already exists. Please use a different mobile number."
                )
        else:
            if Profile.objects.filter(mobile_number=value).exists():
                raise serializers.ValidationError(
                    "A profile with this mobile number already exists. Please use a different mobile number."
                )
        
        return value
    
    def validate_photo(self, value):
        """Validate photo file size and type"""
        if value:
            # Check file size (max 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Photo size should not exceed 5MB.")
            
            # Check file extension
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
            ext = value.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise serializers.ValidationError(
                    f"Only {', '.join(allowed_extensions)} files are allowed."
                )
        return value
    
    def validate(self, attrs):
        """Cross-field validation"""
        # Ensure one profile per user
        if not self.instance:  # Only on creation
            user = attrs.get('user')
            if user and Profile.objects.filter(user=user).exists():
                raise serializers.ValidationError({
                    'user': 'This user already has a profile.'
                })
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with nested profile data.
    Used for user detail and list views.
    """
    profile = ProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'is_admin', 'is_staff', 'is_active', 'profile', 'date_joined',
            'is_blocked', 'blocked_reason', 'blocked_at'
        ]
        read_only_fields = ['id', 'date_joined', 'is_admin', 'is_staff', 'is_blocked', 'blocked_reason', 'blocked_at']
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def get_full_name(self, obj):
        """Return user's full name"""
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with comprehensive validation.
    Uses mobile number instead of email for registration.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password],
        help_text="Password must be at least 8 characters."
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm Password',
        help_text="Enter the same password as before, for verification."
    )
    mobile_number = serializers.CharField(
        required=True,
        max_length=15,
        help_text="Mobile number with country code"
    )
    gender = serializers.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        required=True,
        help_text="Select your gender"
    )
    date_of_birth = serializers.DateField(
        required=True,
        help_text="Date of birth (must be 18+ years old)"
    )
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'first_name', 'last_name', 'mobile_number', 'gender', 'date_of_birth']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'min_length': 3, 'max_length': 150}
        }
    
    def validate_username(self, value):
        """Validate username format"""
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "Username should only contain letters, numbers, and underscores."
            )
        return value.lower()
    
    def validate_date_of_birth(self, value):
        """Validate user is at least 18 years old"""
        from datetime import date
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if age < 18:
            raise serializers.ValidationError(
                "You must be at least 18 years old to register."
            )
        if age > 100:
            raise serializers.ValidationError(
                "Please enter a valid date of birth."
            )
        return value
    
    def validate_mobile_number(self, value):
        """Validate mobile number format and uniqueness"""
        # Check format
        if not re.match(r'^[\d\s\+\-\(\)]+$', value):
            raise serializers.ValidationError(
                "Mobile number should only contain digits, spaces, +, -, (, )."
            )
        # Remove spaces and special characters to check digit count
        digits_only = re.sub(r'[^\d]', '', value)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise serializers.ValidationError(
                "Mobile number should contain between 10 and 15 digits."
            )
        
        # Check if mobile number already exists in Profile
        if Profile.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError(
                "A profile with this mobile number already exists. Please use a different mobile number."
            )
        
        return value
    
    def validate(self, attrs):
        """Cross-field validation for password confirmation"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password2": "Password fields didn't match."
            })
        return attrs
    
    def create(self, validated_data):
        """Create user with hashed password and profile with mobile number, gender, and date_of_birth"""
        validated_data.pop('password2')
        mobile_number = validated_data.pop('mobile_number')
        gender = validated_data.pop('gender').lower()  # Normalize to lowercase
        date_of_birth = validated_data.pop('date_of_birth')
        
        # Normalize name to Title Case
        first_name = validated_data.get('first_name', '').strip().title()
        last_name = validated_data.get('last_name', '').strip().title()
        
        # Create user with dummy email (since email is required by AbstractUser)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=f"{validated_data['username']}@matrimonial.local",  # Dummy email
            password=validated_data['password'],  # create_user handles hashing
            first_name=first_name,
            last_name=last_name
        )
        
        # Calculate age from date_of_birth
        from datetime import date
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        
        # Create profile with mobile number, gender, and date_of_birth
        Profile.objects.create(
            user=user,
            name=f"{first_name} {last_name}".strip() or user.username,
            mobile_number=mobile_number,
            gender=gender,  # Normalized to lowercase
            date_of_birth=date_of_birth,
            age=age,  # Calculated from DOB
            location='Not specified'  # Default, user will update in Edit Profile
        )
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information including profile data.
    Password changes should be handled separately.
    """
    # Profile fields - only include fields that exist in Profile model
    profile_picture = serializers.ImageField(write_only=True, required=False)
    mobile_number = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    height = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)
    education = serializers.CharField(required=False)
    occupation = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    
    # Read-only fields to return profile data at top level
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'profile_picture', 'mobile_number', 
                  'gender', 'date_of_birth', 'height', 'education', 'occupation', 
                  'location', 'bio', 'profile']
        extra_kwargs = {
            'email': {'required': False},
        }
    
    def validate_email(self, value):
        """Validate email uniqueness excluding current user"""
        user = self.instance
        if User.objects.filter(email__iexact=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()
    
    def update(self, instance, validated_data):
        """Update both User and Profile models"""
        # Extract profile fields (only those that exist in Profile model)
        profile_field_mapping = {
            'profile_picture': 'photo',
            'mobile_number': 'mobile_number',
            'gender': 'gender',
            'height': 'height',
            'education': 'education',
            'occupation': 'occupation',
            'location': 'location',
            'bio': 'about',  # 'bio' maps to 'about' in Profile model
        }
        
        profile_data = {}
        for form_field, model_field in profile_field_mapping.items():
            if form_field in validated_data:
                profile_data[model_field] = validated_data.pop(form_field)
        
        # Handle date_of_birth separately (need to calculate age)
        date_of_birth = validated_data.pop('date_of_birth', None)
        
        # Update User model
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update or create Profile
        if profile_data or date_of_birth:
            try:
                profile = Profile.objects.get(user=instance)
            except Profile.DoesNotExist:
                raise serializers.ValidationError({
                    'profile': 'Profile does not exist for this user. Please contact support.'
                })
            
            # Calculate age from date_of_birth if provided
            if date_of_birth:
                from datetime import date
                today = date.today()
                age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
                profile.age = age
            
            # Update name from first_name and last_name
            if instance.first_name or instance.last_name:
                profile.name = f"{instance.first_name} {instance.last_name}".strip()
            
            # Update profile fields
            for attr, value in profile_data.items():
                if value is not None:  # Only update if value is provided
                    setattr(profile, attr, value)
            
            profile.save()
        
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change with validation.
    Ensures old password is correct and new password is strong.
    """
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm New Password'
    )
    
    def validate_old_password(self, value):
        """Verify old password is correct"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate(self, attrs):
        """Validate new passwords match"""
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password2": "New password fields didn't match."
            })
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                "new_password": "New password must be different from old password."
            })
        return attrs
    
    def save(self, **kwargs):
        """Update user password with proper hashing"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class OTPVerificationSerializer(serializers.ModelSerializer):
    """
    Serializer for OTP Verification with validation.
    Handles OTP generation, verification, and expiration.
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = OTPVerification
        fields = ['id', 'user', 'user_username', 'otp', 'is_verified', 
                  'created_at', 'expires_at', 'is_expired']
        read_only_fields = ['created_at', 'is_verified']
        extra_kwargs = {
            'user': {'write_only': True},
            'otp': {'min_length': 6, 'max_length': 6},
        }
    
    def get_is_expired(self, obj):
        """Check if OTP has expired"""
        return obj.is_expired()
    
    def validate_otp(self, value):
        """Validate OTP is 6 digits"""
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only digits.")
        if len(value) != 6:
            raise serializers.ValidationError("OTP must be exactly 6 digits.")
        return value
    
    def validate_expires_at(self, value):
        """Ensure expiration time is in the future"""
        if value <= timezone.now():
            raise serializers.ValidationError("Expiration time must be in the future.")
        return value


class OTPVerifySerializer(serializers.Serializer):
    """
    Serializer for verifying OTP code.
    Used when user submits OTP for verification.
    """
    otp = serializers.CharField(
        max_length=6,
        min_length=6,
        required=True,
        help_text="6-digit OTP code"
    )
    
    def validate_otp(self, value):
        """Validate OTP format"""
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only digits.")
        return value


class InterestSerializer(serializers.ModelSerializer):
    """
    Serializer for Interest/Connection Request model.
    Handles interest creation, updates, and validation.
    """
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sender_name = serializers.CharField(source='sender.profile.name', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)
    receiver_name = serializers.CharField(source='receiver.profile.name', read_only=True)
    sender_profile = serializers.SerializerMethodField()
    receiver_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = Interest
        fields = [
            'id', 'sender', 'sender_username', 'sender_name', 'sender_profile',
            'receiver', 'receiver_username', 'receiver_name', 'receiver_profile',
            'status', 'message', 'created_at', 'responded_at'
        ]
        read_only_fields = ['created_at', 'responded_at', 'sender']
        extra_kwargs = {
            'message': {'max_length': 500},
        }
    
    def get_sender_profile(self, obj):
        """Get sender's profile information"""
        try:
            profile = obj.sender.profile
            request = self.context.get('request')
            return {
                'id': profile.id,
                'name': profile.name,
                'profile_picture': request.build_absolute_uri(profile.photo.url) if (request and profile.photo) else None,
                'occupation': profile.occupation,
                'location': profile.location,
                'age': profile.age,
            }
        except Exception as e:
            return None
    
    def get_receiver_profile(self, obj):
        """Get receiver's profile information"""
        try:
            profile = obj.receiver.profile
            request = self.context.get('request')
            return {
                'id': profile.id,
                'name': profile.name,
                'profile_picture': request.build_absolute_uri(profile.photo.url) if (request and profile.photo) else None,
                'occupation': profile.occupation,
                'location': profile.location,
                'age': profile.age,
            }
        except Exception as e:
            return None
    
    def validate_message(self, value):
        """Validate message length and content"""
        if value and len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Message should be at least 10 characters long."
            )
        return value.strip() if value else ""
    
    def validate(self, attrs):
        """Cross-field validation for interests"""
        request = self.context.get('request')
        
        # Prevent self-interest
        receiver = attrs.get('receiver')
        if request and request.user == receiver:
            raise serializers.ValidationError({
                'receiver': "You cannot send interest to yourself."
            })
        
        # Check if interest already exists (on creation)
        if not self.instance and request:
            existing_interest = Interest.objects.filter(
                sender=request.user,
                receiver=receiver
            ).first()
            if existing_interest:
                if existing_interest.status == 'accepted':
                    raise serializers.ValidationError({
                        'error': "Request already sent once. Your interest has been accepted by this user."
                    })
                elif existing_interest.status == 'rejected':
                    raise serializers.ValidationError({
                        'error': "Request already sent once. You cannot send interest again to this user."
                    })
                else:  # pending
                    raise serializers.ValidationError({
                        'error': "Request already sent once. Your interest is pending approval."
                    })
        
        # Only allow status change if updating
        if self.instance:
            if attrs.get('receiver') and attrs['receiver'] != self.instance.receiver:
                raise serializers.ValidationError({
                    'receiver': "Cannot change the receiver of an existing interest."
                })
        
        return attrs
    
    def update(self, instance, validated_data):
        """Update interest and set responded_at when status changes"""
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        
        # Set responded_at when status changes from pending
        if old_status == 'pending' and new_status in ['accepted', 'rejected']:
            validated_data['responded_at'] = timezone.now()
        
        return super().update(instance, validated_data)


class InterestResponseSerializer(serializers.Serializer):
    """
    Serializer for responding to an interest request.
    Used by receiver to accept or reject interest.
    """
    status = serializers.ChoiceField(
        choices=['accepted', 'rejected'],
        required=True,
        help_text="Accept or reject the interest"
    )
    
    def validate_status(self, value):
        """Ensure only accepted or rejected allowed"""
        if value not in ['accepted', 'rejected']:
            raise serializers.ValidationError(
                "Status must be either 'accepted' or 'rejected'."
            )
        return value


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer for Favorite model.
    Handles user favorites/saved profiles.
    """
    profile_name = serializers.CharField(source='profile.name', read_only=True)
    profile_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'profile', 'profile_name', 'profile_details', 'created_at']
        read_only_fields = ['created_at', 'user']
    
    def get_profile_details(self, obj):
        """Get detailed profile information"""
        try:
            profile = obj.profile
            request = self.context.get('request')
            return {
                'id': profile.id,
                'name': profile.name,
                'profile_picture': request.build_absolute_uri(profile.photo.url) if (request and profile.photo) else None,
                'occupation': profile.occupation,
                'location': profile.location,
                'age': profile.age,
                'gender': profile.gender,
                'height': str(profile.height) if profile.height else None,
                'education': profile.education,
            }
        except Exception as e:
            return None
    
    def validate(self, attrs):
        """Validate favorite creation"""
        request = self.context.get('request')
        profile = attrs.get('profile')
        
        # Prevent favoriting own profile
        if request and hasattr(request.user, 'profile') and request.user.profile == profile:
            raise serializers.ValidationError({
                'profile': "You cannot favorite your own profile."
            })
        
        # Check if already favorited (on creation)
        if not self.instance and request:
            existing_favorite = Favorite.objects.filter(
                user=request.user,
                profile=profile
            ).first()
            if existing_favorite:
                raise serializers.ValidationError({
                    'profile': "You have already favorited this profile."
                })
        
        return attrs


class ReportSerializer(serializers.ModelSerializer):
    """
    Serializer for Report model with validation.
    Handles user reports of inappropriate profiles or behavior.
    """
    reporter_username = serializers.CharField(source='reporter.username', read_only=True)
    reporter_name = serializers.CharField(source='reporter.profile.name', read_only=True)
    reported_user_username = serializers.CharField(source='reported_user.username', read_only=True)
    reported_user_name = serializers.CharField(source='reported_user.profile.name', read_only=True)
    reviewed_by_username = serializers.CharField(source='reviewed_by.username', read_only=True, allow_null=True)
    reason_display = serializers.CharField(source='get_reason_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'reporter', 'reporter_username', 'reporter_name',
            'reported_user', 'reported_user_username', 'reported_user_name',
            'reason', 'reason_display', 'description', 'status', 'status_display',
            'created_at', 'reviewed_at', 'reviewed_by', 'reviewed_by_username',
            'admin_notes'
        ]
        read_only_fields = ['created_at', 'reviewed_at', 'reporter', 'reviewed_by']
        extra_kwargs = {
            'description': {'required': True, 'min_length': 20},
            'admin_notes': {'read_only': True},
        }
    
    def validate_description(self, value):
        """Validate description is meaningful"""
        if len(value.strip()) < 20:
            raise serializers.ValidationError(
                "Please provide a detailed description (at least 20 characters)."
            )
        return value.strip()
    
    def validate(self, attrs):
        """Cross-field validation for reports"""
        request = self.context.get('request')
        
        # Prevent self-reporting
        reported_user = attrs.get('reported_user')
        if request and request.user == reported_user:
            raise serializers.ValidationError({
                'reported_user': "You cannot report yourself."
            })
        
        # Check for duplicate reports (within last 24 hours)
        if not self.instance and request:
            from datetime import timedelta
            time_threshold = timezone.now() - timedelta(hours=24)
            existing_report = Report.objects.filter(
                reporter=request.user,
                reported_user=reported_user,
                created_at__gte=time_threshold
            ).first()
            if existing_report:
                raise serializers.ValidationError({
                    'reported_user': "You have already reported this user in the last 24 hours."
                })
        
        return attrs


class ReportReviewSerializer(serializers.Serializer):
    """
    Serializer for admin to review and update report status.
    Only admins can use this serializer.
    """
    status = serializers.ChoiceField(
        choices=['reviewed', 'resolved'],
        required=True,
        help_text="Update report status"
    )
    admin_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=1000,
        help_text="Admin notes on the report"
    )
    
    def validate_status(self, value):
        """Ensure valid status transition"""
        if value not in ['reviewed', 'resolved']:
            raise serializers.ValidationError(
                "Status must be either 'reviewed' or 'resolved'."
            )
        return value


class ExportLogSerializer(serializers.ModelSerializer):
    """
    Serializer for Export Log model with validation.
    Tracks data exports performed by admins.
    """
    admin_username = serializers.CharField(source='admin.username', read_only=True)
    admin_full_name = serializers.SerializerMethodField()
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)
    
    class Meta:
        model = ExportLog
        fields = [
            'id', 'admin', 'admin_username', 'admin_full_name',
            'file_type', 'file_type_display', 'file_name',
            'export_type', 'record_count', 'created_at'
        ]
        read_only_fields = ['created_at', 'admin']
        extra_kwargs = {
            'file_name': {'required': True, 'max_length': 255},
            'export_type': {'required': True, 'max_length': 50},
            'record_count': {'min_value': 0},
        }
    
    def get_admin_full_name(self, obj):
        """Return admin's full name"""
        return f"{obj.admin.first_name} {obj.admin.last_name}".strip() or obj.admin.username
    
    def validate_file_name(self, value):
        """Validate file name format"""
        if not value.strip():
            raise serializers.ValidationError("File name cannot be empty.")
        
        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in value for char in invalid_chars):
            raise serializers.ValidationError(
                f"File name contains invalid characters: {', '.join(invalid_chars)}"
            )
        return value.strip()
    
    def validate_export_type(self, value):
        """Validate export type is meaningful"""
        valid_export_types = ['users', 'profiles', 'reports', 'interests', 'all_data']
        if value.lower() not in valid_export_types:
            raise serializers.ValidationError(
                f"Export type should be one of: {', '.join(valid_export_types)}"
            )
        return value.lower()
    
    def validate(self, attrs):
        """Ensure only admins can create export logs"""
        request = self.context.get('request')
        if request and not request.user.is_admin:
            raise serializers.ValidationError(
                "Only admins can create export logs."
            )
        return attrs


class ExportRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting data export.
    Used by admins to export data in various formats.
    """
    file_type = serializers.ChoiceField(
        choices=['pdf', 'excel', 'csv'],
        required=True,
        help_text="Format of exported file"
    )
    export_type = serializers.ChoiceField(
        choices=['users', 'profiles', 'reports', 'interests', 'all_data'],
        required=True,
        help_text="Type of data to export"
    )
    date_from = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Start date for filtering data"
    )
    date_to = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="End date for filtering data"
    )
    
    def validate(self, attrs):
        """Validate date range"""
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')
        
        if date_from and date_to:
            if date_from > date_to:
                raise serializers.ValidationError({
                    'date_to': "End date must be after start date."
                })
            
            # Ensure date range is not too large (max 1 year)
            from datetime import timedelta
            if (date_to - date_from) > timedelta(days=365):
                raise serializers.ValidationError(
                    "Date range cannot exceed 1 year."
                )
        
        return attrs


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for Feedback model.
    Allows users to submit feedback to admins.
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'user_username', 'user_full_name',
            'category', 'category_display', 'subject', 'message',
            'status', 'status_display', 'admin_response',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user', 'status', 'admin_response']
        extra_kwargs = {
            'subject': {'required': True, 'max_length': 200},
            'message': {'required': True, 'min_length': 10},
        }
    
    def get_user_full_name(self, obj):
        """Return user's full name"""
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
    
    def validate_message(self, value):
        """Validate feedback message"""
        if not value.strip():
            raise serializers.ValidationError("Feedback message cannot be empty.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Feedback message must be at least 10 characters long.")
        return value.strip()
    
    def validate_subject(self, value):
        """Validate subject"""
        if not value.strip():
            raise serializers.ValidationError("Subject cannot be empty.")
        return value.strip()


class PasswordResetRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for Password Reset Requests
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    processed_by_username = serializers.CharField(source='processed_by.username', read_only=True)
    
    class Meta:
        model = PasswordResetRequest
        fields = [
            'id', 'user', 'user_username', 'user_full_name', 'email', 'reason',
            'status', 'admin_notes', 'processed_by', 'processed_by_username',
            'new_password', 'created_at', 'processed_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'processed_by', 'processed_at', 'new_password']
    
    def get_user_full_name(self, obj):
        """Return user's full name"""
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
    
    def validate_email(self, value):
        """Validate email exists in system"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Check if email exists in database
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "No account found with this email address. Please check and try again."
            )
        return value
    
    def create(self, validated_data):
        """Auto-assign user based on email"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        email = validated_data.get('email')
        user = User.objects.get(email=email)
        validated_data['user'] = user
        
        return super().create(validated_data)
