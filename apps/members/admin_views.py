import shutil
from django.shortcuts import render, redirect
from .models import TaiKhoan, DoanhNghiep, NganhNghe, HiepHoi, DangKyHoiVien
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
import qrcode
from io import BytesIO
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
import os
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Doanh Nghiệp
def them_sua_hiephoi(request, ma_hh=None):
    hiephoi = HiepHoi.objects.filter(pk=ma_hh).first() if ma_hh else None

    if request.method == 'POST':
        ten_hiephoi = request.POST.get('TEN_HH')
        mo_ta = request.POST.get('MO_TA_HH')

        if hiephoi:
            # Sửa hội nghị
            hiephoi.TEN_HH = ten_hiephoi
            hiephoi.MO_TA_HH = mo_ta
            hiephoi.save()
        else:
            # Thêm mới hội nghị
            HiepHoi.objects.create(
                TEN_HH=ten_hiephoi,
                MO_TA_HH=mo_ta
            )

        return redirect('admin_core:manage_business')

    return redirect('admin_core:manage_business')

def xoa_hiep_hoi(request, ma_hh):
    try:
        hiep_hoi = HiepHoi.objects.get(MA_HH=ma_hh)
        hiep_hoi.delete()  # Xóa hiệp hội
        return redirect('admin_core:manage_business')  # Quay lại trang quản lý hiệp hội
    except HiepHoi.DoesNotExist:
        raise Http404("Hiệp hội không tồn tại.")
    
def them_sua_nganhnghe(request, ma_nganh=None):
    nganh = NganhNghe.objects.filter(pk=ma_nganh).first() if ma_nganh else None

    if request.method == 'POST':
        ten_nganh = request.POST.get('TEN_NGANH')

        if nganh:
            # Sửa ngành nghề
            nganh.TEN_NGANH = ten_nganh
            nganh.save()
        else:
            # Thêm mới ngành nghề
            NganhNghe.objects.create(
                TEN_NGANH=ten_nganh
            )

        return redirect('admin_core:manage_business')

    return redirect('admin_core:manage_business')

def xoa_nganhnghe(request, ma_nganh):
    try:
        nganh = NganhNghe.objects.get(MA_NGANH=ma_nganh)
        nganh.delete()
        return redirect('admin_core:manage_business')
    except NganhNghe.DoesNotExist:
        raise Http404("Ngành nghề không tồn tại.")

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

def them_sua_doanhnghiep(request, ma_dn=None):
    doanhnghiep = DoanhNghiep.objects.filter(pk=ma_dn).first() if ma_dn else None

    if request.method == 'POST':
        ten_doanhnghiep = request.POST.get('TEN_DN')
        nguoi_dai_dien = request.POST.get('NGUOI_DAI_DIEN')
        email = request.POST.get('EMAIL_DN')
        sdt = request.POST.get('SDT_DN')
        dia_chi = request.POST.get('DIA_CHI')
        ma_nganh = request.POST.get('MA_NGANH')
        trang_thai_duyet = request.POST.get('TRANG_THAI_DUYET')
        qr_data = f"{ten_doanhnghiep} - {email} - {sdt}"

        if doanhnghiep:
            # Nếu có mã QR cũ thì xóa file cũ trước
            if doanhnghiep.MA_QR:
                qr_path = doanhnghiep.MA_QR.path
                if os.path.isfile(qr_path):
                    os.remove(qr_path)

            # Cập nhật thông tin doanh nghiệp
            doanhnghiep.TEN_DN = ten_doanhnghiep
            doanhnghiep.NGUOI_DAI_DIEN = nguoi_dai_dien
            doanhnghiep.EMAIL_DN = email
            doanhnghiep.SDT_DN = sdt
            doanhnghiep.DIA_CHI = dia_chi
            doanhnghiep.MA_NGANH = NganhNghe.objects.get(MA_NGANH=ma_nganh)
            doanhnghiep.TRANG_THAI_DUYET = trang_thai_duyet
            doanhnghiep.save()

            # Tạo mã QR mới (dùng MA_DN làm tên file)
            qr_code_image = generate_qr_code(qr_data)
            doanhnghiep.MA_QR.save(f"{doanhnghiep.MA_DN}_qr.png", qr_code_image, save=True)

        else:
            # Thêm mới doanh nghiệp
            doanhnghiep = DoanhNghiep.objects.create(
                TEN_DN=ten_doanhnghiep,
                NGUOI_DAI_DIEN=nguoi_dai_dien,
                EMAIL_DN=email,
                SDT_DN=sdt,
                DIA_CHI=dia_chi,
                MA_NGANH=NganhNghe.objects.get(MA_NGANH=ma_nganh),
                TRANG_THAI_DUYET=trang_thai_duyet
            )

            # Sau khi tạo mới xong, dùng MA_DN để đặt tên file QR
            qr_code_image = generate_qr_code(qr_data)
            doanhnghiep.MA_QR.save(f"{doanhnghiep.MA_DN}_qr.png", qr_code_image, save=True)

    return redirect('admin_core:manage_business')

