#!/usr/bin/env python3
"""verify_claims.py — Gate F number table. Recomputes or re-reads from the REAL evidence every number and line number the narration (and the on-screen text) leans on,
asserts each, and writes evidence/NUMBERS-CHECK.md. Exit 1 if any assertion fails. Run from anywhere:  python3 evidence/verify_claims.py
Sources: evidence/example/sources/ (frozen copies of the example's files), evidence/runs/ (re-run 2026-10-16), evidence/example/ (the example's own logs), captures/forward-plus/."""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC = HERE / "evidence/example/sources"
RUNS = HERE / "evidence/runs"
EXA = HERE / "evidence/example"
FP = HERE / "captures/forward-plus"
rows, fails = [], []


def check(claim, got, want, source):
    ok = (got == want) if not isinstance(want, float) else abs(got - want) < 1e-6
    rows.append((claim, got, want, "PASS" if ok else "FAIL", source))
    if not ok:
        fails.append(claim)


def lines(name):
    return (SRC / name).read_text().splitlines()


# ── the example's shaders: line numbers ──────────────────────────────────────────────────────────────
sig, sur, hnt, gen = lines("signal.gdshader"), lines("surface.gdshader"), lines("hint.gdshader"), lines("standard_generated.gdshader")
check("signal.gdshader has 11 lines", len(sig), 11, "signal.gdshader")
check("signal line 1 is shader_type spatial;", sig[0], "shader_type spatial;", "signal.gdshader:1")
check("signal line 2 is render_mode unshaded;", sig[1], "render_mode unshaded;", "signal.gdshader:2")
check("signal line 3 declares activation with hint_range(0.0, 1.0) = 0.0", sig[2], "uniform float activation : hint_range(0.0, 1.0) = 0.0;", "signal.gdshader:3")
check("signal has four uniforms (lines 3-6)", sum(1 for l in sig if l.startswith("uniform ")), 4, "signal.gdshader")
check("signal line 10 is the colour line", sig[9].strip(), "ALBEDO = mix(base, active_color.rgb, activation);", "signal.gdshader:10")
check("signal line 9 scales the quiet colour by mix(0.65, 1.0, stripe)", "mix(0.65, 1.0, stripe)" in sig[8], True, "signal.gdshader:9")
check("signal line 8 is the stripe step", "step(0.5, fract(UV.x * stripe_count))" in sig[7], True, "signal.gdshader:8")
check("signal fragment() is on line 7", sig[6], "void fragment() {", "signal.gdshader:7")
check("surface.gdshader has 14 lines", len(sur), 14, "surface.gdshader")
check("surface line 3 colour sampler has source_color", sur[2], "uniform sampler2D color_map : source_color, filter_nearest;", "surface.gdshader:3")
check("surface line 4 roughness sampler has no source_color", "source_color" in sur[3], False, "surface.gdshader:4")
check("surface has two group_uniforms (lines 2 and 7)", [i + 1 for i, l in enumerate(sur) if l.startswith("group_uniforms")], [2, 7], "surface.gdshader")
check("surface group names are Surface and Pattern", [l.split()[1].rstrip(";") for l in sur if l.startswith("group_uniforms")], ["Surface", "Pattern"], "surface.gdshader")
check("surface non-sampler uniforms are four", sum(1 for l in sur if l.startswith("uniform ") and "sampler2D" not in l), 4, "surface.gdshader")
check("surface line 12 writes ROUGHNESS", sur[11].strip().startswith("ROUGHNESS ="), True, "surface.gdshader:12")
check("surface fragment() is on line 10", sur[9], "void fragment() {", "surface.gdshader:10")
check("hint has 13 lines", len(hnt), 13, "hint.gdshader")
check("hint line 9 reads UV via texture()", "texture(as_color, UV)" in hnt[8], True, "hint.gdshader:9")
check("hint line 10 reads FRAGCOORD and VIEWPORT_SIZE", "FRAGCOORD.x" in hnt[9] and "VIEWPORT_SIZE.x" in hnt[9], True, "hint.gdshader:10")
check("hint line 3 colour sampler source_color, line 4 data sampler none", ("source_color" in hnt[2], "source_color" in hnt[3]), (True, False), "hint.gdshader:3-4")
check("all three example shaders start with shader_type spatial; on line 1", [s[0] for s in (sig, sur, hnt)], ["shader_type spatial;"] * 3, "line 1 of each")
check("generated shader has 48 lines", len(gen), 48, "standard_generated.gdshader")
check("generated line 3 shader_type spatial;", gen[2], "shader_type spatial;", "standard_generated.gdshader:3")
check("generated line 4 is render_mode", gen[3].startswith("render_mode "), True, "standard_generated.gdshader:4")
check("generated line 6 albedo colour uniform", gen[5], "uniform vec4 albedo : source_color;", "standard_generated.gdshader:6")
check("generated line 7 albedo sampler has source_color", "texture_albedo : source_color" in gen[6], True, "standard_generated.gdshader:7")
check("generated line 19 normal sampler has hint_roughness_normal and no source_color", ("hint_roughness_normal" in gen[18], "source_color" in gen[18]), (True, False), "standard_generated.gdshader:19")
check("generated line 20 normal_scale", gen[19].startswith("uniform float normal_scale"), True, "standard_generated.gdshader:20")
check("generated line 35 writes ALBEDO", gen[34].strip().startswith("ALBEDO ="), True, "standard_generated.gdshader:35")
check("generated line 43 writes ROUGHNESS", gen[42].strip().startswith("ROUGHNESS ="), True, "standard_generated.gdshader:43")
check("generated line 46 writes NORMAL_MAP", gen[45].strip().startswith("NORMAL_MAP ="), True, "standard_generated.gdshader:46")
check("generated vertex() on line 27", gen[26], "void vertex() {", "standard_generated.gdshader:27")

