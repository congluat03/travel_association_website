from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from apps.members.models import TaiKhoan,DoanhNghiep,NganhNghe,HiepHoi,DangKyHoiVien
from apps.tourism.models import DiaDiemDuLich
from apps.news.models import TinTuc
from apps.support.models import TaiLieu
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
# View cho trang chủ
def trang_chu(request):
    # Lấy 6 địa điểm đầu tiên
    dia_diem = DiaDiemDuLich.objects.all()[:3]
    
    # Lấy 5 tin tức mới nhất, ưu tiên tin nổi bật
    tin_tuc = TinTuc.objects.order_by('-TIN_NOI_BAT', '-NGAY_DANG')[:5]
    
    # Lấy 3 tài liệu đầu tiên
    tai_lieu = TaiLieu.objects.order_by('-NGAY_CAP_NHAT')[:3]
    
    # Lấy 3 đăng ký hội viên đã duyệt
    dang_ky_hoi_vien = DangKyHoiVien.objects.filter(TINH_TRANG=1)[:3]
    khu_list = DiaDiemDuLich.objects.values_list('VI_TRI', flat=True).distinct()
    
    context = {
        'dia_diem': dia_diem,
        'tin_tuc': tin_tuc,
        'tai_lieu': tai_lieu,
        'dang_ky_hoi_vien': dang_ky_hoi_vien,
    }
    return render(request, 'index/home/home.html', context)


def gioithieu(request):
    # Lấy tất cả thông tin từ bảng DoanhNghiep
    doanh_nghiep = DoanhNghiep.objects.all()
    
    # Chuyển dữ liệu vào context
    context = {'doanh_nghiep': doanh_nghiep}
    
    # Render trang giới thiệu
    return render(request, 'index/gioithieu/gioithieu.html', context)

