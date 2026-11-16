#!/usr/bin/env python3
"""Act II arithmetic, recomputed from the frozen sources. Everything the film shows for B15, B16, B13 and B18 is checked here.
Run:  python3 evidence/act2/verify_arithmetic.py        (exit 1 on any mismatch)
Inputs: evidence/example/sources/signal.gdshader (the colour line + defaults), evidence/example/controlled-predictions.json,
        evidence/example/sources/assignment-05.md line 91 (the encode function), evidence/EVIDENCE-NOTES.md hint table.
"""
import json, re, sys
from pathlib import Path
REEL = Path(__file__).resolve().parents[2]
SRC = REEL / "evidence/example/sources"
bad = 0
def ok(cond, msg):
    global bad
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond: bad += 1

# ---------------------------------------------------------------- B15: the pad, by hand
sh = (SRC / "signal.gdshader").read_text().splitlines()
def vec4(line):
    return tuple(float(v) for v in re.search(r"vec4\(([^)]*)\)", line).group(1).split(","))
quiet = vec4(sh[3])[:3]; active = vec4(sh[4])[:3]            # lines 4 and 5
ok(quiet == (0.40, 0.16, 0.09) and active == (0.12, 0.72, 0.52), f"signal.gdshader line 4 quiet_color {quiet}, line 5 active_color {active}")
ok("mix(0.65, 1.0, stripe)" in sh[8] and "mix(base, active_color.rgb, activation)" in sh[9], "line 9 is the stripe scale mix(0.65, 1.0, stripe); line 10 is the colour line")
ok(sh[1].strip() == "render_mode unshaded;", "line 2 is render_mode unshaded;")
def px(activation, stripe):
    f = 0.65 + (1.0 - 0.65) * stripe                          # mix(0.65, 1.0, stripe)
    base = tuple(c * f for c in quiet)
    return tuple(b + (a - b) * activation for b, a in zip(base, active))   # mix(base, active, activation)
def rgb8(v):
    return tuple(int(max(0, min(255, round(x * 255 + 1e-9)))) for x in v)
pred = json.load(open(REEL / "evidence/example/controlled-predictions.json"))
for r in pred["rows"]:
    stripe = 0 if r["stripe"] == "dark" else 1
    v = px(r["activation"], stripe)
    raw_ok = all(abs(a - b) < 1e-9 for a, b in zip(v, r["raw"]))
    ok(raw_ok and list(rgb8(v)) == r["predicted_display_rgb8_compatibility"],
       f"activation {r['activation']:<3} {r['stripe']:<5} raw {tuple(round(x,4) for x in v)} -> x255 {rgb8(v)}  (json: {r['predicted_display_rgb8_compatibility']})")
d = px(0, 0)
print("B15 dark stripe at 0, step by step:")
print("   quiet_color            ", quiet)
print("   x 0.65                 ", tuple(round(c * 0.65, 4) for c in quiet), "exact floats", d)
print("   x 255 (unrounded)      ", tuple(round(c * 255, 2) for c in d))
print("   rounded                ", rgb8(d))
ok(rgb8(d) == (66, 27, 15) and tuple(round(c * 0.65, 4) for c in quiet) == (0.26, 0.104, 0.0585), "B15 spoken numbers: point six five -> sixty-six, twenty-seven, fifteen")
ok(rgb8(px(0.5, 0)) == (48, 105, 74) and rgb8(px(1, 0)) == (31, 184, 133), "B15 on screen: dark stripe at 0.5 -> (48, 105, 74), at 1 -> (31, 184, 133)")

# ---------------------------------------------------------------- B16: the hint experiment's prediction
def encode(x):                                               # assignment-05.md line 91
    return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
def decode(y):
    return y / 12.92 if y <= 0.04045 else ((y + 0.055) / 1.055) ** 2.4
line91 = (SRC / "assignment-05.md").read_text().splitlines()[90]
ok("12.92x" in line91 and "0.0031308" in line91 and "1.055" in line91 and "2.4" in line91, "assignment line 91 states the encode function")
print("B16 greys:")
want = {64: 137, 128: 188, 192: 225}
for b, w in want.items():
    x = b / 255; e = encode(x)
    ok(round(e * 255) == w, f"byte {b}: x={x:.5f} encode={e:.5f} x255={e*255:.4f} -> {round(e*255)}  (spoken/on screen {w})")
    ok(round(encode(decode(x)) * 255) == b, f"byte {b} read as colour: decode then encode returns {round(encode(decode(x))*255)} (unchanged)")
