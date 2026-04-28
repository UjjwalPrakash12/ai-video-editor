"""
AI-Driven Talking-Head Video Editor
Main orchestrator for processing + command-based refinement.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Optional

from animation_engine import AnimationEngine
from caption_generator_module import CaptionGenerator
from chat_interface_module import ChatInterface
from transcript_engine import TranscriptEngine
from video_processor import VideoProcessor
from video_renderer_module import VideoRenderer


class AIVideoEditor:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.video_processor = VideoProcessor()
        self.transcript_engine = TranscriptEngine()
        self.caption_generator = CaptionGenerator()
        self.animation_engine = AnimationEngine()
        self.chat_interface = ChatInterface()
        self.video_renderer = VideoRenderer()

        self.current_video_path: Optional[str] = None
        self.transcript_data: Optional[Dict] = None
        self.edit_decisions = []
        self.final_composition: Optional[Dict] = None

    def process_video(self, video_path: str) -> Dict:
        if not os.path.exists(video_path):
            return {"success": False, "error": f"File not found: {video_path}"}

        video_info = self.video_processor.analyze_video(video_path)
        audio_path = self.video_processor.extract_audio(video_path)
        self.transcript_data = self.transcript_engine.transcribe(audio_path)
        segments = self.transcript_engine.segment_content(self.transcript_data)
        emphasis = self.transcript_engine.detect_emphasis(segments)
        captions = self.caption_generator.create_captions(segments, emphasis)
        self.edit_decisions = self.animation_engine.decide_enhancements(
            segments, emphasis, video_info
        )
        self.final_composition = self.animation_engine.apply_animations(
            video_path, captions, self.edit_decisions
        )
        output_path = self.video_renderer.render(
            self.final_composition, self.output_dir / "edited_video.mp4"
        )
        self.current_video_path = video_path

        return {
            "success": True,
            "output_path": str(output_path),
            "segments": len(segments),
            "enhancements_applied": len(self.edit_decisions),
            "transcript_preview": (self.transcript_data.get("text", "")[:240] if self.transcript_data else ""),
        }

    def chat_edit(self, command: str) -> Dict:
        if not self.final_composition or not self.transcript_data:
            return {"success": False, "error": "No processed video. Upload/process first."}

        modifications = self.chat_interface.parse_command(
            command, self.transcript_data, self.edit_decisions
        )
        self.final_composition = self.animation_engine.apply_modifications(
            self.final_composition, modifications
        )
        output_path = self.video_renderer.render(
            self.final_composition, self.output_dir / "edited_video_modified.mp4"
        )
        return {
            "success": True,
            "modifications": modifications,
            "output_path": str(output_path),
        }
