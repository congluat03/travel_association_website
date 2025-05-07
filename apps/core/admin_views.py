import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from apps.tourism.models import DiaDiemDuLich, DacSan, ThuocTour, TourDuLich  
from apps.news.models import TheTag, TinTuc
from apps.members.models import DoanhNghiep, TaiKhoan
from apps.support.models import TaiLieu
from apps.members.models import TaiKhoan,DoanhNghiep,NganhNghe,HiepHoi,DangKyHoiVien
from .decorators import login_required_custom

@login_required_custom
def admin_dashboard(request):
    user = request.user_info  # Lấy thông tin người dùng từ request.user_info

    # Lấy số lượng các đối tượng từ các bảng khác
    num_members = DoanhNghiep.objects.count()
    num_news = TinTuc.objects.count()
    num_destinations = DiaDiemDuLich.objects.count()
    num_guides = DacSan.objects.count()
    num_tours = TourDuLich.objects.count()

    # Truyền dữ liệu vào template
    context = {
        'user': user,
        'num_members': num_members,
        'num_news': num_news,
        'num_destinations': num_destinations,
        'num_guides': num_guides,
        'num_tours': num_tours,
    }

    # Render trang quản trị với dữ liệu thống kê và thông tin người dùng
    return render(request, 'admin/dashboard.html', context)
@login_required_custom
def staff_dashboard(request):
    return render(request, 'admin/dashboard.html')
@login_required_custom
def profile_view(request):
    user = request.user_info  # Lấy thông tin người dùng từ request.user_info
    return render(request, 'auth/profile.html', {'user': user})

@login_required_custom
def manage_members(request):
    user = request.user_info  # Lấy thông tin người dùng từ request.user_info
    taikhoan = TaiKhoan.objects.select_related('MA_DN').all()
    # Lấy danh sách đăng ký hội viên
    dangkyhoivien = DangKyHoiVien.objects.all()

    doanhnghiep = DoanhNghiep.objects.all()
    
    return render(request, 'admin/members/members.html', {
        'taikhoan': taikhoan,
        'dangkyhoivien': dangkyhoivien,  # Truyền danh sách tài liệu vào context
        'doanhnghiep': doanhnghiep,  # Truyền danh sách tài liệu vào context
        'user': user
    })

@login_required_custom
def manage_business(request):
    user = request.user_info  # Lấy thông tin người dùng từ request.user_info
    # Lấy danh sách tài khoản và liên kết doanh nghiệp
    taikhoan = TaiKhoan.objects.select_related('MA_DN').all()
    
    # Lấy tất cả doanh nghiệp
    doanhnghiep = DoanhNghiep.objects.all()
    
    # Lấy danh sách hiệp hội
    hiepHoi = HiepHoi.objects.all()
    
    # Lấy danh sách ngành nghề
    nganhnghe = NganhNghe.objects.all()

    # Lấy danh sách đăng ký hội viên
    dangkyhoivien = DangKyHoiVien.objects.all()

    return render(request, 'admin/members/business.html', {
        'taikhoan': taikhoan,
        'doanhnghiep': doanhnghiep,
        'nganhnghe': nganhnghe,
        'hiepHoi': hiepHoi,
        'dangkyhoivien': dangkyhoivien,
        'user': user
    })

@login_required_custom
def manage_news(request):
    user = request.user_info  # Lấy thông tin người dùng từ request.user_info
    # Lấy tất cả thẻ tag, tin tức và tài khoản từ cơ sở dữ liệu
    tags = TheTag.objects.all()
    news_list = TinTuc.objects.all()
    tai_khoans = TaiKhoan.objects.all()  # Lấy dữ liệu tài khoản

    # Truyền dữ liệu vào template
    return render(request, 'admin/news/news.html', {
        'tags': tags,
        'news_list': news_list,
        'tai_khoans': tai_khoans,  # Truyền dữ liệu tài khoản vào template
        'user': user
    })

@login_required_custom
def manage_support(request):
    user = request.user_info  # Lấy thông tin người dùng từ request.user_info
    doanhnghieps = DoanhNghiep.objects.all()
    tailieus = TaiLieu.objects.all()  # Lấy tất cả tài liệu
    return render(request, 'admin/support/support.html', {
        'doanhnghieps': doanhnghieps,
        'tailieus': tailieus,  # Truyền danh sách tài liệu vào context
        'user': user
    })

# @login_required_custom
def get_image_list(folder_name):
    folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)
    image_list = []

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        image_list = [
            os.path.join(settings.MEDIA_URL, folder_name, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
        ]
    
    return image_list

@login_required_custom
def manage_tourism(request):
    user = request.user_info  # Lấy thông tin người dùng từ request.user_info
    # Lấy danh sách địa điểm du lịch, doanh nghiệp, đặc sản, tours và schedules
    dia_diems = DiaDiemDuLich.objects.all()
    doanhnghiep_list = DoanhNghiep.objects.all()
    dac_sans = DacSan.objects.select_related('MA_DD').all()
    tours = TourDuLich.objects.prefetch_related('thuoctour_set__MA_DD').all()
    schedules = ThuocTour.objects.select_related('MA_TOUR', 'MA_DD').all().order_by('THOI_GIAN_DI')

    # Lấy ảnh đặc sản
    for ds in dac_sans:
        folder_name = f'dacsan/{ds.MA_DS}'
        ds.image_list = get_image_list(folder_name)

    # Lấy ảnh của địa điểm du lịch
    for dd in dia_diems:
        folder_name = f'diadiem/{dd.MA_DD}'
        dd.image_list = get_image_list(folder_name)

    # Lấy ảnh của tour du lịch
    for tour in tours:
        folder_name = f'tourdulich/{tour.MA_TOUR}'
        tour.image_list = get_image_list(folder_name)

    # Trả về trang quản lý với dữ liệu
    return render(
        request,
        'admin/tourism/tourism.html',
        {
            'dia_diems': dia_diems,
            'doanhnghiep_list': doanhnghiep_list,
            'dac_sans': dac_sans,
            'tours': tours,
            'schedules': schedules,
            'user': user
        }
    )
