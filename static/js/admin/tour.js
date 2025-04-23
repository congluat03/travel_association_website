// Khai báo các biến toàn cục cần thiết
let tourImages = []; // Danh sách ảnh tour cũ
let selectedFilesTour = []; // Danh sách ảnh mới chọn từ máy
let deletedImagesTour = []; // Danh sách ảnh đã bị xóa
let allOriginalImagesTour = []; // Danh sách ảnh gốc từ DB (có thể dùng để xác định ảnh gốc)

function openTourModal(data = null) {
    const modal = document.getElementById("tourModal");
    const form = modal.querySelector("form"); // Lấy form bên trong modal
    const imagePreviewContainer = document.getElementById("tour-image-preview-container");
    const previewList = document.getElementById("tour-image-preview-list"); // Danh sách ảnh xem trước
    const fileInput = document.getElementById("HINH_TOUR"); // Input file hình ảnh

    // Hiển thị modal
    modal.classList.remove("hidden");

    // Reset các biến toàn cục liên quan đến ảnh
    selectedFilesTour = [];
    deletedImagesTour = [];

    // Xoá xem trước ảnh cũ
    previewList.innerHTML = "";

    if (data) {
        // Chế độ chỉnh sửa
        form.action = `/admin/tourism/tourdulich/sua/${data.ma_tour}/`;

        // Điền dữ liệu vào form
        document.getElementById("TEN_TOUR").value = data.ten_tour || "";
        document.getElementById("GIA_TOUR").value = data.gia_tour || "";
        document.getElementById("THOI_GIAN_DI_CHUYEN").value = data.thoi_gian || "";
        document.getElementById("MO_TA_TOUR").value = data.mo_ta || "";

        fileInput.value = ""; // Reset input file

        // Lấy hình ảnh gốc từ carousel (nếu có)
        const carousel = document.getElementById(`carousel-tour-${data.ma_tour}`);
        if (carousel) {
            const images = carousel.querySelectorAll("img");
            allOriginalImagesTour = Array.from(images).map(img => img.getAttribute("data-path") || img.src);
            tourImages = [...allOriginalImagesTour];
        }

        // Hiển thị ảnh xem trước nếu có
        if (allOriginalImagesTour.length > 0) {
            imagePreviewContainer.classList.remove("hidden");
            renderPreviewTour(); // Gọi hàm render ảnh
        }

    } else {
        // Chế độ thêm mới
        form.reset();
        form.action = `/admin/tourism/tourdulich/them/`;
        imagePreviewContainer.classList.add("hidden");
    }
}

document.getElementById("HINH_TOUR").addEventListener("change", function () {
    selectedFilesTour = Array.from(this.files);
    renderPreviewTour();
});

function renderPreviewTour() {
    const container = document.getElementById("tour-image-preview-list");
    const previewSection = document.getElementById("tour-image-preview-container");
    container.innerHTML = ""; // Xóa tất cả các ảnh trước khi render lại

    // Kiểm tra xem có ảnh nào để hiển thị hay không
    if (tourImages.length > 0 || selectedFilesTour.length > 0) {
        previewSection.classList.remove("hidden");
    } else {
        previewSection.classList.add("hidden");
    }

    // Render ảnh gốc (nếu có)
    tourImages.forEach((imagePath, index) => {
        const fileName = imagePath.split("/").pop();
        const wrapper = createImageWrapperTour(imagePath, fileName, () => {
            // Xóa ảnh khỏi danh sách giữ lại
            tourImages.splice(index, 1);

            // Nếu là ảnh gốc, thêm vào danh sách bị xóa
            if (allOriginalImagesTour.includes(imagePath)) {
                if (!deletedImagesTour.includes(fileName)) {
                    deletedImagesTour.push(fileName); // Thêm vào danh sách xóa
                }
            }

            renderPreviewTour();
        });
        container.appendChild(wrapper);
    });

    // Gửi danh sách ảnh giữ lại và ảnh đã xóa vào các trường ẩn
    document.getElementById("EXISTING_TOUR_IMAGES").value = tourImages.join(",");
    document.getElementById("DELETED_TOUR_IMAGES").value = deletedImagesTour.join(",");

    // Render ảnh mới (chưa có trong DB)
    selectedFilesTour.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function (e) {
            const wrapper = createImageWrapperTour(e.target.result, file.name, () => {
                selectedFilesTour.splice(index, 1); // Xóa ảnh khỏi danh sách đã chọn
                renderPreviewTour();
            });
            container.appendChild(wrapper);
        };
        reader.readAsDataURL(file);
    });
}

