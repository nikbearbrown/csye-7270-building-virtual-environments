#!/usr/bin/env python3
"""measure_a5_text.py - measures every Act V string with the real fonts (Menlo, EB Garamond) and prints the A5_BL table that
scenes_act5.py pastes in: (font, size, text) -> (centre_y - baseline, width, top - baseline, bottom - baseline).
The baseline is the median bottom of the glyphs that sit on it (no descenders, no floating marks). It also flags lines whose
width is short of the Menlo advance (the Pango space-collapse bug: a dropped space shows up as a missing 0.25 of width).
  python3 evidence/act5/measure_a5_text.py            (from the reel folder)"""
import sys, statistics
from pathlib import Path
HERE = Path(__file__).resolve().parents[2]
src = (HERE / "kit.py").read_text() + "\n" + (HERE / "scenes_act5.py").read_text()
pass
ns = {"__file__": str(HERE / "scenes.py")}
exec(compile(src, "act5", "exec"), ns)
T, M = ns["T"], ns["M"]
DESC = set("gjpqy,;_()[]{}|/$@Q")
FLOAT = set("'\"*-→·^~`+=<>:?")
out = {}
for f, size, s in ns["A5_ALL"]:
    t = M(s, size) if f == "M" else T(s, size)
    chars = [c for c in s if not c.isspace()]
    glyphs = [g for g in t.submobjects]
    bots = []
    if len(chars) == len(glyphs):
        bots = [g.get_bottom()[1] for c, g in zip(chars, glyphs) if c not in DESC and c not in FLOAT and len(g.points)]
    if not bots:
        bots = [g.get_bottom()[1] for g in glyphs if len(g.points)]
    base = statistics.median(bots)
    cy = t.get_center()[1]
    out[(f, size, s)] = tuple(round(float(v), 4) for v in (cy - base, t.width, t.get_top()[1] - base, t.get_bottom()[1] - base))
    if f == "M":
        exp = (len(s) - 1) * 0.2496
        if t.width < exp - 0.15:
            print(f"# WARN possible dropped space: {s!r} width {t.width:.2f} < {exp:.2f}", file=sys.stderr)
    if len(chars) != len(glyphs):
        print(f"# note: glyph count {len(glyphs)} != chars {len(chars)} for {s!r}", file=sys.stderr)
arrows, pieces = {}, {}
for f, size, s in ns["A5_ALL"]:
    if f == "M" and "→" in s:
        t = M(s, size)
        chars = [c for c in s if not c.isspace()]
        left = t.get_left()[0]
        arrows[s] = [round(float(g.get_center()[0] - left), 4) for c, g in zip(chars, t.submobjects) if c == "→"]
        # the words between the arrows, each with its left ink edge measured from the row's left ink edge
        out_p, k = [], 0
        for part in s.split("→"):
            word = part.strip()
            n = len([c for c in part if not c.isspace()])
            if word:
                out_p.append((word, round(float(t.submobjects[k].get_left()[0] - left), 4)))
            k += n + 1
        pieces[s] = out_p
print("A5_ARROWS = " + repr(arrows))
print("A5_PIECES = " + repr(pieces))
print("A5_BL = {")
for k, v in out.items():
    print(f"    {k!r}: {v!r},")
print("}")

if "--write" in sys.argv:          # paste the three tables into scenes_act5.py
    import io, contextlib, re
    p = HERE / "scenes_act5.py"
    s = p.read_text()
    bl = "A5_BL = {\n" + "".join(f"    {k!r}: {v!r},\n" for k, v in out.items()) + "}"
    s = re.sub(r"A5_BL = \{.*?\n\}|A5_BL = \{\}", lambda _: bl, s, count=1, flags=re.S)
    s = re.sub(r"A5_ARROWS = \{.*?\}\n", lambda _: "A5_ARROWS = " + repr(arrows) + "\n", s, count=1, flags=re.S)
    s = re.sub(r"A5_PIECES = \{.*?\}\n", lambda _: "A5_PIECES = " + repr(pieces) + "\n", s, count=1, flags=re.S)
    p.write_text(s)
    print("# wrote A5_BL, A5_ARROWS, A5_PIECES into", p, file=sys.stderr)
