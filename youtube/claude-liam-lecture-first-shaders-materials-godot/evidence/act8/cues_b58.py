#!/usr/bin/env python3
"""cues_b58.py — recompute the CCPlainShell `lineCues` of B58 from the MEASURED audio length, and (with --write) patch lanes/act8.json.
Run from the reel folder AFTER audio exists, then re-run make_sheet.py:
    python3 evidence/act8/cues_b58.py            # print the 14 cues (frames at 30 fps)
    python3 evidence/act8/cues_b58.py --write    # patch lanes/act8.json
Rule (Remotion `at` cues must stay out of the 45-55 % window): the material-test block (lines 0-9) lands between 4 % and 40 % of the beat,
the calibration block (lines 10-13) between 60 % and 88 %, evenly spaced. At the 11.88 s estimate that puts 'an audit that expected' at 1.4 s,
the last FAIL line before 'four failures' (5.3 s), the second command at 7.1 s and the last comment on 'no declared type' (10.9 s)."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[2]
sheet = json.loads((HERE / "beat_sheet.json").read_text())
b = next(x for x in sheet["beats"] if x["beat_id"] == "B58")
T = float(b.get("actual_duration_s") or b["estimated_duration_s"])
FPS = 30
def space(a, z, n):
    return [round((a + (z - a) * i / (n - 1)) * T * FPS) for i in range(n)]
cues = space(0.04, 0.40, 10) + space(0.60, 0.88, 4)
lo, hi = 0.45 * T * FPS, 0.55 * T * FPS
assert not any(lo <= c <= hi for c in cues), "a cue falls in the 45-55 % window"
print("T =", T, "s; lineCues =", cues)
if "--write" in sys.argv:
    p = HERE / "lanes" / "act8.json"
    d = json.loads(p.read_text())
    d["B58"]["props"]["lineCues"] = cues
    p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    print("patched", p)
