// Swiper JS tối giản
document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM loaded, initializing custom Swiper...');

    const swiperContainer = document.querySelector('.swiper-container');
    const swiperWrapper = swiperContainer.querySelector('.swiper-wrapper');
    const slides = swiperWrapper.querySelectorAll('.swiper-slide');
    const pagination = swiperContainer.querySelector('.swiper-pagination');
    const prevButton = swiperContainer.querySelector('.swiper-button-prev');
    const nextButton = swiperContainer.querySelector('.swiper-button-next');

    if (!slides.length) {
        console.error('No slides found.');
        return;
    }

    let currentIndex = 0;
    const totalSlides = slides.length;
    let autoplayInterval;

    // Tạo pagination bullets
    function createPagination() {
        pagination.innerHTML = '';
        for (let i = 0; i < totalSlides; i++) {
            const bullet = document.createElement('span');
            bullet.classList.add('swiper-pagination-bullet');
            if (i === currentIndex) bullet.classList.add('swiper-pagination-bullet-active');
            bullet.addEventListener('click', () => {
                currentIndex = i;
                updateSwiper();
                resetAutoplay();
            });
            pagination.appendChild(bullet);
        }
    }

    // Cập nhật trạng thái Swiper
    function updateSwiper() {
        // Cập nhật vị trí slide
        swiperWrapper.style.transform = `translateX(-${currentIndex * 100}%)`;

        // Cập nhật pagination
        const bullets = pagination.querySelectorAll('.swiper-pagination-bullet');
        bullets.forEach((bullet, index) => {
            bullet.classList.toggle('swiper-pagination-bullet-active', index === currentIndex);
        });

        // Ẩn/hiện nút prev/next
        prevButton.style.display = currentIndex === 0 ? 'none' : 'block';
        nextButton.style.display = currentIndex === totalSlides - 1 ? 'none' : 'block';
    }

    // Chuyển slide tiếp theo
    function nextSlide() {
        if (currentIndex < totalSlides - 1) {
            currentIndex++;
            updateSwiper();
        } else if (swiperContainer.dataset.loop === 'true') {
            currentIndex = 0;
            updateSwiper();
        }
    }

    // Chuyển slide trước đó
    function prevSlide() {
        if (currentIndex > 0) {
            currentIndex--;
            updateSwiper();
        } else if (swiperContainer.dataset.loop === 'true') {
            currentIndex = totalSlides - 1;
            updateSwiper();
        }
    }

    // Tự động chuyển slide
    function startAutoplay() {
        const delay = parseInt(swiperContainer.dataset.autoplayDelay) || 5000;
        autoplayInterval = setInterval(nextSlide, delay);
    }

    // Reset autoplay khi người dùng tương tác
    function resetAutoplay() {
        clearInterval(autoplayInterval);
        startAutoplay();
    }

    // Thêm sự kiện cho nút prev/next
    nextButton.addEventListener('click', () => {
        nextSlide();
        resetAutoplay();
    });

    prevButton.addEventListener('click', () => {
        prevSlide();
        resetAutoplay();
    });

    // Khởi tạo Swiper
    swiperContainer.dataset.loop = 'true'; // Kích hoạt loop
    swiperContainer.dataset.autoplayDelay = '5000'; // Autoplay delay 5 giây
    createPagination();
    updateSwiper();
    startAutoplay();

    console.log('Custom Swiper initialized successfully.');
});