from django.db import models

# Create your models here.
class LopHoc(models.Model):
    MALOPHOC = models.CharField(max_length=20, unique=True)  # Mã lớp học, đảm bảo không trùng
    TENLOP = models.CharField(max_length=200)  # Tên lớp học
    MONHOC = models.CharField(max_length=100)  # Môn học
    SOLUONGHOCVIEN = models.IntegerField()  # Số lượng học viên

    def __str__(self):
        return f"{self.TENLOP} - {self.MONHOC}"