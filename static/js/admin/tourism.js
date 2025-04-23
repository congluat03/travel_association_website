




function closeModalDS() {
  const modal = document.getElementById("dacSanModal");
  const form = document.getElementById("dacSanForm");
  const imagePreviewList = document.getElementById("image-preview-list");
  const imagePreviewContainer = document.getElementById("image-preview-container");

  // 1. Ẩn modal
  modal.classList.add("hidden");

  // 2. Reset form
  form.reset();

  // 3. Xóa hình ảnh hiển thị trước đó
  imagePreviewList.innerHTML = "";
  imagePreviewContainer.classList.add("hidden");

  form.action = "";
}


let allOriginalImages = [];  // Danh sách ảnh từ DB
let dacSanImages1 = [];      // Danh sách ảnh giữ lại
let selectedFiles = [];      // Ảnh mới từ máy người dùng
let deletedImages2 = [];     // Ảnh gốc đã xóa (để gửi về server)

function openDacSanModal(data = null) {
  const modal = document.getElementById("dacSanModal");
  const form = document.getElementById("dacSanForm");
  const imagePreviewContainer = document.getElementById("image-preview-container");
  const imagePreviewList = document.getElementById("image-preview-list");
  const fileInput = document.getElementById("HINH_DS");

  modal.classList.remove("hidden");
  selectedFiles = [];
  allOriginalImages = [];
  dacSanImages1 = [];
  deletedImages2 = [];  // Reset danh sách ảnh xóa

  if (data) {
    form.action = `/admin/tourism/dacsan/sua/${data.ma_ds}/`;
    document.getElementById("TEN_DS").value = data.ten;
    document.getElementById("MA_DD").value = data.ma_dd;
    document.getElementById("MO_TA_DS").value = data.mo_ta;
    fileInput.value = "";

    const carouselContainer = document.getElementById(`carousel-${data.ma_ds}`);
    if (carouselContainer) {
      const images = carouselContainer.querySelectorAll('img');
      allOriginalImages = Array.from(images).map(img => img.getAttribute('data-path') || img.src);
      dacSanImages1 = [...allOriginalImages];
    }

    renderPreview();
  } else {
    form.reset();
    form.action = `/admin/tourism/dacsan/them/`;
    imagePreviewContainer.classList.add("hidden");
  }
}


document.getElementById("HINH_DS").addEventListener("change", function () {
  selectedFiles = Array.from(this.files);
  renderPreview();
});

function renderPreview() {
  const container = document.getElementById("image-preview-list");
  const previewSection = document.getElementById("image-preview-container");
  container.innerHTML = "";

  if (dacSanImages1.length > 0 || selectedFiles.length > 0) {
    previewSection.classList.remove("hidden");
  } else {
    previewSection.classList.add("hidden");
  }

  // Ảnh gốc còn giữ lại
  dacSanImages1.forEach((imagePath, index) => {
    const fileName = imagePath.split('/').pop();
    const wrapper = createImageWrapper(imagePath, fileName, () => {
      // Xóa ảnh khỏi danh sách giữ lại
      dacSanImages1.splice(index, 1);

      // Nếu là ảnh từ DB (gốc), thêm vào danh sách bị xóa
      if (allOriginalImages.includes(imagePath)) {
        if (!deletedImages2.includes(fileName)) {
          deletedImages2.push(fileName);  // Thêm vào danh sách xóa
        }
      }

      renderPreview();
    });
    container.appendChild(wrapper);
  });

  // Gửi danh sách ảnh giữ lại và ảnh đã xóa
  document.getElementById("EXISTING_IMAGES").value = dacSanImages1.join(',');
  document.getElementById("DELETED_IMAGES").value = deletedImages2.join(',');

  // Ảnh mới từ máy
  selectedFiles.forEach((file, index) => {
    const reader = new FileReader();
    reader.onload = function (e) {
      const wrapper = createImageWrapper(e.target.result, file.name, () => {
        selectedFiles.splice(index, 1);
        renderPreview();
      });
      container.appendChild(wrapper);
    };
    reader.readAsDataURL(file);
  });
}

