from .models import DangKyHoiVien

def thong_bao_context(request):
    # Lọc các thông báo có trạng thái TINH_TRANG = 0 (chưa xử lý)
    thong_bao_moi = DangKyHoiVien.objects.filter(TINH_TRANG=0)

    # Trả về cả thông báo mới và số lượng thông báo
    return {
        'thong_bao_moi': thong_bao_moi,
        'thong_bao_count': thong_bao_moi.count()
    }
