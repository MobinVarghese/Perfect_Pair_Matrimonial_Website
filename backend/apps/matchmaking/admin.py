from django.contrib import admin
from .models import Interest


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at', 'responded_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sender__username', 'receiver__username']
    readonly_fields = ['created_at', 'responded_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Interest Details', {'fields': ('sender', 'receiver', 'status', 'message')}),
        ('Timestamps', {'fields': ('created_at', 'responded_at')}),
    )
