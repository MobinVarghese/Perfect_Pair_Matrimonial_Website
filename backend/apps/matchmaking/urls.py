from django.urls import path
from . import views

app_name = 'matchmaking'

urlpatterns = [
    path('interest/send/<int:user_id>/', views.send_interest_view, name='send_interest'),
    path('interest/<int:interest_id>/respond/', views.respond_interest_view, name='respond_interest'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('accepted-interests/', views.accepted_interests_view, name='accepted_interests'),
]