def xoa_doanhnghiep(request, ma_dn):
    try:
        doanhnghiep = DoanhNghiep.objects.get(MA_DN=ma_dn)

        # Xóa file QR code nếu tồn tại
        if doanhnghiep.MA_QR:
            qr_path = doanhnghiep.MA_QR.path
            if qr_path and os.path.exists(qr_path):
                try:
                    os.remove(qr_path)
                except Exception as e:
                    print(f"Không thể xóa file QR: {e}")

        # Xóa doanh nghiệp trong DB
        doanhnghiep.delete()

        return redirect('admin_core:manage_business')
    except DoanhNghiep.DoesNotExist:
        raise Http404("Doanh nghiệp không tồn tại.")

def profile_doanhnghiep(request, ma_dn):
    dn = get_object_or_404(DoanhNghiep, pk=ma_dn)
    return render(request, 'admin/members/doanhnghiep/profile_doanhnghiep.html', {'dn': dn})

# Thành Viên
def xoa_tai_khoan(request, ma_tk):
    try:
        # Tìm đối tượng tài khoản theo MA_TK
        taikhoan = TaiKhoan.objects.get(MA_TK=ma_tk)

        # Lấy đường dẫn thư mục chứa hình ảnh của tài khoản
        folder_path = os.path.join(settings.MEDIA_ROOT, 'taikhoan', str(taikhoan.MA_TK))

        # Nếu thư mục chứa hình ảnh tồn tại, xóa thư mục
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # Xóa đối tượng khỏi cơ sở dữ liệu
        taikhoan.delete()

        # Chuyển hướng về trang quản lý thành viên
        return redirect('admin_core:manage_members')

    except TaiKhoan.DoesNotExist:
        raise Http404("Tài khoản không tồn tại.")

