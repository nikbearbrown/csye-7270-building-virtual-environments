#!/usr/bin/env python3
"""capture_all.py: record every Godot capture of "Reading the Screen" (C01 to C23) from the film's own layout, one after another.

  python3 capture_all.py --dry-run                    print what it would do (no Godot, no ffmpeg)
  python3 capture_all.py                              all 23 captures into <toolkit>/runtime/remotion/public/reading-the-screen/ (22 at 3840 x 2160 over a
                                                      1280 x 720 canvas; C13 natively at 1920 x 1080, see ROUTES below)
  python3 capture_all.py --only C05 C17               just these
  python3 capture_all.py --size 480x270 --frames 6 --public-dir /tmp/x   a tiny test run (what this script was tested with)

Where it gets its facts (nothing is typed twice):
  * lanes/act*.json: each capture lane's `props.video` (the file name the film uses) and `capture_spec`, which starts "Cnn: scene_xxx.gd".
  * beat_sheet.json: each beat's measured audio length (`actual_duration_s`, after generate_audio_kokoro.py) or, before that, the estimate.
    A capture used by two beats (C01, C06) takes the longer length. Every scene is a function of u = t / length, so it fits any length.
Routes (verify10.gd, run-25 and run-26): a shader that works in fractions looks the same through the 3840 x 2160 SubViewport over a 1280 x 720 canvas
(the spotlight scenes C06, C07, C08 and C23 land within 1 canvas pixel of the 1280 x 720 result), so those 22 captures use it and stay crisp in the 4K master.
A mip-level blur counts texels of the screen texture and is less than half as blurred on that route, so C13 is captured natively at 1920 x 1080 at scale 1
(a SubViewport of that size, the scene built for a 1920 x 1080 canvas), the size it is shown at in the layout.
It calls ./run-checks.sh capture ... (a scratch Godot project built from this folder, serialised with the Shader Lab lock, fixed 30 fps tick so TIME
repeats exactly, SubViewport over the 1280 x 720 canvas), then ffmpeg, then deletes the PNG sequence. One capture at a time; disk is checked first.
"""
import argparse
import glob
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
BOOKS = FILM.parents[2]
TOOLKIT = BOOKS / "brutalist.art"
FRAMES_ROOT = Path("/private/tmp/claude-501/rts-checks/capture")
NATIVE = {"C13": (1920, 1080)}            # captures that must run at the size they are shown (no 3x SubViewport); every other capture uses --size


def plan():
    lanes = {}
    for f in sorted(glob.glob(str(FILM / "lanes" / "*.json"))):
        lanes.update(json.loads(Path(f).read_text()))
    sheet = json.loads((FILM / "beat_sheet.json").read_text())
    dur = {b["beat_id"]: (b.get("actual_duration_s") or b.get("estimated_duration_s")) for b in sheet["beats"]}
    caps = {}
    scene_of = {}
    for bid, lane in lanes.items():          # first pass: where each capture id is defined ("C01: scene_c01_pool.gd ...")
        m = re.match(r"(C\d\d): (scene_\w+)\.gd", lane.get("capture_spec", ""))
        if m:
            scene_of[m.group(1)] = m.group(2)
    for bid, lane in lanes.items():
        if lane.get("lane") != "capture":
            continue
        m = re.match(r"(C\d\d)(?:: (scene_\w+)\.gd| again)", lane.get("capture_spec", ""))
        if not m:
            raise SystemExit(f"{bid}: capture_spec does not start 'Cnn: scene_xxx.gd' or 'Cnn again'")
        cid = m.group(1)
        scene = m.group(2) or scene_of[cid]
        video = lane["props"]["video"]
        c = caps.setdefault(cid, {"scene": scene, "video": video, "beats": [], "seconds": 0.0})
        assert c["scene"] == scene and c["video"] == video, f"{cid}: two beats disagree about the scene or the video"
        c["beats"].append(bid)
        c["seconds"] = max(c["seconds"], float(dur[bid]))
    return dict(sorted(caps.items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="capture ids, e.g. C05 C17")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--size", default="3840x2160")
    ap.add_argument("--frames", type=int, default=0, help="render only the first N frames (a test)")
    ap.add_argument("--public-dir", default=str(TOOLKIT / "runtime" / "remotion" / "public" / "reading-the-screen"))
    ap.add_argument("--keep-frames", action="store_true")
    a = ap.parse_args()
    w, h = a.size.split("x")
    caps = plan()
    todo = {k: v for k, v in caps.items() if not a.only or k in a.only}
    pub = Path(a.public_dir)
    print(f"{len(todo)} captures, {w} x {h}, into {pub}")
    for cid, c in todo.items():
        name = Path(c["video"]).name
        route = "native %d x %d" % NATIVE[cid] if cid in NATIVE else f"{w} x {h} over 1280 x 720"
        print(f"  {cid} {c['scene']:28} beats {','.join(c['beats']):8} {c['seconds']:5.1f} s  {route:26} ->  {name}")
    if a.dry_run:
        return 0
    free_gb = shutil.disk_usage("/").free / 1e9
    print(f"free disk: {free_gb:.0f} GB")
    if free_gb < 15:
        raise SystemExit("under 15 GB free: stop (a 4K PNG sequence is large)")
    pub.mkdir(parents=True, exist_ok=True)
    for cid, c in todo.items():
        name = Path(c["video"]).name
        if cid in NATIVE:                 # at the real size, unless this is a tiny test run (--size other than the default)
            nw, nh = NATIVE[cid] if a.size == "3840x2160" else (int(w), int(h))
            extra = ["--native", "--width", str(nw), "--height", str(nh)]
        else:
            extra = ["--width", w, "--height", h]
        extra += ["--frames", str(a.frames)] if a.frames else []
        cmd = [str(HERE / "run-checks.sh"), "capture", c["scene"], f"{c['seconds']:.3f}", "forward_plus"] + extra
        print("$", " ".join(cmd), flush=True)
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = r.stdout + r.stderr
        if '"id":"capture"' not in out or "ERROR" in out.replace("# exit 0", ""):
            print(out[-1500:])
            raise SystemExit(f"{cid}: the capture driver did not finish cleanly")
        frames = FRAMES_ROOT / c["scene"]
        n = len(list(frames.glob("f*.png")))
        target = pub / name
        enc = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", str(frames / "f%05d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "12", str(target)]
        print("$", " ".join(enc), flush=True)
        subprocess.run(enc, check=True)
        print(f"  {cid}: {n} frames -> {target} ({target.stat().st_size / 1e6:.1f} MB)")
        if not a.keep_frames:
            shutil.rmtree(frames, ignore_errors=True)
    print("done. LOOK at the 50 % and 85 % frame of each video against evidence/planning-checks/frames/ before the 4K render.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
