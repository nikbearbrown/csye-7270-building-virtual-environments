#!/usr/bin/env python3
"""run_scenes.py: plays every scene spec in scenes/ with the reference runner run_scene.sh at the times that matter: the film's 50 % and 85 % frames, the
last frame, and 0.3 s after every keyframe (the settled state each change leads to). Frames go to png/scenes/; analyze_scenes.py then measures them.
Usage: python3 run_scenes.py [scene id ...]"""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent


def key_times(spec):
    ts = set()
    def walk(v):
        if isinstance(v, dict):
            if "keys" in v:
                for k in v["keys"]:
                    ts.add(float(k[0]))
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(spec.get("sprites", []))
    for ev in spec.get("input", []):
        ts.add(float(ev["t"]))
    for sp in spec.get("sprites", []):
        if "instance_from" in sp:
            ts.add(float(sp["instance_from"]))
    return sorted(ts)


def times_for(spec):
    dur = float(spec["duration"])
    ts = {0.05, round(dur * 0.5, 2), round(dur * 0.85, 2), round(dur - 0.05, 2)}
    ks = key_times(spec)
    for k in ks:
        ts.add(round(min(k + 0.3, dur - 0.05), 2))
    for a, b in zip(ks, ks[1:]):                      # two frames inside every ramp, to see the motion between keyframes
        for f in (0.35, 0.7):
            ts.add(round(a + (b - a) * f, 2))
    return sorted(ts)


if __name__ == "__main__":
    want = sys.argv[1:]
    for f in sorted((HERE / "scenes").glob("*.json")):
        d = json.loads(f.read_text())
        if want and d["id"] not in want:
            continue
        out = subprocess.run([str(HERE / "run_scene.sh"), str(f), "--times", ",".join(str(t) for t in times_for(d))], capture_output=True, text=True)
        print(d["id"], "OK" if '"spec"' in out.stdout else "FAILED: " + (out.stdout + out.stderr)[:300])
