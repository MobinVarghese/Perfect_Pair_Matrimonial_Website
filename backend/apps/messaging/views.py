from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

from apps.messaging.models import Conversation, Message
from apps.matchmaking.models import Interest

User = get_user_model()


def _get_or_create_conversation(user1, user2):
    """Get or create a conversation between two users, ensuring canonical order."""
    if user1.pk > user2.pk:
        user1, user2 = user2, user1
    conv, _ = Conversation.objects.get_or_create(user1=user1, user2=user2)
    return conv


@login_required
def inbox_view(request):
    conversations = Conversation.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).select_related('user1', 'user1__profile', 'user2', 'user2__profile').order_by('-updated_at')

    conv_list = []
    for conv in conversations:
        other = conv.other_user(request.user)
        last_msg = conv.last_message()
        unread = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
        conv_list.append({
            'conversation': conv,
            'other_user': other,
            'last_message': last_msg,
            'unread_count': unread,
        })

    return render(request, 'messaging/inbox.html', {'conversations': conv_list})


@login_required
def conversation_view(request, conversation_id):
    conv = get_object_or_404(Conversation, pk=conversation_id)

    if request.user not in (conv.user1, conv.user2):
        messages.error(request, 'Access denied.')
        return redirect('messaging:inbox')

    interest = Interest.objects.filter(
        Q(sender=conv.user1, receiver=conv.user2) |
        Q(sender=conv.user2, receiver=conv.user1),
        status='accepted'
    ).first()
    if not interest:
        messages.error(request, 'You can only message users with mutually accepted interest.')
        return redirect('messaging:inbox')

    conv.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    other = conv.other_user(request.user)
    all_messages = conv.messages.select_related('sender').order_by('created_at')

    return render(request, 'messaging/conversation.html', {
        'conversation': conv,
        'other_user': other,
        'chat_messages': all_messages,
    })


@login_required
def send_message_view(request, conversation_id):
    if request.method != 'POST':
        return redirect('messaging:conversation', conversation_id=conversation_id)

    conv = get_object_or_404(Conversation, pk=conversation_id)

    if request.user not in (conv.user1, conv.user2):
        return HttpResponse('Access denied.', status=403)

    interest = Interest.objects.filter(
        Q(sender=conv.user1, receiver=conv.user2) |
        Q(sender=conv.user2, receiver=conv.user1),
        status='accepted'
    ).first()
    if not interest:
        return HttpResponse('Messaging not allowed.', status=403)

    content = request.POST.get('content', '').strip()
    if not content:
        return HttpResponse('', status=204)

    msg = Message.objects.create(
        conversation=conv,
        sender=request.user,
        content=content,
    )
    conv.save()  # update updated_at

    if request.headers.get('HX-Request'):
        return render(request, 'messaging/partials/message_bubble.html', {
            'msg': msg,
            'is_mine': True,
        })

    return redirect('messaging:conversation', conversation_id=conversation_id)


@login_required
def fetch_new_messages_view(request, conversation_id):
    conv = get_object_or_404(Conversation, pk=conversation_id)

    if request.user not in (conv.user1, conv.user2):
        return HttpResponse('', status=403)

    last_id = request.GET.get('last_id', '0')
    try:
        last_id = int(last_id)
    except ValueError:
        last_id = 0

    new_msgs = conv.messages.filter(pk__gt=last_id).exclude(
        sender=request.user
    ).select_related('sender').order_by('created_at')

    new_msgs.filter(is_read=False).update(is_read=True)

    if not new_msgs.exists():
        return HttpResponse('', status=204)

    return render(request, 'messaging/partials/new_messages.html', {
        'new_messages': new_msgs,
    })


@login_required
def start_conversation_view(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)

    if other_user == request.user:
        messages.error(request, 'Cannot message yourself.')
        return redirect('profiles:home')

    interest = Interest.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user),
        status='accepted'
    ).first()

    if not interest:
        messages.error(request, 'You can only message users with mutually accepted interest.')
        return redirect('profiles:home')

    conv = _get_or_create_conversation(request.user, other_user)
    return redirect('messaging:conversation', conversation_id=conv.pk)