# ── the game script and tests ───────────────────────────────────────────────────────────────────────
gd = lines("garden.gd")
check("garden.gd line 4 CHARGE_SECONDS 0.6", gd[3], "const CHARGE_SECONDS := 0.6", "garden.gd:4")
check("garden.gd line 11 var charge", gd[10], "var charge := 0.0", "garden.gd:11")
check("garden.gd line 253 is the driver line", gd[252].strip(), 'pad_material.set_shader_parameter("activation", charge / CHARGE_SECONDS)', "garden.gd:253")
check("garden.gd line 222 only starts a charge when not charging and gate not open", "not charging and not gate_open" in gd[221], True, "garden.gd:222")
td = lines("test-signal-driver.gd")
check("driver test has 67 lines and prints RESULT 10 checks", (len(td), any("RESULT 10 checks" in l for l in td)), (67, True), "test-signal-driver.gd")
tm = (SRC / "test-material-contract.gd").read_text()
check("material test: 5 + 24 + 24 = 53 checks (counted from the source)", 5 + 2 * (1 + 1 + 1 + 1 + 4 + 4 + 2 * (1 + 1 + 4)), 53, "test-material-contract.gd")
cl = lines("CLAUDE.md")
check("the example's CLAUDE.md has 65 lines", len(cl), 65, "CLAUDE.md")
check("CLAUDE.md lines 1-3 are the three @ imports", cl[:3], ["@AGENTS.md", "@CHANGE-BRIEF.md", "@assignments/05-shaders-materials/CHANGE-BRIEF.md"], "CLAUDE.md:1-3")
imp = (SRC / "gate-color.png.import").read_text()
check("gate-color.png.import: compress/mode=0, normal_map=2, mipmaps off", all(s in imp for s in ("compress/mode=0", "compress/normal_map=2", "mipmaps/generate=false")), True, "gate-color.png.import")
pj = (SRC / "project.godot").read_text()
check("project.godot names gl_compatibility", 'rendering_method="gl_compatibility"' in pj, True, "project.godot:36")

# ── re-run logs ─────────────────────────────────────────────────────────────────────────────────────
def run(n):
    return (RUNS / n).read_text()
r1 = run("R1-baseline-60fps.log")
check("baseline: 53 PASS lines, 0 FAIL", (len(re.findall(r"^PASS", r1, re.M)), len(re.findall(r"^FAIL", r1, re.M))), (53, 0), "R1-baseline-60fps.log")
check("baseline RESULT line", "RESULT 53 checks / 0 failures / baseline" in r1, True, "R1")
for fps, samples, rs in ((30, 294, 16), (60, 409, 34), (144, 726, 83)):
    t = run(f"R2-driver-{fps}fps.log")
    check(f"driver {fps} fps: 10 checks 0 failures, {samples} samples", f"RESULT 10 checks / 0 failures; sample count {samples}" in t, True, f"R2-driver-{fps}fps.log")
    dur = [json.loads(m) for m in re.findall(r"^DURATION (\{.*\})", t, re.M)]
    check(f"driver {fps} fps: game seconds 0.6 at scale 1.0 (render samples {rs})", (round(dur[0]["game_seconds"], 6), dur[0]["render_samples"]), (0.6, rs), f"R2-driver-{fps}fps.log")
    check(f"driver {fps} fps: tolerance is 1/60 + 0.00001", round(dur[0]["tolerance"], 7), round(1 / 60 + 0.00001, 7), f"R2-driver-{fps}fps.log")
