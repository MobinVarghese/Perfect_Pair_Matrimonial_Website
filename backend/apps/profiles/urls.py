from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<int:pk>/', views.profile_detail_view, name='profile_detail'),
    path('admin/export/pdf/', views.export_pdf_view, name='export_pdf'),
    path('admin/export/excel/', views.export_excel_view, name='export_excel'),
]
