from rest_framework import serializers
from .models import DiaDiemDuLich, DacSan, TourDuLich, ThuocTour

class DiaDiemDuLichSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaDiemDuLich
        fields = '__all__'

class DacSanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DacSan
        fields = '__all__'

class TourDuLichSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDuLich
        fields = '__all__'

class ThuocTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThuocTour
        fields = '__all__'
