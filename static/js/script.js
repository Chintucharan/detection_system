var slideshowDuration = 4000;
var slideshow = $('.main-content .slideshow');
var timeout;

// ---------------- SLIDE SWITCH ----------------
function slideshowSwitch(slideshow, index, auto) {

    if (!slideshow || slideshow.data('wait')) return;

    var slides = slideshow.find('.slide');
    var activeSlide = slides.filter('.is-active');
    var newSlide = slides.eq(index);

    if (newSlide.is(activeSlide)) return;

    var activeImage = activeSlide.find('.image-container');
    var newImage = newSlide.find('.image-container');
    var elements = newSlide.find('.caption > *');

    newSlide.addClass('is-new');

    clearTimeout(slideshow.data('timeout'));
    slideshow.data('wait', true);

    var transition = slideshow.attr('data-transition');

    // ---------------- FADE ----------------
    if (transition === 'fade') {

        newSlide.css({ display: 'block', zIndex: 2 });
        newImage.css({ opacity: 0 });

        TweenMax.to(newImage, 1, {
            alpha: 1,
            onComplete: function () {
                newSlide.addClass('is-active').removeClass('is-new');
                activeSlide.removeClass('is-active');

                slideshow.find('.pagination').trigger('check');
                slideshow.data('wait', false);

                if (auto) {
                    timeout = setTimeout(function () {
                        slideshowNext(slideshow, false, true);
                    }, slideshowDuration);
                    slideshow.data('timeout', timeout);
                }
            }
        });

    }

    // ---------------- SLIDE ANIMATION ----------------
    else {

        var direction = newSlide.index() > activeSlide.index();

        newSlide.css({
            display: 'block',
            width: 0,
            zIndex: 2
        });

        activeImage.css({ left: 0 });

        TweenMax.to(activeImage, 1, {
            left: direction ? -slideshow.width() / 4 : slideshow.width() / 4,
            ease: Power3.easeInOut
        });

        TweenMax.to(newSlide, 1, {
            width: slideshow.width(),
            ease: Power3.easeInOut
        });

        TweenMax.fromTo(elements, 0.8,
            { alpha: 0, y: 60 },
            { alpha: 1, y: 0, delay: 0.6, ease: Power3.easeOut }
        );

        setTimeout(function () {

            newSlide.addClass('is-active').removeClass('is-new');
            activeSlide.removeClass('is-active');

            slideshow.find('.pagination').trigger('check');
            slideshow.data('wait', false);

            if (auto) {
                timeout = setTimeout(function () {
                    slideshowNext(slideshow, false, true);
                }, slideshowDuration);
                slideshow.data('timeout', timeout);
            }

        }, 1000);
    }
}

// ---------------- NEXT / PREV ----------------
function slideshowNext(slideshow, previous, auto) {

    var slides = slideshow.find('.slide');
    var active = slides.filter('.is-active');
    var newSlide;

    if (previous) {
        newSlide = active.prev('.slide');
        if (!newSlide.length) newSlide = slides.last();
    } else {
        newSlide = active.next('.slide');
        if (!newSlide.length) newSlide = slides.first();
    }

    slideshowSwitch(slideshow, newSlide.index(), auto);
}

// ---------------- INIT ----------------
$(document).ready(function () {

    if (!slideshow.length) return;

    $('.slide').addClass('is-loaded');

    $('.slideshow .arrows .arrow').on('click', function () {
        slideshowNext(slideshow, $(this).hasClass('prev'));
    });

    $('.slideshow .pagination .item').on('click', function () {
        slideshowSwitch(slideshow, $(this).index());
    });

    $('.slideshow .pagination').on('check', function () {

        var pages = $(this).find('.item');
        var index = slideshow.find('.slide.is-active').index();

        pages.removeClass('is-active');
        pages.eq(index).addClass('is-active');
    });

    timeout = setTimeout(function () {
        slideshowNext(slideshow, false, true);
    }, slideshowDuration);

    slideshow.data('timeout', timeout);
});