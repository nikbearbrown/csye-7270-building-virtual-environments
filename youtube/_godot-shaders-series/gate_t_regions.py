#!/usr/bin/env python3
"""Add qc.typography_regions (toolkit-sanctioned, opt-in) to every ShaderLab beat of a shader film.

Why: GATE T's pixel checks read the Godot capture's mid-tone dusk-blue floor and its glow as 'text blobs'
(false positives). The toolkit's own remedy is a reviewed inventory of the AUTHORED text regions
(type_check.typography_frame); the picture inside the window is image content. Boxes mirror ShaderLab.tsx
geometry (1920x1080 design px). Run: python3 gate_t_regions.py <reel> [--draw OUTDIR]. Idempotent. Written 2026-10-14.
"""
import json, sys, math
from pathlib import Path

NUM_W, PAD_X, LINE_H = 68, 22, 48

def rows_for(code, layout, fs0=None):
    lines = code.split('\n')[:14] if code else []
    cardW0 = 1280 if layout == 'code' else 1100 if layout == 'stack' else 736
    fs0 = fs0 or (36 if layout == 'code' else 32)
    per = max(20, math.floor((cardW0 - NUM_W - PAD_X - 24) / (0.602 * fs0)))
    n = 0
    for ln in lines:
        t = ln.replace('\t', '    ')
        if len(t) <= per: n += 1; continue
        rest, first = t, True
        while rest:
            room = per if first else per - 6
            cut = len(rest)
            if len(rest) > room:
                cut = room
                for j in range(room, int(room * 0.5), -1):
                    if rest[j - 1] in ' ,.(/': cut = j; break
            n += 1; rest = rest[cut:].lstrip(' '); first = False
    return n

def regions(p):
    layout = p.get('layout', 'side'); aspect = p.get('videoAspect', 16 / 9)
    code = p.get('code', '')
    if not code and p.get('codeFile'):
        code = ''
    nlines = rows_for(code, layout)
    LH = LINE_H
    if layout != 'code' and nlines > 18:
        nlines = rows_for(code, layout, 27); LH = 42
    hasCode = nlines > 0 and layout in ('side', 'stack', 'code')
    hasVideo = bool(p.get('video')) and layout != 'code'
    top = 150 if p.get('title') else 70; zoneH = 1020 - top
    codeH = min(nlines, 21 if LH == 42 else 18) * LH + 36
    winW, winLeft, winTop = 928, 884, top
    ramp = bool(p.get('ramp')); cap = bool(p.get('caption'))
    box = {'left': 112, 'top': top, 'width': 736, 'height': codeH}
    if layout == 'side':
        winW = min(928, 640 * aspect); winLeft = 884 + (928 - winW) / 2
        winH0 = winW / aspect; colH = 34 + winH0 + (70 if ramp else 0) + (44 if cap else 0)
        winTop = top + max(34, (zoneH - colH) / 2 + 34)
        box = {'left': 112, 'top': top + max(0, (zoneH - codeH) / 2 - 20), 'width': 736, 'height': codeH}
    elif layout == 'stack':
        exH = min(nlines, 4) * LH + 36
        winH = min(660, zoneH - exH - (70 if ramp else 0) - (44 if cap else 0) - 34 - 40)
        winW = min(1500, winH * aspect); winLeft = (1920 - winW) / 2; winTop = top + 34
        box = {'left': max(80, (1920 - 1100) / 2), 'top': winTop + winH + (70 if ramp else 0) + (44 if cap else 0) + 24, 'width': 1100, 'height': exH}
    elif layout == 'video':
        maxH = zoneH - 34 - (70 if ramp else 0) - (50 if cap else 0) - 10
        winW = min(1560, maxH * aspect); winLeft = (1920 - winW) / 2; winTop = top + 34
    elif layout == 'code':
        rows_n = min(nlines, 14)
        box = {'left': max(80, (1920 - 1280) / 2), 'top': top + max(0, (zoneH - (rows_n * 52 + 36)) / 2), 'width': 1280, 'height': rows_n * 52 + 36}
    winH = winW / aspect
    R = []
    if p.get('title'):
        R.append(('title', 100, 40, min(1900, 112 + len(p['title']) * 31 + 30), 135))
    if hasCode:
        R.append(('code card', box['left'] - 6, box['top'] - 6, box['left'] + box['width'] + 6, box['top'] + box['height'] + 6))
        if p.get('codeFile'):
            R.append(('code file', box['left'], box['top'] + box['height'] + 6, box['left'] + box['width'], box['top'] + box['height'] + 46))
        if any(c.get('label') for c in p.get('cues', [])):
            R.append(('cue tag', box['left'], box['top'] + box['height'] + 44, box['left'] + box['width'], box['top'] + box['height'] + 100))
    if hasVideo:
        if p.get('videoLabel'):
            x0 = min(winLeft, 884); R.append(('video label', x0 - 6, winTop - 10 - 80, x0 + (max(winW, 928) if layout == 'side' else max(winW, min(1500, 1824 - winLeft))) + 6, winTop - 6))
        if cap:
            ct = winTop + winH + (78 if ramp else 18)
            lines_n = max(1, math.ceil(len(p['caption']) * 15.5 / max(winW, 1)))
            R.append(('caption', winLeft - 6, ct - 4, winLeft + winW + 6, ct + 8 + 42 * lines_n))
        if ramp:
            y = winTop + winH + 22
            R.append(('ramp labels', winLeft - 6, y + 20, winLeft + winW + 20, y + 70))
        seen = {}
        for r in p.get('readouts', []): seen[(r['x'], r['y'])] = r
        for r in p.get('readouts', []):
            halfW = (len(r['text']) * 17 + 56) / 2 + 6
            cx = min(winW - halfW, max(halfW, r['x'] * winW))
            X = winLeft + cx; Y = winTop + r['y'] * winH
            hw = (len(r['text']) * 14.6 + 56) / 2 + 4
            R.append((f"readout {r['text']}", X - hw, Y - 22, X + hw, Y + 22))
    out = []
    for lab, x0, y0, x1, y1 in R:
        x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(1920, x1), min(1080, y1)
        out.append({'label': lab, 'box': [round(x0 / 1920, 4), round(y0 / 1080, 4), round(x1 / 1920, 4), round(y1 / 1080, 4)]})
    return out

