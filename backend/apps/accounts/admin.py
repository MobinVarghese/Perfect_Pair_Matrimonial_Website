from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Q
from django.utils import timezone
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
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
        updated = queryset.filter(is_blocked=True).update(
            is_blocked=False, blocked_reason=None,
            blocked_at=None, blocked_by=None
        )
        self.message_user(request, f'{updated} user(s) have been unblocked.')
    unblock_users.short_description = 'Unblock selected users'
