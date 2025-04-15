from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DiaDiemDuLich, DacSan, TourDuLich, ThuocTour
from .serializers import DiaDiemDuLichSerializer, DacSanSerializer, TourDuLichSerializer, ThuocTourSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from apps.members.models import DoanhNghiep
from apps.core import admin_views
from django.http import Http404
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



def dia_diem_form(request, id=None):
    dia_diem = None
    if id:
        dia_diem = get_object_or_404(DiaDiemDuLich, pk=id)
    if request.method == "POST":
        data = request.POST
        if dia_diem:  # cập nhật
            dia_diem.TEN_DIA_DIEM = data.get("TEN_DIA_DIEM")
            dia_diem.MA_DN_id = data.get("MA_DN")
            dia_diem.TINH_THANH_PHO = data.get("TINH_THANH_PHO")
            dia_diem.QUAN_HUYEN = data.get("QUAN_HUYEN")
            dia_diem.KHU_VUC = data.get("KHU_VUC")
            dia_diem.HINH_ANH_DD = data.get("HINH_ANH_DD")
            dia_diem.VI_TRI = data.get("VI_TRI")
            dia_diem.MO_TA_DD = data.get("MO_TA_DD")
            dia_diem.save()
        else:  # thêm mới
            DiaDiemDuLich.objects.create(
                TEN_DIA_DIEM=data.get("TEN_DIA_DIEM"),
                MA_DN_id=data.get("MA_DN"),
                TINH_THANH_PHO=data.get("TINH_THANH_PHO"),
                QUAN_HUYEN=data.get("QUAN_HUYEN"),
                KHU_VUC=data.get("KHU_VUC"),
                HINH_ANH_DD=data.get("HINH_ANH_DD"),
                VI_TRI=data.get("VI_TRI"),
                MO_TA_DD=data.get("MO_TA_DD")
            )

    return admin_views.manage_tourism(request)
def xoa_dia_diem(request, ma_dd):
    try:
        dia_diem = DiaDiemDuLich.objects.get(MA_DD=ma_dd)
        dia_diem.delete()  # Xóa địa điểm
        return admin_views.manage_tourism(request) # Quay lại trang quản lý địa điểm
    except DiaDiemDuLich.DoesNotExist:
        raise Http404("Địa điểm không tồn tại.")
    
def them_sua_dacsan(request, id=None):
    dacsan = DacSan.objects.filter(pk=id).first() if id else None

    if request.method == 'POST':
        ten_ds = request.POST.get('TEN_DS')
        ma_dd = request.POST.get('MA_DD')
        hinh_anh = request.POST.get('HINH_DS')
        mo_ta = request.POST.get('MO_TA_DS')

        if dacsan:
            # Sửa
            dacsan.TEN_DAC_SAN = ten_ds
            dacsan.MA_DD_id = ma_dd
            dacsan.HINH__DS = hinh_anh
            dacsan.MO_TA_DS = mo_ta
            dacsan.save()
        else:
            # Thêm
            DacSan.objects.create(
                TEN_DAC_SAN=ten_ds,
                MA_DD_id=ma_dd,
                HINH_DS=hinh_anh,
                MO_TA_DS=mo_ta
            )
        return admin_views.manage_tourism(request)

    return admin_views.manage_tourism(request)
def xoa_dac_san(request, ma_ds):
    try:
        dac_san = DacSan.objects.get(MA_DS=ma_ds)  # Tìm đặc sản theo MA_DS
        dac_san.delete()  # Xóa đặc sản
        return admin_views.manage_tourism(request)
    except DacSan.DoesNotExist:
        raise Http404("Đặc sản không tồn tại.")

def them_sua_tour(request, ma_tour=None):
    tour = TourDuLich.objects.filter(pk=ma_tour).first() if id else None

    if request.method == 'POST':
        ten_tour = request.POST.get('TEN_TOUR')
        hinh_tour = request.POST.get('HINH_TOUR')
        mo_ta = request.POST.get('MO_TA_TOUR')
        gia = request.POST.get('GIA_TOUR')
        thoi_gian = request.POST.get('THOI_GIAN_DI_CHUYEN')

        if tour:
            # Sửa tour
            tour.TEN_TOUR = ten_tour
            tour.HINH_TOUR = hinh_tour
            tour.MO_TA_TOUR = mo_ta
            tour.GIA_TOUR = gia
            tour.THOI_GIAN_DI_CHUYEN = thoi_gian
            tour.save()
        else:
            # Thêm mới tour
            TourDuLich.objects.create(
                TEN_TOUR=ten_tour,
                HINH_TOUR=hinh_tour,
                MO_TA_TOUR=mo_ta,
                GIA_TOUR=gia,
                THOI_GIAN_DI_CHUYEN=thoi_gian
            )

        return admin_views.manage_tourism(request)

    return admin_views.manage_tourism(request)

def xoa_tour(request, ma_tour):
    try:
        tour = TourDuLich.objects.get(MA_TOUR=ma_tour)
        tour.delete()
        return admin_views.manage_tourism(request)
    except TourDuLich.DoesNotExist:
        raise Http404("Tour không tồn tại.")
def them_sua_lich_trinh(request, ma_tour=None, ma_lich_trinh=None):
    tour = TourDuLich.objects.filter(MA_TOUR=ma_tour).first()

    if request.method == 'POST':
        ma_dd = request.POST.get('MA_DD')
        thu_thu = request.POST.get('THU_THU')
        thoi_gian_di = request.POST.get('THOI_GIAN_DI')
        thoi_gian_den = request.POST.get('THOI_GIAN_DEN')

        if tour:
            try:
                dia_diem = DiaDiemDuLich.objects.get(MA_DD=ma_dd)
                if ma_lich_trinh:
                    # Sửa lịch trình
                    thuoc_tour = ThuocTour.objects.get(MA_TOUR=tour, MA_LICH_TRINH=ma_lich_trinh)
                    thuoc_tour.THU_THU = thu_thu
                    thuoc_tour.THOI_GIAN_DI = thoi_gian_di
                    thuoc_tour.THOI_GIAN_DEN = thoi_gian_den
                    thuoc_tour.save()
                else:
                    # Thêm mới lịch trình
                    ThuocTour.objects.create(
                        MA_TOUR=tour,
                        MA_DD=dia_diem,
                        THU_THU=thu_thu,
                        THOI_GIAN_DI=thoi_gian_di,
                        THOI_GIAN_DEN=thoi_gian_den
                    )
            except DiaDiemDuLich.DoesNotExist:
                raise Http404("Địa điểm không tồn tại.")
        else:
            raise Http404("Tour không tồn tại.")

        return admin_views.manage_tourism(request)

    return admin_views.manage_tourism(request)
def xoa_lich_trinh(request, ma_tour, ma_lich_trinh):
    try:
        # Lấy tour theo mã
        tour = TourDuLich.objects.get(MA_TOUR=ma_tour)
        
        # Lấy lịch trình theo mã
        thuoc_tour = ThuocTour.objects.get(MA_TOUR=tour, MA_DD=ma_lich_trinh)
        
        # Xóa lịch trình
        thuoc_tour.delete()

        # Sau khi xóa, chuyển hướng về trang quản lý lịch trình của tour
        return admin_views.manage_tourism(request)

    except TourDuLich.DoesNotExist:
        raise Http404("Tour không tồn tại.")
    except ThuocTour.DoesNotExist:
        raise Http404("Lịch trình không tồn tại.")