from rest_framework import serializers
from .models import TaiLieu

class TaiLieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaiLieu
        fields = '__all__'