def them_sua_taikhoan(request, id=None):
    taikhoan = get_object_or_404(TaiKhoan, pk=id) if id else None

    if request.method == "POST":
        data = request.POST
        file = request.FILES.get("ANH_DAI_DIEN")  # Trường ảnh đại diện
        ma_dn = data.get("MA_DN")

        if taikhoan:
            # === SỬA TÀI KHOẢN ===
            taikhoan.EMAIL_TK = data.get("EMAIL_TK")
            taikhoan.TEN_DANG_NHAP = data.get("TEN_DANG_NHAP")

            password = data.get("MAT_KHAU")
            if password:
                taikhoan.MAT_KHAU = make_password(password)

            taikhoan.VAI_TRO = data.get("VAI_TRO")
            taikhoan.TRANG_THAI_TK = data.get("TRANG_THAI_TK") == '1'
            taikhoan.MA_DN_id = ma_dn or None

            if file:
                # XÓA ẢNH CŨ nếu có
                if taikhoan.HINH_TK and default_storage.exists(str(taikhoan.HINH_TK)):
                    default_storage.delete(str(taikhoan.HINH_TK))

                # LƯU ẢNH MỚI
                folder_path = os.path.join('taikhoan', str(taikhoan.MA_TK))
                full_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
                os.makedirs(full_folder_path, exist_ok=True)

                image_path = os.path.join(folder_path, file.name)
                with default_storage.open(image_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                taikhoan.HINH_TK = image_path

            taikhoan.save()

        else:
            # === THÊM MỚI TÀI KHOẢN ===
            password = data.get("MAT_KHAU")
            new_account = TaiKhoan(
                EMAIL_TK=data.get("EMAIL_TK"),
                TEN_DANG_NHAP=data.get("TEN_DANG_NHAP"),
                VAI_TRO=data.get("VAI_TRO"),
                TRANG_THAI_TK=data.get("TRANG_THAI_TK") == '1',
                MA_DN_id=ma_dn or None,
            )

            if password:
                new_account.MAT_KHAU = make_password(password)

            new_account.save()  # Lưu để có MA_TK

            if file:
                folder_path = os.path.join('taikhoan', str(new_account.MA_TK))
                full_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
                os.makedirs(full_folder_path, exist_ok=True)

                image_path = os.path.join(folder_path, file.name)
                with default_storage.open(image_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                new_account.HINH_TK = image_path
                new_account.save()

        return redirect('admin_core:manage_members')

    return redirect('admin_core:manage_members')

def them_sua_dangkyhoivien(request, ma_dk_hh=None):
    dangky = DangKyHoiVien.objects.filter(pk=ma_dk_hh).first() if ma_dk_hh else None

    if request.method == 'POST':
        ma_hh = request.POST.get('MA_HH')
        ma_dn = request.POST.get('MA_DN')
        tinh_trang = request.POST.get('TINH_TRANG')
        ngay_dang_ky = request.POST.get('NGAY_DANG_KY')  # dạng 'YYYY-MM-DD'

        # Debug kiểm tra đầu vào
        print(f"MA_HH: {ma_hh}, MA_DN: {ma_dn}, TINH_TRANG: {tinh_trang}, NGAY_DANG_KY: {ngay_dang_ky}")

        # Kiểm tra nếu ngày đăng ký hợp lệ
        try:
            ngay_dk = datetime.strptime(ngay_dang_ky, '%Y-%m-%d').date() if ngay_dang_ky else None
        except ValueError as e:
            print(f"Error parsing date: {e}")
            ngay_dk = None

        # Kiểm tra và lấy đối tượng Hiệp hội và Doanh nghiệp
        hiep_hoi = get_object_or_404(HiepHoi, pk=ma_hh)
        doanh_nghiep = get_object_or_404(DoanhNghiep, pk=ma_dn)

        # Kiểm tra tình trạng duyệt có hợp lệ
        try:
            tinh_trang_int = int(tinh_trang) if tinh_trang else 0  # Mặc định là 0 nếu không có giá trị
            if tinh_trang_int not in [0, 1]:  # Đảm bảo chỉ nhận giá trị 0 hoặc 1
                tinh_trang_int = 0  # Mặc định là 0 nếu giá trị không hợp lệ
        except ValueError as e:
            print(f"Error converting TINH_TRANG to integer: {e}")
            tinh_trang_int = 0  # Mặc định là 0 nếu lỗi

        # Xử lý dữ liệu và lưu vào cơ sở dữ liệu
        if dangky:
            # Sửa đăng ký hội viên
            dangky.MA_HH = hiep_hoi
            dangky.MA_DN = doanh_nghiep
            dangky.TINH_TRANG = tinh_trang_int
            dangky.NGAY_DANG_KY = ngay_dk
            dangky.save()
        else:
            # Thêm mới đăng ký hội viên
            DangKyHoiVien.objects.create(
                MA_HH=hiep_hoi,
                MA_DN=doanh_nghiep,
                TINH_TRANG=tinh_trang_int,
                NGAY_DANG_KY=ngay_dk
            )

        # Sau khi xử lý, chuyển hướng về trang quản lý đăng ký
        return redirect('admin_core:manage_members')

    return redirect('admin_core:manage_members')

def xoa_dangkyhiephoi(request, ma_dk_hh):
    try:
        dangkihoivien = DangKyHoiVien.objects.get(MA_DK_HH=ma_dk_hh)
        dangkihoivien.delete()
        return redirect('admin_core:manage_members')  # hoặc redirect nếu muốn
    except DangKyHoiVien.DoesNotExist:
        raise Http404(" hiệp hội đăng kí không tồn tại.")  


@csrf_exempt
def toggle_trang_thai_tai_khoan(request, ma_tk):
    if request.method == 'POST':
        try:
            tk = TaiKhoan.objects.get(pk=ma_tk)
            tk.TRANG_THAI_TK = not tk.TRANG_THAI_TK
            tk.save()
            return JsonResponse({'success': True, 'new_status': tk.TRANG_THAI_TK})
        except TaiKhoan.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tài khoản không tồn tại'}, status=404)
    return JsonResponse({'success': False, 'error': 'Phương thức không hợp lệ'}, status=400)

@csrf_exempt
def toggle_tinh_trang_hiep_hoi(request, MA_DK_HH):
    # return JsonResponse({'success': True, 'new_status': MA_DK_HH})
    if request.method == 'POST':
        try:
            dk = DangKyHoiVien.objects.get(pk=MA_DK_HH)
            # Chuyển trạng thái từ '0' (Chưa duyệt) sang '1' (Duyệt) và ngược lại
            dk.TINH_TRANG = not dk.TINH_TRANG
            dk.save()
            return JsonResponse({'success': True, 'new_status': dk.TINH_TRANG})
        except DangKyHoiVien.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Đăng ký hội viên không tồn tại'}, status=404)
    return JsonResponse({'success': False, 'error': 'Phương thức không hợp lệ'}, status=400)
