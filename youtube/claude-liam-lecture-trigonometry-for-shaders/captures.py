#!/usr/bin/env python3
"""captures.py: this film's 13 Godot captures (CAPTURE-PLAN.md) with the shared harness. Squares are captured at 1920 x 1920 (the harness's logical canvas
is 1280 x 1280; every shader here works in UV fractions); the wide one at 1920 x 1080. Clips are the beat's MEASURED audio + 1.0 s tail, scripted values are
fractions of the beat. Output: TK/runtime/remotion/public/godot-shaders/ (file names the lanes use).  python3 captures.py [--only C01 ...]"""
import json, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent; S = R.parent / "_godot-shaders-series"; LAB = S / "lab"
DEST = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/godot-shaders"); DEST.mkdir(parents=True, exist_ok=True)
SH = R / "lab-shaders"; LOGD = R / "evidence" / "build-captures"; LOGD.mkdir(parents=True, exist_ok=True)
sheet = json.loads((R / "beat_sheet.json").read_text())
DUR = {b["beat_id"]: float(b["actual_duration_s"]) for b in sheet["beats"] if b.get("actual_duration_s")}
SQ = ["--size", "1920x1920"]
SPR = ["--kind", "sprite", "--sprite-res", "512", "--linear"]
def P(*xy): return [("0.5f" if False else t, p) for t, p in xy]
C = [
 ("C01","B01","06-meteor-orbit","trig-hook",SQ+["--kind","rect"],[],False,[("0.5f","0.5,0.5")]),
 ("C02","B19","01-moon-fixed","trig-moon-fixed",SQ+["--kind","rect"],[],True,[("0","0.7598,0.65"),("0","0.7598,0.35"),("0","0.5,0.5")]),
 ("C03","B21","02-orbit","trig-orbit",SQ+["--kind","rect"],[],False,[]),
 ("C04","B22","03-orbit-fast","trig-orbit-fast",SQ+["--kind","rect"],[],False,[]),
 ("C05","B23","05-moons-evenly","trig-moons",SQ+["--kind","rect"],[],False,[]),
 ("C06","B24","04-orbit-aspect","trig-aspect",["--size","1920x1080","--kind","rect"],["--animate","aspect:0:1.0,0.58f:1.0,0.82f:1.7778,1f:1.7778"],False,[("0.5f","0.5,0.5"),("0.9f","0.5,0.5")]),
 ("C07","B28","06-meteor-orbit","trig-meteor",SQ+["--kind","rect"],[],False,[]),
 ("C08","B29","07-meteor-reverse","trig-meteor-reverse",SQ+["--kind","rect"],[],False,[]),
 ("C09","B35","08-atan-colors","trig-atan-colors",SQ+["--kind","rect"],[],True,[("0","0.9,0.5"),("0","0.5,0.9"),("0","0.5,0.1"),("0","0.1,0.45"),("0","0.1,0.55")]),
 ("C10","B36","09-atan-one-argument","trig-atan-one-argument",SQ+["--kind","rect"],[],True,[("0","0.8,0.8"),("0","0.2,0.2"),("0","0.8,0.2"),("0","0.2,0.8")]),
 ("C11","B38","10-sweep","trig-sweep",SQ+SPR,["--animate","sweep:0:0.3,0.68f:0.3,0.6801f:0.0,0.97f:1.0,1f:1.0"],False,[("0.5f","0.36,0.36"),("0.5f","0.64,0.64")]),
 ("C12","B39","11-sweep-top","trig-sweep-top",SQ+SPR,["--animate","sweep:0:0.3,0.60f:0.3,0.6001f:0.0,0.97f:1.0,1f:1.0"],False,[("0.5f","0.64,0.36")]),
 ("C13","B40","12-flower","trig-flower",SQ+["--kind","rect"],[],False,[]),
]
only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
for cid, bid, shader, name, kind, extra, still, probes in C:
    if only and cid not in only: continue
    d = DUR[bid]
    a = ["--shader", str(SH / f"{shader}.gdshader")] + kind + extra + ["--length", f"{d:.2f}"]
    if not still: a += ["--tail", "1.0"]
    for t, xy in probes: a += ["--probe-at", f"{t}:{xy}"]
    cmd = [str(LAB / "capture_shader.sh")] + a + ["--name", name, "--dest", str(DEST)] + (["--png", "1"] if still else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    (LOGD / f"{cid}-{name}.log").write_text(" ".join(cmd) + "\n" + r.stdout + r.stderr)
    res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
    j = json.loads(res[0][7:]) if res else {}
    print(cid, bid, name, f"{d:.2f}s", "ok" if j.get("ok") else "FAILED " + (r.stdout + r.stderr)[-300:], [(p["t"], p["at"], p["rgba"][:3]) for p in j.get("probes", [])], flush=True)
