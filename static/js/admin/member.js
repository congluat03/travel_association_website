console.log("Script loaded");
function openHiepHoiModal(data = null) {
  const modal = document.getElementById("hiepHoiModal");
  const form = document.getElementById("hiepHoiForm");

  if (data) {
    form.MA_HH.value = data.ma_hh || "";
    form.TEN_HH.value = data.ten || "";
    form.MO_TA_HH.value = data.mo_ta || "";
    form.action = `/admin/members/hiephoi/sua/${data.ma_hh}/`;  // Đảm bảo URL đúng
  } else {
    form.reset();
    form.action = "/admin/members/hiephoi/them/";
  }

  modal.classList.remove("hidden");
  alert(form.action);
}


function closeHiepHoiModal() {
  document.getElementById("hiepHoiModal").classList.add("hidden");
}

function openNganhModal(data = null) {
  const modal = document.getElementById("nganhModal");
  const form = document.getElementById("nganhForm");

  if (data) {
    form.MA_NGANH.value = data.ma_nganh || "";
    form.TEN_NGANH.value = data.ten_nganh || "";
    form.action = `/admin/members/nganhnghe/sua/${data.ma_nganh}/`;  // URL sửa
  } else {
    form.reset();
    form.action = "/admin/members/nganhnghe/them/";  // URL thêm
  }

  modal.classList.remove("hidden");
  alert(form.action); // chỉ để test, có thể bỏ nếu không cần
}

function closeNganhModal() {
  document.getElementById("nganhModal").classList.add("hidden");
}

function openDoanhNghiepModal(data = null) {
  const modal = document.getElementById("doanhNghiepModal");
  const form = document.getElementById("doanhNghiepForm");

  if (data) {
    form.MA_DN.value = data.ma_dn || "";
    form.TEN_DN.value = data.ten_dn || "";
    form.NGUOI_DAI_DIEN.value = data.nguoi_dai_dien || "";
    form.EMAIL_DN.value = data.email || "";
    form.SDT_DN.value = data.sdt || "";
    form.DIA_CHI.value = data.dia_chi || "";
    form.MA_NGANH.value = data.ma_nganh || ""; // set combobox ngành theo id
    form.TRANG_THAI_DUYET.value = data.trang_thai_duyet !== undefined ? data.trang_thai_duyet : "0";  // Set giá trị duyệt (0 hoặc 1)
    form.action = `/admin/members/doanhnghiep/sua/${data.ma_dn}/`;  // URL sửa
  } else {
    form.reset();
    form.TRANG_THAI_DUYET.value = "0";  // Mặc định là Chưa Duyệt (0)
    form.action = "/admin/members/doanhnghiep/them/";  // URL thêm
  }

  modal.classList.remove("hidden");
}
// const today = new Date("2025-04-20");  // Ngày hiện tại
//   const rows = document.querySelectorAll("tbody tr");

//   rows.forEach(row => {
//     const ngayDangKyStr = row.querySelector("[data-ngay-dang-ky]").getAttribute("data-ngay-dang-ky");
//     if (ngayDangKyStr) {
//       const ngayDangKy = new Date(ngayDangKyStr);
//       const soNgay = Math.floor((today - ngayDangKy) / (1000 * 60 * 60 * 24));  // Tính số ngày
//       row.querySelector("[data-ngay-dang-ky]").textContent = soNgay >= 0 ? soNgay : "N/A";
//     } else {
//       row.querySelector("[data-ngay-dang-ky]").textContent = "N/A";
//     }
//   });

function closeDoanhNghiepModal() {
  document.getElementById("doanhNghiepModal").classList.add("hidden");
}
function openDangKyHoiVienModal(data = null) {
  console.log("Dữ liệu truyền vào modal:", data);  // Gỡ lỗi dữ liệu
  const modal = document.getElementById("dangKyHoiVienModal");
  const form = document.getElementById("dangKyHoiVienForm");

  if (data) {
    console.log("Đặt MA_HH thành:", data.ma_hh);  // Gỡ lỗi giá trị MA_HH
    console.log("Tên Hiệp Hội:", data.ten_hh);    // Gỡ lỗi tên Hiệp Hội
    console.log("Đặt MA_DN thành:", data.ma_dn);  // Gỡ lỗi giá trị MA_DN
    console.log("Tên Doanh Nghiệp:", data.ten_dn); // Gỡ lỗi tên Doanh Nghiệp

    form.MA_DK_HH.value = data.ma_dk_hh || "";
    form.MA_HH.value = data.ma_hh || "";  // Đặt ID cho dropdown Hiệp Hội
    form.MA_DN.value = data.ma_dn || "";  // Đặt ID cho dropdown Doanh Nghiệp
    form.TINH_TRANG.value = data.tinh_trang !== undefined ? data.tinh_trang : "0";
    form.NGAY_DANG_KY.value = data.ngay_dang_ky || "";
    form.action = `/admin/members/dangkyhoivien/sua/${data.ma_dk_hh}/`;
  } else {
    form.reset();
    form.TINH_TRANG.value = "0"; // Mặc định là Chưa duyệt
    form.action = "/admin/members/dangkyhoivien/them/";
  }

  modal.classList.remove("hidden");
}

function closeDangKyHoiVienModal() {
  document.getElementById("dangKyHoiVienModal").classList.add("hidden");
}


function openTaiKhoanModal(data = null) {
  const modal = document.getElementById("nguoiDungModal");
  const form = document.getElementById("form_taikhoan");

  // Hiển thị modal
  modal.classList.remove("hidden");

  if (data) {
    // Gán giá trị vào form
    form.TEN_DANG_NHAP.value = data.ten_dang_nhap || "";
    form.EMAIL_TK.value = data.email || "";
    form.MAT_KHAU.value = data.mat_khau || "";
    form.VAI_TRO.value = data.vai_tro || "";
    form.TRANG_THAI_TK.value = (data.trang_thai === true || data.trang_thai === 'True') ? '1' : '0';
    form.MA_DN.value = data.ma_dn || "";

    // Gán đường dẫn action để sửa tài khoản
    form.action = `/admin/members/taikhoan/sua/${data.ma_tk}/`;
    // Hiển thị ảnh nếu có
    const previewImg = document.getElementById("previewImg");
    if (data.anh_dai_dien) {
      previewImg.src = data.anh_dai_dien;
      previewImg.classList.remove("hidden"); // Hiển thị ảnh
    } else {
      previewImg.src = "#";
      previewImg.classList.add("hidden"); // Ẩn ảnh nếu không có
    }
  } else {
    // Reset form khi thêm mới
    form.reset();
    form.action = "/admin/members/taikhoan/them/";
    form.TRANG_THAI_TK.value = "1"; // Mặc định hoạt động

    // Tiêu đề
    document.getElementById("form-title").textContent = "👤 Thêm người dùng";

    // Ẩn ảnh preview
    const previewImg = document.getElementById("previewImg");
    previewImg.src = "#";
    previewImg.classList.add("hidden");
  }
}


function closeTaiKhoanModal() {
  document.getElementById("nguoiDungModal").classList.add("hidden");
}


