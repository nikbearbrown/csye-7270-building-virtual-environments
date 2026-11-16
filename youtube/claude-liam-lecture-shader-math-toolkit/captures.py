#!/usr/bin/env python3
"""captures.py: this film's 16 Godot captures (CAPTURE-PLAN.md) with the shared harness. Sweeps are the plan's piecewise-linear keyframes with their times
converted to FRACTIONS of the plan's clip length and applied to the beat's MEASURED audio (clip = audio + 0.6 s tail), so each sweep finishes by about 85 %
and holds. Square pictures: sprite route (white 128 px texture at scale 5.625 = a 720 x 720 square on the 1280 x 720 logical canvas).
Output: TK/runtime/remotion/public/godot-shaders/math-toolkit/.  python3 captures.py [--only C01 ...]"""
import json, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent; S = R.parent / "_godot-shaders-series"; LAB = S / "lab"
DEST = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/godot-shaders/math-toolkit"); DEST.mkdir(parents=True, exist_ok=True)
SH = R / "lab-shaders"; LOGD = R / "evidence" / "build-captures"; LOGD.mkdir(parents=True, exist_ok=True)
sheet = json.loads((R / "beat_sheet.json").read_text())
DUR = {b["beat_id"]: float(b["actual_duration_s"]) for b in sheet["beats"] if b.get("actual_duration_s")}
SQ = ["--kind", "sprite", "--sprite-tex", "white", "--sprite-scale", "5.625"]
def sx(u): return f"{0.5 + (u - 0.5) * 0.5625:.4f}"          # square coordinate u (0..1) -> frame x
def key(name, pts, plan_len):
    return ["--animate", name + ":" + ",".join(f"{t / plan_len:.4f}f:{v}" for t, v in pts)]
# id, beat, shader, name, kind args, extra args, plan length (None = still), probes
C = [
 ("C01","B01","15-ring-final","ring-grow",SQ,key("radius",[(0,.12),(.5,.12),(11,.38),(13,.38)],13),13,[("0.5f",sx(.5)+",0.5")]),
 ("C02","B03","01-ramp","ramp",["--kind","rect"],[],None,[("0","0.02,0.5"),("0","0.5,0.5"),("0","0.98,0.5")]),
 ("C03","B08","02-step","step-sweep",["--kind","rect"],key("edge",[(0,.5),(4,.5),(6.5,.2),(10.5,.8),(12.5,.8)],12.5),12.5,[("0.97f","0.45,0.5"),("0.97f","0.55,0.5")]),
 ("C04","B13","03-smoothstep","smoothstep-sweep",["--kind","rect"],key("width",[(0,.4),(3.5,.4),(10,.03),(13,.03)],13),13,[("0.97f","0.25,0.5"),("0.97f","0.5,0.5"),("0.97f","0.75,0.5")]),
 ("C05","B15","04-mix-colors","mix-colors",["--kind","rect"],[],None,[("0","0.02,0.5"),("0","0.5,0.5"),("0","0.98,0.5")]),
 ("C06","B20","05-fract","fract-sweep",["--kind","rect"],key("count",[(0,1),(4.5,1),(10.5,6),(12.5,6)],12.5),12.5,[("0.97f","0.1,0.5"),("0.97f","0.3,0.5"),("0.97f","0.6,0.5"),("0.97f","0.9,0.5")]),
 ("C07","B23","06-stripes","stripes",["--kind","rect"],[],None,[("0","0.05,0.5"),("0","0.1,0.5"),("0","0.15,0.5"),("0","0.2,0.5")]),
 ("C08","B29","08-distance","distance",SQ,[],None,[("0",sx(.5)+",0.5"),("0",sx(.75)+",0.5"),("0",sx(1)+",0.5"),("0",sx(1)+",1.0")]),
 ("C09","B31","09-glow","glow",SQ,[],None,[("0",sx(.5)+",0.5"),("0",sx(.75)+",0.5"),("0",sx(1)+",0.5")]),
 ("C10","B33","07-pow","pow-sweep",["--kind","rect"],key("power",[(0,1),(3,1),(11,6),(15.5,6)],15.5),15.5,[("0.97f","0.5,0.5"),("0.97f","0.9,0.5")]),
 ("C11","B35","10-disk","disk",SQ,[],None,[("0",sx(.5)+",0.5"),("0",sx(.7)+",0.5"),("0",sx(.9)+",0.5"),("0",sx(1)+",1.0")]),
 ("C12","B36","11-disk-flip","disk-flip",SQ,[],None,[("0",sx(.5)+",0.5"),("0",sx(.9)+",0.5"),("0",sx(1)+",1.0")]),
 ("C13","B38","12-ring-hard","ring-hard",SQ,[],None,[("0",sx(.7)+",0.5"),("0",sx(.84)+",0.5"),("0",sx(.95)+",0.5")]),
 ("C14","B39","13-ring-color","ring-color",SQ,[],None,[("0",sx(.7)+",0.5"),("0",sx(.84)+",0.5"),("0",sx(.95)+",0.5")]),
 ("C15","B40","14-ring-soft","ring-soft",SQ,[],None,[("0",sx(.7)+",0.5"),("0",sx(.84)+",0.5"),("0",sx(.95)+",0.5")]),
 ("C16","B41","15-ring-final","ring-dial",SQ,key("radius",[(0,.3),(6,.3),(8.5,.12),(11.5,.38),(12.5,.38)],12.5),12.5,[("0.5f",sx(.5)+",0.5"),("0.85f",sx(.5)+",0.5")]),
]
only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
for cid, bid, shader, name, kind, extra, plan_len, probes in C:
    if only and cid not in only: continue
    d = DUR[bid]
    a = ["--shader", str(SH / f"{shader}.gdshader")] + kind + extra + ["--length", f"{d:.2f}"]
    if plan_len: a += ["--tail", "0.6"]
    for t, xy in probes: a += ["--probe-at", f"{t}:{xy}"]
    cmd = [str(LAB / "capture_shader.sh")] + a + ["--name", name, "--dest", str(DEST)] + ([] if plan_len else ["--png", "1"])
    r = subprocess.run(cmd, capture_output=True, text=True)
    (LOGD / f"{cid}-{name}.log").write_text(" ".join(cmd) + "\n" + r.stdout + r.stderr)
    res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
    j = json.loads(res[0][7:]) if res else {}
    print(cid, bid, name, f"{d:.2f}s", "ok" if j.get("ok") else "FAILED " + r.stdout[-300:], [(p["at"], p["rgba"][:3]) for p in j.get("probes", [])], flush=True)
