from __future__ import annotations

from typing import Dict, List


class CaptionGenerator:
    def create_captions(self, segments: List[Dict], emphasis_points: List[Dict]) -> List[Dict]:
        out: List[Dict] = []
        for i, seg in enumerate(segments):
            emphasized = {
                e.get("word_index")
                for e in emphasis_points
                if e.get("segment_index") == i and e.get("word_index") is not None
            }
            words = []
            for wi, w in enumerate(seg.get("words", [])):
                words.append(
                    {
                        "text": w["word"],
                        "start": w["start"],
                        "end": w["end"],
                        "style": {"color": "yellow" if wi in emphasized else "white", "font_size": 56},
                        "animation": {"type": "fade"},
                    }
                )
            out.append(
                {
                    "segment_index": i,
                    "text": seg["text"],
                    "start": seg["start"],
                    "end": seg["end"],
                    "words": words,
                    "display_mode": "word_by_word",
                }
            )
        return out
