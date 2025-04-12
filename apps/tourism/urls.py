from django.urls import path
from . import views, admin_views

app_name = 'tourism'
urlpatterns = [
    # path('', views.home, name='tourism'),
    # Địa điểm du lịch
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