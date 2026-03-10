from django.db import models
from django.conf import settings


class Interest(models.Model):
    """Interest/Connection Request between users."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interests_sent'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interests_received'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text='Optional message with interest request')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users_interest'
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'
        ordering = ['-created_at']
        unique_together = ['sender', 'receiver']

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username} ({self.status})"
