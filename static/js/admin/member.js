
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

function closeDoanhNghiepModal() {
    document.getElementById("doanhNghiepModal").classList.add("hidden");
}
