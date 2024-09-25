document.addEventListener("DOMContentLoaded", function () {
    var videoContainer = document.getElementById("video-container");
    var videoElement = document.getElementById("intro-video");
    var mainContent = document.getElementById("main-content");
    if (videoContainer && videoElement && mainContent) {
        // näita videokonteinerit ja mängi video
        videoContainer.style.display = "block"; // tegemist on block level elemendiga
        videoElement.play();
        // peida videokonteiner peale viite sekundit
        setTimeout(function () {
            videoContainer.style.display = "none";
            mainContent.style.display = "block"; // näita main contenti pärast timeouti
        }, 5000);
        // peida vidoekonteiner kui video lõppeb
        videoElement.addEventListener('ended', function () {
            videoContainer.style.display = 'none';
            mainContent.style.display = 'block';
        });
        // skipi video kui kasutaja klikib videol
        videoElement.addEventListener('click', function () {
            this.currentTime = this.duration;
        });
    }
});