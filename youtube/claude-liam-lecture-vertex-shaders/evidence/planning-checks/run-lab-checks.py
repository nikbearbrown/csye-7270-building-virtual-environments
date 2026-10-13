#!/usr/bin/env python3
"""run-lab-checks.py: runs every shader this film shows (and the verification-only shaders) through the Shader Lab
(../../../_godot-shaders-series/lab/check_shader.sh = a real Godot 4.7.2 window) and records what came out.

Output:  lab-results.jsonl  (one line per check: name, the exact command line, exit code, the RESULT line or the compiler message)
         png/<name>.png      (the rendered frame of every check)
Safe to re-run; it overwrites its own outputs. Machine: Apple M4 Pro, macOS, Godot 4.7.2 stable, Forward+ unless a check says otherwise.
Probe positions are given in PIXELS (x, y) of the window and converted to the Lab's normalised 0..1 positions.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
LAB = FILM.parent / "_godot-shaders-series" / "lab" / "check_shader.sh"
SH = FILM / "lab-shaders"
CK = HERE / "check-shaders"
PNG = HERE / "png"
PNG.mkdir(exist_ok=True)
RES = HERE / "lab-results.jsonl"


def probe(x, y, w=640, h=360):
    """normalised position whose Lab pixel is exactly (x, y): the Lab uses int(p * (size - 1))"""
    return f"{(x + 0.25) / (w - 1):.6f},{(y + 0.25) / (h - 1):.6f}"


def run(name, shader, args, out):
    png = PNG / f"{name}.png"
    cmd = [str(LAB), str(shader)] + args + ["--png", str(png)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    text = (p.stdout + p.stderr).strip()
    rec = {"check": name, "shader": str(Path(shader).relative_to(FILM)), "exit": p.returncode,
           "cmd": "lab/check_shader.sh " + Path(shader).name + " " + " ".join(args + ["--png", f"png/{name}.png"]), "output": text}
    out.write(json.dumps(rec) + "\n")
    out.flush()
    status = "ok " if p.returncode == 0 else f"[{p.returncode}]"
    print(status, name)
    return rec


def main():
    c = (320, 180)
    left, right, top, bottom = 258, 381, 118, 241        # two pixels inside each edge of a 128 px sprite at scale 1.0 in the 640 x 360 window
    checks = []

    def add(name, shader, args):
        checks.append((name, shader, args))

    SP = ["--kind", "sprite", "--sprite-tex", "white", "--sprite-scale", "1.0"]
    SPC = ["--kind", "sprite", "--sprite-tex", "checker", "--sprite-scale", "1.0"]
    # ---------- Act I: slide, local space, squash, lean ----------
    add("c0-plain-white", CK / "c0-noop.gdshader", SP)
    add("c0-plain-checker", CK / "c0-noop.gdshader", SPC)
    add("c0-plain-white-scale2", CK / "c0-noop.gdshader", ["--kind", "sprite", "--sprite-tex", "white", "--sprite-scale", "2.0"])
    add("c0-plain-white-scale2.25-lab-default", CK / "c0-noop.gdshader", ["--kind", "sprite", "--sprite-tex", "white"])
    add("01-slide-white", SH / "01-slide.gdshader", SP)
    add("01-slide-checker", SH / "01-slide.gdshader", SPC)
    add("01-slide-white-scale2", SH / "01-slide.gdshader", ["--kind", "sprite", "--sprite-tex", "white", "--sprite-scale", "2.0"])
    add("01-slide-white-scale2.25-lab-default", SH / "01-slide.gdshader", ["--kind", "sprite", "--sprite-tex", "white"])
    add("02-squash-white", SH / "02-squash.gdshader", SP)
    add("02-squash-checker", SH / "02-squash.gdshader", SPC)
    add("03-lean-white", SH / "03-lean.gdshader", SP)
    add("03-lean-checker", SH / "03-lean.gdshader", SPC)
    # VERTEX and UV at the corners, as colours through a varying (check-shader c1): 0 at -64, 1 at +64 for VERTEX; blue = UV.x
    add("c1-vertex-local-scale1", CK / "c1-vertex-local.gdshader",
        SP + ["--probe", probe(left, top), "--probe", probe(right, top), "--probe", probe(left, bottom), "--probe", probe(right, bottom), "--probe", probe(*c)])
    add("c1-vertex-local-scale2.25-lab-default", CK / "c1-vertex-local.gdshader",
        ["--kind", "sprite", "--sprite-tex", "white",
         "--probe", probe(178, 38), "--probe", probe(461, 38), "--probe", probe(178, 321), "--probe", probe(461, 321), "--probe", probe(*c)])
    add("c4-uv-passes-through", CK / "c4-uv-passes-through.gdshader", SP + ["--probe", probe(left, c[1]), "--probe", probe(right, c[1]), "--probe", probe(*c)])
    # ---------- Act II: the ripple on four vertices ----------
    add("04-ripple-white", SH / "04-ripple.gdshader", SP)
    add("04-ripple-checker", SH / "04-ripple.gdshader", SPC)
    # ---------- Act III: the flag steps on four vertices (compile, and the four-vertex behaviour) ----------
    add("05-flag-travelling-white", SH / "05-flag-travelling.gdshader", SP)
    add("06-flag-pinned-white", SH / "06-flag-pinned.gdshader", SP)
    add("07-flag-dials-white", SH / "07-flag-dials.gdshader", SP)
    add("07-flag-dials-amplitude0", SH / "07-flag-dials.gdshader", SP + ["--set", "amplitude=0.0"])
    # ---------- Act IV: varying ----------
    corner_probes = ["--probe", probe(left, top), "--probe", probe(right, top), "--probe", probe(left, bottom), "--probe", probe(right, bottom),
                     "--probe", probe(c[0], top), "--probe", probe(left, c[1]), "--probe", probe(*c), "--probe", probe(right, c[1]), "--probe", probe(c[0], bottom)]
    add("08-corner-colors", SH / "08-corner-colors.gdshader", SP + corner_probes)
    add("08-corner-colors-gl_compatibility", SH / "08-corner-colors.gdshader", SP + corner_probes + ["--renderer", "gl_compatibility"])
    add("09-corner-colors-flat", SH / "09-corner-colors-flat.gdshader", SP + corner_probes + ["--probe", probe(300, 140), "--probe", probe(340, 220)])
    add("10-flag-lit-checker", SH / "10-flag-lit.gdshader", SPC)
    add("11-flag-final-checker", SH / "11-flag-final.gdshader", SPC)
    stripe_probes = ["--probe", probe(left, c[1]), "--probe", probe(c[0] - 30, c[1]), "--probe", probe(*c), "--probe", probe(c[0] + 30, c[1]), "--probe", probe(right, c[1])]
    add("12-stripes-from-vertex", SH / "12-stripes-from-vertex.gdshader", SP + stripe_probes)
    add("13-stripes-from-fragment", SH / "13-stripes-from-fragment.gdshader", SP + stripe_probes)
    add("c6-varying-written-in-fragment-read-in-vertex", CK / "c6-varying-written-in-fragment-read-in-vertex.gdshader", ["--kind", "sprite", "--sprite-tex", "white"])
    add("c7-varying-assigned-in-vertex-only", CK / "c7-varying-assigned-in-vertex-only.gdshader", ["--kind", "sprite", "--sprite-tex", "white", "--probe", probe(*c)])
    # ---------- Act V: VERTEX in vertex() against VERTEX in fragment(), in a 1280 x 720 window; and a far slide ----------
    W2, H2 = 1280, 720
    c2 = (640, 360)
    pos_probes = ["--probe", probe(578, 298, W2, H2), "--probe", probe(*c2, W2, H2), "--probe", probe(702, 422, W2, H2)]
    big = ["--kind", "sprite", "--sprite-tex", "white", "--sprite-scale", "1.0", "--size", "1280x720"]
    add("14-position-from-fragment", SH / "14-position-from-fragment.gdshader", big + pos_probes)
    add("15-position-from-vertex", SH / "15-position-from-vertex.gdshader", big + pos_probes)
    add("14-position-from-fragment-gl_compatibility", SH / "14-position-from-fragment.gdshader", big + pos_probes + ["--renderer", "gl_compatibility"])
    add("15-position-from-vertex-gl_compatibility", SH / "15-position-from-vertex.gdshader", big + pos_probes + ["--renderer", "gl_compatibility"])
    add("16-slide-far-white", SH / "16-slide-far.gdshader", SP)
    # ---------- the pixel counts do not depend on the renderer ----------
    add("01-slide-white-gl_compatibility", SH / "01-slide.gdshader", SP + ["--renderer", "gl_compatibility"])
    add("03-lean-white-gl_compatibility", SH / "03-lean.gdshader", SP + ["--renderer", "gl_compatibility"])

    only = sys.argv[1:]
    with RES.open("w") as out:
        for name, shader, args in checks:
            if only and not any(o in name for o in only):
                continue
            run(name, shader, args, out)
    print("wrote", RES)


if __name__ == "__main__":
    main()
