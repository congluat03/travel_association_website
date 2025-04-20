// Hàm này sẽ được gọi khi trạng thái checkbox thay đổi
function toggleTinNoiBat() {
  const checkbox = document.getElementById("tin_noi_bat");
  const statusOff = document.getElementById("status-off");
  const statusOn = document.getElementById("status-on");
  const background = document.getElementById("toggle-background");
  const dot = document.getElementById("dot");

  if (checkbox.checked) {
    background.style.backgroundColor = "#4CAF50"; // Màu xanh khi bật
    dot.style.transform = "translateX(28px)"; // Di chuyển dot sang phải

    statusOff.classList.remove("font-bold", "text-red-600");
    statusOn.classList.add("font-bold", "text-green-700");
  } else {
    background.style.backgroundColor = "#D1D5DB"; // Màu xám khi tắt
    dot.style.transform = "translateX(0)"; // Di chuyển dot về vị trí ban đầu

    statusOn.classList.remove("font-bold", "text-green-700");
    statusOff.classList.add("font-bold", "text-red-600");
  }
}

function updateSelectedTags() {
  const checkboxes = document.querySelectorAll('input[name="MA_TAG"]:checked');
  const selectedTagsContainer = document.getElementById("selected_tags");

  selectedTagsContainer.innerHTML = "";

  checkboxes.forEach((cb) => {
    const label = document.querySelector(`label[for="${cb.id}"]`);
    if (label) {
      const span = document.createElement("span");
      span.className =
        "px-3 py-1 rounded-full bg-green-100 text-green-700 text-sm shadow-sm";
      span.textContent = label.textContent;
      selectedTagsContainer.appendChild(span);
    }
  });
}

function openTagModal(data = null) {
  const modal = document.getElementById("tagModal");
  modal.classList.remove("hidden");

  const form = modal.querySelector("form"); // Lấy form bên trong modal

  if (data) {
    // Gán URL sửa nếu có thẻ tag
    form.action = `/admin/news/thetag/sua/${data.ma_tag}/`; // Duy trì ma_tag trong URL nhưng không điền vào form

    // Điền dữ liệu vào các input
    document.getElementById("ten_tag").value = data.ten_tag || ""; // Tên thẻ tag
    document.getElementById("mo_ta_tag").value = data.mo_ta_tag || ""; // Mô tả thẻ tag
  } else {
    // Gán URL thêm mới và reset form
    form.action = `/admin/news/thetag/them/`;
    form.reset(); // Reset form để thêm mới
  }
}

function closeModalTag() {
  document.getElementById("tagModal").classList.add("hidden");
}

function openNewsModal(data = null) {
  const modal = document.getElementById("newsModal");
  modal.classList.remove("hidden");

  const form = modal.querySelector("form");

  // Gán lại các field cơ bản khi sửa
  if (data) {
    form.action = `/admin/news/tintuc/sua/${data.ma_tin}/`;
    document.getElementById("tieu_de").value = data.tieu_de || "";
    document.getElementById("ngay_dang").value = data.ngay_dang || "";
    document.getElementById("loai_tin_tuc").value = data.loai || "";
    document.getElementById("noi_dung").value = data.noi_dung || "";
    document.getElementById("tin_noi_bat").checked = data.tin_noi_bat || false;

    // Hiển thị tài khoản liên quan đến tin tức
    document.getElementById("ma_tk").value = data.ma_tk || ""; // Thêm phần nhập tài khoản

    // Đặt lại tất cả checkbox về unchecked
    document
      .querySelectorAll('input[name="MA_TAG"]')
      .forEach((cb) => (cb.checked = false));

    // Nếu có thẻ tag liên quan thì set checked
    const selectedTagsContainer = document.getElementById("selected_tags");
    selectedTagsContainer.innerHTML = ""; // Reset vùng hiển thị thẻ đã chọn

    data.ma_tag.forEach((tag) => {
      // Set checked nếu tồn tại
      const checkbox = document.getElementById(`tag_${tag.pk}`);
      if (checkbox) checkbox.checked = true;

      // Hiện thị ra vùng đã chọn
      const span = document.createElement("span");
      span.className =
        "px-3 py-1 rounded-full bg-green-100 text-green-700 text-sm shadow-sm";
      span.textContent = tag.ten_tag;
      selectedTagsContainer.appendChild(span);
    });
  } else {
    // Nếu không có dữ liệu, thì form được thiết lập cho thêm mới
    form.action = `/admin/news/tintuc/them/`;
    form.reset();

    // Reset checkbox
    document
      .querySelectorAll('input[name="MA_TAG"]')
      .forEach((cb) => (cb.checked = false));

    // Xóa thẻ tag đã chọn
    document.getElementById("selected_tags").innerHTML = "";

    // Reset tài khoản
    document.getElementById("ma_tk").value = ""; // Reset tài khoản khi thêm mới
  }
}

function closeModalNews() {
  document.getElementById("newsModal").classList.add("hidden");
}
