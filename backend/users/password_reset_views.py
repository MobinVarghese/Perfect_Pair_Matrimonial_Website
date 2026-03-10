from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from .models import OTPVerification

User = get_user_model()


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
        OTPVerification.objects.filter(user=user).delete()
        
        # Create new OTP with 10-minute expiration
        from django.utils import timezone
        from datetime import timedelta
        
        OTPVerification.objects.create(
            user=user,
            otp=otp_code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        
        # In production, send email here
        # For development, we'll just return the OTP (remove this in production!)
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
                is_verified=False
            )
            
            # Check if OTP is expired
            if timezone.now() > otp_obj.expires_at:
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
