from django.db import models
import os
# Create your models here.
def tailieu_file_upload_path(instance, filename):
    # Lưu file vào: tailieu/<MA_TL>/<filename>
    return os.path.join('tailieu', str(instance.MA_TL or 'temp'), filename)
class TaiLieu(models.Model):
    MA_TL = models.AutoField(primary_key=True)
    MA_DN = models.ForeignKey(
        'members.DoanhNghiep',
        on_delete=models.CASCADE,
        db_column='MA_DN'
    )
    TIEU_DE_TL = models.CharField(max_length=255)
    MO_TA_TL = models.TextField()
    # Thay đổi từ URLField → FileField để lưu trữ nội bộ
    DUONG_DAN_FILE = models.FileField(upload_to=tailieu_file_upload_path, blank=True, null=True)
    LOAI_TAI_LIEU = models.CharField(max_length=100)
    NGAY_CAP_NHAT = models.DateField()

    def __str__(self):
        return self.TIEU_DE_TL

    class Meta:
        db_table = 'tailieu'
