#!/usr/bin/env python3
"""captures.py: this film's 25 captures (CAPTURE-PLAN.md). The planning scene script (evidence/planning-checks/light_scene.gd, unchanged) is driven by
captures.json; its event times were estimated from the narration at 0.34 s a word, so every time field (at, appear, t0, t1) is scaled by
measured / estimated for the capture's beat when they differ by more than one second (written to capture-scenes/captures-build.json). Native route (1920 x 1080 at
scale 1: screen-space shader numbers are physical pixels). Clip = beat audio + 1.0 s tail. Output: TK/runtime/remotion/public/godot-shaders/ (names from captures.json 'out').
  python3 captures.py [--only C01 ...]"""
import copy, json, os, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent; S = R.parent / "_godot-shaders-series"; LAB = S / "lab"
DEST = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/godot-shaders"); DEST.mkdir(parents=True, exist_ok=True)
LOGD = R / "evidence" / "build-captures"; LOGD.mkdir(parents=True, exist_ok=True)
sheet = json.loads((R / "beat_sheet.json").read_text())
B = {b["beat_id"]: b for b in sheet["beats"]}
caps = json.loads((R / "evidence/planning-checks/captures.json").read_text())
def scale(o, r):
    if isinstance(o, dict):
        return {k: (v * r if k in ("at", "appear", "t0", "t1") and isinstance(v, (int, float)) else scale(v, r)) for k, v in o.items()}
    if isinstance(o, list): return [scale(x, r) for x in o]
    return o
build, info = {}, {}
for cid, c in caps.items():
    bid = c["beats"][0]; act = float(B[bid]["actual_duration_s"]); est = float(B[bid]["estimated_duration_s"])
    r = act / est if abs(act - est) > 1.0 else 1.0
    build[cid] = scale(c, r); info[cid] = (act, est, r, max(float(B[b]["actual_duration_s"]) for b in c["beats"]))
(R / "capture-scenes/captures-build.json").write_text(json.dumps(build, indent=1))
only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
for cid, c in caps.items():
    if only and cid not in only: continue
    act, est, r, longest = info[cid]
    still = bool(c.get("still"))
    name = c["out"].rsplit(".", 1)[0]
    L = 0.5 if still else longest
    env = dict(os.environ); env["L_ID"] = cid
    a = ["--native", "--scene", str(R / "capture-scenes/light_adapter.gd"), "--length", f"{L:.2f}"] + ([] if still else ["--tail", "1.0"])
    cmd = [str(LAB / "capture_shader.sh")] + a + ["--name", name, "--dest", str(DEST)] + (["--png", "1"] if still else [])
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    (LOGD / f"{cid}-{name}.log").write_text(" ".join(cmd) + "\n" + p.stdout + p.stderr)
    ok = "WROTE" in p.stdout and "SCRIPT_ERROR" not in p.stdout
    print(cid, name, f"{L:.2f}s (scale {r:.2f})", "ok" if ok else "FAILED " + (p.stdout + p.stderr)[-400:], flush=True)