function createImageWrapperTour(src, name, onRemove) {
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
    removeBtn.className =
        "absolute -top-2 -right-2 bg-red-600 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm hover:bg-red-700 shadow-md";

    removeBtn.onclick = function () {
        // Xóa ảnh khỏi danh sách giữ lại và ảnh mới
        onRemove();

        // Nếu ảnh chưa xóa thì thêm vào danh sách xóa
        if (!deletedImagesTour.includes(name)) {
            deletedImagesTour.push(name);
        }

        // Cập nhật giá trị trường ẩn DELETED_TOUR_IMAGES
        document.getElementById("DELETED_TOUR_IMAGES").value = deletedImagesTour.join(",");
    };

    wrapper.appendChild(img);
    wrapper.appendChild(removeBtn);
    wrapper.appendChild(fileName);
    return wrapper;
}

let currentTourImageIndex = 0;
let tourImages1 = [];

// Mở modal và hiển thị tất cả các hình ảnh cùng thông tin cho từng tour
function openTourCarousel(maTour) {
  const carouselContainer = document.getElementById(`carousel-tour-${maTour}`);
  const images = carouselContainer.querySelectorAll('img');

  // Lấy danh sách các hình ảnh của tour
  tourImages1 = Array.from(images).map(img => img.src);
  currentTourImageIndex = 0;

  // Hiển thị chỉ 1 ảnh đầu tiên trong modal
  updateTourCarousel();

  // Mở modal với id 'tourCarouselModal'
  document.getElementById('tourCarouselModal').classList.remove('hidden');
}

// Đóng modal
function closeTourCarousel() {
  document.getElementById('tourCarouselModal').classList.add('hidden');
}

// Cập nhật ảnh trong carousel khi xem ảnh riêng biệt của tour
function updateTourCarousel() {
  const carouselImagesDiv = document.getElementById('tourCarouselImages');
  carouselImagesDiv.innerHTML = '';  // Xóa ảnh cũ

  // Tạo phần tử img mới và thiết lập nguồn
  const imgElement = document.createElement('img');
  imgElement.src = tourImages1[currentTourImageIndex];
  imgElement.alt = `Ảnh tour ${currentTourImageIndex + 1}`;
  imgElement.classList.add(
    'max-w-full',         // Đảm bảo ảnh không vượt quá chiều rộng modal
    'max-h-[80vh]',       // Đảm bảo ảnh không vượt quá chiều cao của modal
    'object-contain',     // Giữ tỷ lệ ảnh không bị méo và không bị cắt
    'rounded',
    'w-auto',             // Cho phép chiều rộng ảnh thay đổi tự động, giúp duy trì tỷ lệ gốc
    'h-auto'              // Cho phép chiều cao ảnh thay đổi tự động, giúp duy trì tỷ lệ gốc
  );

  // Tạo tên file
  const fileName = tourImages1[currentTourImageIndex].split('/').pop();
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
  const imageCountDiv = document.getElementById('tourImageCount');
  imageCountDiv.textContent = `Ảnh ${currentTourImageIndex + 1} / ${tourImages1.length}`;
}

// Chuyển ảnh trước
function prevTourImage() {
  currentTourImageIndex = (currentTourImageIndex - 1 + tourImages1.length) % tourImages1.length;
  updateTourCarousel();
}

// Chuyển ảnh tiếp theo
function nextTourImage() {
  currentTourImageIndex = (currentTourImageIndex + 1) % tourImages1.length;
  updateTourCarousel();
}
