"""lab_tools.py: small helpers shared by the planning-check scripts of this film.

run_lab(): runs ../../../_godot-shaders-series/lab/check_shader.sh (real Godot 4.7.2, serialized by the Lab's own lock) and returns the RESULT line.
table_shader(): writes a "table" shader: five vertical bands across UV.x, band k evaluates the expression at the exact value xs[k]
(so a function can be probed at x = 0, 0.25, 0.5 ... exactly, not at a pixel centre). The output is encoded as COLOR = (v * scale + offset)
so that negative or large values survive the 8-bit frame buffer; decode() undoes it. Probes are read at the band centres.
"""
import json
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
LAB = FILM.parent / "_godot-shaders-series" / "lab" / "check_shader.sh"
BAND_CENTRES = [0.1, 0.3, 0.5, 0.7, 0.9]


def run_lab(shader, args, label, log):
    """Run one Lab check. Appends a record (command, exit code, raw output) to the list `log` and returns the parsed RESULT dict (or None)."""
    cmd = [str(LAB), str(shader)] + [str(a) for a in args]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    out = (p.stdout + p.stderr).strip()
    rec = {"check": label, "command": " ".join(cmd[1:]).replace(str(FILM) + "/", ""), "exit": p.returncode,
           "seconds": round(time.time() - t0, 1), "output": out}
    log.append(rec)
    result = None
    for line in out.splitlines():
        if line.startswith("RESULT "):
            try:
                result = json.loads(line[len("RESULT "):])
            except Exception:  # noqa: BLE001
                pass
    return result


def table_shader(path, xs, expr, scale=1.0, offset=0.0, decls=""):
    """Write a five-band table shader. `expr` is GLSL using the float `x`; the band's value is v = expr."""
    assert len(xs) == 5
    picks = " else ".join(f"if (k == {i}) {{ x = {float(xs[i])!r}; }}" for i in range(5))
    code = f"""shader_type canvas_item;
{decls}
void fragment() {{
	int k = min(int(floor(UV.x * 5.0)), 4);
	float x = 0.0;
	{picks}
	float v = {expr};
	COLOR = vec4(vec3(v * {float(scale)!r} + {float(offset)!r}), 1.0);
}}
"""
    Path(path).write_text(code)
    return code


def decode(result, scale=1.0, offset=0.0):
    """Read the five band-centre probes of a table run and undo the encoding. Returns a list of five floats (None on failure)."""
    if not result or not result.get("ok"):
        return None
    vals = []
    for pr in result["probes"]:
        r, g, b, _ = pr["rgba"]
        vals.append(round((r - offset) / scale, 5))
    return vals


def probes_arg(points):
    out = []
    for x, y in points:
        out += ["--probe", f"{x},{y}"]
    return out
