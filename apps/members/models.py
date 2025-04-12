from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class TaiKhoan(models.Model):
    MA_TK = models.AutoField(primary_key=True)
    MA_DN = models.CharField(max_length=50, null=True, blank=True)  # Có thể để rỗng
    EMAIL_TK = models.EmailField(unique=True)
    TEN_DANG_NHAP = models.CharField(max_length=50, unique=True)
    MAT_KHAU = models.CharField(max_length=100)  # Nên mã hóa mật khẩu
    VAI_TRO = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('user', 'User')])
    TRANG_THAI_TK = models.BooleanField(default=True)
    NGAY_DANG_KY_TK = models.DateField(auto_now_add=True)  # Sử dụng DateTimeField

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
        db_column='ma_nganh'  # Tên cột tùy chỉnh trong cơ sở dữ liệu
    )
    TEN_DN = models.CharField(max_length=255)
    DIA_CHI = models.TextField(blank=True)  # Có thể để rỗng
    SDT_DN = models.CharField(max_length=20, null=True, blank=True)  # Có thể để rỗng
    EMAIL_DN = models.EmailField(null=True, blank=True)  # Có thể để rỗng
    MA_QR = models.CharField(max_length=100, blank=True)  # Có thể để rỗng
    NGUOI_DAI_DIEN = models.CharField(max_length=255, null=True, blank=True)  # Có thể để rỗng
    TRANG_THAI_DUYET = models.BooleanField(default=False)

    def __str__(self):
        return self.TEN_DN

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
        HiepHoi, 
        on_delete=models.CASCADE, 
        related_name="dang_ky_hv",
        db_column='MA_HH'
    )
    MA_DN = models.ForeignKey(
        DoanhNghiep, 
        on_delete=models.CASCADE, 
        related_name="dang_ky_hv",
        db_column='MA_DN'
    )
    TINH_TRANG = models.CharField(max_length=100, null=True, blank=True)
    NGAY_DANG_KY = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'dangkyhoivien'