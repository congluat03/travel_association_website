from django.urls import path
from . import views

app_name = 'tourism'
urlpatterns = [
    path('', views.home, name='tourism'),
]