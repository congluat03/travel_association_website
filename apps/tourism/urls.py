from django.urls import path
from . import views, admin_views

app_name = 'tourism'
urlpatterns = [
    # path('', views.home, name='tourism'),
    # Địa điểm du lịch
    path('diadiem/them/', admin_views.them_sua_diadiem, name='them_dia_diem'),
    path('diadiem/sua/<int:id>/', admin_views.them_sua_diadiem, name='sua_dia_diem'),
    path('diadiem/xoa/<int:ma_dd>/', admin_views.xoa_dia_diem, name='xoa_dia_diem'),

    path('dacsan/them/', admin_views.them_sua_dacsan, name='them_dacsan'),
    path('dacsan/sua/<int:id>/', admin_views.them_sua_dacsan, name='sua_dacsan'),
    path('dacsan/xoa/<int:ma_ds>/', admin_views.xoa_dac_san, name='xoa_dac_san'),

    path('tourdulich/them/', admin_views.them_sua_tour, name='them_tour'),
    path('tourdulich/sua/<int:ma_tour>/', admin_views.them_sua_tour, name='sua_tour'),
    path('tourdulich/xoa/<int:ma_tour>/', admin_views.xoa_tour, name='xoa_tour'),

    path('lichtrinh/them/', admin_views.them_sua_lich_trinh, name='them_lich_trinh'),
    path('lichtrinh/sua/<int:ma_tour>/<int:ma_lich_trinh>/', admin_views.them_sua_lich_trinh, name='sua_lich_trinh'),
    path('lichtrinh/xoa/<int:ma_lich_trinh>/', admin_views.xoa_lich_trinh, name='xoa_lich_trinh'),

    # phần index 

    path('diadiem/', views.danhsachdiadiem, name='danhsachdiadiem'),
    path('diadiem/<int:ma_dd>/', views.chitietdiadiem, name='chitietdiadiem'),
    path('diadiemdacsan/', views.danhsachdacsan, name='diadiemdacsan'),
    path('tourdiadiemdulich/', views.tour, name='tourdiadiemdulich'),
    path('tourdiadiemdulich/<int:ma_tour>/', views.chitiettour, name='chitiettour'),
]