const playPauseButton = document.getElementById('playPauseButton');
const audio = document.getElementById('song');
const refreshButton = document.getElementById("refresh-btn");

playPauseButton.addEventListener('click', function() {
    if (audio.paused) {
        audio.play();
        playPauseButton.innerHTML = '&#10074;&#10074;'; 
    } else {
        audio.pause();
        playPauseButton.innerHTML = '&#9658;';
    }
});

refreshButton.addEventListener("click", function() {
    audio.pause();
    audio.currentTime = 0;
    
    playPauseButton.innerHTML = '&#9658;';
});