from django.urls import path
from . import admin_views, views # ✅ import đúng file

app_name = 'members'
urlpatterns = [
   
    path('members/add_members', admin_views.tai_khoan_list, name='add_members'),
    path('taikhoan/', admin_views.tai_khoan_list, name='tai-khoan-list'),
    path('taikhoan/<int:pk>/', admin_views.tai_khoan_detail, name='tai-khoan-detail'),
    # Doanh nghiệp
    path('doanhnghiep/', admin_views.doanh_nghiep_list),
    path('doanhnghiep/<int:pk>/', admin_views.doanh_nghiep_detail),
    # Ngành nghề
    path('nganhnghe/', admin_views.nganh_nghe_list),
    path('nganhnghe/<int:pk>/', admin_views.nganh_nghe_detail),

    path('hiephoi/', admin_views.hiephoi_list, name='hiephoi-list'),
    path('hiephoi/<int:pk>/', admin_views.hiephoi_detail, name='hiephoi-detail'),

    path('dangkyhoivien/', admin_views.dangky_list, name='dangkyhoivien-list'),
    path('dangkyhoivien/<int:pk>/', admin_views.dangky_detail, name='dangkyhoivien-detail'),
]