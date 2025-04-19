from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from .models import TaiKhoan, DoanhNghiep, NganhNghe, HiepHoi, DangKyHoiVien
from .serializers import TaiKhoanSerializer, DoanhNghiepSerializer, NganhNgheSerializer, HiepHoiSerializer, DangKyHoiVienSerializer
from django.http import Http404,HttpResponse
from apps.core import admin_views
from django.shortcuts import get_object_or_404, redirect
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
# @login_required
def all_members(request):
    return render(request, 'admin/members/add_members.html')

# Hàm dùng chung
def list_create_view(model, serializer_class, request):
    if request.method == 'GET':
        queryset = model.objects.all()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def retrieve_update_delete_view(model, serializer_class, request, pk):
    try:
        instance = model.objects.get(pk=pk)
    except model.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializer_class(instance)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = serializer_class(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            try:
                updated_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
def xoa_tai_khoan(request, MA_TK):
    try:
        TaiKhoan = TaiKhoan.objects.get(MA_TK=MA_TK)  # Tìm đặc sản theo MA_DS
        TaiKhoan.delete()  # Xóa đặc sản
        return admin_views.manage_members(request)
    except TaiKhoan.DoesNotExist:
        raise Http404("Tài khoản không tồn tại.") # Quay lại danh sách tài khoản
    


def them_sua_taikhoan(request, id=None):
    taikhoan = None
    if id:
        taikhoan = get_object_or_404(TaiKhoan, pk=id)
    
    if request.method == "POST":
        data = request.POST
        if taikhoan:  # Cập nhật tài khoản
            taikhoan.EMAIL_TK = data.get("EMAIL_TK")
            taikhoan.TEN_DANG_NHAP = data.get("TEN_DANG_NHAP")
            taikhoan.MAT_KHAU = data.get("MAT_KHAU")  # Mã hóa mật khẩu nếu cần
            taikhoan.VAI_TRO = data.get("VAI_TRO")
            taikhoan.TRANG_THAI_TK = data.get("TRANG_THAI_TK") == 'on'  # Chuyển trạng thái sang boolean
            taikhoan.NGAY_DANG_KY_TK = data.get("NGAY_DANG_KY_TK")
            taikhoan.MA_DN = data.get("MA_DN")
            taikhoan.save()
        else:  # Thêm mới tài khoản
            TaiKhoan.objects.create(
                EMAIL_TK=data.get("EMAIL_TK"),
                TEN_DANG_NHAP=data.get("TEN_DANG_NHAP"),
                MAT_KHAU=data.get("MAT_KHAU"),  # Mã hóa mật khẩu nếu cần
                VAI_TRO=data.get("VAI_TRO"),
                TRANG_THAI_TK=data.get("TRANG_THAI_TK") == 'on',  # Chuyển trạng thái sang boolean
                NGAY_DANG_KY_TK=data.get("NGAY_DANG_KY_TK"),
                MA_DN=data.get("MA_DN")
            )

        # Quay lại trang quản lý tài khoản sau khi thêm hoặc cập nhật
        return HttpResponseRedirect(reverse('admin_views.manage_taikhoan'))

    # Trả về form nếu không phải request POST (hiển thị form thêm/sửa tài khoản)
    return admin_views.manage_members(request)

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

        return admin_views.manage_members(request)

    return admin_views.manage_members(request)

def xoa_hiep_hoi(request, ma_hh):
    try:
        hiep_hoi = HiepHoi.objects.get(MA_HH=ma_hh)
        hiep_hoi.delete()  # Xóa hiệp hội
        return admin_views.manage_members(request)  # Quay lại trang quản lý hiệp hội
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

        return admin_views.manage_members(request)

    return admin_views.manage_members(request)



def xoa_nganhnghe(request, ma_nganh):
    try:
        nganh = NganhNghe.objects.get(MA_NGANH=ma_nganh)
        nganh.delete()
        return admin_views.manage_members(request)
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
        trang_thai_duyet = request.POST.get('TRANG_THAI_DUYET')  # Lấy trạng thái duyệt từ form
    # Kiểm tra giá trị nhận được từ form
        print(f"Trang thai duyet: {trang_thai_duyet}")  # In ra giá trị nhận được
        # Tạo chuỗi dữ liệu để sinh mã QR (có thể là tên, email, số điện thoại...)
        qr_data = f"{ten_doanhnghiep} - {email} - {sdt}"

        if doanhnghiep:
            # Sửa doanh nghiệp
            doanhnghiep.TEN_DN = ten_doanhnghiep
            doanhnghiep.NGUOI_DAI_DIEN = nguoi_dai_dien
            doanhnghiep.EMAIL_DN = email
            doanhnghiep.SDT_DN = sdt
            doanhnghiep.DIA_CHI = dia_chi
            doanhnghiep.MA_NGANH = NganhNghe.objects.get(MA_NGANH=ma_nganh)
            doanhnghiep.TRANG_THAI_DUYET = trang_thai_duyet  # Cập nhật trạng thái duyệt

            # Tạo mã QR mới khi sửa
            qr_code_image = generate_qr_code(qr_data)
            doanhnghiep.MA_QR.save(f"{ten_doanhnghiep}_qr.png", qr_code_image, save=True)

            doanhnghiep.save()
        else:
            # Thêm mới doanh nghiệp
            doanhnghiep = DoanhNghiep.objects.create(
                TEN_DN=ten_doanhnghiep,
                NGUOI_DAI_DIEN=nguoi_dai_dien,
                EMAIL_DN=email,
                SDT_DN=sdt,
                DIA_CHI=dia_chi,
                MA_NGANH=NganhNghe.objects.get(MA_NGANH=ma_nganh),
                TRANG_THAI_DUYET=trang_thai_duyet  # Cập nhật trạng thái duyệt khi thêm mới
            )

            # Tạo mã QR mới khi thêm
            qr_code_image = generate_qr_code(qr_data)
            doanhnghiep.MA_QR.save(f"{ten_doanhnghiep}_qr.png", qr_code_image, save=True)

        # Sau khi thêm hoặc sửa, chuyển đến trang quản lý doanh nghiệp
        return admin_views.manage_members(request)


    return admin_views.manage_members(request)
def xoa_doanhnghiep(request, ma_dn):
    try:
        doanhnghiep = DoanhNghiep.objects.get(MA_DN=ma_dn)
        doanhnghiep.delete()
        return admin_views.manage_members(request)  # hoặc redirect nếu muốn
    except DoanhNghiep.DoesNotExist:
        raise Http404("Doanh nghiệp không tồn tại.")  
    
def profile_doanhnghiep(request, ma_dn):
    dn = get_object_or_404(DoanhNghiep, pk=ma_dn)
    return render(request, 'admin/members/doanhnghiep/profile_doanhnghiep.html', {'dn': dn})

def xoa_dangkyhiephoi(request, ma_dk_hh):
    try:
        dangkihoivien = DangKyHoiVien.objects.get(MA_DK_HHH=ma_dk_hh)
        dangkihoivien.delete()
        return admin_views.manage_members(request)  # hoặc redirect nếu muốn
    except DangKyHoiVien.DoesNotExist:
        raise Http404(" hiệp hội đăng kí không tồn tại.")  
    
# Các API sử dụng lại
@api_view(['GET', 'POST'])
def tai_khoan_list(request):
    return list_create_view(TaiKhoan, TaiKhoanSerializer, request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def tai_khoan_detail(request, pk):
    return retrieve_update_delete_view(TaiKhoan, TaiKhoanSerializer, request, pk)

@api_view(['GET', 'POST'])
def doanh_nghiep_list(request):
    return list_create_view(DoanhNghiep, DoanhNghiepSerializer, request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def doanh_nghiep_detail(request, pk):
    return retrieve_update_delete_view(DoanhNghiep, DoanhNghiepSerializer, request, pk)

@api_view(['GET', 'POST'])
def nganh_nghe_list(request):
    return list_create_view(NganhNghe, NganhNgheSerializer, request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def nganh_nghe_detail(request, pk):
    return retrieve_update_delete_view(NganhNghe, NganhNgheSerializer, request, pk)

@api_view(['GET', 'POST'])
def hiephoi_list(request):
    return list_create_view(HiepHoi, HiepHoiSerializer, request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def hiephoi_detail(request, pk):
    return retrieve_update_delete_view(HiepHoi, HiepHoiSerializer, request, pk)

@api_view(['GET', 'POST'])
def dangky_list(request):
    return list_create_view(DangKyHoiVien, DangKyHoiVienSerializer, request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def dangky_detail(request, pk):
    return retrieve_update_delete_view(DangKyHoiVien, DangKyHoiVienSerializer, request, pk)






