from django.urls import path
from . import views, admin_views

app_name = 'tourism'
urlpatterns = [
    # path('', views.home, name='tourism'),
    # Địa điểm du lịch
    path('diadiem/them/', admin_views.dia_diem_form, name='them_dia_diem'),
    path('diadiem/sua/<int:id>/', admin_views.dia_diem_form, name='sua_dia_diem'),
    path('diadiem/xoa/<int:ma_dd>/', admin_views.xoa_dia_diem, name='xoa_dia_diem'),

    path('dacsan/them/', admin_views.them_sua_dacsan, name='them_dacsan'),
    path('dacsan/sua/<int:id>/', admin_views.them_sua_dacsan, name='sua_dacsan'),
    path('dacsan/xoa/<int:ma_ds>/', admin_views.xoa_dac_san, name='xoa_dac_san'),

    path('tourdulich/them/', admin_views.them_sua_tour, name='them_tour'),
    path('tourdulich/sua/<int:ma_tour>/', admin_views.them_sua_tour, name='sua_tour'),
    path('tourdulich/xoa/<int:ma_tour>/', admin_views.xoa_tour, name='xoa_tour'),

    path('lichtrinh/them/', admin_views.them_sua_lich_trinh, name='them_lich_trinh'),
    path('lichtrinh/sua/<int:ma_tour>/<int:ma_lich_trinh>/', admin_views.them_sua_lich_trinh, name='sua_lich_trinh'),
    path('lichtrinh/xoa/<int:ma_tour>/<int:ma_lich_trinh>/', admin_views.xoa_lich_trinh, name='xoa_lich_trinh'),


    path('diadiemdulich/', admin_views.diadiemdulich_list, name='diadiemdulich-list'),
    path('diadiemdulich/<int:pk>/', admin_views.diadiemdulich_detail, name='diadiemdulich-detail'),

    # Đặc sản
    path('dacsan/', admin_views.dacsan_list, name='dacsan-list'),
    path('dacsan/<int:pk>/', admin_views.dacsan_detail, name='dacsan-detail'),

    # Tour du lịch
    path('tourdulich/', admin_views.tourdulich_list, name='tourdulich-list'),
    path('tourdulich/<int:pk>/', admin_views.tourdulich_detail, name='tourdulich-detail'),

    # Thuộc tour
    path('thuoctour/', admin_views.thuoctour_list, name='thuoctour-list'),
    path('thuoctour/<int:pk>/', admin_views.thuoctour_detail, name='thuoctour-detail'),
]