from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from main import AIVideoEditor

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

editor = AIVideoEditor(output_dir=str(OUTPUT_DIR))


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "ai-video-editor-backend"})


@app.post("/api/upload")
def upload_video():
    video = request.files.get("video")
    if not video:
        return jsonify({"success": False, "error": "No video file in request"}), 400

    safe_name = video.filename or "input_video.mp4"
    path = UPLOAD_DIR / safe_name
    video.save(path)

    result = editor.process_video(str(path))
    code = 200 if result.get("success") else 500
    return jsonify(result), code


@app.post("/api/command")
def command():
    payload = request.get_json(silent=True) or {}
    command_text = (payload.get("command") or "").strip()
    if not command_text:
        return jsonify({"success": False, "error": "Missing command"}), 400

    result = editor.chat_edit(command_text)
    code = 200 if result.get("success") else 400
    return jsonify(result), code


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)
