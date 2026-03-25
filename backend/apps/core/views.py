from django.shortcuts import render

from apps.feedback.models import Feedback


def landing_view(request):
    public_testimonials = Feedback.objects.select_related('user').filter(
        is_public=True,
    ).order_by('-created_at')
    return render(request, 'base/landing.html', {
        'testimonials': public_testimonials,
    })