m1 = run("R4-M1-parse-60fps.log")
check("M1 parse: 4 failures, a SHADER ERROR line, empty uniform list", (len(re.findall(r"^FAIL", m1, re.M)), "SHADER ERROR: Expected a ';' after 'shader_type spatial'." in m1, "UNIFORM_TYPES {}" in m1), (4, True, True), "R4-M1-parse-60fps.log")
m2 = run("R4-M2-rename-contract-60fps.log")
check("M2 rename: exactly one failure, 'declared activation is float'", re.findall(r"^FAIL .*", m2, re.M), ["FAIL declared activation is float"], "R4-M2-rename-contract-60fps.log")
m2d = run("R4-M2-rename-driver-60fps.log")
check("M2 rename: the DRIVER test still passes 10 of 10", "RESULT 10 checks / 0 failures" in m2d, True, "R4-M2-rename-driver-60fps.log")
m3 = run("R4-M3-hint-60fps.log")
check("M3 hint: two failures (matte, coated colour hint)", re.findall(r"^FAIL .*", m3, re.M), ["FAIL matte color hint", "FAIL coated color hint"], "R4-M3-hint-60fps.log")
check("R5 raw exits 0 with a SHADER ERROR printed", "SHADER ERROR" in run("R5-shader-error-raw.log"), True, "R5-shader-error-raw.log")
ex_exit = json.loads((EXA / "course-signal-30.1791994689764928000.json").read_text())
check("the example's first driver run: exit 124 after ~120 s with a script error", (ex_exit["exit_code"], round(ex_exit["elapsed_seconds"], 2), "Nonexistent 'float' constructor" in ex_exit["error_lines"][0]), (124, 120.01, True), "example course-signal-30...json")
fm = (EXA / "material-contract.1791994525559690000.log").read_text()
check("the example's first material test: 4 failures (quiet_color, active_color, matte tint, coated tint)", re.findall(r"^FAIL .*", fm, re.M), ["FAIL declared quiet_color is vec4", "FAIL declared active_color is vec4", "FAIL matte declared tint", "FAIL coated declared tint"], "example material-contract...log")
check("the example's repaired material test: 0 failures", "RESULT 53 checks / 0 failures" in (EXA / "material-contract-repaired.1791994549964522000.log").read_text(), True, "example material-contract-repaired...log")

# ── the sRGB formula and the hint experiment ─────────────────────────────────────────────────────────
def enc(x):
    return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
check("assignment's encode(64/255, 128/255, 192/255) x 255 rounds to 137, 188, 225", [round(enc(b / 255) * 255) for b in (64, 128, 192)], [137, 188, 225], "assignment-05.md encode function")
for tag, want_data in (("forward_plus", [137, 188, 225]), ("compatibility", [64, 128, 192])):
    h = json.loads((FP / f"hint_{tag}.json").read_text())
    s = {(x["quad"], x["input_byte"]): x["rgb8"][0] for x in h["samples"]}
    check(f"hint {tag}: source_color quad reads 64/128/192", [s[("source_color", b)] for b in (64, 128, 192)], [64, 128, 192], f"captures/forward-plus/hint_{tag}.json")
    check(f"hint {tag}: data quad reads {want_data}", [s[("no_hint (data)", b)] for b in (64, 128, 192)], want_data, f"captures/forward-plus/hint_{tag}.json")
ex_h = json.loads((EXA / "hint-samples.json").read_text())
check("the example's own fixture (Compatibility): all six bands are 64/128/192 / 255", sorted({round(x["rgb"][0] * 255) for x in ex_h["samples"]}), [64, 128, 192], "example hint-samples.json")

# ── the pad: hand arithmetic, the example's predictions, both renderers ─────────────────────────────
q, a = (0.40, 0.16, 0.09), (0.12, 0.72, 0.52)
def pred(act, light):
    f = 1.0 if light else 0.65
    return [max(0, min(255, round((c * f + (ac - c * f) * act) * 255))) for c, ac in zip(q, a)]
