from apps.core import admin_views
from django.http import Http404, JsonResponse

from .models import TinTuc, TheTag, TrackingXemTin, CoTheTag

from apps.members.models import TaiKhoan

def them_sua_tag(request, ma_tag=None):
    # Kiểm tra xem có id (thẻ tag cần sửa) không
    tag = TheTag.objects.filter(pk=ma_tag).first() if ma_tag else None

    if request.method == 'POST':
        ten_tag = request.POST.get('TEN_TAG')  # Lấy tên thẻ tag
        mo_ta_tag = request.POST.get('MO_TA_TAG')  # Lấy mô tả thẻ tag

        if tag:
            # Sửa thẻ tag nếu đã tồn tại
            tag.TEN_TAG = ten_tag
            tag.MO_TA_TAG = mo_ta_tag
            tag.save()
        else:
            # Thêm thẻ tag nếu chưa có
            TheTag.objects.create(
                TEN_TAG=ten_tag,
                MO_TA_TAG=mo_ta_tag
            )
        # Sau khi thêm/sửa xong, quay lại trang quản lý thẻ tag
        return admin_views.manage_news(request)  # Quay lại trang quản lý tin tức hoặc thẻ tag tùy theo yêu cầu

    # Nếu không phải POST, chỉ trả về trang quản lý thẻ tag
    return admin_views.manage_news(request)
def xoa_thetag(request, ma_tag):
    try:
        tag = TheTag.objects.get(MA_TAG=ma_tag)  # Tìm thẻ tag theo MA_TAG
        tag.delete()  # Xóa thẻ tag
        return admin_views.manage_news(request)  # Quay lại trang quản lý tin tức hoặc tag
    except TheTag.DoesNotExist:
        raise Http404("Thẻ tag không tồn tại.")
def xoa_news(request, ma_tin):
    try:
        news = TinTuc.objects.get(MA_TIN=ma_tin)
        news_title = news.TIEU_DE
        news.delete()  # Tự động xóa luôn các bản ghi liên quan trong CoTheTag nhờ on_delete
        return admin_views.manage_news(request)
    except TinTuc.DoesNotExist:
        raise Http404("Tin tức không tồn tại.")
def them_sua_tintuc(request, ma_tin=None):
    # Kiểm tra nếu là sửa tin tức (có mã tin)
    tintuc = TinTuc.objects.filter(pk=ma_tin).first() if ma_tin else None

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        ma_tk = request.POST.get('MA_TK')
        tieu_de = request.POST.get('TIEU_DE')
        noi_dung = request.POST.get('NOI_DUNG_CHI_TIET')
        loai_tin_tuc = request.POST.get('LOAI_TIN_TUC')
        ngay_dang = request.POST.get('NGAY_DANG')
        # Trong views.py của Django
        tin_noi_bat = request.POST.get('tin_noi_bat') == 'true'

        url_hinh = request.POST.get('URL_HINH', None)  # Tuỳ chọn, không có trong form bạn gửi
        ds_tag = request.POST.getlist('MA_TAG')  # Lấy danh sách thẻ tag
        # Kiểm tra tài khoản hợp lệ
        try:
            tai_khoan = TaiKhoan.objects.get(pk=ma_tk)
        except TaiKhoan.DoesNotExist:
            return JsonResponse({'error': 'Tài khoản không tồn tại'}, status=400)

        if tintuc:
            # Cập nhật tin tức
            tintuc.MA_TK = tai_khoan
            tintuc.TIEU_DE = tieu_de
            tintuc.NOI_DUNG_CHI_TIET = noi_dung
            tintuc.LOAI_TIN_TUC = loai_tin_tuc
            tintuc.TIN_NOI_BAT = tin_noi_bat
            tintuc.NGAY_DANG = ngay_dang  # Hoặc ngày bạn muốn cập nhật
            if url_hinh:
                tintuc.URL_HINH = url_hinh
            tintuc.save()

            # Cập nhật các thẻ tag (xoá hết rồi thêm lại)
            CoTheTag.objects.filter(MA_TIN=tintuc).delete()
            for ma_tag in ds_tag:
                try:
                    tag = TheTag.objects.get(pk=ma_tag)
                    CoTheTag.objects.create(MA_TIN=tintuc, MA_TAG=tag)
                except TheTag.DoesNotExist:
                    return JsonResponse({'error': f'Tag {ma_tag} không tồn tại'}, status=400)

        else:
            # Thêm mới tin tức
            tintuc = TinTuc.objects.create(
                MA_TK=tai_khoan,
                TIEU_DE=tieu_de,
                NOI_DUNG_CHI_TIET=noi_dung,
                NGAY_DANG=ngay_dang,
                LOAI_TIN_TUC=loai_tin_tuc,
                TIN_NOI_BAT=tin_noi_bat,
                URL_HINH=url_hinh
            )

            # Thêm các thẻ tag
            for ma_tag in ds_tag:
                try:
                    tag = TheTag.objects.get(pk=ma_tag)
                    CoTheTag.objects.create(MA_TIN=tintuc, MA_TAG=tag)
                except TheTag.DoesNotExist:
                    return JsonResponse({'error': f'Tag {ma_tag} không tồn tại'}, status=400)

        # Sau khi thêm/sửa, chuyển về trang quản lý tin tức
        return admin_views.manage_news(request)

    # Nếu không phải POST, chuyển hướng hoặc render tùy ý (tuỳ bạn)
    return admin_views.manage_news(request)