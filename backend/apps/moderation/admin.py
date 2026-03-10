from django.contrib import admin
from .models import Report, ExportLog


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'reported_user', 'reason', 'status', 'created_at', 'reviewed_by']
    list_filter = ['status', 'reason', 'created_at']
    search_fields = ['reporter__username', 'reported_user__username']
    readonly_fields = ['created_at', 'reviewed_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Report Details', {'fields': ('reporter', 'reported_user', 'reason', 'description', 'status')}),
        ('Review Information', {'fields': ('reviewed_by', 'reviewed_at', 'admin_notes')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )


@admin.register(ExportLog)
class ExportLogAdmin(admin.ModelAdmin):
    list_display = ['admin', 'export_type', 'file_type', 'file_name', 'record_count', 'created_at']
    list_filter = ['file_type', 'export_type', 'created_at']
    search_fields = ['admin__username', 'file_name', 'export_type']
    readonly_fields = ['created_at', 'admin']
    ordering = ['-created_at']

    fieldsets = (
        ('Export Details', {'fields': ('admin', 'export_type', 'file_type', 'file_name', 'record_count')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.admin = request.user
        super().save_model(request, obj, form, change)