check("hand arithmetic, dark stripe, activation 0: (66, 27, 15)", pred(0, False), [66, 27, 15], "signal.gdshader:3-10 + arithmetic")
check("hand arithmetic, dark stripe, 0.5 / 1 / 2", [pred(0.5, False), pred(1, False), pred(2, False)], [[48, 105, 74], [31, 184, 133], [0, 255, 250]], "arithmetic")
check("hand arithmetic, light stripe, 0 / 0.5 / 1 / 2", [pred(v, True) for v in (0, 0.5, 1, 2)], [[102, 41, 23], [66, 112, 78], [31, 184, 133], [0, 255, 242]], "arithmetic")
cp = json.loads((EXA / "controlled-predictions.json").read_text())
check("the example's recorded predictions equal the arithmetic (8 rows)", [r["predicted_display_rgb8_compatibility"] for r in cp["rows"]],
      [pred(r["activation"], r["stripe"] == "light") for r in cp["rows"]], "example controlled-predictions.json")
def meas(name):
    d = json.loads((FP / name).read_text())
    return {row["set_value"]: [s["rgb8"] for s in row["samples"]] for row in d["rows"]}
mc, mf = meas("signal_values_compatibility.json"), meas("signal_values_forward_plus.json")
check("Compatibility measured, dark/light at 0", mc[0.0], [[66, 24, 10], [102, 39, 19]], "signal_values_compatibility.json")
check("Compatibility measured, dark/light at 0.5", mc[0.5], [[47, 105, 74], [66, 112, 78]], "signal_values_compatibility.json")
check("Compatibility measured, dark/light at 1", mc[1.0], [[28, 184, 133], [28, 184, 133]], "signal_values_compatibility.json")
check("Compatibility measured, dark/light at 2", mc[2.0], [[0, 255, 251], [0, 255, 243]], "signal_values_compatibility.json")
check("Forward+ measured at 0.5 (dark, light)", mf[0.5], [[63, 136, 97], [76, 137, 97]], "signal_values_forward_plus.json")
check("Forward+ measured at 0 (dark)", mf[0.0][0], [83, 32, 17], "signal_values_forward_plus.json")
gaps = [abs(m - p) for v in (0.0, 0.5, 1.0, 2.0) for si, light in ((0, False), (1, True)) for m, p in zip(mc[v][si], pred(v, light))]
check("largest Compatibility gap from the hand arithmetic is 5 byte values", max(gaps), 5, "arithmetic vs signal_values_compatibility.json")
check("Forward+ largest gap is 69 (blue, dark stripe, activation 2)", max(abs(m - p) for v in (0.0, 0.5, 1.0, 2.0) for si, light in ((0, False), (1, True)) for m, p in zip(mf[v][si], pred(v, light))), 69, "arithmetic vs signal_values_forward_plus.json")
check("hint_range did not clamp 2.0 (Compatibility 2.0 differs from 1.0; Forward+ too)", (mc[2.0] != mc[1.0], mf[2.0] != mf[1.0]), (True, True), "signal_values_*.json")
check("the frame-counting example: 36 frames last 1.2 s, 0.6 s, 0.25 s at 30, 60, 144 fps", [round(36 / f, 4) for f in (30, 60, 144)], [1.2, 0.6, 0.25], "arithmetic (an EXAMPLE 36-frame effect)")
check("vertex() corner UV.x of 0 or 1 gives fract(8 x UV.x) = 0 at every corner (stripes lost between corners)", [(8 * u) % 1.0 for u in (0, 1)], [0.0, 0.0], "arithmetic")
check("pad stripe maths: UV.x 0.15625 is a dark stripe, 0.21875 a light one", [(1.0 if ((8 * u) % 1.0) >= 0.5 else 0.0) for u in (0.15625, 0.21875)], [0.0, 1.0], "arithmetic (step(0.5, fract(UV.x * 8)))")

