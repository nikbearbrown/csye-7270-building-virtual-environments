#!/usr/bin/env python3
"""Write SHOTLIST.md from beat_sheet.json: what each beat shows, when, and where it came from.

    python3 tools/make_shotlist.py
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]


def main() -> None:
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    out = ["# SHOTLIST", "",
           f"Film `{sheet['metadata']['slug']}` · \"{sheet['metadata']['title']}\" · game source revision "
           f"{sheet['metadata']['game']['source_revision'][:7]}. Times are seconds into each beat, or the narration "
           "phrase a reveal is timed to. Sources: CAPTURE.md (takes and Blender stills), FACTCHECK.md (claims).", ""]
    total = 0.0
    for b in sheet["beats"]:
        d = float(b.get("actual_duration_s") or 0)
        total += d
        shot = b["shot"]
        rem = shot.get("remotion", {})
        kind = rem.get("pattern") or ("media/" + b["beat_id"] + ".mp4 (tools/build_media.py)")
        out.append(f"## {b['beat_id']} · {b['act']} · {d:.2f} s · {kind}")
        out.append("")
        out.append(b["role_note"])
        out.append("")
        for s in shot.get("show", []):
            out.append(f"- `{s['at']}` — {s['event']}")
        if shot.get("evidence_media"):
            out.append(f"- result media (hashed in gamedev-evidence.json): `{shot['evidence_media']}`")
        out.append("")
    out.append(f"Total: {len(sheet['beats'])} beats, {total:.1f} s.")
    (REEL / "SHOTLIST.md").write_text("\n".join(out) + "\n")
    print("SHOTLIST.md", len(sheet["beats"]), "beats", round(total, 1), "s")


if __name__ == "__main__":
    main()
