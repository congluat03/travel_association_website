from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TaiKhoan, DoanhNghiep, NganhNghe, HiepHoi, DangKyHoiVien
from .serializers import TaiKhoanSerializer, DoanhNghiepSerializer, NganhNgheSerializer, HiepHoiSerializer, DangKyHoiVienSerializer

# Hàm dùng chung
def list_create_view(model, serializer_class, request):
    if request.method == 'GET':
        queryset = model.objects.all()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def retrieve_update_delete_view(model, serializer_class, request, pk):
    try:
        instance = model.objects.get(pk=pk)
    except model.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializer_class(instance)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = serializer_class(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            try:
                updated_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Các API sử dụng lại
@api_view(['GET', 'POST'])
def tai_khoan_list(request):
    return list_create_view(TaiKhoan, TaiKhoanSerializer, request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def tai_khoan_detail(request, pk):
    return retrieve_update_delete_view(TaiKhoan, TaiKhoanSerializer, request, pk)

@api_view(['GET', 'POST'])
def doanh_nghiep_list(request):
    return list_create_view(DoanhNghiep, DoanhNghiepSerializer, request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def doanh_nghiep_detail(request, pk):
    return retrieve_update_delete_view(DoanhNghiep, DoanhNghiepSerializer, request, pk)

@api_view(['GET', 'POST'])
def nganh_nghe_list(request):
    return list_create_view(NganhNghe, NganhNgheSerializer, request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def nganh_nghe_detail(request, pk):
    return retrieve_update_delete_view(NganhNghe, NganhNgheSerializer, request, pk)

@api_view(['GET', 'POST'])
def hiephoi_list(request):
    return list_create_view(HiepHoi, HiepHoiSerializer, request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def hiephoi_detail(request, pk):
    return retrieve_update_delete_view(HiepHoi, HiepHoiSerializer, request, pk)

@api_view(['GET', 'POST'])
def dangky_list(request):
    return list_create_view(DangKyHoiVien, DangKyHoiVienSerializer, request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def dangky_detail(request, pk):
    return retrieve_update_delete_view(DangKyHoiVien, DangKyHoiVienSerializer, request, pk)
