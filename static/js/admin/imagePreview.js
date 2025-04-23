let allOriginalImagesDD = []; // Danh sách ảnh từ DB (địa điểm du lịch)
let diaDiemImages = []; // Danh sách ảnh giữ lại (địa điểm du lịch)
let selectedFilesDD = []; // Ảnh mới từ máy người dùng (địa điểm du lịch)
let deletedImagesDD = []; // Danh sách ảnh đã xóa (địa điểm du lịch)

function openModal(data = null) {
    const modal = document.getElementById("diaDiemModal");
    const form = document.getElementById("diaDiemForm");
    const fileInput = document.getElementById("HINH_ANH_DD");
    const previewContainer = document.getElementById("image-preview-container-dd");
    const previewList = document.getElementById("image-preview-list-dd");

    // Hiển thị modal
    modal.classList.remove("hidden");

    // Reset các biến toàn cục liên quan đến ảnh
    allOriginalImagesDD = [];
    diaDiemImages = [];
    selectedFilesDD = [];
    deletedImagesDD = [];

    // Xoá xem trước ảnh cũ
    previewList.innerHTML = "";

    if (data) {
        // Chế độ chỉnh sửa
        form.action = `/admin/tourism/diadiem/sua/${data.ma_dd}/`;

        // Điền dữ liệu vào form
        form.TEN_DIA_DIEM.value = data.ten || "";
        form.MA_DN.value = data.ma_dn || "";
        form.TINH_THANH_PHO.value = data.tinh_tp || "";
        form.QUAN_HUYEN.value = data.quan_huyen || "";
        form.KHU_VUC.value = data.khu_vuc || "";
        form.VI_TRI.value = data.vi_tri || "";
        form.MO_TA_DD.value = data.mo_ta || "";

        fileInput.value = ""; // Reset input file

        // Lấy hình ảnh gốc từ carousel (nếu có)
        const carousel = document.getElementById(`carousel-dd-${data.ma_dd}`);
        if (carousel) {
            const images = carousel.querySelectorAll("img");
            allOriginalImagesDD = Array.from(images).map(img => img.getAttribute("data-path") || img.src);
            diaDiemImages = [...allOriginalImagesDD];
           
        }

        // Hiển thị ảnh xem trước nếu có
        if (allOriginalImagesDD.length > 0) {
            previewContainer.classList.remove("hidden");
            renderPreviewDD(); // Gọi hàm render ảnh
        }

    } else {
        // Chế độ thêm mới
        form.reset();
        form.action = `/admin/tourism/diadiem/them/`;
        previewContainer.classList.add("hidden");
    }
}



function closeModal() {
    document.getElementById("diaDiemModal").classList.add("hidden");
}
document.getElementById("HINH_ANH_DD").addEventListener("change", function () {
    selectedFilesDD = Array.from(this.files);
    renderPreviewDD();
});

function renderPreviewDD() {
    const container = document.getElementById("image-preview-list-dd");
    const previewSection = document.getElementById("image-preview-container-dd");
    container.innerHTML = "";

    if (diaDiemImages.length > 0 || selectedFilesDD.length > 0) {
        previewSection.classList.remove("hidden");
    } else {
        previewSection.classList.add("hidden");
    }

    // Ảnh gốc còn giữ lại
    diaDiemImages.forEach((imagePath, index) => {
        const fileName = imagePath.split("/").pop();
        const wrapper = createImageWrapperDD(imagePath, fileName, () => {
            // Xóa ảnh khỏi danh sách giữ lại
            diaDiemImages.splice(index, 1);

            // Nếu là ảnh từ DB (gốc), thêm vào danh sách bị xóa
            if (allOriginalImagesDD.includes(imagePath)) {
                if (!deletedImagesDD.includes(fileName)) {
                    deletedImagesDD.push(fileName); // Thêm vào danh sách xóa
                }
            }

            renderPreviewDD();
        });
        container.appendChild(wrapper);
    });

    // Gửi danh sách ảnh giữ lại và ảnh đã xóa
    document.getElementById("EXISTING_IMAGES_DD").value = diaDiemImages.join(",");
    document.getElementById("DELETED_IMAGES_DD").value =
        deletedImagesDD.join(",");

    // Ảnh mới từ máy
    selectedFilesDD.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function (e) {
            const wrapper = createImageWrapperDD(e.target.result, file.name, () => {
                selectedFilesDD.splice(index, 1);
                renderPreviewDD();
            });
            container.appendChild(wrapper);
        };
        reader.readAsDataURL(file);
    });
}

