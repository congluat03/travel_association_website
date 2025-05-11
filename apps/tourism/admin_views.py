
import shutil
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DiaDiemDuLich, DacSan, TourDuLich, ThuocTour
from .serializers import DiaDiemDuLichSerializer, DacSanSerializer, TourDuLichSerializer, ThuocTourSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from apps.members.models import DoanhNghiep
from apps.core import admin_views
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib import messages
import os
from django.conf import settings
from django.core.files.storage import default_storage
# Generic functions
def them_sua_diadiem(request, id=None):
    dia_diem = None
    if id:
        dia_diem = get_object_or_404(DiaDiemDuLich, pk=id)

    if request.method == "POST":
        data = request.POST
        hinh_anh_files = request.FILES.getlist('HINH_ANH_DD[]')
        deleted_images = request.POST.get('DELETED_IMAGES_DD', '').split(',')
        deleted_images = [img.strip() for img in deleted_images if img.strip()]
        # ===== CẬP NHẬT =====
        if dia_diem:
            dia_diem.TEN_DIA_DIEM = data.get("TEN_DIA_DIEM")
            dia_diem.MA_DN_id = data.get("MA_DN")
            dia_diem.TINH_THANH_PHO = data.get("TINH_THANH_PHO")
            dia_diem.QUAN_HUYEN = data.get("QUAN_HUYEN")
            dia_diem.KHU_VUC = data.get("KHU_VUC")
            dia_diem.VI_TRI = data.get("VI_TRI")
            dia_diem.MO_TA_DD = data.get("MO_TA_DD")
            dia_diem.save()

            # Thư mục chứa hình ảnh
            folder_path = os.path.join(settings.MEDIA_ROOT, 'diadiem', str(dia_diem.MA_DD))

            os.makedirs(folder_path, exist_ok=True)
 
            # Xóa ảnh bị đánh dấu xoá
            for img in deleted_images:
                file_path = os.path.join(folder_path, os.path.basename(img))
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    os.remove(file_path)
               

            # Thêm ảnh mới
            image_paths = []
            for f in hinh_anh_files:
                image_name = f.name
                image_path = os.path.join('diadiem', str(dia_diem.MA_DD), image_name)

                with default_storage.open(image_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                image_paths.append(image_path)

            # Gộp ảnh cũ (chưa bị xoá) nếu cần
            if dia_diem.HINH_ANH_DD:
                # Xử lý khi HINH_ANH_DD là một chuỗi
                if isinstance(dia_diem.HINH_ANH_DD, str):
                    existing_images = [img for img in dia_diem.HINH_ANH_DD.split(',') if os.path.basename(img) not in deleted_images]
                else:
                    # Nếu là ImageField, chuyển đổi thành chuỗi
                    existing_images = []
                image_paths = existing_images + image_paths

            dia_diem.HINH_ANH_DD = ','.join(image_paths)
            dia_diem.save()

        # ===== THÊM MỚI =====
        else:
            dia_diem = DiaDiemDuLich.objects.create(
                TEN_DIA_DIEM=data.get("TEN_DIA_DIEM"),
                MA_DN_id=data.get("MA_DN"),
                TINH_THANH_PHO=data.get("TINH_THANH_PHO"),
                QUAN_HUYEN=data.get("QUAN_HUYEN"),
                KHU_VUC=data.get("KHU_VUC"),
                VI_TRI=data.get("VI_TRI"),
                MO_TA_DD=data.get("MO_TA_DD"),
            )

            # Sau khi tạo, đã có MA_DD để đặt folder ảnh đúng
            folder_path = os.path.join('diadiem', str(dia_diem.MA_DD))
            full_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
            os.makedirs(full_folder_path, exist_ok=True)

            image_paths = []
            for f in hinh_anh_files:
                image_name = f.name
                image_path = os.path.join(folder_path, image_name)

                with default_storage.open(image_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                image_paths.append(image_path)

            dia_diem.HINH_ANH_DD = ','.join(image_paths)
            dia_diem.save()

        return redirect('admin_core:manage_tourism')

    return redirect('admin_core:manage_tourism')
def xoa_dia_diem(request, ma_dd):
    try:
        # Tìm đối tượng DiaDiemDuLich theo MA_DD
        dia_diem = DiaDiemDuLich.objects.get(MA_DD=ma_dd)

        # Lấy đường dẫn thư mục chứa hình ảnh của địa điểm du lịch
        folder_path = os.path.join(settings.MEDIA_ROOT, 'diadiem', str(dia_diem.MA_DD))
        # Kiểm tra nếu thư mục tồn tại, xóa thư mục và các file bên trong
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # Xóa thư mục và tất cả các file trong thư mục

        # Xóa đối tượng DiaDiemDuLich khỏi cơ sở dữ liệu
        dia_diem.delete()

        # Sau khi xóa thành công, chuyển hướng đến trang quản lý
        return redirect('admin_core:manage_tourism')

    except DiaDiemDuLich.DoesNotExist:
        # Nếu không tìm thấy đối tượng DiaDiemDuLich, trả về lỗi 404
        raise Http404("Địa điểm không tồn tại.")  
def them_sua_dacsan(request, id=None):
    dacsan = DacSan.objects.filter(pk=id).first() if id else None

    if request.method == 'POST':
        ten_ds = request.POST.get('TEN_DS')
        ma_dd = request.POST.get('MA_DD')
        mo_ta = request.POST.get('MO_TA_DS')
        hinh_files = request.FILES.getlist('HINH_DS[]')
        deleted_images = request.POST.get('DELETED_IMAGES', '').split(',')

        deleted_images = [img.strip() for img in deleted_images if img.strip()]

        if dacsan:
            # === SỬA ===
            dacsan.TEN_DAC_SAN = ten_ds
            dacsan.MA_DD_id = ma_dd
            dacsan.MO_TA_DS = mo_ta

            folder_path = os.path.join(settings.MEDIA_ROOT, 'dacsan', str(dacsan.MA_DS))

            # Xóa các ảnh bị đánh dấu xóa
            for img in deleted_images:
                file_path = os.path.join(folder_path, os.path.basename(img))
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    os.remove(file_path)

            # Thêm ảnh mới
            if hinh_files:
                os.makedirs(folder_path, exist_ok=True)
                image_paths = []
                for f in hinh_files:
                    image_path = os.path.join('dacsan', str(dacsan.MA_DS), f.name)
                    full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
                    with default_storage.open(image_path, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    image_paths.append(image_path)

                # Cập nhật lại danh sách ảnh mới vào cơ sở dữ liệu
                dacsan.HINH_DS = ','.join(image_paths)

            dacsan.save()

        else:
            # === THÊM MỚI ===
            dacsan = DacSan.objects.create(
                TEN_DAC_SAN=ten_ds,
                MA_DD_id=ma_dd,
                MO_TA_DS=mo_ta,
            )

            if hinh_files:
                folder_path = os.path.join('dacsan', str(dacsan.MA_DS))
                full_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
                os.makedirs(full_folder_path, exist_ok=True)

                image_paths = []
                for f in hinh_files:
                    image_path = os.path.join(folder_path, f.name)
                    with default_storage.open(image_path, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    image_paths.append(image_path)

                dacsan.HINH_DS = ','.join(image_paths)
                dacsan.save()

        return redirect('admin_core:manage_tourism')

    return redirect('admin_core:manage_tourism')

def xoa_dac_san(request, ma_ds):
    try:
        # Tìm đối tượng DacSan theo MA_DS
        dac_san = DacSan.objects.get(MA_DS=ma_ds)

        # Lấy đường dẫn thư mục chứa hình ảnh của đặc sản
        folder_path = os.path.join(settings.MEDIA_ROOT, 'dacsan', str(dac_san.MA_DS))
        
        # Kiểm tra nếu thư mục tồn tại, xóa thư mục và các file bên trong
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # Xóa thư mục và tất cả các file trong thư mục

        # Xóa đối tượng DacSan khỏi cơ sở dữ liệu
        dac_san.delete()

        # Sau khi xóa thành công, chuyển hướng đến trang quản lý
        return redirect('admin_core:manage_tourism')

    except DacSan.DoesNotExist:
        # Nếu không tìm thấy đối tượng DacSan, trả về lỗi 404
        raise Http404("Đặc sản không tồn tại.")

def them_sua_tour(request, ma_tour=None):
    # Kiểm tra nếu tour đã tồn tại
    tour = TourDuLich.objects.filter(pk=ma_tour).first() if ma_tour else None

    if request.method == 'POST':
        # Lấy thông tin từ form
        ten_tour = request.POST.get('TEN_TOUR')
        mo_ta = request.POST.get('MO_TA_TOUR')
        gia = request.POST.get('GIA_TOUR')
        thoi_gian = request.POST.get('THOI_GIAN_DI_CHUYEN')
        hinh_files = request.FILES.getlist('HINH_TOUR[]')  # Lấy tất cả các tệp hình ảnh
        deleted_images = request.POST.get('DELETED_TOUR_IMAGES', '').split(',')  # Lấy các ảnh bị xóa

        deleted_images = [img.strip() for img in deleted_images if img.strip()]  # Làm sạch danh sách

        if tour:
            # === SỬA ===
            tour.TEN_TOUR = ten_tour
            tour.MO_TA_TOUR = mo_ta
            tour.GIA_TOUR = gia
            tour.THOI_GIAN_DI_CHUYEN = thoi_gian

            # Xử lý thư mục lưu trữ hình ảnh
            folder_path = os.path.join(settings.MEDIA_ROOT, 'tourdulich', str(tour.MA_TOUR))

            # Xóa các ảnh bị đánh dấu xóa
            for img in deleted_images:
                file_path = os.path.join(folder_path, os.path.basename(img))
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    os.remove(file_path)

            # Thêm ảnh mới
            if hinh_files:
                os.makedirs(folder_path, exist_ok=True)
                image_paths = []
                for f in hinh_files:
                    image_path = os.path.join('tourdulich', str(tour.MA_TOUR), f.name)
                    full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
                    with default_storage.open(image_path, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    image_paths.append(image_path)

                # Cập nhật lại danh sách ảnh mới vào cơ sở dữ liệu
                tour.HINH_TOUR = ','.join(image_paths)

            tour.save()

        else:
            # === THÊM MỚI ===
            # Tạo đối tượng Tour mới
            tour = TourDuLich.objects.create(
                TEN_TOUR=ten_tour,
                MO_TA_TOUR=mo_ta,
                GIA_TOUR=gia,
                THOI_GIAN_DI_CHUYEN=thoi_gian,
            )

            if hinh_files:
                folder_path = os.path.join('tourdulich', str(tour.MA_TOUR))
                full_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
                os.makedirs(full_folder_path, exist_ok=True)

                image_paths = []
                for f in hinh_files:
                    image_path = os.path.join(folder_path, f.name)
                    with default_storage.open(image_path, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    image_paths.append(image_path)

                tour.HINH_TOUR = ','.join(image_paths)
                tour.save()

        return redirect('admin_core:manage_tourism')

    return redirect('admin_core:manage_tourism')

def xoa_tour(request, ma_tour):
    try:
        # Tìm đối tượng TourDuLich theo MA_TOUR
        tour = TourDuLich.objects.get(MA_TOUR=ma_tour)

        # Lấy đường dẫn thư mục chứa hình ảnh của tour
        folder_path = os.path.join(settings.MEDIA_ROOT, 'tourdulich', str(tour.MA_TOUR))

        # Kiểm tra nếu thư mục tồn tại, xóa thư mục và các file bên trong
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # Xóa thư mục và tất cả các file trong thư mục

        # Xóa đối tượng TourDuLich khỏi cơ sở dữ liệu
        tour.delete()

        # Sau khi xóa thành công, chuyển hướng đến trang quản lý
        return redirect('admin_core:manage_tourism')

    except TourDuLich.DoesNotExist:
        # Nếu không tìm thấy đối tượng TourDuLich, trả về lỗi 404
        raise Http404("Tour không tồn tại.")
    
    
def them_sua_lich_trinh(request, ma_tour=None, ma_lich_trinh=None):
    thuoc_tour = ThuocTour.objects.filter(pk=ma_lich_trinh).first() if ma_lich_trinh else None

    if request.method == 'POST':
        ma_dd = request.POST.get('MA_DD')
        ma_tour = request.POST.get('MA_TOUR')
        thoi_gian_di = request.POST.get('THOI_GIAN_DI')
        thoi_gian_den = request.POST.get('THOI_GIAN_DEN')

        tour = TourDuLich.objects.filter(pk=ma_tour).first()
        dia_diem = DiaDiemDuLich.objects.filter(pk=ma_dd).first()

        if not tour or not dia_diem:
            raise Http404("Tour hoặc Địa điểm không tồn tại.")

        # Nếu là thêm mới
        if not thuoc_tour:
            if ThuocTour.objects.filter(MA_TOUR=tour, MA_DD=dia_diem).exists():
                messages.error(request, "Địa điểm này đã có trong tour.")
                return redirect('admin_core:manage_tourism')

            ThuocTour.objects.create(
                MA_TOUR=tour,
                MA_DD=dia_diem,
                THOI_GIAN_DI=thoi_gian_di,
                THOI_GIAN_DEN=thoi_gian_den
            )
            messages.success(request, "Thêm lịch trình thành công.")
        else:
            # Kiểm tra trùng khi cập nhật (bỏ qua chính nó)
            if ThuocTour.objects.filter(MA_TOUR=tour, MA_DD=dia_diem).exclude(pk=thuoc_tour.pk).exists():
                messages.error(request, "Địa điểm này đã có trong tour.")
                return redirect('admin_core:manage_tourism')

            thuoc_tour.MA_TOUR = tour
            thuoc_tour.MA_DD = dia_diem
            thuoc_tour.THOI_GIAN_DI = thoi_gian_di
            thuoc_tour.THOI_GIAN_DEN = thoi_gian_den
            thuoc_tour.save()
            messages.success(request, "Cập nhật lịch trình thành công.")

        return redirect('admin_core:manage_tourism')

    return redirect('admin_core:manage_tourism')

def xoa_lich_trinh(request, ma_lich_trinh):
    try:       
        # Lấy lịch trình theo mã
        thuoc_tour = ThuocTour.objects.get(MA_TUOCTOUR=ma_lich_trinh)
        
        # Xóa lịch trình
        thuoc_tour.delete()

        # Sau khi xóa, chuyển hướng về trang quản lý lịch trình của tour
        return redirect('admin_core:manage_tourism')

    except TourDuLich.DoesNotExist:
        raise Http404("Tour không tồn tại.")
    except ThuocTour.DoesNotExist:
        raise Http404("Lịch trình không tồn tại.")