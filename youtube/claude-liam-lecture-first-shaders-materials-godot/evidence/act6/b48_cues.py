#!/usr/bin/env python3
"""b48_cues.py [seconds]  -- computes the CCPlainShell `lineCues` / `rings` frames for B48 from the beat's duration.
With no argument it reads beat_sheet.json (actual_duration_s if audio exists, else estimated_duration_s). Each line lands at the character share of the
narration phrase it goes with (minus a lead), lines keep their order, and no landing falls inside the 45-55 % window of the clip (a Remotion cue there is sampled
by GATE T / Gate V mid-spring). Prints JSON for the lane's props. Run again after audio exists and paste the result into lanes/act6.json and beat_sheet.json."""
import json, sys
from pathlib import Path
REEL = Path(__file__).resolve().parent.parent.parent
sheet = json.loads((REEL / "beat_sheet.json").read_text())
beat = next(b for b in sheet["beats"] if b["beat_id"] == "B48")
D = float(sys.argv[1]) if len(sys.argv) > 1 else float(beat.get("actual_duration_s") or beat["estimated_duration_s"])
narr = beat["narration_text"]; FPS = 30
F = int(D * FPS)
def at(phrase, lead=0.0):
    return int(round((D * narr.index(phrase) / len(narr) - lead) * FPS))
# (line index, cue frame or None = "after the previous one by N frames")
plan = [
    (0, 6),                                   # # no godot/.godot folder in this copy
    (1, at("reimport", 0.7)),                 # $ godot --headless --path godot --import
    (2, ("+", 8)),                            # ...
    (3, ("+", 8)),                            # [ DONE ] reimport
    (4, at("run again", 0.4)),                # $ ./scripts/run-test.sh test-material-contract.gd 60
    (5, ("+", 8)),                            # ...
    (6, ("+", 8)),                            # RESULT 53 checks / 0 failures / baseline
    (7, ("+", 6)),                            # # exit 0
    (8, at("Then delete source color", 0.9)), # # edit: source_color deleted from surface.gdshader line 3
    (9, at("The test must exit one", 1.0)),   # $ ./scripts/run-test.sh test-material-contract.gd 60  (after the midpoint window)
    (10, at("The test must exit one", 0.0)),  # FAIL matte color hint
    (11, ("+", 12)),                          # FAIL coated color hint
    (12, ("+", 12)),                          # RESULT 53 checks / 2 failures / baseline
    (13, at("one per material", 0.2)),        # # exit 1
]
cues = []
for i, c in plan:
    if isinstance(c, tuple):
        c = cues[-1] + c[1]
    if cues:
        c = max(c, cues[-1] + 6)
    cues.append(c)
lo, hi = int(0.44 * F), int(0.56 * F)
for k in range(len(cues)):
    if lo <= cues[k] <= hi:                   # move out of the mid-clip window, keep order
        cues[k] = hi + 2
        for j in range(k + 1, len(cues)):
            cues[j] = max(cues[j], cues[j - 1] + 8)
out = {"durationSeconds": D, "frames": F, "lineCues": cues, "rings": [{"line": 10, "cue": cues[12] + 4}, {"line": 11, "cue": cues[12] + 8}, {"line": 13, "cue": cues[13] + 2}],
       "window_45_55": [int(0.45 * F), int(0.55 * F)], "last_cue_pct": round(100 * cues[-1] / F, 1)}
print(json.dumps(out))
