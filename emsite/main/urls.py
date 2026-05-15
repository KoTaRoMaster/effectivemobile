"""
URL configuration for effectivemobile project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('staff/', views.staff_view, name='staff'),
    path('staff/edit/office=<int:office_id>&date=<str:data>', views.staff_edit_view, name='staff_edit'),

    path('user_records/', views.user_records_view, name='user_records'),

    path('records/', views.records_view, name='records'),
    path('records_write/office=<int:office_id>&date=<str:data>', views.records_write_view, name='records_write'),

    path('admin/', views.admin_view, name='admin'),

    path('admin/users/', views.admin_users_partial, name='admin_users'),
    path('admin/offices/', views.admin_offices_partial, name='admin_offices'),
    path('admin/staff/', views.admin_staff_partial, name='admin_staff'),

    path('admin/create-user/', views.admin_user_create_view, name='admin_create_user'),
    path('admin/create-staff/', views.admin_staff_create_view, name='admin_create_staff'),
    path('admin/create-office/', views.admin_office_create_view, name='admin_create_office'),

    path('admin/edit-user/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('admin/edit-staff/<int:staff_id>/', views.admin_edit_staff, name='admin_edit_staff'),
    path('admin/edit-office/<int:office_id>/', views.admin_edit_office, name='admin_edit_office'),

    path('admin/delete-users/', views.admin_delete_users, name='admin_delete_users'),
    path('admin/delete-staff/', views.admin_delete_staffs, name='admin_delete_staff'),
    path('admin/delete-offices/', views.admin_delete_offices, name='admin_delete_offices'),
]
