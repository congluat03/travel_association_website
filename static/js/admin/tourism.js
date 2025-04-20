function openModal(data = null) {
  const modal = document.getElementById("diaDiemModal");
  modal.classList.remove("hidden");

  const form = modal.querySelector("form");
  if (data) {
    // Cập nhật action cho form sửa
    form.action = `/admin/tourism/diadiem/sua/${data.ma_dd}/`; // Hoặc dùng URL template nếu bạn render URL từ Django

    form.TEN_DIA_DIEM.value = data.ten;
    form.MA_DN.value = data.ma_dn;
    form.TINH_THANH_PHO.value = data.tinh_tp;
    form.QUAN_HUYEN.value = data.quan_huyen;
    form.KHU_VUC.value = data.khu_vuc;
    //   form.HINH_ANH_DD.value = data.hinh_anh;
    form.VI_TRI.value = data.vi_tri;
    form.MO_TA_DD.value = data.mo_ta;
  } else {
    form.reset(); // Nếu không có data thì reset form (thêm mới)
    form.action = `/admin/tourism/them/`; // URL thêm địa điểm
  }
}

function closeModal() {
  document.getElementById("diaDiemModal").classList.add("hidden");
}
function closeModalDS() {
  document.getElementById("dacSanModal").classList.add("hidden");
}
function openDacSanModal(data = null) {
  const modal = document.getElementById("dacSanModal"); // ID của modal đặc sản
  modal.classList.remove("hidden"); // Mở modal

  const form = document.getElementById("dacSanForm"); // Lấy form trong modal
  const imagePreviewContainer = document.getElementById(
    "image-preview-container"
  );
  const imagePreview = document.getElementById("image-preview");

  // Nếu có dữ liệu (sửa)
  if (data) {
    form.action = `/admin/tourism/dacsan/sua/${data.ma_ds}/`; // URL sửa đặc sản

    // Điền các giá trị vào form
    document.getElementById("TEN_DS").value = data.ten;
    document.getElementById("MA_DD").value = data.ma_dd;
    document.getElementById("MO_TA_DS").value = data.mo_ta;
    document.getElementById("HINH_DS").value = data.hinh;

    // Hiển thị hình ảnh hiện tại
    if (data.hinh) {
      imagePreview.src = data.hinh;
      imagePreviewContainer.classList.remove("hidden");
    }
  } else {
    form.reset(); // Nếu không có data thì reset form (thêm mới)
    form.action = `/admin/tourism/dacsan/them/`; // URL thêm đặc sản
    imagePreviewContainer.classList.add("hidden"); // Ẩn hình ảnh khi thêm mới
  }
  alert(form.action); // Thông báo mở modal
}

function closeModalTour() {
  document.getElementById("tourModal").classList.add("hidden");
}

function openTourModal(data = null) {
  const modal = document.getElementById("tourModal");
  modal.classList.remove("hidden");

  const form = modal.querySelector("form"); // Lấy form bên trong modal
  const imagePreviewContainer = document.getElementById(
    "image-preview-container-tour"
  );
  const imagePreview = document.getElementById("image-preview-tour");
  if (data) {
    // Gán URL sửa nếu có tour
    form.action = `/admin/tourism/tourdulich/sua/${data.ma_tour}/`;

    // Điền dữ liệu từ `data` vào các input
    document.getElementById("TEN_TOUR").value = data.ten_tour || "";
    document.getElementById("GIA_TOUR").value = data.gia_tour || "";
    document.getElementById("THOI_GIAN_DI_CHUYEN").value = data.thoi_gian || "";
    document.getElementById("HINH_TOUR").value = data.hinh || "";
    document.getElementById("MO_TA_TOUR").value = data.mo_ta || "";

    // Hiển thị ảnh nếu có
    if (data.hinh) {
      imagePreview.src = data.hinh;
      imagePreviewContainer.classList.remove("hidden");
    } else {
      imagePreviewContainer.classList.add("hidden");
    }
  } else {
    // Gán URL thêm mới và reset form
    form.action = `/admin/tourism/tourdulich/them/`;
    form.reset();
    imagePreviewContainer.classList.add("hidden");
  }
}
function openScheduleModal(data = null) {
  const modal = document.getElementById("scheduleModal");
  modal.classList.remove("hidden");

  const form = modal.querySelector("form");

  if (data) {
    console.log(data);  // In ra dữ liệu để kiểm tra

    // Gán URL sửa nếu có lịch trình
    form.action = `/admin/tourism/lichtrinh/sua/${data.ma_tour}/${data.ma_tuoctour}/`;

    // Chuyển thời gian về định dạng mà input[type="datetime-local"] có thể hiểu (yyyy-mm-ddThh:mm)
    const thoiGianDi = data.thoi_gian_di ? data.thoi_gian_di.replace(" ", "T") : "";
    const thoiGianDen = data.thoi_gian_den ? data.thoi_gian_den.replace(" ", "T") : "";

    // Điền dữ liệu vào các input
    document.getElementById("ma_tour").value = data.ma_tour || "";
    document.getElementById("ma_dd").value = data.ma_dd || "";
    document.getElementById("thoi_gian_di").value = thoiGianDi;
    document.getElementById("thoi_gian_den").value = thoiGianDen;

    // Lưu mã lịch trình
    document.getElementById("ma_lich_trinh").value = data.ma_tuoctour || "";
  } else {
    form.action = `/admin/tourism/lichtrinh/them/`;
    form.reset();
  }
}

function closeModalLichTrinh() {
  document.getElementById("scheduleModal").classList.add("hidden");
}
