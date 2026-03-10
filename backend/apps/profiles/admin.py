from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime
import csv

from .models import Profile
from apps.moderation.models import ExportLog, Report
from apps.matchmaking.models import Interest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'gender', 'age', 'location', 'mobile_number', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['name', 'user__username', 'user__email', 'mobile_number', 'location']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    actions = ['export_profiles_csv', 'export_statistics']

    fieldsets = (
        ('User Information', {'fields': ('user', 'name', 'mobile_number')}),
        ('Personal Details', {'fields': ('gender', 'age', 'height', 'location', 'photo')}),
        ('Professional Information', {'fields': ('occupation', 'education')}),
        ('About', {'fields': ('about', 'desired_partner_traits')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def export_profiles_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="profiles_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Gender', 'Age', 'Location', 'Occupation', 'Education', 'Mobile', 'Email', 'Created'])

        for profile in queryset:
            writer.writerow([
                profile.name, profile.gender, profile.age,
                profile.location or 'N/A', profile.occupation or 'N/A',
                profile.education or 'N/A', profile.mobile_number or 'N/A',
                profile.user.email, profile.created_at.strftime('%Y-%m-%d')
            ])

        ExportLog.objects.create(
            admin=request.user, export_type='profiles', file_type='csv',
            file_name=response['Content-Disposition'].split('=')[1].strip('"'),
            record_count=queryset.count()
        )
        return response
    export_profiles_csv.short_description = "Export selected profiles to CSV"

    def export_statistics(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="statistics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'

        writer = csv.writer(response)
        total = Profile.objects.count()
        male_count = Profile.objects.filter(gender='M').count()
        female_count = Profile.objects.filter(gender='F').count()

        writer.writerow(['=== OVERALL DEMOGRAPHICS ==='])
        writer.writerow(['Metric', 'Count', 'Percentage'])
        writer.writerow(['Total Profiles', total, '100%'])
        writer.writerow(['Male Users', male_count, f'{(male_count/total*100):.1f}%' if total > 0 else '0%'])
        writer.writerow(['Female Users', female_count, f'{(female_count/total*100):.1f}%' if total > 0 else '0%'])
        writer.writerow([])

        writer.writerow(['=== TOP 10 LOCATIONS ==='])
        writer.writerow(['Location', 'Count'])
        locations = Profile.objects.values('location').annotate(count=Count('id')).order_by('-count')[:10]
        for loc in locations:
            writer.writerow([loc['location'] or 'Not specified', loc['count']])
        writer.writerow([])

        writer.writerow(['=== AGE DISTRIBUTION ==='])
        writer.writerow(['Age Group', 'Count'])
        for label, min_age, max_age in [('18-24', 18, 24), ('25-30', 25, 30), ('31-35', 31, 35), ('36-40', 36, 40), ('41+', 41, 150)]:
            count = Profile.objects.filter(age__gte=min_age, age__lte=max_age).count()
            writer.writerow([label, count])
        writer.writerow([])

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

        writer.writerow(['=== REPORT STATISTICS ==='])
        writer.writerow(['Metric', 'Count'])
        total_reports = Report.objects.count()
        writer.writerow(['Total Reports', total_reports])
        writer.writerow(['Pending Review', Report.objects.filter(status='pending').count()])
        writer.writerow(['Reviewed', Report.objects.filter(status='reviewed').count()])
        writer.writerow([])

        writer.writerow(['=== REPORT REASONS ==='])
        writer.writerow(['Reason', 'Count'])
        reasons = Report.objects.values('reason').annotate(count=Count('id')).order_by('-count')
        for reason in reasons:
            writer.writerow([reason['reason'].replace('_', ' ').title(), reason['count']])

        ExportLog.objects.create(
            admin=request.user, export_type='statistics', file_type='csv',
            file_name=response['Content-Disposition'].split('=')[1].strip('"'),
            record_count=total
        )
        return response
    export_statistics.short_description = "Export platform statistics"
