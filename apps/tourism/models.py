from django.db import models

# Create your models here.
# models.py
from django.db import models

class DiaDiemDuLich(models.Model):
    MA_DD = models.AutoField(primary_key=True)
    MA_DN = models.ForeignKey(
        'members.DoanhNghiep', 
        on_delete=models.CASCADE,
        db_column='MA_DN'  # Tên cột tùy chỉnh
    )
    TEN_DIA_DIEM = models.CharField(max_length=255)
    MO_TA_DD = models.TextField()
    VI_TRI = models.CharField(max_length=255)
    HINH_ANH_DD = models.URLField(blank=True, null=True)
    TINH_THANH_PHO = models.CharField(max_length=100)
    QUAN_HUYEN = models.CharField(max_length=100)
    KHU_VUC = models.CharField(max_length=100)

    class Meta:
        db_table = 'diadiemdulich'

    def get_full_address(self):
        return f"{self.KHU_VUC}, {self.QUAN_HUYEN}, {self.TINH_THANH_PHO}"

    def get_google_map_url(self):
        # Tạo URL Google Maps từ các thông tin địa chỉ
        address = f"{self.KHU_VUC}, {self.QUAN_HUYEN}, {self.TINH_THANH_PHO}"
        return f"https://www.google.com/maps?q={address.replace(' ', '+')}"


class DacSan(models.Model):
    MA_DS = models.AutoField(primary_key=True)
    MA_DD = models.ForeignKey(DiaDiemDuLich, on_delete=models.CASCADE, db_column='MA_DD')
    TEN_DAC_SAN = models.CharField(max_length=255)
    MO_TA_DS = models.TextField()
    HINH_DS = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'dacsan'

class TourDuLich(models.Model):
    MA_TOUR = models.AutoField(primary_key=True)
    TEN_TOUR = models.CharField(max_length=255)
    MO_TA_TOUR = models.TextField()
    GIA_TOUR = models.DecimalField(max_digits=12, decimal_places=2)
    HINH_TOUR = models.URLField(blank=True, null=True)
    THOI_GIAN_DI_CHUYEN = models.CharField(max_length=100)

    class Meta:
        db_table = 'tourdulich'


class ThuocTour(models.Model):
    MA_TUOCTOUR = models.AutoField(primary_key=True)
    MA_DD = models.ForeignKey('DiaDiemDuLich', on_delete=models.CASCADE, db_column='MA_DD')
    MA_TOUR = models.ForeignKey('TourDuLich', on_delete=models.CASCADE, db_column='MA_TOUR')
    THU_THU = models.PositiveSmallIntegerField()  # Nếu là số ngày trong tuần từ 0 đến 6
    THOI_GIAN_DI = models.DateTimeField()  # Nếu cần cả ngày và giờ
    THOI_GIAN_DEN = models.DateTimeField()  # Nếu cần cả ngày và giờ

    class Meta:
        db_table = 'thuoctour'
        constraints = [
            models.UniqueConstraint(fields=['MA_DD', 'MA_TOUR'], name='unique_ma_dd_ma_tour')  # Thay thế unique_together
        ]

    def __str__(self):
        return f"Tour {self.MA_TOUR} tại {self.MA_DD}"

