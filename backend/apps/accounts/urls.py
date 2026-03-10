from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('admin/reset/<int:request_id>/approve/', views.approve_password_reset_view, name='approve_password_reset'),
    path('admin/reset/<int:request_id>/reject/', views.reject_password_reset_view, name='reject_password_reset'),
]
