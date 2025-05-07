from django.shortcuts import render
from .models import TinTuc, TheTag,TrackingXemTin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator

def danhsachtintuc(request):
     query = request.GET.get('q', '')  
     tag_id = request.GET.get('tag', '')  
     only_highlight = request.GET.get('only_highlight', '')  
     loai_tin_tuc = request.GET.get('loai_tin_tuc', '') 
 
     # Lọc tin tức theo các điều kiện
     tin_tuc_list = TinTuc.objects.all().order_by('-NGAY_DANG')
 
     # Lọc theo tiêu đề hoặc nội dung nếu query không phải rỗng
     if query:
         tin_tuc_list = tin_tuc_list.filter(
             Q(TIEU_DE__icontains=query) | Q(NOI_DUNG_CHI_TIET__icontains=query)
         )
 
     # Lọc theo tag nếu tag_id không phải rỗng
     if tag_id:
         tin_tuc_list = tin_tuc_list.filter(MA_TAG__MA_TAG=tag_id)
 
     # Lọc theo Nổi bật nếu only_highlight có giá trị '0' hoặc '1'
     if only_highlight in ['0', '1']:  
         tin_tuc_list = tin_tuc_list.filter(TIN_NOI_BAT=(only_highlight == '1'))
 
     # Lọc theo Loại Tin Tức nếu loai_tin_tuc không phải rỗng
     if loai_tin_tuc:
         tin_tuc_list = tin_tuc_list.filter(LOAI_TIN_TUC=loai_tin_tuc)
 
     # Phân trang: Mỗi trang có tối đa 10 tin tức
     paginator = Paginator(tin_tuc_list, 10)  
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
 
     # Lấy danh sách tag để hiển thị trên giao diện
     tags = TheTag.objects.all()
 
     # Lấy tất cả các loại tin tức (để hiển thị trong dropdown)
     loai_tin_tuc_list = TinTuc.objects.values('LOAI_TIN_TUC').distinct()
 
     # Sao chép các tham số query để giữ lại khi phân trang
     query_params = request.GET.copy()
 
     context = {
         'page_obj': page_obj,
         'query': query,  
         'tags': tags,
         'selected_tag': tag_id,
         'only_highlight': only_highlight,
         'loai_tin_tuc': loai_tin_tuc,
         'loai_tin_tuc_list': loai_tin_tuc_list,  # Truyền danh sách loại tin tức
         'query_params': query_params,  
     }
 
     return render(request, 'index/news/tintuc.html', context)
 
 
 
 
 
def chitiettintuc(request, ma_tin):
    # Truy vấn bài viết theo MA_TIN
    tin = get_object_or_404(TinTuc, MA_TIN=ma_tin)

    # Tăng số lượt xem
    tin.SO_LUOT_XEM += 1
    tin.save()

    # Ghi tracking nếu người dùng đã đăng nhập
    if request.user.is_authenticated:
        try:
            from members.models import TaiKhoan  # import nếu chưa có
            tai_khoan = getattr(request.user, 'taikhoan', None)  # lấy đối tượng TaiKhoan liên kết với User

            if tai_khoan:
                TrackingXemTin.objects.create(
                    MA_TK=tai_khoan,
                    MA_TIN=tin,
                    THOI_GIAN_XEM=timezone.now()
                )
        except Exception as e:
            # Có thể ghi log nếu gặp lỗi ở đây
            print(f"Lỗi khi ghi tracking: {e}")

    # Lấy danh sách các tag của bài viết
    tags = tin.MA_TAG.all()

    # Trả về dữ liệu để render template
    context = {
        'tin': tin,
        'tags': tags,
    }
    return render(request, 'index/news/chitiettintuc.html', context)