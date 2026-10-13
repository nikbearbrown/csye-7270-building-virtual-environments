"""analyze_lab.py: compares the Lab renders with the formulas, pixel by pixel. Writes lab-analysis.txt next to this file.

For every shader that draws a teal disc or spot over the Lab stage (#D9D5CA) the alpha of each pixel is recovered from its colour
(least squares between stage colour and teal) and compared with the formula. For the two bubble shaders the colour itself is compared.
Run:  python3 -I analyze_lab.py     (Pillow only)
"""
import json
import math
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
RES = {}
for line in open(HERE / "lab-results.jsonl"):
    d = json.loads(line)
    out = d["output"]
    RES[d["check"]] = json.loads(out.split("RESULT ", 1)[1]) if "RESULT " in out else None

BG = (217, 213, 202)          # Lab stage #D9D5CA
TEAL = (94, 163, 145)         # Color(0.37, 0.64, 0.57) as 8-bit
OUT = []


def say(s=""):
    print(s)
    OUT.append(s)


def smooth(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3.0 - 2.0 * t)


def alpha_of(c):
    num = sum((BG[i] - c[i]) * (BG[i] - TEAL[i]) for i in range(3))
    den = sum((BG[i] - TEAL[i]) ** 2 for i in range(3))
    return num / den


def uv(px, py, n=256):
    return (px + 0.5) / n, (py + 0.5) / n


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def clamp01(x):
    return max(0.0, min(1.0, x))


FORMULAS = {
    "01-hard-disc": lambda u, v, o: 1.0 if dist((u, v), (0.5, 0.5)) < 0.4 else 0.0,
    "02-soft-disc": lambda u, v, o: 1.0 - smooth(0.25, 0.4, dist((u, v), (0.5, 0.5))),
    "04-spot": lambda u, v, o: clamp01(1.0 - dist((u, v), (0.35, 0.35))),
    "06-spot-in-disc": lambda u, v, o: clamp01(1.0 - dist((u, v), (0.35, 0.35))) ** 3 * (1.0 - smooth(0.25, 0.4, dist((u, v), (0.5, 0.5)))),
}
for s in ("0.15", "0.05", "0.4", "0.0"):
    FORMULAS[f"03-soft-width-{s}"] = (lambda sv: (lambda u, v, o: 1.0 - smooth(0.4 - max(sv, 0.01), 0.4, dist((u, v), (0.5, 0.5)))))(float(s))
for lab, c in (("07-spot-moves-a", (0.35, 0.35)), ("07-spot-moves-b", (0.65, 0.4))):
    FORMULAS[lab] = (lambda cc: (lambda u, v, o: clamp01(1.0 - dist((u, v), cc)) ** 3 * (1.0 - smooth(0.25, 0.4, dist((u, v), (0.5, 0.5))))))(c)
for p in (1, 3, 8):
    FORMULAS[f"05-spot-power-{p}"] = (lambda pv: (lambda u, v, o: clamp01(1.0 - dist((u, v), (0.35, 0.35))) ** pv))(p)


def whole_image(label, fn):
    im = Image.open(HERE / "png" / f"{label}.png").convert("RGB")
    W, H = im.size
    worst = 0.0
    total = 0.0
    inter = 0
    colors = set()
    for py in range(H):
        for px in range(W):
            c = im.getpixel((px, py))
            colors.add(c)
            u, v = uv(px, py, W)
            e = abs(alpha_of(c) - fn(u, v, None))
            worst = max(worst, e)
            total += e
            a = alpha_of(c)
            if 0.02 < a < 0.98:
                inter += 1
    return worst, total / (W * H), inter, len(colors)


def probe_table(label, fn):
    r = RES.get(label)
    if not r:
        return
    for p in r["probes"]:
        px, py = p["px"]
        u, v = uv(px, py)
        c = [round(x * 255) for x in p["rgba"][:3]]
        meas = alpha_of(c)
        exp = fn(u, v, None)
        say(f"    px ({px:3d},{py:3d})  UV ({u:.4f}, {v:.4f})  measured alpha {meas:6.3f}   formula {exp:6.3f}   diff {meas - exp:+.3f}")


say("# Lab analysis: expected (formula) against measured (real Godot 4.7.2 window, Forward+, Apple M4 Pro)\n")
say("Alpha is recovered from the pixel colour (least squares between the Lab stage #D9D5CA and the teal). The 8-bit frame limits the precision to about 0.01.\n")
for label, fn in FORMULAS.items():
    if not (HERE / "png" / f"{label}.png").exists():
        continue
    worst, mean, inter, ncol = whole_image(label, fn)
    say(f"## {label}: every one of the 65,536 pixels against the formula")
    say(f"    worst difference {worst:.3f}   mean difference {mean:.4f}   pixels with an in-between alpha (0.02 to 0.98): {inter}   distinct colours in the picture: {ncol}")
    probe_table(label, fn)
    say()

# the three numbers of the film's S-curve, from the soft disc: distances of the probe pixels along the middle row
say("## The smoothstep numbers (02-soft-disc, probes along the middle row)")
r = RES["02-soft-disc"]
for p in r["probes"]:
    px, py = p["px"]
    u, v = uv(px, py)
    d = dist((u, v), (0.5, 0.5))
    if 0.25 < d < 0.4:
        t = (d - 0.25) / 0.15
        c = [round(x * 255) for x in p["rgba"][:3]]
        say(f"    px {px}: distance {d:.4f}, t = {t:.3f}; smoothstep = {smooth(0.25, 0.4, d):.3f} (a straight ramp would say {t:.3f}); body measured {alpha_of(c):.3f}, formula {1 - smooth(0.25, 0.4, d):.3f}, a straight ramp would give {1 - t:.3f}")
