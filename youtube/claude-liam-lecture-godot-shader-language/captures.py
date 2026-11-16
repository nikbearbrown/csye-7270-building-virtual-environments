#!/usr/bin/env python3
"""captures.py: records this film's Godot captures (CAPTURE-PLAN.md). Stills: Lab check_shader.sh at 1920x1080 (even width) with probes; clips:
the shared harness (S/lab/capture_shader.sh) at 4K on the SubViewport route. Output: TK/runtime/remotion/public/godot-shader-language/ (+ pantry/ copies for Manim).
  python3 captures.py [--only C01a C02 ...]"""
import json, math, shutil, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent
S = R.parent / "_godot-shaders-series"; LAB = S / "lab"
DEST = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/godot-shader-language")
SH = R / "lab-shaders"; PAN = R / "pantry"; PAN.mkdir(exist_ok=True); DEST.mkdir(parents=True, exist_ok=True)
LOGD = R / "evidence" / "build-captures"; LOGD.mkdir(parents=True, exist_ok=True)
sheet = json.loads((R / "beat_sheet.json").read_text())
DUR = {b["beat_id"]: float(b["actual_duration_s"]) for b in sheet["beats"] if b.get("actual_duration_s")}
def best_origin(a):
    """t0 over one period (pi) MAXIMISING the min wave at 0.5a and 0.85a (wave = 0.5+0.5 sin(2(t0+t))). The shader is mix(vec3(0.9), base, wave): wave 1 is TEAL,
    wave 0 is pale gray. (CAPTURE-PLAN.md states the rule the other way round; that would put the pale phase on the Gate V frames. Logged in BUILD-LOG.)"""
    best = None
    for i in range(0, 628):
        t0 = i / 200.0
        w = min(0.5 + 0.5 * math.sin(2 * (t0 + f * a)) for f in (0.5, 0.85))
        if best is None or w > best[1]: best = (t0, w)
    return best
STILLS = [("C02","02-spacing-neat","spacing",["0.25,0.25"]),("C03a","03-comment-on","comment-on",["0.02,0.02","0.98,0.98"]),("C03b","03-comment-off","comment-off",["0.02,0.02","0.98,0.02","0.02,0.975","0.98,0.975"]),
          ("C04","05-pastel","pastel",["0.02,0.02","0.98,0.02","0.02,0.98","0.98,0.98","0.5,0.5"]),("C05b","06-pastel-bgr","pastel-bgr",["0.02,0.02","0.98,0.02","0.02,0.98","0.98,0.98"]),
          ("C06","10-pass-uv-in","pass-uv",["0.02,0.02","0.98,0.98"]),("C07","15-overload","overload",["0.25,0.5","0.75,0.5"]),("C08","16-split-if","split-if",["0.25,0.5","0.75,0.5"]),
          ("C09","18-stripes","stripes",["0.5,0.1","0.5,0.5"]),("C10a","19-float-equals","float-equals-1920",["0.5,0.5"]),("C10b","20-float-range","float-range-1920",["0.5,0.5"])]
def still(cid, shader, name, probes):
    cmd = [str(LAB / "check_shader.sh"), str(SH / f"{shader}.gdshader"), "--kind", "rect", "--size", "1920x1080", "--png", str(DEST / f"{name}.png")]
    for p in probes: cmd += ["--probe", p]
    r = subprocess.run(cmd, capture_output=True, text=True)
    (LOGD / f"{cid}-{name}.log").write_text(" ".join(cmd) + "\n" + r.stdout + r.stderr)
    res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
    j = json.loads(res[0][7:]) if res else {}
    print(cid, name, "ok" if j.get("ok") else "FAILED", j.get("size"), [(p["at"], p["rgba"][:3]) for p in j.get("probes", [])], flush=True)
    if (DEST / f"{name}.png").exists(): shutil.copy(DEST / f"{name}.png", PAN / f"{name}.png")
def clip(cid, bid, name, extra=""):
    d = DUR[bid] + 0.6                                  # a little longer than the audio
    t0, w = best_origin(d - 0.6)
    cmd = [str(LAB / "capture_shader.sh"), "--shader", str(SH / "01-breathe.gdshader"), "--kind", "rect", "--set", "tint=#5FA391", "--length", f"{d:.2f}", "--time-origin", f"{t0:.3f}",
           "--probe-at", f"{0.5*(d-0.6):.2f}:0.5,0.5", "--probe-at", f"{0.85*(d-0.6):.2f}:0.5,0.5", "--name", name, "--dest", str(DEST)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    (LOGD / f"{cid}-{name}.log").write_text(" ".join(cmd) + "\n" + r.stdout + r.stderr)
    res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
    j = json.loads(res[0][7:]) if res else {}
    print(cid, name, "ok" if j.get("ok") else "FAILED", f"origin {t0:.3f} wave {w:.2f}", [(p["t"], p["rgba"][:3]) for p in j.get("probes", [])], flush=True)
def dissolve():
    d = DUR["B17"]
    a, b = DEST / "pastel.png", DEST / "pastel-bgr.png"
    t1 = 0.14 * d
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", f"{d+0.6:.2f}", "-framerate", "30", "-i", str(a), "-loop", "1", "-t", f"{d+0.6:.2f}", "-framerate", "30", "-i", str(b),
           "-filter_complex", f"[0:v][1:v]xfade=transition=fade:duration=0.7:offset={t1:.2f},format=yuv420p[o]", "-map", "[o]", "-t", f"{d+0.6:.2f}", "-c:v", "libx264", "-crf", "14", "-r", "30", str(DEST / "pastel-to-bgr.mp4")]
    subprocess.run(cmd, check=True); print("C05 pastel-to-bgr.mp4 written (two real renders, dissolved by ffmpeg)")
only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
for cid, shader, name, probes in STILLS:
    if not only or cid in only: still(cid, shader, name, probes)
if not only or "C05" in only: dissolve()
if not only or "C01a" in only: clip("C01a", "B01", "breathe-b01")
if not only or "C01b" in only: clip("C01b", "B40", "breathe-b40")
