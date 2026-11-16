#!/usr/bin/env python3
"""verify_numbers.py — asserts that every pixel number Act IX (scenes_act9.py) puts on screen equals the value in the evidence files.
Run from anywhere:  python3 evidence/act9/verify_numbers.py     (exit 0 = every number matches; prints each check)
Sources: evidence/example/controlled-predictions.json (the example's predictions), captures/forward-plus/signal_values_{compatibility,forward_plus}.json,
         evidence/example/material-native-results.json (the example's own native Compatibility readings), evidence/runs/R9-constant-albedo-compatibility.json.
"""
import ast, json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[2]
src = (HERE / "scenes_act9.py").read_text()
tree = ast.parse(src)
consts = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id.startswith("A9_"):
        try:
            consts[node.targets[0].id] = ast.literal_eval(node.value)
        except Exception:
            pass
bad = 0


def check(label, ok):
    global bad
    print(("OK   " if ok else "FAIL ") + label)
    bad += 0 if ok else 1


pred = {(r["activation"], r["stripe"]): r["predicted_display_rgb8_compatibility"] for r in json.load(open(HERE / "evidence/example/controlled-predictions.json"))["rows"]}
comp = json.load(open(HERE / "captures/forward-plus/signal_values_compatibility.json"))["rows"]
fpl = json.load(open(HERE / "captures/forward-plus/signal_values_forward_plus.json"))["rows"]
nat = [r for r in json.load(open(HERE / "evidence/example/material-native-results.json"))["rows"] if r.get("case") == "signal"]


def sample(rows, a, j):
    return [r for r in rows if r["set_value"] == a][0]["samples"][j]["rgb8"]


# B61: predicted vs measured, dark stripe (uv_x 0.15625, sample index 0)
for key, a in (("0", 0), ("0.5", 0.5), ("1", 1), ("2", 2)):
    check(f"B61 predicted dark @ {key}: {consts['A9_PRED'][key]} == controlled-predictions {pred[(a, 'dark')]}", tuple(pred[(a, 'dark')]) == consts["A9_PRED"][key])
    m = sample(comp, float(a), 0)
    ex = sample(nat, float(a), 0)
    check(f"B61 measured dark @ {key}: {consts['A9_MEAS'][key]} == re-run Compat {m} == the example's own {ex}", tuple(m) == consts["A9_MEAS"][key] == tuple(ex))
# B62: gaps (measured minus predicted, Compatibility): dark @0 and (any stripe) @1
g0 = tuple(m - p for m, p in zip(sample(comp, 0.0, 0), pred[(0, "dark")]))
g1 = tuple(m - p for m, p in zip(sample(comp, 1.0, 0), pred[(1, "dark")]))
check(f"B62 gap row 'activation 0, dark stripe' {consts['A9_GAP'][0][2]} == {g0}", tuple(consts["A9_GAP"][0][2]) == g0)
check(f"B62 gap row 'activation 1' {consts['A9_GAP'][1][2]} == {g1} (light stripe gives the same: {tuple(m - p for m, p in zip(sample(comp, 1.0, 1), pred[(1, 'light')]))})", tuple(consts["A9_GAP"][1][2]) == g1)
rows = {r["value"]: r for r in json.load(open(HERE / "evidence/runs/R9-constant-albedo-compatibility.json"))["rows"] if r["row"] == "const"}
for v, w, r in consts["A9_PROBE"]:
    check(f"B62 probe {v}: written {w} (= round({v} x 255)) read {r} == R9 json {rows[v]['rgb8']}", round(v * 255) == w and rows[v]["rgb8"] == [r, r, r])
