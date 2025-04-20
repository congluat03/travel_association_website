from django.db import models

class TheTag(models.Model):
    MA_TAG = models.AutoField(primary_key=True)
    TEN_TAG = models.CharField(max_length=255)
    MO_TA_TAG = models.TextField(blank=True, null=True)  # Thêm trường mô tả thẻ tag

    def __str__(self):
        return self.TEN_TAG

    class Meta:
        db_table = 'thetag'

class TinTuc(models.Model):
    MA_TIN = models.AutoField(primary_key=True)
    MA_TK = models.ForeignKey(
        'members.TaiKhoan',
        on_delete=models.CASCADE,
        db_column='MA_TK',
        related_name='tintucs'  # giúp truy cập từ TaiKhoan.tintuces dễ hơn
    )
    TIEU_DE = models.CharField(max_length=255)
    NOI_DUNG_CHI_TIET = models.TextField()
    NGAY_DANG = models.DateField()
    LOAI_TIN_TUC = models.CharField(max_length=100)
    TIN_NOI_BAT = models.BooleanField(default=False)
    URL_HINH = models.URLField(blank=True, null=True)
    SO_LUOT_XEM = models.IntegerField(default=0)
    MA_TAG = models.ManyToManyField('TheTag', through='CoTheTag', related_name='tintucs')

    def __str__(self):
        return self.TIEU_DE

    class Meta:
        db_table = 'tintuc'


class CoTheTag(models.Model):
    MA_COTHETAP = models.AutoField(primary_key=True)  # Đánh dấu là khóa chính và tự động tăng
    MA_TIN = models.ForeignKey(
        TinTuc, on_delete=models.CASCADE, db_column='MA_TIN'
    )
    MA_TAG = models.ForeignKey(
        TheTag, on_delete=models.CASCADE, db_column='MA_TAG'
    )

    class Meta:
        unique_together = ('MA_TIN', 'MA_TAG')  # Đảm bảo sự kết hợp MA_TIN và MA_TAG là duy nhất
        db_table = 'cothetag'

    def __str__(self):
        return f"{self.MA_TIN} - {self.MA_TAG}"
class TrackingXemTin(models.Model):
    ID_TRACKING = models.AutoField(primary_key=True)
    MA_TK = models.ForeignKey(
        'members.TaiKhoan', on_delete=models.CASCADE, db_column='MA_TK'
    )
    MA_TIN = models.ForeignKey(
        'TinTuc', on_delete=models.CASCADE, db_column='MA_TIN'
    )
    THOI_GIAN_XEM = models.DateTimeField()
    TONG_THOI_GIAN_XEM = models.CharField(max_length=50, null=True, blank=True)  # varchar

    def __str__(self):
        return f"Tracking #{self.ID_TRACKING} - {self.MA_TK} - {self.MA_TIN}"

    class Meta:
        db_table = 'trackingxemtin'
