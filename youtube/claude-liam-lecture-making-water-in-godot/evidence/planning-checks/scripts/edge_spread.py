#!/usr/bin/env python3
"""edge_spread.py <clip.mp4> [...]: the near-edge spread of the low-camera clips (B31, B38; 1280 x 720 recordings).
For frames of the clip (10 per second), the lowest row of every column that is not the stage grey (217, 213, 202) is found by scanning up from the bottom;
the spread of a frame is its max row minus its min row. Prints min, mean and max spread over the clip. Frames go to a scratch folder and are deleted."""
import glob
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image


def spreads(clip):
    d = Path(tempfile.mkdtemp(prefix="edge-", dir="/private/tmp/claude-501"))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-i", clip, "-vf", "fps=10", str(d / "f_%04d.png")], check=True)
    bg = np.array([217, 213, 202])
    out, shape = [], None
    for f in sorted(glob.glob(str(d / "f_*.png"))):
        a = np.asarray(Image.open(f).convert("RGB")).astype(int)
        shape = a.shape
        rows = []
        for x in range(int(a.shape[1] * 0.05), int(a.shape[1] * 0.95), 4):
            col = a[:, x, :]
            y = a.shape[0] - 1
            while y > 0 and np.abs(col[y] - bg).max() < 10:
                y -= 1
            rows.append(y)
        out.append((min(rows), max(rows)))
    for f in glob.glob(str(d / "*")):
        Path(f).unlink()
    d.rmdir()
    return out, shape


for clip in sys.argv[1:]:
    s, shape = spreads(clip)
    sp = [b - a for a, b in s]
    print(f"{Path(clip).name} ({shape[1]} x {shape[0]}): {len(s)} frames; near-edge spread min {min(sp)}, mean {np.mean(sp):.0f}, max {max(sp)} rows; "
          f"lowest row seen {max(b for a, b in s)}, highest {min(a for a, b in s)}")
