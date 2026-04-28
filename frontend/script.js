const API_BASE = "http://localhost:5001/api";

const videoInput = document.getElementById("videoInput");
const processBtn = document.getElementById("processBtn");
const statusText = document.getElementById("status");
const resultBox = document.getElementById("result");
const commandInput = document.getElementById("commandInput");
const sendBtn = document.getElementById("sendBtn");
const commandResult = document.getElementById("commandResult");

async function processVideo() {
  const file = videoInput.files?.[0];
  if (!file) {
    statusText.textContent = "Status: select a video first";
    return;
  }

  statusText.textContent = "Status: uploading + processing...";
  const form = new FormData();
  form.append("video", file);

  try {
    const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form });
    const json = await res.json();
    resultBox.textContent = JSON.stringify(json, null, 2);
    statusText.textContent = json.success ? "Status: processed" : "Status: failed";
  } catch (err) {
    statusText.textContent = "Status: backend unreachable";
    resultBox.textContent = String(err);
  }
}

async function sendCommand(textOverride) {
  const cmd = (textOverride || commandInput.value || "").trim();
  if (!cmd) return;
  try {
    const res = await fetch(`${API_BASE}/command`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: cmd }),
    });
    const json = await res.json();
    commandResult.textContent = JSON.stringify(json, null, 2);
  } catch (err) {
    commandResult.textContent = String(err);
  }
}

processBtn.addEventListener("click", processVideo);
sendBtn.addEventListener("click", () => sendCommand());
commandInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendCommand();
});
document.querySelectorAll("[data-cmd]").forEach((btn) => {
  btn.addEventListener("click", () => sendCommand(btn.getAttribute("data-cmd")));
});
