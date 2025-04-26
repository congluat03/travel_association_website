from django.http import Http404
from .models import TaiLieu
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import redirect
import shutil

def them_sua_tailieu(request, ma_tl=None): 
    tailieu = TaiLieu.objects.filter(pk=ma_tl).first() if ma_tl else None

    if request.method == 'POST':
        tieu_de = request.POST.get('TIEU_DE_TL')
        mo_ta = request.POST.get('MO_TA_TL')
        loai = request.POST.get('LOAI_TAI_LIEU')
        ngay = request.POST.get('NGAY_CAP_NHAT')
        ma_dn = request.POST.get('MA_DN')
        file = request.FILES.get('DUONG_DAN_FILE')

        if tailieu:
            # === CẬP NHẬT TÀI LIỆU ===
            tailieu.TIEU_DE_TL = tieu_de
            tailieu.MO_TA_TL = mo_ta
            tailieu.LOAI_TAI_LIEU = loai
            tailieu.NGAY_CAP_NHAT = ngay
            tailieu.MA_DN_id = ma_dn

            if file:
                # XÓA FILE CŨ nếu có
                if tailieu.DUONG_DAN_FILE and default_storage.exists(str(tailieu.DUONG_DAN_FILE)):
                    default_storage.delete(str(tailieu.DUONG_DAN_FILE))

                # LƯU FILE MỚI
                folder_path = os.path.join('tailieu', str(tailieu.MA_TL))
                os.makedirs(os.path.join(settings.MEDIA_ROOT, folder_path), exist_ok=True)

                file_path = os.path.join(folder_path, file.name)
                with default_storage.open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                tailieu.DUONG_DAN_FILE = file_path

            tailieu.save()

        else:
            # === THÊM MỚI TÀI LIỆU ===
            new_tailieu = TaiLieu.objects.create(
                TIEU_DE_TL=tieu_de,
                MO_TA_TL=mo_ta,
                LOAI_TAI_LIEU=loai,
                NGAY_CAP_NHAT=ngay,
                MA_DN_id=ma_dn
            )

            if file:
                folder_path = os.path.join('tailieu', str(new_tailieu.MA_TL))
                os.makedirs(os.path.join(settings.MEDIA_ROOT, folder_path), exist_ok=True)

                file_path = os.path.join(folder_path, file.name)
                with default_storage.open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                new_tailieu.DUONG_DAN_FILE = file_path
                new_tailieu.save()

        # Sau khi thêm hoặc sửa xong, quay lại trang quản lý tài liệu
        return redirect('admin_core:manage_support')

    # Nếu GET request, hiển thị lại giao diện quản lý
    return redirect('admin_core:manage_support')
def xoa_tailieu(request, ma_tl):
    try:
        # Tìm tài liệu theo MA_TL
        tailieu = TaiLieu.objects.get(MA_TL=ma_tl)

        # Lấy đường dẫn thư mục chứa tài liệu (ở media/tailieu/<MA_TL>/)
        folder_path = os.path.join(settings.MEDIA_ROOT, 'tailieu', str(tailieu.MA_TL))

        # Nếu thư mục chứa tài liệu tồn tại, xoá thư mục
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # Xoá thư mục và tất cả nội dung bên trong

        # Xoá tài liệu khỏi cơ sở dữ liệu
        tailieu.delete()

        # Điều hướng về trang danh sách tài liệu sau khi xóa
        return redirect('admin_core:manage_support')

    except TaiLieu.DoesNotExist:
        raise Http404("Tài liệu không tồn tại.")