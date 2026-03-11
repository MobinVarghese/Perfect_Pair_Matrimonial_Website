import re
from datetime import date, datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone

import secrets
import string

from apps.profiles.models import Profile
from apps.accounts.models import PasswordResetRequest
from apps.core.decorators import admin_required

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_admin:
            return redirect('/admin/')
        return redirect('profiles:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_blocked:
                block_date = (
                    user.blocked_at.strftime('%Y-%m-%d') if user.blocked_at else 'Unknown'
                )
                return render(request, 'accounts/login.html', {
                    'error': 'Your account has been blocked.',
                    'is_blocked': True,
                    'block_reason': user.blocked_reason or 'No reason provided',
                    'block_date': block_date,
                    'username': username,
                })
            if not user.is_active:
                return render(request, 'accounts/login.html', {
                    'error': 'Your account is inactive. Please contact support.',
                    'username': username,
                })
            login(request, user)
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            if user.is_superuser or user.is_admin:
                return redirect('/admin/')
            return redirect('profiles:home')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password.',
                'username': username,
            })

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profiles:home')

    if request.method == 'POST':
        data = request.POST
        errors = {}

        username    = data.get('username', '').strip()
        email       = data.get('email', '').strip()
        first_name  = data.get('first_name', '').strip()
        last_name   = data.get('last_name', '').strip()
        password    = data.get('password', '')
        password2   = data.get('password2', '')
        gender      = data.get('gender', '').lower()
        dob_str     = data.get('date_of_birth', '')
        mobile      = data.get('mobile_number', '').strip()

        if not username:
            errors['username'] = 'Username is required.'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'This username is already taken.'

        if not email:
            errors['email'] = 'Email is required.'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'An account with this email already exists.'

        if not first_name:
            errors['first_name'] = 'First name is required.'

        if not last_name:
            errors['last_name'] = 'Last name is required.'

        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters.'

        if password != password2:
            errors['password2'] = 'Passwords do not match.'

        if gender not in ('male', 'female'):
            errors['gender'] = 'Please select a valid gender.'

        dob = None
        if not dob_str:
            errors['date_of_birth'] = 'Date of birth is required.'
        else:
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                today = date.today()
                age = today.year - dob.year
                if (today.month, today.day) < (dob.month, dob.day):
                    age -= 1
                if age < 18:
                    errors['date_of_birth'] = 'You must be at least 18 years old.'
            except ValueError:
                errors['date_of_birth'] = 'Invalid date format.'

        if not mobile:
            errors['mobile_number'] = 'Mobile number is required.'
        elif not re.match(r'^[\d\s\+\-\(\)]+$', mobile):
            errors['mobile_number'] = 'Invalid mobile number format.'
        elif Profile.objects.filter(mobile_number=mobile).exists():
            errors['mobile_number'] = 'This mobile number is already registered.'

        if errors:
            return render(request, 'accounts/register.html', {
                'errors': errors,
                'form_data': data,
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        today = date.today()
        age = today.year - dob.year
        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1

        Profile.objects.create(
            user=user,
            name=f"{first_name} {last_name}",
            gender=gender,
            date_of_birth=dob,
            age=age,
            mobile_number=mobile,
            location='',
        )

        messages.success(request, 'Registration successful! Please login.')
        return redirect('accounts:login')

    return render(request, 'accounts/register.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email  = request.POST.get('email', '').strip()
        reason = request.POST.get('reason', '').strip()

        if not email:
            return render(request, 'accounts/forgot_password.html', {
                'error': 'Email is required.',
            })

        try:
            user = User.objects.get(email=email)
            PasswordResetRequest.objects.create(
                user=user,
                email=email,
                reason=reason or 'No reason provided.',
            )
            return render(request, 'accounts/forgot_password.html', {'success': True})
        except User.DoesNotExist:
            return render(request, 'accounts/forgot_password.html', {
                'error': 'No account found with this email address.',
                'email': email,
            })

    return render(request, 'accounts/forgot_password.html', {'success': False})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        old_password     = request.POST.get('old_password', '')
        new_password     = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('profiles:edit_profile')

        if len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters.')
            return redirect('profiles:edit_profile')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('profiles:edit_profile')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Password changed successfully!')
        return redirect('profiles:edit_profile')

    return redirect('profiles:edit_profile')


@admin_required
def approve_password_reset_view(request, request_id):
    if request.method == 'POST':
        reset_req = get_object_or_404(PasswordResetRequest, pk=request_id)

        if reset_req.status != 'pending':
            messages.info(request, 'This request has already been processed.')
            return redirect('moderation:admin_dashboard')

        alphabet     = string.ascii_letters + string.digits
        new_password = ''.join(secrets.choice(alphabet) for _ in range(12))

        reset_req.user.set_password(new_password)
        reset_req.user.save()

        reset_req.status       = 'approved'
        reset_req.new_password  = new_password
        reset_req.processed_by = request.user
        reset_req.processed_at = timezone.now()
        reset_req.save()

        messages.success(
            request,
            f'Password reset approved. New password for {reset_req.user.username}: '
            f'{new_password}  (Share securely!)'
        )

    return redirect('moderation:admin_dashboard')


@admin_required
def reject_password_reset_view(request, request_id):
    if request.method == 'POST':
        reset_req   = get_object_or_404(PasswordResetRequest, pk=request_id)
        admin_notes = request.POST.get('admin_notes', '').strip()

        if reset_req.status != 'pending':
            messages.info(request, 'This request has already been processed.')
            return redirect('moderation:admin_dashboard')

        reset_req.status       = 'rejected'
        reset_req.admin_notes  = admin_notes
        reset_req.processed_by = request.user
        reset_req.processed_at = timezone.now()
        reset_req.save()
        messages.info(request, 'Password reset request rejected.')

    return redirect('moderation:admin_dashboard')
