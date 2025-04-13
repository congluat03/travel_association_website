
// ===============================
// 📌 Hàm hiển thị tab tương ứng
// ===============================
function showTab(tabId, btn) {
    document.querySelectorAll(".tab-content").forEach((tab) => {
      tab.classList.add("hidden");
    });
    document.getElementById(tabId).classList.remove("hidden");
  
    const buttons = document.querySelectorAll(".tab-btn");
    buttons.forEach((button) => {
      button.classList.remove("bg-green-600", "text-white");
      button.classList.add("bg-gray-100", "text-gray-700");
    });
  
    btn.classList.remove("bg-gray-100", "text-gray-700");
    btn.classList.add("bg-green-600", "text-white");
  }
  