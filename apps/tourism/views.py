from django.shortcuts import render
from apps.tourism.models import DiaDiemDuLich,DacSan,TourDuLich,ThuocTour
from apps.members.models import DoanhNghiep
from django.shortcuts import get_object_or_404, redirect
import os
from django.conf import settings
from django.db.models import Q
# Create your views here.
def home(request):
    return render(request, 'core/home.html', {'title': 'Trang chủ'})

from django.core.paginator import Paginator


def danhsachdiadiem(request):
    query = request.GET.get('q', '')  # Nếu không có giá trị thì mặc định là chuỗi rỗng
    tinh_loc = request.GET.get('tinh', '')  # Mặc định là chuỗi rỗng
    khu_loc = request.GET.get('khu', '')  # Mặc định là chuỗi rỗng

    # Lấy danh sách địa điểm du lịch
    diadiem_list = DiaDiemDuLich.objects.all()

    # Áp dụng tìm kiếm theo tên địa điểm
    if query:
        diadiem_list = diadiem_list.filter(TEN_DIA_DIEM__icontains=query)

    # Lọc theo tỉnh thành
    if tinh_loc:
        diadiem_list = diadiem_list.filter(TINH_THANH_PHO=tinh_loc)

    # Lọc theo khu vực
    if khu_loc:
        diadiem_list = diadiem_list.filter(KHU_VUC__icontains=khu_loc)

    # Phân trang: Mỗi trang có tối đa 8 địa điểm (4 card mỗi dòng, 2 dòng mỗi trang)
    paginator = Paginator(diadiem_list, 8)  # Số lượng địa điểm trên mỗi trang là 8
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lấy danh sách tỉnh và khu vực duy nhất để làm dropdown lọc
    danh_sach_tinh = DiaDiemDuLich.objects.values_list('TINH_THANH_PHO', flat=True).distinct()
    danh_sach_khu = DiaDiemDuLich.objects.values_list('KHU_VUC', flat=True).distinct()

    # Sao chép các tham số query để giữ lại khi phân trang
    query_params = request.GET.copy()

    return render(request, 'index/tourism/diadiem/diadiemdulich.html', {
        'diadiem_list': page_obj,
        'danh_sach_tinh': danh_sach_tinh,
        'danh_sach_khu': danh_sach_khu,
        'query': query,
        'tinh_loc': tinh_loc,
        'khu_loc': khu_loc,
        'query_params': query_params,
    })

def chitietdiadiem(request, ma_dd):
    dd = get_object_or_404(DiaDiemDuLich, MA_DD=ma_dd)

    # Lấy các đặc sản theo địa điểm
    dacsan_list = DacSan.objects.filter(MA_DD=dd)

    # Lấy các tour có liên quan đến địa điểm này
    tour_list = TourDuLich.objects.filter(thuoctour__MA_DD=dd).distinct()

    # Lấy các địa điểm liên quan (cùng khu vực)
    related_dd_list = DiaDiemDuLich.objects.filter(TINH_THANH_PHO=dd.TINH_THANH_PHO).exclude(MA_DD=ma_dd)[:6]

    # Lấy danh sách ảnh từ thư mục media/diadiem/<MA_DD>/
    image_dir = os.path.join(settings.MEDIA_ROOT, 'diadiem', str(dd.MA_DD))
    images = []
    
    if os.path.exists(image_dir):
        images = [
            f"/media/diadiem/{dd.MA_DD}/{filename}"
            for filename in os.listdir(image_dir)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]
    
    # Nếu HINH_ANH_DD có ảnh, đảm bảo nó được bao gồm trong danh sách
    if dd.HINH_ANH_DD and dd.HINH_ANH_DD.url not in images:
        images.insert(0, dd.HINH_ANH_DD.url)  # Thêm ảnh từ HINH_ANH_DD lên đầu danh sách

    return render(request, 'index/tourism/diadiem/chitietdiadiem.html', {
        'dd': dd,
        'dacsan_list': dacsan_list,
        'tour_list': tour_list,
        'related_dd_list': related_dd_list,
        'images': images,  # Truyền danh sách ảnh vào template
    })

def danhsachdacsan(request):
    provinces = DiaDiemDuLich.objects.values_list('TINH_THANH_PHO', flat=True).distinct()

    province = request.GET.get('province', '')  # Mặc định là chuỗi rỗng nếu không có giá trị
    query = request.GET.get('q', '')

    if province and query:
        dacsans = DacSan.objects.filter(
            Q(TEN_DAC_SAN__icontains=query),
            Q(MA_DD__TINH_THANH_PHO=province)
        )
    elif province:
        dacsans = DacSan.objects.filter(MA_DD__TINH_THANH_PHO=province)
    elif query:
        dacsans = DacSan.objects.filter(TEN_DAC_SAN__icontains=query)
    else:
        dacsans = DacSan.objects.all()

    # Phân trang
    paginator = Paginator(dacsans, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index/tourism/dacsan/dacsan.html', {
        'dacsans': page_obj,
        'provinces': provinces,
        'query': query,
        'province': province,  # Truyền giá trị province vào context
    })


