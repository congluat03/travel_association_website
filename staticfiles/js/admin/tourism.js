
  // function openModal(data = null) {
  //   const modal = document.getElementById("diaDiemModal");
  //   modal.classList.remove("hidden");

  //   const form = modal.querySelector("form");
  //   if (data) {
  //     // Cập nhật action cho form sửa
  //     form.action = `/admin/tourism/diadiem/sua/${data.ma_dd}/`;  // Hoặc dùng URL template nếu bạn render URL từ Django

  //     form.TEN_DIA_DIEM.value = data.ten;
  //     form.MA_DN.value = data.ma_dn;
  //     form.TINH_THANH_PHO.value = data.tinh_tp;
  //     form.QUAN_HUYEN.value = data.quan_huyen;
  //     form.KHU_VUC.value = data.khu_vuc;
  //   //   form.HINH_ANH_DD.value = data.hinh_anh;
  //     form.VI_TRI.value = data.vi_tri;
  //     form.MO_TA_DD.value = data.mo_ta;
  //   } else {
  //     form.reset();  // Nếu không có data thì reset form (thêm mới)
  //     form.action = `/admin/tourism/them/`;  // URL thêm địa điểm
  //   }
  // }

  // function closeModal() {
  //   document.getElementById("diaDiemModal").classList.add("hidden");
  // }

