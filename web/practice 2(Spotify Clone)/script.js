let songs = [];
let currentSongIndex = 0;
let isPlaying = false;

// ===== SELECT ELEMENTS =====
const audio = document.getElementById("audio-player");
const progress = document.querySelector(".progress");
const titleEl = document.querySelector(".music-title span");
const imageEl = document.querySelector(".album-mini img");
const currentTimeEl = document.getElementById("current-time");
const durationEl = document.getElementById("duration");
const playBtn = document.querySelector(".play");
const albumContainers = document.querySelectorAll(".album");

// ===== LOAD SONGS FROM JSON =====
async function loadSongs() {
    try {
        const response = await fetch("songs.json");
        songs = await response.json();

        renderCards();
        loadSong(0);

    } catch (error) {
        console.log("Error loading songs:", error);
    }
}

// ===== RENDER CARDS =====
function renderCards() {
    albumContainers.forEach(container => {
        container.innerHTML = "";

        songs.forEach((song, index) => {
            container.innerHTML += `
                <div class="card" onclick="playSongFromCard(${index})">
                    <div class="img-box">
                        <img src="${song.image}" class="img1" alt="${song.title}">
                        <img src="assests/play_musicbar.png" class="img2" alt="play">
                    </div>
                    <p class="card-title">${song.title}</p>
                    <p class="card-desc">${song.artist}</p>
                </div>
            `;
        });
    });
}

// ===== LOAD SONG =====
function loadSong(index) {
    const song = songs[index];

    audio.src = song.audio;
    titleEl.textContent = song.title;
    imageEl.src = song.image;

    progress.value = 0;
    currentTimeEl.textContent = "0:00";
}

// ===== PLAY SONG =====
function playSong(){
    audio.play();
    isPlaying = true;
    playBtn.src = "assests/pause.png";
}

function pauseSong(){
    audio.pause();
    isPlaying = false;
    playBtn.src = "assests/player_icon3.png";
}

// ===== PLAY FROM CARD =====
function playSongFromCard(index) {
    currentSongIndex = index;
    loadSong(index);
    playSong();
}

// ===== PLAY / PAUSE BUTTON =====
playBtn.addEventListener("click", () => {
    if (isPlaying) {
        pauseSong();
    } else {
        playSong();
    }
});

// ===== TIME FORMAT =====
function formatTime(seconds) {
    let min = Math.floor(seconds / 60);
    let sec = Math.floor(seconds % 60);

    return `${min}:${sec < 10 ? "0" + sec : sec}`;
}

// ===== UPDATE DURATION =====
audio.addEventListener("loadedmetadata", () => {
    durationEl.textContent = formatTime(audio.duration);
});

// ===== UPDATE PROGRESS =====
audio.addEventListener("timeupdate", () => {
    let percent = (audio.currentTime / audio.duration) * 100;

    progress.value = percent;

    progress.style.background =
        `linear-gradient(to right, white ${percent}%, #555 ${percent}%)`;

    currentTimeEl.textContent = formatTime(audio.currentTime);
});

// ===== DRAG PROGRESS BAR =====
progress.addEventListener("input", () => {
    audio.currentTime = (progress.value / 100) * audio.duration;
});

// ===== AUTO NEXT SONG =====
audio.addEventListener("ended", () => {
    currentSongIndex = (currentSongIndex + 1) % songs.length;
    loadSong(currentSongIndex);
    playSong();
});

// ===== NEXT BUTTON =====
document.querySelectorAll(".progress-bar img")[3].addEventListener("click", () => {
    currentSongIndex = (currentSongIndex + 1) % songs.length;
    loadSong(currentSongIndex);
    playSong();
});

// ===== PREVIOUS BUTTON =====
document.querySelectorAll(".progress-bar img")[1].addEventListener("click", () => {
    currentSongIndex =
        (currentSongIndex - 1 + songs.length) % songs.length;

    loadSong(currentSongIndex);
    playSong();
});

// ===== INITIAL LOAD =====
loadSongs();