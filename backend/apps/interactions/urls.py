from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/toggle/<int:profile_id>/', views.toggle_favorite_view, name='toggle_favorite'),
]
