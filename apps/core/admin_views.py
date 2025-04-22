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
# Create your views here.
def home(request):
    return render(request, 'index/index_layout.html', {'title': 'Trang chủ'})
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin/auth/login.html', {'error': 'Sai tài khoản hoặc mật khẩu'})
    return render(request, 'admin/auth/login.html')
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'admin/auth/register.html', {'error': 'Mật khẩu không khớp!'})

        if User.objects.filter(username=username).exists():
            return render(request, 'admin/auth/register.html', {'error': 'Tên đăng nhập đã tồn tại!'})

        User.objects.create_user(username=username, email=email, password=password1)
        return redirect('login')  # hoặc chuyển đến trang khác

    return render(request, 'admin/auth/register.html')
# @login_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

# @login_required
def manage_members(request):
    taikhoan = TaiKhoan.objects.all()
    return render(request, 'admin/members/members.html', {
            'taikhoan': taikhoan})

# @login_required
def manage_news(request):
    # Lấy tất cả thẻ tag, tin tức và tài khoản từ cơ sở dữ liệu
    tags = TheTag.objects.all()
    news_list = TinTuc.objects.all()
    tai_khoans = TaiKhoan.objects.all()  # Lấy dữ liệu tài khoản

    # Truyền dữ liệu vào template
    return render(request, 'admin/news/news.html', {
        'tags': tags,
        'news_list': news_list,
        'tai_khoans': tai_khoans,  # Truyền dữ liệu tài khoản vào template
    })

def manage_support(request):
    doanhnghieps = DoanhNghiep.objects.all()
    tailieus = TaiLieu.objects.all()  # Lấy tất cả tài liệu
    return render(request, 'admin/support/support.html', {
        'doanhnghieps': doanhnghieps,
        'tailieus': tailieus  # Truyền danh sách tài liệu vào context
    })

# @login_required
def manage_tourism(request):
    dia_diems = DiaDiemDuLich.objects.all()
    doanhnghiep_list = DoanhNghiep.objects.all()
    dac_sans = DacSan.objects.select_related('MA_DD').all()
    tours = TourDuLich.objects.prefetch_related('thuoctour_set__MA_DD').all()
    schedules = ThuocTour.objects.select_related('MA_TOUR', 'MA_DD').all().order_by('THOI_GIAN_DI')

    for ds in dac_sans:
        # Lấy thư mục chứa ảnh, ví dụ: dacsan/23
        folder_name = f'dacsan/{ds.MA_DS}'
        folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            ds.image_list = [
                os.path.join(settings.MEDIA_URL, folder_name, f)
                for f in os.listdir(folder_path)
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
            ]
        else:
            ds.image_list = []

    return render(
        request,
        'admin/tourism/tourism.html',
        {
            'dia_diems': dia_diems,
            'doanhnghiep_list': doanhnghiep_list,
            'dac_sans': dac_sans,
            'tours': tours,
            'schedules': schedules,
        }
    )