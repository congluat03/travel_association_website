from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from apps.members.models import TaiKhoan,DoanhNghiep,NganhNghe,HiepHoi,DangKyHoiVien
from apps.tourism.models import DiaDiemDuLich, TourDuLich
from apps.news.models import TinTuc
from apps.support.models import TaiLieu
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, 'index/index_layout.html', {'title': 'Trang chủ'})
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = TaiKhoan.objects.get(TEN_DANG_NHAP=username)
            if user.check_mat_khau(password):
                if user.TRANG_THAI_TK:
                    # Lưu thông tin vào session
                    request.session['user_id'] = user.MA_TK
                    request.session['username'] = user.TEN_DANG_NHAP
                    request.session['vai_tro'] = user.VAI_TRO
                    
                    # Điều hướng dựa trên vai trò
                    if user.VAI_TRO == 'admin':
                        return redirect('admin_dashboard')
                    elif user.VAI_TRO == 'nhanvien':                       
                        return redirect('admin_dashboard')
                    else:
                        return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Tài khoản đã bị khóa.')
            else:
                messages.error(request, 'Mật khẩu không đúng.')
        except TaiKhoan.DoesNotExist:
            messages.error(request, 'Tài khoản không tồn tại.')

    return render(request, 'auth/login.html')

def custom_logout(request):
    request.session.flush()
    return redirect('custom_login')
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'auth/register.html', {'error': 'Mật khẩu không khớp!'})

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {'error': 'Tên đăng nhập đã tồn tại!'})

        User.objects.create_user(username=username, email=email, password=password1)
        return redirect('login')  # hoặc chuyển đến trang khác

    return render(request, 'auth/register.html')

def trang_chu(request):
    # Lấy 3 địa điểm đầu tiên
    dia_diem = DiaDiemDuLich.objects.all()[:3]
    
    # Lấy 5 tin tức mới nhất, ưu tiên tin nổi bật
    tin_tuc = TinTuc.objects.order_by('-TIN_NOI_BAT', '-NGAY_DANG')[:5]
    
    # Lấy 3 tài liệu đầu tiên
    tai_lieu = TaiLieu.objects.order_by('-NGAY_CAP_NHAT')[:3]
    
    # Lấy 3 đăng ký hội viên đã duyệt
    dang_ky_hoi_vien = DangKyHoiVien.objects.filter(TINH_TRANG=1)[:3]
    
    # Lấy các vị trí địa lý
    khu_list = DiaDiemDuLich.objects.values_list('VI_TRI', flat=True).distinct()
    
    # Lấy tất cả các tour
    tours = TourDuLich.objects.order_by('-MA_TOUR')[:3]


    # Tính giá theo triệu và làm tròn, bỏ phần ".0" nếu là số nguyên
    for tour in tours:
        tour.gia_trieu = round(tour.GIA_TOUR / 1_000_000, 1)
        # Kiểm tra nếu giá trị là số nguyên bằng cách so sánh với giá trị làm tròn
        if tour.gia_trieu == int(tour.gia_trieu):
            tour.gia_trieu = int(tour.gia_trieu)  # Nếu là số nguyên, bỏ phần ".0"
    
    # Trả về context với các đối tượng
    context = {
        'dia_diem': dia_diem,
        'tin_tuc': tin_tuc,
        'tai_lieu': tai_lieu,
        'dang_ky_hoi_vien': dang_ky_hoi_vien,
        'tours': tours,
        'khu_list': khu_list,  # Thêm danh sách khu vực vào context nếu cần
    }
    
    return render(request, 'index/home/home.html', context)

def gioithieu(request):
    # Lấy tất cả thông tin từ bảng DoanhNghiep
    doanh_nghiep = DoanhNghiep.objects.order_by('-MA_DN')[:3]

    
    # Chuyển dữ liệu vào context
    context = {'doanh_nghiep': doanh_nghiep}
    
    # Render trang giới thiệu
    return render(request, 'index/introduce/introduce.html', context)

def lienhe(request):
     if request.method == 'POST':
         ho_ten = request.POST.get('ho_ten', '').strip()
         email = request.POST.get('email', '').strip()
         so_dien_thoai = request.POST.get('so_dien_thoai', '').strip()
         noi_dung = request.POST.get('noi_dung', '').strip()
         
         # TODO: Xử lý dữ liệu ở đây (ví dụ: lưu database hoặc gửi email)
         # print(ho_ten, email, so_dien_thoai, noi_dung)
 
         if ho_ten and email and noi_dung:
             messages.success(request, 'Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi trong thời gian sớm nhất.')
         else:
             messages.error(request, 'Vui lòng điền đầy đủ thông tin trước khi gửi liên hệ.')
 
         return redirect('core:contact')  # <-- sửa đúng đây nè
 
     return render(request, 'index/contact/contact.html')