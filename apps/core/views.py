from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    return render(request, 'index/index_layout.html', {'title': 'Trang chủ'})