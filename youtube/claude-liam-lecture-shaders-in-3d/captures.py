#!/usr/bin/env python3
"""captures.py: this film's 19 Godot captures (CAPTURE-PLAN.md) with the shared harness; scene scripts in capture-scenes/ (S_VARIANT / CLIP_L go in the
environment). Every clip is as long as its beat's MEASURED audio (+0.6 s tail), events are fractions of it. Output: TK/runtime/remotion/public/shaders-in-3d/.
  python3 captures.py [--only C01 ...]"""
import json, os, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent; S = R.parent / "_godot-shaders-series"; LAB = S / "lab"
DEST = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/shaders-in-3d"); DEST.mkdir(parents=True, exist_ok=True)
SH = R / "lab-shaders"; SC = R / "capture-scenes"; LOGD = R / "evidence" / "build-captures"; LOGD.mkdir(parents=True, exist_ok=True)
TMP = Path("/private/tmp/claude-501/s3d-parts"); TMP.mkdir(parents=True, exist_ok=True)
sheet = json.loads((R / "beat_sheet.json").read_text())
DUR = {b["beat_id"]: float(b["actual_duration_s"]) for b in sheet["beats"] if b.get("actual_duration_s")}
def sh(n): return ["--shader", str(SH / n)]
def scene(n): return ["--scene", str(SC / n)]
def run(cid, name, args, L, variant=None, still=False, renderer=None, dest=None, size=None, probes=()):
    env = dict(os.environ)
    if variant: env["S_VARIANT"] = variant
    env["CLIP_L"] = f"{L:.2f}"
    a = args + ["--length", f"{L:.2f}"]
    if not still: a += ["--tail", "0.6"]
    if size: a += ["--size", size]
    for t, xy in probes: a += ["--probe-at", f"{t}:{xy}"]
    cmd = [str(LAB / "capture_shader.sh")] + a + ["--name", name, "--dest", str(dest or DEST)] + (["--png", "1"] if still else []) + (["--renderer", renderer] if renderer else [])
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    (LOGD / f"{cid}-{name}.log").write_text(" ".join(cmd) + "\n" + r.stdout + r.stderr)
    res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
    j = json.loads(res[0][7:]) if res else {}
    print(cid, name, f"{L:.2f}s", renderer or "", "ok" if j.get("ok") else "FAILED " + (r.stdout + r.stderr)[-300:], [(p["t"], p["at"], p["rgba"][:3]) for p in j.get("probes", [])], flush=True)
    return j.get("ok")
def hstack(left, right, out):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(left), "-i", str(right), "-filter_complex", "hstack=inputs=2", str(out)], check=True)
def sqx(u): return f"{0.5 + (u - 0.5) * 0.5063:.4f}"
def sqy(v): return f"{0.5 + (v - 0.5) * 0.9:.4f}"
T = []
def want(c): return not ONLY or c in ONLY
ONLY = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
if want("C01"): run("C01", "pad-angled-sweep", sh("12-signal-pad.gdshader") + scene("S1-pad.gd") + ["--animate", "pad.activation:0:0,0.86f:1,1f:1"], max(DUR["B01"], DUR["B29"]), "single")
if want("C02"): run("C02", "uv-meshes-turn", sh("06-uv-colors-3d.gdshader") + scene("S2-three-meshes.gd"), DUR["B08"])
if want("C03a"): run("C03a", "lamp-0", scene("S3-lamp.gd") + ["--call-at", f"{0.56 * DUR['B10']:.2f}:lamp_on"], DUR["B10"], "a", probes=[("0.3f", "0.5,0.5"), ("0.85f", "0.44,0.5"), ("0.85f", "0.56,0.5")])
if want("C03"): run("C03", "lamp-1", scene("S3-lamp.gd"), DUR["B11"], "1", probes=[("0.5f", "0.5,0.5"), ("0.85f", "0.5,0.5")])
if want("C04"): run("C04", "lamp-2", scene("S3-lamp.gd"), DUR["B14"], "2")
if want("C05"): run("C05", "lamp-3", scene("S3-lamp.gd"), DUR["B16"], "3")
if want("C06"): run("C06", "turnaround", scene("S4-turnaround.gd"), DUR["B17"])
if want("C07"): run("C07", "uv-colors-quad", sh("06-uv-colors-3d.gdshader") + scene("S5-face-on-square.gd"), 0.1, still=True,
                    probes=[("0", f"{sqx(.02)},{sqy(.02)}"), ("0", f"{sqx(.98)},{sqy(.02)}"), ("0", f"{sqx(.02)},{sqy(.98)}"), ("0", f"{sqx(.98)},{sqy(.98)}"), ("0", "0.5,0.5")])
