from django.urls import path
from . import views, admin_views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),

    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('members/', admin_views.manage_members, name='manage_members'),
    path('news/', admin_views.manage_news, name='manage_news'),
    path('tourism/', admin_views.manage_tourism, name='manage_tourism'),
    path('support/', admin_views.manage_support, name='manage_support'),
]