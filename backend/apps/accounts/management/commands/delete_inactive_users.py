# management/commands/delete_inactive_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Permanently delete inactive users whose scheduled_deletion_at has passed.'

    def handle(self, *args, **options):
        User = get_user_model()
        cutoff = now()
        qs = User.objects.filter(
            is_active=False,
            scheduled_deletion_at__isnull=False,
            scheduled_deletion_at__lte=cutoff,
        )
        count = qs.count()
        for user in qs:
            user.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} inactive users.'))
