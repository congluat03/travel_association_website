from django.urls import path
from . import admin_views, views

app_name = 'support'
urlpatterns = [
    # Phân Admin
    path('tailieu/them/', admin_views.them_sua_tailieu, name='them_tailieu'),
    path('tailieu/sua/<int:ma_tl>/', admin_views.them_sua_tailieu, name='sua_tailieu'),
    path('tailieu/xoa/<int:ma_tl>/', admin_views.xoa_tailieu, name='xoa_tailieu'),

    # Phân index
    path('tailieu-index/', views.danh_sach_tailieu, name='tailieu_index'),
    path('tailieu-index/chitettailieu/<int:pk>/', views.chi_tiet_tailieu, name='chi_tiet_tailieu'),
]