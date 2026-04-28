from __future__ import annotations

import os
from pathlib import Path
from typing import Dict


class VideoProcessor:
    def __init__(self, temp_dir: str = "temp"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def analyze_video(self, video_path: str) -> Dict:
        if not os.path.exists(video_path):
            raise FileNotFoundError(video_path)
        # Lightweight mock-compatible metadata
        return {
            "path": video_path,
            "duration": 60.0,
            "fps": 30.0,
            "size": (1920, 1080),
            "aspect_ratio": 16 / 9,
            "has_audio": True,
        }

    def extract_audio(self, _video_path: str, output_path: str | None = None) -> str:
        out = Path(output_path) if output_path else self.temp_dir / "extracted_audio.wav"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.touch(exist_ok=True)
        return str(out)
