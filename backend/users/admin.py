from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils import timezone
from .models import User, Profile, OTPVerification, Interest, Favorite, Report, ExportLog, Feedback, PasswordResetRequest
import csv
from datetime import datetime

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin with blocking functionality"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_blocked', 'is_admin', 'is_staff', 'date_joined']
    list_filter = ['is_blocked', 'is_admin', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    actions = ['block_users', 'unblock_users']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_admin',)}),
        ('Account Blocking', {
            'fields': ('is_blocked', 'blocked_reason', 'blocked_at', 'blocked_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['blocked_at', 'blocked_by']
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('is_admin',)}),
    )
    
    def block_users(self, request, queryset):
        """Block selected users"""
        from django.utils import timezone
        
        # Exclude admins and self
        users_to_block = queryset.exclude(
            Q(is_admin=True) | Q(is_staff=True) | Q(id=request.user.id)
        )
        
        updated = 0
        for user in users_to_block:
            if not user.is_blocked:
                user.is_blocked = True
                user.blocked_reason = 'Blocked by admin via bulk action'
                user.blocked_at = timezone.now()
                user.blocked_by = request.user
                user.save()
                updated += 1
        
        self.message_user(request, f'{updated} user(s) have been blocked.')
    block_users.short_description = 'Block selected users'
    
    def unblock_users(self, request, queryset):
        """Unblock selected users"""
        updated = queryset.filter(is_blocked=True).update(
            is_blocked=False,
            blocked_reason=None,
            blocked_at=None,
            blocked_by=None
        )
        self.message_user(request, f'{updated} user(s) have been unblocked.')
    unblock_users.short_description = 'Unblock selected users'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile Admin"""
    list_display = ['name', 'user', 'gender', 'age', 'location', 'mobile_number', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['name', 'user__username', 'user__email', 'mobile_number', 'location']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    actions = ['export_profiles_csv', 'export_statistics']
    
    def export_profiles_csv(self, request, queryset):
        """Export selected profiles to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="profiles_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Gender', 'Age', 'Location', 'Occupation', 'Education', 'Mobile', 'Email', 'Created'])
        
        for profile in queryset:
            writer.writerow([
                profile.name,
                profile.gender,
                profile.age,
                profile.location or 'N/A',
                profile.occupation or 'N/A',
                profile.education or 'N/A',
                profile.mobile_number or 'N/A',
                profile.user.email,
                profile.created_at.strftime('%Y-%m-%d')
            ])
        
        # Log the export
        ExportLog.objects.create(
            admin=request.user,
            export_type='profiles',
            file_type='csv',
            file_name=response['Content-Disposition'].split('=')[1].strip('"'),
            record_count=queryset.count()
        )
        
        return response
    export_profiles_csv.short_description = "Export selected profiles to CSV"
    
    def export_statistics(self, request, queryset):
        """Export demographic statistics"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="statistics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        
        # Overall statistics
        total = Profile.objects.count()
        male_count = Profile.objects.filter(gender='M').count()
        female_count = Profile.objects.filter(gender='F').count()
        
        writer.writerow(['=== OVERALL DEMOGRAPHICS ==='])
        writer.writerow(['Metric', 'Count', 'Percentage'])
        writer.writerow(['Total Profiles', total, '100%'])
        writer.writerow(['Male Users', male_count, f'{(male_count/total*100):.1f}%' if total > 0 else '0%'])
        writer.writerow(['Female Users', female_count, f'{(female_count/total*100):.1f}%' if total > 0 else '0%'])
        writer.writerow([])
        
        # Location distribution
        writer.writerow(['=== TOP 10 LOCATIONS ==='])
        writer.writerow(['Location', 'Count'])
        locations = Profile.objects.values('location').annotate(count=Count('id')).order_by('-count')[:10]
        for loc in locations:
            writer.writerow([loc['location'] or 'Not specified', loc['count']])
        writer.writerow([])
        
        # Age distribution
        writer.writerow(['=== AGE DISTRIBUTION ==='])
        writer.writerow(['Age Group', 'Count'])
        age_groups = [
            ('18-24', 18, 24),
            ('25-30', 25, 30),
            ('31-35', 31, 35),
            ('36-40', 36, 40),
            ('41+', 41, 150)
        ]
        for label, min_age, max_age in age_groups:
            count = Profile.objects.filter(age__gte=min_age, age__lte=max_age).count()
            writer.writerow([label, count])
        writer.writerow([])
        
        # Interest statistics
        writer.writerow(['=== INTEREST STATISTICS ==='])
        writer.writerow(['Metric', 'Count'])
        total_interests = Interest.objects.count()
        pending = Interest.objects.filter(status='pending').count()
        accepted = Interest.objects.filter(status='accepted').count()
        rejected = Interest.objects.filter(status='rejected').count()
        
        writer.writerow(['Total Interests Sent', total_interests])
        writer.writerow(['Pending', pending])
        writer.writerow(['Accepted', accepted])
        writer.writerow(['Rejected', rejected])
        if total_interests > 0:
            writer.writerow(['Acceptance Rate', f'{(accepted/total_interests*100):.1f}%'])
        writer.writerow([])
        
        # Report statistics
        writer.writerow(['=== REPORT STATISTICS ==='])
        writer.writerow(['Metric', 'Count'])
        total_reports = Report.objects.count()
        pending_reports = Report.objects.filter(status='pending').count()
        reviewed_reports = Report.objects.filter(status='reviewed').count()
        
        writer.writerow(['Total Reports', total_reports])
        writer.writerow(['Pending Review', pending_reports])
        writer.writerow(['Reviewed', reviewed_reports])
        writer.writerow([])
        
        # Report reasons
        writer.writerow(['=== REPORT REASONS ==='])
        writer.writerow(['Reason', 'Count'])
        reasons = Report.objects.values('reason').annotate(count=Count('id')).order_by('-count')
        for reason in reasons:
            writer.writerow([reason['reason'].replace('_', ' ').title(), reason['count']])
        
        # Log the export
        ExportLog.objects.create(
            admin=request.user,
            export_type='statistics',
            file_type='csv',
            file_name=response['Content-Disposition'].split('=')[1].strip('"'),
            record_count=total
        )
        
        return response
    export_statistics.short_description = "Export platform statistics"
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'name', 'mobile_number')
        }),
        ('Personal Details', {
            'fields': ('gender', 'age', 'height', 'location', 'photo')
        }),
        ('Professional Information', {
            'fields': ('occupation', 'education')
        }),
        ('About', {
            'fields': ('about', 'desired_partner_traits')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# @admin.register(OTPVerification)
# class OTPVerificationAdmin(admin.ModelAdmin):
#     """OTP Verification Admin"""
#     list_display = ['user', 'otp', 'is_verified', 'created_at', 'expires_at', 'is_expired_status']
#     list_filter = ['is_verified', 'created_at']
#     search_fields = ['user__username', 'otp']
#     readonly_fields = ['created_at']
#     ordering = ['-created_at']
#     
#     def is_expired_status(self, obj):
#         """Display if OTP is expired"""
#         return obj.is_expired()
#     is_expired_status.boolean = True
#     is_expired_status.short_description = 'Expired'


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    """Interest Admin"""
    list_display = ['sender', 'receiver', 'status', 'created_at', 'responded_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sender__username', 'receiver__username']
    readonly_fields = ['created_at', 'responded_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Interest Details', {
            'fields': ('sender', 'receiver', 'status', 'message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'responded_at')
        }),
    )


# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin):
#     """Favorite Admin"""
#     list_display = ['user', 'profile', 'created_at']
#     list_filter = ['created_at']
#     search_fields = ['user__username', 'profile__name']
#     readonly_fields = ['created_at']
#     ordering = ['-created_at']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Report Admin"""
    list_display = ['reporter', 'reported_user', 'reason', 'status', 'created_at', 'reviewed_by']
    list_filter = ['status', 'reason', 'created_at']
    search_fields = ['reporter__username', 'reported_user__username']
    readonly_fields = ['created_at', 'reviewed_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Report Details', {
            'fields': ('reporter', 'reported_user', 'reason', 'description', 'status')
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'reviewed_at', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(ExportLog)
class ExportLogAdmin(admin.ModelAdmin):
    """Export Log Admin"""
    list_display = ['admin', 'export_type', 'file_type', 'file_name', 'record_count', 'created_at']
    list_filter = ['file_type', 'export_type', 'created_at']
    search_fields = ['admin__username', 'file_name', 'export_type']
    readonly_fields = ['created_at', 'admin']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Export Details', {
            'fields': ('admin', 'export_type', 'file_type', 'file_name', 'record_count')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Automatically set the admin field to the current logged-in user."""
        if not change:  # Only set on creation
            obj.admin = request.user
        super().save_model(request, obj, form, change)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Feedback Admin"""
    list_display = ['user', 'category', 'subject', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['user__username', 'subject', 'message', 'admin_response']
    readonly_fields = ['user', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Feedback Details', {
            'fields': ('user', 'category', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('status', 'admin_response')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    list_per_page = 25
    
    actions = ['mark_as_reviewed', 'mark_as_resolved']
    
    def mark_as_reviewed(self, request, queryset):
        """Mark selected feedback as reviewed"""
        updated = queryset.update(status='reviewed')
        self.message_user(request, f'{updated} feedback(s) marked as reviewed.')
    mark_as_reviewed.short_description = 'Mark selected as Reviewed'
    
    def mark_as_resolved(self, request, queryset):
        """Mark selected feedback as resolved"""
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} feedback(s) marked as resolved.')
    mark_as_resolved.short_description = 'Mark selected as Resolved'


@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):
    """Password Reset Request Admin"""
    list_display = ['user', 'email', 'status', 'display_password', 'created_at', 'processed_by']
    list_filter = ['status', 'created_at', 'processed_at']
    search_fields = ['user__username', 'email', 'reason', 'admin_notes']
    readonly_fields = ['user', 'email', 'created_at', 'processed_at', 'processed_by', 'display_new_password']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Request Details', {
            'fields': ('user', 'email', 'reason')
        }),
        ('Status', {
            'fields': ('status', 'admin_notes')
        }),
        ('New Password', {
            'fields': ('display_new_password',),
            'description': 'The generated password will appear here after approval. Copy this to share with the user if email fails.'
        }),
        ('Processing Information', {
            'fields': ('processed_by', 'processed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    def display_password(self, obj):
        """Display password in list view"""
        if obj.new_password:
            return f"🔑 {obj.new_password}"
        return "-"
    display_password.short_description = 'New Password'
    
    def display_new_password(self, obj):
        """Display password prominently in detail view"""
        if obj.new_password:
            from django.utils.html import format_html
            return format_html(
                '<div style="background-color: #fff3cd; border: 2px solid #ffc107; '
                'padding: 15px; border-radius: 5px; font-size: 16px; font-weight: bold; '
                'font-family: monospace; color: #856404;">'
                '🔑 New Password: <span style="color: #d63384; font-size: 18px;">{}</span>'
                '<br><small style="font-weight: normal; color: #666;">Copy this password to share with the user manually if email delivery fails.</small>'
                '</div>',
                obj.new_password
            )
        return format_html(
            '<div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; color: #6c757d;">'
            'Password will be generated when request is approved.'
            '</div>'
        )
    display_new_password.short_description = 'Generated Password'
    
    list_per_page = 25
    
    actions = ['approve_requests', 'approve_with_custom_password', 'reject_requests']
    
    def approve_with_custom_password(self, request, queryset):
        """Approve with custom password - opens form for admin to set password"""
        from django.shortcuts import render, redirect
        from django import forms
        from django.contrib import messages
        
        pending = queryset.filter(status='pending')
        
        if not pending.exists():
            self.message_user(request, 'No pending requests selected.', level='warning')
            return
        
        if pending.count() > 1:
            self.message_user(request, 'Please select only ONE request for custom password.', level='warning')
            return
        
        reset_request = pending.first()
        
        class CustomPasswordForm(forms.Form):
            password = forms.CharField(
                widget=forms.TextInput(attrs={'size': '40'}),
                min_length=8,
                help_text='Enter a password (min 8 characters). Leave empty to auto-generate.',
                required=False
            )
            send_email = forms.BooleanField(
                initial=True,
                required=False,
                label='Send email to user'
            )
        
        if 'apply' in request.POST:
            form = CustomPasswordForm(request.POST)
            if form.is_valid():
                import random
                import string
                from django.utils import timezone
                
                # Use custom password or generate one
                custom_pwd = form.cleaned_data.get('password', '').strip()
                if custom_pwd:
                    new_password = custom_pwd
                else:
                    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                
                # Update user password
                user = reset_request.user
                user.set_password(new_password)
                user.save()
                
                # Update reset request
                reset_request.status = 'approved'
                reset_request.processed_by = request.user
                reset_request.processed_at = timezone.now()
                reset_request.new_password = new_password
                reset_request.admin_notes = f'Approved with custom password by {request.user.username}'
                reset_request.save()
                
                # Send email if requested
                if form.cleaned_data.get('send_email'):
                    try:
                        from django.core.mail import send_mail
                        from django.conf import settings
                        
                        subject = 'Password Reset - PerfectPair Matrimonial'
                        message = f"""
Hello {user.first_name or user.username},

Your password has been reset by admin.

Your new password is: {new_password}

Please login and change it immediately.

Login URL: http://localhost:3000/login

Best regards,
PerfectPair Team
                        """
                        
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [reset_request.email],
                            fail_silently=True,
                        )
                        messages.success(request, f'Password set to: {new_password} and email sent.')
                    except Exception as e:
                        messages.warning(request, f'Password set to: {new_password} but email failed. Please share manually.')
                else:
                    messages.success(request, f'Password set to: {new_password} (no email sent).')
                
                return redirect(request.get_full_path())
        else:
            form = CustomPasswordForm()
        
        return render(request, 'admin/custom_password_form.html', {
            'form': form,
            'reset_request': reset_request,
            'opts': self.model._meta,
        })
    approve_with_custom_password.short_description = 'Approve with Custom Password'
    
    def approve_requests(self, request, queryset):
        """Approve selected password reset requests"""
        pending = queryset.filter(status='pending')
        
        if not pending.exists():
            self.message_user(request, 'No pending requests selected.', level='warning')
            return
        
        # Generate passwords and update users
        import random
        import string
        from django.utils import timezone
        
        approved_count = 0
        for reset_request in pending:
            # Generate random password
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            # Update user password
            user = reset_request.user
            user.set_password(new_password)
            user.save()
            
            # Update reset request
            reset_request.status = 'approved'
            reset_request.processed_by = request.user
            reset_request.processed_at = timezone.now()
            reset_request.new_password = new_password
            reset_request.admin_notes = f'Approved via bulk action by {request.user.username}'
            reset_request.save()
            
            approved_count += 1
            
            # Try to send email
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                subject = 'Password Reset - PerfectPair Matrimonial'
                message = f"""
Hello {user.first_name or user.username},

Your password reset request has been approved.

Your new temporary password is: {new_password}

Please login and change it immediately.

Login URL: http://localhost:3000/login

Best regards,
PerfectPair Team
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [reset_request.email],
                    fail_silently=True,
                )
            except Exception as e:
                pass  # Continue even if email fails
        
        self.message_user(request, f'{approved_count} password reset request(s) approved and emails sent.')
    approve_requests.short_description = 'Approve and Send New Passwords'
    
    def reject_requests(self, request, queryset):
        """Reject selected password reset requests"""
        from django.utils import timezone
        
        updated = queryset.filter(status='pending').update(
            status='rejected',
            processed_by=request.user,
            processed_at=timezone.now(),
            admin_notes=f'Rejected via bulk action by {request.user.username}'
        )
        self.message_user(request, f'{updated} password reset request(s) rejected.')
    reject_requests.short_description = 'Reject Selected Requests'