# B63: light stripe at 0.5, Compat and Forward+ (uv_x 0.21875, sample index 1)
check("B63 Compat light @0.5 66,112,78", sample(comp, 0.5, 1) == [66, 112, 78] and tuple(pred[(0.5, "light")]) == (66, 112, 78))
check("B63 Forward+ light @0.5 76,137,97", sample(fpl, 0.5, 1) == [76, 137, 97])
# B64: activation 1 and 2
check("B64 Compat dark @1 28,184,133", sample(comp, 1.0, 0) == [28, 184, 133])
check("B64 Compat dark @2 0,255,251", sample(comp, 2.0, 0) == [0, 255, 251])
check("B64 Forward+ dark @2 0,248,181", sample(fpl, 2.0, 0) == [0, 248, 181])
red = 0.26 + (0.12 - 0.26) * 2
green = 0.104 + (0.72 - 0.104) * 2
check(f"B64 arithmetic mix(base, active, 2.0): red {red:.3f} (shown -0.02), green {green:.3f} (shown 1.34)", abs(red + 0.02) < 1e-9 and abs(green - 1.336) < 1e-9)
for s_ in ("28,184,133", "0,255,251", "0,248,181", "66,112,78", "76,137,97", "red \\u22120.02, shown 0", "green 1.34, shown 255"):
    check(f"scenes_act9.py contains the string {s_!r}", s_ in src)
# the a9 sample pixels
check("sample pixels: UV.x 0.15625 -> source x 253, 0.21875 -> 354 (1620 px = 3 units, quad centred)", round(0.15625 * 1620) == 253 and round(0.21875 * 1620) == 354)
# B60: the code lines shown are verbatim (assignment-05.md lines 457-460; render-material-evidence.gd line 11, tab shown as 4 spaces)
asg = (HERE / "evidence/example/sources/assignment-05.md").read_text().splitlines()
for n in (457, 458, 459, 460):
    check(f"B60 code line {n} verbatim in scenes_act9.py: {asg[n-1]!r}", ('"' + asg[n - 1] + '"') in src)
rme = (HERE / "evidence/example/sources/render-material-evidence.gd").read_text().splitlines()
check(f"B60 example line 11 verbatim ({rme[10]!r} with the tab as 4 spaces)", ('"\\t' + rme[10].lstrip("\t") + '"') in src and rme[10].startswith("\t"))
# B66: the values on the row labels equal the script's own values (render-material-evidence.gd lines 61-64)
check("B66 values: roughness_gain [0.0,0.8,1.0] / uv_scale [0.25,1.0,4.0] / metallic [0.0,0.0,1.0] / tint [BLACK, WHITE, Color(1,0.2,0.2)] in the script", all(t in "\n".join(rme) for t in ("[Color.BLACK,Color.WHITE,Color(1,0.2,0.2)]", "[0.0,0.8,1.0]", "[0.25,1.0,4.0]", "[0.0,0.0,1.0]")))
check("B67 shared edit multiplies tint by (1.0, 0.25, 0.25) in a duplicate of the shader; one-value edit sets the left tint Color(0.2,0.2,1.0)", "shared.code.replace(\"* tint.rgb;\", \"* tint.rgb * vec3(1.0, 0.25, 0.25);\")" in "\n".join(rme) and "set_shader_parameter(\"tint\",Color(0.2,0.2,1.0))" in "\n".join(rme) and ".shader.duplicate()" in "\n".join(rme))
# B65: HUD words and percentages come from the frames' own panels/states: the charge at each frame
st = {}
for line in open(HERE / "captures/lab/states.jsonl"):
    d = json.loads(line)
    st[d["frame"]] = d
check("B65 frame 597: charge/0.6 = %.3f (HUD 'CHARGING / 27%%', panel 0.278)" % (st[597]["charge"] / 0.6), int(st[597]["charge"] / 0.6 * 100) == 27)
check("B65 frame 609: charge/0.6 = %.3f (HUD 'CHARGING / 94%%', panel 0.944)" % (st[609]["charge"] / 0.6), int(st[609]["charge"] / 0.6 * 100) == 94)
check("B65 frame 610: gate_open True (HUD 'GATE OPEN')", st[610]["gate_open"] is True)
keys = [json.loads(l) for l in open(HERE / "captures/lab/inputs.jsonl")]
check("B65 the E key goes down at frame 593 (scripted, inputs.jsonl)", {"down": True, "frame": 593, "key": "E"} in keys)
print("ALL MATCH" if not bad else f"{bad} MISMATCH(ES)")
sys.exit(1 if bad else 0)
