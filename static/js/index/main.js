// Toggle dropdown menu
function toggleDropdown() {
    const menu = document.getElementById('dropdown-menu');
    const isHidden = menu.classList.contains('hidden');
    
    // Toggle visibility
    menu.classList.toggle('hidden');
    menu.classList.toggle('show');

    // Close other dropdowns if any (optional, for future expansion)
    document.querySelectorAll('.dropdown-menu').forEach((dropdown) => {
      if (dropdown !== menu && !dropdown.classList.contains('hidden')) {
        dropdown.classList.add('hidden');
        dropdown.classList.remove('show');
      }
    });
  }

  // Close dropdown when clicking outside
  document.addEventListener('click', function (event) {
    const dropdown = document.getElementById('dropdown-menu');
    const button = document.querySelector('.dropdown-button');
    if (!dropdown.contains(event.target) && !button.contains(event.target)) {
      dropdown.classList.add('hidden');
      dropdown.classList.remove('show');
    }
  });