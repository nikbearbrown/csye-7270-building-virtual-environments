#!/usr/bin/env python3
"""gate4k.py CLASS...  -- renders each Manim class of the act's assembled scenes.py at 3840x2160 (low fps: only the frames matter),
extracts the 50% and 85% frames and runs the toolkit's own GATE T checks (type_check.py functions) and Gate V (final_frame_check.analyze_frame).
Deletes the class's scratch media afterwards (disk is tight)."""
import sys, subprocess, shutil, json, numpy as np
from pathlib import Path
from PIL import Image
sys.path.insert(0, "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts")
sys.path.insert(0, "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/qc")
import type_check as tc
import final_frame_check as fv
SCR = Path("/private/tmp/claude-501/lecture-a5shaders-act6")
REEL = "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot"
OUT = Path("/private/tmp/claude-501/a6-scratch/frames4k"); OUT.mkdir(exist_ok=True)
sparse = set(sys.argv[sys.argv.index("--sparse") + 1].split(",")) if "--sparse" in sys.argv else set()
classes = [a for a in sys.argv[1:] if not a.startswith("--") and a not in sparse and "," not in a]
for cls in classes:
    media = Path("/private/tmp/claude-501/a6-scratch/media4k") / cls
    shutil.rmtree(media, ignore_errors=True)
    r = subprocess.run(["manim", "--resolution", "3840,2160", "--fps", "8", "--media_dir", str(media), str(SCR / "scenes.py"), cls],
                       cwd=SCR, capture_output=True, text=True)
    vids = list(media.rglob(f"{cls}.mp4"))
    if not vids:
        print(cls, "NO VIDEO"); print((r.stdout + r.stderr)[-1500:]); continue
    v = vids[0]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)], text=True))
    print(f"=== {cls}  {dur:.2f}s  " + [l for l in r.stdout.splitlines() if "[pace]" in l][0] if any("[pace]" in l for l in r.stdout.splitlines()) else f"=== {cls} {dur:.2f}s")
    for pct in (50, 85):
        png = OUT / f"{cls.split('_')[0]}_{pct}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(min(dur * pct / 100, dur - 0.05)), "-i", str(v), "-frames:v", "1", str(png)], check=True)
        img = Image.open(png).convert("RGB")
        arr = np.array(img)
        pol, bg = tc.detect_polarity(arr)
        pattern = cls
        res = []
        res.append(("min-size", *tc.check_min_size(img, cls, pattern, polarity=pol)))
        res.append(("overflow", *tc.check_overflow(img, cls, polarity=pol, pattern=pattern)))
        res.append(("contrast", *tc.check_contrast(img, cls, pattern, polarity=pol, bg_rgb=bg)))
        res.append(("contrast-local", *tc.check_contrast_per_blob(img, polarity=pol)))
        res.append(("bbox-overlap", *tc.check_bbox_overlap(img, polarity=pol)))
        res.append(("kerning", *tc.check_kerning_sanity(img, cls, True, False, pattern)))
        print(f"  --- {pct}%  polarity={pol}")
        for name, st, msg in res:
            print(f"   {'FAIL' if st=='FAIL' else st:4} {name}: {msg[:150]}")
        d, cover = fv.analyze_frame(str(png))
        if cls.split('_')[0] in sparse:
            d = [x for x in d if x[1] not in ("underfill", "clustered", "empty-frame")]
        print(f"   Gate V: cover={cover*100:.0f}% defects={d}")
    shutil.rmtree(media, ignore_errors=True)
