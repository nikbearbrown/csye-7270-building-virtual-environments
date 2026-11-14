"""Assignment 7, prompt 8 step 5: the run cycle's seam and registration from the windowed Movie Maker fixture capture.

Reads captures/run/game-r2-seam/ticks.jsonl (tests/capture_run_seam.gd, --fixed-fps 30: two physics ticks per movie
frame; movie frame m shows tick 2m - 1, read from the harness label) and the movie frames in MOVIE_DIR (not committed).
Writes into captures/run/game-r2-seam/:
  - one movie frame per cycle frame (cell) for two wraps: c<cycle>-cell<k>-tick<t>.png (640x360, as captured);
  - strip.png: every movie frame across those two wraps and the next wrap, cropped around the mage at 3x, labelled;
  - seam.json: per-tick cell runs, ticks and movie frames per cell per cycle, every wrap, repeats, and registration
    (the Sprite2D offset and position on every RUN tick; per cell of the sheet: lowest opaque row, feet span on that
    row, torso centroid, top row).
Usage, from assignment-7/: python -I walker-magic-zhefan/tools/measure_run_seam.py <MOVIE_DIR>
"""
import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]          # assignment-7/
OUT = ROOT / "captures/run/game-r2-seam"
SHEET = ROOT / "walker-magic-zhefan/assets/sprites/mage/mage_run_cycle_sheet.png"
CELL_W, CELL_H, CELLS = 62, 69, 4
OFFSET = (-31, -67)                                 # Sprite2D offset: the feet anchor at (31, 67) in each cell
TORSO_ROWS = (28, 50)                               # cell rows of the robe body, below the arms' reach of the hat


def movie_frame_for(tick):
    return (tick + 1) // 2 if tick % 2 == 1 else None


