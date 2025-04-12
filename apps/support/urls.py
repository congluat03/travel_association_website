from django.urls import path
from . import admin_views

app_name = 'support'
urlpatterns = [
    path('tailieu/', admin_views.tailieu_list, name='tailieu-list'),
    path('tailieu/<int:pk>/', admin_views.tailieu_detail, name='tailieu-detail'),
]