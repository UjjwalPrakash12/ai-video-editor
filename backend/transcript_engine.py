from __future__ import annotations

from typing import Dict, List


class TranscriptEngine:
    def transcribe(self, _audio_path: str) -> Dict:
        text = (
            "Welcome to the AI video editor demo. "
            "This pipeline can segment speech, generate captions, and apply edits."
        )
        words: List[Dict] = []
        t = 0.0
        for token in text.split():
            dur = 0.25
            words.append({"word": token.strip(".,!?"), "start": t, "end": t + dur})
            t += dur + 0.05
        return {"text": text, "words": words, "segments": [], "language": "en"}

    def segment_content(self, transcript_data: Dict) -> List[Dict]:
        words = transcript_data.get("words", [])
        if not words:
            return []
        # Simple fixed-size segmentation
        segments = []
        step = 8
        for i in range(0, len(words), step):
            chunk = words[i : i + step]
            segments.append(
                {
                    "text": " ".join(w["word"] for w in chunk),
                    "words": chunk,
                    "start": chunk[0]["start"],
                    "end": chunk[-1]["end"],
                    "duration": chunk[-1]["end"] - chunk[0]["start"],
                }
            )
        return segments

    def detect_emphasis(self, segments: List[Dict]) -> List[Dict]:
        emphasis: List[Dict] = []
        for i, seg in enumerate(segments):
            if seg["words"]:
                emphasis.append(
                    {
                        "type": "sentence_start",
                        "segment_index": i,
                        "word_index": 0,
                        "word": seg["words"][0]["word"],
                        "start": seg["words"][0]["start"],
                        "end": seg["words"][0]["end"],
                        "intensity": 0.6,
                    }
                )
        return emphasis