function createImageWrapper(src, name, onRemove) {
  const wrapper = document.createElement("div");
  wrapper.className = "relative w-32";

  const img = document.createElement("img");
  img.src = src;
  img.className = "w-32 h-20 object-cover rounded-lg shadow";

  const fileName = document.createElement("p");
  fileName.className = "text-xs mt-1 text-center truncate text-gray-700";
  fileName.innerText = name;

  const removeBtn = document.createElement("button");
  removeBtn.type = "button";
  removeBtn.innerHTML = "&times;";
  removeBtn.className = "absolute -top-2 -right-2 bg-red-600 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm hover:bg-red-700 shadow-md";

  removeBtn.onclick = function() {
    // Xóa ảnh khỏi danh sách giữ lại
    onRemove();

    // Thêm ảnh vào danh sách xóa (DELETED_IMAGES)
    if (!deletedImages2.includes(name)) {
      deletedImages2.push(name);  // Thêm vào danh sách xóa
    }

    // Cập nhật giá trị của trường ẩn DELETED_IMAGES
    document.getElementById("DELETED_IMAGES").value = deletedImages2.join(',');
  };

  wrapper.appendChild(img);
  wrapper.appendChild(removeBtn);
  wrapper.appendChild(fileName);
  return wrapper;
}














function closeModalTour() {
  document.getElementById("tourModal").classList.add("hidden");
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




let currentImageIndex = 0;
let dacSanImages = [];

// Mở modal và hiển thị tất cả các hình ảnh cùng thông tin
function openCarousel(maDs) {
  const carouselContainer = document.getElementById(`carousel-${maDs}`);
  const images = carouselContainer.querySelectorAll('img');

  dacSanImages = Array.from(images).map(img => img.src);
  currentImageIndex = 0;

  // Hiển thị chỉ 1 ảnh đầu tiên
  updateCarousel();

  document.getElementById('carouselModal').classList.remove('hidden');
}

// Đóng modal
function closeCarousel() {
  document.getElementById('carouselModal').classList.add('hidden');
}

// Cập nhật ảnh trong carousel khi xem ảnh riêng biệt
function updateCarousel() {
  const carouselImagesDiv = document.getElementById('carouselImages');
  carouselImagesDiv.innerHTML = '';  // Xóa ảnh cũ

  // Tạo phần tử img mới và thiết lập nguồn
  const imgElement = document.createElement('img');
  imgElement.src = dacSanImages[currentImageIndex];
  imgElement.alt = `Ảnh đặc sản ${currentImageIndex + 1}`;
  imgElement.classList.add(
    'max-w-full',         // Đảm bảo ảnh không vượt quá chiều rộng modal
    'max-h-[80vh]',       // Đảm bảo ảnh không vượt quá chiều cao của modal
    'object-contain',     // Giữ tỷ lệ ảnh không bị méo và không bị cắt
    'rounded',
    'w-auto',             // Cho phép chiều rộng ảnh thay đổi tự động, giúp duy trì tỷ lệ gốc
    'h-auto'              // Cho phép chiều cao ảnh thay đổi tự động, giúp duy trì tỷ lệ gốc
  );

  // Tạo tên file
  const fileName = dacSanImages[currentImageIndex].split('/').pop();
  const imageNameDiv = document.createElement('div');
  imageNameDiv.classList.add('text-center', 'text-sm', 'mt-2');
  imageNameDiv.textContent = fileName;

  // Tạo một container chứa ảnh và tên file
  const imageWrapper = document.createElement('div');
  imageWrapper.classList.add('flex', 'flex-col', 'items-center', 'w-full', 'h-full', 'overflow-hidden');
  imageWrapper.appendChild(imgElement);
  imageWrapper.appendChild(imageNameDiv);

  carouselImagesDiv.appendChild(imageWrapper);

  // Cập nhật số lượng ảnh
  const imageCountDiv = document.getElementById('imageCount');
  imageCountDiv.textContent = `Ảnh ${currentImageIndex + 1} / ${dacSanImages.length}`;
}

// Chuyển ảnh trước
function prevImage() {
  currentImageIndex = (currentImageIndex - 1 + dacSanImages.length) % dacSanImages.length;
  updateCarousel();
}

// Chuyển ảnh tiếp theo
function nextImage() {
  currentImageIndex = (currentImageIndex + 1) % dacSanImages.length;
  updateCarousel();
}
