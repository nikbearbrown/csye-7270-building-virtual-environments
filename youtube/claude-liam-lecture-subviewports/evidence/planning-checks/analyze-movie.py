#!/usr/bin/env python3
"""SubViewports film: reads the PNG frames Movie Maker wrote for a capture-scene rehearsal (run-movie-rehearsal.sh) and prints the numbers as RESULT lines.
Needs Pillow and numpy.   Modes:
  once DIR            scene c21 (Update Mode Once): the first teal pixel of the left and right pictures at chosen frames, against the formula
  first DIR_PREFIX id...   for each scene id, how many pixels differ from the stage colour in frames 0..7 (is frame 0 blank?)
  distinct DIR N      how many of the N written frames differ from the one before (a window that is not drawn leaves repeated frames)
"""
import hashlib, json, math, os, sys
from PIL import Image
import numpy as np

STAGE = np.array([0xD9, 0xD5, 0xCA])
TEAL = np.array([0x5F, 0xA3, 0x91])

def out(id_, d):
    d["id"] = id_
    print("RESULT " + json.dumps(d, sort_keys=True))

def frame(dir_, k):
    return f"{dir_}/f{k:08d}.png"

def first_teal_x(path, x0, x1, y0=104, y1=616):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    reg = a[y0:y1, x0:x1]
    m = (np.abs(reg - TEAL).max(axis=2) <= 8)
    cols = np.where(m.any(axis=0))[0]
    return int(cols[0]) if len(cols) else -1

def mode_once(d):
    left_edge = 0.30 * 448 * 0.6
    live = lambda t: max(256.0 + 150.0 * math.sin(0.9 * t) - left_edge, 0.0)
    rows = {}
    for f in (100, 200, 250, 254, 255, 256, 260, 300, 330, 360, 399):
        if not os.path.exists(frame(d, f)):
            continue
        rows[str(f)] = {"t": round(f / 30.0, 3), "left_first_teal_x": first_teal_x(frame(d, f), 100, 612), "left_by_formula": round(live(f / 30.0), 1), "right_first_teal_x": first_teal_x(frame(d, f), 668, 1180)}
    out("M1-c21-update-once-recorded-by-movie-maker", {"frames": rows, "right_frozen_by_formula_at_8.5_s": round(live(8.5), 1),
        "reading": "frame 255 is 8.5 s: from that frame on the right picture stays at the 8.5 s picture (323) while the left keeps following the sprite"})

def mode_first(prefix, ids):
    res = {}
    for sid in ids:
        counts = []
        for k in range(8):
            p = frame(f"{prefix}{sid}", k)
            if not os.path.exists(p):
                counts.append(None)
                continue
            a = np.asarray(Image.open(p).convert("RGB")).astype(int)
            counts.append(int((np.abs(a - STAGE).max(axis=2) > 8).sum()))
        res[sid] = counts
    blank0 = [s for s, c in res.items() if c[0] is not None and c[1] is not None and c[0] < 0.7 * c[1]]
    out("M2-first-frames-of-every-scene", {"pixels_that_differ_from_the_stage_colour_in_frames_0_to_7": res, "scenes_whose_frame_0_is_missing_most_of_frame_1": blank0,
        "reading": "a picture inside a SubViewport appears one draw after its texture is first used, so frame 0 of a recording can lack it: pre-roll one or two frames or drop frame 0"})

def mode_distinct(d, n):
    hs = []
    for k in range(n):
        p = frame(d, k)
        if not os.path.exists(p):
            break
        hs.append(hashlib.md5(open(p, "rb").read()).hexdigest())
    changes = sum(1 for i in range(1, len(hs)) if hs[i] != hs[i - 1])
    out("M3-frames-that-really-differ", {"directory": os.path.basename(d), "files_written": len(hs), "frames_that_differ_from_the_previous_one": changes,
        "reading": "files_written is what --quit-after asked for; a window that was not drawn leaves repeated frames, so the second number can be far smaller"})

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "once":
        mode_once(sys.argv[2])
    elif mode == "first":
        mode_first(sys.argv[2], sys.argv[3:])
    elif mode == "distinct":
        mode_distinct(sys.argv[2], int(sys.argv[3]))
