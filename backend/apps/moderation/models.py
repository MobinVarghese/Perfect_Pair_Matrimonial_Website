from django.db import models
from django.conf import settings


class Report(models.Model):
    """Report model for users to report inappropriate profiles or behavior."""
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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made'
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_received'
    )
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, help_text='Reason for reporting')
    description = models.TextField(blank=True, help_text='Detailed description of the issue')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
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
    """Export Log model to track data exports by admins."""
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='export_logs', limit_choices_to={'is_admin': True}
    )
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, help_text='Type of exported file')
    file_name = models.CharField(max_length=255, help_text='Name of exported file')
    export_type = models.CharField(max_length=50, help_text='Type of data exported')
    record_count = models.PositiveIntegerField(default=0, help_text='Number of records exported')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_exportlog'
        verbose_name = 'Export Log'
        verbose_name_plural = 'Export Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.admin.username} exported {self.export_type} as {self.file_type} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