if want("C08"): run("C08", "stripes-grey", sh("10-stripes-grey.gdshader") + ["--kind", "quad3d"], 0.1, still=True, probes=[("0", "0.03125,0.5"), ("0", "0.09375,0.5")])
if want("C09"): run("C09", "mix-dial-sweep", sh("11-mix-dial.gdshader") + ["--kind", "quad3d", "--animate", "activation:0:1"], DUR["B25"], probes=[("0.5f", "0.5,0.5"), ("0.85f", "0.5,0.5")])
if want("C10"): run("C10", "set-parameter", sh("12-signal-pad.gdshader") + scene("S5-face-on-square.gd") + ["--call-at", f"{0.34 * DUR['B27']:.2f}:fire"], DUR["B27"], probes=[("0.2f", "0.5,0.5"), ("0.85f", "0.5,0.5")])
if want("C11"): run("C11", "tween", sh("12-signal-pad.gdshader") + scene("S5-face-on-square.gd") + ["--call-at", f"{0.04 * DUR['B28']:.2f}:set_start", "--call-at", f"{0.19 * DUR['B28']:.2f}:start_tween"], DUR["B28"], probes=[("0.1f", "0.5,0.5"), ("0.85f", "0.5,0.5")])
if want("C12"): run("C12", "pad-face-sweep", sh("12-signal-pad.gdshader") + ["--kind", "quad3d", "--animate", "activation:0:1"], DUR["B34"], probes=[("0.5f", "0.5,0.5"), ("0.97f", "0.5,0.5")])
if want("C13"): run("C13", "pad-face-held", sh("12-signal-pad.gdshader") + ["--kind", "quad3d", "--set", "activation=0.3"], 0.1, still=True, probes=[("0", "0.03125,0.5"), ("0", "0.09375,0.5")])
if want("C14"): run("C14", "box-vs-square", sh("12-signal-pad.gdshader") + scene("S1-pad.gd") + ["--set", "activation=0.3"], DUR["B36"], "two")
def pair(cid, name, shader, L, still, extra, probes=()):
    parts = {}
    for rend in ("forward_plus", "gl_compatibility"):
        pn = f"{name}-{rend}"
        ok = run(cid, pn, sh(shader) + ["--kind", "quad3d"] + extra, L, still=still, renderer=rend, dest=TMP, size="1920x2160", probes=probes)
        parts[rend] = TMP / (pn + (".png" if still else ".mp4"))
    hstack(parts["forward_plus"], parts["gl_compatibility"], DEST / (name + (".png" if still else ".mp4")))
    print(cid, name, "joined: Forward+ left, Compatibility right", flush=True)
if want("C15"): pair("C15", "pad-two-renderers", "12-signal-pad.gdshader", DUR["B37"], False, ["--animate", "activation:0:0,0.44f:0.7,1f:0.7", "--tail", "0.6"][:2] + ["--animate", "activation:0:0,0.44f:0.7,1f:0.7"][2:] if False else ["--animate", "activation:0:0,0.44f:0.7,1f:0.7"], [("0.5f", "0.5,0.5")])
if want("C16"): pair("C16", "pad-two-renderers-half", "12-signal-pad.gdshader", 0.1, True, ["--set", "activation=0.5"], [("0", "0.03125,0.5"), ("0", "0.09375,0.5")])
if want("C17"): pair("C17", "grey-two-renderers", "14-grey-3d.gdshader", 0.1, True, [], [("0", "0.5,0.5")])
if want("C18"): run("C18", "wrong-type", scene("S6-wrong-type.gd") + ["--call-at", f"{0.12 * DUR['B07']:.2f}:give_shaders"], DUR["B07"], probes=[("0.05f", "0.4,0.5"), ("0.9f", "0.4,0.5"), ("0.9f", "0.6,0.5")])