say()
say("## The same numbers at the five pixels whose t is 0.100, 0.250, 0.500, 0.750, 0.900 (02-soft-disc-t)")
for p in RES["02-soft-disc-t"]["probes"]:
    px, py = p["px"]
    u, v = uv(px, py)
    d = dist((u, v), (0.5, 0.5))
    t = (d - 0.25) / 0.15
    c = [round(x * 255) for x in p["rgba"][:3]]
    say(f"    px ({px},{py}): t = {t:.4f}; smoothstep {smooth(0.25, 0.4, d):.4f}, a straight ramp {t:.4f}; body measured {alpha_of(c):.3f}, formula {1 - smooth(0.25, 0.4, d):.3f}, a straight ramp would give {1 - t:.3f}")
say()
say("## Hand-checkable values of t * t * (3 - 2t)")
for t in (0.1, 0.25, 0.5, 0.75, 0.9):
    say(f"    t = {t}: {t * t * (3 - 2 * t):.4f}   (a straight ramp: {t})")
say()

# the bubbles: colour compared with the formula
MAIN = (0.37, 0.64, 0.57)
SPOT = (0.55, 0.52, 0.45)


def bubble_rgb(u, v, brightness, bug, glow=None):
    disc = 1.0 - smooth(0.25, 0.4, dist((u, v), (0.5, 0.5)))
    spot = clamp01(1.0 - dist((u, v), (0.35, 0.35))) ** 3
    if glow is not None:
        rgb = [(MAIN[i] + SPOT[i] * spot) * (1.0 + glow * 5.0) for i in range(3)]
    elif bug:
        rgb = [MAIN[i] + SPOT[i] * spot * brightness for i in range(3)]
    else:
        rgb = [(MAIN[i] + SPOT[i] * spot) * brightness for i in range(3)]
    # blend over the stage; the 8-bit target clamps each channel
    out = [clamp01(rgb[i]) * disc + (BG[i] / 255.0) * (1.0 - disc) for i in range(3)]
    return rgb, out, disc, spot


for label, bright, bug, glow in (("08-bubble-1.0", 1.0, False, None), ("08-bubble-0.6", 0.6, False, None), ("09-bubble-bug-1.0", 1.0, True, None), ("09-bubble-bug-0.6", 0.6, True, None),
                                  ("14-glow-bubble-0", None, False, 0.0), ("14-glow-bubble-0.1", None, False, 0.1), ("14-glow-bubble-1", None, False, 1.0)):
    r = RES.get(label)
    if not r:
        continue
    say(f"## {label}  (uniforms reported by Godot: {', '.join(r['uniforms'])})")
    for p in r["probes"]:
        px, py = p["px"]
        u, v = uv(px, py)
        rgb, out, disc, spot = bubble_rgb(u, v, bright, bug, glow)
        meas = p["rgba"][:3]
        say(f"    px ({px:3d},{py:3d}) disc {disc:.3f} spot {spot:.3f}  shader rgb before the screen clips it ({rgb[0]:.3f}, {rgb[1]:.3f}, {rgb[2]:.3f})  "
            f"expected on screen ({out[0]:.3f}, {out[1]:.3f}, {out[2]:.3f})  measured ({meas[0]:.3f}, {meas[1]:.3f}, {meas[2]:.3f})")
    say()

# the unique-colour test for the equal-edge and reversed-edge cases
say("## Equal edges and reversed edges (evidence only)")
for label in ("ev-equal-edges-fplus", "ev-equal-edges-compat", "ev-reversed-fplus", "ev-reversed-compat"):
    im = Image.open(HERE / "png" / f"{label}.png").convert("RGB")
    cols = len(set(im.getdata()))
    r = RES[label]
    vals = [round(alpha_of([round(x * 255) for x in p["rgba"][:3]]), 3) for p in r["probes"]]
    say(f"    {label}: renderer {r['renderer']}, distinct colours {cols}, alpha at the probes {vals}")
say()
say("## pow() of a negative base on this machine (evidence only; red = NaN, green = negative, blue = positive)")
for label in ("ev-pow-negative-fplus", "ev-pow-negative-compat", "ev-pow-fraction-fplus", "ev-pow-fraction-compat"):
    r = RES[label]
    say(f"    {label}: renderer {r['renderer']}, probes (x = -0.8, ~0, +0.8 as available) {[p['rgba'][:3] for p in r['probes']]}")
for label in ("ev-pow-unclamped", "ev-pow-clamped"):
    r = RES[label]
    say(f"    {label}: far-corner probes {[p['rgba'][:3] for p in r['probes']]}  (stage colour is 0.851, 0.8353, 0.7922: the NaN corner draws as nothing)")

say()
say("## The vertex pulse, VERTEX += normalize(VERTEX) * 30.0 (left out of the film; a note for a vertex-stage film)")
for label in ("ev-vertex-pulse-sprite", "ev-vertex-pulse-rect"):
    im = Image.open(HERE / "png" / f"{label}.png").convert("RGB")
    W, H = im.size
    pts = [(x, y) for y in range(H) for x in range(W) if im.getpixel((x, y)) != BG]
    if pts:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        say(f"    {label}: covered pixels {len(pts)}, bounding box x {min(xs)} to {max(xs)} ({max(xs) - min(xs) + 1} px wide), y {min(ys)} to {max(ys)}  (a 128 px square moved outward by 30 px at each corner: 128 + 2 * 21.2 = 170 px)")
    else:
        say(f"    {label}: covered pixels 0: the whole rectangle disappeared (its corner vertex is at (0, 0), so normalize(VERTEX) is a zero-length vector)")
(HERE / "lab-analysis.txt").write_text("\n".join(OUT) + "\n")
