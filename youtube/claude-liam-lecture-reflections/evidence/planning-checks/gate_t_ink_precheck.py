#!/usr/bin/env python3
"""gate_t_ink_precheck.py <scratch project dir> <frames out dir>: could anything in a capture be mistaken for text by GATE T?

GATE T (the toolkit's type_check.py) reads as text every pixel within 48 RGB of ink (#3D3929) or mute (#5D584F), then looks for text-like
blobs. Real captures with dark regions are the usual way a build fails it. This renders the 50 % and 85 % frames (the ones Gate V samples)
of all nineteen captures at full 3840 x 2160 in the route the film uses (C08: the 1:1 route, enlarged 3x by whole pixels), then runs the
toolkit's OWN mask and blob functions on each frame (type_check.py is imported, not copied or edited) and reports, per frame:
  ink-or-mute pixels, blobs of 30+ pixels, and how many of them GATE T would count as text runs.
The raw capture has no text, so this says "nothing in the picture can be read as text"; it cannot say the final composition passes (the
ShaderLab frame adds code, labels and rings: GATE T on the real frames is the build's job).
Needs godot 4.7.2 on PATH, Pillow, numpy, scipy. Writes only into the two directories given. One fresh Godot process per capture.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
TYPE_CHECK = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/type_check.py")


def load_type_check():
    spec = importlib.util.spec_from_file_location("type_check_readonly", TYPE_CHECK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def capture_ids():
    out = subprocess.run([sys.executable, str(HERE / "capture_list.py")], capture_output=True, text=True, check=True).stdout
    return [line.split("\t")[0] for line in out.splitlines() if line.strip()]


def render_frames(proj: Path, frames: Path, cid: str):
    """50 % and 85 % frames of one capture at 3840 x 2160 (C08: 1:1 route, then enlarged 3x by whole pixels)."""
    if cid == "C08":
        route = ["--route", "direct", "--scale", "1"]
    else:
        route = ["--route", "sv", "--scale", "3", "--full"]
    cmd = ["godot", "--path", str(proj), "--script", "res://scene_runner.gd", "--", "--capture", cid, *route,
           "--times", "50%,85%", "--out", str(frames)]
    subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    got = sorted(frames.glob(f"{cid}-t*.png"))
    if cid == "C08":
        for p in got:
            im = Image.open(p).convert("RGB")
            if im.size != (3840, 2160):
                im.resize((3840, 2160), Image.NEAREST).save(p)
    return got


def main():
    proj, frames = Path(sys.argv[1]), Path(sys.argv[2])
    proj.mkdir(parents=True, exist_ok=True)
    frames.mkdir(parents=True, exist_ok=True)
    if not (proj / "project.godot").exists():
        (proj / "project.godot").write_text((HERE / "project.godot").read_text())
    for f in HERE.glob("*.gd"):
        (proj / f.name).write_text(f.read_text())
    tc = load_type_check()
    ink, mute = tc.hex_to_rgb(tc.INK_HEX), tc.hex_to_rgb(tc.MUTE_HEX)
    print(f"GATE T mask: pixels within {48} RGB of ink {tc.INK_HEX} {ink} or mute {tc.MUTE_HEX} {mute} (type_check.py)")
    print(f"{'frame':22} {'ink/mute px':>12} {'blobs>=30px':>12} {'text-run blobs':>15}  note")
    flagged = 0
    for cid in capture_ids():
        for p in render_frames(proj, frames, cid):
            arr = np.array(Image.open(p).convert("RGB"))
            polarity, _ = tc.detect_polarity(arr)
            mask = tc.visible_text_mask(arr, polarity)
            lab, n = tc.labeled_blobs(mask)
            raw = tc.blob_bboxes(lab, n) if n else []
            runs = tc.text_run_bboxes(raw, arr.shape[0]) if raw else []
            note = f"polarity {polarity}"
            if runs:
                flagged += 1
                note += "; LOOK: " + ", ".join(f"{x1 - x0 + 1}x{y1 - y0 + 1}px at ({x0},{y0})" for x0, y0, x1, y1, _ in runs[:3])
            print(f"{p.name:22} {int(mask.sum()):>12} {len(raw):>12} {len(runs):>15}  {note}")
    print(f"\nframes with text-run blobs: {flagged}")


if __name__ == "__main__":
    main()
