from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from apps.moderation.models import Report, ExportLog
from apps.profiles.models import Profile
from apps.accounts.models import PasswordResetRequest
from apps.feedback.models import Feedback
from apps.core.decorators import admin_required

User = get_user_model()


@login_required
def report_profile_view(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)

    if profile.user == request.user:
        messages.error(request, 'You cannot report your own profile.')
        return redirect('profiles:profile_detail', pk=profile_id)

    if request.method == 'POST':
        reason      = request.POST.get('reason', 'other')
        description = request.POST.get('description', '').strip()

        valid_reasons = ['fake_profile', 'inappropriate_content', 'harassment', 'spam', 'other']
        if reason not in valid_reasons:
            reason = 'other'

        if len(description) < 20:
            messages.error(request, 'Please provide a detailed reason (at least 20 characters).')
            return redirect('profiles:profile_detail', pk=profile_id)

        existing = Report.objects.filter(
            reporter=request.user,
            reported_user=profile.user,
            status='pending'
        ).first()

        if existing:
            messages.info(request, 'You already have an open report against this user.')
        else:
            Report.objects.create(
                reporter=request.user,
                reported_user=profile.user,
                reason=reason,
                description=description,
            )
            messages.success(request, 'Report submitted. Admin will review it.')

        return redirect('profiles:profile_detail', pk=profile_id)

    return redirect('profiles:profile_detail', pk=profile_id)


@admin_required
def admin_dashboard_view(request):
    tab = request.GET.get('tab', 'users')

    tabs = [
        ('users', 'Users'),
        ('reports', 'Reports'),
        ('exports', 'Exports'),
        ('password-resets', 'Password Resets'),
        ('feedback', 'Feedback'),
    ]

    context = {
        'active_tab': tab,
        'tabs': tabs,
        'stats': {
            'total_users':      User.objects.filter(is_active=True).count(),
            'total_profiles':   Profile.objects.count(),
            'pending_reports':  Report.objects.filter(status='pending').count(),
            'pending_resets':   PasswordResetRequest.objects.filter(status='pending').count(),
            'pending_feedback': Feedback.objects.filter(status='pending').count(),
        },
    }

    if tab == 'users':
        context['users'] = User.objects.select_related('profile').order_by('-date_joined')
    elif tab == 'reports':
        context['reports'] = Report.objects.select_related(
            'reporter', 'reported_user', 'reviewed_by'
        ).order_by('-created_at')
    elif tab == 'exports':
        context['export_logs'] = ExportLog.objects.select_related('admin').order_by('-created_at')
    elif tab == 'password-resets':
        context['reset_requests'] = PasswordResetRequest.objects.select_related(
            'user', 'processed_by'
        ).order_by('-created_at')
    elif tab == 'feedback':
        context['feedbacks'] = Feedback.objects.select_related('user').order_by('-created_at')

    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def block_user_view(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, pk=user_id)

        if target_user == request.user:
            messages.error(request, 'You cannot block your own account.')
            return redirect('moderation:admin_dashboard')

        action = request.POST.get('action', '')

        if action == 'block':
            reason = request.POST.get('reason', '').strip()
            if not reason:
                messages.error(request, 'Please provide a reason for blocking.')
                return redirect('moderation:admin_dashboard')
            target_user.is_blocked    = True
            target_user.blocked_reason = reason
            target_user.blocked_at    = timezone.now()
            target_user.blocked_by    = request.user
            target_user.save()
            messages.success(request, f'User {target_user.username} has been blocked.')

        elif action == 'unblock':
            target_user.is_blocked    = False
            target_user.blocked_reason = None
            target_user.blocked_at    = None
            target_user.blocked_by    = None
            target_user.save()
            messages.success(request, f'User {target_user.username} has been unblocked.')
        else:
            messages.error(request, 'Invalid action.')

    return redirect('moderation:admin_dashboard')


@admin_required
def review_report_view(request, report_id):
    if request.method == 'POST':
        report      = get_object_or_404(Report, pk=report_id)
        new_status  = request.POST.get('status', '')
        admin_notes = request.POST.get('admin_notes', '').strip()

        if new_status not in ('reviewed', 'resolved'):
            messages.error(request, 'Invalid status.')
            return redirect('moderation:admin_dashboard')

        report.status      = new_status
        report.admin_notes = admin_notes
        report.reviewed_by = request.user
        report.reviewed_at = timezone.now()
        report.save()
        messages.success(request, f'Report marked as {new_status}.')

    return redirect('moderation:admin_dashboard')
