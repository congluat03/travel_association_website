# apps/members/serializers.py

from rest_framework import serializers
from .models import TaiKhoan, DoanhNghiep, NganhNghe, HiepHoi, DangKyHoiVien

class TaiKhoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaiKhoan
        fields = '__all__'
class NganhNgheSerializer(serializers.ModelSerializer):
    class Meta:
        model = NganhNghe
        fields = ['MA_NGANH', 'TEN_NGANH']

class DoanhNghiepSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoanhNghiep
        fields = '__all__'
class HiepHoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiepHoi
        fields = '__all__'

class DangKyHoiVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = DangKyHoiVien
        fields = '__all__'