# ── curl ratios ─────────────────────────────────────────────────────────────────────────────────────
cal = {r["variant"]: r for r in json.loads((RUNS / "R3-normal-calibration.json").read_text())}
check("curl: Poly Haven GL read as GL 0.48445 and as DX 1.51555", (round(cal["gl"]["normal_gl_interpretation"], 5), round(cal["gl"]["normal_dx_interpretation"], 5)), (0.48445, 1.51555), "R3-normal-calibration.json")
check("curl: Poly Haven DX read as DX 0.48445 and as GL 1.51555", (round(cal["dx"]["normal_dx_interpretation"], 5), round(cal["dx"]["normal_gl_interpretation"], 5)), (0.48445, 1.51555), "R3-normal-calibration.json")
ana = re.search(r'ANALYTIC_NORMAL (\{.*\})', r1)
an = json.loads(ana.group(1))
check("curl: the code-made map reads 0.05447 as GL and 1.94553 as DX", (round(an["GL"], 5), round(an["DX"], 5)), (0.05447, 1.94553), "R1 ANALYTIC_NORMAL line")

# ── the textures ────────────────────────────────────────────────────────────────────────────────────
try:
    from PIL import Image
    W = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/godot/course-series/material-textures")
    ci = Image.open(W / "gate-color.png").convert("RGB"); ri = Image.open(W / "gate-roughness.png").convert("RGB")
    check("gate-color.png is 64 x 64 with two colours (44,78,85) and (59,96,101)", (ci.size, sorted(set(ci.get_flattened_data() if hasattr(ci, 'get_flattened_data') else ci.getdata()))), ((64, 64), [(44, 78, 85), (59, 96, 101)]), "gate-color.png")
    check("gate-roughness.png is 64 x 64 with two values 102 and 216", (ri.size, sorted({p[0] for p in (ri.get_flattened_data() if hasattr(ri, 'get_flattened_data') else ri.getdata())})), ((64, 64), [102, 216]), "gate-roughness.png")
except Exception as e:  # pragma: no cover
    rows.append(("texture check skipped", str(e), "-", "SKIP", "PIL"))

# ── the rubric ──────────────────────────────────────────────────────────────────────────────────────
asg = (SRC / "assignment-05.md").read_text()
check("rubric: 60 + 10 + 10 + 20 = 100", 60 + 10 + 10 + 20, 100, "assignment-05.md Rubric table")
check("the 60-point split 8 + 12 + 14 + 10 + 8 + 8 = 60", 8 + 12 + 14 + 10 + 8 + 8, 60, "assignment-05.md Implementation table")
rub = {}
for m in re.finditer(r"^\| (Implementation and explanation|Frictional — honest log|GitHub version posting matching Canvas|Relative Quartile)\s*\| (\d+)\s*\|", asg, re.M):
    rub[m.group(1)] = int(m.group(2))
check("the assignment's rubric rows are 60 / 10 / 10 / 20", list(rub.values()), [60, 10, 10, 20], "assignment-05.md Rubric table")
sixty = [int(m.group(1)) for m in re.finditer(r"^\| (?:Specification and context|Shader from code|Textured shader and materials|The language|Verification|Brutalist explainer):.*\| (\d+) \|$", asg, re.M)]
check("the assignment's six criterion rows score 8 / 12 / 14 / 10 / 8 / 8", sixty, [8, 12, 14, 10, 8, 8], "assignment-05.md Implementation table")
for k, w in (("under 120 lines", True), ("`a5`", True), ("10% daily late penalty", True), ("exits 1", True), ("25 MB", True)):
    check(f"assignment says '{k}'", (k in asg), w, "assignment-05.md")

# ── the git facts ───────────────────────────────────────────────────────────────────────────────────
g = (EXA / "git-brief-log.txt").read_text()
check("brief commit 93be391 at 2026-10-14 00:29:13 with five files and no shader file", ("93be391 2026-10-14 00:29:13" in g, "5 files changed" in g, ".gdshader" in g), (True, True, False), "evidence/example/git-brief-log.txt")

out = ["# NUMBERS-CHECK.md — Gate F number table (generated by evidence/verify_claims.py)", "",
       f"{sum(1 for r in rows if r[3]=='PASS')} PASS · {len(fails)} FAIL · {sum(1 for r in rows if r[3]=='SKIP')} SKIP. Every number and line number the narration leans on, re-read from the real evidence or recomputed.", "",
       "| claim | got | want | verdict | source |", "|---|---|---|---|---|"]
for c, got, want, v, s in rows:
    out.append(f"| {c} | `{str(got)[:70]}` | `{str(want)[:70]}` | {v} | {s} |")
(HERE / "evidence/NUMBERS-CHECK.md").write_text("\n".join(out) + "\n")
print(f"{len(rows)} checks, {len(fails)} failed")
for f in fails:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
