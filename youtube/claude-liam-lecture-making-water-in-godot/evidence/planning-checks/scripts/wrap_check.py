#!/usr/bin/env python3
"""wrap_check.py: replays ShaderLab's code-line wrapping (ShaderLab.tsx buildRows) on every ShaderLab beat of the film and lists the places where it would cut a
number in two (a break right after a '.' that sits between digits). Cosmetic only; the code text is never changed here."""
import json, math, re, glob
from pathlib import Path
R = Path(__file__).resolve().parents[3]
NUM_W, PAD_X = 68, 22
def rows(code, layout, fs=32):
    cardW0 = 1280 if layout == 'code' else 1100 if layout == 'stack' else 736
    per = max(20, math.floor((cardW0 - NUM_W - PAD_X - 24) / (0.602 * fs)))
    out = []
    for i, ln in enumerate(code.split('\n')[:14]):
        t = ln.replace('\t', '    ')
        if len(t) <= per:
            out.append(t); continue
        rest, first = t, True
        while rest:
            room = per if first else per - 6
            cut = len(rest)
            if len(rest) > room:
                cut = room
                for j in range(room, int(room * 0.5), -1):
                    if rest[j - 1] in ' ,.(/': cut = j; break
            out.append(rest[:cut]); rest = rest[cut:].lstrip(' '); first = False
    return out
bad = 0
for f in sorted(glob.glob(str(R / 'lanes/*.json'))):
    for bid, v in json.load(open(f)).items():
        p = v.get('props', {})
        if v.get('pattern') != 'ShaderLab' or not p.get('code'): continue
        rs = rows(p['code'], p['layout'])
        for a, b in zip(rs, rs[1:]):
            if re.search(r'\d\.$', a) and re.match(r'^\s*\d', b):
                bad += 1; print(f"{bid}: a number is cut across rows: ...{a[-14:]!r} / {b.strip()[:14]!r}")
print(f"{bad} cut numbers")
