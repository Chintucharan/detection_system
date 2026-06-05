$(function () {

    $('.carousel-item').eq(0).addClass('active');

    let total = $('.carousel-item').length;
    let current = 0;

    function setSlide(next) {
        if (next > total - 1) current = 0;
        else if (next < 0) current = total - 1;
        else current = next;

        $('.carousel-item').removeClass('active');
        $('.carousel-item').eq(current).addClass('active');

        console.log("Current Slide:", current);
    }

    $('#moveRight').on('click', function () {
        setSlide(current + 1);
    });

    $('#moveLeft').on('click', function () {
        setSlide(current - 1);
    });

});


// ---------------- SAFETY CHECKS ----------------
const quoteText = document.querySelector(".quote");
const quoteBtn = document.querySelector(".newQuote");
const authorName = document.querySelector(".name");

const speechBtn = document.querySelector(".speech");
const copyBtn = document.querySelector(".copy");
const twitterBtn = document.querySelector(".twitter");

const synth = window.speechSynthesis;


// ---------------- FETCH QUOTE ----------------
function fetchQuote() {

    if (!quoteText || !authorName || !quoteBtn) return;

    quoteBtn.classList.add("loading");
    quoteBtn.innerText = "Loading...";

    fetch("/get_quote")
        .then(res => res.json())
        .then(data => {

            quoteText.innerText = data.content;
            authorName.innerText = data.author;

            quoteBtn.classList.remove("loading");
            quoteBtn.innerText = "New Quote";
        })
        .catch(err => {
            console.error("Quote error:", err);
            quoteBtn.classList.remove("loading");
            quoteBtn.innerText = "Try Again";
        });
}


// ---------------- TEXT TO SPEECH ----------------
speechBtn?.addEventListener("click", () => {
    if (!quoteText) return;

    let utterance = new SpeechSynthesisUtterance(
        `${quoteText.innerText} by ${authorName.innerText}`
    );

    synth.cancel();
    synth.speak(utterance);
});


// ---------------- COPY ----------------
copyBtn?.addEventListener("click", () => {
    navigator.clipboard.writeText(
        `${quoteText.innerText} — ${authorName.innerText}`
    );
});


// ---------------- TWITTER ----------------
twitterBtn?.addEventListener("click", () => {
    let text = encodeURIComponent(
        `${quoteText.innerText} — ${authorName.innerText}`
    );

    window.open(`https://twitter.com/intent/tweet?text=${text}`, "_blank");
});


// ---------------- BUTTON ----------------
quoteBtn?.addEventListener("click", fetchQuote);