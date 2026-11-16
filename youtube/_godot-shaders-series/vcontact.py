#!/usr/bin/env python3
"""vcontact.py OUT.png clip.mp4 [clip2.mp4 ...] [--n 6]: a contact sheet, one row per clip, n frames evenly spaced (small), to LOOK at captures."""
import subprocess, sys
from pathlib import Path
a = sys.argv[1:]; n = 6
if "--n" in a: i = a.index("--n"); n = int(a[i + 1]); del a[i:i + 2]
out, clips = a[0], a[1:]
rows = []
tmp = Path("/private/tmp/claude-501/vcontact"); tmp.mkdir(parents=True, exist_ok=True)
for ci, c in enumerate(clips):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", c], capture_output=True, text=True).stdout)
    fr = []
    for k in range(n):
        t = dur * (k + 0.5) / n
        f = tmp / f"{ci}_{k}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", c, "-frames:v", "1", "-vf", "scale=384:216", str(f)], check=True)
        fr.append(str(f))
    r = tmp / f"row{ci}.png"
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in fr: cmd += ["-i", f]
    cmd += ["-filter_complex", f"hstack=inputs={n}", str(r)]
    subprocess.run(cmd, check=True); rows.append(str(r))
cmd = ["ffmpeg", "-y", "-loglevel", "error"]
for r in rows: cmd += ["-i", r]
cmd += ["-filter_complex", f"vstack=inputs={len(rows)}" if len(rows) > 1 else "null", out]
subprocess.run(cmd, check=True); print("wrote", out)
