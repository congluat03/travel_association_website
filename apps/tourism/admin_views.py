from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DiaDiemDuLich, DacSan, TourDuLich, ThuocTour
from .serializers import DiaDiemDuLichSerializer, DacSanSerializer, TourDuLichSerializer, ThuocTourSerializer

# Generic functions
def get_object_or_404(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None

def handle_get_list(model, serializer_class):
    data = model.objects.all()
    serializer = serializer_class(data, many=True)
    return Response(serializer.data)

def handle_post_create(model, serializer_class, request):
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def handle_put_update(obj, serializer_class, request):
    serializer = serializer_class(obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def handle_patch_update(obj, serializer_class, request):
    # Xử lý với PATCH: Cập nhật một phần
    serializer = serializer_class(obj, data=request.data, partial=True)  # partial=True để cập nhật một phần
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def handle_delete(obj):
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Tạo view list_create_view cho GET và POST
def list_create_view(request, model, serializer_class):
    if request.method == 'GET':
        return handle_get_list(model, serializer_class)
    elif request.method == 'POST':
        return handle_post_create(model, serializer_class, request)

# Tạo view retrieve_update_delete_view cho GET, PUT, PATCH và DELETE
def retrieve_update_delete_view(request, pk, model, serializer_class):
    obj = get_object_or_404(model, pk)
    if not obj:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializer_class(obj)
        return Response(serializer.data)
    elif request.method == 'PUT':
        return handle_put_update(obj, serializer_class, request)
    elif request.method == 'PATCH':
        return handle_patch_update(obj, serializer_class, request)  # Thêm xử lý PATCH
    elif request.method == 'DELETE':
        return handle_delete(obj)

# DiaDiemDuLich
@api_view(['GET', 'POST'])
def diadiemdulich_list(request):
    return list_create_view(request, DiaDiemDuLich, DiaDiemDuLichSerializer)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])  # Thêm PATCH vào đây
def diadiemdulich_detail(request, pk):
    return retrieve_update_delete_view(request, pk, DiaDiemDuLich, DiaDiemDuLichSerializer)

# DacSan
@api_view(['GET', 'POST'])
def dacsan_list(request):
    return list_create_view(request, DacSan, DacSanSerializer)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])  # Thêm PATCH vào đây
def dacsan_detail(request, pk):
    return retrieve_update_delete_view(request, pk, DacSan, DacSanSerializer)

# TourDuLich
@api_view(['GET', 'POST'])
def tourdulich_list(request):
    return list_create_view(request, TourDuLich, TourDuLichSerializer)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])  # Thêm PATCH vào đây
def tourdulich_detail(request, pk):
    return retrieve_update_delete_view(request, pk, TourDuLich, TourDuLichSerializer)

# ThuocTour
@api_view(['GET', 'POST'])
def thuoctour_list(request):
    return list_create_view(request, ThuocTour, ThuocTourSerializer)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])  # Thêm PATCH vào đây
def thuoctour_detail(request, pk):
    return retrieve_update_delete_view(request, pk, ThuocTour, ThuocTourSerializer)
