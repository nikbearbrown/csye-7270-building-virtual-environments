#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json, SHOTLIST.md, CAPTURE-PLAN.md and evidence/planning-checks/captures.json.

Why a generator: the code shown on screen must be the tested file text; every capture's event times must come from the narration (so a change to
a line moves its picture with it); and the shot list, capture plan and lanes must say the same thing.
Re-run after any edit:   python3 _gen_lanes.py && python3 make_sheet.py
Times: the voice speaks about 0.34 s per word (series_config.SEC_PER_WORD), so a sentence starts at (words before it) * 0.34 s into its beat.
A capture is recorded for that estimate; the build session re-times a capture (edit captures.json, re-record) if a measured beat differs by more than a second.
"""
import importlib.util
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
EV = HERE / "evidence" / "planning-checks"
spec = importlib.util.spec_from_file_location("narration", HERE / "narration.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)

SPW = 0.34
TEXT = {bid: t for bid, _, t in N.BODY}
ACTOF = {bid: a for bid, a, _ in N.BODY}


# ───────────────────────────── timing helpers ─────────────────────────────
def sents(bid):
    return re.split(r"(?<=[.!?])\s+", TEXT[bid].strip())


def D(bid):
    return len(TEXT[bid].split()) * SPW


def T(bid, k, off=0.0):
    """Estimated start (seconds into the beat) of sentence k, plus off."""
    return round(sum(len(s.split()) for s in sents(bid)[:k]) * SPW + off, 2)


def TW(bid, k, w):
    """Estimated start of word w (0-based) inside sentence k."""
    return round((sum(len(s.split()) for s in sents(bid)[:k]) + w) * SPW, 2)


def F(bid, t):
    """Seconds -> fraction of the beat, kept out of the 45 to 55 percent window (no cue starts there)."""
    f = max(0.02, min(0.97, t / D(bid)))
    if 0.44 < f < 0.56:
        f = 0.43 if f < 0.5 else 0.57
    return round(f, 3)


def SECONDS(bid):
    return int(math.ceil(D(bid))) + 1


# ───────────────────────────── code helpers ─────────────────────────────
def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def ln(fn, needle, nth=1):
    """1-based line number of the nth line containing needle."""
    k = 0
    for i, line in enumerate(code_of(fn).split("\n"), 1):
        if needle in line:
            k += 1
            if k == nth:
                return i
    raise KeyError(f"{needle!r} not in {fn}")


# ───────────────────────────── registries ─────────────────────────────
E = []      # lane entries in beat order
CAPS = {}   # capture id -> scene description (captures.json) + plan text


def add(bid, about, entry, evidence=""):
    E.append({"bid": bid, "act": ACTOF[bid], "about": about, "evidence": evidence, "entry": entry})


def manim(bid, about, cls, intent, motion, show, runner, why, evidence):
    add(bid, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                     "show": [{"at": F(bid, t), "event": ev} for t, ev in show], "runner_up": runner, "why": why, "sparse": True}, evidence)


def rem(bid, about, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                     "show": [{"at": F(bid, t), "event": ev} for t, ev in show], "runner_up": runner, "why": why, "sparse": False}, evidence)


def cap(cid, bid, plan, verified, **cfg):
    d = {"beats": [bid], "seconds": cfg.pop("seconds", SECONDS(bid))}
    d.update(cfg)
    CAPS[cid] = {"cfg": d, "plan": plan, "verified": verified, "bid": bid}
    return cid


def lab(bid, about, cid, shader, video, label, cues, intent, motion, show, runner, why, evidence, layout="side", readouts=None,
        rings=None, ramp=None, title=None, caption="", code=None, code_file=None, lane="capture"):
    c = CAPS[cid]
    c["cfg"]["out"] = video.split("/")[-1]       # the file name the lane expects under godot-shaders/ (record_all.sh names its output so)
    for cue in cues:
        assert len(cue) < 3 or len(cue[2]) <= 60, f"{bid}: cue label over 60 characters: {cue[2]!r}"
    assert len(caption) <= 80, f"{bid}: caption over 80 characters"
    spec_txt = (f"{cid}: {c['plan']} Scene = evidence/planning-checks/light_scene.gd with captures.json id {cid}; 1920 x 1080 window at scale 1, "
                f"30 fps, {c['cfg']['seconds']} s, Forward+. Expected: {c['verified']}")
    props = {"layout": layout, "code": code if code is not None else (code_of(shader) if shader else ""),
             "codeFile": code_file or (f"lab-shaders/{shader}" if shader else ""),
             "cues": [dict({"at": F(bid, c[0]), "lines": c[1]}, **({"label": c[2]} if len(c) > 2 else {})) for c in cues],
             "video": video, "videoLabel": label,
             "readouts": [{"at": F(bid, t), "text": txt, "x": x, "y": y} for t, txt, x, y in (readouts or [])],
             "rings": [{"at": F(bid, t), "box": box} for t, box in (rings or [])],
             "caption": caption, "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = {"at": F(bid, ramp[0]), "from": ramp[1], "to": ramp[2]}
    add(bid, about, {"lane": lane, "pattern": "ShaderLab", "props": props, "capture_spec": spec_txt, "visual_intent": intent,
                     "motion_claim": motion, "show": [{"at": F(bid, t), "event": ev} for t, ev in show], "runner_up": runner,
                     "why": why, "sparse": False}, evidence)


# lamp / scene vocabulary used by captures (see light_scene.gd)
BLOB = {"kind": "blob", "x": 1280, "y": 720, "scale": 2.0}
WARM_LAMP = {"x": 960, "y": 540, "color": "warm", "energy": 1.0}


def lamp(scale, **kw):
    d = dict(WARM_LAMP)
    d["scale"] = scale
    d.update(kw)
    return d


VL = "Godot 4.7.2 · Forward+ · 1920 × 1080"

# ═════════════════════════════ ACT I · Lights in 2D ═════════════════════════════
cap("C01", "B01", "Dusk tiled floor, one warm lamp (scale 7: reach 896 px) at the centre, the teal blob at lower right on default lighting. The lamp bulb disc marks the lamp.",
    "before the switch a soft round glow on the tiles; after it a soft-edged wedge turning clockwise from the lamp, the blob unchanged.",
    ambient="dusk", lamp_bulbs=True, props=[BLOB], lamps=[lamp(7.0)],
    shader=[{"node": "floor", "file": "13-lighthouse-soft.gdshader", "at": TW("B01", 1, 7)}])
lab("B01", "a flat-looking glow, then a beam", "C01", "13-lighthouse-soft.gdshader", "godot-shaders/ls-c01-hook.mp4",
    "Godot 4.7.2 · same scene, light() switched on · scripted", [],
    "Act title 'Lights in 2D' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a dusk-blue tiled floor, a teal blob and a lamp. For a few seconds the lamp is a soft round glow. At the words 'one function later' the floor's shader switches on and the glow becomes a soft-edged beam sweeping round. Caption: 'light(): runs once per pixel for each light that touches it'.",
    "The glow turns into a sweeping beam at the moment the voice says 'one function later'.",
    [(0.0, "soft glow, window labelled"), (TW("B01", 1, 7), "shader switches on: the beam appears and turns")],
    "manim drawing of a glow becoming a beam", "A real render is the honest picture of 'a glow' versus 'a beam from the same light'; a drawing would only claim it.",
    "Capture C01 (scene verified; the wedge shader measured in verify8 C15 and verify7 D)", layout="video", title="Lights in 2D",
    readouts=[(0.2, "default light", 0.17, 0.07), (TW("B01", 1, 7), "light()", 0.83, 0.07)], caption="light(): runs once per pixel for each light that touches it")

manim("B02", "two kinds of 2D light", "TwoLights",
      "Two panels on the cream stage, each a short strip of six outlined floor tiles. Left: a pale lamp disc above the strip with rays fanning out to every tile, label 'point light'. Right: a sun disc far up with parallel rays slanting the same way onto the strip, label 'directional light'. Grey captions under them: 'like a lamp', 'like the sun'.",
      "Rays fan out from the lamp in every direction; on the right they arrive side by side, all parallel.",
      [(0.4, "two floor strips"), (T("B02", 1), "rays fan out from the lamp"), (T("B02", 2), "parallel rays from the sun"), (T("B02", 3), "ring on the lamp")],
      "isometric lamp and sun drawing (show-tell)", "Fan versus parallel is the whole difference between the two lights, and rays drawn on the spoken cue show it with motion.",
      "docs: Light2D / DirectionalLight2D classes (parallel rays); verify2 Q (one arrow everywhere)")

cap("C02", "B03", "Dusk floor with ONE lamp (scale 4) at (760, 520) and the blob at (1180, 660). No tint for the first part (a white CanvasModulate: the scene is fully lit); the tint eases to dusk (0.50, 0.55, 0.72) over one second.",
    "no tint: far floor (1500, 300) = tile colour (0.867, 0.847, 0.788), lit centre clipped to white; dusk: far floor (0.435, 0.467, 0.569), lit (900, 520) = (0.980, 0.910, 0.804).",
    ambient="off", lamp_bulbs=True, props=[{"kind": "blob", "x": 1180, "y": 660, "scale": 2.0}],
    lamps=[lamp(4.0, x=760, y=520)], ambient_to={"from": "off", "to": "dusk", "t0": TW("B03", 2, 9), "t1": TW("B03", 2, 9) + 1.0})
lab("B03", "a light needs a dim scene; the ambient tint", "C02", None, "godot-shaders/ls-c02-ambient.mp4", "Godot 4.7.2 · ambient tint added · scripted", [],
    "A real Godot render in a framed window: a cream-tiled floor already fully lit, a lamp that barely shows. At 'set it dim' the tint eases in, the floor goes dusk blue and the lamp's glow blooms. Caption: 'ambient light: the tint where no lamp reaches'; a label 'Canvas Modulate' lands as the node is named.",
    "The scene dims and the lamp suddenly stands out.",
    [(0.2, "fully lit floor, lamp barely visible"), (TW("B03", 2, 9), "dusk tint eases in; the glow blooms"), (T("B03", 3), "'ambient' label on the dim floor")],
    "manim: floor strip with a tint slider", "The film's first point is a before and after on one scene; only a real render shows how little a light adds to a bright floor.",
    "Capture C02; docs 2D lights and shadows (CanvasModulate)", layout="video",
    readouts=[(0.4, "no tint", 0.17, 0.07), (TW("B03", 2, 2), "Canvas Modulate", 0.17, 0.14), (T("B03", 3), "ambient", 0.80, 0.80)], caption="ambient light: the tint where no lamp reaches")

cap("C03", "B05", "Dusk floor, one warm lamp at the centre, blob at lower right. In turn: scale 2 to 6 (smooth), colour warm to cool blue-white, energy 1.0 to 0.2 then to 1.5 (smooth).",
    "lamp settings read back from the scene: scale 2.0 at 4.0 s and 6.0 at 6.5 s; colour from warm (1.0, 0.86, 0.55) to cool (0.55, 0.85, 1.0) by 8.3 s; energy 0.21 at 8.7 s and 1.5 at 10.5 s (render_captures state print). No pixel probe: these are lamp settings, not shader results.",
    ambient="dusk", lamp_bulbs=True, props=[BLOB],
    lamps=[{"x": 960, "y": 540, "scale": 2.0, "energy": 1.0, "color": "warm",
            "sweeps": [{"prop": "scale", "from": 2.0, "to": 6.0, "t0": T("B05", 2, 0.1), "t1": T("B05", 3, -0.1), "ease": "smooth"},
                       {"prop": "energy", "from": 1.0, "to": 0.2, "t0": TW("B05", 3, 4), "t1": TW("B05", 3, 4) + 0.8, "ease": "smooth"},
                       {"prop": "energy", "from": 0.2, "to": 1.5, "t0": TW("B05", 3, 4) + 0.8, "t1": TW("B05", 3, 4) + 2.6, "ease": "smooth"}],
            "color_sweep": {"from": "warm", "to": [0.55, 0.85, 1.0], "t0": T("B05", 3, 0.0), "t1": T("B05", 3, 1.7)}}])
lab("B05", "a light's settings: texture, scale, color, energy", "C03", None, "godot-shaders/ls-c03-settings.mp4", "Godot 4.7.2 · lamp settings changed in turn · scripted", [],
    "A real Godot render: one lamp on the dusk floor. Its glow first grows (scale), then shifts from warm to cool (color), then dims and brightens (energy); a small label names each setting as the voice says it. Caption: 'reach: how far the light spreads · energy: how strong it is'.",
    "The same lamp grows, changes color, then dims and brightens, one setting at a time.",
    [(T("B05", 1), "texture: the soft shape"), (T("B05", 2, 0.1), "scale sweep"), (T("B05", 3), "color sweep"), (TW("B05", 3, 4), "energy sweep")],
    "manim: three dials", "Each setting changes the glow differently, and a real render shows all three effects on the same lamp.",
    "Capture C03; docs Light2D / PointLight2D class properties", layout="video",
    readouts=[(T("B05", 1), "texture", 0.17, 0.07), (T("B05", 2), "scale", 0.17, 0.14), (T("B05", 3), "color", 0.17, 0.21), (TW("B05", 3, 4), "energy", 0.17, 0.28)],
    caption="reach: how far the light spreads · energy: how strong it is")

rem("B04", "the docs' recipe for a soft glow", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html", "image": "godot-shaders/ls-docs-2d-lights.png",
     "caption": "Godot 4.7 documentation · 2D lights and shadows · captured at build time", "frame": "browser",
     "moves": [{"at": 0.0, "x": 0.5, "y": 0.5, "scale": 1},
               {"at": F("B04", T("B04", 1)), "x": 0.42, "y": 0.52, "scale": 1.5, "ring": [0.08, 0.46, 0.84, 0.14]},
               {"at": F("B04", T("B04", 3)), "x": 0.42, "y": 0.55, "scale": 2.2, "ring": [0.36, 0.55, 0.40, 0.04]}],
     "moveSeconds": 1.2, "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 'Point lights' section in a browser window. The camera pushes in on the paragraph that gives the recipe (gradient texture, fill radial, opaque white to transparent white) with one terracotta ring, then closes in on the words 'opaque white to transparent white'.",
    "The camera pushes in on the recipe paragraph, then on the two colors the voice names.",
    [(0.0, "page"), (T("B04", 1), "push-in and ring on the recipe paragraph"), (T("B04", 3), "closer ring on 'opaque white to transparent white'")],
    "manim: a gradient strip from white to transparent", "The recipe is a documentation claim, and the documentation itself is the evidence (SHOW-THE-THING); the ring positions are set from the real capture.",
    "Playwright capture D1 of the live docs page (1600 x 900 at 2.4x) at build time; read 2026-10-13")

cap("C04", "B06", "Dusk tiled floor. Three warm lamps (scale 3.5, energy 0.4) close together in a triangle: the first is on from the start, the second appears at 'overlapping', the third at 'three make it brighter still'.",
    "overlap point (960, 540) steps up with each lamp (verify9 B: far floor (0.435, 0.467, 0.569) stays the same; the overlap rises from dusk to near white).",
    ambient="dusk", lamp_bulbs=True,
    lamps=[lamp(3.5, x=860, y=590, energy=0.4), lamp(3.5, x=1060, y=590, energy=0.4, appear=TW("B06", 1, 0) + 0.2), lamp(3.5, x=960, y=420, energy=0.4, appear=TW("B06", 1, 8))])
lab("B06", "lights add", "C04", None, "godot-shaders/ls-c04-lights-add.mp4", "Godot 4.7.2 · lamps switched on one by one · scripted", [],
    "A real Godot render: dusk floor and three warm lamps in a triangle that switch on one after another. The overlap gets brighter with each lamp while the far floor stays at its dim ambient look. Small labels '1 lamp', '2 lamps', '3 lamps' and 'ambient' (on the far floor).",
    "The overlap brightens in steps as each lamp appears; the far floor does not change.",
    [(0.0, "one lamp"), (TW("B06", 1, 0) + 0.2, "second lamp: the overlap brightens"), (TW("B06", 1, 8), "third lamp: brighter still"), (T("B06", 2), "far floor stays dim: 'ambient'")],
    "manim: three overlapping circles", "Brightness stepping up where lights overlap is best seen on the real floor; circles would only suggest it.",
    "Capture C04; verify4 N, verify9 B", layout="video",
    readouts=[(0.1, "1 lamp", 0.17, 0.07), (TW("B06", 1, 0) + 0.2, "2 lamps", 0.17, 0.14), (TW("B06", 1, 8), "3 lamps", 0.17, 0.21), (T("B06", 2), "ambient", 0.85, 0.85)])

manim("B07", "the pixel rule, measured", "Formula",
      "The rule as outlined swatch boxes on the cream stage: [surface 0.5] x ( [ambient 0.2] + [lamp 0.4] + [lamp 0.4] ) = [pixel 0.5], each swatch filled with the grey of its own number. Small grey credit: 'measured · Godot 4.7.2 · Forward+ · 0, 1, 2, 3 lamps: 0.1, 0.3, 0.5, 0.7'.",
      "The two lamp boxes slide in one after the other and the result swatch fills to the sum, ending on one half.",
      [(T("B07", 1, 0.4), "surface box"), (T("B07", 1, 3.0), "ambient box inside the bracket"), (TW("B07", 2, 11), "first lamp box"), (TW("B07", 2, 14), "second lamp box"), (TW("B07", 2, 19), "result swatch fills: one half")],
      "LectureEvidenceTable", "A sum that builds as each lamp arrives is the rule in motion; a table only lists the numbers.",
      "verify7 E: 0.098, 0.298, 0.498, 0.698 for 0 to 3 lamps (surface 0.5, ambient 0.2, energy 0.4 each); verify1 C to F2")

manim("B08", "a 2D shader has three functions; light asks per lamp per pixel", "PerLamp",
      "A header strip of three outlined boxes, 'vertex()  corners', 'fragment()  pixels', 'light()  lamps'; the third is ringed. Below, one pixel cell on a small floor strip with two lamp dots; an arrow runs from each lamp to the pixel and a small 'light()' box answers each arrow with its own swatch, the swatches piling up. Caption: 'light(): once per pixel, for each light that touches it'.",
      "The two arrows travel from the lamps to the pixel; each is answered by a swatch and the swatches pile up.",
      [(0.4, "three function boxes"), (T("B08", 2), "light() ringed"), (TW("B08", 2, 8), "arrows from both lamps"), (TW("B08", 2, 17), "answers pile up at the pixel")],
      "DesignPipelineClaim, show-tell isometric", "The idea is one function called many times, once per lamp per pixel; arrows arriving one after another show the repetition.",
      "docs: CanvasItem shaders (vertex, fragment, light); verify4 N (ambient + 0.2 per lamp, 0 to 4 lamps)")

# ═════════════════════════════ ACT II · The Light Function ═════════════════════════════
cap("C05", "B09", "Dusk tiled floor, one warm lamp (scale 5) at the centre, the blob at (1250, 700). The floor starts on default lighting; at 'Even an empty one' it switches to 01-light-empty. The blob never changes.",
    "floor (1100, 540) = (1.000, 0.949, 0.824) before and (0.400, 0.427, 0.518) after (tile x dusk); blob centre (0.365, 0.616, 0.561) before and after (verify8 C05).",
    ambient="dusk", lamp_bulbs=True, props=[{"kind": "blob", "x": 1250, "y": 700, "scale": 2.0}], lamps=[lamp(5.0)],
    shader=[{"node": "floor", "file": "01-light-empty.gdshader", "at": T("B09", 1)}])
lab("B09", "an empty light() replaces the default for that sprite", "C05", "01-light-empty.gdshader", "godot-shaders/ls-c05-empty-light.mp4",
    "Godot 4.7.2 · empty light() assigned to the ground · scripted",
    [(0.5, [3, 4], "light(): runs once per pixel for each light that touches it"), (T("B09", 3), [3, 4], "replaces Godot's default lighting for this sprite")],
    "Act title 'The Light Function' (serif 40) top-left. Code card at left with the empty light() function and a definition tag on its first line ('light(): runs once per pixel for each light that touches it'); at right a real Godot window: the lit floor and the blob. At 'Even an empty one' the glow leaves the floor (only the dusk look is left) while the blob stays lit. A ring settles on the blob, labels 'default lighting' (blob) and 'empty light()' (ground).",
    "The glow vanishes from the floor but stays on the blob the instant the empty function is added.",
    [(0.3, "function lines highlighted"), (T("B09", 1), "empty function assigned: the glow leaves the ground"), (T("B09", 2), "ring on the blob: still lit"), (T("B09", 3), "code highlighted again: it belongs to the sprite")],
    "LectureCodeTrace alone", "The claim is a before and after on one picture, with the unchanged blob as the control; the code card is the cause.",
    "Capture C05; verify1 G, verify4 O, verify8 C05", title="The Light Function",
    readouts=[(T("B09", 2), "default lighting", 0.68, 0.52), (T("B09", 2), "empty light()", 0.2, 0.2)],
    rings=[(T("B09", 2), [0.585, 0.56, 0.72, 0.74])])

cap("C06", "B10", "Dusk tiled floor with three warm lamps (scale 3.4, energy 0.4) stacked near the centre that switch on at 'Add a lamp', 'Add another' and 'once for each lamp'. A grey card (0.7, 640 x 400 px) at the centre wears 02-light-flat; the floor stays on default lighting.",
    "card at (700, 700): (0.349, 0.384, 0.502) with no lamp, then (0.549, 0.584, 0.702), (0.749, 0.784, 0.902), (0.949, 0.984, 1.000): +0.2 per lamp (verify8 C06).",
    ambient="dusk", lamp_bulbs=True, card={"x": 960, "y": 540, "w": 640, "h": 400, "color": [0.7, 0.7, 0.7]},
    lamps=[lamp(3.4, x=900, y=500, energy=0.4, appear=T("B10", 1, 0.3)), lamp(3.4, x=960, y=540, energy=0.4, appear=T("B10", 2, 0.2)), lamp(3.4, x=1020, y=580, energy=0.4, appear=T("B10", 3, 0.6))],
    shader=[{"node": "card", "file": "02-light-flat.gdshader", "at": 0}])
lab("B10", "a flat light(): once per lamp, answers add", "C06", "02-light-flat.gdshader", "godot-shaders/ls-c06-flat-light.mp4",
    "Godot 4.7.2 · lamps switched on one by one · scripted",
    [(0.4, [4]), (T("B10", 3), [3, 4, 5])],
    "Code card at left with the flat light() (LIGHT = vec4(0.2, 0.2, 0.2, 1.0)); at right a real Godot window: a grey card on the dusk floor. Each lamp that switches on lifts the card by one more flat step, with no soft falloff, while the floor around it shows the lamps' soft glows. Readouts '+0.2', '+0.4', '+0.6'.",
    "The card brightens by the same step each time a lamp appears.",
    [(0.4, "flat function highlighted"), (T("B10", 1, 0.3), "first lamp: +0.2"), (T("B10", 2, 0.2), "second lamp: +0.4"), (T("B10", 3, 0.6), "third lamp: +0.6")],
    "manim: three stacked swatches", "Equal steps per lamp on a real card are the proof that the function runs once per lamp and the answers add.",
    "Capture C06; verify4 N (0.2, 0.4, 0.6, 0.8, 1.0), verify8 C06",
    readouts=[(T("B10", 1, 0.3), "+0.2", 0.85, 0.62), (T("B10", 2, 0.2), "+0.4", 0.85, 0.70), (T("B10", 3, 0.6), "+0.6", 0.85, 0.78)])

manim("B11", "built-ins in, LIGHT out", "FunctionBox",
      "A box labelled light(). Four arrows come in from the left, labelled in monospace capitals COLOR, UV, LIGHT_COLOR, LIGHT_ENERGY; one arrow leaves to the right labelled LIGHT. Caption: 'built-in: a value the engine hands to a function, or collects from it'. A grey note: 'more in the docs: NORMAL, SCREEN_UV ...'.",
      "The four inputs slide into the box one after another and the single answer leaves on the right.",
      [(0.4, "box"), (T("B11", 1, 0.3), "COLOR and UV arrive"), (T("B11", 2, 0.3), "LIGHT_COLOR and LIGHT_ENERGY arrive"), (T("B11", 3, 2.0), "LIGHT leaves")],
      "BrowserCapture of the docs table", "The idea is values in and one value out; a box with arrows is exactly that, while the docs table has more rows than the voice can name.",
      "docs: CanvasItem shaders, Light built-ins (read 2026-10-13); verify1 K, M, M2; verify4 U (UV in light), C (COLOR is fragment's output)")

manim("B12", "fragment first, then light per lamp, then the sum", "Order",
      "A strip left to right on the cream stage: 'fragment()  sets color' -> 'light()  once per lamp' (two small lamp dots feed it, each answer a small swatch) -> '+ dim ambient look' -> a pixel swatch. A token travels the strip; the arrows are drawn shapes pointing only forward.",
      "A token passes fragment, splits into one pass per lamp, and the answers join the ambient look to make the pixel.",
      [(0.4, "strip"), (T("B12", 1, 0.6), "token through fragment()"), (T("B12", 2, 0.4), "one pass per lamp"), (T("B12", 3), "the sum fills the pixel")],
      "DesignPipelineClaim, show-tell isometric", "An order of work is a token moving forward through stages, never back.",
      "verify4 C (COLOR in light() is what fragment() set); verify1 H (ambient look + each LIGHT)")

cap("C07", "B13", "Dusk tiled floor in two halves of one picture (left half default, right half wears 03-light-default); one warm lamp (scale 6) on the seam at the centre; the blob at (1250, 700) on default lighting.",
    "right half against an all-default render of the same scene: max difference 0.000, 0 of 1,036,800 pixels differ (Forward+); Compatibility within one step of 255 (verify8 C07, verify3 R1).",
    ambient="dusk", split=True, lamp_bulbs=True, props=[{"kind": "blob", "x": 1250, "y": 700, "scale": 2.0}], lamps=[lamp(6.0)],
    shader=[{"node": "floor", "file": "03-light-default.gdshader", "at": 0}])
lab("B13", "the three-line copy of Godot's default", "C07", "03-light-default.gdshader", "godot-shaders/ls-c07-rebuilt-default.mp4",
    "Godot 4.7.2 · left: default · right: this shader",
    [(T("B13", 1), [4]), (T("B13", 2), [5], "alpha: how visible a pixel is: 0 invisible, 1 solid")],
    "Code card at left (the three-line light()); at right a real Godot window: one floor, one lamp on the seam. The left half uses Godot's default lighting, the right half the shader, and the join is invisible. Labels 'default' (left) and 'this shader' (right) land at the last sentence, with the caption '0 of 1,036,800 pixels differ · Forward+'. The alpha line carries the tag 'alpha: how visible a pixel is: 0 invisible, 1 solid' as alpha is spoken.",
    "The two halves read as one picture; the label 'this shader' lands on the right half only.",
    [(T("B13", 1), "color line highlighted"), (T("B13", 2), "alpha line highlighted"), (T("B13", 3), "labels land on the halves: no seam")],
    "LectureCodeTrace alone", "Code beside a seamless picture is the claim: the copy equals the default.",
    "Capture C07; verify3 R1, verify7 A, verify9 A1 (the file), verify8 C07",
    readouts=[(T("B13", 3), "default", 0.25, 0.1), (T("B13", 3), "this shader", 0.75, 0.1)], caption="0 of 1,036,800 pixels differ · Forward+")

cap("C08", "B14", "Dusk tiled floor, one warm lamp (scale 3.2: a 819 px square texture) at the centre. Default lighting first; at 'Force it to one' the floor switches to 04-light-hard-edge.",
    "after the switch the lit area is a hard square ending exactly at the texture's half-width 409.6 px: added red 0.60 at 390 px and 0.0 at 430 px (verify8 C08).",
    ambient="dusk", lamp_bulbs=True, lamps=[lamp(3.2)],
    shader=[{"node": "floor", "file": "04-light-hard-edge.gdshader", "at": TW("B14", 1, 4)}])
lab("B14", "alpha is the soft edge: force it to one and the glow is a square", "C08", "04-light-hard-edge.gdshader", "godot-shaders/ls-c08-hard-edge.mp4",
    "Godot 4.7.2 · alpha forced to 1.0 · scripted",
    [(0.3, [5]), (TW("B14", 1, 4), [5])],
    "Code card at left (rgb line, then LIGHT = vec4(rgb, 1.0)); at right a real Godot window with the soft round glow until 'Force it to one', when it snaps to a hard square exactly as wide as the lamp's texture. Labels 'soft edge' (glow) and 'hard square'. Caption: 'alpha: how visible a pixel is: 0 invisible, 1 solid'.",
    "The soft glow snaps into a hard-edged square the instant alpha is forced to one.",
    [(0.3, "glow with its soft edge"), (TW("B14", 1, 4), "alpha forced to one: the glow becomes a square"), (T("B14", 2), "label: hard square")],
    "manim: a fading disc against a flat square", "A real render shows the square the texture really is; the drawing of a disc would not.",
    "Capture C08; verify3 R2 (max diff 0.867), verify8 C08, alpha-paint.gdshader (evidence)", title=None,
    readouts=[(0.2, "soft edge", 0.17, 0.07), (T("B14", 2), "hard square", 0.83, 0.07)], caption="alpha: how visible a pixel is: 0 invisible, 1 solid")

cap("C09", "B15", "Dusk tiled floor, one warm lamp (scale 5), the blob. Default glow first; at 'the glow becomes bands' the floor switches to 05-light-bands.",
    "three lit bands plus the dark outer ring; on a grey 0.5 surface (verify7 C) the red channel reads 0.475, 0.349, 0.224, then 0.098 (ambient only).",
    ambient="dusk", lamp_bulbs=True, props=[{"kind": "blob", "x": 1250, "y": 700, "scale": 2.0}], lamps=[lamp(5.0)],
    shader=[{"node": "floor", "file": "05-light-bands.gdshader", "at": TW("B15", 1, 7)}])
lab("B15", "reshape the fade: bands", "C09", "05-light-bands.gdshader", "godot-shaders/ls-c09-bands.mp4", "Godot 4.7.2 · bands switched on · scripted",
    [(T("B15", 1), [5, 6], "floor(x): rounds down to the whole number below"), (T("B15", 3), [5, 6])],
    "Code card at left (the bands line with the tag 'floor(x): rounds down to the whole number below', then LIGHT = vec4(rgb, bands)); at right a real Godot window: the smooth glow turns into three concentric bands like cel shading, the blob still smoothly lit beside it.",
    "The smooth glow snaps into concentric bands when the fade is rounded.",
    [(T("B15", 1), "bands line highlighted"), (TW("B15", 1, 7), "glow becomes bands"), (T("B15", 3), "same lamp, same ground")],
    "manim: a ramp turning into a staircase", "Bands on the real floor beside the unchanged blob show that only the light function changed.",
    "Capture C09; verify7 C (grey surface: 0.475, 0.349, 0.224, 0.098)")

cap("C10", "B16", "Dusk tiled floor, one warm lamp (scale 5), the blob. Default glow first; at 'the lamp breathes' the floor switches to 06-light-pulse.",
    "red at 150 px from the lamp swings between 0.698 and 1.0 (clipped) over two seconds (verify8 C10).",
    ambient="dusk", lamp_bulbs=True, props=[{"kind": "blob", "x": 1250, "y": 700, "scale": 2.0}], lamps=[lamp(5.0)],
    shader=[{"node": "floor", "file": "06-light-pulse.gdshader", "at": TW("B16", 1, 12)}])
lab("B16", "let TIME shape the light: a pulse", "C10", "06-light-pulse.gdshader", "godot-shaders/ls-c10-pulse.mp4", "Godot 4.7.2 · live clock",
    [(T("B16", 1, 0.5), [4], "abs(x): drops the minus sign: -0.3 becomes 0.3"), (T("B16", 1, 3.0), [5])],
    "Code card at left (the pulse line, then the rgb line that multiplies by it); at right a real Godot window where the lamp breathes brighter and dimmer. Caption: 'TIME: seconds on one clock shared by the whole game'.",
    "The glow swells and fades on its own, over and over.",
    [(T("B16", 1, 0.5), "pulse line highlighted"), (TW("B16", 1, 12), "the lamp starts to breathe"), (T("B16", 2), "it keeps going with no game code")],
    "manim sine plot", "A real pulse next to the one line that makes it shows the effect and the cause.",
    "Capture C10; verify8 C10; docs TIME", caption="TIME: seconds on one clock shared by the whole game")

cap("C11", "B17", "Dusk tiled floor, no lamps. Two pale bulb discs (scale 1.9, about 120 px) at (700, 540) and (1220, 540) on default lighting; at 'unshaded' the right one gets 07-unshaded.",
    "bulb 1 stays (0.502, 0.510, 0.447); bulb 2 goes from that to its own colour (1.0, 0.929, 0.620) (verify8 C11).",
    ambient="dusk", props=[{"kind": "bulb", "name": "bulb1", "x": 700, "y": 540, "scale": 1.9}, {"kind": "bulb", "name": "bulb2", "x": 1220, "y": 540, "scale": 1.9}],
    shader=[{"node": "bulb2", "file": "07-unshaded.gdshader", "at": TW("B17", 1, 3)}])
lab("B17", "render mode unshaded: ignores lights and the ambient tint", "C11", "07-unshaded.gdshader", "godot-shaders/ls-c11-unshaded.mp4",
    "Godot 4.7.2 · render_mode unshaded on the right bulb · scripted",
    [(T("B17", 1), [2])],
    "Code card at left (shader_type and render_mode unshaded; two lines); at right a real Godot window: two pale bulb discs on the dusk floor, both dull. At 'unshaded' the right one lights up to its own bright yellow while the left stays dim. Labels 'shaded' and 'unshaded'. Caption: 'unshaded: ignores lights and the ambient tint'.",
    "The right bulb jumps to full brightness the moment unshaded is added; the left one stays dim.",
    [(T("B17", 1), "render_mode line highlighted"), (TW("B17", 1, 3), "right bulb: full brightness"), (T("B17", 2), "'the lamp's own bulb'")],
    "manim: two swatches", "A bright bulb beside a dim one on the same dusk floor shows the whole effect at a glance.",
    "Capture C11; docs render modes; verify4 R (unshaded: surface colour in every case), verify8 C11",
    readouts=[(0.2, "shaded", 0.365, 0.38), (TW("B17", 1, 3), "unshaded", 0.635, 0.38)], caption="unshaded: ignores lights and the ambient tint")

rem("B18", "what the three-line copy misses", "LectureEvidenceTable",
    {"title": "What the three-line copy misses", "headers": ["Scene", "Pixels that differ"],
     "rows": [["Shadows from an occluder", "0 of 57,600"], ["A normal map: the copy", "51,197 of 57,600"], ["A normal map: the docs' version", "0 of 57,600"]],
     "note": "normal map: an image of the direction each pixel faces · Forward+", "cues": [F("B18", T("B18", 1)), F("B18", T("B18", 2, 0.2)), F("B18", T("B18", 3, 1.5))], "durationSeconds": "__AUDIO__"},
    "A three-row table of measured pixel counts, each row ringed as the voice reaches it. The table note defines the word: 'normal map: an image of the direction each pixel faces · Forward+'. The counts are pixels that differ by more than one step in 255, from 320 x 180 test scenes (FACTCHECK rows 38 to 41).",
    "The ring steps down the three rows with the voice.",
    [(T("B18", 1), "shadow row"), (T("B18", 2, 0.2), "normal map: the copy"), (T("B18", 3, 1.5), "normal map: the docs' version")],
    "manim: two renders side by side", "Three measured counts are exactly what the table component is for; the picture of a normal map would need an art asset.",
    "verify9 A2, A3, A4; docs CanvasItem shaders (light example with NORMAL)")

# ═════════════════════════════ ACT III · Which Way Is the Light? ═════════════════════════════
manim("B19", "LIGHT_DIRECTION: an arrow from the pixel toward the lamp", "Arrows",
      "Act title 'Which Way Is the Light?' (serif 40) top-left. A lamp dot in the middle of a pixel-grid field; eight pixel dots on a ring around it; from each pixel dot a short arrow of the same length points at the lamp. Labels 'LIGHT_DIRECTION' and 'length 1'. The dot left of the lamp has its arrow pointing right, the dot above has its arrow pointing down, each ringed in turn. Caption: 'vector: a bundle of two to four numbers'.",
      "An arrow sprouts from every pixel dot and every one of them aims at the lamp.",
      [(0.4, "act title, lamp, pixel dots"), (TW("B19", 1, 6), "arrows sprout from all eight"), (T("B19", 2), "left dot: arrow points right"), (T("B19", 3), "top dot: arrow points down")],
      "ShaderLab colour wheel", "Arrows from many pixels converging on one lamp is the definition itself; the colour wheel would hide which way they point.",
      "verify2 D (E pixel (-1, 0, 0); N pixel (0, +1, 0); S pixel (0, -1, 0); length one)")

cap("C12", "B20", "Dusk tiled floor, one warm lamp (scale 5). Default glow first; at 'Multiply the lamp by it' the floor switches to 08-direction-ramp.",
    "share of the lamp left at 300 px: left 1.00, right 0.00, above 0.49, below 0.50, up-left steep 0.70 (verify8 C12).",
    ambient="dusk", lamp_bulbs=True, lamps=[lamp(5.0)],
    shader=[{"node": "floor", "file": "08-direction-ramp.gdshader", "at": T("B20", 2)}])
lab("B20", "use the arrow's x number as brightness", "C12", "08-direction-ramp.gdshader", "godot-shaders/ls-c12-direction-brightness.mp4", "Godot 4.7.2 · direction used as brightness · scripted",
    [(T("B20", 1), [4]), (T("B20", 2), [5, 6])],
    "Code card at left (the across line, the rgb line that multiplies by it); at right a real Godot window: the smooth glow becomes a lamp that is strongest on its left and fades to nothing on its right. Labels 'full' (left of the lamp) and 'none' (right of it).",
    "The glow slides to the left half of the lamp, fading smoothly toward the right.",
    [(T("B20", 1), "across line highlighted"), (T("B20", 2), "lamp multiplied by it"), (T("B20", 3), "left: full"), (T("B20", 4), "right: none")],
    "manim: a grey ramp strip", "The number used as brightness on the real lamp is the picture of 'painting a number'.",
    "Capture C12; verify8 C12",
    readouts=[(T("B20", 3), "full", 0.30, 0.50), (T("B20", 4), "none", 0.70, 0.50)])

cap("C13", "B21", "Dusk tiled floor, one warm lamp (scale 5). Starts on 08-direction-ramp (the previous beat's picture); at 'multiply the light by the result' the floor switches to 09-half-light.",
    "share of the lamp at 300 px: left 1, right 0, above 0, below 0, up-left steep 1 (verify8 C13).",
    ambient="dusk", lamp_bulbs=True, lamps=[lamp(5.0)],
    shader=[{"node": "floor", "file": "08-direction-ramp.gdshader", "at": 0}, {"node": "floor", "file": "09-half-light.gdshader", "at": T("B21", 2, 3.4)}])
lab("B21", "step turns the number into a mask: half a lamp", "C13", "09-half-light.gdshader", "godot-shaders/ls-c13-half-light.mp4", "Godot 4.7.2 · ramp, then step · scripted",
    [(T("B21", 0, 0.6), [4], "step(edge, x): 0 below the edge, 1 from the edge up"), (T("B21", 2, 0.2), [4]), (T("B21", 2, 3.4), [5, 6])],
    "Code card at left (mask = step(0.0, LIGHT_DIRECTION.x), the rgb line, LIGHT); at right a real Godot window: the smooth left-to-right fade snaps into a sharp half lamp, the left half on and the right half dark, with a clean vertical edge through the lamp. The mask line carries the tag 'step(edge, x): 0 below the edge, 1 from the edge up'.",
    "The smooth fade snaps into a hard half the moment step is applied.",
    [(T("B21", 0, 0.6), "mask line highlighted"), (T("B21", 0, 0.6), "mask line tagged: what step does"), (T("B21", 2, 3.4), "the right half goes dark")],
    "manim: a ramp becoming a staircase", "Seeing the same lamp go from a fade to a hard half is the mask idea in one cut.",
    "Capture C13; docs step; verify5 M1, verify8 C13")

cap("C14", "B22", "Dusk tiled floor, one warm lamp (scale 5). Starts on 09-half-light; at 'both sides count' the floor switches to 10-bowtie-light.",
    "share of the lamp at 300 px: left 1, right 1, above 0, below 0, up-left steep 0 (verify8 C14).",
    ambient="dusk", lamp_bulbs=True, lamps=[lamp(5.0)],
    shader=[{"node": "floor", "file": "09-half-light.gdshader", "at": 0}, {"node": "floor", "file": "10-bowtie-light.gdshader", "at": TW("B22", 0, 5)}])
lab("B22", "abs and a high edge: two wedges", "C14", "10-bowtie-light.gdshader", "godot-shaders/ls-c14-bowtie.mp4", "Godot 4.7.2 · half lamp, then abs · scripted",
    [(T("B22", 0, 0.5), [4], "abs(x): drops the minus sign: -0.3 becomes 0.3"), (T("B22", 1), [4])],
    "Code card at left (mask = step(0.9, abs(LIGHT_DIRECTION.x)), the rgb line, LIGHT); at right a real Godot window: the half lamp becomes a bow-tie, one wedge pointing left and one pointing right, dark above and below.",
    "The half lamp splits into two opposite wedges.",
    [(T("B22", 0, 0.5), "mask line highlighted"), (TW("B22", 0, 5), "half lamp becomes a bow-tie"), (T("B22", 2), "a wedge on each side")],
    "manim: two cones", "Two real wedges around a real lamp, one cut after the half lamp, show what abs adds.",
    "Capture C14; verify5 M2, verify8 C14")

manim("B23", "a directional light: the same arrow everywhere", "Sun",
      "Two panels. Left: a lamp with five pixel dots, each with its own arrow toward the lamp (five different directions). Right: a sun disc with the same five pixel dots, every arrow identical and pointing up toward the sun. Captions: 'point light: a different arrow per pixel', 'directional light: the same arrow everywhere'. Grey note: 'its position is always (0, 0, 0) · Godot docs'.",
      "On the left the five arrows differ; on the right they appear one after another and all match.",
      [(0.4, "two panels"), (T("B23", 1), "right-hand arrows all identical"), (TW("B23", 1, 11), "position note"), (T("B23", 2), "masks light everything or nothing: label")],
      "ShaderLab", "Five different arrows beside five identical ones is the contrast itself.",
      "verify2 Q, Q2; verify5 D (rotation 0, 90, -90: all or nothing); docs: LIGHT_POSITION is always (0, 0, 0) for a DirectionalLight2D")

# ═════════════════════════════ ACT IV · A Lighthouse ═════════════════════════════
manim("B24", "an arrow of your own: cos and sin of an angle", "AimArrow",
      "Act title 'A Lighthouse' (serif 40) top-left. A unit circle drawn in screen orientation (the vertical axis points DOWN, labelled 'y points down'); an arrow from the centre to the circle at angle a, labelled '(cos a, sin a)'; its horizontal and vertical grey projections shown as segments whose lengths change as the arrow turns clockwise through a quarter turn; the angle drawn as a small arc.",
      "The arrow turns clockwise around the circle while its two projections lengthen and shorten.",
      [(0.4, "act title and unit circle"), (T("B24", 1), "arrow and its cos and sin projections"), (T("B24", 2), "the arrow turns clockwise")],
      "plot of sine and cosine curves", "The unit arrow turning is the object the next beats rotate; the projections show where cos and sin come from.",
      "math identity (cos^2 + sin^2 = 1); verify5 L (aim 0, 45, 90, 180, 270 degrees light the matching wedge, clockwise from +x)")

manim("B25", "dot product: how much two arrows agree", "Agree",
      "Two arrows from one point: a grey 'pixel arrow' fixed at 25 degrees clockwise from right, and an ink 'aim' arrow with a terracotta tip dot that sweeps from -40 to 90 degrees. A two-line caption 'dot(a, b): multiply the matching parts and add them; with a unit direction, how far a point lies along it'. A live number 'dot = 0.97' beside a horizontal bar from -1 to 1 with a marker and a tick at 0.95. The sector between the two arrows lights up, labelled 'kept', whenever the number passes the tick.",
      "The aim arrow sweeps and the live number rises to one as the arrows line up, crossing the 0.95 tick.",
      [(0.4, "two arrows and the bar"), (T("B25", 1), "sweep: the number rises and falls"), (T("B25", 2), "the 0.95 tick: 'kept'")],
      "LectureEvidenceTable of three dot values", "A live number that peaks when two arrows agree is the dot product; a table of three values would be static.",
      "docs: dot(a, b); math; verify5 L (step 0.95 keeps +-18.2 degrees)")

cap("C15", "B26", "Dusk tiled floor, one warm lamp (scale 7: reach 896 px) at the centre, blob at lower right. 11-lighthouse is on the floor from 0.5 s and runs on TIME; the beam turns clockwise from the +x axis at one radian per second.",
    "wedge span on a 300 px ring = 36 degrees (expected 36.4 for a 0.95 cutoff); the wedge centre equals TIME in radians, clockwise from +x (verify5 T, verify8 C15).",
    ambient="dusk", lamp_bulbs=True, props=[BLOB], lamps=[lamp(7.0)],
    shader=[{"node": "floor", "file": "11-lighthouse.gdshader", "at": 0.5}])
lab("B26", "the lighthouse", "C15", "11-lighthouse.gdshader", "godot-shaders/ls-c15-lighthouse.mp4", "Godot 4.7.2 · live clock · clockwise on screen",
    [(0.5, [4]), (T("B26", 2), [5], "dot(a, b): multiply the matching parts and add them"), (T("B26", 3), [4])],
    "Code card at left (aim from cos and sin of TIME, agree = dot(-LIGHT_DIRECTION.xy, aim), the step, the rgb line, LIGHT); at right a real Godot window: a hard-edged beam turning clockwise round the lamp with the blob beside it. Caption: 'TIME: seconds on one clock shared by the whole game'. The dot line carries the tag 'dot(a, b): multiply the matching parts and add them'.",
    "The wedge turns round the lamp, clockwise, while the code lines light up in turn.",
    [(0.5, "aim line highlighted; the beam turns"), (T("B26", 2), "the minus sign highlighted"), (T("B26", 3), "clockwise: y points down")],
    "manim: a wedge turning on a circle", "This is the film's first payoff, and the real beam beside the real code is the proof.",
    "Capture C15; verify5 L, T; verify8 C15", caption="TIME: seconds on one clock shared by the whole game",
    readouts=[(T("B26", 3), "clockwise", 0.83, 0.07)])

cap("C16", "B27", "Dusk tiled floor, one warm lamp (scale 7), blob. 12-lighthouse-width on the floor; the cutoff uniform holds 0.95, eases down to 0.7 at 'Lower the cutoff', then up to 0.99 at 'Raise it'.",
    "wedge span on a 300 px ring: 17, 37, 52, 74, 92 degrees for cutoff 0.99, 0.95, 0.9, 0.8, 0.7 (expected 16.2, 36.4, 51.7, 73.7, 91.1) (verify8 C16).",
    ambient="dusk", lamp_bulbs=True, props=[BLOB], lamps=[lamp(7.0)],
    shader=[{"node": "floor", "file": "12-lighthouse-width.gdshader", "at": 0, "uniforms": {"cutoff": 0.95}}],
    uniform_sweeps=[{"node": "floor", "name": "cutoff", "from": 0.95, "to": 0.7, "t0": T("B27", 1), "t1": T("B27", 1, 2.0), "ease": "smooth"},
                    {"node": "floor", "name": "cutoff", "from": 0.7, "to": 0.99, "t0": T("B27", 2), "t1": T("B27", 2, 1.9), "ease": "smooth"}])
lab("B27", "make the cutoff a uniform: the beam's width is a setting", "C16", "12-lighthouse-width.gdshader", "godot-shaders/ls-c16-cutoff.mp4", "Godot 4.7.2 · cutoff swept by script · scripted",
    [(0.3, [3]), (T("B27", 1), [8])],
    "Code card at left (the uniform line at the top, the step line using it); at right a real Godot window: the beam turning round the lamp gets wider as the cutoff is lowered and narrower as it is raised. Readouts 'cutoff 0.95', 'cutoff 0.7', 'cutoff 0.99'. Caption: 'uniform: a value your game sets from outside; every pixel sees the same one'.",
    "The beam widens and then narrows as the dial moves.",
    [(0.3, "uniform line highlighted"), (T("B27", 1), "lower: the beam widens"), (T("B27", 2), "raise: the beam narrows")],
    "manim: a dial next to a wedge", "A dial moving while a real beam widens shows exactly what a uniform is for.",
    "Capture C16; docs uniforms; verify8 C16",
    readouts=[(0.3, "cutoff 0.95", 0.17, 0.90), (T("B27", 1, 2.0), "cutoff 0.7", 0.17, 0.94), (T("B27", 2, 1.9), "cutoff 0.99", 0.17, 0.98)],
    caption="uniform: a value your game sets from outside; every pixel sees the same one")

cap("C17", "B28", "Dusk tiled floor, one warm lamp (scale 7), blob. The beam starts on 11-lighthouse (hard edge); at 'the edge of the beam goes soft' the floor switches to 13-lighthouse-soft. Both run on TIME, so the beam keeps its angle across the switch.",
    "hard: lit out to +-18.2 degrees, nothing beyond; soft: smoothstep 0.9 to 0.99 fades between 8 and 26 degrees (verify7 D masks 1.0, 1.0, 0.98, 0.8, 0.61, 0.44, 0.02, 0.0 at 0, 5, 10, 15, 18, 20, 25, 30 degrees).",
    ambient="dusk", lamp_bulbs=True, props=[BLOB], lamps=[lamp(7.0)],
    shader=[{"node": "floor", "file": "11-lighthouse.gdshader", "at": 0}, {"node": "floor", "file": "13-lighthouse-soft.gdshader", "at": TW("B28", 0, 15)}])
lab("B28", "smoothstep: a soft beam edge", "C17", "13-lighthouse-soft.gdshader", "godot-shaders/ls-c17-soft-edge.mp4", "Godot 4.7.2 · step, then smoothstep · scripted",
    [(0.3, [8], "smoothstep(a, b, x): a smooth ramp from a to b"), (TW("B28", 0, 15), [8])],
    "Code card at left (the smoothstep line); at right a real Godot window: a hard-edged beam turns, then at 'goes soft' its edge feathers while it keeps turning at the same angle. Labels 'step' then 'smooth step'; the code line carries the tag 'smoothstep(a, b, x): a smooth ramp from a to b'.",
    "The beam's sharp edge feathers while the beam keeps turning.",
    [(0.3, "smoothstep line highlighted"), (TW("B28", 0, 15), "the edge goes soft"), (T("B28", 1), "same lamp, same beam")],
    "manim: a step curve and a smoothstep curve", "The same beam before and after is the clearest picture of a soft edge.",
    "Capture C17; docs smoothstep; verify7 D",
    readouts=[(0.2, "step", 0.17, 0.07), (TW("B28", 0, 15), "smooth step", 0.83, 0.07)])

cap("C18", "B29", "Dusk tiled floor, no blob. One warm lamp (scale 5) at (560, 540) with 13-lighthouse-soft on the floor; a second, cool lamp (colour 0.6, 0.85, 1.0, scale 5) at (1360, 540) appears at 'second lamp'.",
    "strongest added colour on a 150 px ring: warm lamp (0.565, 0.533, 0.329), cool lamp (0.369, 0.506, 0.482) (verify8 C18); beams are parallel because both lamps aim at the same TIME angle.",
    ambient="dusk", lamp_bulbs=True,
    lamps=[lamp(5.0, x=560, y=540), lamp(5.0, x=1360, y=540, color=[0.6, 0.85, 1.0], appear=TW("B29", 0, 2) + 0.4)],
    shader=[{"node": "floor", "file": "13-lighthouse-soft.gdshader", "at": 0}])
lab("B29", "a second lamp: the same function, its own arrows", "C18", "13-lighthouse-soft.gdshader", "godot-shaders/ls-c18-two-lamps.mp4", "Godot 4.7.2 · a second lamp added · scripted",
    [(0.3, [9]), (T("B29", 1), [9, 10])],
    "Code card at left (the soft lighthouse, unchanged); at right a real Godot window: one warm lamp with its beam, then a second cool lamp appears and a second beam starts from it, each in its own color. Labels 'lamp 1', 'lamp 2'.",
    "A second beam, in the second lamp's color, starts from the second lamp the moment it appears.",
    [(0.3, "one lamp, one beam"), (TW("B29", 0, 2) + 0.4, "second lamp: second beam"), (T("B29", 1), "each beam in its lamp's color")],
    "manim: two lamps and one function", "Two real beams in two colors from one unchanged code card prove the function runs again for each lamp.",
    "Capture C18; verify5 TL; verify8 C18",
    readouts=[(0.3, "lamp 1", 0.20, 0.70), (TW("B29", 0, 2) + 0.4, "lamp 2", 0.62, 0.70)])

cap("C19", "B30", "Dusk tiled floor. One warm lamp (scale 2.5: reach 320 px) with 13-lighthouse-soft; a thin grey square outlines the lamp's texture; from 'scale the lamp' the lamp's scale eases from 2.5 up to 7 and the outline grows with it.",
    "with alpha forced to one the lit square ends exactly at the texture's half-width: added red 0.565 at 300 and 315 px, 0.0 at 325 and 340 px for half-width 320 (verify8 C19).",
    ambient="dusk", lamp_bulbs=True, outline_lamp=0, props=[{"kind": "outline", "name": "outline"}],
    lamps=[{"x": 960, "y": 540, "scale": 2.5, "energy": 1.0, "color": "warm", "sweeps": [{"prop": "scale", "from": 2.5, "to": 7.0, "t0": TW("B30", 2, 4), "t1": TW("B30", 2, 4) + 2.8, "ease": "smooth"}]}],
    shader=[{"node": "floor", "file": "13-lighthouse-soft.gdshader", "at": 0}])
lab("B30", "a beam exists only where a lamp reaches", "C19", None, "godot-shaders/ls-c19-reach.mp4", "Godot 4.7.2 · lamp scale changed · scripted", [],
    "A real Godot window, result only: the turning beam stops at a thin grey square marking the lamp's texture; outside the square nothing is lit. At 'scale the lamp' the square and the beam grow together. Labels 'lamp reach', 'no light() here', 'scale'.",
    "The beam is cut off at the square; when the lamp is scaled up the square and the beam grow together.",
    [(T("B30", 0, 0.5), "the beam stops at the lamp's square"), (T("B30", 1), "outside: no light() runs"), (TW("B30", 2, 4), "scale the lamp: the beam lengthens")],
    "manim: a square with a wedge", "A real beam clipped by a real square, then growing with the lamp, is the whole caution.",
    "Capture C19; verify5 TL (outside the lamp squares nothing is lit); verify8 C19", layout="video",
    readouts=[(T("B30", 0, 0.5), "lamp reach", 0.5, 0.20), (T("B30", 1), "no light() here", 0.88, 0.50), (TW("B30", 2, 4), "scale", 0.17, 0.07)])

# ═════════════════════════════ ACT V · Where Is the Light? ═════════════════════════════
manim("B31", "LIGHT_POSITION and LIGHT_VERTEX in screen space", "ScreenSpace",
      "Act title 'Where Is the Light?' (serif 40) top-left. A 16:9 rectangle (the window) with an origin dot at its top-left labelled (0, 0); an x arrow along the top pointing right and a y arrow down the left side pointing DOWN. A lamp dot at (960, 540) labelled LIGHT_POSITION and a pixel dot at (1130, 640) labelled LIGHT_VERTEX, each with its coordinates. Caption: 'screen space: pixels of the window, from the top left'. Small grey: 'window 1920 x 1080'.",
      "The two dots appear one after the other and their coordinates count up from the corner.",
      [(0.4, "window, origin, axes"), (TW("B31", 1, 0), "lamp dot: LIGHT_POSITION"), (TW("B31", 1, 9), "pixel dot: LIGHT_VERTEX"), (T("B31", 2), "caption: screen space")],
      "ShaderLab readouts over a capture", "Coordinates measured from a corner need the corner and the axes drawn; a capture would hide them.",
      "verify2 P, V; verify6 X (position exact; vertex = pixel centre, x + 0.5)")

manim("B32", "pixel minus lamp: an arrow, and its length", "Subtract",
      "The same window frame. A lamp dot at (960, 540) and a pixel dot at (1130, 640). An arrow grows from the lamp dot to the pixel dot (terracotta dot at its tip), labelled 'pixel - lamp'; a brace along it counts up to 'length 197 px'. Under it in grey: '(170, 100)'. Caption: 'length(v): the length of a vector; of an offset, the distance'.",
      "The arrow grows from the lamp to the pixel while the brace counts the distance up to 197.",
      [(0.4, "lamp and pixel dots"), (T("B32", 0, 0.6), "arrow grows: pixel - lamp"), (T("B32", 1), "brace: length 197 px")],
      "ShaderLab", "Subtracting two positions is an arrow, and the arrow's length is a distance; the drawing shows both.",
      "sqrt(170^2 + 100^2) = 197.2; verify6 DM, G")

cap("C20", "B33", "Dusk tiled floor, one warm lamp (scale 4: a 1024 px square texture). 14-distance-map on the floor from the start.",
    "added red at 250 px = 0.247 and at 500 px = 0.498 (d / 1000); at the lamp 0 (verify8 C20).",
    ambient="dusk", lamp_bulbs=True, lamps=[lamp(4.0)], shader=[{"node": "floor", "file": "14-distance-map.gdshader", "at": 0}])
lab("B33", "distance as brightness", "C20", "14-distance-map.gdshader", "godot-shaders/ls-c20-distance.mp4", "Godot 4.7.2 · distance painted as brightness",
    [(0.3, [5]), (T("B33", 1), [4], "length: the length of a vector; of an offset, the distance")],
    "Code card at left (d = length(LIGHT_VERTEX.xy - LIGHT_POSITION.xy), then LIGHT = vec4(vec3(d / 1000.0), 1.0)); at right a real Godot window: nothing added at the lamp and more and more brightness with every step away, filling the lamp's square. A thin ramp under the window with a marker travelling from 0 to 0.5.",
    "The brightness grows outward from the lamp; the marker travels along the ramp.",
    [(0.3, "LIGHT line highlighted"), (T("B33", 1), "distance line highlighted; the marker moves"), (T("B33", 2), "every pixel knows its distance")],
    "manim: a distance ruler", "A real gradient centred on the lamp shows the distance map; the ramp under it ties the brightness to the number.",
    "Capture C20; verify6 DM; verify8 C20", ramp=(T("B33", 1), 0.0, 0.5))

manim("B34", "step splits the ground; two steps subtracted make a ring", "RingFromSteps",
      "A lamp dot at the centre. Two outlined circles centred on it, radius 390 and radius 450, with chips 'step(390, d)' and 'step(450, d)'. The ground outside the small circle fills pale grey ('inside / outside'), then the ground outside the large circle is subtracted from it, and the band between the two circles is left: a ring. Labels 'radius 390', 'radius 450', 'a ring'. Caption: 'step(edge, x): 0 below the edge, 1 from the edge up'.",
      "The outside of the big circle is subtracted from the outside of the small one and a ring remains.",
      [(0.4, "lamp and the two circles"), (TW("B34", 0, 10), "ground splits in two: inside and outside"), (T("B34", 1, 1.0), "the second fill is subtracted"), (T("B34", 1, 4.6), "the band between: a ring")],
      "ShaderLab ring capture", "Subtracting one outside from another leaves the band between; seeing the band appear is the idea.",
      "verify6 G; verify8 C21 (ring lit where 390 <= d < 450)")

cap("C21", "B35", "Still frame: dusk tiled floor, one warm lamp (scale 7), blob; 15-ring-light at its defaults (radius 450, thickness 60). One PNG at t = 0.5 s.",
    "lit at 395, 440, 445 px from the lamp; unlit at 370, 380, 455, 470 px (verify8 C21).",
    still=True, seconds=1, ambient="dusk", lamp_bulbs=True, props=[BLOB], lamps=[lamp(7.0)],
    shader=[{"node": "floor", "file": "15-ring-light.gdshader", "at": 0}])
lab("B35", "the ring shader, still", "C21", "15-ring-light.gdshader", "godot-shaders/ls-c21-ring.png", "Godot 4.7.2 · Forward+ · 1920 × 1080",
    [(0.3, [7, 8]), (T("B35", 0, 3.5), [9, 10]), (T("B35", 1), [3, 4])],
    "Code card at left (two uniforms, the distance, the two steps, the rgb line); at right a real Godot window (a still): a ring of light round the lamp on the dusk floor. Labels 'radius 450' and 'thickness 60'.",
    "Highlight steps from the distance and steps to the two uniform lines while the ring stays still.",
    [(0.3, "distance and ring lines highlighted"), (T("B35", 1), "uniform lines highlighted")],
    "LectureCodeTrace alone", "The whole shader fits on screen with its result; a still is enough because the next beat animates it.",
    "Capture C21; verify8 C21",
    readouts=[(T("B35", 0, 3.5), "radius 450", 0.80, 0.50), (T("B35", 1), "thickness 60", 0.50, 0.035)])

GD_RING = ('$Floor.material.set_shader_parameter("radius", 0.0)\n'
           'var tween := create_tween()\n'
           'tween.tween_property($Floor.material, "shader_parameter/radius", 880.0, 3.0)')
cap("C22", "B36", "Dusk tiled floor, one warm lamp (scale 7: reach 896 px), blob. 15-ring-light with radius set to 0; the radius ramps 0 to 880 over 3 s (a linear tween) at 'then tween it out', and once more over 3 s as the last sentence begins.",
    "at 1, 2 and 3 s of a real tween the radius reads 298, 594, 880 and the ring's outer edge follows it (verify9 C); a tween on a uniform never set from code fails (verify9 C2).",
    ambient="dusk", lamp_bulbs=True, props=[BLOB], lamps=[lamp(7.0)],
    shader=[{"node": "floor", "file": "15-ring-light.gdshader", "at": 0, "uniforms": {"radius": 0.0, "thickness": 60.0}}],
    uniform_sweeps=[{"node": "floor", "name": "radius", "from": 0.0, "to": 880.0, "t0": TW("B36", 2, 7), "t1": TW("B36", 2, 7) + 3.0},
                    {"node": "floor", "name": "radius", "from": 0.0, "to": 880.0, "t0": T("B36", 3, -1.0), "t1": T("B36", 3, -1.0) + 3.0}])
lab("B36", "the game drives the radius with a tween", "C22", None, "godot-shaders/ls-c22-ring-expands.mp4", "Godot 4.7.2 · scripted run (a tween, not player input)",
    [(T("B36", 2), [1]), (TW("B36", 2, 7), [2, 3])],
    "A three-line GDScript card at left (set the radius to zero, create a tween, tween the property to 880 over 3 seconds); at right a real Godot window: nothing at first, then a ring spreads from the lamp, thinning as it nears the lamp's edge, then does it again. A label 'scripted run' is always on screen. Caption: 'tween: Godot's way to change a value smoothly over time from GDScript'.",
    "The ring spreads out from the lamp as the tween runs.",
    [(T("B36", 2), "first code line: the radius set to zero"), (TW("B36", 2, 7), "tween lines: the ring spreads"), (T("B36", 3, -1.0), "the ring spreads again: scripted run")],
    "ShaderLab with the earlier still", "Cause (the tween lines) and effect (the spreading ring) together; the label keeps the input honest.",
    "Capture C22; verify9 C, C2; docs Tween (default linear)", code=GD_RING, code_file="scene script (GDScript)",
    readouts=[(0.05, "scripted run", 0.5, 0.05)], caption="tween: Godot's way to change a value smoothly over time from GDScript")

cap("C23", "B37", "Dusk tiled floor, one warm lamp (scale 7), blob; 15-ring-light at its defaults. At 'Zoom the camera in' a Camera2D zooms from 1 to 2 (smooth) over three seconds and stays at 2.",
    "the ring is lit at the same screen pixels (395 and 440 px lit; 380 and 455 unlit) at zoom 1 and at zoom 2 (verify6 Z, verify8 C23); the floor tiles, bulb and blob double in size.",
    ambient="dusk", lamp_bulbs=True, props=[BLOB], lamps=[lamp(7.0)],
    shader=[{"node": "floor", "file": "15-ring-light.gdshader", "at": 0}],
    zoom={"from": 1.0, "to": 2.0, "t0": T("B37", 2, 1.0), "t1": T("B37", 2, 4.0)})
lab("B37", "screen-space numbers are window pixels: zoom does not move the ring", "C23", "15-ring-light.gdshader", "godot-shaders/ls-c23-zoom.mp4", "Godot 4.7.2 · camera zoom 1 to 2 · scripted",
    [(0.3, [7, 8])],
    "Code card at left (the ring shader, unchanged); at right a real Godot window: the ring of 450 px round the lamp; the camera zooms in, the tiles, bulb and blob double in size, but the ring does not change size. Readouts 'ring 450 px', 'zoom 1', then 'zoom 2'.",
    "The world doubles around a ring that stays exactly the same size.",
    [(0.3, "ring and code"), (T("B37", 2, 1.0), "zoom in: the ground doubles"), (T("B37", 2, 6.0), "the ring is still 450 px")],
    "manim: a ruler against a zooming grid", "A real zoom with a ring that does not follow it is the warning, in one picture.",
    "Capture C23; verify6 Z, SV; verify8 C23",
    readouts=[(0.1, "ring 450 px", 0.80, 0.50), (0.1, "zoom 1", 0.17, 0.07), (T("B37", 2, 4.2), "zoom 2", 0.17, 0.14)])

cap("C24", "B38", "Dusk tiled floor (2,520 px wide so it can slide), one warm lamp (scale 5). Default glow first; at 'you get stripes' the floor switches to 16-stripes-light; during the last sentence the floor slides 250 px right, then 500 px left.",
    "160 lit columns (ten stripes of 16 px, 384 to 399, 512 to 527 ...) at t = 0.5 s and at t = 6 s with the floor moved: identical (verify8 C24).",
    ambient="dusk", lamp_bulbs=True, floor_extra=300, lamps=[lamp(5.0)],
    shader=[{"node": "floor", "file": "16-stripes-light.gdshader", "at": TW("B38", 2, 12)}],
    moves=[{"node": "floor", "x0": 0, "x1": 250, "y0": 0, "y1": 0, "t0": T("B38", 3, 0.7), "t1": T("B38", 3, 2.7), "ease": "smooth"},
           {"node": "floor", "x0": 250, "x1": -250, "y0": 0, "y1": 0, "t0": T("B38", 3, 2.9), "t1": T("B38", 3, 5.4), "ease": "smooth"}])
lab("B38", "mod: stripes that belong to the screen", "C24", "16-stripes-light.gdshader", "godot-shaders/ls-c24-stripes.mp4", "Godot 4.7.2 · floor slid by script · scripted",
    [(T("B38", 2), [4], "mod(x, y): the remainder after dividing x by y"), (T("B38", 3), [4])],
    "Code card at left (the stripe line with mod and step, the rgb line, LIGHT); at right a real Godot window: vertical stripes of light inside the lamp's reach; the tiled floor slides left and right underneath while the stripes stay exactly where they are. The stripe line carries the tag 'mod(x, y): the remainder after dividing x by y'. Label 'stripes stay'.",
    "The tiles slide under stripes that do not move.",
    [(T("B38", 2), "stripe line highlighted"), (TW("B38", 2, 12), "stripes appear"), (T("B38", 3, 0.7), "the floor slides; the stripes stay")],
    "manim: a number line wrapping round", "A real floor sliding under fixed stripes proves they belong to the screen.",
    "Capture C24; docs mod; verify6 MOD; verify8 C24",
    readouts=[(T("B38", 3, 1.0), "stripes stay", 0.83, 0.07)])

cap("C25", "B39", "Dusk tiled floor, one warm lamp (scale 5). Starts on 16-stripes-light; at 'Do the same for y' the floor switches to 17-grid-light.",
    "horizontal line runs at x = 1000: y 384 to 399, 512 to 527, 640 to 655, 768 to 783; lines 16 px wide every 128 px, anchored to the screen (verify8 C25).",
    ambient="dusk", lamp_bulbs=True, lamps=[lamp(5.0)],
    shader=[{"node": "floor", "file": "16-stripes-light.gdshader", "at": 0}, {"node": "floor", "file": "17-grid-light.gdshader", "at": TW("B39", 0, 4)}])
lab("B39", "stripes in both directions: a grid", "C25", "17-grid-light.gdshader", "godot-shaders/ls-c25-grid.mp4", "Godot 4.7.2 · stripes, then a grid · scripted",
    [(0.3, [4, 5]), (T("B39", 1), [5], "max(a, b): the larger of the two")],
    "Code card at left (cell = mod(LIGHT_VERTEX.xy, 128.0), lines = max of two steps, the rgb line, LIGHT); at right a real Godot window: the vertical stripes gain horizontal lines and become a grid of light inside the lamp's reach.",
    "Horizontal lines join the stripes and make a grid.",
    [(0.3, "cell and lines highlighted"), (TW("B39", 0, 4), "horizontal lines appear"), (T("B39", 1), "a grid, only where the lamp reaches")],
    "manim: two number lines crossing", "Lines appearing across the stripes show exactly what max adds.",
    "Capture C25; verify8 C25")

rem("B40", "where each job belongs", "LectureEvidenceTable",
    {"title": "Where each job belongs", "headers": ["The effect depends on", "Write it in"],
     "rows": [["a lamp: its direction, distance or color", "light()"], ["the surface alone: a pattern, a gradient", "fragment()"], ["the shape's corners: a lean, a wobble", "vertex()"]],
     "note": "A rule of thumb from this film's runs · Godot 4.7 shader reference", "cues": [F("B40", T("B40", 1)), F("B40", T("B40", 2, 0.2)), F("B40", TW("B40", 2, 9))], "durationSeconds": "__AUDIO__"},
    "A three-row table, one row ringed as each kind of effect is named.", "The ring steps down the rows with the voice.",
    [(T("B40", 1), "a lamp: light()"), (T("B40", 2, 0.2), "the surface alone: fragment()"), (TW("B40", 2, 9), "the corners: vertex()")],
    "manim", "A short decision aid is the right shape for a table, and the film has just shown each case.",
    "design advice (EXEMPT); verify1 to verify9 for the cases")

# ═════════════════════════════ write lanes, captures.json, SHOTLIST.md, CAPTURE-PLAN.md ═════════════════════════════
order = [b for b, _, _ in N.BODY]
assert [e["bid"] for e in sorted(E, key=lambda e: order.index(e["bid"]))] == order, "every body beat needs exactly one lane entry"
E.sort(key=lambda e: order.index(e["bid"]))

(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(len(N.ACTS)):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

EV.mkdir(parents=True, exist_ok=True)
(EV / "captures.json").write_text(json.dumps({k: v["cfg"] for k, v in CAPS.items()}, indent=1, ensure_ascii=False) + "\n")

hist = {}
for e in E:
    hist[e["entry"]["lane"]] = hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
sl = ["# Shot list: Light Shaders\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a capture of a scene in `evidence/planning-checks/light_scene.gd` (data: `captures.json`) running a tested file in `lab-shaders/`; there is no editor frame. Six things must exist before the build (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`; shared with every shader film). 2. **`shader_kit.py`** Manim helpers (same file). "
      "3. **Film-local Manim helpers** in the scene file: `lamp_dot`, `unit_arrow(from, to)`, `swatch(value)`, `window_frame(w, h)` with an origin dot and a DOWN-pointing y axis. "
      "4. **Capture loop**: `evidence/planning-checks/record_capture.gd` (PNG sequence from `light_scene.gd`; see `CAPTURE-PLAN.md`), then ffmpeg to MP4 at 30 fps. "
      "5. **Docs screenshot** for B04 via Playwright (D1). 6. Nothing else: no editor action and no generated media.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")

# CAPTURE-PLAN.md
cp = ["# Capture plan: Light Shaders\n",
      "**What this is.** Every Godot render and screenshot the build session must record for this film: the scene, the shader file, what moves and when, the length, the renderer, and the result already verified. Nothing is recorded yet; every number below comes from planning runs in `evidence/planning-checks/`.\n",
      "**Why.** Films show only what was really done and recorded. This is the list of things to really do, written so a medium-effort session can do them without further judgment: all 25 scenes are one script (`light_scene.gd`) driven by one data file (`captures.json`).\n",
      f"**Found.** {len(CAPS)} Godot captures (24 clips and one still) and 1 docs screenshot; no editor frame and no interactive editor action. All shaders compile in the Lab and every probe below was read in a real Godot 4.7.2 window on Forward+ (Apple M4 Pro); Compatibility matched within one step of 255 on every comparison. One trap changes the series convention: **these captures are 1920 x 1080 at scale 1, not the 3x SubViewport route**, because screen-space numbers are physical pixels (below).\n",
      "## Conventions for every capture\n",
      "- **Resolution and scale.** 1920 x 1080 SubViewport at scale 1, no `size_2d_override`. `LIGHT_POSITION` and `LIGHT_VERTEX` are in physical pixels of the render target: measured (verify6 SV) with a 1920 x 1080 SubViewport over a 640 x 360 canvas, a ring of radius 150 sat at 150 physical pixels, not 450. The ring, distance, stripe and grid shaders hold pixel constants (450, 60, 880, 1000, 128, 16), so the 3x route would draw them three times too small. Show a capture in a ShaderLab window of about 1,900 px (1:1) and never upscale it more than 1.3x.",
      "- **Scene.** `evidence/planning-checks/light_scene.gd` builds each capture from `captures.json` (floor, lamps, props, shader switches, sweeps, zoom, moves). Every shader file is read from `lab-shaders/` (pass its absolute path). The cast is the same in every scene: dusk tiled floor (CanvasModulate 0.50, 0.55, 0.72), warm lamps with the docs' own radial texture, a pale bulb disc on each lamp, the teal blob.",
      "- **Loop.** `evidence/planning-checks/record_all.sh [ids]` records every capture (or the ids you name): for each it runs `record_capture.gd` (`godot --path <scratch copy of evidence/planning-checks> --fixed-fps 30 --script res://record_capture.gd -- <id> <frames> <out dir> <abs lab-shaders> <abs captures.json>`, one PNG per frame, the clock driven by hand so t is exactly frame / 30) and then ffmpeg (`-framerate 30 -c:v libx264 -pix_fmt yuv420p -crf 14`), writing into `/private/tmp/claude-501/ls-capture/out` and never into the film folder. Smoke-tested on 2026-10-13 with 12 frames of C05 (1920 x 1080, 30 fps) and the still C21. Frames = 30 x the length in the table. If the shared harness `lab/capture.gd` already exists when you build, its `--scene PATH.gd` option can drive `light_scene.gd` instead (the script exposes `setup(id, shaders, captures_path)`, `step(dt)` and `manual`; set `manual = true` and call `step(1.0 / 30.0)` once per frame). Offline and fixed-tick: it says nothing about real-time frame rate.",
      "- **Timing.** Every event time is estimated from the narration at 0.34 s per word (the script `_gen_lanes.py` computes them). After the audio is measured, if a beat differs from its estimate by more than one second, scale that capture's event times in `captures.json` by the ratio and re-record that capture. Do not edit the narration.",
      "- **Labels.** Every capture is labelled `Godot 4.7.2 · Forward+ · 1920 x 1080` plus what is scripted. Scripted switches, sweeps and zooms are not player input and are labelled so.",
      "- **Traps.** Dark art: the floor is a mid-tone dusk blue on purpose (GATE T); do not darken the CanvasModulate. Debug-style shaders add on top of the ambient, so they clip at white by design. The lamp bulb disc is `render_mode unshaded` so it stays bright. TIME-driven shaders (C01, C15 to C19, C10) use the engine clock, so their beam angle at a given second depends on how long the engine has run; that is cosmetic.",
      "- **Renderer.** Forward+ for the film. The same scenes were also run on Compatibility (`--rendering-method gl_compatibility`): every comparison agreed within one step of 255 (logs `*-compat.log`).\n",
      "## Godot captures\n",
      "| ID | Beat | Shader (in `lab-shaders/`) | Scene and timeline | Length | Verified result to reproduce |",
      "|---|---|---|---|---|---|"]
for cid, c in CAPS.items():
    shaders = sorted({s["file"] for s in c["cfg"].get("shader", [])})
    cp.append(f"| {cid} | {c['bid']} | {', '.join(f'`{s}`' for s in shaders) if shaders else 'none (default lighting)'} | {c['plan']} | {'one PNG' if c['cfg'].get('still') else str(c['cfg']['seconds']) + ' s'} | {c['verified']} |")
cp += ["",
       "## Screenshot\n",
       "| ID | Beat | What | How |", "|---|---|---|---|",
       "| D1 | B04 | The Godot 4.7 \"2D lights and shadows\" page, the Point lights section with the paragraph that begins \"If you need different falloff\", 1600 x 900 at device scale 2.4, from `https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html` | Playwright (BrowserCapture convention): scroll the paragraph to the middle of the viewport, then capture; caption with the capture date; set the two `moves` rings from the real positions of the paragraph and of \"opaque white to transparent white\" |",
       "",
       "## Editor frames\n",
       "None. This film needs no editor capture and no interactive editor action (the lights are shown as renders, and the recipe is shown from the docs page).\n",
       "## Not captured on purpose\n",
       "No GPU timing and no real-time frame-rate claim anywhere. No pixel probe is claimed for a TIME-driven frame except the beam width and the beam-centre equals TIME result (verify5, verify8). No capture shows the Godot editor."]
(HERE / "CAPTURE-PLAN.md").write_text("\n".join(cp) + "\n")
print(len(E), "beats;", hist, "; captures:", len(CAPS))