def tour(request):
    # Lấy tất cả các tour ban đầu
    tours = TourDuLich.objects.all()

    # Lọc theo tỉnh (từ bảng DiaDiemDuLich thông qua ThuocTour)
    tinh_chon = request.GET.get('tinh', '')  # Mặc định là chuỗi rỗng
    if tinh_chon:
        tours = tours.filter(
            thuoctour__MA_DD__TINH_THANH_PHO=tinh_chon
        )

    # Lọc theo thời gian (từ bảng TourDuLich)
    thoigian_chon = request.GET.get('thoigian', '')  # Mặc định là chuỗi rỗng
    if thoigian_chon:
        if thoigian_chon == '1':
            tours = tours.filter(THOI_GIAN_DI_CHUYEN__icontains='1 ngày')
        elif thoigian_chon == '2-3':
            tours = tours.filter(Q(THOI_GIAN_DI_CHUYEN__icontains='2 ngày') | Q(THOI_GIAN_DI_CHUYEN__icontains='3 ngày'))
        elif thoigian_chon == '3+':
            tours = tours.exclude(THOI_GIAN_DI_CHUYEN__icontains='1 ngày') \
                         .exclude(THOI_GIAN_DI_CHUYEN__icontains='2 ngày') \
                         .exclude(THOI_GIAN_DI_CHUYEN__icontains='3 ngày')

    # Lọc theo giá (từ bảng TourDuLich)
    giatour_chon = request.GET.get('gia', '')  # Mặc định là chuỗi rỗng
    if giatour_chon:
        if giatour_chon == 'duoi1':
            tours = tours.filter(GIA_TOUR__lt=1_000_000)
        elif giatour_chon == '1-3':
            tours = tours.filter(GIA_TOUR__gte=1_000_000, GIA_TOUR__lte=3_000_000)
        elif giatour_chon == 'tren3':
            tours = tours.filter(GIA_TOUR__gt=3_000_000)

    # Tìm kiếm theo tên hoặc mô tả tour (tour đi)
    timkiem_chon = request.GET.get('timkiem', '')  # Mặc định là chuỗi rỗng
    if timkiem_chon:
        tours = tours.filter(
            Q(TEN_TOUR__icontains=timkiem_chon) | Q(MO_TA_TOUR__icontains=timkiem_chon)
        )

    # Tính giá theo triệu (từ bảng TourDuLich)
    for tour in tours:
        tour.gia_trieu = round(tour.GIA_TOUR / 1_000_000, 1)

    # Danh sách tỉnh để hiển thị ở dropdown (lấy từ bảng DiaDiemDuLich)
    tinhs = DiaDiemDuLich.objects.values_list('TINH_THANH_PHO', flat=True).distinct()

    return render(request, 'index/tourism/tour/tourdulich.html', {
        'tours': tours,
        'tinhs': tinhs,
        'tinh_chon': tinh_chon,
        'thoigian_chon': thoigian_chon,
        'giatour_chon': giatour_chon,
        'timkiem_chon': timkiem_chon,  # Truyền giá trị tìm kiếm vào template
    })


def chitiettour(request, ma_tour):
    # Lấy tour theo ID
    tour = get_object_or_404(TourDuLich, MA_TOUR=ma_tour)

    # Lấy các địa điểm thuộc tour này
    related_dd_list = DiaDiemDuLich.objects.filter(thuoctour__MA_TOUR=tour)

    # Lấy các thông tin liên quan trong bảng ThuocTour
    thuoc_tour = ThuocTour.objects.filter(MA_TOUR=tour)  # Truy vấn theo MA_TOUR
    
    # Tính giá theo triệu để hiển thị đẹp hơn
    if tour.GIA_TOUR > 0:  # Kiểm tra giá trị hợp lệ
        tour.gia_trieu = round(tour.GIA_TOUR / 1_000_000, 1)
    else:
        tour.gia_trieu = 0  # Nếu giá không hợp lệ, đặt là 0

    # Lấy danh sách ảnh từ thư mục media/tourdulich/<MA_TOUR>/
    image_dir = os.path.join(settings.MEDIA_ROOT, 'tourdulich', str(tour.MA_TOUR))
    images = []

    if os.path.exists(image_dir):
        images = [
            f"/media/tourdulich/{tour.MA_TOUR}/{filename}"
            for filename in os.listdir(image_dir)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]

    return render(request, 'index/tourism/tour/chitiettour.html', {
        'tour': tour,
        'related_dd_list': related_dd_list,
        'thuoc_tour': thuoc_tour,
        'images': images,
    })
