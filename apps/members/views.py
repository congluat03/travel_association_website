from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from apps.members.models import TaiKhoan,DoanhNghiep,NganhNghe,HiepHoi,DangKyHoiVien
from apps.tourism.models import DiaDiemDuLich
from .admin_views import them_sua_dangkyhoivien
# Create your views here.
def home(request):
    return render(request, 'core/home.html', {'title': 'Trang chủ'})

def hoivien(request):
    doanh_nghiep = DoanhNghiep.objects.filter(TRANG_THAI_DUYET=1)  # Tìm các doanh nghiệp đã duyệt
    return render(request, 'index/members/hoivien.html', {'doanh_nghiep': doanh_nghiep})

def chitiethoivien(request, ma_dn):
    dn = get_object_or_404(DoanhNghiep, MA_DN=ma_dn)
    return render(request, 'index/members/chitiethoivien.html', {'dn': dn})
def dangky_hoivien_user(request):
    return redirect('hoivien')  # fallback nếu không phải POST