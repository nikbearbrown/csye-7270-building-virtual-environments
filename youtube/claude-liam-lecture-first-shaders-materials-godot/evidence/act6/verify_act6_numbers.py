#!/usr/bin/env python3
"""verify_act6_numbers.py: re-derives every number Act VI puts on screen from the frozen evidence. Run from anywhere:
    python3 evidence/act6/verify_act6_numbers.py        (writes evidence/act6/verify_act6_numbers.log)
It reads only files inside this reel folder (nothing under walker-claude, no Godot run)."""
import json, re, sys
from pathlib import Path
REEL = Path(__file__).resolve().parent.parent.parent
out = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

# 1. the assignment's sRGB encode (assignment-05.md, "The hint experiment"): encode(x) = 12.92x for x <= 0.0031308, else 1.055 x^(1/2.4) - 0.055
def encode(x): return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
say("== hint experiment, predicted by the assignment's formula (Forward+ data read) ==")
pred = {}
for b in (64, 128, 192):
    x = b / 255
    pred[b] = round(encode(x) * 255)
    say(f"  band {b}: x = {x:.5f}  encode(x) = {encode(x):.5f}  x255 = {encode(x)*255:.4f}  -> {pred[b]}")
assert [pred[64], pred[128], pred[192]] == [137, 188, 225]

say("== hint experiment, measured RGB8 (re-run for this film, 16 Oct; 3840x2160; Linear tonemap, exposure 1.0) ==")
for tag in ("forward_plus", "compatibility"):
    d = json.loads((REEL / f"captures/forward-plus/hint_{tag}.json").read_text())
    rows = {"source_color": [], "no_hint (data)": []}
    for s in d["samples"]:
        assert s["rgb8"][0] == s["rgb8"][1] == s["rgb8"][2]
        rows[s["quad"]].append(s["rgb8"][0])
    say(f"  {d['rendering_method']:>14} ({d['rendering_driver']}, {d['adapter']}):  source_color {rows['source_color']}   data {rows['no_hint (data)']}")
    if tag == "forward_plus":
        assert rows["source_color"] == [64, 128, 192] and rows["no_hint (data)"] == [pred[64], pred[128], pred[192]]
    else:
        assert rows["source_color"] == [64, 128, 192] and rows["no_hint (data)"] == [64, 128, 192]

say("== the example's own fixture, 14 Oct (Compatibility), hint-samples.json: float x 255 ==")
d = json.loads((REEL / "evidence/example/hint-samples.json").read_text())
say("  renderer string:", d["rendering_method"], "| engine", d["engine"]["string"])
ex = {"source_color": [], "data": []}
for s in d["samples"]:
    v = [round(c * 255) for c in s["rgb"]]
    assert v[0] == v[1] == v[2] == s["input_byte"]
    ex[s["hint"]].append(v[0])
say("  source_color", ex["source_color"], "  data", ex["data"])
assert ex["source_color"] == ex["data"] == [64, 128, 192]
img = json.loads((REEL / "captures/forward-plus/hint_forward_plus.json").read_text())
say("  re-run image formats: Forward+ =", img["image_format"], "(RGB8), Compatibility =",
    json.loads((REEL / "captures/forward-plus/hint_compatibility.json").read_text())["image_format"], "(RGBA8)")

say("== curl ratios (stride 2, 1k Poly Haven stone_floor pair; the example's helper) ==")
r3 = json.loads((REEL / "evidence/runs/R3-normal-calibration.json").read_text())
for r in r3:
    say(f"  {r['variant'].upper()} file ({r['width']}x{r['height']}): read as GL {r['normal_gl_interpretation']:.5f}   read as DX {r['normal_dx_interpretation']:.5f}")
by = {r["variant"]: r for r in r3}
assert round(by["gl"]["normal_gl_interpretation"], 5) == 0.48445 and round(by["gl"]["normal_dx_interpretation"], 5) == 1.51555
assert round(by["dx"]["normal_gl_interpretation"], 5) == 1.51555 and round(by["dx"]["normal_dx_interpretation"], 5) == 0.48445
say("  distance of the right-convention read from the ideal 0:", round(by['gl']['normal_gl_interpretation'], 5), "; of the wrong-convention read from the ideal 2:", round(2 - by['gl']['normal_dx_interpretation'] + 0, 5) if False else round(abs(2 - by['gl']['normal_dx_interpretation']), 5))
log = (REEL / "evidence/runs/R1-baseline-60fps.log").read_text()
m = re.search(r'ANALYTIC_NORMAL (\{.*\})', log); an = json.loads(m.group(1))
say(f"  code-made map (analytic-normal-gl.png, 256x256), from the baseline log: GL {an['GL']:.5f}   DX {an['DX']:.5f}")
assert round(an["GL"], 5) == 0.05447 and round(an["DX"], 5) == 1.94553

say("== the 53 checks ==")
src = (REEL / "evidence/example/sources/test-material-contract.gd").read_text()
sig = len(re.findall(r'^\tcheck\("', src.split("var paths")[0], flags=re.M))
say("  checks on the pad shader (lines 17-21 of test-material-contract.gd):", sig)
per = 1 + 1 + 1 + 1 + 4 + 4 + 2 * (1 + 1 + 4)      # shared shader, colour hint, data hint, two groups, 4 declared, 4 values, per sampler: path + import readable + 4 import keys
say("  checks per material:", per)
assert sig == 5 and per == 24 and sig + 2 * per == 53
res = [l for l in log.splitlines() if l.startswith("RESULT")]
npass = sum(1 for l in log.splitlines() if l.startswith("PASS")); nfail = sum(1 for l in log.splitlines() if l.startswith("FAIL"))
say(f"  baseline log: {npass} PASS lines, {nfail} FAIL lines; {res[0]}")
assert npass == 53 and nfail == 0
m3 = (REEL / "evidence/runs/R4-M3-hint-60fps.log").read_text()
fails = [l for l in m3.splitlines() if l.startswith("FAIL")]
say("  mutation log FAIL lines:", fails, "|", [l for l in m3.splitlines() if l.startswith("RESULT")][0])
assert fails == ["FAIL matte color hint", "FAIL coated color hint"]
say("ALL ASSERTIONS HOLD")
(REEL / "evidence/act6/verify_act6_numbers.log").write_text("\n".join(out) + "\n")
