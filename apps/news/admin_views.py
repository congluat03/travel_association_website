from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import TinTuc, TheTag, TrackingXemTin, CoTheTag
from .serializers import TinTucSerializer, TheTagSerializer, TrackingXemTinSerializer


def handle_list_create(request, model, serializer_class, related_model=None, relation_field=None):
    if request.method == 'GET':
        queryset = model.objects.all()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            if related_model and relation_field:
                # Xử lý các mối quan hệ many-to-many nếu có
                related_data = request.data.get(relation_field, [])
                for related_id in related_data:
                    # Truy vấn theo MA_TAG, không phải id
                    related_instance = related_model.objects.filter(MA_TAG=related_id).first()
                    if related_instance:
                        # Kiểm tra nếu cặp MA_TIN và MA_TAG đã tồn tại trong bảng CoTheTag
                        if not CoTheTag.objects.filter(MA_TIN=instance, MA_TAG=related_instance).exists():
                            CoTheTag.objects.create(MA_TIN=instance, MA_TAG=related_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def handle_detail(request, pk, model, serializer_class, related_model=None, relation_field=None):
    instance = get_object_or_404(model, pk=pk)

    if request.method == 'GET':
        serializer = serializer_class(instance)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = serializer_class(instance, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            instance = serializer.save()
            if related_model and relation_field:
                # Xử lý mối quan hệ many-to-many
                if relation_field in request.data:
                    # Xóa các mối quan hệ cũ trước khi thêm mối quan hệ mới
                    CoTheTag.objects.filter(MA_TIN=instance).delete()  # Đảm bảo sử dụng MA_TIN cho truy vấn
                    related_data = request.data[relation_field]
                    for related_id in related_data:
                        related_instance = related_model.objects.filter(MA_TAG=related_id).first()  # Truy vấn theo MA_TAG
                        if related_instance:
                            # Kiểm tra nếu cặp MA_TIN và MA_TAG đã tồn tại trong bảng CoTheTag
                            if not CoTheTag.objects.filter(MA_TIN=instance, MA_TAG=related_instance).exists():
                                CoTheTag.objects.create(MA_TIN=instance, MA_TAG=related_instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- TinTuc --- 
@api_view(['GET', 'POST'])
def tintuc_list(request):
    return handle_list_create(request, TinTuc, TinTucSerializer, TheTag, 'MA_TAG')


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def tintuc_detail(request, pk):
    return handle_detail(request, pk, TinTuc, TinTucSerializer, TheTag, 'MA_TAG')


# --- TheTag --- 
@api_view(['GET', 'POST'])
def thetag_list(request):
    return handle_list_create(request, TheTag, TheTagSerializer)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def thetag_detail(request, pk):
    return handle_detail(request, pk, TheTag, TheTagSerializer)


# --- TrackingXemTin --- 
@api_view(['GET', 'POST'])
def trackingxemtin_list(request):
    return handle_list_create(request, TrackingXemTin, TrackingXemTinSerializer)

@api_view(['GET', 'PUT', 'DELETE'])
def trackingxemtin_detail(request, pk):
    return handle_detail(request, pk, TrackingXemTin, TrackingXemTinSerializer)