function createImageWrapperDD(src, name, onRemove) {
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
        // Xóa ảnh khỏi danh sách giữ lại
        onRemove();

        // Thêm ảnh vào danh sách xóa (DELETED_IMAGES_DD)
        if (!deletedImagesDD.includes(name)) {
            deletedImagesDD.push(name); // Thêm vào danh sách xóa
        }

        // Cập nhật giá trị của trường ẩn DELETED_IMAGES_DD
        document.getElementById("DELETED_IMAGES_DD").value =
            deletedImagesDD.join(",");
    };

    wrapper.appendChild(img);
    wrapper.appendChild(removeBtn);
    wrapper.appendChild(fileName);
    return wrapper;
}

let currentDiaDiemImageIndex = 0;
let diaDiemImages1 = [];

// Mở modal
function openDiaDiemModal1(maDiaDiem) {
    // Đúng id: carousel-dd-{{ dia_diem.MA_DD }}
    const container = document.getElementById(`carousel-${maDiaDiem}`);
    if (!container) {
        alert("Không tìm thấy ảnh cho địa điểm này.");
        return;
    }

    const imgElements = container.querySelectorAll("img");
    if (imgElements.length === 0) {
        alert("Địa điểm này không có ảnh.");
        return;
    }

    // Lưu mảng ảnh
    diaDiemImages1 = Array.from(imgElements).map((img) => img.src);
    currentDiaDiemImageIndex = 0;

    updateDiaDiemCarousel();
    document.getElementById("diaDiemModal1").classList.remove("hidden");
}


// Đóng modal
function closeDiaDiemModal() {
    document.getElementById("diaDiemModal1").classList.add("hidden");
}

// Cập nhật ảnh
function updateDiaDiemCarousel() {
    const imageDiv = document.getElementById("diaDiemCarouselImages");
    imageDiv.innerHTML = "";

    const img = document.createElement("img");
    img.src = diaDiemImages1[currentDiaDiemImageIndex];
    img.alt = `Ảnh địa điểm ${currentDiaDiemImageIndex + 1}`;
    img.classList.add(
        "max-w-full",
        "max-h-[80vh]",
        "object-contain",
        "rounded",
        "w-auto",
        "h-auto"
    );

    const fileName = diaDiemImages1[currentDiaDiemImageIndex].split("/").pop();
    const caption = document.createElement("div");
    caption.classList.add("text-center", "text-sm", "mt-2");
    caption.textContent = fileName;

    const wrapper = document.createElement("div");
    wrapper.classList.add(
        "flex",
        "flex-col",
        "items-center",
        "w-full",
        "h-full",
        "overflow-hidden"
    );
    wrapper.appendChild(img);
    wrapper.appendChild(caption);

    imageDiv.appendChild(wrapper);

    const countDiv = document.getElementById("diaDiemImageCount");
    countDiv.textContent = `Ảnh ${currentDiaDiemImageIndex + 1} / ${diaDiemImages1.length
        }`;
}

// Lùi lại
function prevDiaDiemImage() {
    currentDiaDiemImageIndex =
        (currentDiaDiemImageIndex - 1 + diaDiemImages1.length) %
        diaDiemImages1.length;
    updateDiaDiemCarousel();
}

// Tiếp theo
function nextDiaDiemImage() {
    currentDiaDiemImageIndex =
        (currentDiaDiemImageIndex + 1) % diaDiemImages1.length;
    updateDiaDiemCarousel();
}
