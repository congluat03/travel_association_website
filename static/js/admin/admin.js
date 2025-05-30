function showTab(tabId, btn = null) {
  // Hide all tabs
  document.querySelectorAll(".tab-content").forEach((tab) => {
    tab.classList.add("hidden");
  });

  // Show selected tab
  document.getElementById(tabId).classList.remove("hidden");

  // Update tab buttons style
  document.querySelectorAll(".tab-btn").forEach((button) => {
    button.classList.remove("bg-green-600", "text-white");
    button.classList.add("bg-gray-100", "text-gray-700");
  });

  // Highlight current tab
  if (btn) {
    btn.classList.remove("bg-gray-100", "text-gray-700");
    btn.classList.add("bg-green-600", "text-white");
  } else {
    const activeBtn = document.getElementById(tabId + "-btn");
    if (activeBtn) {
      activeBtn.classList.remove("bg-gray-100", "text-gray-700");
      activeBtn.classList.add("bg-green-600", "text-white");
    }
  }
}
function toggleUserDropdown() {
  const menu = document.getElementById("user-dropdown-menu");
  menu.classList.toggle("hidden");
}

// Đóng dropdown nếu click ra ngoài
document.addEventListener("click", function (event) {
  const dropdown = document.getElementById("user-dropdown-menu");
  const button = document.querySelector(".dropdown-button");

  if (!dropdown.contains(event.target) && !button.contains(event.target)) {
    dropdown.classList.add("hidden");
  }
});
