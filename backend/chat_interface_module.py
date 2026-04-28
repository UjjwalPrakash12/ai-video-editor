from __future__ import annotations

import re
from typing import Dict, List


class ChatInterface:
    def parse_command(self, command: str, transcript_data: Dict, edit_decisions: List[Dict]) -> List[Dict]:
        cmd = command.lower().strip()
        if re.search(r"bold|bolder", cmd):
            return [
                {
                    "action": "modify_style",
                    "target": {"type": "caption"},
                    "updates": {"font_size": 72, "stroke_width": 3},
                    "description": "Made captions bolder",
                }
            ]
        if match := re.search(r"(?:change|make).*color.*to\s+(\w+)", cmd):
            color = match.group(1)
            return [
                {
                    "action": "modify_style",
                    "target": {"type": "caption"},
                    "updates": {"color": color},
                    "description": f"Changed caption color to {color}",
                }
            ]
        if "add title" in cmd:
            text = " ".join(transcript_data.get("text", "").split()[:5]).upper() or "VIDEO TITLE"
            return [
                {
                    "action": "add",
                    "layer": {
                        "type": "title",
                        "z_index": 20,
                        "data": {
                            "text": text,
                            "start": 0.5,
                            "end": 3.5,
                            "position": "center",
                            "style": {"font_size": 72, "color": "white"},
                            "animation": {"type": "fade"},
                        },
                    },
                    "description": "Added title",
                }
            ]
        return [{"action": "none", "description": f'No parser rule matched: "{command}"'}]
