#!/usr/bin/env python3
"""captures.py: records every Godot capture of this film with the shared harness (S/lab/capture_shader.sh).
Each clip is recorded at its beat's MEASURED duration (beat_sheet.json actual_duration_s) and every scripted event is a FRACTION of it (the 'f'
suffix), taken from the lanes' `show` cues, so the picture lands on the words. Output: TK/runtime/remotion/public/godot-shaders/.
  python3 captures.py [--only C01 C02 ...] [--list]
"""
import json, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent
S = R.parent / "_godot-shaders-series"
LAB = S / "lab"
DEST = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/godot-shaders")
SH = R / "lab-shaders"
sheet = json.loads((R / "beat_sheet.json").read_text())
DUR = {b["beat_id"]: float(b["actual_duration_s"]) for b in sheet["beats"] if b.get("actual_duration_s")}
def sh(n): return ["--shader", str(SH / n)]
SC = str(LAB / "scenes")
# id, beat, output name, still?, args
C = [
 ("C01", "B01", "hook",          False, sh("02-hook-wobble.gdshader") + ["--kind", "sprite", "--material-at", "2.0"]),
 ("C02", "B06", "gradient",      True,  sh("01-gradient.gdshader") + ["--kind", "rect", "--probe-at", "0:0.02,0.5", "--probe-at", "0:0.5,0.5", "--probe-at", "0:0.98,0.5"]),
 ("C03", "B13", "red",           True,  sh("03-red.gdshader") + ["--kind", "rect", "--probe-at", "0:0.5,0.5"]),
 ("C03b", "B16", "lean",         False, sh("04-lean.gdshader") + ["--kind", "sprite", "--sprite-tex", "checker", "--sprite-scale", "1.0", "--material-at", "0.2f"]),
 ("C04", "B20", "discard",       True,  sh("05-discard-half.gdshader") + ["--kind", "rect", "--probe-at", "0:0.25,0.5", "--probe-at", "0:0.75,0.5"]),
 ("C05", "B21", "light-count",   False, sh("13-light-count.gdshader") + ["--scene", f"{SC}/light_count.gd", "--call-at", "0.28f:add_light", "--call-at", "0.58f:add_light", "--call-at", "0.83f:add_light",
                                       "--probe-at", "0.2f:0.5,0.5", "--probe-at", "0.45f:0.5,0.5", "--probe-at", "0.75f:0.5,0.5", "--probe-at", "0.97f:0.5,0.5"]),
 ("C06a", "B26", "dial-default", True,  sh("06-dial.gdshader") + ["--kind", "rect", "--probe-at", "0:0.5,0.5"]),
 ("C07", "B28", "mixer",         False, sh("07-mixer.gdshader") + ["--kind", "rect", "--animate", "red:0.06f:0,0.2f:1", "--animate", "green:0.2f:0,0.32f:1", "--animate", "blue:0.32f:0,0.44f:1",
                                       "--probe-at", "0.2f:0.5,0.5", "--probe-at", "0.32f:0.5,0.5", "--probe-at", "0.97f:0.5,0.5"]),
 ("C09", "B31", "set-parameter", False, sh("06-dial.gdshader") + ["--scene", f"{SC}/dial_rect.gd", "--call-at", "0.62f:fire_set", "--probe-at", "0.5f:0.5,0.5", "--probe-at", "0.97f:0.5,0.5"]),
 ("C10", "B32", "typo",          False, sh("06-dial.gdshader") + ["--scene", f"{SC}/dial_rect.gd", "--set", "red=0.2", "--call-at", "0.15f:fire_typo", "--call-at", "0.7f:fire_correct",
                                       "--probe-at", "0.1f:0.5,0.5", "--probe-at", "0.6f:0.5,0.5", "--probe-at", "0.97f:0.5,0.5"]),
 ("C11", "B33", "tween",         False, sh("06-dial.gdshader") + ["--scene", f"{SC}/dial_rect.gd", "--call-at", "0.1f:fire_start", "--call-at", "0.3f:fire_tween",
                                       "--probe-at", "0.2f:0.5,0.5", "--probe-at", "0.97f:0.5,0.5"]),
 ("C12", "B37", "uv-colors",     True,  sh("08-uv-colors.gdshader") + ["--kind", "rect", "--probe-at", "0:0.02,0.02", "--probe-at", "0:0.98,0.02", "--probe-at", "0:0.02,0.98", "--probe-at", "0:0.98,0.98"]),
 ("C13", "B38", "uv-fade",       True,  sh("09-uv-fade.gdshader") + ["--kind", "sprite", "--sprite-tex", "white", "--probe-at", "0:0.05,0.5", "--probe-at", "0:0.30,0.5", "--probe-at", "0:0.70,0.5"]),
 ("C14", "B39", "pulse",         False, sh("10-pulse.gdshader") + ["--kind", "rect", "--probe-at", "0.3f:0.5,0.5", "--probe-at", "0.5f:0.5,0.5"]),
 ("C15", "B40", "time-bar",      False, sh("11-time-bar.gdshader") + ["--scene", f"{SC}/time_bars.gd", "--hold-clock", "2.44", "--call-at", "0.56f:add_right"]),
 ("C16", "B42", "iris-sweep",    False, sh("12-iris.gdshader") + ["--kind", "sprite", "--sprite-tex", "checker", "--animate", "radius:0.1f:0,0.9f:0.8",
                                       "--probe-at", "0:0.5,0.5", "--probe-at", "0.5f:0.5,0.5"]),
 ("C17", "B43", "iris-key",      False, sh("12-iris.gdshader") + ["--scene", f"{SC}/iris_key.gd", "--key-at", "0.6f:Space", "--probe-at", "0.5f:0.5,0.5", "--probe-at", "0.97f:0.5,0.5"]),
]
def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1:]
    if "--list" in sys.argv:
        for c in C: print(c[0], c[1], c[2], DUR.get(c[1])); return
    DEST.mkdir(parents=True, exist_ok=True)
    log = R / "evidence" / "build-captures"; log.mkdir(parents=True, exist_ok=True)
    for cid, bid, name, still, args in C:
        if only and cid not in only: continue
        d = DUR[bid]
        a = ["--length", f"{d:.2f}"] + args
        cmd = [str(LAB / "capture_shader.sh")] + a + ["--name", name, "--dest", str(DEST)]
        if still: cmd += ["--png", "1"]
        print("==", cid, bid, name, f"{d:.2f}s", flush=True)
        r = subprocess.run(cmd, capture_output=True, text=True)
        (log / f"{cid}-{name}.log").write_text(" ".join(cmd) + "\n" + r.stdout + r.stderr)
        res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
        if res:
            j = json.loads(res[0][7:])
            print("   ok" if j.get("ok") else "   NOT OK", [ (p["t"], p["rgba"][:3]) for p in j.get("probes", [])], j.get("events"))
        print("   ", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:], flush=True)
main()
