from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.uploadedfile import InMemoryUploadedFile
import qrcode
from io import BytesIO
class TaiKhoan(models.Model):
    MA_TK = models.AutoField(primary_key=True)
    MA_DN = models.ForeignKey(
        'DoanhNghiep',  # Sử dụng chuỗi thay vì tham chiếu trực tiếp
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='MA_DN'  # Đặt tên cột trong DB nếu cần khớp với dữ liệu cũ
    )
    EMAIL_TK = models.EmailField(unique=True)
    TEN_DANG_NHAP = models.CharField(max_length=50, unique=True)
    MAT_KHAU = models.CharField(max_length=100)  # Nên mã hóa mật khẩu
    VAI_TRO = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('user', 'User')])
    TRANG_THAI_TK = models.BooleanField(default=True)  # Đảm bảo kiểu BooleanField
    NGAY_DANG_KY_TK = models.DateField(auto_now_add=True)

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
    
    # Thay đổi kiểu TRANG_THAI_DUYET sang IntegerField
    TRANG_THAI_DUYET = models.IntegerField(
        choices=[(0, 'Chưa Duyệt'), (1, 'Duyệt')],  # Sử dụng số 0 và 1
        default=0  # Mặc định là Chưa Duyệt (0)
    )

    def __str__(self):
        return self.TEN_DN

    def save(self, *args, **kwargs):
        # Tạo mã QR tự động khi tạo hoặc cập nhật doanh nghiệp
        if not self.MA_QR:
            url = f"http://127.0.0.1:8000/profile/{self.MA_DN}/"  # hoặc dùng reverse nếu trong Django
            qr_code = qrcode.make(url)
            buffer = BytesIO()
            qr_code.save(buffer, format="PNG")
            buffer.seek(0)
            self.MA_QR = InMemoryUploadedFile(
                buffer, None, f"{self.MA_DN}_qr.png", 'image/png', buffer.tell(), None
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

from django.db import models

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
