from django.urls import path
from . import admin_views, views # ✅ import đúng file

app_name = 'members'
urlpatterns = [
   
    
    # Tài khoản
    path('taikhoan/them/', admin_views.them_sua_taikhoan, name='them_tai_khoan'),
    path('taikhoan/sua/<int:id>/', admin_views.them_sua_taikhoan, name='sua_tai_khoan'),
    path('taikhoan/xoa/<int:ma_tk>/', admin_views.xoa_tai_khoan, name='xoa_tai_khoan'),
    path('toggle-trang-thai/<int:ma_tk>/', admin_views.toggle_trang_thai_tai_khoan, name='toggle_trang_thai'),

    # Doanh nghiệp
    path('doanhnghiep/them/', admin_views.them_sua_doanhnghiep, name='them_doanh_nghiep'),
    path('doanhnghiep/sua/<int:ma_dn>/', admin_views.them_sua_doanhnghiep, name='sua_doanh_nghiep'),
    path('doanhnghiep/xoa/<int:ma_dn>/', admin_views.xoa_doanhnghiep, name='xoa_doanh_nghiep'),
    path('profile/<int:ma_dn>/', admin_views.profile_doanhnghiep, name='profile_doanhnghiep'),
 
    # Ngành nghề
    path('nganhnghe/them/', admin_views.them_sua_nganhnghe, name='them_nganh_nghe'),
    path('nganhnghe/sua/<int:ma_nganh>/', admin_views.them_sua_nganhnghe, name='sua_nganh_nghe'),
    path('nganhnghe/xoa/<int:ma_nganh>/', admin_views.xoa_nganhnghe, name='xoa_nganh_nghe'),
    # Hiệp hội
    path('hiephoi/them/', admin_views.them_sua_hiephoi, name='them_hiep_hoi'),
    path('hiephoi/sua/<int:ma_hh>/', admin_views.them_sua_hiephoi, name='sua_hiep_hoi'),
    path('hiephoi/xoa/<int:ma_hh>/', admin_views.xoa_hiep_hoi, name='xoa_hiep_hoi'),

    path('dangkyhoivien/them/', admin_views.them_sua_dangkyhoivien, name='them_đk_hoivien'),
    path('dangkyhoivien/sua/<int:ma_dk_hh>/', admin_views.them_sua_dangkyhoivien, name='sua_đk_hoivien'),
    path('dangkyhoivien/xoa/<int:ma_dk_hh>/', admin_views.xoa_dangkyhiephoi, name='xoa_dk_hoivien'),
    path('toggle-trang-thai-hiep-hoi/<int:MA_DK_HH>/', admin_views.toggle_tinh_trang_hiep_hoi, name='toggle_trang_thai_hiep_hoi'),
   
    path('hoivien/', views.hoivien, name='hoivien'),
    path('hoivien/<int:ma_dn>/', views.chitiethoivien, name='chitiethoivien'),

    path('hoivien/dangky/', views.dangky_hoivien_user, name='dangky_hoivien_user'),
    path('hoivien/dangky/them', views.dang_ky_hoi_vien, name='dang_ky_hoi_vien'),

    


]