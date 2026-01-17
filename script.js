let videoLoaded = false;

function handleVideoImport(event) {
    const file = event.target.files[0];
    if (!file) return;

    videoLoaded = true;

    document.getElementById("videoFrame").innerHTML = `
        <p style="color:#4facfe; font-weight:600;">🎬 Video Loaded</p>
        <p style="color:#aaa; font-size:0.9em; margin-top:6px;">
            ${file.name}
        </p>
    `;

    document.getElementById("statusText").innerText = "Video Imported";
    document.getElementById("duration").innerText = "—";
}

function startProcessing() {
    if (!videoLoaded) {
        alert("Please import a video first!");
        return;
    }

    document.getElementById("statusText").innerText = "Processing...";
    document.getElementById("segmentCount").innerText = "0";
    document.getElementById("enhancementCount").innerText = "0";

    let segments = 0;
    let enhancements = 0;

    const interval = setInterval(() => {
        segments++;
        enhancements++;

        document.getElementById("segmentCount").innerText = segments;
        document.getElementById("enhancementCount").innerText = enhancements;

        if (segments >= 5) {
            clearInterval(interval);
            document.getElementById("statusext").innerText = "Processing Complete";
            document.getElementById("duration").innerText = "2:34";
        }
    }, 600);
}

function exportVideo() {
    if (!videoLoaded) {
        alert("No processed video to export!");
        return;
    }
    alert("⬇ Video exported successfully (demo)");
}

function sendCommand(commandText) {
    const input = document.getElementById("commandInput");
    const text = commandText || input.value.trim();
    if (!text) return;

    const chat = document.getElementById("chatMessages");

    chat.innerHTML += `
        <div class="message system">🧠 AI applied: "${text}"</div>
    `;

    input.value = "";
    chat.scrollTop = chat.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendCommand();
    }
}

