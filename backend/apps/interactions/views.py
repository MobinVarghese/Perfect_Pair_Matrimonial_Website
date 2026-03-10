from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.interactions.models import Favorite
from apps.profiles.models import Profile


@login_required
def toggle_favorite_view(request, profile_id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, pk=profile_id)
        favorite = Favorite.objects.filter(user=request.user, profile=profile).first()

        if favorite:
            favorite.delete()
            messages.info(request, f'Removed {profile.name} from favorites.')
        else:
            Favorite.objects.create(user=request.user, profile=profile)
            messages.success(request, f'Added {profile.name} to favorites!')

        next_url = request.POST.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('profiles:profile_detail', pk=profile_id)

    return redirect('profiles:home')


@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('profile', 'profile__user').order_by('-created_at')

    return render(request, 'interactions/favorites.html', {'favorites': favorites})
