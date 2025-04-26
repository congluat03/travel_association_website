from django.urls import path
from . import admin_views  # ✅ import đúng file


app_name = 'news'

urlpatterns = [  
    # Thẻ tag
    path('thetag/them/', admin_views.them_sua_tag, name='them_tag'),  # Thêm thẻ tag
    path('thetag/sua/<int:ma_tag>/', admin_views.them_sua_tag, name='sua_tag'),  # Sửa thẻ tag
    path('thetag/xoa/<str:ma_tag>/', admin_views.xoa_thetag, name='xoa_thetag'),
    # Tin tức
    path('tintuc/them/', admin_views.them_sua_tintuc, name='them_tin_tuc'),  # Thêm thẻ tag
    path('tintuc/sua/<int:ma_tin>/', admin_views.them_sua_tintuc, name='sua_tin_tuc'),  # Sửa thẻ tag
    path('tintuc/xoa/<int:ma_tin>/', admin_views.xoa_news, name='xoa_news'),
]