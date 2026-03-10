from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.feedback.models import Feedback


@login_required
def feedback_view(request):
    if request.method == 'POST':
        category     = request.POST.get('category', 'general')
        subject      = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not subject or not message_text:
            messages.error(request, 'Please fill in all fields.')
        elif len(message_text) < 10:
            messages.error(request, 'Message must be at least 10 characters.')
        else:
            valid_cats = ['bug', 'feature', 'general', 'complaint', 'suggestion']
            if category not in valid_cats:
                category = 'general'
            Feedback.objects.create(
                user=request.user,
                category=category,
                subject=subject,
                message=message_text,
            )
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('feedback:feedback')

    user_feedbacks = Feedback.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'feedback/feedback.html', {'feedbacks': user_feedbacks})
