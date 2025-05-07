from django.urls import path
from . import views, admin_views

app_name = 'core'
urlpatterns = [
    path('', views.trang_chu, name='home'),

    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('members/', admin_views.manage_members, name='manage_members'),
    path('business/', admin_views.manage_business, name='manage_business'),
    path('news/', admin_views.manage_news, name='manage_news'),
    path('tourism/', admin_views.manage_tourism, name='manage_tourism'),
    path('support/', admin_views.manage_support, name='manage_support'),
    # Phần danh cho index 
    path('introduce/', views.gioithieu, name='introduce'),
    path('contact/', views.lienhe, name='contact'),
    
]