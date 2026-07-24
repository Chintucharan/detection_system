let lastPlayTime = 0;
const COOLDOWN = 2000;

function playAlarm() {
    const audio = document.getElementById("alarmSound");
    if (!audio) return;

    audio.currentTime = 0;
    audio.play().catch(err => {
        console.log("Audio blocked until click:", err);
    });
}

// optional: unlock audio on first click (IMPORTANT)
document.addEventListener("click", () => {
    const audio = document.getElementById("alarmSound");
    if (audio) {
        audio.play().then(() => {
            audio.pause();
            audio.currentTime = 0;
        }).catch(() => {});
    }
}, { once: true });

// poll backend
setInterval(() => {

    fetch("/status", {
        cache: "no-store"
    })
    .then(res => res.json())
    .then(data => {

        const now = Date.now();

        if (now - lastPlayTime < COOLDOWN) return;

        // Flask key = "alarm"
        if (data.alarm === true) {

            playAlarm();
            lastPlayTime = now;

            console.log("ALARM TYPE:", data.type);
        }

    })
    .catch(err => {
        console.log("Status error:", err);
    });

}, 1000);