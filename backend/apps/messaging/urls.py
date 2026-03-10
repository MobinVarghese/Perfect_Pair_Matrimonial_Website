from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('messages/', views.inbox_view, name='inbox'),
    path('messages/<int:conversation_id>/', views.conversation_view, name='conversation'),
    path('messages/<int:conversation_id>/send/', views.send_message_view, name='send_message'),
    path('messages/<int:conversation_id>/new/', views.fetch_new_messages_view, name='fetch_new_messages'),
    path('messages/start/<int:user_id>/', views.start_conversation_view, name='start_conversation'),
]
