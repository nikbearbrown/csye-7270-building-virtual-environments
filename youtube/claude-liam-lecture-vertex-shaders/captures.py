#!/usr/bin/env python3
"""captures.py: this film's captures (CAPTURE-PLAN.md): 24 custom scenes through the scene library in capture-scenes/ (adapter vertex_scene.gd; scene id in V_ID,
beat length in CLIP_L) plus the Lab sprite still C18. Each clip is the beat's MEASURED audio + 1.0 s tail (events inside the library are fractions of that audio).
The two loop clips (final, dials-rest) serve two beats each: recorded once at the longer beat's length. Output: TK/runtime/remotion/public/vertex-shaders/.
  python3 captures.py [--only final slide ...]"""
import json, os, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent; S = R.parent / "_godot-shaders-series"; LAB = S / "lab"
DEST = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/vertex-shaders"); DEST.mkdir(parents=True, exist_ok=True)
LOGD = R / "evidence" / "build-captures"; LOGD.mkdir(parents=True, exist_ok=True)
sheet = json.loads((R / "beat_sheet.json").read_text())
DUR = {b["beat_id"]: float(b["actual_duration_s"]) for b in sheet["beats"] if b.get("actual_duration_s")}
# scene id, output name, beats (longest wins), still?
C = [("final","flag-final",["B01","B33"],False),("slide","slide",["B05"],False),("local","local",["B06"],False),("squash","squash",["B07"],False),("lean","lean",["B09"],False),
     ("triptych","triptych",["B11"],False),("tilt","tilt",["B12"],False),("mesh-recipe","mesh-recipe",["B15"],False),("pair","pair",["B17"],False),("densities","densities",["B18"],False),
     ("cut-along","cut-along",["B19"],False),("polygon","polygon",["B20"],False),("travel","travel",["B21"],False),("pinned","pinned",["B22"],False),("dials-rest","dials-rest",["B23","B26"],False),
     ("sweeps","sweeps",["B24"],False),("wind","wind",["B25"],False),("flat-mesh","flat-mesh",["B30"],True),("lit","lit",["B32"],False),("stripes","stripes",["B34"],True),
     ("flip","flip",["B35"],False),("vertex-two","vertex-two",["B37"],False),("polygon-uv","polygon-uv",["B38"],False),("drawing-only","drawing-only",["B39"],False)]
only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
def go(label, name, a, L, still, env_extra):
    env = dict(os.environ); env.update(env_extra); env["CLIP_L"] = f"{L:.2f}"
    a = a + ["--length", f"{L:.2f}"] + ([] if still else ["--tail", "1.0"])
    cmd = [str(LAB / "capture_shader.sh")] + a + ["--name", name, "--dest", str(DEST)] + (["--png", "1"] if still else [])
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    (LOGD / f"{label}-{name}.log").write_text(" ".join(cmd) + "\n" + r.stdout + r.stderr)
    res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
    j = json.loads(res[0][7:]) if res else {}
    print(label, name, f"{L:.2f}s", "ok" if (j.get("ok") and "WROTE" in r.stdout and "SCRIPT_ERROR" not in r.stdout) else "FAILED " + (r.stdout + r.stderr)[-400:], [(p["t"], p["at"], p["rgba"][:3]) for p in j.get("probes", [])], flush=True)
for sid, name, beats, still in C:
    if only and sid not in only: continue
    L = 0.1 if still else max(DUR[b] for b in beats)
    go(sid, name, ["--scene", str(R / "capture-scenes/vertex_scene.gd")], L, still, {"V_ID": sid})
if not only or "corner-colors" in only:
    probes = []
    for xy in ["0.36,0.2", "0.64,0.2", "0.36,0.8", "0.64,0.8", "0.5,0.5"]: probes += ["--probe-at", f"0:{xy}"]
    go("C18", "corner-colors", ["--shader", str(R / "lab-shaders/08-corner-colors.gdshader"), "--kind", "sprite", "--sprite-tex", "white"] + probes, 0.1, True, {})
