from django.urls import path
from . import admin_views

app_name = 'support'
urlpatterns = [
    path('tailieu/', admin_views.tailieu_list, name='tailieu-list'),
    path('tailieu/<int:pk>/', admin_views.tailieu_detail, name='tailieu-detail'),

    path('tailieu/them/', admin_views.them_sua_tailieu, name='them_tailieu'),
    path('tailieu/sua/<int:ma_tl>/', admin_views.them_sua_tailieu, name='sua_tailieu'),
    path('tailieu/xoa/<int:ma_tl>/', admin_views.xoa_tailieu, name='xoa_tailieu'),
]