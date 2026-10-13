#!/usr/bin/env python3
"""linear-mix-check.py: arithmetic behind the film's two renderer explanations, compared with the measured Lab pixels.
Hypotheses (read from the docs and tested here, nothing assumed):
  H1  Forward+ treats ALBEDO as LINEAR light and encodes it with the standard sRGB curve on its way to the screen, and it converts a
      source_color uniform from sRGB to linear first; so a mix of two source_color values happens in linear light.
  H2  The Compatibility renderer draws the numbers as written (OUTPUT_IS_SRGB is true): a mix is the plain average of the typed numbers.
Measured values are read from lab-results.jsonl (run-lab-checks.sh)."""
import json
from pathlib import Path

here = Path(__file__).resolve().parent


def to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_srgb(l):
    return l * 12.92 if l <= 0.0031308 else 1.055 * l ** (1 / 2.4) - 0.055


def measured(label):
    for raw in (here / "lab-results.jsonl").read_text().splitlines():
        rec = json.loads(raw)
        if rec["check"] == label:
            for line in rec["output"].splitlines():
                if line.startswith("RESULT "):
                    return [p["rgba"][:3] for p in json.loads(line[7:])["probes"]]
    raise KeyError(label)


def steps(a, b):
    return [round(abs(x - y) * 255, 1) for x, y in zip(a, b)]


print("== grey 0.5, unshaded ALBEDO, in 3D")
fp = measured("14-grey-3d-forward_plus")[0][0]
gc = measured("14-grey-3d-gl_compatibility")[0][0]
d2 = measured("13-grey-2d-forward_plus")[0][0]
print(f"   H1 predicts Forward+ = sRGB-encode(0.5 linear) = {to_srgb(0.5):.4f} ({to_srgb(0.5) * 255:.1f}/255); measured {fp} ({fp * 255:.0f}/255)")
print(f"   H2 predicts Compatibility = 0.5 ({0.5 * 255:.1f}/255); measured {gc} ({gc * 255:.0f}/255)")
print(f"   2D COLOR 0.5 (Forward+, canvas_item) measured {d2}: a 2D COLOR is drawn as written")

quiet = [0.40, 0.16, 0.09]
active = [0.12, 0.72, 0.52]
print("== the pad's colours mixed at activation 0.5 (flat 11-mix-dial; also the pad's light stripe)")
typed_mid = [(a + b) / 2 for a, b in zip(quiet, active)]
lin_mid = [to_srgb((to_linear(a) + to_linear(b)) / 2) for a, b in zip(quiet, active)]
m_fp = measured("11-mix-dial-fp-0.5")[0]
m_gc = measured("11-mix-dial-gc-0.5")[0]
print("   typed numbers averaged        :", [round(x, 4) for x in typed_mid])
print("   linear-light mix, back to sRGB:", [round(x, 4) for x in lin_mid])
print("   measured Forward+             :", m_fp, "  distance from the linear-light mix, in 8-bit steps:", steps(m_fp, lin_mid))
print("   measured Compatibility        :", m_gc, "  distance from the typed average,    in 8-bit steps:", steps(m_gc, typed_mid))
print("   (and the cross-checks: Forward+ vs typed average:", steps(m_fp, typed_mid), "; Compatibility vs linear-light mix:", steps(m_gc, lin_mid), ")")
print("== one channel (red) as drawn in the film: rust 0.40 and green 0.12")
a, b = quiet[0], active[0]
print(f"   typed average (0.40 + 0.12) / 2 = {(a + b) / 2:.4f}")
print(f"   linear light: 0.40 -> {to_linear(a):.4f}, 0.12 -> {to_linear(b):.4f}, mean {(to_linear(a) + to_linear(b)) / 2:.4f}, back to the screen {to_srgb((to_linear(a) + to_linear(b)) / 2):.4f}")
print("== endpoints (activation 0 and 1) in Compatibility are NOT exactly the typed numbers: low channels read a few steps low")
for label, typed in (("11-mix-dial-gc-0.0", quiet), ("11-mix-dial-gc-1.0", active)):
    m = measured(label)[0]
    print(f"   {label}: typed {typed} measured {m} -> steps {steps(m, typed)}")
for label, typed in (("11-mix-dial-fp-0.0", quiet), ("11-mix-dial-fp-1.0", active)):
    m = measured(label)[0]
    print(f"   {label}: typed {typed} measured {m} -> steps {steps(m, typed)}")
