"""twin_lib.py: shared helpers for run_twins.py (pixel probes) and run_images.py (whole-picture checks).

A shader that reads TIME cannot be probed at a chosen time in the Shader Lab. So each shown shader is copied to a TWIN that differs in
exactly three ways: every TIME is replaced by a uniform `tv`, the line `uniform float tv = 0.0;` is added after `shader_type`, and
`instance uniform` becomes `uniform` (the Lab sets uniforms through the material). The Lab then renders the twin at chosen values of tv.
The shown shader files themselves are run with the real TIME in verify2.gd and verify3.gd (pixel against the TIME decoded in the same
frame) and compile and render in the Lab.
"""
import json
import math
import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parent.parent
SHADERS = FILM / "lab-shaders"
TWINS = HERE / "twins"
RENDERER = os.environ.get("TWIN_RENDERER", "")          # set TWIN_RENDERER=gl_compatibility to run everything in the Compatibility renderer
SUFFIX = "" if not RENDERER else "-" + {"gl_compatibility": "compat"}.get(RENDERER, RENDERER)
PNG = HERE / f"png{SUFFIX}"
LAB = FILM.parent / "_godot-shaders-series" / "lab" / "check_shader.sh"
TWINS.mkdir(exist_ok=True)
PNG.mkdir(exist_ok=True)

TEAL = (0.37, 0.64, 0.57)
CREAM = (0.98, 0.97, 0.96)
STAGE = (0.851, 0.8353, 0.7922)       # the Lab's clear color #D9D5CA
TRACK = (0.93, 0.92, 0.88)             # the unfilled part of a bar in 04-three-shapes
TAU = 2 * math.pi

results = []
fails = 0


def make_twin(name):
    src = (SHADERS / name).read_text()
    out = []
    for ln in src.split("\n"):
        ln = re.sub(r"\bTIME\b", "tv", ln)
        ln = ln.replace("instance uniform", "uniform")
        out.append(ln)
        if ln.startswith("shader_type"):
            out.append("uniform float tv = 0.0;")
    twin = TWINS / (name.replace(".gdshader", ".twin.gdshader"))
    twin.write_text("\n".join(out))
    return twin


def mix(a, b, t):
    return tuple(x * (1 - t) + y * t for x, y in zip(a, b))


def pulse_color(p):
    return mix(TEAL, CREAM, p)


def lab(shader_path, args, png=None):
    cmd = [str(LAB), str(shader_path)] + args + (["--png", str(png)] if png else []) + (["--renderer", RENDERER] if RENDERER else [])
    p = subprocess.run(cmd, capture_output=True, text=True)
    line = [ln for ln in p.stdout.splitlines() if ln.startswith("RESULT ")]
    if p.returncode != 0 or not line:
        return {"ok": False, "error": (p.stdout + p.stderr)[-600:], "cmd": " ".join(cmd)}
    r = json.loads(line[0][len("RESULT "):])
    r["cmd"] = " ".join(cmd)
    return r


def check(label, shader, args, probes_expected, tol=1.01, png=None):
    """probes_expected: list of ((x, y), (r, g, b[, a]) expected). Compared in 8-bit steps; tol in steps."""
    global fails
    twin = make_twin(shader)
    pargs = list(args)
    for (x, y), _ in probes_expected:
        pargs += ["--probe", f"{x},{y}"]
    r = lab(twin, pargs, png=png)
    row = {"check": label, "shader": shader, "args": args, "ok": False, "details": []}
    if not r.get("ok"):
        row["error"] = r.get("error")
        results.append(row)
        fails += 1
        print(f"[FAIL] {label}: Lab error {r.get('error')}")
        return
    good = True
    for p, ((x, y), exp) in zip(r["probes"], probes_expected):
        got = p["rgba"]
        diffs = [abs(got[i] * 255 - exp[i] * 255) for i in range(len(exp))]
        ok = max(diffs) <= tol
        good &= ok
        row["details"].append({"at": [x, y], "got": got[:len(exp)], "expected": [round(v, 4) for v in exp], "max_step_diff": round(max(diffs), 2), "ok": ok})
    row["ok"] = good
    row["renderer"] = r.get("renderer")
    row["cmd"] = r.get("cmd")
    results.append(row)
    if not good:
        fails += 1
    print(f"[{'PASS' if good else 'FAIL'}] {label}")
    if not good:
        for d in row["details"]:
            if not d["ok"]:
                print("        ", d)


def record(label, ok, detail, cmd=""):
    global fails
    results.append({"check": label, "ok": bool(ok), "details": detail, "cmd": cmd})
    if not ok:
        fails += 1
    print(f"[{'PASS' if ok else 'FAIL'}] {label}  {detail if not ok else ''}")


def lab_png(label, shader, args):
    """Render a twin at the given args and return (image as int array, RESULT dict)."""
    from PIL import Image
    import numpy as np
    twin = make_twin(shader)
    out = PNG / f"{label}.png"
    r = lab(twin, args, png=out)
    if not r.get("ok"):
        print(f"[FAIL] {label}: {r.get('error')}")
        return None, r
    return np.asarray(Image.open(out).convert("RGB")).astype(int), r


def finish(prefix):
    n_ok = sum(1 for r in results if r["ok"])
    ren = RENDERER or next((r.get("renderer") for r in results if r.get("renderer")), "forward_plus")
    prefix = prefix + SUFFIX
    (HERE / f"{prefix}-results.jsonl").write_text("".join(json.dumps(r) + "\n" for r in results))
    summary = f"{n_ok}/{len(results)} {prefix} checks passed (Godot 4.7.2, {ren}, tolerance about one 8-bit step)\n"
    (HERE / f"{prefix}-summary.txt").write_text(summary)
    print(summary)
    return 1 if fails else 0
