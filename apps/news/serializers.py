from rest_framework import serializers
from .models import TheTag, CoTheTag, TinTuc, TrackingXemTin
from django.db.models import Max


class TheTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheTag
        fields = '__all__'

class CoTheTagSerializer(serializers.ModelSerializer):
    # Sử dụng `MA_TIN` và `MA_TAG` dưới dạng các đối tượng thay vì chỉ khóa ngoại
    MA_TIN = serializers.PrimaryKeyRelatedField(queryset=TinTuc.objects.all(), required=False)
    MA_TAG = serializers.PrimaryKeyRelatedField(queryset=TheTag.objects.all(), required=False)

    class Meta:
        model = CoTheTag
        fields = '__all__'
        extra_kwargs = {
            'MA_TIN': {'required': False},  # Nếu không bắt buộc, bạn có thể để trường này không yêu cầu
            'MA_TAG': {'required': False}   # Tương tự cho MA_TAG
        }
class TinTucSerializer(serializers.ModelSerializer):

    class Meta:
        model = TinTuc
        fields = '__all__'



class TrackingXemTinSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingXemTin
        fields = '__all__'
