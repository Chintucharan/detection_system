document.addEventListener("DOMContentLoaded", () => {

    let slideIndex = 0;
    const slides = document.querySelectorAll(".motivation-slide");

    const nextBtn = document.getElementById("nextSlide");
    const prevBtn = document.getElementById("prevSlide");

    if (!slides.length || !nextBtn || !prevBtn) return;

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove("active"));
        slides[index].classList.add("active");
    }

    function changeSlide(direction) {
        slideIndex = (slideIndex + direction + slides.length) % slides.length;
        showSlide(slideIndex);
    }

    nextBtn.addEventListener("click", () => changeSlide(1));
    prevBtn.addEventListener("click", () => changeSlide(-1));

    // ---------------- SAFE AUTO SLIDE ----------------
    let autoSlide;

    function startAutoSlide() {
        autoSlide = setInterval(() => {
            changeSlide(1);
        }, 5000);
    }

    function stopAutoSlide() {
        clearInterval(autoSlide);
    }

    startAutoSlide();

    const container = document.querySelector(".motivation-carousel");

    if (container) {
        container.addEventListener("mouseenter", stopAutoSlide);
        container.addEventListener("mouseleave", startAutoSlide);
    }

});