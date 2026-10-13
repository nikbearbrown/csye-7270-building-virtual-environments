#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text (a slice of it for the long crosshair file), the cue line numbers
must point at the right lines, the shot list must say exactly what the lanes say, and every cue time must come from where the words fall
in the narration (T() and M() below read narration.py), not from a guess. Re-run after any edit to the lanes OR the narration:
    python3 _gen_lanes.py && python3 make_sheet.py
Timing model. Before the voice exists, an ESTIMATE: each word weighs its letters, plus a pause after a comma, colon or full stop; a phrase starts
at (weight before it) / (weight of the beat). After the build has generated the audio and run the toolkit's word clock
(`runtime/scripts/align.py <this folder>`, which writes mp3/words.json: one entry per word of the narration, in frames), the same calls use
the MEASURED start of the phrase instead, as a fraction of the beat's measured length. Nothing else in this file needs to change:
    python3 _gen_lanes.py && python3 make_sheet.py          # estimate, or measured when mp3/words.json exists and matches the narration
    python3 _gen_lanes.py --times                           # print every phrase used: estimated and measured fraction (to re-place the capture breakpoints)
GEN_WORDS=/path/to/words.json overrides the location of the word clock (used to test the measured path without touching this folder).
Rules enforced at the bottom (check_timing): nothing starts inside the 45 to 55 % window of a beat (the frame the gates sample must be a
settled still); a Manim motion starts by 30 %, or is a quick one (0.35 s at most, done by 44 %) up to 40 %, or starts at 56 % or later.
"""
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
PUB = "godot-shaders/drawing-shapes/"          # under TK/runtime/remotion/public/ (own folder: other films use godot-shaders/ too)
E = []                                         # entries in beat order

_spec = importlib.util.spec_from_file_location("narration", HERE / "narration.py")
NARR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(NARR)
TEXT = {b: t for b, _, t in NARR.BODY}


def _weights(text):
    toks = text.split()
    ws = []
    for tok in toks:
        core = re.sub(r"[^\w']", "", tok)
        w = max(2, len(core))
        if tok.endswith((".", "!", "?")):
            w += 6
        elif tok.endswith(":"):
            w += 4
        elif tok.endswith((",", ";")):
            w += 3
        ws.append(w)
    return toks, ws


def _load_json(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return None


WORDS = _load_json(os.environ.get("GEN_WORDS") or (HERE / "mp3" / "words.json"))     # the toolkit's word clock, after the build ran align.py
_SHEET = _load_json(HERE / "beat_sheet.json") or {}
DURATION = {b.get("beat_id"): b.get("actual_duration_s") for b in _SHEET.get("beats", []) if b.get("actual_duration_s")}
USED = []                                                                          # (bid, phrase) in call order, for --times


def _find(bid, phrase):
    toks = TEXT[bid].split()
    norm = [re.sub(r"[^\w']", "", t).lower() for t in toks]
    tgt = [re.sub(r"[^\w']", "", t).lower() for t in phrase.split()]
    for i in range(len(norm) - len(tgt) + 1):
        if norm[i:i + len(tgt)] == tgt:
            return i
    raise KeyError(f"{bid}: {phrase!r} is not in the narration")


def estimated_start(bid, phrase):
    toks, ws = _weights(TEXT[bid])
    return sum(ws[:_find(bid, phrase)]) / sum(ws)


def measured_start(bid, phrase):
    """The measured start of the phrase as a fraction of the beat, or None while there is no word clock for this beat (or it is stale)."""
    if not WORDS or bid not in WORDS.get("beats", {}):
        return None
    ws = WORDS["beats"][bid]
    if len(ws) != len(TEXT[bid].split()):
        return None
    fps = WORDS.get("fps", 24)
    dur = DURATION.get(bid) or (ws[-1]["endFrame"] / fps)
    return min(1.0, ws[_find(bid, phrase)]["startFrame"] / fps / dur)


def start_of(bid, phrase):
    """Start of `phrase` as a fraction of the beat: measured when the word clock exists, otherwise estimated."""
    USED.append((bid, phrase))
    m = measured_start(bid, phrase)
    return m if m is not None else estimated_start(bid, phrase)


def T(bid, phrase, lead=0.02, prefer=None):
    """Time of an instant change (a highlight, a readout, a ring): just ahead of the words, never inside 45 to 55 % or on the 85 % frame."""
    f = round(max(0.02, start_of(bid, phrase) - lead), 2)
    if 0.45 <= f <= 0.55:
        f = 0.56 if (prefer == "late" or (prefer is None and f > 0.50)) else 0.44
    return nudge(f) if (0.83 <= f <= 0.87) else f


def M(bid, phrase, lead=0.03):
    """Time of a Manim motion and whether it must be a quick one: by 30 %, quick up to 40 %, or from 56 % on."""
    f = round(max(0.02, start_of(bid, phrase) - lead), 2)
    if 0.40 < f < 0.56:
        f = 0.40 if f <= 0.48 else 0.56
    return f, 0.30 < f <= 0.40


def ev(bid, phrase, text, lead=0.03):
    f, quick = M(bid, phrase, lead)
    return {"at": f, "event": text + (" [quick: 0.35 s at most, done by 0.44]" if quick else "")}


def ev0(at, text):
    return {"at": at, "event": text}


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def slice_of(fn, a, b):
    """Lines a..b (1-based, inclusive) of a shader file: real contiguous text."""
    return "\n".join(code_of(fn).split("\n")[a - 1:b])


def cue(at, code, needles, label=None):
    """A ShaderLab cue: the 1-based line numbers (in the DISPLAYED code) of every line containing one of the needles."""
    if isinstance(needles, str):
        needles = [needles]
    lines = [i + 1 for i, ln in enumerate(code.split("\n")) if any(n in ln for n in needles)]
    assert lines, f"no line of the code contains any of {needles}"
    c = {"at": at, "lines": lines}
    if label:
        c["label"] = label
    return c


def rng(at, a, b, label=None):
    """A ShaderLab cue on an explicit range of DISPLAYED lines a..b (1-based, inclusive)."""
    c = {"at": at, "lines": list(range(a, b + 1))}
    if label:
        c["label"] = label
    return c


RO_TOP = (0.2, 0.06)    # status readouts live at the top-left of the result window: clear of every shape this film draws


def ro(at, text, xy=RO_TOP):
    return {"at": at, "text": text, "x": xy[0], "y": xy[1]}


def nudge(f):
    """Move an instant change out of the 45 to 55 % window and off the 85 % frame (the frames the gates sample must be settled)."""
    f = round(f, 2)
    if 0.45 <= f <= 0.55:
        f = 0.44 if f <= 0.50 else 0.56
    if 0.83 <= f <= 0.87:
        f = 0.82 if f < 0.85 else 0.88
    return f


def after(prev, t, gap=0.03):
    """A cue that follows another one: never earlier than `gap` after it, and still outside 45 to 55 %."""
    return nudge(max(t, prev + gap))


# ── dial sweeps: every segment of a video capture is placed from the words (a small search, so any measured word clock gets a schedule) ──
LOW_LIM, HIGH_LIM = 0.44, 0.56      # a move may not overlap (0.44, 0.56): it ends by 0.44 or starts at 0.56, so the 50 % frame is a hold
END_BY = 0.82                       # the last move ends by 82 %, so the 85 % frame is a hold and its readout has settled


def _grid(lo, hi, step=0.01):
    return [round(k * step, 2) for k in range(round(lo / step), round(hi / step) + 1)]


def _clear(s, d):
    """True if a move of length d starting at s stays out of the sampled window (0.44, 0.56)."""
    return s + d <= LOW_LIM + 1e-9 or s >= HIGH_LIM - 1e-9


def avoid(s, d, hi=1.0):
    """Start time for a move of length d wanted at s that does not overlap (0.44, 0.56): it ends at 0.44 or starts at 0.56."""
    if _clear(s, d):
        return s
    cands = [c for c in (LOW_LIM - d, HIGH_LIM) if c >= 0.0 and c + d <= hi]
    return min(cands, key=lambda c: abs(c - s))


def dial_candidates(bid, rise_phrase, drop_phrase=None, drop_d=0.06, hold0=0.04, rise_d=0.18, hold_min=0.02, cover=False):
    """Every placement (cost, drop start, drop length, rise start, rise length) of one dial that keeps its moves out of the sampled window,
    ends by 82 % and leaves a hold of at least `hold_min` at the low value; cheapest first. With `cover`, the low hold must span the whole sampled window (the drop ends by 44 %, the rise starts at 56 % or later). The cost is the distance of the rise from
    its words, of the drop from its words (or from `hold0` before the rise), and a charge for every shortened move."""
    ra = start_of(bid, rise_phrase) - 0.01
    da = (start_of(bid, drop_phrase) - 0.02) if drop_phrase else None
    out = []
    for rd in sorted({rise_d} | {x for x in (0.15, 0.12) if x < rise_d}, reverse=True):
        for r0 in _grid(0.04, END_BY - rd):
            if not _clear(r0, rd) or (cover and r0 < HIGH_LIM - 1e-9):
                continue
            for dd in sorted({drop_d} | {x for x in (0.05, 0.04, 0.03) if x < drop_d}, reverse=True):
                for d0 in _grid(0.02, r0 - dd - hold_min):
                    if not _clear(d0, dd) or (cover and d0 + dd > LOW_LIM + 1e-9):
                        continue
                    want = da if da is not None else (r0 - dd - hold0)
                    out.append((abs(r0 - ra) + 0.6 * abs(d0 - want) + 4.0 * ((rise_d - rd) + (drop_d - dd)), d0, dd, r0, rd))
    out.sort()
    return out


def _dial_result(name, default, low, high, cand):
    _, d0, dd, r0, rd = cand
    d1, r1 = d0 + dd, r0 + rd
    assert _clear(d0, dd) and _clear(r0, rd) and d1 < r0 and r1 <= END_BY + 1e-9, (name, cand)
    return {"name": name, "default": default, "low": low, "high": high, "drop": (round(d0, 2), round(d1, 2)), "rise": (round(r0, 2), round(r1, 2)),
            "cue": nudge(d0), "t_low": nudge(d1 + 0.01), "t_high": nudge(r1 + 0.01), "label": name.replace("_", " ")}


def dial(bid, name, default, rise_phrase, drop_phrase=None, low=0.0, high=1.0, **kw):
    """One dial on its own: default, down to `low`, a hold, up to `high`, a hold to the end (the rise at `rise_phrase`, the drop at `drop_phrase` or just before the rise)."""
    c = dial_candidates(bid, rise_phrase, drop_phrase, cover=True, **kw)
    assert c, f"{bid} {name}: no schedule keeps the moves out of the sampled window"
    return _dial_result(name, default, low, high, c[0])


def dial_pair(bid, first, second):
    """Two dials in one clip: the second drops after the first has finished rising (the first stays at its `high`). `first` and `second` are dicts of
    dial() arguments (name, default, rise_phrase, ...). Returns the pair of schedules with the lowest total cost."""
    def split(spec):
        spec = dict(spec)
        keep = {k: spec.pop(k) for k in ("name", "default", "low", "high") if k in spec}
        return keep, spec
    k1, a1 = split(first)
    k2, a2 = split(second)
    c1 = dial_candidates(bid, **a1)
    c2 = dial_candidates(bid, cover=True, **a2)
    best = None
    for x in c1[:500]:
        end1 = x[3] + x[4]
        for y in c2:
            if y[1] >= end1 + 0.01:
                if best is None or x[0] + y[0] < best[0]:
                    best = (x[0] + y[0], x, y)
                break
    assert best, f"{bid}: no schedule fits the two dials in one clip"
    return (_dial_result(k1["name"], k1["default"], k1.get("low", 0.0), k1.get("high", 1.0), best[1]),
            _dial_result(k2["name"], k2["default"], k2.get("low", 0.0), k2.get("high", 1.0), best[2]))


def pct(x):
    return f"{round(x * 100):d} %"


def sweep_text(sw):
    d0, d1 = sw["drop"]
    r0, r1 = sw["rise"]
    return (f"{sw['name']}: default {sw['default']:g} held to {pct(d0)}, down to {sw['low']:g} by {pct(d1)}, hold at {sw['low']:g} to {pct(r0)}, "
            f"up to {sw['high']:g} by {pct(r1)}, hold to 100 %")


def animate_arg(sw):
    d0, d1 = sw["drop"]
    r0, r1 = sw["rise"]
    kf = [(0.0, sw["default"]), (d0, sw["default"]), (d1, sw["low"]), (r0, sw["low"]), (r1, sw["high"]), (1.0, sw["high"])]
    return f"--animate {sw['name']}:" + ",".join(f"{t:.2f}:{v:g}" for t, v in kf)


SWEEPS = {}         # capture id -> list of sweeps / step lists, printed by --times in harness syntax


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


MANIM_EVIDENCE = {
    "B02": "Illustration (a labelled drawing of the idea); the real answers are the render of C03 (B09)",
    "B03": "By construction: center (0.5, 0.5), pixel (0.62, 0.66); UV runs 0 to 1 and y grows downward (calc uv-corners)",
    "B06": "Illustration of the distance along the middle row, abs(x - 0.5); the circle of B09 matches an independent model on every pixel (analysis-masks.txt)",
    "B07": "Illustration of step; docs: b < a ? 0.0 : 1.0; calculator cells 1 to 4",
    "B08": "Illustration; calculator cells 1 and 2, calc-step-hole, and step(d, r) = 1 - step(r, d) on every pixel (analysis-calcs.txt)",
    "B11": "Illustration of 1 - 1 = 0 and 1 - 0 = 1 (calculator cells 6 to 8); the real ring is C05 (B12)",
    "B20": "Illustration of abs(UV.x - 0.5); the real band is C11 (B22), which matches the model on every pixel",
    "B21": "Illustration of abs; the values -0.3 and 0.3 are plain arithmetic; the real band is symmetric (C11)",
    "B24": "Illustration; the formulas are computed in Godot (calculator cells 17 to 23; max = add-then-cap on every pixel, analysis-calcs.txt) and shown as real renders in B12, B23 and B25",
    "B28": "The code is real text (the vertical-pair line, line 6 of lab-shaders/14-four-arms.gdshader, set as three stacked calls); the lift-out is an illustration of a uniform (docs: uniforms)",
    "B29": "Design advice (EXEMPT): the crosshair file scales its six 0-to-1 sliders by constants (verify-c.gd)",
    "B31": "Docs: 'Global built-ins are available everywhere, including custom functions.'; Lab: UV in a function fails, TIME compiles, uv passed in compiles",
    "B33": "Lab: UV corners (0,0) to (1,1) on a 640 x 360 view; the radius-0.3 circle measures 384 x 216 px, ratio 1.778 = the view's ratio (analysis-calcs.txt)",
    "B34": "Lab: the 480 x 480 circle render has exactly 2 distinct colors; the rows step 24, 42, 54, 64 px (analysis-calcs.txt)",
}


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects + this film's own helpers)"):
    if evidence.startswith("Manim only"):
        evidence = MANIM_EVIDENCE.get(bid, evidence)
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, ramp=None, title=None, code=None, code_file=None, lane="capture", caption="", sparse=None):
    code = code if code is not None else (code_of(shader) if shader else "")
    props = {"layout": layout, "code": code, "codeFile": code_file or (f"lab-shaders/{shader}" if shader else ""), "cues": cues,
             "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption,
             "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    entry = {"lane": lane, "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": intent,
             "motion_claim": motion, "show": show, "runner_up": runner, "why": why, "sparse": (layout == "video") if sparse is None else sparse}
    if entry["sparse"]:
        entry["sparse_reason"] = ("Result-only layout: a square Godot window centred on the 16:9 stage; the underfill is by design because the window "
                                  "is the subject. Only the underfill check is waived.")
    add(bid, act, about, entry, evidence)


def rem(bid, act, about, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, act, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


FWD = "Godot 4.7.2 · Forward+ · the shader on the left"
CROSS = "17-crosshair.gdshader"
CROSS_CODE = code_of(CROSS)

# ═════════════════════════════ ACT I · Inside or Outside ═════════════════════════════
t = T("B01", "No picture file")
lab("B01", 0, "the finished crosshair, drawn with no picture file", None, PUB + "hook-crosshair.mp4",
    "Godot 4.7.2 · Forward+ · dials moved by a script", [],
    "Act title 'Inside or Outside' (serif 40) top-left of the stage. A real Godot render of the finished crosshair in a SQUARE framed window on the cream stage; "
    "a script moves the six dials one after another, each out to 1.0 and back to its default (dot size, ring distance, ring width, then a pause at the defaults, "
    "then arm gap, arm length, arm width). At the top-left of the window a readout 'no picture file' lands as the pause begins; under the window a one-line "
    "caption defines the node the shader paints: 'Color Rect: a flat rectangle the shader paints'.",
    "Each dial moves in turn and the crosshair reshapes with it, so the shape is plainly made by rules and not by a picture; the pause lands on the words 'no picture file'.",
    [ev0(0.0, "crosshair at its defaults, window labelled; the caption defines Color Rect"), ev0(0.04, "the first three dials move, one after another"),
     ev0(max(t, 0.44), "the dials pause at their defaults; readout 'no picture file' lands"), ev0(0.56, "the last three dials move"), ev0(0.96, "back at the defaults")],
    "manim drawing of a crosshair with six dial icons",
    "A real render is the honest proof of 'drawn by a shader, no picture file'; a drawing would only claim it.",
    "C01: lab-shaders/17-crosshair.gdshader, a ColorRect on a square canvas, Forward+, 30 fps, `--length` = the measured audio of B01 (about 13 s). "
    "Keyframes as fractions of the clip, the dials in file order: hold the defaults to 4 %; dot_size, ring_distance, ring_width one after another from 4 % to 44 % "
    "(13.3 % each: 4.4 % up to 1.0, 4.4 % hold, 4.4 % back to its default); hold the defaults from 44 % to 56 % (the 50 % frame is inside this hold; the voice says "
    "'No picture file sits behind it'); arm_gap 56 to 67 % (up to 59.5, hold to 63.5, back to 67), arm_length 67 to 78 % (up to 70.5, hold to 74.5, back to 78), arm_width "
    "78 to 96 % (up to 83, hold at 1.0 to 91 so the 85 % frame is a hold, back to 96); hold 96 % to 100 %. Scripted.",
    "Lab: crosshair defaults and extremes match an independent model, 0 of 230,400 pixels differ; no texture anywhere in the file; Docs: ColorRect is 'A control that displays a solid color rectangle.' (FACTCHECK 74)",
    layout="video", title="Inside or Outside", code_file="lab-shaders/17-crosshair.gdshader",
    caption="Color Rect: a flat rectangle the shader paints", readouts=[ro(max(t, 0.44), "no picture file")])

manim("B02", 0, "a shader asks every pixel a yes-or-no question", "AskEveryPixel",
      "A 13-by-13 grid of outline cells centred on the stage (the pixel grid), the label 'fragment() · once per pixel' above it. One cell near the "
      "middle gets a terracotta ring and a small tag 'my address'; the tag then changes to 'inside?'. Then every cell answers at once: cells within five cells "
      "of the middle fill teal ('yes'), the rest stay empty ('no'), and a circle with a stepped edge appears out of the answers. Caption: 'yes: on · no: off'.",
      "One cell is handed its own address and asks 'inside?', then every cell answers yes or no at the same instant and a circle appears out of the answers.",
      [ev("B02", "The fragment function runs once", "grid and the label 'fragment() · once per pixel'"),
       ev("B02", "and each run is handed", "one cell ringed, tag 'my address'"),
       ev("B02", "So it does not draw a circle", "the tag becomes 'inside?'", lead=0.0),
       ev("B02", "It answers a question about itself", "all cells answer at once; the teal circle forms"),
       ev("B02", "am I inside the circle", "caption 'yes: on · no: off'")],
      "ShaderLab with the circle capture",
      "Yes-or-no answers from every cell forming a circle is the whole idea, and a grid shows it at cell level; the real render arrives in a few beats.")

manim("B03", 0, "a pixel's address, the center, and one pixel to work with", "AddressAndCenter",
      "A square (the UV square) on the cream stage with an 'across · 0 to 1' axis along the top and a 'down · 0 to 1' axis down the left side, the second axis "
      "pointing DOWN. A terracotta cross at the middle labelled 'center · 0.5, 0.5'. A teal dot drops in to the lower right of the center, labelled "
      "'this pixel · 0.62, 0.66'.",
      "The center marker appears, then the pixel's dot drops onto the square and its address label counts up to 0.62, 0.66.",
      [ev0(0.03, "the square with its two axes"), ev("B03", "and where the center is", "center marker and its label"),
       ev("B03", "Our pixel sits", "pixel dot drops in; its address label counts up to 0.62, 0.66")],
      "ShaderLab with a UV picture",
      "An address is a position on a square; a dot with a live label is the clearest picture of it.")

manim("B04", 0, "the distance, worked by hand: 0.12, 0.16, 0.2", "ByHand",
      "The square zooms to the center and the pixel; a caption defines the word: 'distance: how far apart two points are'. A right triangle is drawn between them: the "
      "horizontal leg labelled 0.12, the vertical leg labelled 0.16, the long side between center and pixel. Beside it the arithmetic types in as MathTex, line by "
      "line: 0.12² + 0.16², then = 0.0144 + 0.0256 = 0.04, then √0.04, then = 0.2. The long side takes the label 'distance 0.2' and a terracotta ring.",
      "The two legs draw in, the arithmetic lands line by line, and the long side takes its label.",
      [ev0(0.02, "the square zooms to the center and the pixel; caption defines distance"),
       ev("B04", "It is zero point one two", "the horizontal leg draws, labelled 0.12"),
       ev("B04", "and zero point one six", "the vertical leg draws, labelled 0.16"),
       ev("B04", "Square both", "the arithmetic starts: 0.12² + 0.16²"), ev("B04", "add them", "= 0.0144 + 0.0256 = 0.04"),
       ev("B04", "take the square root", "√0.04"), ev("B04", "exactly zero point two", "= 0.2; the long side labelled 'distance 0.2' and ringed")],
      "LectureEvidenceTable of the numbers",
      "A triangle with its legs and long side is the geometry of a distance; the numbers then land on it as they are spoken.",
      "Calculator cell 0: Godot computes distance((0.62, 0.66), (0.5, 0.5)) = 0.2 within 1e-6 (evidence/planning-checks/calc-results.txt)")

_d = code_of("01-distance.gdshader")
lab("B05", 0, "distance as one function, drawn as alpha", "01-distance.gdshader", PUB + "distance.png", FWD,
    [cue(T("B05", "distance"), _d, "distance(", "distance: how far apart. vec2(0.5) is the center"),
     cue(T("B05", "Feed the answer into", prefer="late"), _d, "COLOR", "alpha: how visible a pixel is: 0 invisible, 1 solid")],
    "Code card at left (the six-line shader, blank line and braces included; the distance line, then the color line, highlighted in turn); at right a real Godot window with the "
    "radial picture: nothing visible in the middle, more teal toward the edges. A label on the distance line glosses vec2(0.5) as the center; a label on the color "
    "line defines the new word: 'alpha: how visible a pixel is: 0 invisible, 1 solid'. A ring on the pixel worked by hand (0.62, 0.66) with the readout 'd = 0.2', "
    "and 'd = 0.7' near a corner; a thin 0 to 0.7 strip under the window with a marker.",
    "The highlight moves from the distance line to the color line while a marker runs up the strip as the picture fills in toward the edges.",
    [ev0(T("B05", "distance"), "distance line highlighted: how far apart, and vec2(0.5) is the center"),
     ev0(T("B05", "Give it the pixel's address"), "ring on our pixel; readout d = 0.2"),
     ev0(T("B05", "Feed the answer into", prefer="late"), "color line highlighted and alpha defined; the marker starts"),
     ev0(T("B05", "and the middle fades out"), "readout d = 0.7 near the corner")],
    "LectureCodeTrace alone",
    "Code beside the picture of the number growing outward: the picture is what makes 'distance is a ramp from the center' visible.",
    "C02: lab-shaders/01-distance.gdshader, still on a square canvas, Forward+ (probes: (0.5, 0.2) reads 0.7059, 0.7765, 0.7255; corner reads "
    "0.5098, 0.698, 0.6353; the middle is the stage color).",
    "Lab: alpha recovered from the pixels equals the distance within 0.006 on all 230,400 pixels",
    ramp={"at": T("B05", "Feed the answer into", prefer="late"), "from": 0, "to": 0.7}, caption="distance(a, b): how far apart two points are",
    readouts=[{"at": T("B05", "Give it the pixel's address"), "text": "d = 0.2", "x": 0.77, "y": 0.62},
              {"at": T("B05", "and the middle fades out"), "text": "d = 0.7", "x": 0.88, "y": 0.9}],
    rings=[{"at": T("B05", "Give it the pixel's address"), "box": [0.59, 0.63, 0.65, 0.69]}])

manim("B06", 0, "inside means the distance is under the radius", "BelowTheLine",
      "A plot on the cream stage: the x axis 'across the shape' from 0 to 1, the y axis 'distance from the middle' from 0 to 0.5. A V-shaped teal "
      "curve (0.5 at both ends, 0 at x = 0.5). A horizontal terracotta line at 0.3 labelled 'radius 0.3'. A grey dot starts on the V at the left end, above the "
      "line; it then rides the V to the right, turning teal under the line, and the stretch of the x axis where the V lies under the line (x from 0.2 to 0.8) "
      "lights up and is labelled 'inside'.",
      "The V draws in, the radius line slides down to 0.3, a dot rides the V and turns teal under the line, and the stretch of the axis beneath it lights up as 'inside'.",
      [ev0(0.02, "axes and the V of distances"), ev("B06", "say zero point three", "the radius line slides to 0.3, labelled"),
       ev("B06", "A pixel is inside", "a grey dot appears on the V, above the line"),
       ev("B06", "the distance dips to zero", "the dot rides the V, turns teal under the line; the stretch under the line lights", lead=0.0),
       ev("B06", "Everything under the line", "the lit stretch is labelled 'inside'")],
      "ShaderLab with a ramp strip",
      "A function against a threshold line is a plot; the lit stretch under the line is the claim.")

manim("B07", 0, "step: zero below the edge, one from the edge on", "StepJump",
      "A small plot: the x axis 'value' from 0 to 0.6, the y axis 'output' from 0 to 1. A vertical terracotta line at 0.3 labelled 'edge'. A dot labelled 'value' "
      "starts left of the edge with a readout beside it. The step curve draws in two stretches: output 0 left of the edge, then output 1 from the edge on, labelled "
      "'step(edge, x)'. The dot slides across the edge and the readout flips from 0 to 1. Caption (the glossary's wording): '0 below the edge, 1 from the edge up'.",
      "A dot slides along the axis and the output jumps from 0 to 1 at the edge.",
      [ev("B07", "use step", "axes and the edge line, labelled 'edge'"), ev("B07", "Give it an edge and a value", "the dot appears left of the edge; readout 0"),
       ev("B07", "It returns zero while", "the left stretch of the curve (output 0) draws"),
       ev("B07", "and one once the value reaches it", "the dot crosses the edge; the readout flips to 1; the right stretch draws"),
       ev("B07", "A switch that flips", "caption '0 below the edge, 1 from the edge up'")],
      "LectureEvidenceTable of three inputs and their outputs",
      "A jump at an edge is a motion; a table would only list the values.",
      "Docs: step is `b < a ? 0.0 : 1.0`; calculator cells 1 to 4 (below 0, above 1, equal 1)")

manim("B08", 0, "mind the order of step's two inputs: the flip", "StepFlip",
      "A row of 25 pixel cells with centres at x = 0.02, 0.06, ... 0.98 (cells 5 to 19, the ones within 0.3 of the middle, are inside; no cell lies exactly on 0.3) "
      "with the V profile above it and the radius line. Below, a row of 0 and 1 values. First the label 'step(0.3, d)' and the small question 'd ≥ radius?': inside "
      "cells read 0 (empty), outside cells read 1 (teal), a hole. Then the two inputs trade places in the label to 'step(d, 0.3)', the question becomes 'radius ≥ d?' "
      "and the row flips: inside cells read 1 (teal), outside cells 0 (empty). Cells are numbered from 0. A terracotta ring marks cell 17, a pixel at distance 0.2 like ours (our own pixel is off this row), throughout. At the end the teal stretch is labelled 'the circle'.",
      "The two inputs trade places and the row of ones and zeros flips inside out.",
      [ev0(0.02, "the row, the profile and the radius line; ring on cell 17 (distance 0.2)"), ev("B08", "With the radius first", "label 'step(0.3, d)'"),
       ev("B08", "has the distance reached", "question 'd ≥ radius?'"),
       ev("B08", "Inside the circle", "all cells answer at once: inside 0, outside 1 (a hole)"),
       ev("B08", "Swap them", "inputs swap places in the label; the row flips"),
       ev("B08", "has the radius reached", "question 'radius ≥ d?'"), ev("B08", "That's our circle", "label 'the circle' under the teal stretch")],
      "ShaderLab with a capture of the hole",
      "The flip happens to a whole row at once, so the motion is the claim; the real circle follows in the next beat.",
      "Calculator cells 1 and 2; Lab calc-step-hole (middle = stage, outside = teal); flip equals 1 - step(r, d) on all 230,400 pixels")

_c = code_of("02-circle.gdshader")
lab("B09", 0, "the circle, and the word mask", "02-circle.gdshader", PUB + "circle.png", FWD,
    [cue(T("B09", "distance zero point two"), _c, "distance("), cue(T("B09", "radius zero point three"), _c, "step(d", "1 inside · 0 outside"),
     cue(T("B09", "Those ones and zeros"), _c, "COLOR")],
    "Code card at left (the seven-line circle shader; the distance, step and color lines highlighted in turn); at right a real Godot window with a "
    "teal circle (radius 0.3) on the stage. A ring on our pixel (0.62, 0.66, inside) with the readout 'step: 1', then a ring on a pixel at distance "
    "0.4 (0.5, 0.9, outside) with 'step: 0'; the caption defines the new word in the glossary's wording: 'mask: a number from 0 to 1 per pixel saying how much of something to show'.",
    "The highlight steps from the distance line to the step line to the color line while one ring visits our pixel (step says 1) and then a pixel "
    "outside (step says 0).",
    [ev0(T("B09", "distance zero point two"), "distance line"), ev0(T("B09", "radius zero point three"), "step line"),
     ev0(T("B09", "so step says one"), "ring on our pixel; readout step: 1"),
     ev0(T("B09", "A pixel at distance zero point four", prefer="late"), "ring on a pixel at distance 0.4; readout step: 0"),
     ev0(T("B09", "Those ones and zeros"), "color line; the caption defines mask")],
    "manim circle with the per-pixel numbers",
    "The real render with the code that made it, and the new word 'mask' defined on screen where it is first spoken.",
    "C03: lab-shaders/02-circle.gdshader, still on a square canvas, Forward+ (probes: middle, (0.5, 0.25) and our pixel (0.62, 0.66) teal "
    "0.3686, 0.6392, 0.5686; (0.5, 0.15), (0.5, 0.9) at distance 0.4, and the corner stage 0.851, 0.8353, 0.7922).",
    "Lab: 0 of 230,400 pixels differ from an independent model; exactly 2 colors in the picture",
    caption="mask: a number from 0 to 1 per pixel saying how much of something to show",
    readouts=[{"at": T("B09", "so step says one"), "text": "step: 1", "x": 0.78, "y": 0.62},
              {"at": T("B09", "A pixel at distance zero point four", prefer="late"), "text": "step: 0", "x": 0.7, "y": 0.9}],
    rings=[{"at": T("B09", "so step says one"), "box": [0.59, 0.63, 0.65, 0.69]},
           {"at": T("B09", "A pixel at distance zero point four", prefer="late"), "box": [0.47, 0.87, 0.53, 0.93]}])

_s = code_of("03-circle-slider.gdshader")
_rad = dial("B10", "radius", 0.3, "Turn the dial and the circle grows", drop_phrase="and the circle gets a dial", low=0.1, high=0.45, drop_d=0.18, rise_d=0.20)
SWEEPS["C04"] = [_rad]
lab("B10", 0, "the radius as a uniform: a dial", "03-circle-slider.gdshader", PUB + "circle-slider.mp4",
    "Godot 4.7.2 · Forward+ · radius moved by a script",
    [cue(T("B10", "a uniform"), _s, "uniform"), cue(T("B10", "The shader reads it"), _s, "step(d"),
     cue(T("B10", "What follows the colon"), _s, "uniform", "hint_range: a slider from 0 to 0.5")],
    "Code card at left (the uniform line, then the line that reads it, then the uniform line again, labelled with what this hint does); at right a real Godot window "
    "where the circle shrinks to radius 0.1 and then grows to 0.45 as a script moves the radius; the value reads out at the top-left of the window. A caption under the "
    "window defines the new word in the glossary's wording: 'hint: the word after a colon that tells Godot how to treat a uniform'.",
    "The circle shrinks and then grows as the radius value changes, and ends large.",
    [ev0(T("B10", "a uniform"), "uniform line: a value set from outside"), ev0(_rad["drop"][0], "the circle shrinks to radius 0.1"), ev0(_rad["t_low"], "readout 0.1"),
     ev0(T("B10", "The shader reads it"), "the line that reads the radius"), ev0(_rad["rise"][0], "the circle grows to radius 0.45"), ev0(_rad["t_high"], "readout 0.45"),
     ev0(T("B10", "What follows the colon"), "uniform line again: hint_range is a slider")],
    "GodotDevWorkbench (labelled reconstruction of the Inspector)",
    "A real sweep shows what the number does; the Inspector itself is shown by a real editor capture in the last act.",
    "C04: lab-shaders/03-circle-slider.gdshader, 30 fps, `--length` = the measured audio of B10 (about 12 s), Forward+. `radius` as fractions of the clip: " + sweep_text(_rad) +
    "; the voice says 'Turn the dial and the circle grows' as it rises. The 50 % frame is inside the hold at 0.1 and the 85 % frame in the final hold. Scripted. Harness: `" + animate_arg(_rad) + "`.",
    "Lab: radius 0.1, 0.3 and 0.45 match the model on every pixel (coverage 0.0314, 0.2828, 0.6363)",
    caption="hint: the word after a colon that tells Godot how to treat a uniform", readouts=[ro(_rad["t_low"], "0.1"), ro(_rad["t_high"], "0.45")])

# ═════════════════════════════ ACT II · Rings and Cutouts ═════════════════════════════
manim("B11", 1, "a ring is one mask subtracted from another", "SubtractMasks",
      "Act title 'Rings and Cutouts' (serif 40) top-left. A big teal disc labelled 'outer mask'. A smaller teal disc labelled 'inner mask' hovers "
      "above it with a minus sign between them. The small disc drops onto the big disc's center and cuts: the middle turns empty (the stage color), "
      "leaving a ring labelled 'ring'. Two number tags, set beside the shapes on leader lines and never on a fill: '1 − 1 = 0' by the hole and '1 − 0 = 1' by the band.",
      "The small disc drops into the big one and the middle empties, leaving a ring.",
      [ev0(0.02, "act title; the big disc"), ev("B11", "Draw the big mask", "label 'outer mask'"),
       ev("B11", "draw the small mask", "the small disc hovers above, labelled 'inner mask'; the minus sign pops in"),
       ev("B11", "Where both say one", "the small disc drops and cuts: a ring", lead=0.0),
       ev("B11", "one minus one leaves zero", "tag '1 − 1 = 0' beside the hole"), ev("B11", "Only the strip", "tag '1 − 0 = 1' beside the band; label 'ring'")],
      "ShaderLab with the ring capture",
      "A disc dropped out of a disc is the subtraction itself; the code and the real render come in the next beat.")

_r = code_of("04-ring.gdshader")
lab("B12", 1, "the ring in code: two steps and a minus", "04-ring.gdshader", PUB + "ring.png", FWD,
    [cue(T("B12", "The outer circle"), _r, "outer ="), cue(T("B12", "the inner one", prefer="late"), _r, "inner ="),
     cue(T("B12", "Their difference is a ring"), _r, "COLOR")],
    "Code card at left (the ring shader; the outer line, the inner line and the subtraction highlighted in turn); at right a real Godot window with "
    "a teal ring (outer radius 0.35, inner 0.3) on the stage. Readouts 'outer 0.35' above the ring, 'inner 0.3' in the hole, 'width 0.05' below; "
    "one ring marks the top of the band.",
    "The highlight moves line by line and the three readouts land on the ring as each number is named.",
    [ev0(T("B12", "The outer circle"), "outer line; readout outer 0.35"), ev0(T("B12", "the inner one", prefer="late"), "inner line; readout inner 0.3"),
     ev0(T("B12", "Their difference is a ring"), "the subtraction; ring on the band"), ev0(T("B12", "five hundredths wide"), "readout width 0.05")],
    "LectureCodeTrace alone",
    "Code and the ring it makes together, with the three numbers sitting where they apply.",
    "C05: lab-shaders/04-ring.gdshader, still on a square canvas, Forward+ (probes: middle = stage; (0.5, 0.18) teal; (0.5, 0.13) stage).",
    "Lab: 0 of 230,400 pixels differ from an independent model (coverage 0.1021)",
    readouts=[{"at": T("B12", "The outer circle"), "text": "outer 0.35", "x": 0.5, "y": 0.06},
              {"at": T("B12", "the inner one", prefer="late"), "text": "inner 0.3", "x": 0.5, "y": 0.5},
              {"at": T("B12", "five hundredths wide"), "text": "width 0.05", "x": 0.5, "y": 0.95}],
    rings=[{"at": T("B12", "Their difference is a ring"), "box": [0.4, 0.12, 0.6, 0.23]}])

rem("B13", 1, "the ring in numbers: three pixels", "LectureEvidenceTable",
    {"title": "Three pixels, by hand", "headers": ["Distance", "Outer", "Inner", "Ring"],
     "rows": [["0.20", "1", "1", "0"], ["0.33", "1", "0", "1"], ["0.45", "0", "0", "0"]],
     "note": "Godot 4.7.2 · ring = outer − inner",
     "cues": [T("B13", "At distance zero point two"), T("B13", "At zero point three three", prefer="late"), T("B13", "At zero point four five")],
     "durationSeconds": "__AUDIO__"},
    "A four-column table, one row per pixel (distance 0.20, 0.33, 0.45), each row revealed and ringed as the voice reaches it; the last column is the ring mask.",
    "The ring steps down the three rows with the voice.",
    [ev0(T("B13", "At distance zero point two"), "distance 0.20 row"), ev0(T("B13", "At zero point three three", prefer="late"), "distance 0.33 row"),
     ev0(T("B13", "At zero point four five"), "distance 0.45 row")],
    "manim: a row of cells with the numbers above them",
    "Plugging numbers in for three pixels is the habit being taught; a three-row table with one row ringed per pixel is exactly that.",
    "Calculator cells 6, 7, 8 (0, 1, 0), Godot 4.7.2")

_o = code_of("05-overlap-sum.gdshader")
_o1 = T("B14", "Now overlap two circles")
_o2 = after(_o1, T("B14", "two circles"))
_o3 = after(_o2, T("B14", "add their masks"))
lab("B14", 1, "two masks added: the overlap is two, and looks like one", "05-overlap-sum.gdshader", PUB + "overlap-sum.png",
    "Godot 4.7.2 · Forward+ · default project settings · the shader on the left",
    [cue(_o1, _o, "float a"), cue(_o2, _o, "float b"), cue(_o3, _o, "float mask")],
    "Code card at left (two circle masks and their sum); at right a real Godot window with two overlapping teal circles that read as one solid "
    "shape. One ring marks the overlap lens; readouts 'sum = 2' inside it and 'looks like 1' at the top-left of the window.",
    "The ring settles on the overlap and the readouts say two, then 'looks like 1'.",
    [ev0(_o1, "mask a"), ev0(_o2, "mask b"), ev0(_o3, "the sum line"),
     ev0(T("B14", "so the sum is two"), "ring on the overlap; readout sum = 2"), ev0(T("B14", "an alpha of two looks exactly like one"), "readout 'looks like 1'")],
    "manim: two circles with number labels",
    "A real render makes the point that the overlap is invisible as a doubling; the readouts say what the screen cannot.",
    "C06: lab-shaders/05-overlap-sum.gdshader, still on a square canvas, Forward+ (probes: middle and (0.3, 0.5) teal; (0.9, 0.5) stage).",
    "Lab: 0 of 230,400 pixels differ from the model; in a default project alpha 2.0 reads the same as 1.0 on Forward+ and on Compatibility (calc alpha-clamp); with 2D HDR switched on it does NOT (run-d), which is why the voice says 'in a default project'",
    readouts=[{"at": T("B14", "so the sum is two"), "text": "sum = 2", "x": 0.5, "y": 0.5}, ro(T("B14", "an alpha of two looks exactly like one"), "looks like 1")],
    rings=[{"at": T("B14", "so the sum is two"), "box": [0.37, 0.28, 0.63, 0.72]}])

_h = code_of("06-overlap-hole-bug.gdshader")
lab("B15", 1, "the cutout that vanishes", "06-overlap-hole-bug.gdshader", PUB + "hole-bug.png", FWD,
    [cue(T("B15", "Cut a small hole"), _h, "float hole"), cue(T("B15", "by subtracting"), _h, "float mask"),
     cue(T("B15", "One plus one minus one"), _h, "float mask")],
    "Code card at left (the same two circles, a third mask for a hole, and a + b - hole); at right a real Godot window: two overlapping circles, "
    "solid, with NO hole. One ring marks the spot in the middle where the hole should be; readout 'hole: missing' at the top-left of the window.",
    "The ring lands on the middle of the solid shape, exactly where the hole was supposed to be.",
    [ev0(T("B15", "Cut a small hole"), "the third mask: a small hole"), ev0(T("B15", "by subtracting"), "a + b - hole"),
     ev0(T("B15", "It does not", prefer="late"), "ring on the middle; readout hole: missing"), ev0(T("B15", "One plus one minus one"), "the mask line again")],
    "manim: three masks and their sum",
    "A real render of the code a viewer might write: the missing hole is the bug, plainly visible.",
    "C07: lab-shaders/06-overlap-hole-bug.gdshader, still on a square canvas, Forward+ (probe: the middle (0.5, 0.5) is TEAL: the hole is absent).",
    "Lab: 0 of 230,400 pixels differ from the model; the overlap in the hole reads 1 + 1 - 1 = 1 (calculator cell 11)",
    readouts=[ro(T("B15", "It does not", prefer="late"), "hole: missing")], rings=[{"at": T("B15", "It does not", prefer="late"), "box": [0.42, 0.42, 0.58, 0.58]}])

rem("B16", 1, "the hidden two, in numbers", "LectureEvidenceTable",
    {"title": "The hidden two", "headers": ["Pixel", "Wanted", "a + b − hole"],
     "rows": [["one circle", "1", "1"], ["the overlap", "1", "2"], ["the hole", "0", "1"]],
     "note": "Godot 4.7.2 · mask = a + b − hole",
     "cues": [T("B16", "Inside one circle"), T("B16", "In the overlap"), T("B16", "In the hole", prefer="early")],
     "durationSeconds": "__AUDIO__"},
    "A three-column table, one row per kind of pixel (one circle, the overlap, the hole), each row revealed and ringed as the voice reaches it; the third column reads "
    "1, 2, 1 and the hole row (the whole row is ringed: the table rings rows, not cells) shows 1 where 0 is wanted. No fix is in the table: min arrives in the next beat.",
    "The ring steps down the rows and lands on the hole row, where the third column reads 1 and 0 was wanted.",
    [ev0(T("B16", "Inside one circle"), "one circle row"), ev0(T("B16", "In the overlap"), "the overlap row: 2"),
     ev0(T("B16", "In the hole", prefer="early"), "the hole row: 1, wanted 0, ringed")],
    "manim: a number line from -1 to 2",
    "Three kinds of pixel, wanted against got, is a table; the one wrong row can be ringed.",
    "Calculator cells 9 to 11, Godot 4.7.2")

_f = code_of("07-overlap-hole-fixed.gdshader")
lab("B17", 1, "the fix: cap the sum at one with min", "07-overlap-hole-fixed.gdshader", PUB + "hole-fixed.png", FWD,
    [cue(T("B17", "with min"), _f, "float mask", "min: the smaller of two values"), cue(T("B17", "and the hole takes it down"), _f, "float mask")],
    "Code card at left (the same shader; the mask line now reads min(a + b, 1.0) - hole, highlighted); at right a real Godot window: the same two "
    "circles, now WITH the hole in the middle, ringed; readout 'hole: there' at the top-left of the window.",
    "The min line lights up and the ring settles on the hole that now exists.",
    [ev0(T("B17", "with min"), "the min line: the smaller of two values"), ev0(T("B17", "and the hole takes it down"), "the mask line again"),
     ev0(T("B17", "Now the hole appears"), "ring on the hole; readout hole: there")],
    "manim: a number line with the cap at one",
    "The same scene as the last beat with a one-word fix, so the hole appearing is the proof.",
    "C08: lab-shaders/07-overlap-hole-fixed.gdshader, still on a square canvas, Forward+ (probe: the middle (0.5, 0.5) is STAGE: the hole is there).",
    "Lab: 0 of 230,400 pixels differ from the model (coverage 0.2916, 0.0201 less than the bug: the hole's area); calculator cells 12 and 13",
    readouts=[ro(T("B17", "Now the hole appears"), "hole: there")], rings=[{"at": T("B17", "Now the hole appears"), "box": [0.42, 0.42, 0.58, 0.58]}])

_n = code_of("08-negative-eats-dot.gdshader")
lab("B18", 1, "the mirror-image bug: a bite that reaches past the disc takes the spot below zero", "08-negative-eats-dot.gdshader", PUB + "negative-bug.png", FWD,
    [rng(T("B18", "Cut a bite from the disc"), 4, 5), cue(T("B18", "There", prefer="early"), _n, "float mask"), cue(T("B18", "Add a spot there"), _n, "float spot")],
    "Code card at left (a disc, a bite cut from it, a small spot, and disc - bite + spot); at right a real Godot window: a teal disc with a round bite out of its "
    "right side and NOTHING in the stretch of the bite that reaches past the disc's edge. One ring marks that stretch, then a smaller ring marks where the spot should be. "
    "A readout just below the ring (at the foot of the bite, under the spot's place) reads 'mask −1' and then 'mask 0'; 'spot: missing' lands at the top-left of the window.",
    "The ring marks the stretch of the bite past the disc, the readout there says minus one, and then the spot's place stays empty.",
    [ev0(T("B18", "Cut a bite from the disc"), "disc and bite lines"), ev0(T("B18", "reaching past its edge"), "ring on the stretch of the bite past the disc"),
     ev0(T("B18", "There", prefer="early"), "mask line; readout mask −1 below the spot's place"), ev0(T("B18", "Add a spot there"), "spot line; smaller ring where the spot should be"),
     ev0(T("B18", "minus one plus one"), "readout becomes mask 0"), ev0(T("B18", "so it never shows"), "readout spot: missing")],
    "manim: a number line with minus one marked",
    "A real render shows the symptom (the spot is missing), which no number line would; the arithmetic is in the readouts and the voice.",
    "C09: lab-shaders/08-negative-eats-dot.gdshader, still on a square canvas, Forward+ (probes: (0.88, 0.5), where the spot should be, reads the STAGE color "
    "0.851, 0.8353, 0.7922; (0.7, 0.5) stage; (0.4, 0.5) teal; (0.9, 0.35) stage).",
    "Lab: 0 of 230,400 pixels differ from the model (coverage 0.2290); calculator cells 14 and 15 (0 - 1 = -1; then + 1 = 0); alpha -1 reads the same as 0 in a default project (calc alpha-clamp)",
    readouts=[{"at": T("B18", "There", prefer="early"), "text": "mask −1", "x": 0.88, "y": 0.76}, {"at": T("B18", "minus one plus one"), "text": "mask 0", "x": 0.88, "y": 0.76},
              ro(T("B18", "so it never shows"), "spot: missing")],
    rings=[{"at": T("B18", "reaching past its edge"), "box": [0.72, 0.3, 0.99, 0.7]}, {"at": T("B18", "Add a spot there"), "box": [0.78, 0.4, 0.98, 0.6]}])

_m = code_of("09-negative-fixed.gdshader")
lab("B19", 1, "the fix: max against zero; the rule for both bugs", "09-negative-fixed.gdshader", PUB + "negative-fixed.png", FWD,
    [cue(T("B19", "The fix is max"), _m, "float mask", "max: the larger of two values"), cue(T("B19", "Max of minus one"), _m, "float mask")],
    "Code card at left (the same shader; the mask line now reads max(disc - bite, 0.0) + spot, highlighted); at right a real Godot window with the "
    "same disc and bite and the spot now THERE, ringed. A readout below the spot (so it does not cover it) reads 'mask 0' (after the max) and then 'mask 1' (after the spot adds one); "
    "'spot: there' lands at the top-left; a caption states the rule: 'after adding, cap at one · after subtracting, floor at zero'.",
    "The max line lights up, the readout goes from 0 to 1 and the ring settles on the spot that now shows.",
    [ev0(T("B19", "The fix is max"), "the max line: the larger of two values"), ev0(T("B19", "Max of minus one"), "readout mask 0 below the spot"),
     ev0(T("B19", "and then the spot adds one"), "readout mask 1; ring on the spot; readout spot: there"),
     ev0(T("B19", "The rule for both bugs"), "the caption states the rule (on screen from the start of the beat)")],
    "manim: a strip from -1 to 2 with the 0 to 1 zone shaded",
    "The spot coming back is the proof; the rule for both bugs is stated in the voice and on the caption.",
    "C10: lab-shaders/09-negative-fixed.gdshader, still on a square canvas, Forward+ (probes: (0.88, 0.5) reads TEAL 0.3686, 0.6392, 0.5686: the spot is there; "
    "(0.7, 0.5) stage; (0.4, 0.5) teal; (0.9, 0.35) stage).",
    "Lab: 0 of 230,400 pixels differ from the model (coverage 0.2491, 0.0201 more than the bug: the spot's area); calculator cells 16 and 18",
    caption="after adding, cap at one · after subtracting, floor at zero",
    readouts=[{"at": T("B19", "Max of minus one"), "text": "mask 0", "x": 0.88, "y": 0.76}, {"at": T("B19", "and then the spot adds one"), "text": "mask 1", "x": 0.88, "y": 0.76},
              ro(T("B19", "and then the spot adds one"), "spot: there")],
    rings=[{"at": T("B19", "and then the spot adds one"), "box": [0.78, 0.4, 0.98, 0.6]}])

# ═════════════════════════════ ACT III · Lines and Crosses ═════════════════════════════
manim("B20", 2, "distance to a line: how far right of the middle the pixel is", "DistanceToALine",
      "Act title 'Lines and Crosses' (serif 40) top-left. The UV square with a grey dot at its center ringed by a thin circle (a circle measures distance to a point); "
      "its top axis is tagged 'UV.x · horizontal address' and its left axis 'UV.y · vertical address', which defines the code notation where it is first used. "
      "The circle fades and the vertical middle line draws in grey; a caption defines the new word in the glossary's wording, set as two lines so no text object "
      "runs past twelve words: 'band: the strip of pixels near a line or an edge,' / 'as wide as the thickness or the softness'. A teal dot at (0.7, 0.4); a horizontal terracotta "
      "segment runs from the dot to the line, labelled 'UV.x − 0.5'. When the voice says how far right it sits, the length label 0.2 appears; the dot then moves to two "
      "other places on the right and the segment and its length follow.",
      "The circle gives way to a line, and the dot moves while the horizontal segment to the middle line stretches and shrinks with a live length label.",
      [ev0(0.02, "act title; the square with its two tagged axes, the center dot and its circle"), ev("B20", "A band measures it", "the circle fades; the middle line draws; the caption defines band"),
       ev("B20", "subtract a half from", "the teal dot appears; the segment to the line draws, labelled 'UV.x − 0.5'"),
       ev("B20", "and you get how far right", "the length label 0.2; the dot moves to two other places and the segment follows")],
      "ShaderLab with the distance picture",
      "Distance to a line is a length you can see: a segment with a live label is the clearest picture of it.")

manim("B21", 2, "abs folds the left side onto the right", "AbsFold",
      "A horizontal number line from -0.5 to 0.5 labelled 'UV.x − 0.5' with a vertical tick at 0. A dot at -0.3 reads -0.3. A caption (the glossary's wording) 'abs: drops the "
      "minus sign: -0.3 becomes 0.3'. The left half of the line folds over the zero tick onto the right half (a mirror), the dot lands at +0.3 and reads 0.3. A "
      "V-shaped plot of the folded values sits under the line.",
      "The left half folds over onto the right and the dot lands on the positive side.",
      [ev0(0.02, "the line and the dot at -0.3"), ev("B21", "The function abs drops", "caption: abs drops the minus sign"),
       ev("B21", "it folds the left", "the fold begins and settles on the right; the dot reads 0.3", lead=0.0), ev("B21", "so one formula measures", "the V plot of the folded values")],
      "LectureEvidenceTable of before and after values",
      "A fold is a motion; a table would list -0.3 and 0.3 without showing why.")

_b = code_of("10-band.gdshader")
_m1 = T("B22", "measure", prefer="late")
_m2 = after(_m1, T("B22", "compare get one"))
_m3 = after(_m2, T("B22", "get one or zero"))
lab("B22", 2, "a band: measure, compare, get one or zero", "10-band.gdshader", PUB + "band.png", FWD,
    [cue(T("B22", "Compare that distance"), _b, "float across", "abs: drops the minus sign: -0.3 becomes 0.3"), cue(T("B22", "and step gives a vertical band"), _b, "float band"),
     cue(_m1, _b, "float across"), cue(_m2, _b, "float band"), cue(_m3, _b, "COLOR")],
    "Code card at left (across, band, color); at right a real Godot window with a vertical teal band down the middle, 0.1 wide. Readout "
    "'half-width 0.05' at the top-left of the window as the voice says 'half the band's width'.",
    "The highlight moves from across to band to color as each is named, and the band is already on screen.",
    [ev0(T("B22", "Compare that distance"), "across: abs of the address minus a half (abs defined)"), ev0(T("B22", "half the band's width"), "readout half-width 0.05"),
     ev0(T("B22", "and step gives a vertical band"), "band: step against half the width"), ev0(_m1, "measure: the across line"),
     ev0(_m2, "compare: the band line"), ev0(_m3, "get one or zero: the color line")],
    "manim: the band drawn over the V plot",
    "The real band with the three lines that make it.",
    "C11: lab-shaders/10-band.gdshader, still on a square canvas, Forward+ (probes: (0.5, 0.1) and the middle teal; (0.7, 0.5) stage).",
    "Lab: 0 of 230,400 pixels differ from the model (coverage 0.1000)",
    readouts=[ro(T("B22", "half the band's width"), "half-width 0.05")])

_x = code_of("11-cross.gdshader")
lab("B23", 2, "a cross is either band: max, not a sum", "11-cross.gdshader", PUB + "cross.png", FWD,
    [rng(T("B23", "A cross is every pixel"), 6, 7), cue(T("B23", "Take the larger of the two masks"), _x, "float mask", "max: the larger of two values")],
    "Code card at left (the two band masks and the max); at right a real Godot window with a teal cross whose arms run to the edges. A readout on the middle "
    "reads 'max gives 1'; later, in the same place, it becomes 'adding gives 2'.",
    "The highlight lands on the max line, then the readout on the middle shows what max gives and then what a sum would give.",
    [ev0(T("B23", "A cross is every pixel"), "the two band lines"), ev0(T("B23", "Take the larger of the two masks"), "max line: the larger of two values"),
     ev0(T("B23", "with max"), "readout max gives 1"), ev0(T("B23", "Adding alone would put a two"), "readout adding gives 2")],
    "manim: the cross assembled from two bands",
    "The real cross plus the two readouts, which carry the hidden-two idea from the last act into a new shape.",
    "C12: lab-shaders/11-cross.gdshader, still on a square canvas, Forward+ (probes: middle, (0.5, 0.1), (0.1, 0.5) teal; (0.1, 0.1) stage).",
    "Lab: 0 of 230,400 pixels differ from the model (coverage 0.1900 = 2 x 0.1 - 0.1 x 0.1); max = min(a + b, 1) on every pixel of the two-circle picture (calc max-equals-capped-sum); calculator cell 21",
    readouts=[{"at": T("B23", "with max"), "text": "max gives 1", "x": 0.5, "y": 0.5}, {"at": T("B23", "Adding alone would put a two"), "text": "adding gives 2", "x": 0.5, "y": 0.5}])

manim("B24", 2, "three ways to combine masks: either, both, cutout", "ThreeWays",
      "Two overlapping circle outlines, a (left) and b (right), in grey with a faint label each. Three captions arrive in turn under the pair, each "
      "with the region it names shaded teal: 'either · max(a, b)' (the union), 'both · a × b' (the lens), 'cutout · max(a − b, 0)' (a with b taken "
      "out, a crescent). Then a strip from -1 to 2 with the zero-to-one zone shaded: tags 'max' and 'a × b' sit inside the zone; tags 'a + b' and 'a − b' "
      "slide out of it, to 2 and to -1.",
      "The same two circles light up three different regions as each combination is named, then two tags stay in the zero-to-one zone and two leave it.",
      [ev0(0.03, "the two circles"), ev("B24", "For either", "either: the union lights"), ev("B24", "For both", "both: the lens lights"),
       ev("B24", "For a cutout", "cutout: the crescent lights"), ev("B24", "Max and multiply stay", "the strip; max and a × b sit inside the zone"),
       ev("B24", "Adding and subtracting can leave", "a + b slides out to 2; a − b slides out to -1")],
      "LectureEvidenceTable of three formulas",
      "Which region each formula selects is a picture; a table would list the formulas without the regions.",
      "Calculator cells 17 to 23 (min, max, product, union), Godot 4.7.2")

_a = code_of("12-arm-rectangle.gdshader")
lab("B25", 2, "an arm: two conditions multiplied", "12-arm-rectangle.gdshader", PUB + "arm-rectangle.png", FWD,
    [cue(T("B25", "not too far along the line"), _a, "float not_too_far"), cue(T("B25", "and close to it"), _a, "float near_line"),
     cue(T("B25", "Two masks", prefer="late"), _a, "float mask")],
    "Code card at left (not_too_far, near_line and their product); at right a real Godot window with one tall thin teal rectangle in the middle "
    "(0.06 wide, 0.7 tall). One ring settles on it; readout 'both are 1' beside it.",
    "The highlight moves to the product line and the ring settles on the rectangle.",
    [ev0(T("B25", "not too far along the line"), "not too far along the line"), ev0(T("B25", "and close to it"), "close to it"),
     ev0(T("B25", "Two masks", prefer="late"), "the product"), ev0(T("B25", "Both must be one"), "ring on the rectangle; readout both are 1")],
    "manim: two masks multiplying",
    "A real rectangle appearing where two thin conditions overlap is the claim: both must be one.",
    "C13: lab-shaders/12-arm-rectangle.gdshader, still on a square canvas, Forward+ (probes: middle and (0.5, 0.25) teal; (0.5, 0.1) and (0.6, 0.5) stage).",
    "Lab: 0 of 230,400 pixels differ from the model (coverage 0.0408)",
    readouts=[{"at": T("B25", "Both must be one"), "text": "both are 1", "x": 0.72, "y": 0.5}], rings=[{"at": T("B25", "Both must be one"), "box": [0.45, 0.13, 0.55, 0.87]}])

_g = code_of("13-arms-gap.gdshader")
_n1 = T("B26", "not too far", prefer="late")
_n2 = after(_n1, T("B26", "near the line"))
lab("B26", 2, "a gap: a third condition, and one formula for both sides", "13-arms-gap.gdshader", PUB + "arms-gap.png", FWD,
    [cue(T("B26", "Add a third condition"), _g, "float far_enough"), cue(T("B26", "Far enough"), _g, "float far_enough"),
     cue(_n1, _g, "float not_too_far"), cue(_n2, _g, "float near_line"), rng(after(_n2, T("B26", "Because of abs")), 4, 5)],
    "Code card at left (far_enough, not_too_far, near_line and their product); at right a real Godot window with two short thin vertical teal bars, above and "
    "below the middle, and an empty gap between them. One ring marks the gap (readout 'gap'), then one ring on the top arm and one on the bottom arm.",
    "Each condition lights in turn, the ring settles on the gap, then the same formula is ringed on both arms.",
    [ev0(T("B26", "Add a third condition"), "far_enough: at least this far out"), ev0(T("B26", "at least this far out"), "ring on the gap; readout gap"),
     ev0(T("B26", "Far enough"), "far enough"), ev0(_n1, "not too far"), ev0(_n2, "near the line"),
     ev0(after(_n2, T("B26", "Because of abs")), "the two abs lines"), ev0(T("B26", "one formula draws"), "ring on the top arm"), ev0(T("B26", "and the bottom"), "ring on the bottom arm")],
    "manim: the three conditions on a number line",
    "Real arms with a real gap show that one formula draws both sides.",
    "C14: lab-shaders/13-arms-gap.gdshader, still on a square canvas, Forward+ (probes: (0.5, 0.3) and (0.5, 0.7) teal; the middle, (0.5, 0.95), "
    "(0.3, 0.5) stage).",
    "Lab: 0 of 230,400 pixels differ from the model (coverage 0.0292)",
    readouts=[{"at": T("B26", "at least this far out"), "text": "gap", "x": 0.5, "y": 0.5}],
    rings=[{"at": T("B26", "at least this far out"), "box": [0.42, 0.41, 0.58, 0.59]}, {"at": T("B26", "one formula draws"), "box": [0.43, 0.13, 0.57, 0.42]},
           {"at": T("B26", "and the bottom"), "box": [0.43, 0.58, 0.57, 0.87]}])

_q = code_of("14-four-arms.gdshader")
lab("B27", 2, "four arms from two lines and a max; measure, compare, combine", "14-four-arms.gdshader", PUB + "four-arms.png", FWD,
    [cue(T("B27", "Swap the two addresses"), _q, "float v"), cue(T("B27", "for the horizontal pair"), _q, "float h"), cue(T("B27", "then take the max"), _q, "float mask")],
    "Code card at left (the vertical pair v, the horizontal pair h, and the max that joins them); at right a real Godot window with four short "
    "teal arms around an empty middle. Under the window: 'measure, compare, combine'.",
    "The vertical pair, then the horizontal pair, then the max that joins them, each highlighted as it is named.",
    [ev0(T("B27", "Swap the two addresses"), "the vertical pair (v)"), ev0(T("B27", "for the horizontal pair"), "swap the two addresses: the horizontal pair (h)"), ev0(T("B27", "then take the max"), "the max"),
     ev0(T("B27", "Measure"), "label measure, compare, combine")],
    "manim: the arms assembled from two pairs",
    "Four real arms from two lines of code; the closing phrase of the act sits under the picture.",
    "C15: lab-shaders/14-four-arms.gdshader, still on a square canvas, Forward+ (probes: four arms teal at (0.3, 0.5), (0.7, 0.5), (0.5, 0.3), "
    "(0.5, 0.7); middle and (0.3, 0.3) stage).",
    "Lab: 0 of 230,400 pixels differ from the model (coverage 0.0583)",
    readouts=[{"at": T("B27", "Measure"), "text": "measure, compare, combine", "x": 0.5, "y": 0.95}])

# ═════════════════════════════ ACT IV · Make It a Tool ═════════════════════════════
manim("B28", 3, "every baked-in number becomes a uniform: a dial", "NumbersBecomeDials",
      "Act title 'Make It a Tool' (serif 40) top-left. At left, the vertical-pair line set as three STACKED calls in monospace on a cream card (the whole line is "
      "55 characters and does not fit beside a panel at size 32): `step(0.1, y) *`, `step(y, 0.35) *`, `step(x, 0.03)`. At right, an empty panel with three labelled "
      "slots 'gap', 'end', 'width'. As each number is named it lifts out of its call and lands in its slot as a slider knob on a short track, leaving the "
      "name in its place: the calls then read `step(gap, y) *`, `step(y, end) *`, `step(x, width)`. The sliders get end labels '0' and '1' (a range) and the tag 'uniform'; "
      "the panel is labelled 'in the editor'.",
      "Each baked-in number lifts out of its call and lands as a slider, leaving its name behind.",
      [ev0(0.03, "act title; the three stacked calls and the empty panel"), ev("B28", "the gap", "0.1 becomes the gap slider"), ev("B28", "the end", "0.35 becomes the end slider"),
       ev("B28", "the width", "0.03 becomes the width slider"), ev("B28", "A tool needs dials", "label 'dials' above the panel"),
       ev("B28", "Turn each number into a uniform with a range", "each slider gets end labels 0 and 1 and the tag 'uniform'", lead=0.0),
       ev("B28", "and the editor gives you a slider", "the panel is labelled 'in the editor'")],
      "LectureCodeTrace",
      "A number leaving the code and becoming a dial is the idea of a uniform; a code card alone would not move.")

manim("B29", 3, "make every dial run from zero to one; scale inside the shader", "ZeroToOneDials",
      "Left, under 'three scales': sliders 'radius 0 to 0.5', 'width 0 to 0.05' and 'gap 0 to 0.2', each with different tick labels. They "
      "morph into three identical 0 to 1 sliders with the same ticks; to the right of each a multiplier tag ('× 0.5', '× 0.05', '× 0.2') and a "
      "small teal shape showing the real size at slider = 1. At the end the three knobs travel from 0 to 1 together.",
      "Three differently scaled sliders turn into three identical zero-to-one sliders with the real size beside each, and the knobs move as one.",
      [ev0(0.03, "three sliders, three different scales"), ev("B29", "every slider runs from zero to one", "they morph into identical 0 to 1 sliders"),
       ev("B29", "multiply by the biggest value", "the three multiplier tags pop in"),
       ev("B29", "Then every dial behaves", "the real sizes appear beside each slider"), ev("B29", "and you never memorize", "the three knobs travel from 0 to 1 together")],
      "ShaderLab with the scaled crosshair",
      "'Every dial has the same range' is a picture of sameness; one frame of three identical sliders says it.")

_t = code_of("15-ring-tool.gdshader")
lab("B30", 3, "a function that returns a mask", "15-ring-tool.gdshader", PUB + "ring-tool.png", FWD,
    [cue(T("B30", "A function can return a mask"), _t, "float make_ring", "function: a named block of code you can call"),
     cue(T("B30", "This one takes an address"), _t, "float make_ring"), cue(T("B30", "and returns the ring"), _t, ["float d", "return step"]),
     cue(T("B30", "The fragment function only calls it"), _t, "make_ring(UV")],
    "Code card at left (make_ring and the fragment function that calls it); at right a real Godot window with the teal ring. The function's first "
    "line carries the definition of the word 'function'; the signature, the body and the call line are highlighted in turn; one ring marks the top of the band at the call.",
    "The highlight moves from the function's name to its inputs, its body and the call that uses it.",
    [ev0(T("B30", "A function can return a mask"), "make_ring: a function (defined)"), ev0(T("B30", "This one takes an address"), "its three inputs"),
     ev0(T("B30", "and returns the ring"), "its body returns the mask"), ev0(T("B30", "The fragment function only calls it"), "the call in the fragment function; ring on the band")],
    "LectureCodeTrace alone",
    "The function and the ring it returns, side by side; the picture proves the function draws the same ring as the inline version.",
    "C16: lab-shaders/15-ring-tool.gdshader, still on a square canvas, Forward+ (probes: middle stage; (0.5, 0.18) teal).",
    "Lab: 0 of 230,400 pixels differ from the model; identical pixels to 04-ring (same radii)",
    rings=[{"at": T("B30", "The fragment function only calls it"), "box": [0.4, 0.12, 0.6, 0.23]}])

manim("B31", 3, "built-ins like UV are not visible inside your own function", "WhoCanSeeUV",
      "A large box labelled 'fragment()' holding three values in monospace: UV, COLOR, TIME. To its right a smaller box labelled 'make_ring()' inside "
      "a thick wall. A caption in the glossary's wording, set as two lines beside the first box and never on a fill ('built-in: a value the engine hands' / 'to a function, or collects from it'). UV tries to travel into the second box and bounces "
      "off the wall; TIME slips through, tagged 'global: works anywhere'; then a small teal packet (its label 'uv', the input's own name, set beside it on a leader line) travels "
      "from fragment() through an input slot in the wall into make_ring().",
      "UV bounces off the wall of the second function, TIME slips through, and a packet named uv carries the address in through the input slot.",
      [ev("B31", "Built-in values like", "the two boxes and the caption"), ev("B31", "but not in yours", "UV bounces off the wall", lead=0.06),
       ev("B31", "are global and work anywhere", "TIME slips through, tagged global", lead=0.0), ev("B31", "So fragment hands", "the uv packet enters through the slot")],
      "LectureCodeTrace",
      "Visibility is a wall around a box; seeing UV bounce, TIME pass and an input carry the address through is the rule.")

_e = code_of("16-uv-inside-function-FAILS.gdshader")
rem("B32", 3, "the compile error when UV is used inside your own function", "LectureCodeTrace",
    {"title": "Using UV inside your own function", "code": _e,
     "note": "Godot 4.7.2 · line 3: Unknown identifier in expression: 'UV'.",
     "cues": [0.04, 0.04, 0.04, T("B32", "The version from a moment ago"), T("B32", "The version from a moment ago"),
              T("B32", "The version from a moment ago"), T("B32", "The version from a moment ago"), 1.5], "durationSeconds": "__AUDIO__"},
    "A cream code card with the eight real lines of the failing shader (UV used directly inside make_ring); focus lands on line 3, the line the engine "
    "names, and the engine's own message sits under the card.",
    "Focus lands on the line Godot names and stays there, then jumps to the call that passes nothing in.",
    [ev0(0.04, "line 3 focused: UV inside the function"), ev0(T("B32", "The version from a moment ago"), "focus on the call that passes nothing in")],
    "CCPlainShell with the engine's log",
    "The failing line in the real code with the engine's own message under it shows 'refuses to compile' without a dark terminal on screen.",
    "Lab and verify-b.gd: the engine prints 'SHADER ERROR: Unknown identifier in expression: 'UV'.' at line 3 (run-b2-verify-b-final-failing-file.log; the eight-line "
    "file is lab-shaders/16-uv-inside-function-FAILS.gdshader, kept as a failing file on purpose)")

manim("B33", 3, "the honest limit: shapes assume a square", "SquareLimit",
      "Left: a square with a teal circle inside it. Right: the same shape stretched into a 16:9 rectangle; the circle stretches into an oval with it. "
      "Corner labels (0, 0) and (1, 1) stay at the same corners on both. A label 'oval' lands beside the stretched circle. Credit, small and grey, set as two lines: "
      "'Godot 4.7.2 · Forward+ · 640 × 360 view' / 'measured 384 × 216 px'.",
      "The square stretches wide and the circle stretches into an oval with it.",
      [ev("B33", "these shapes assume a square", "the square and its circle"), ev("B33", "On a wide rectangle", "the stretch to a wide rectangle; the circle becomes an oval; the corner labels stay"),
       ev("B33", "so a circle becomes an oval", "label 'oval'", lead=0.0), ev("B33", "We measured it", "credit line with the measured numbers")],
      "ShaderLab with a capture of the oval",
      "A stretch is a motion and the circle going oval with it is the claim; the measured numbers sit in the credit line.")

manim("B34", 3, "the edge is hard: every pixel is in or out", "Staircase",
      "A zoomed pixel grid (14 columns by 9 rows) showing a quarter of a circle's edge, a small dot at the CENTRE of every cell. A cell is teal when its centre dot "
      "lies inside the ideal circle and empty when it lies outside (the pixel's centre decides, as in the shader). A smooth terracotta arc, the ideal circle, is drawn over the "
      "grid and the cells step along it like a staircase; a cell that the arc cuts through is teal or empty by its centre alone. Caption 'in or out · nothing between'. "
      "Credit, small and grey, set as two lines: 'Godot 4.7.2 · Forward+ · 480 × 480 render' / 'the whole picture has 2 colors'.",
      "The cells fill in or out by their centres, then the ideal arc draws over them and the cells step along it like a staircase.",
      [ev0(0.02, "the zoomed grid with a centre dot in each cell"), ev("B34", "Every pixel is fully in", "the cells fill in or out by their centre dots; caption"),
       ev("B34", "so the circle's edge", "the ideal arc draws over them"), ev("B34", "The whole picture has exactly", "credit: the whole render has 2 colors")],
      "ShaderLab with a crop of the real render",
      "A cell-level zoom with the ideal arc over it shows exactly why the edge steps; the credit carries the measurement.")

# ═════════════════════════════ ACT V · The Crosshair ═════════════════════════════
_u = slice_of(CROSS, 1, 8)
lab("B35", 4, "six uniforms, each from zero to one", None, PUB + "crosshair-defaults.png", FWD,
    [cue(T("B35", "dot size"), _u, "dot_size"), cue(T("B35", "ring distance"), _u, "ring_distance"), cue(T("B35", "ring width"), _u, "ring_width"),
     cue(T("B35", "arm gap"), _u, "arm_gap"), cue(T("B35", "arm length and arm width", lead=0.02), _u, "arm_length"),
     cue(T("B35", "and arm width", prefer="late"), _u, "arm_width"), rng(T("B35", "Each runs from zero to one", lead=-0.02), 3, 8, "hint_range(0, 1): a slider from 0 to 1")],
    "Act title 'The Crosshair' (serif 40) top-left. Code card at left (the shader type line and the six uniform lines, lines 1 to 8 of the file; "
    "each uniform highlighted as its name is spoken; then all six with a label on the range); at right a real Godot window with the finished crosshair at its defaults.",
    "The highlight walks down the six uniform lines while the finished crosshair sits at its defaults.",
    [ev0(T("B35", "dot size"), "dot_size"), ev0(T("B35", "ring distance"), "ring_distance"), ev0(T("B35", "ring width"), "ring_width"), ev0(T("B35", "arm gap"), "arm_gap"),
     ev0(T("B35", "arm length and arm width", lead=0.02), "arm_length"), ev0(T("B35", "and arm width", prefer="late"), "arm_width"),
     ev0(T("B35", "Each runs from zero to one", lead=-0.02), "all six: the range label")],
    "LectureCodeTrace alone",
    "The six dials listed beside the crosshair they control; the card shows lines 1 to 8 of the real file.",
    "C17: lab-shaders/17-crosshair.gdshader, still on a square canvas, Forward+, defaults (probes: middle and (0.35, 0.5) teal; (0.5, 0.2) stage). "
    "Also used by B38.",
    "Lab: defaults match the model, 0 of 230,400 pixels differ (coverage 0.0398); uniform list: six floats with RANGE hints 0.0 to 1.0 (verify-c.gd)",
    title="The Crosshair", code=_u, code_file="lab-shaders/17-crosshair.gdshader · lines 1 to 8")

_dr = slice_of(CROSS, 10, 17)
lab("B36", 4, "the dot and the ring as functions", None, PUB + "crosshair-dot-ring.png", "Godot 4.7.2 · Forward+ · arm length set to 0",
    [rng(T("B36", "the dot is the circle"), 1, 3), rng(T("B36", "and the ring is the outer circle", prefer="late"), 5, 8)],
    "Code card at left (make_dot and make_ring, lines 10 to 17 of the file); at right a real Godot window with the crosshair's dot and ring only "
    "(arm length dialled to 0, labelled). One ring lands on the dot when make_dot is highlighted, then on the ring top when make_ring is.",
    "The ring marker lands on the dot, then on the ring, as each function is highlighted.",
    [ev0(T("B36", "the dot is the circle"), "make_dot highlighted; ring on the dot"), ev0(T("B36", "and the ring is the outer circle", prefer="late"), "make_ring highlighted; ring on the ring")],
    "LectureCodeTrace alone",
    "Each function beside the piece of the picture it makes.",
    "C18: lab-shaders/17-crosshair.gdshader, still on a square canvas, Forward+, arm_length = 0 (probes: the dot and the ring drawn, no arms).",
    "Lab: arm_length = 0 leaves the dot and the ring (coverage 0.0234), matches the model on every pixel",
    code=_dr, code_file="lab-shaders/17-crosshair.gdshader · lines 10 to 17", readouts=[ro(0.1, "arms off")],
    rings=[{"at": T("B36", "the dot is the circle"), "box": [0.45, 0.45, 0.55, 0.55]},
           {"at": T("B36", "and the ring is the outer circle", prefer="late"), "box": [0.42, 0.24, 0.58, 0.31]}])

_ar = slice_of(CROSS, 19, 26)
lab("B37", 4, "the arms as a function", None, PUB + "crosshair-arms.png", "Godot 4.7.2 · Forward+ · dot size 0 and ring width 0",
    [rng(0.02, 5, 6), rng(T("B37", "Gap"), 1, 1), rng(T("B37", "gap plus length"), 4, 4), rng(T("B37", "abs folds each side", prefer="late"), 2, 3), rng(T("B37", "max joins"), 7, 7)],
    "Code card at left (make_arms, lines 19 to 26 of the file); at right a real Godot window with the four arms alone (dot size and ring width "
    "dialled to 0, labelled). The vertical and horizontal pair lines, the signature, the end line (gap plus length), the two abs lines and the final max are highlighted in turn.",
    "The highlight moves from the two pair lines to the function's inputs to the folding lines to the max that joins the pairs.",
    [ev0(0.02, "the vertical and horizontal pairs: the rule from before"), ev0(T("B37", "Gap"), "gap, length and width come in"),
     ev0(T("B37", "gap plus length"), "gap plus length is the end"), ev0(T("B37", "abs folds each side", prefer="late"), "abs folds each side"), ev0(T("B37", "max joins"), "max joins the two pairs")],
    "LectureCodeTrace alone",
    "The arms function beside the arms it draws; the dials set to 0 are labelled so nothing is hidden.",
    "C19: lab-shaders/17-crosshair.gdshader, still on a square canvas, Forward+, dot_size = 0 and ring_width = 0 (probes: four arms drawn; the dot gone).",
    "Lab: dot_size = 0 and ring_width = 0 leave the four arms alone (crosshair-arms-only: coverage 0.0179), matching the model on every pixel",
    code=_ar, code_file="lab-shaders/17-crosshair.gdshader · lines 19 to 26", readouts=[ro(0.1, "arms alone")])

_fr = slice_of(CROSS, 28, 39)
lab("B38", 4, "the fragment function: scale, combine with max", None, PUB + "crosshair-defaults.png", FWD,
    [rng(0.02, 2, 7), rng(T("B38", "then joins the three masks"), 8, 10), rng(T("B38", "The mask goes straight"), 11, 11)],
    "Code card at left (the fragment function, lines 28 to 39 of the file); at right a real Godot window with the finished crosshair at its defaults. "
    "The six scaling lines, the three mask lines and the color line are highlighted in turn; where an arm crosses the ring, one ring and the readout 'still 1' land.",
    "The highlight moves from the six scaling lines to the three max lines, a ring lands where an arm crosses the ring, then the color line lights.",
    [ev0(0.02, "each slider scaled to a real size"), ev0(T("B38", "then joins the three masks"), "the three masks joined with max"),
     ev0(T("B38", "Where the ring and arms cross", prefer="late"), "ring where the arm crosses the ring; readout still 1"),
     ev0(T("B38", "The mask goes straight"), "the mask goes into the alpha")],
    "LectureCodeTrace alone",
    "The assembly beside the assembled crosshair: the whole film's idea in twelve lines.",
    "C17 again (the same defaults still, no new capture).",
    "Lab: defaults match the model; extremes (all dials 0 draw nothing, all dials 1 coverage 0.1998) match too",
    code=_fr, code_file="lab-shaders/17-crosshair.gdshader · lines 28 to 39",
    readouts=[ro(T("B38", "Where the ring and arms cross", prefer="late"), "still 1")],
    rings=[{"at": T("B38", "Where the ring and arms cross", prefer="late"), "box": [0.68, 0.45, 0.78, 0.55]}])

lab("B39", 4, "outside the mask, whatever is behind shows through", None, PUB + "crosshair-backdrops.png",
    "Godot 4.7.2 · Forward+ · two flat backdrops behind the crosshair", [],
    "A real Godot window: the finished crosshair over two flat backdrops, cream on the left half and sand on the right half. One ring marks a "
    "see-through patch on the left (readout 'mask = 0' at the top-left), then one on the right (readout 'see-through' at the top-right).",
    "The ring lands on a patch of each backdrop showing through, one after the other.",
    [ev0(T("B39", "Wherever the mask is zero"), "readout mask = 0; ring on a left patch"), ev0(T("B39", "so whatever is behind", prefer="late"), "ring on a right patch; readout see-through")],
    "manim: a layer diagram",
    "The real thing over two real backdrops is the proof that zero means see-through.",
    "C20: a **scene script** (`--scene`, as the harness spec describes) builds two ColorRect backdrops (left half #FAF9F5, right half #C9B79C) and the "
    "crosshair ColorRect on top at the defaults; still, Forward+. Copy the structure of evidence/planning-checks/verify-a.gd, check 2: a pixel outside "
    "the shape reads exactly the backdrop color on each side.",
    "verify-a.gd 2-overlay: (60, 60) reads 0.9804, 0.9765, 0.9608 (cream); (420, 60) reads 0.7882, 0.7176, 0.6118 (sand); the shape pixels read teal",
    layout="video", readouts=[ro(T("B39", "Wherever the mask is zero"), "mask = 0"), ro(T("B39", "so whatever is behind", prefer="late"), "see-through", (0.8, 0.06))],
    rings=[{"at": T("B39", "Wherever the mask is zero"), "box": [0.05, 0.16, 0.28, 0.39]}, {"at": T("B39", "so whatever is behind", prefer="late"), "box": [0.72, 0.16, 0.95, 0.39]}])

_dials = slice_of(CROSS, 1, 8)
_a1, _a2 = dial_pair("B40", dict(name="dot_size", default=0.5, rise_phrase="Dot size grows the dot"),
                     dict(name="ring_distance", default=0.55, rise_phrase="Ring distance pushes the ring"))
SWEEPS["C21"] = [_a1, _a2]
lab("B40", 4, "the dials, one at a time: dot size and ring distance", None, PUB + "sweep-dot-ring.mp4", "Godot 4.7.2 · Forward+ · dials moved by a script",
    [cue(_a1["cue"], _dials, "dot_size"), cue(_a2["cue"], _dials, "ring_distance")],
    "Code card at left (lines 1 to 8: the six uniforms; the one being moved is highlighted); at right a real Godot window: dot size drops to 0 and grows to 1, "
    "then ring distance drops to 0 and grows to 1 while the arms stay put. A readout names the dial and its value at each hold, at the top-left of the window.",
    "The dot grows from nothing; then the ring moves out from the middle while the arms stay put.",
    [ev0(_a1["cue"], "dot_size line; the dot shrinks to nothing"), ev0(_a1["t_low"], "readout dot size 0"), ev0(_a1["rise"][0], "the dot grows"),
     ev0(_a1["t_high"], "readout dot size 1"), ev0(_a2["cue"], "ring_distance line; the ring collapses"), ev0(_a2["t_low"], "readout ring distance 0"),
     ev0(_a2["rise"][0], "the ring moves out while the arms stay put"), ev0(_a2["t_high"], "readout ring distance 1")],
    "manim: a dial icon driving a drawn crosshair",
    "Real sweeps show each dial changing exactly one thing, which is the point of the act.",
    "C21: 17-crosshair at defaults, 30 fps, `--length` = the measured audio of B40 (about 10.5 s). Two dials back to back, each from 0 to 1 and ending on 1 (the voice says "
    "'grows' and 'pushes the ring outward'); the first dial stays at 1.0 while the second moves. " + sweep_text(_a1) + "; then " + sweep_text(_a2) +
    ". The 50 % frame is inside ring_distance's hold at 0 (with dot_size at 1.0) and the 85 % frame in the final hold (both at 1.0). Scripted. Harness: `" +
    animate_arg(_a1) + "` and `" + animate_arg(_a2) + "`.",
    "Lab: dot_size and ring_distance at 0 and at 1 match the model on every pixel (coverage 0.0379/0.0457 and 0.0199/0.0582); the two held pairs (dot_size 1 with ring_distance 0, and both at 1) are `pair-dot1-ring0` and `pair-dot1-ring1`",
    code=_dials, code_file="lab-shaders/17-crosshair.gdshader · lines 1 to 8",
    readouts=[ro(_a1["t_low"], "dot size 0"), ro(_a1["t_high"], "dot size 1"), ro(_a2["t_low"], "ring distance 0"), ro(_a2["t_high"], "ring distance 1")])

_b1, _b2 = dial_pair("B41", dict(name="ring_width", default=0.3, rise_phrase="Ring width thickens the ring", hold_min=0.04),
                     dict(name="arm_length", default=0.6, rise_phrase="Arm length stretches the arms"))
SWEEPS["C22"] = [_b1, _b2]
_cross_at = round(_b2["rise"][0] + 0.5 * (_b2["rise"][1] - _b2["rise"][0]) * 1.0, 2)
lab("B41", 4, "ring width and arm length", None, PUB + "sweep-width-length.mp4", "Godot 4.7.2 · Forward+ · dials moved by a script",
    [cue(_b1["cue"], _dials, "ring_width"), cue(_b2["cue"], _dials, "arm_length")],
    "Code card at left (lines 1 to 8; the dial being moved is highlighted); at right a real Godot window: ring width drops to nothing and grows to a thick "
    "band, then arm length drops to 0 and stretches the arms until they cross the ring and run on past it, ending on 1 (the ring stays thick). Readouts name the dial and value at each hold.",
    "The ring thickens from nothing to a band; the arms lengthen across the ring and the picture ends with nothing doubled where they cross.",
    [ev0(_b1["cue"], "ring_width line; the ring thins to nothing"), ev0(_b1["t_low"], "readout ring width 0"), ev0(_b1["rise"][0], "the ring thickens to a band"),
     ev0(_b1["t_high"], "readout ring width 1"), ev0(_b2["cue"], "arm_length line; the arms retract"), ev0(_b2["t_low"], "readout arm length 0"),
     ev0(_b2["rise"][0], f"the arms stretch; they cross the ring near {pct(_cross_at)}"), ev0(_b2["t_high"], "readout arm length 1")],
    "manim: a dial icon driving a drawn crosshair",
    "Real sweeps; where the arms cross the ring nothing doubles, which is visible only in a real render.",
    "C22: 17-crosshair at defaults, 30 fps, `--length` = the measured audio of B41 (about 9.5 s), the same shape as C21 (the first dial stays at 1.0 while the second moves). " +
    sweep_text(_b1) + "; then " + sweep_text(_b2) + f". The arms cross the ring at about 0.5 on the dial, near {pct(_cross_at)} of the beat; the voice says 'Nothing doubles where they cross' over the final hold. "
    "The 50 % frame is inside arm_length's hold at 0 (with ring_width at 1.0) and the 85 % frame in the final hold (both at 1.0). Scripted. Harness: `" +
    animate_arg(_b1) + "` and `" + animate_arg(_b2) + "`.",
    "Lab: ring_width and arm_length at 0 and at 1 match the model on every pixel (coverage 0.0199/0.0939 and 0.0234/0.0519); the two held pairs are `pair-rw1-al0` and `pair-rw1-al1`",
    code=_dials, code_file="lab-shaders/17-crosshair.gdshader · lines 1 to 8",
    readouts=[ro(_b1["t_low"], "ring width 0"), ro(_b1["t_high"], "ring width 1"), ro(_b2["t_low"], "arm length 0"), ro(_b2["t_high"], "arm length 1")])

_c1, _c2 = dial_pair("B42", dict(name="arm_width", default=0.4, rise_phrase="Arm width thickens the arms", drop_d=0.04, hold0=0.04, rise_d=0.12, hold_min=0.04),
                     dict(name="arm_gap", default=0.35, rise_phrase="to arms that start far from it", drop_phrase="from arms that run into the dot", rise_d=0.14))
SWEEPS["C23"] = [_c1, _c2]
lab("B42", 4, "arm width and arm gap", None, PUB + "sweep-armwidth-gap.mp4", "Godot 4.7.2 · Forward+ · dials moved by a script",
    [cue(_c1["cue"], _dials, "arm_width"), cue(_c2["cue"], _dials, "arm_gap")],
    "Code card at left (lines 1 to 8; the dial being moved is highlighted); at right a real Godot window: arm width drops to 0 and thickens the arms to 1, "
    "then arm gap drops to 0 (arms that run into the dot) and opens the middle to 1 (arms that start far from it). Readouts name the dial and value.",
    "The arms thicken from nothing; then they slide away from the middle, opening a gap.",
    [ev0(_c1["cue"], "arm_width line; the arms thin to nothing"), ev0(_c1["t_low"], "readout arm width 0"), ev0(_c1["rise"][0], "the arms thicken"),
     ev0(_c1["t_high"], "readout arm width 1"), ev0(_c2["cue"], "arm_gap line; the arms slide into the dot"), ev0(_c2["t_low"], "readout arm gap 0: the arms run into the dot"),
     ev0(_c2["rise"][0], "the middle opens"), ev0(_c2["t_high"], "readout arm gap 1")],
    "manim: a dial icon driving a drawn crosshair",
    "Real sweeps again; the last pair of dials, so the viewer has seen all six move.",
    "C23: 17-crosshair at defaults, 30 fps, `--length` = the measured audio of B42 (about 8 s), the same shape as C21 (the first dial stays at 1.0 while the second moves). " +
    sweep_text(_c1) + "; then " + sweep_text(_c2) + ". The voice says 'arms that run into the dot' over the hold at 0 and 'arms that start far from it' as the gap opens. "
    "The 50 % frame is inside arm_gap's hold at 0 (with arm_width at 1.0) and the 85 % frame in the final hold (both at 1.0). Scripted. Harness: `" +
    animate_arg(_c1) + "` and `" + animate_arg(_c2) + "`.",
    "Lab: arm_width and arm_gap at 0 and at 1 match the model on every pixel (coverage 0.0234/0.0617 and 0.0389/0.0398); the two held pairs are `pair-aw1-ag0` and `pair-aw1-ag1`",
    code=_dials, code_file="lab-shaders/17-crosshair.gdshader · lines 1 to 8",
    readouts=[ro(_c1["t_low"], "arm width 0"), ro(_c1["t_high"], "arm width 1"), ro(_c2["t_low"], "arm gap 0"), ro(_c2["t_high"], "arm gap 1")])

# C24 is stepped: the state changes are instant, so only the readouts keep out of 45 to 55 %
_t1 = round(start_of("B43", "The dot and the ring") - 0.01, 2)      # arm_length = 0
_t2 = round(start_of("B43", "Ring width at zero") - 0.01, 2)        # back to the defaults, while the next question is asked
_t3 = round(start_of("B43", "The dot and the arms") - 0.01, 2)      # ring_width = 0
_t4 = round(start_of("B43", "Push any dial to either end") - 0.01, 2)   # all six = 1
assert 0.02 < _t1 < _t2 < _t3 < _t4 < 0.9, (_t1, _t2, _t3, _t4)
_steps = {"dot_size": [(0, 0.5), (_t4, 1)], "ring_distance": [(0, 0.55), (_t4, 1)], "ring_width": [(0, 0.3), (_t3, 0), (_t4, 1)],
          "arm_gap": [(0, 0.35), (_t4, 1)], "arm_length": [(0, 0.6), (_t1, 0), (_t2, 0.6), (_t4, 1)], "arm_width": [(0, 0.4), (_t4, 1)]}
SWEEPS["C24"] = _steps
_steps_arg = " ".join(f"--steps {n}:" + ",".join(f"{t:g}:{v:g}" for t, v in kv) for n, kv in _steps.items())
lab("B43", 4, "predict, then reveal: dials at their ends, and nothing breaks", None, PUB + "extremes.mp4",
    "Godot 4.7.2 · Forward+ · values set by a script", [],
    "A real Godot window, result only. The crosshair at its defaults ('predict first'); the readout 'arm length 0?' asks, then the state jumps to arm length 0 "
    "(dot and ring) as the answer is voiced; the picture goes back to the defaults while 'ring width 0?' asks, then jumps to ring width 0 (dot and arms) as that answer is voiced; "
    "then every dial at 1 (everything at its largest). Readouts sit at the top-left of the window and name each state.",
    "The crosshair jumps between states and the readout names each one, so the viewer can check the prediction.",
    [ev0(0.02, "defaults; readout predict first"), ev0(T("B43", "Arm length at zero"), "readout arm length 0? (the question)"),
     ev0(_t1, "arm length 0: dot and ring remain"), ev0(nudge(_t1 + 0.01), "readout arm length 0"), ev0(_t2, "back to the defaults"),
     ev0(T("B43", "Ring width at zero"), "readout ring width 0? (the question)"), ev0(_t3, "ring width 0: dot and arms remain (the change lands as the answer is voiced)"),
     ev0(nudge(_t3 + 0.01), "readout ring width 0"), ev0(_t4, "every dial 1: everything at its largest"), ev0(nudge(_t4 + 0.01), "readout every dial 1")],
    "manim: four small crosshairs in a row",
    "Predict-then-reveal needs the real states one after another; the stepped capture is the reveal.",
    "C24: 17-crosshair, 30 fps, `--length` = the measured audio of B43 (about 13 s), STEPPED (`--steps`: instant changes, no ramps), as fractions of the clip: "
    f"defaults to {pct(_t1)}; arm_length = 0 from {pct(_t1)} to {pct(_t2)} (the voice says 'The dot and the ring'); the defaults again from {pct(_t2)} to {pct(_t3)} while 'Ring width at zero?' is asked "
    f"(the 50 % frame is a settled state); ring_width = 0 from {pct(_t3)} to {pct(_t4)} ('The dot and the arms'); all six dials = 1.0 from {pct(_t4)} to the end (the 85 % frame). "
    "Scripted. Harness: `" + _steps_arg + "`.",
    "Lab: arm_length = 0 leaves dot and ring; ring_width = 0 leaves dot and arms; all dials 0 draw nothing (coverage 0.0000); all dials 1 coverage 0.1998",
    layout="video", readouts=[ro(0.02, "predict first"), ro(T("B43", "Arm length at zero"), "arm length 0?"), ro(nudge(_t1 + 0.01), "arm length 0"),
                              ro(T("B43", "Ring width at zero"), "ring width 0?"), ro(nudge(_t3 + 0.01), "ring width 0"), ro(nudge(_t4 + 0.01), "every dial 1")])

# E1: three states, two cross-dissolves placed from the words; the rings are in the crop's own coordinates (placeholders: derive them from the real crop)
_e1 = round(avoid(min(start_of("B44", "A designer can tune") - 0.01, END_BY - 0.22), 0.06), 2)
_e2 = round(avoid(_e1 + 0.16, 0.06), 2)
SWEEPS["E1"] = [("dissolve to dot_size 1.0", _e1, _e1 + 0.06), ("dissolve to ring_distance 0.2", _e2, _e2 + 0.06)]
lab("B44", 4, "the six uniforms as six sliders in the real Inspector", None, PUB + "editor-inspector.mp4",
    "Godot 4.7.2 editor · three real frames", [],
    "Three real frames of the Godot editor's Inspector, cropped to the ShaderMaterial's 'Shader Parameters' group (no thumbnail, no viewport): the six uniforms as six "
    "sliders at their defaults; then dot size at 1.0; then ring distance at 0.2 (dot size stays 1.0). Slow cross-dissolves between the frames; one terracotta ring on the group, "
    "then on the slider being named.",
    "The slider knobs step through three real states.",
    [ev0(T("B44", "the six uniforms"), "six sliders at their defaults; ring on the group"),
     ev0(_e1, f"dissolve ({pct(_e1)} to {pct(_e1 + 0.06)}) to dot size at 1.0"), ev0(nudge(_e1 + 0.07), "ring on the dot size slider"),
     ev0(_e2, f"dissolve ({pct(_e2)} to {pct(_e2 + 0.06)}) to ring distance at 0.2"), ev0(nudge(_e2 + 0.07), "ring on the ring distance slider")],
    "GodotDevWorkbench (labelled reconstruction)",
    "Real editor frames are the rung-1 SHOW-THE-THING answer; the reconstruction is the labelled fallback.",
    "E1: three static editor frames of a scratch project via Movie Maker (method proven 2026-10-09; driver for this exact view proven 2026-10-13 in evidence/planning-checks/editor-driver/): ColorRect 480 x 480 with a ShaderMaterial on "
    "lab-shaders/17-crosshair.gdshader, the values saved in the scene file (state 1: defaults; state 2: dot_size 1.0; state 3: dot_size 1.0 and ring_distance 0.2, as in the proven frame); Inspector scrolled to the "
    "material's six uniforms, then CROPPED to the 'Shader Parameters' group. The clicks themselves are not shown, only the resulting states. Output `editor-inspector.mp4`: the three stills "
    f"joined by two 0.4 s cross-dissolves (for example ffmpeg `xfade`), the first from {pct(_e1)} and the second from {pct(_e2)} of the beat. At the default dock width the label 'Ring Distance' loses its last letter "
    "(see `png/editor-inspector-check-2d.png`): widen the Inspector dock by hand in the scratch project's layout (editor-driver/README.md) or crop so the cut label is not the one being named. "
    "Recording the editor at 3840 by 2160 is a recommendation for a sharp crop, not something the planning check did (it ran at 1920 by 1080).",
    "Docs: uniforms 'will appear as editable parameters in the material's inspector'; EditorSpinSlider: 'If the Range.step value is not 1, a slider will be "
    "displayed instead' (the uniforms' step is 0.001, verify-c.gd). The real Inspector was observed in a planning-check frame (evidence/planning-checks/png/editor-inspector-check-2d.png, driver in editor-driver/); capture E1 re-records it cleanly for the film",
    layout="video", lane="editor", code_file="lab-shaders/17-crosshair.gdshader", sparse=False,
    caption="Inspector: the editor panel that lists the selected item's settings",
    rings=[{"at": T("B44", "the six uniforms"), "box": [0.02, 0.02, 0.98, 0.98]}, {"at": nudge(_e1 + 0.07), "box": [0.02, 0.12, 0.98, 0.27]},
           {"at": nudge(_e2 + 0.07), "box": [0.02, 0.27, 0.98, 0.42]}])


# ───────────────────────────── timing and size checks ─────────────────────────────
def check_timing():
    bad = []
    for e in E:
        en, bid = e["entry"], e["bid"]
        if en["lane"] == "manim":
            for s in en["show"]:
                a = s["at"]
                if 0.40 < a < 0.56:
                    bad.append(f"{bid}: Manim event at {a} is inside the 40 to 56 % dead zone: {s['event']}")
                if 0.30 < a <= 0.40 and "quick" not in s["event"]:
                    bad.append(f"{bid}: Manim event at {a} must be a quick one: {s['event']}")
            continue
        p = en.get("props", {})
        times = []
        for c in p.get("cues", []):
            times.append(c["at"] if isinstance(c, dict) else c)
            if isinstance(c, dict) and len(c.get("label", "")) > 60:
                bad.append(f"{bid}: cue label over 60 characters: {c['label']!r}")
        for key in ("readouts", "rings"):
            for r in p.get(key, []):
                times.append(r["at"])
                if key == "readouts" and len(r["text"].split()) > 3:
                    bad.append(f"{bid}: readout over 3 words: {r['text']!r}")
        if p.get("ramp"):
            times.append(p["ramp"]["at"])
        for a in times:
            if isinstance(a, (int, float)) and a <= 1 and (0.45 <= a <= 0.55 or 0.83 <= a <= 0.87):
                bad.append(f"{bid}: a cue, readout or ring starts at {a} (inside 45 to 55 % or on the 85 % frame)")
        if len(p.get("caption", "")) > 80:
            bad.append(f"{bid}: caption over 80 characters")
        if p.get("code") and len(p["code"].split("\n")) > 14:
            bad.append(f"{bid}: code over 14 lines")
        for k in ("note", "title"):
            v = p.get(k)
            if isinstance(v, str) and len(v.split()) > 12:
                bad.append(f"{bid}: {k} over 12 words (GATE T 8.5): {v!r}")
        for s in en["show"]:
            if not (0 <= s["at"] <= 1):
                bad.append(f"{bid}: show time out of range {s}")
    return bad


for _e in E:
    _e["entry"]["show"] = sorted(_e["entry"]["show"], key=lambda x: x["at"])      # cue lists read in time order
problems = check_timing()
if problems:
    print("TIMING / SIZE PROBLEMS:")
    for pr in problems:
        print("  " + pr)

# Where each capture's breakpoints should sit, in words (printed by --times next to the estimated and measured fractions).
ANCHORS = [
    ("C01", "B01", "a crosshair with six dials", "the first dial may start moving"),
    ("C01", "B01", "No picture file", "the pause at the defaults (44 to 56 %) should cover this phrase"),
    ("C01", "B01", "every piece is a rule", "the last three dials begin"),
    ("C04", "B10", "and the circle gets a dial", "the radius drops to 0.1 over this clause"),
    ("C04", "B10", "Turn the dial and the circle grows", "the radius rises to 0.45 here (inside no cue window; keep the hold across 50 %)"),
    ("C21", "B40", "Dot size grows the dot", "dot_size rises from 0 to 1.0 over this sentence"),
    ("C21", "B40", "Ring distance pushes the ring", "ring_distance drops to 0 as this starts, holds across 50 %, rises to 1.0 over the rest"),
    ("C22", "B41", "Ring width thickens the ring", "ring_width rises from 0 to 1.0 over this sentence"),
    ("C22", "B41", "Arm length stretches the arms", "arm_length drops to 0 as this starts, holds across 50 %, rises to 1.0 (crossing the ring at about half the rise)"),
    ("C22", "B41", "Nothing doubles where they cross", "arm_length is holding at 1.0 from here to the end"),
    ("C23", "B42", "Arm width thickens the arms", "arm_width rises from 0 to 1.0 over this sentence"),
    ("C23", "B42", "Arm gap opens the middle", "arm_gap drops to 0 as this starts (arms that run into the dot)"),
    ("C23", "B42", "to arms that start far from it", "arm_gap rises to 1.0 here"),
    ("C24", "B43", "Arm length at zero", "readout 'arm length 0?' (the question)"),
    ("C24", "B43", "The dot and the ring", "the state jumps to arm_length = 0"),
    ("C24", "B43", "Ring width at zero", "readout 'ring width 0?' (the question)"),
    ("C24", "B43", "The dot and the arms", "the state jumps to ring_width = 0 (arm_length back to its default)"),
    ("C24", "B43", "Push any dial to either end", "all six dials = 1.0"),
    ("E1", "B44", "the six uniforms", "ring on the group"),
    ("E1", "B44", "A designer can tune", "the first dissolve (state 2) begins about here; the second (state 3) about 0.16 of the beat later"),
]

if "--capture-rows" in sys.argv:
    def _row(cid, beat, shader, target, length, verified):
        print(f"| {cid} | {beat} | `{shader}` | {target} | {length} | {verified} |")
    _row("C04", "B10", "03-circle-slider", "`--length` = the audio of B10. " + sweep_text(_rad) + " (the voice says \"Turn the dial and the circle grows\" as it rises). `circle-slider.mp4`", "about 12 s",
         "coverage 0.0314 at 0.1, 0.2828 at 0.3, 0.6363 at 0.45 (480 by 480)")
    _row("C21", "B40", "17-crosshair", "`--length` = the audio of B40. Two dials back to back, each from 0 to 1 and ending on 1; the first stays at 1.0 while the second moves. " + sweep_text(_a1) + "; then " + sweep_text(_a2) +
         ". The 50 % frame is inside ring_distance's hold at 0 (dot_size at 1.0), the 85 % frame in the final hold (both at 1.0). `sweep-dot-ring.mp4`", "about 10.5 s",
         "`dot_size` 0 and 1: coverage 0.0379 and 0.0457; `ring_distance` 0 and 1: 0.0199 and 0.0582; held pairs (`pair-dot1-ring0`, `pair-dot1-ring1`): 0.0257 and 0.0641")
    _row("C22", "B41", "17-crosshair", "`--length` = the audio of B41; the same shape as C21. " + sweep_text(_b1) + "; then " + sweep_text(_b2) +
         f". The arms cross the ring at about 0.5 on the dial, near {pct(_cross_at)} of the beat; the voice says \"Nothing doubles where they cross\" over the final hold. `sweep-width-length.mp4`", "about 9.5 s",
         "`ring_width` 0 and 1: 0.0199 and 0.0939; `arm_length` 0 and 1: 0.0234 and 0.0519; held pairs (`pair-rw1-al0`, `pair-rw1-al1`): 0.0789 and 0.1039")
    _row("C23", "B42", "17-crosshair", "`--length` = the audio of B42; the same shape as C21. " + sweep_text(_c1) + "; then " + sweep_text(_c2) +
         ". The voice says \"arms that run into the dot\" over arm_gap's hold at 0 and \"arms that start far from it\" as the gap opens. `sweep-armwidth-gap.mp4`", "about 8 s",
         "`arm_width` 0 and 1: 0.0234 and 0.0617; `arm_gap` 0 and 1: 0.0389 and 0.0398 (at 0 the arms start at the center and run into the dot); held pairs (`pair-aw1-ag0`, `pair-aw1-ag1`): 0.0598 and 0.0617")
    _row("C24", "B43", "17-crosshair", "STEPPED (`--steps`: instant changes, no ramps), fractions of the clip: defaults to " + pct(_t1) + "; `arm_length` = 0 from " + pct(_t1) + " to " + pct(_t2) +
         "; the defaults again from " + pct(_t2) + " to " + pct(_t3) + " (the 50 % frame is a settled state); `ring_width` = 0 from " + pct(_t3) + " to " + pct(_t4) + "; all six dials = 1.0 from " + pct(_t4) +
         " to the end (the 85 % frame). Harness: `" + _steps_arg + "`. `extremes.mp4`", "about 13 s",
         "all six at 0 draws nothing (coverage 0.0000); all six at 1 has coverage 0.1998; the two held states are single-dial renders: `crosshair-arm_length-0` (0.0234, dot and ring) and `crosshair-ring_width-0` (0.0199, dot and arms)")
    print(f"\nE1 timeline: defaults to {pct(_e1)}; dissolve to state 2 from {pct(_e1)} to {pct(_e1 + 0.06)}; hold; dissolve to state 3 from {pct(_e2)} to {pct(_e2 + 0.06)}; hold to the end.")
    sys.exit(0)

if "--times" in sys.argv:
    print(f"{'beat':5} {'estimated':>9} {'measured':>9}  phrase")
    seen = set()
    for bid, phrase in USED:
        if (bid, phrase) in seen:
            continue
        seen.add((bid, phrase))
        m = measured_start(bid, phrase)
        print(f"{bid:5} {estimated_start(bid, phrase):9.2f} {('%9.2f' % m) if m is not None else '        -'}  {phrase}")
    print("\nBreakpoints for the sweep captures (fractions of the clip; the harness converts them with --length SECONDS):")
    for cid, sw in SWEEPS.items():
        if cid == "C24":
            print(f"{cid}: " + " ".join(f"--steps {n}:" + ",".join(f"{t:g}:{v:g}" for t, v in kv) for n, kv in sw.items()))
        elif cid == "E1":
            for what, a0, a1 in sw:
                print(f"{cid}: {what} from {a0:.2f} to {a1:.2f}")
        else:
            for one in sw:
                print(f"{cid}: " + animate_arg(one))
    print("\nCapture anchors (the phrases the breakpoints above follow, estimated and measured fraction; use them to check by ear that a move starts where the voice names it):")
    for cid, bid, phrase, note in ANCHORS:
        m = measured_start(bid, phrase)
        print(f"{cid:4} {bid:5} {estimated_start(bid, phrase):9.2f} {('%9.2f' % m) if m is not None else '        -'}  {phrase}: {note}")
    sys.exit(0)

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
(HERE / "lanes").mkdir(exist_ok=True)
NACTS = 5
for ai in range(NACTS):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

lanes_hist = {}
for e in E:
    lanes_hist[e["entry"]["lane"]] = lanes_hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
sl = ["# Shot list: Drawing Shapes with Math\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat "
      "was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can "
      "disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab or editor capture of a tested file in `lab-shaders/`; every number on screen was computed or measured in "
      "Godot 4.7.2 (`evidence/planning-checks/`). The capture lane is the largest because this film is about code and its picture; each of those beats "
      "was weighed against a drawing and won on evidence, not on habit. Every cue time in `lanes/` is derived from where the words fall in the narration "
      "(`_gen_lanes.py`), and none starts inside the 45 to 55 % window the gates sample.\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`), with a **square result window** (every result in this film "
      "is 1:1; the spec shows only 16:9). 2. **`shader_kit.py`** Manim objects used here: `ramp_strip`, `pixel_grid`, `plot`, `uv_square`; this film "
      "adds film-local helpers in `scenes.py` (a disc, a slider with a knob, a wall-and-box, a two-circle Venn). 3. **Capture harness** `lab/capture.gd` "
      "+ `capture_shader.sh` (piecewise `--animate`, `--steps`, `--set-at`, `--scene` and fractional keyframes with `--length` are all in the spec), which must also give square output. 4. **Editor frames E1** (see "
      "`CAPTURE-PLAN.md`; E2, an editor view of the compile error, is an optional upgrade for B32). 5. Registered patterns used: `LectureEvidenceTable`, "
      "`LectureCodeTrace` (checked with `./brutalist.art/art scenes --check`).\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
