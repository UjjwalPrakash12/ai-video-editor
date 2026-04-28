"""
Animation/decision layer for AI video editor.
This module keeps logic lightweight and deterministic so the API can run
without heavy model dependencies during development.
"""

from __future__ import annotations

from typing import Dict, List


class AnimationEngine:
    """Creates and mutates composition layers from transcript + commands."""

    def decide_enhancements(
        self,
        segments: List[Dict],
        emphasis_points: List[Dict],
        _video_info: Dict,
    ) -> List[Dict]:
        decisions: List[Dict] = []
        for i, seg in enumerate(segments):
            intensity = 0.4
            if any(e.get("segment_index") == i for e in emphasis_points):
                intensity = 0.8
            decisions.append(
                {
                    "id": f"seg-{i}",
                    "type": "segment_enhancement",
                    "start": seg["start"],
                    "end": seg["end"],
                    "intensity": intensity,
                }
            )
        return decisions

    def apply_animations(
        self,
        source_video: str,
        captions: List[Dict],
        edit_decisions: List[Dict],
    ) -> Dict:
        layers: List[Dict] = [{"type": "video", "data": {}, "z_index": 0}]
        for cap in captions:
            layers.append({"type": "caption", "data": cap, "z_index": 10})
        for dec in edit_decisions:
            layers.append({"type": "keyword_highlight", "data": dec, "z_index": 15})

        return {"source_video": source_video, "layers": layers}

    def apply_modifications(self, composition: Dict, modifications: List[Dict]) -> Dict:
        layers = composition.get("layers", [])
        for mod in modifications:
            action = mod.get("action")
            if action == "add":
                layer = mod.get("layer")
                if layer:
                    layers.append(layer)
            elif action == "remove":
                target = mod.get("target", {}).get("type")
                if target:
                    layers = [l for l in layers if l.get("type") != target]
            elif action == "modify_style":
                target = mod.get("target", {}).get("type")
                updates = mod.get("updates", {})
                for layer in layers:
                    if target and layer.get("type") != target:
                        continue
                    data = layer.setdefault("data", {})
                    style = data.setdefault("style", {})
                    style.update(updates)

        composition["layers"] = layers
        return composition