notes = (REEL / "evidence/EVIDENCE-NOTES.md").read_text()
ok(all(f"**{w}**" in notes for w in want.values()), "EVIDENCE-NOTES.md hint table lists 137 / 188 / 225")
# the curve drawn in B16 (x = byte/255, y = encode(x)) at a few points, for the plot's labels
print("curve samples:", [(round(x, 3), round(encode(x), 3)) for x in (0.0, 0.25098, 0.50196, 0.75294, 1.0)])

# ---------------------------------------------------------------- B13: the rule; B18: frame counting
ok(abs(0.6 * 30 - 18) < 1e-9 and abs(0.6 * 60 - 36) < 1e-9 and abs(0.6 * 144 - 86.4) < 1e-9, "0.6 s holds 18 frames at 30, 36 at 60, 86.4 at 144 (B13 ticks are drawn denser, no count is shown)")
for fps, want_s in ((30, 1.2), (60, 0.6), (144, 0.25)):
    t = 36 / fps
    ok(abs(t - want_s) < 1e-12, f"B18 example: 36 frames / {fps} fps = {t} s")
garden = (SRC / "garden.gd").read_text().splitlines()
ok(garden[3] == "const CHARGE_SECONDS := 0.6" and garden[10] == "var charge := 0.0", "garden.gd line 4 const CHARGE_SECONDS := 0.6; line 11 var charge := 0.0")
ok('pad_material.set_shader_parameter("activation", charge / CHARGE_SECONDS)' in garden[252], "garden.gd line 253 sets activation = charge / CHARGE_SECONDS")
ok("charge = minf(CHARGE_SECONDS, charge + delta)" in garden[227], "garden.gd line 228 caps charge at CHARGE_SECONDS, so activation ends at 1.0")
ok("not charging" in garden[221], "garden.gd line 222: a second E press while charging is ignored (not charging)")

# ---------------------------------------------------------------- the code literals embedded in scenes_act2.py are verbatim copies
import ast
tree = ast.parse((REEL / "scenes_act2.py").read_text())
lits = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id.startswith("A2_"):
        try:
            lits[node.targets[0].id] = ast.literal_eval(node.value)
        except Exception:
            pass
frozen = {"A2_SIGNAL": (SRC / "signal.gdshader").read_text().splitlines(),
          "A2_GIT": (REEL / "evidence/act2/b09-git-output-manim.txt").read_text().splitlines()}
for name, want in frozen.items():
    ok(lits.get(name) == want, f"scenes_act2.py {name} is identical to its source file ({len(want)} lines)")


# the prediction table drawn in B15 (A2_PRED) and the two garden.gd lines drawn in B10 are verbatim
pred_lit = lits.get("A2_PRED")
want = {}
for r in pred["rows"]:
    want.setdefault(r["activation"], {})[r["stripe"]] = tuple(r["predicted_display_rgb8_compatibility"])
for a in (0.0, 0.5, 1.0):
    ok(pred_lit is not None and pred_lit[a] == (want[a]["dark"], want[a]["light"]), f"A2_PRED[{a}] dark {want[a]['dark']} light {want[a]['light']} equals controlled-predictions.json")
src = (REEL / "scenes_act2.py").read_text()
for lineno, text in ((4, "const CHARGE_SECONDS := 0.6"), (11, "var charge := 0.0")):
    ok(garden[lineno - 1] == text and f'a2_code(["{text}"]' in src, f"B10 draws garden.gd line {lineno} verbatim: {text}")
# the five Act II colour chips are computed, not typed: defaults x 255
ok(rgb8(quiet) == (102, 41, 23) and rgb8(active) == (31, 184, 133), "B11 colour chips: quiet_color x255 = (102, 41, 23), active_color x255 = (31, 184, 133)")


# numbers typed into the scenes match what was computed above
for needle, why in (("PRED = [137, 188, 225]", "B16 predicted greys"), ('GREYS = [64, 128, 192]', "B16 file greys"),
                    ('"(0.40, 0.16, 0.09)"', "B15 quiet_color tuple"), ('"(0.26, 0.104, 0.0585)"', "B15 product tuple"), ('"(66, 27, 15)"', "B15 result tuple"),
                    ('SEC_S = ["1.2 s", "0.6 s", "0.25 s"]', "B18 seconds"), ('FPS = [30, 60, 144]', "B18 rates"), ('SEC = [1.2, 0.6, 0.25]', "B18 bar scale")):
    ok(needle in src, f"scenes_act2.py carries {why}: {needle}")

print("\nALL PASS" if not bad else f"\n{bad} FAILURE(S)")
sys.exit(1 if bad else 0)
