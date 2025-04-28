from django.urls import path
from . import admin_views  # ✅ import đúng file
from . import views

app_name = 'news'

urlpatterns = [
    # Tin tức
    path('tintuc/', admin_views.tintuc_list),
    path('tintuc/<int:pk>/', admin_views.tintuc_detail),

    # Thẻ tag
    path('thetag/them/', admin_views.them_sua_tag, name='them_tag'),  # Thêm thẻ tag
    path('thetag/sua/<int:ma_tag>/', admin_views.them_sua_tag, name='sua_tag'),  # Sửa thẻ tag
    path('thetag/xoa/<str:ma_tag>/', admin_views.xoa_thetag, name='xoa_thetag'),

    path('tintuc/them/', admin_views.them_sua_tintuc, name='them_tin_tuc'),  # Thêm thẻ tag
    path('tintuc/sua/<int:ma_tin>/', admin_views.them_sua_tintuc, name='sua_tin_tuc'),  # Sửa thẻ tag
    path('tintuc/xoa/<int:ma_tin>/', admin_views.xoa_news, name='xoa_news'),


    path('thetag/', admin_views.thetag_list),
    path('thetag/<int:pk>/', admin_views.thetag_detail),

    path('trackingxemtin/', admin_views.trackingxemtin_list, name='trackingxemtin-list'),
    path('trackingxemtin/<int:pk>/', admin_views.trackingxemtin_detail, name='trackingxemtin-detail'), 
    # phần index
    path('tintucsukien/', views.danhsachtintuc, name='danhsachtintucsukien'),
    path('tintucsukien/<int:ma_tin>/', views.chitiettintuc, name='chitiettintucsukien')
]