from __future__ import annotations

from pathlib import Path
from typing import Dict


class VideoRenderer:
    """
    Development renderer:
    writes a placeholder output file so the whole API flow works even without
    ffmpeg/moviepy runtime on local machines.
    """

    def render(self, composition: Dict, output_path: str | Path) -> str:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        summary = [
            "AI Video Editor Placeholder Output",
            f"source_video={composition.get('source_video', '')}",
            f"layers={len(composition.get('layers', []))}",
        ]
        out.write_text("\n".join(summary), encoding="utf-8")
        return str(out)
