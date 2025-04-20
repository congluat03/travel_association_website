function openTaiLieuModal(data = null) {
    const modal = document.getElementById("taiLieuModal");
    modal.classList.remove("hidden");

    const form = document.getElementById("taiLieuForm");

    // Nếu có dữ liệu, thiết lập để sửa
    if (data) {
        // Đảm bảo URL sửa tài liệu đúng
        form.action = `/admin/support/tailieu/sua/${data.ma_tl}/`;

        // Cập nhật các trường trong form
        document.getElementById("tieu_de_tl").value = data.tieu_de_tl || "";
        document.getElementById("loai_tai_lieu").value = data.loai_tai_lieu || "";
        document.getElementById("ngay_cap_nhat").value = data.ngay_cap_nhat || "";
        document.getElementById("duong_dan_file").value = data.duong_dan_file || "";
        document.getElementById("ma_dn").value = data.ma_dn || "";
        document.getElementById("mo_ta_tl").value = data.mo_ta_tl || "";
    } else {
        // Nếu không có dữ liệu, thiết lập để thêm mới
        form.action = "/admin/support/tailieu/them/";
        form.reset();  // Reset form

        // Reset hidden input mã tài liệu (tránh giữ mã cũ)
        document.getElementById("ma_tl").value = "";
    }
}


function closeTaiLieuModal() {
    document.getElementById("taiLieuModal").classList.add("hidden");
}
