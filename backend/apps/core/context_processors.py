from django.db.models import Q

from apps.matchmaking.models import Interest
from apps.messaging.models import Message


def pending_interests_count(request):
    if request.user.is_authenticated:
        return {
            'pending_interests_count': Interest.objects.filter(
                receiver=request.user, status='pending'
            ).count()
        }
    return {'pending_interests_count': 0}


def unread_messages_count(request):
    if request.user.is_authenticated:
        return {
            'unread_messages_count': Message.objects.filter(
                Q(conversation__user1=request.user) |
                Q(conversation__user2=request.user),
                is_read=False
            ).exclude(sender=request.user).count()
        }
    return {'unread_messages_count': 0}
