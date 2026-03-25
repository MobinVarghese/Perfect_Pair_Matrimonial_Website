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


def preference_completion_alert(request):
    if not request.user.is_authenticated:
        return {'show_preference_alert': False}

    user = request.user
    profile = getattr(user, 'profile', None)
    if profile is None:
        return {'show_preference_alert': False}

    def _normalize_values(value):
        if value is None:
            return []
        if isinstance(value, (list, tuple, set)):
            return [str(v).strip() for v in value if str(v).strip()]
        # assume comma-separated string
        return [v.strip() for v in str(value).split(',') if v.strip()]

    locations = _normalize_values(getattr(profile, 'preferred_locations', None))
    religions = _normalize_values(getattr(profile, 'preferred_religions', None))
    education = _normalize_values(getattr(profile, 'preferred_education', None))

    show = (
        len(locations) < 2 or
        len(religions) < 2 or
        len(education) < 2
    )

    return {'show_preference_alert': show}