def main():
    reel = Path(sys.argv[1]); draw = sys.argv[sys.argv.index('--draw') + 1] if '--draw' in sys.argv else None
    bsp = reel / 'beat_sheet.json'; bs = json.loads(bsp.read_text()); n = 0
    for b in bs['beats']:
        r = (b.get('shot') or {}).get('remotion') or {}
        if r.get('pattern') != 'ShaderLab': continue
        props = dict(r['props'])
        if not props.get('code') and props.get('codeFile'):
            f = reel / props['codeFile']
            if f.exists(): props['code'] = f.read_text().rstrip('\n')
        regs = regions(props)
        if not regs: continue
        qc = b.setdefault('qc', {})
        qc['typography_regions'] = regs
        static = [r for r in regs if r['label'] in ('title', 'code file', 'video label', 'caption')]
        if static:
            qc['contrast_regions'] = static
            qc['contrast_reason'] = ('ShaderLab capture beat: Gate V averages ink over the whole frame, which measures the Godot picture (grey stage, pale or dusk floor), not text. '
                                     'The always-visible authored text outside the code card (title, file name, video label, caption) is measured in its own regions; the code card is INK #3D3929 on #FFFEFB (11.5:1) and on its #E6D3C2 highlight (8.0:1), and its highlight band would be averaged in as ink.')
        qc['typography_reason'] = ('ShaderLab capture beat: the Godot picture in the framed window is image content (its mid-tone floor and glow read as '
                                   'text blobs); every authored text region (title, code card, tags, labels, caption, readouts) is listed and checked at native resolution.')
        n += 1
    bsp.write_text(json.dumps(bs, indent=2, ensure_ascii=False) + '\n')
    print(f'{n} ShaderLab beats given typography_regions')

if __name__ == '__main__':
    main()
