from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from apps.matchmaking.models import Interest
from apps.profiles.models import Profile

User = get_user_model()


@login_required
def send_interest_view(request, user_id):
    if request.method == 'POST':
        today = timezone.now().date()
        sent_today = Interest.objects.filter(sender=request.user, created_at__date=today).count()
        if request.user.has_active_gold_subscription():
            max_daily = 15
        else:
            max_daily = 5

        if sent_today >= max_daily:
            messages.error(request, f'You have reached your daily limit of {max_daily} interest requests.')
            return redirect('profiles:home')

        receiver = get_object_or_404(User, pk=user_id)

        if receiver == request.user:
            messages.error(request, 'You cannot send interest to yourself.')
            return redirect('profiles:home')

        if receiver.is_blocked:
            messages.error(request, 'Cannot send interest to this user.')
            return redirect('profiles:home')

        existing = Interest.objects.filter(
            Q(sender=request.user, receiver=receiver) |
            Q(sender=receiver, receiver=request.user)
        ).first()

        if existing:
            messages.info(request, 'An interest already exists with this user.')
        else:
            Interest.objects.create(
                sender=request.user,
                receiver=receiver,
                message=request.POST.get('message', ''),
            )
            name = receiver.get_full_name() or receiver.username
            messages.success(request, f'Interest sent to {name}!')

        try:
            return redirect('profiles:profile_detail', pk=receiver.profile.pk)
        except Profile.DoesNotExist:
            return redirect('profiles:home')

    return redirect('profiles:home')


@login_required
def respond_interest_view(request, interest_id):
    if request.method == 'POST':
        interest = get_object_or_404(Interest, pk=interest_id, receiver=request.user)

        if interest.status != 'pending':
            messages.info(request, f'Interest already {interest.status}.')
            return redirect('matchmaking:notifications')

        action = request.POST.get('action', '')
        if action == 'accept':
            interest.status = 'accepted'
            interest.responded_at = timezone.now()
            interest.save()
            messages.success(request, 'Interest accepted!')
        elif action == 'reject':
            interest.status = 'rejected'
            interest.responded_at = timezone.now()
            interest.save()
            messages.info(request, 'Interest declined.')
        else:
            messages.error(request, 'Invalid action.')

    return redirect('matchmaking:notifications')


@login_required
def notifications_view(request):
    received_interests = Interest.objects.filter(
        receiver=request.user
    ).select_related('sender', 'sender__profile').order_by('-created_at')

    sent_interests = Interest.objects.filter(
        sender=request.user
    ).select_related('receiver', 'receiver__profile').order_by('-created_at')

    pending_count = received_interests.filter(status='pending').count()

    return render(request, 'matchmaking/notifications.html', {
        'received_interests': received_interests,
        'sent_interests': sent_interests,
        'pending_count': pending_count,
    })


@login_required
def accepted_interests_view(request):
    interests = Interest.objects.filter(
        status='accepted'
    ).filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender__profile', 'receiver__profile').order_by('-responded_at', '-created_at')

    accepted_items = []
    for interest in interests:
        if interest.sender_id == request.user.id:
            other_user = interest.receiver
            direction = 'sent'
        else:
            other_user = interest.sender
            direction = 'received'

        other_profile = getattr(other_user, 'profile', None)
        accepted_items.append({
            'interest': interest,
            'other_user': other_user,
            'other_profile': other_profile,
            'direction': direction,
        })

    return render(request, 'matchmaking/accepted_interests.html', {
        'accepted_items': accepted_items,
    })
