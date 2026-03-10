from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root redirect to login
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # App routes
    path('', include('apps.accounts.urls', namespace='accounts')),
    path('', include('apps.profiles.urls', namespace='profiles')),
    path('', include('apps.matchmaking.urls', namespace='matchmaking')),
    path('', include('apps.messaging.urls', namespace='messaging')),
    path('', include('apps.interactions.urls', namespace='interactions')),
    path('', include('apps.moderation.urls', namespace='moderation')),
    path('', include('apps.feedback.urls', namespace='feedback')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
