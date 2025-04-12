from django.db import models

# Create your models here.
class TaiLieu(models.Model):
    MA_TL = models.AutoField(primary_key=True)
    MA_DN = models.ForeignKey(
        'members.DoanhNghiep', 
        on_delete=models.CASCADE,
        db_column='MA_DN'  # Tên cột tùy chỉnh cho mối quan hệ DoanhNghiep
    )
    TIEU_DE_TL = models.CharField(max_length=255)
    MO_TA_TL = models.TextField()
    DUONG_DAN_FILE = models.URLField()
    LOAI_TAI_LIEU = models.CharField(max_length=100)
    NGAY_CAP_NHAT = models.DateField()

    def __str__(self):
        return self.TIEU_DE_TL

    class Meta:
        db_table = 'tailieu'
