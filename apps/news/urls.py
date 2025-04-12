from django.urls import path
from . import admin_views  # ✅ import đúng file


app_name = 'news'

urlpatterns = [
    # Tin tức
    path('tintuc/', admin_views.tintuc_list),
    path('tintuc/<int:pk>/', admin_views.tintuc_detail),

    # Thẻ tag
    path('thetag/', admin_views.thetag_list),
    path('thetag/<int:pk>/', admin_views.thetag_detail),

    path('trackingxemtin/', admin_views.trackingxemtin_list, name='trackingxemtin-list'),
    path('trackingxemtin/<int:pk>/', admin_views.trackingxemtin_detail, name='trackingxemtin-detail'),
]