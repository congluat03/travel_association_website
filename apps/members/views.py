import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, render, redirect
from .models import DoanhNghiep, NganhNghe, HiepHoi, TaiKhoan, DangKyHoiVien
from io import BytesIO
import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(request, 'core/home.html', {'title': 'Trang chủ'})

def hoivien(request):
    # Lọc doanh nghiệp đã duyệt
    doanh_nghiep = DoanhNghiep.objects.filter(dang_ky_hv__TINH_TRANG=1).distinct().order_by('-MA_DN')

    # Lấy toàn bộ danh sách ngành nghề
    cac_nganh = NganhNghe.objects.values_list('TEN_NGANH', flat=True).distinct()

    # Lọc theo từ khóa tìm kiếm và ngành nghề (nếu có)
    search = request.GET.get('search', '')
    nganh = request.GET.get('nganh', '')

    if search:
        doanh_nghiep = doanh_nghiep.filter(TEN_DN__icontains=search)

    if nganh:
        doanh_nghiep = doanh_nghiep.filter(MA_NGANH__TEN_NGANH=nganh)

    # Phân trang: hiển thị 6 doanh nghiệp mỗi trang
    paginator = Paginator(doanh_nghiep, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index/members/hoivien.html', {
        'doanh_nghiep': page_obj,
        'cac_nganh': cac_nganh,
    })

def chitiethoivien(request, ma_dn):
    dn = get_object_or_404(DoanhNghiep, MA_DN=ma_dn)
    # Lấy danh sách ngành nghề duy nhất (dùng cho combobox lọc)
    return render(request, 'index/members/chitiethoivien.html', {'dn': dn})

def dangky_hoivien_user(request):
    cac_hiephoi = HiepHoi.objects.all()
    cac_nganh = NganhNghe.objects.values_list('TEN_NGANH', flat=True).distinct()
    return render(request, 'index/members/dangkyhoivien.html',  { 'cac_nganh': cac_nganh, 'cac_hiephoi': cac_hiephoi })

def generate_qr_code(data: str):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    
    # Chuyển ảnh thành file để lưu vào mô hình
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return InMemoryUploadedFile(img_byte_arr, None, "qr.png", 'image/png', img_byte_arr.tell(), None)


def dang_ky_hoi_vien(request):
    if request.method == 'POST':
        # Lấy thông tin từ form
        ten_dn = request.POST.get('ten_dn')
        ma_nganh = request.POST.get('ma_nganh')  # Dữ liệu chuỗi, ví dụ 'Khách Sạn'
        dia_chi = request.POST.get('dia_chi')
        sdt_dn = request.POST.get('sdt_dn')
        email_dn = request.POST.get('email_dn')
        nguoi_dai_dien = request.POST.get('nguoi_dai_dien')

        # Truy vấn đối tượng NganhNghe dựa trên TEN_NGANH
        try:
            nganh = NganhNghe.objects.get(TEN_NGANH=ma_nganh)  # Tìm theo tên ngành nghề
            doanh_nghiep = DoanhNghiep.objects.create(
                MA_NGANH=nganh,  # Gán đối tượng NganhNghe vào MA_NGANH
                TEN_DN=ten_dn,
                DIA_CHI=dia_chi,
                SDT_DN=sdt_dn,
                EMAIL_DN=email_dn,
                NGUOI_DAI_DIEN=nguoi_dai_dien,
                TRANG_THAI_DUYET=0  # Mặc định là Chưa duyệt
            )

            # Lưu đối tượng DoanhNghiep trước khi truy cập id
            doanh_nghiep.save()

            # Tạo mã QR cho doanh nghiệp
            qr_data = f"{ten_dn} - {email_dn} - {sdt_dn}"
            qr_code_image = generate_qr_code(qr_data)
            doanh_nghiep.MA_QR.save(f"{ten_dn}_qr.png", qr_code_image, save=True)

        except NganhNghe.DoesNotExist:
            return JsonResponse({'error': 'Ngành nghề không tồn tại.'}, status=400)

        # Lấy thông tin hiệp hội và tài khoản
        ma_hiephoi = request.POST.get('ma_hiephoi')
        ten_dang_nhap = request.POST.get('ten_dang_nhap')
        email_tk = request.POST.get('email_tk')
        mat_khau = request.POST.get('mat_khau')
        hinh_tk = request.FILES.get('hinh_tk')

        # Tạo tài khoản người dùng
        try:
            hiep_hoi = HiepHoi.objects.get(MA_HH=ma_hiephoi)  # Sử dụng MA_HH để tìm hiệp hội

            # Lưu ảnh đại diện nếu có
            image_path = None
            if hinh_tk:
                folder_path = os.path.join('taikhoan', str(doanh_nghiep.MA_DN))  # Sử dụng doanh_nghiep.MA_DN thay vì id
                full_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
                os.makedirs(full_folder_path, exist_ok=True)

                image_path = os.path.join(folder_path, hinh_tk.name)
                with default_storage.open(image_path, 'wb+') as destination:
                    for chunk in hinh_tk.chunks():
                        destination.write(chunk)

            # Tạo tài khoản người dùng
            tai_khoan = TaiKhoan.objects.create(
                MA_DN=doanh_nghiep,
                EMAIL_TK=email_tk,
                TEN_DANG_NHAP=ten_dang_nhap,
                MAT_KHAU=make_password(mat_khau),  # Mã hóa mật khẩu
                VAI_TRO="nhanvien",  # Mặc định là Nhân viên
                TRANG_THAI_TK=True,
                NGAY_DANG_KY_TK=timezone.now(),
                HINH_TK=image_path if image_path else None
            )
        except HiepHoi.DoesNotExist:
            return JsonResponse({'error': 'Hiệp hội không tồn tại.'}, status=400)

        # Đăng ký hội viên cho doanh nghiệp
        try:
            DangKyHoiVien.objects.create(
                MA_HH=hiep_hoi,
                MA_DN=doanh_nghiep,
                TINH_TRANG=0,  # Chưa duyệt
                NGAY_DANG_KY=timezone.now()
            )
        except Exception as e:
            return JsonResponse({'error': f"Đăng ký hội viên thất bại: {str(e)}"}, status=400)

        # Quay lại trang danh sách hội viên hoặc trang khác
        return redirect('/members/hoivien/')  # Hoặc trang khác mà bạn muốn điều hướng

    else:
        # Nếu không phải POST, chuyển hướng về trang khác hoặc trả về form đăng ký
        return redirect('/members/hoivien/dangky/')
  
