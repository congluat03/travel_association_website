from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.uploadedfile import InMemoryUploadedFile
import qrcode
from io import BytesIO
import os
import sys
from PIL import Image
# Hàm tạo đường dẫn lưu hình ảnh tài khoản
def account_image_upload_path(instance, filename):
    # Lưu ảnh vào: taikhoan/<MA_TK>/<filename>
    return os.path.join('taikhoan', str(instance.MA_TK), filename)
class VaiTro(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    NHAN_VIEN = 'nhanvien', 'Nhân viên'
    NGUOI_DUNG = 'nguoidung', 'Người dùng'
class TaiKhoan(models.Model): 
    MA_TK = models.AutoField(primary_key=True)
    MA_DN = models.ForeignKey(
        'DoanhNghiep',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='MA_DN'
    )
    EMAIL_TK = models.EmailField(unique=True)
    TEN_DANG_NHAP = models.CharField(max_length=50, unique=True)
    MAT_KHAU = models.CharField(max_length=100)
    VAI_TRO = models.CharField(
        max_length=20,
        choices=VaiTro.choices,
        default=VaiTro.NGUOI_DUNG
    )
    TRANG_THAI_TK = models.BooleanField(default=True)
    NGAY_DANG_KY_TK = models.DateField(auto_now_add=True)
    HINH_TK = models.ImageField(upload_to=account_image_upload_path, blank=True, null=True)  # Hình đại diện tài khoản

    def set_mat_khau(self, password):
        self.MAT_KHAU = make_password(password)

    def check_mat_khau(self, password):
        return check_password(password, self.MAT_KHAU)

    def __str__(self):
        return self.TEN_DANG_NHAP

    class Meta:
        db_table = 'taikhoan'


class NganhNghe(models.Model):
    MA_NGANH = models.AutoField(primary_key=True)
    TEN_NGANH = models.CharField(max_length=255, null=True, blank=True)  # Có thể để rỗng

    def __str__(self):
        return self.TEN_NGANH

    class Meta:
        db_table = 'nganhnghe'

class DoanhNghiep(models.Model):
    MA_DN = models.AutoField(primary_key=True)
    MA_NGANH = models.ForeignKey(
        NganhNghe, 
        on_delete=models.CASCADE, 
        related_name="doanh_nghieps", 
        db_column='ma_nganh'
    )
    TEN_DN = models.CharField(max_length=255)
    DIA_CHI = models.TextField(blank=True)
    SDT_DN = models.CharField(max_length=20, null=True, blank=True)
    EMAIL_DN = models.EmailField(null=True, blank=True)
    MA_QR = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    NGUOI_DAI_DIEN = models.CharField(max_length=255, null=True, blank=True)
    TRANG_THAI_DUYET = models.IntegerField(
        choices=[(0, 'Chưa Duyệt'), (1, 'Duyệt')], 
        default=0
    )
    
    def __str__(self):
        return self.TEN_DN

    def save(self, *args, **kwargs):
        # Sử dụng địa chỉ IP thay cho localhost (127.0.0.1)
        ip_address = '192.168.0.102'  # Thay thế địa chỉ IP của máy tính của bạn tại đây
        url = f"http://{ip_address}:8000/members/hoivien/{self.MA_DN}/"
        
        # Khởi tạo QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Tạo hình ảnh QR Code
        img = qr.make_image(fill="black", back_color="white")

        # Lưu vào bộ nhớ tạm
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Đặt tên file QR Code
        file_name = f"{self.MA_DN}_qr.png"

        # Tạo file InMemoryUploadedFile để lưu vào ImageField
        self.MA_QR = InMemoryUploadedFile(
            buffer,
            None,
            file_name,
            'image/png',
            sys.getsizeof(buffer),
            None
        )

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'doanhnghiep'



class HiepHoi(models.Model):
    MA_HH = models.AutoField(primary_key=True)
    TEN_HH = models.CharField(max_length=255, null=True, blank=True)  # Có thể để rỗng
    MO_TA_HH = models.TextField(blank=True)  # Có thể để rỗng

    def __str__(self):
        return self.TEN_HH

    class Meta:
        db_table = 'hiephoi'

class DangKyHoiVien(models.Model):
    MA_DK_HH = models.AutoField(primary_key=True)  # Khóa chính riêng
    MA_HH = models.ForeignKey(
        'HiepHoi', 
        on_delete=models.CASCADE, 
        related_name="dang_ky_hv",
        db_column='MA_HH'
    )
    MA_DN = models.ForeignKey(
        'DoanhNghiep', 
        on_delete=models.CASCADE, 
        related_name="dang_ky_hv",
        db_column='MA_DN'
    )
    # Trường trạng thái duyệt
    TINH_TRANG = models.IntegerField(
        choices=[(0, 'Chưa Duyệt'), (1, 'Duyệt')],  # Sử dụng số 0 và 1
        default=0  # Mặc định là Chưa Duyệt (0)
    )
    NGAY_DANG_KY = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Đăng ký hội viên: {self.MA_DK_HH} - {self.MA_DN.TEN_DN}"

    class Meta:
        db_table = 'dangkyhoivien'
