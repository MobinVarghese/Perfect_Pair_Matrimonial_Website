from django.db import models
from django.conf import settings
from apps.profiles.models import Profile


class Favorite(models.Model):
    """Favorite model for users to save profiles they're interested in."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites'
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_favorite'
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        ordering = ['-created_at']
        unique_together = ['user', 'profile']

    def __str__(self):
        return f"{self.user.username} favorited {self.profile.name}"
