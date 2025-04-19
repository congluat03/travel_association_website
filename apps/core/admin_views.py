from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from apps.members.models import TaiKhoan,DoanhNghiep,NganhNghe,HiepHoi,DangKyHoiVien

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

    return render(request, 'admin/members/members.html', {
        'taikhoan': taikhoan,
        'doanhnghiep': doanhnghiep,
        'nganhnghe': nganhnghe,
        'hiepHoi': hiepHoi,
        'dangkyhoivien': dangkyhoivien
    })




# @login_required
def manage_news(request):
    return render(request, 'admin/news/news.html')

def manage_support(request):
    return render(request, 'admin/support/support.html')

# @login_required
def manage_tourism(request):
    return render(request, 'admin/tourism/tourism.html')