from django.shortcuts import get_object_or_404, render
from .models import TaiLieu
from django.core.paginator import Paginator  # t
from django.db.models import Q
# Create your views here.
def danh_sach_tailieu(request): 
    """Hiển thị thư viện tài liệu với tìm kiếm, bộ lọc & phân trang."""
    # --- lấy tham số ---
    q = request.GET.get('q', '').strip()
    loai = request.GET.get('loai', '').strip()

    # --- dựng queryset ---
    qs = TaiLieu.objects.all()

    if q:
        qs = qs.filter(
            Q(TIEU_DE_TL__icontains=q) |
            Q(MO_TA_TL__icontains=q)   |
            Q(MA_DN__TEN_DN__icontains=q)
        )

    if loai:
        qs = qs.filter(LOAI_TAI_LIEU=loai)

    qs = qs.order_by('-NGAY_CAP_NHAT')

    # --- phân trang ---
    paginator = Paginator(qs, 8)  # 8 tài liệu / trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- danh sách loại tài liệu (đổ vào dropdown) ---
    loai_list = (TaiLieu.objects
                 .values_list('LOAI_TAI_LIEU', flat=True)
                 .distinct()
                 .order_by('LOAI_TAI_LIEU'))

    # --- context ---
    context = {
        'tailieu_list': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'loai_list': loai_list,
        'search': q,
        'nganh': loai,
    }

    return render(request, 'index/support/tailieu.html', context)

def chi_tiet_tailieu(request, pk):
    tailieu = get_object_or_404(TaiLieu, pk=pk)
    return render(request, 'index/support/chitiettailieu.html', {'tailieu': tailieu})
