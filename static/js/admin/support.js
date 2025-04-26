function openTaiLieuModal(data = null) {
    const modal = document.getElementById("taiLieuModal");
    modal.classList.remove("hidden");

    const form = document.getElementById("taiLieuForm");

    if (data) {
        // URL sửa
        form.action = `/admin/support/tailieu/sua/${data.ma_tl}/`;

        // điền các trường văn bản
        document.getElementById("tieu_de_tl").value = data.tieu_de_tl ?? "";
        document.getElementById("loai_tai_lieu").value = data.loai_tai_lieu ?? "";
        document.getElementById("ngay_cap_nhat").value = data.ngay_cap_nhat ?? "";
        document.getElementById("ma_dn").value = data.ma_dn ?? "";
        document.getElementById("mo_ta_tl").value = data.mo_ta_tl ?? "";
        // hiển thị tên file hiện có (nếu cần)
        const fileNameLabel = document.getElementById("duong_dan_file");
        if (fileNameLabel) {
            fileNameLabel.textContent = data.duong_dan_file?.split("/").pop() || "Chưa có";
        }
        // KHÔNG gán .value cho input file!
    } else {
        // URL thêm mới
        form.action = "/admin/support/tailieu/them/";
        form.reset();

        // xóa mã tài liệu ẩn
        document.getElementById("ma_tl").value = "";

        // xóa nhãn tên file hiện tại (nếu có)
        const fileNameLabel = document.getElementById("ten_file_hien_tai");
        if (fileNameLabel) fileNameLabel.textContent = "";
    }
}



function closeTaiLieuModal() {
    document.getElementById("taiLieuModal").classList.add("hidden");
}
