#!/usr/bin/env python3
"""retime_cues.py [--check] — after the audio exists: scale the CCPlainShell cue frames of the six Remotion body beats
(B20, B21, B22, B48, B58, B71) from the ESTIMATED duration they were written against to the MEASURED audio duration.

Run it right after `make_sheet.py` (which rebuilds beat_sheet.json with the estimate-based cues and the measured durationSeconds), and again
every time make_sheet.py is re-run. It is idempotent: make_sheet.py always restores the estimate basis, and this script always scales from it.

  new_cue = round(old_cue * actual / estimated)        (a cue <= 0 means "on screen from frame 0" and is left alone)
Then: a cue that would land inside the 44-56 % window of the clip is moved to the nearer edge of the window (GATE T and Gate V sample the 50 % frame;
a spring that is half-way there reads as a blur), order among the non-zero cues is kept, and no cue is later than (clip frames - 12).
With --check it prints what it would change and writes nothing. It never touches the narration, the scenes or any other beat.
The beat's `props.lineCues` and `props.rings[].cue` are the only fields it writes (beat_sheet.json only; lanes/*.json keep the estimate basis)."""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FPS = 30
BEATS = ("B20", "B21", "B22", "B48", "B58", "B71")
check = "--check" in sys.argv
path = HERE / "beat_sheet.json"
sheet = json.loads(path.read_text())
changed = 0
for b in sheet["beats"]:
    if b["beat_id"] not in BEATS:
        continue
    actual, est = b.get("actual_duration_s"), b.get("estimated_duration_s")
    if not actual or not est:
        print(b["beat_id"], "no measured audio yet: left alone")
        continue
    props = b["shot"]["remotion"]["props"]
    dur = float(props["durationSeconds"])
    F = int(round(dur * FPS))
    ratio = float(actual) / float(est)
    lo, hi = int(0.44 * F), int(0.56 * F)

    def scale(c):
        if c <= 0:
            return c
        v = int(round(c * ratio))
        if lo <= v <= hi:
            v = lo - 1 if (v - lo) < (hi - v) else hi + 1
        return max(1, min(v, F - 12))

    old = list(props.get("lineCues", []))
    new, prev = [], 0
    for c in old:
        v = scale(c)
        if v > 0:
            v = max(v, prev)
            prev = v
        new.append(v)
    rings_old = [dict(r) for r in props.get("rings", [])]
    rings_new = [{"line": r["line"], "cue": max(scale(r["cue"]), (new[r["line"]] if r["line"] < len(new) else 0))} for r in rings_old]
    print(f"{b['beat_id']}: estimated {est} s, measured {actual} s (x{ratio:.3f}); clip {F} frames; window {lo}-{hi}")
    print("   lineCues", old, "->", new)
    if rings_old:
        print("   rings   ", [r["cue"] for r in rings_old], "->", [r["cue"] for r in rings_new])
    if not check:
        props["lineCues"] = new
        if rings_old:
            props["rings"] = rings_new
    changed += 1
if not check and changed:
    path.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
    print("beat_sheet.json updated for", changed, "beats")
elif check:
    print("(--check: nothing written)")
