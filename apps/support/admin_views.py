from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TaiLieu
from .serializers import TaiLieuSerializer
from apps.core import admin_views

# ====== HÀM CHỨC NĂNG ======

def get_all_tailieu():
    queryset = TaiLieu.objects.all()
    return TaiLieuSerializer(queryset, many=True)

def create_tailieu(data):
    serializer = TaiLieuSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_tailieu_by_pk(pk):
    try:
        return TaiLieu.objects.get(pk=pk)
    except TaiLieu.DoesNotExist:
        return None

def update_tailieu(instance, data):
    serializer = TaiLieuSerializer(instance, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_tailieu(instance):
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ====== VIEW CHÍNH ======

@api_view(['GET', 'POST'])
def tailieu_list(request):
    if request.method == 'GET':
        serializer = get_all_tailieu()
        return Response(serializer.data)
    elif request.method == 'POST':
        return create_tailieu(request.data)

@api_view(['GET', 'PUT', 'DELETE'])
def tailieu_detail(request, pk):
    tailieu = get_tailieu_by_pk(pk)
    if not tailieu:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaiLieuSerializer(tailieu)
        return Response(serializer.data)
    elif request.method == 'PUT':
        return update_tailieu(tailieu, request.data)
    elif request.method == 'DELETE':
        return delete_tailieu(tailieu)
def them_sua_tailieu(request, ma_tl=None):
    # Nếu ma_tl tồn tại => Sửa, ngược lại là Thêm mới
    tailieu = TaiLieu.objects.filter(pk=ma_tl).first() if ma_tl else None

    if request.method == 'POST':
        tieu_de = request.POST.get('TIEU_DE_TL')
        mo_ta = request.POST.get('MO_TA_TL')
        duong_dan = request.POST.get('DUONG_DAN_FILE')
        loai = request.POST.get('LOAI_TAI_LIEU')
        ngay = request.POST.get('NGAY_CAP_NHAT')
        ma_dn = request.POST.get('MA_DN')

        if tailieu:
            # Sửa tài liệu
            tailieu.TIEU_DE_TL = tieu_de
            tailieu.MO_TA_TL = mo_ta
            tailieu.DUONG_DAN_FILE = duong_dan
            tailieu.LOAI_TAI_LIEU = loai
            tailieu.NGAY_CAP_NHAT = ngay
            tailieu.MA_DN_id = ma_dn
            tailieu.save()
        else:
            # Thêm mới tài liệu
            TaiLieu.objects.create(
                TIEU_DE_TL=tieu_de,
                MO_TA_TL=mo_ta,
                DUONG_DAN_FILE=duong_dan,
                LOAI_TAI_LIEU=loai,
                NGAY_CAP_NHAT=ngay,
                MA_DN_id=ma_dn
            )

        # Quay về trang quản lý tin tức hoặc tài liệu
        return admin_views.manage_support(request)

    # Nếu không phải POST thì trả về trang (tùy bạn định nghĩa lại giao diện)
    return admin_views.manage_support(request)
def xoa_tailieu(request, ma_tl):
    try:
        # Tìm tài liệu theo MA_TL
        tailieu = TaiLieu.objects.get(MA_TL=ma_tl)
        # Xóa tài liệu
        tailieu.delete()  # Django sẽ tự động xử lý các bản ghi liên quan nếu bạn đã sử dụng on_delete trong model
        return admin_views.manage_support(request)  # Điều hướng về trang danh sách tài liệu sau khi xóa
    except TaiLieu.DoesNotExist:
        raise Http404("Tài liệu không tồn tại.")