def main(movie_dir):
    rows = [json.loads(l) for l in (OUT / "ticks.jsonl").read_text().splitlines() if l.strip()]
    run = [r for r in rows if r["state"] == "RUN"]
    runs = []
    for r in run:
        if runs and runs[-1]["cell"] == r["frame"]:
            runs[-1]["ticks"] += 1
        else:
            runs.append({"cell": r["frame"], "first_tick": r["tick"], "ticks": 1})
    # Cycles start at each run of cell 0; the last, cut short by the key release, is dropped.
    cycles, cur = [], []
    for rn in runs:
        if rn["cell"] == 0 and cur:
            cycles.append(cur)
            cur = []
        cur.append(rn)
    complete = [c for c in cycles if [x["cell"] for x in c] == [0, 1, 2, 3]]
    for c in complete:
        for rn in c:
            ticks = range(rn["first_tick"], rn["first_tick"] + rn["ticks"])
            rn["movie_frames"] = [movie_frame_for(t) for t in ticks if movie_frame_for(t) is not None]
    wraps = []
    for a, b in zip(runs, runs[1:]):
        if b["cell"] == 0:
            wraps.append({"tick": b["first_tick"], "from_cell": a["cell"], "to_cell": b["cell"],
                          "ticks_of_cell_before": a["ticks"], "ticks_of_cell_after": b["ticks"]})
    repeats = [w for w in wraps if w["from_cell"] == w["to_cell"] or w["from_cell"] != 3]
    in_cycle_repeats = [c for c in cycles if len({x["cell"] for x in c}) != len(c)]

    # Movie frames per cell at 30 fps, per complete cycle.
    frames_per_cell = [[len(rn["movie_frames"]) for rn in c] for c in complete]

    # Keep one frame per cell for two wraps: cycles 3 and 4 (steady state), the first movie frame showing each cell.
    keep = []
    for ci in (2, 3):
        for rn in complete[ci]:
            m = rn["movie_frames"][0]
            t = 2 * m - 1
            name = f"c{ci + 1}-cell{rn['cell']}-tick{t}.png"
            shutil.copyfile(Path(movie_dir) / f"seam{m:08d}.png", OUT / name)
            keep.append({"file": name, "movie_frame": m, "tick": t, "cell": rn["cell"]})

    # Strip: every movie frame from the first kept frame through the frame after the third wrap of the pair.
    by_tick = {r["tick"]: r for r in rows}
    m0 = keep[0]["movie_frame"]
    m1 = movie_frame_for(complete[4][0]["first_tick"] + (1 if complete[4][0]["first_tick"] % 2 == 0 else 0)) + 1
    crops = []
    for m in range(m0, m1 + 1):
        t = 2 * m - 1
        r = by_tick[t]
        sx = int(round(min(r["x"], 320.0)))              # camera clamps at the level's left edge: screen x = x
        img = Image.open(Path(movie_dir) / f"seam{m:08d}.png").convert("RGB")
        box = (sx - 36, 327 - 76, sx + 36, 327 + 6)
        c = img.crop(box).resize(((box[2] - box[0]) * 3, (box[3] - box[1]) * 3), Image.NEAREST)
        d = ImageDraw.Draw(c)
        ax = (sx - box[0]) * 3
        d.line([(ax, 0), (ax, c.height)], fill=(255, 255, 0), width=1)        # the body's x (feet anchor)
        d.line([(0, (327 - box[1]) * 3), (c.width, (327 - box[1]) * 3)], fill=(255, 255, 0), width=1)
        crops.append((c, f"t{t} c{r['frame']}"))
    w, h = crops[0][0].size
    strip = Image.new("RGB", (w * len(crops), h + 22), (20, 20, 24))
    d = ImageDraw.Draw(strip)
    for i, (c, label) in enumerate(crops):
        strip.paste(c, (i * w, 22))
        d.text((i * w + 4, 4), label, fill=(240, 240, 240))
    strip.save(OUT / "strip.png")

    # Registration on the sheet, per cell (exact pixels: what the engine draws, the imported texture equals the PNG).
    a = np.asarray(Image.open(SHEET).convert("RGBA"))[:, :, 3] > 0
    cells = []
    for k in range(CELLS):
        m = a[:, k * CELL_W:(k + 1) * CELL_W]
        ys, xs = np.nonzero(m)
        low = int(ys.max())
        feet = np.nonzero(m[low])[0]
        t0, t1 = TORSO_ROWS
        ty, tx = np.nonzero(m[t0:t1 + 1])
        cells.append({"cell": k, "lowest_row": low, "feet_x_on_lowest_row": [int(feet.min()), int(feet.max())],
                      "torso_centroid_x": round(float(tx.mean()), 2), "top_row": int(ys.min()),
                      "bbox_x": [int(xs.min()), int(xs.max())]})
    tx = [c["torso_centroid_x"] for c in cells]
    anchor = {"offsets_on_run_ticks": sorted({tuple(r["offset"]) for r in run}),
              "sprite_positions_on_run_ticks": sorted({tuple(r["sprite_pos"]) for r in run}),
              "flip_h_on_run_ticks": sorted({r["flip_h"] for r in run}),
              "anchor_in_cell": [-OFFSET[0], -OFFSET[1]]}
    out = {
        "fixture": "capture harness places the characters (tests/capture_run_seam.gd); windowed Movie Maker, "
                   "--fixed-fps 30, --debug-collisions; movie frame m shows tick 2m - 1",
        "run_ticks": [run[0]["tick"], run[-1]["tick"]], "complete_cycles": len(complete), "wraps": wraps,
        "ticks_per_cell_per_cycle": [[x["ticks"] for x in c] for c in complete],
        "movie_frames_per_cell_per_cycle_at_30fps": frames_per_cell,
        "repeats_at_wrap": repeats, "cycles_with_a_repeated_cell": len(in_cycle_repeats),
        "kept_frames": keep, "strip": {"file": "strip.png", "movie_frames": [m0, m1], "scale": 3,
                                       "yellow_lines": "body x (feet anchor) and ground y 327"},
        "registration": {"engine": anchor, "sheet_cells": cells,
                         "torso_centroid_x_range_px": round(max(tx) - min(tx), 2),
                         "lowest_rows": [c["lowest_row"] for c in cells]},
        "cell_runs": [f"{x['cell']}@{x['first_tick']} x{x['ticks']}" for x in runs],
    }
    (OUT / "seam.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("complete_cycles", "ticks_per_cell_per_cycle",
                                          "movie_frames_per_cell_per_cycle_at_30fps", "repeats_at_wrap",
                                          "cycles_with_a_repeated_cell")}))
    print(json.dumps(out["registration"]))
    print(json.dumps([k["file"] for k in keep]), out["strip"])


if __name__ == "__main__":
    main(sys.argv[1])
