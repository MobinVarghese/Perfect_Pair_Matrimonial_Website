from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('profile/<int:profile_id>/report/', views.report_profile_view, name='report_profile'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/user/<int:user_id>/block/', views.block_user_view, name='block_user'),
    path('admin/report/<int:report_id>/review/', views.review_report_view, name='review_report'),
]
