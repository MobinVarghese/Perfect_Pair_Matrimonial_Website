from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'subject', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['user__username', 'subject', 'message', 'admin_response']
    readonly_fields = ['user', 'created_at', 'updated_at']
    ordering = ['-created_at']
    list_per_page = 25
    actions = ['mark_as_reviewed', 'mark_as_resolved']

    fieldsets = (
        ('Feedback Details', {'fields': ('user', 'category', 'subject', 'message')}),
        ('Status', {'fields': ('status', 'admin_response')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(status='reviewed')
        self.message_user(request, f'{updated} feedback(s) marked as reviewed.')
    mark_as_reviewed.short_description = 'Mark selected as Reviewed'

    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} feedback(s) marked as resolved.')
    mark_as_resolved.short_description = 'Mark selected as Resolved'
