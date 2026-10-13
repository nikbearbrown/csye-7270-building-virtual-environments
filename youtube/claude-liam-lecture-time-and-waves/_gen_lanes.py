#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text, the highlighted line numbers must be the real line numbers, cue times
must follow the spoken words, and the shot list must say exactly what the lanes say. Re-run after any edit to narration.py or a shader:
    python3 _gen_lanes.py && python3 make_sheet.py
Layout stage only. Once the build has started, do NOT re-run it: the B02 ring box below is a placeholder that the build replaces
with the box measured on the real docs screenshot, and a re-run would put the placeholder back. Edit lanes/*.json by hand from then on.
"""
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
spec = importlib.util.spec_from_file_location("narration", HERE / "narration.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
TEXT = {bid: t for bid, _, t in N.BODY}
ACT = {bid: a for bid, a, _ in N.BODY}
E = []          # entries in beat order


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def ln(fn, needle, nth=0):
    """1-based line number of the nth line of a shader file containing `needle`."""
    hits = [i + 1 for i, l in enumerate(code_of(fn).split("\n")) if needle in l]
    assert len(hits) > nth, f"{needle!r} not found in {fn}"
    return hits[nth]


def fix(f):
    """no cue may start inside the 45 to 55 percent window (GATE T and Gate V sample the midpoint)"""
    f = max(0.02, min(0.94, f))
    if 0.45 <= f <= 0.55:
        f = 0.43 if f < 0.5 else 0.57
    return round(f, 2)


def at(bid, phrase, lead=0.0, nth=0):
    """fraction of the beat at which `phrase` begins to be spoken (by word position), kept out of the midpoint window; nth=-1 takes the last match"""
    words = TEXT[bid].split()
    target = phrase.split()
    norm = lambda ws: [re.sub(r"[^\w']", "", w).lower() for w in ws]
    hits = [i for i in range(len(words) - len(target) + 1) if norm(words[i:i + len(target)]) == norm(target)]
    if not hits:
        raise ValueError(f"{phrase!r} not in {bid}")
    return fix(hits[nth] / len(words) + lead)


def add(bid, about, entry, evidence=""):
    E.append({"bid": bid, "act": ACT[bid], "about": about, "evidence": evidence, "entry": entry})


def manim(bid, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects and film-local helpers)"):
    add(bid, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                     "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, about, video, label, intent, motion, show, runner, why, spec, evidence, layout="side", code="", code_file="", cues=None,
        readouts=None, rings=None, ramp=None, title=None, caption="", lane="capture"):
    props = {"layout": layout, "code": code, "codeFile": code_file, "cues": cues or [], "video": video, "videoLabel": label,
             "readouts": readouts or [], "rings": rings or [], "caption": caption, "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    entry = {"lane": lane, "pattern": "ShaderLab", "props": props, "visual_intent": intent, "motion_claim": motion, "show": show,
             "runner_up": runner, "why": why, "sparse": False}
    if spec:
        entry["capture_spec"] = spec
    add(bid, about, entry, evidence)


def rem(bid, about, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                     "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


def shaderlab_code(bid, about, file, cues, intent, motion, show, runner, why, evidence, caption="", title=None):
    """ShaderLab with layout 'code': the real file text, paced line focus, no capture"""
    props = {"layout": "code", "code": code_of(file), "codeFile": f"lab-shaders/{file}", "cues": cues, "video": "", "videoLabel": "",
             "readouts": [], "rings": [], "caption": caption, "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    add(bid, about, {"lane": "remotion", "pattern": "ShaderLab", "props": props, "visual_intent": intent, "motion_claim": motion,
                     "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


V = "godot-shaders/time-and-waves/"        # where the captures land under runtime/remotion/public/
PULSE = "02-pulse.gdshader"
DIALS = "03-dials.gdshader"
SHAPES = "04-three-shapes.gdshader"
CURVE = "05-curve-loop.gdshader"
STRIPES = "06-stripes.gdshader"
TRAVEL = "07-travel.gdshader"
RINGS = "08-rings.gdshader"
RIPPLE = "09-ripple.gdshader"
FLAG = "10-flag.gdshader"
TWO = "11-two-waves.gdshader"
BREATH = "12-breath.gdshader"
BANNER = "13-banner.gdshader"
SCENES = "evidence/planning-checks/scene-project/scenes"

# ═════════════════════════════ ACT I · One Clock ═════════════════════════════
lab("B01", "a node added late joins in step: one global clock", V + "late-join.mp4",
    "Godot 4.7.2 · Forward+ · scripted run: the second square is added late",
    "Act title 'One Clock' (serif 40) top-left. A real Godot render in a framed window on the cream stage: two squares that pulse between teal and cream, the left one pulsing alone from the first frame, the right one added late. Labels 'from the start' under the left and 'added late' under the right. Caption: 'TIME · seconds on one clock shared by the whole game'.",
    "The right square appears in the middle of its pulse already the same color as the left, and the two keep pulsing together.",
    [{"at": 0.0, "event": "the left square pulses alone; window labelled"}, {"at": at("B01", "Watch."), "event": "the right square appears, same color as the left; 'added late' label"}],
    "manim: two dots reading one clock bar", "A real run is the evidence that a late node shares the clock; a drawing would only assert it. The surprise is the claim.",
    f"C01: {SCENES}/scene_c01_late_join.gd. Two 02-pulse squares (left centred at 0.30, 0.50; right at 0.70, 0.50; each 0.30 of the frame height). The right square is added at frame 300 (10.0 s). 15 s, 30 fps, Forward+, no input. Event times may be shifted by holding the first frame so the join lands on the spoken word 'Watch'.",
    "Movie Maker run (decode-scenes-act1.txt): TIME 1/30 s per frame; after the join the two squares differ by 0.0 steps for 151 frames",
    layout="video", title=N.ACTS[0][1], caption="TIME · seconds on one clock shared by the whole game",
    readouts=[{"at": 0.02, "text": "from the start", "x": 0.30, "y": 0.80}, {"at": at("B01", "Watch."), "text": "added late", "x": 0.70, "y": 0.80}])

rem("B02", "time is seconds since the engine started; one shared clock", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html",
     "image": V + "docs-time.png", "caption": "Godot 4.7 documentation · Canvas item shaders · Global built-ins · captured at build time",
     "frame": "browser",
     "moves": [{"at": 0.0, "x": 0.5, "y": 0.5, "scale": 1}, {"at": 0.28, "x": 0.5, "y": 0.5, "scale": 1.7},
               {"at": at("B02", "the seconds since"), "x": 0.5, "y": 0.5, "scale": 2.1, "ring": [0.15, 0.47, 0.7, 0.07]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 canvas item shader page in a browser window, scrolled to the Global built-ins table. The camera pushes in on the TIME row and a terracotta ring marks 'Global time since the engine has started, in seconds.' The first line of the row is also the glossary wording on screen: 'TIME · seconds on one clock shared by the whole game'.",
    "The camera pushes in on the TIME row and the ring lands as the voice says 'the seconds since the engine started'.",
    [{"at": 0.0, "event": "the docs page in a browser window"}, {"at": 0.28, "event": "push-in on the Global built-ins table"}, {"at": at("B02", "the seconds since"), "event": "ring on the TIME row"}],
    "manim: three nodes reading one clock (a fan of lines)", "The definition is a documentation claim, so the documentation itself is the evidence (SHOW-THE-THING, rung one). B01 already showed the shared clock in motion.",
    "Playwright capture of the live docs page at build time: open .../canvas_item_shader.html#global-built-ins, scroll the TIME row to about 40 percent of the viewport height, 1600x900 at device scale 2.4; the ring box is measured on the real capture")

lab("B03", "time scale changes TIME; pausing does not", V + "scale-and-pause.mp4",
    "Godot 4.7.2 · Forward+ · scripted run: time scale, then pause",
    "A real render: a grey track with a teal marker that a script moves by delta (top), and below it a square pulsing on TIME. At about 25 percent of the beat the time scale drops to one half: the marker and the pulse both slow. At about 60 percent the tree is paused: the marker freezes and the pulse carries on. Labels 'time scale 0.5' then 'paused'. Caption: 'time scale: how fast the game's clock runs · 1 is normal'.",
    "Both things slow under the time scale; under the pause the marker freezes and the pulse keeps going.",
    [{"at": 0.0, "event": "marker slides and the square pulses at normal speed"}, {"at": at("B03", "The game's time scale"), "event": "time scale 0.5: marker and pulse slow together"},
     {"at": at("B03", "Pausing does not"), "event": "paused: marker frozen, pulse still going"}],
    "manim: two clocks, one at half rate", "A real run shows the two cases the sentence contrasts, in one take; a drawing of a frozen marker and a living pulse would be a claim, not a result.",
    f"C03: {SCENES}/scene_c03_scale_pause.gd. A marker (a ColorRect moved by delta, 0.2 of the width per game second) on a grey track at y 0.28, and a 02-pulse square centred (0.50, 0.68), 0.34 of the height. Frame-counted events: time scale 0.5 from frame 84 (2.8 s) to 209, 1.0 from 210, paused from frame 228 (7.6 s) to the end. 12 s, 30 fps, Forward+. The controller runs while paused (process mode always); the marker is pausable.",
    "Movie Maker run: TIME 1/30 s per frame normally, 1/60 at time scale 0.5, and still 1/30 while paused; the marker moves 4.267 px per frame, 2.14 at half, and is frozen while paused",
    layout="video", caption="time scale: how fast the game's clock runs · 1 is normal",
    readouts=[{"at": at("B03", "The game's time scale", 0.03), "text": "time scale 0.5", "x": 0.5, "y": 0.10}, {"at": at("B03", "Pausing does not", 0.03), "text": "paused", "x": 0.5, "y": 0.10}])

manim("B04", "the clock wraps after an hour; a pulse that fits does not jump", "RolloverJump",
      "A horizontal clock bar labelled 'default limit: 3,600 s · one hour' with a terracotta marker that runs to the right end and wraps back to 0. Beneath it a zoom, labelled 'shown with the limit at 2 s so it fits on screen' (the measured check): time from 0 to 4 s, the wrap marked at 2 s and at 4 s. Two curves on it: the upper one (speed 1, two whole cycles in 2 s) carries on unbroken through each wrap; the lower one (speed 0.7, 1.4 cycles) snaps to a different height at each wrap, a vertical gap ringed in terracotta. Labels: 'a whole number of cycles: no jump' and 'any other: one jump'. Small grey credit: 'Apple M4 Pro · Godot 4.7.2 · limit set to 2 s · pulse change at the wrap: 4 steps against 44 (of 255)'.",
      "The marker runs to the end of the bar and wraps; in the zoom the upper curve carries on through the wrap unbroken while the lower curve snaps to a different height.",
      [{"at": 0.12, "event": "clock bar with its marker; the zoom with the two curves"}, {"at": at("B04", "It wraps back"), "event": "marker reaches the end and wraps to zero; the zoom's wrap lines"},
       {"at": at("B04", "A pulse that repeats"), "event": "upper curve: unbroken through the wrap"}, {"at": at("B04", "Any other pulse"), "event": "lower curve: the vertical jump, ringed"}],
      "capture: a real run with the limit set to two seconds", "The real wrap takes an hour; the drawing is of the measured two-second run, labelled as such, with both cases side by side and the measured numbers on it.",
      "verify5_rollover.gd: limit 2 s; speed 1.0 changes 4 steps at the wrap (ordinary frames: 6); speed 0.7 changes 44 and 43 steps (ordinary: 3)")

manim("B05", "the tick counter and TIME have different zeros", "TwoZeros",
      "Two horizontal rulers in seconds, one above the other. The top, labelled 'tick counter' (with the real call name in grey, Time.get_ticks_msec()), starts at 0 on the left. The bottom, labelled 'TIME', has its 0 a little to the right. Terracotta markers run along both at the same pace. A bracket between the two zeros reads 'about 0.25 s on this Mac'. A small cross over a subtraction sign between the two ruler labels lands on the words 'Do not'. Small grey credit: 'Apple M4 Pro · Godot 4.7.2 · three runs: 0.26, 0.29, 0.26 s'.",
      "Both markers move together, always a quarter second apart: the zeros never line up.",
      [{"at": 0.12, "event": "the two rulers with their zeros"}, {"at": at("B05", "Do not."), "event": "a cross over a subtraction sign between the labels"}, {"at": at("B05", "It starts earlier"), "event": "bracket between the zeros: about 0.25 s; markers run together; credit line with the three runs"}],
      "LectureEvidenceTable of the three measured gaps", "A gap between two zeros is a spatial fact: two rulers show it, a table only lists numbers.",
      "verify1_clocks.gd A (ticks minus TIME: 0.259, 0.288, 0.264 s median per run; 0.254 in the first draft and 0.240, 0.243, 0.242 in the re-run of 2026-10-13; 0.75 in a first cold launch, kept)")

manim("B06", "the tick counter ignores the time scale: the clocks drift apart for good", "Drift",
      "The two rulers from the previous picture. For one second the bottom marker (TIME) slows to half speed while the top marker (tick counter) keeps its pace; then both run normally again. The bracket between the zeros grows from 0.25 s to 0.75 s and stays there. Labels: 'time scale 0.5 for one second' and 'gap +0.5 s'.",
      "The bottom marker lags for a second and the bracket widens by exactly half a second, then stays.",
      [{"at": 0.1, "event": "the two rulers and the 0.25 s bracket"}, {"at": at("B06", "Run one second"), "event": "bottom marker slows for one second; bracket widens"},
       {"at": at("B06", "The two clocks"), "event": "both run normally; the bracket stays at 0.75 s"}],
      "capture: two number readouts side by side", "Two markers drifting apart carry 'they never agree again' as motion; the drift (+0.500, +0.502, +0.501 s) is printed on the picture.",
      "verify1_clocks.gd D, E (time scale 0.5 for 1 s: TIME rate 0.504; the offset grew by 0.500, 0.502, 0.501 s in three runs and stayed there)")

lab("B07", "an age you count from delta starts at zero with the node", V + "age.mp4",
    "Godot 4.7.2 · Forward+ · scripted run: the second square is added late",
    "GDScript card at left (the age counter, five lines). At right a real render: the left square pulses on TIME; a second square is added late and starts its pulse from the beginning, out of step with the first. Labels 'TIME' under the left square and 'age' under the right. Caption: 'delta: seconds since the last frame'.",
    "The late square starts at the beginning of its own pulse while the first carries on, so the two are visibly out of step.",
    [{"at": at("B07", "Add delta"), "event": "the age += delta line highlighted"}, {"at": at("B07", "and pass the age"), "event": "the set_shader_parameter line highlighted"},
     {"at": at("B07", "Now the late square"), "event": "the late square appears and starts from the beginning of its pulse"}],
    "LectureCodeTrace of the GDScript alone", "Cause and effect together: the five lines on the left, and the out-of-step pulse they cause on the right. B01 showed the opposite, so the contrast is the point.",
    f"C07: {SCENES}/scene_c07_age.gd. Left square: 02-pulse (TIME). Right square: 01-age (uniform age), added at frame 324 (10.8 s), its own _process adds delta to age and passes it with set_shader_parameter. Squares centred (0.30, 0.50) and (0.70, 0.50), 0.30 of the height. 14 s, 30 fps, Forward+, no input.",
    "Movie Maker run: the late square matches 0.5 + 0.5 sin(TAU age) within 0.5 steps; against the left square it differs by up to 95 steps in the first second",
    code='var age := 0.0\n\nfunc _process(delta):\n\tage += delta\n\tmaterial.set_shader_parameter("age", age)', code_file="scene script (GDScript)",
    cues=[{"at": at("B07", "Add delta"), "lines": [4]}, {"at": at("B07", "and pass the age"), "lines": [5]}],
    caption="delta: seconds since the last frame",
    readouts=[{"at": 0.06, "text": "TIME", "x": 0.30, "y": 0.80}, {"at": at("B07", "Now the late square"), "text": "age", "x": 0.70, "y": 0.80}])

rem("B08", "choose the clock by the job", "LectureEvidenceTable",
    {"title": "Which clock?", "headers": ["The job", "Use"],
     "rows": [["A loop that never needs to start", "time"], ["An effect that begins with a node", "an age you count"], ["A one-time effect", "a uniform your game moves"]],
     "note": "Godot 4.7 documentation · checked in Godot 4.7.2 (FACTCHECK rows for B01 to B07)", "cues": [at("B08", "A loop that never"), at("B08", "An effect that begins"), at("B08", "A one-time effect")], "durationSeconds": "__AUDIO__"},
    "A three-row table, one row ringed as each job is named, the clock beside it.", "The ring moves down the rows with the voice.",
    [{"at": at("B08", "A loop that never"), "event": "loop row"}, {"at": at("B08", "An effect that begins"), "event": "age row"}, {"at": at("B08", "A one-time effect"), "event": "one-time row"}],
    "manim: three tracks", "A short comparison of three parallel facts is exactly what the table component is for, and the three rows are the film's map.", "B01 to B07; wind uniform in B39 and B40")

# ═════════════════════════════ ACT II · The Wave ═════════════════════════════
manim("B09", "sine of time: swings between -1 and 1, one swing = 6.28 s", "SineOfTime",
      "Act title 'The Wave' (serif 40) top-left. Axes: time in seconds along x (0 to 13), value from -1 to 1 up the side. A terracotta dot travels along y = sin(TIME) at the pace of the clock, tracing the curve. A bracket under the first full swing reads 'one swing = 6.28 s'. At the end a label 'TAU = 6.28 · one full turn' lands beside the bracket (glossary: the number of radians in a full turn).",
      "The dot traces the curve up to 1 and down to -1; the bracket closes around the first full swing.",
      [{"at": 0.1, "event": "axes and the dot starts tracing"}, {"at": at("B09", "Sine counts in angles"), "event": "bracket around the first full swing: 6.28 s"}, {"at": at("B09", "That number is tau"), "event": "label: TAU = 6.28 · one full turn"}],
      "ShaderLab capture of sin(TIME) as a color", "A curve traced by a dot shows the range and the period at once; a color pulse would hide the negative half.",
      "Docs: sin takes radians; TAU = 6.283185. Math: period of sin(TIME) is 2 pi s")

manim("B10", "multiply time by tau: one swing per second", "TauTurn",
      "The same axes. The curve squeezes horizontally to a sixth of its width as the label changes from 'sin(TIME)' to 'sin(TIME × TAU)': the bracket under the first swing shrinks from '6.28 s' to '1 s', and tick marks at 1, 2 and 3 seconds each land where a swing begins (the curve crossing zero on its way up).",
      "The curve compresses: one swing now fits in one second.",
      [{"at": 0.1, "event": "the 6.28 s curve and its bracket"}, {"at": at("B10", "Multiply time by tau"), "event": "the curve compresses; bracket 1 s; ticks at 1, 2, 3 s mark where each swing begins"}],
      "LectureCodeTrace of one line", "The claim is a change of shape; a transform shows exactly that, and the ticks on the crests are the proof.",
      "Lab twins: 02-pulse reads the same at tv and tv + 1 (twin-summary.txt)")

manim("B11", "a raw sine as a color: the negative half clamps to zero", "ClampedHalf",
      "The sine curve again, with the ramp strip (0 to 1, drawn in greys) under it and a terracotta marker riding the strip with the dot. While the curve is below zero the curve is drawn grey and flattened onto the zero line, and the marker waits at the dark end of the strip. Labels: 'below zero → 0' and 'a color cannot be negative'.",
      "The marker rides the strip with the dot, then waits at the dark end for half of every swing.",
      [{"at": 0.1, "event": "curve, strip and marker moving together"}, {"at": at("B11", "Send a raw sine"), "event": "the negative half greys out and flattens; marker waits"}, {"at": at("B11", "The pulse sits"), "event": "label: half of each swing"}],
      "capture: a raw sine shader (a large dark field)", "A real capture would be a big dark field, hard to read as a wait; the plot with the strip shows the clamp at a glance, and the clamp itself was measured.",
      "run_images.py: sin = -1 and -0.707 read 0.000; +1 reads 1.000 (image-summary.txt)")

manim("B12", "squeeze into zero to one: halve, then lift", "HalveAndLift",
      "The curve shrinks to half its height, then slides up by a half until it fills 0 to 1 exactly; the strip's marker now travels the whole strip. A formula caption builds as '0.5 + 0.5 × sine', the first 0.5 lighting up with the lift and the second with the halving.",
      "Two moves in order, shrink then lift; afterwards the marker travels the whole strip.",
      [{"at": 0.1, "event": "the full-height curve and strip"}, {"at": at("B12", "Halve the swing"), "event": "the curve shrinks to half height"}, {"at": at("B12", "then lift it"), "event": "the curve slides up to fill 0 to 1; marker travels the whole strip"}],
      "LectureCodeTrace", "Shrink then lift is two visible transforms; code alone would hide which half does which.",
      "Lab twins: 02-pulse reads 0.0 to 1.0 only (twin-summary.txt)")

lab("B13", "the pulse as a shader: mix blends two colors", V + "pulse.mp4",
    "Godot 4.7.2 · Forward+ · live clock",
    "Code card at left (02-pulse.gdshader, eight lines); at right a real Godot window filled with a color that swings between teal and cream once a second. The pulse line is highlighted first, then the two color lines (label 'vec3: a bundle of three numbers: red, green, blue'), then the COLOR line (label 'vec4: red, green, blue, alpha (1 is solid)'). Caption: 'mix(a, b, t) blends from a to b: t of 0 gives a, 1 gives b'.",
    "The window swings between teal and cream while the highlight moves from the pulse line to the two colors and then to the blend.",
    [{"at": at("B13", "Here is that line"), "event": "the pulse line highlighted"}, {"at": at("B13", "The pulse blends"), "event": "the two color lines highlighted; vec3 label"}, {"at": at("B13", "Mix does the blending"), "event": "the COLOR line highlighted; vec4 label"}, {"at": 0.8, "event": "the pulse keeps running"}],
    "manim: the plot with a marker", "Code and its live result side by side is the claim: one line makes it breathe. The plots before and after carry the numbers, so a ramp marker here would only repeat them.",
    f"C13: Lab rect, lab-shaders/{PULSE}, 12 s, 30 fps, Forward+, no input.",
    "verify2 A: the pixel equals the formula of the decoded TIME within 0.5 steps over 90 frames",
    code=code_of(PULSE), code_file=f"lab-shaders/{PULSE}",
    cues=[{"at": at("B13", "Here is that line"), "lines": [ln(PULSE, "float pulse")]},
          {"at": at("B13", "The pulse blends"), "lines": [ln(PULSE, "vec3 teal"), ln(PULSE, "vec3 cream")], "label": "vec3: a bundle of three numbers: red, green, blue"},
          {"at": at("B13", "Mix does the blending"), "lines": [ln(PULSE, "COLOR =")], "label": "vec4: red, green, blue, alpha (1 is solid)"}],
    caption="mix(a, b, t) blends from a to b: t of 0 gives a, 1 gives b")

manim("B14", "amplitude: how far it swings from its middle", "Amplitude",
      "The plot with the ramp strip (middle line at 0.5). A slider labelled 'amplitude' moves 0.5, 0.25, 0 and back to 0.5: the curve's height changes around the middle line, and the strip's marker travels a shorter and shorter stretch around the middle, resting there at 0. A bracket from the middle to a crest is labelled 'amplitude'. Caption: 'amplitude: how far the wave swings from its middle'. A grey note: 'a half is the most that fits in 0 to 1'.",
      "The curve flattens as the slider falls and the marker parks at the middle.",
      [{"at": 0.1, "event": "plot, strip, slider at 0.5"}, {"at": at("B14", "Shrink it"), "event": "slider to 0.25 then 0: the curve flattens, the marker parks at the middle"}, {"at": at("B14", "A half is the most"), "event": "note: a half is the most that fits in 0 to 1"}],
      "ShaderLab sweep capture", "The curve's height is the thing amplitude changes, and the plot shows it directly while the strip shows the effect.",
      "Lab twins: 03-dials amplitude 0.25 and 0.0 (twin-summary.txt)")

manim("B15", "speed: how quickly it repeats; time times speed counts the cycles", "Speed",
      "The plot. A slider labelled 'speed' moves 0.5, 1, 2: the curve compresses in time, with brackets under the first swing reading '2 s', '1 s', '0.5 s'. A caption builds: 'cycles = TIME × speed' and 'one cycle = one full swing'. Caption: 'speed: how quickly it repeats'.",
      "The curve compresses horizontally as the slider rises and the dot's pace quickens.",
      [{"at": 0.1, "event": "plot and slider at 0.5: bracket 2 s"}, {"at": at("B15", "Time times speed"), "event": "caption: cycles = TIME × speed; one cycle = one full swing"}, {"at": at("B15", "Speed one half"), "event": "slider to 0.5: 2 s"}, {"at": at("B15", "Speed two"), "event": "slider to 2: 0.5 s"}],
      "ShaderLab sweep capture", "Compression along the time axis is what speed does; the brackets put the periods on the picture.",
      "Lab twins: 03-dials period 2.0 s at speed 0.5 and 0.5 s at speed 2.0 (twin-summary.txt)")

manim("B16", "offset: where in its cycle the wave starts; a half is exactly opposite", "Offset",
      "Two curves on one plot and two ramp strips with two markers: a plain one (offset 0) and one with offset 0.25, slid left by a quarter cycle so it starts at its crest; then the second curve slides to offset 0.5, exactly mirrored: it has a crest where the first has a trough. The two markers travel the strips in opposite directions. Caption: 'offset: added to slide the wave', second line 'here: where in its cycle it starts'.",
      "The second curve slides sideways until it mirrors the first, and the markers move opposite ways.",
      [{"at": 0.1, "event": "two identical curves and two markers"}, {"at": at("B16", "Offset a quarter"), "event": "second curve slides a quarter cycle: it starts at its crest"}, {"at": at("B16", "Offset a half"), "event": "second curve mirrors the first; markers move in opposite directions"}],
      "ShaderLab: two squares", "Sliding along the time axis is what offset does, and two markers going opposite ways prove 'exactly opposite'.",
      "Lab twins: 03-dials offset 0.25 reads 1.0 at tv 0; offset 0.5 pulse + plain pulse = 1 at every time tested (twin-summary.txt)")

shaderlab_code("B17", "the three dials as uniforms; offset is an instance uniform", DIALS,
               [{"at": at("B17", "Here are all three"), "lines": [ln(DIALS, "amplitude")], "label": "hint_range: the editor limits it to 0 to 0.5"}, {"at": at("B17", "dials your game"), "lines": [ln(DIALS, "uniform float speed")]},
                {"at": at("B17", "Time times speed"), "lines": [ln(DIALS, "float cycles")]}, {"at": at("B17", "Offset is an instance"), "lines": [ln(DIALS, "instance uniform")], "label": "instance uniform: each node keeps its own value"},
                {"at": at("B17", "The fourth number"), "lines": [ln(DIALS, "instance uniform") + 1], "label": "a fourth dial waits here: frequency"}],
               "The real 03-dials.gdshader (thirteen lines) on a cream code card: the three uniform lines, then the line that counts the cycles, then the instance uniform line again; at the end the empty line under the three uniforms is highlighted as the slot for a fourth dial. Cue labels: 'hint_range: the editor limits it to 0 to 0.5' on the amplitude line, 'instance uniform: each node keeps its own value' on the offset line and 'a fourth dial waits here: frequency' on the empty line.",
               "Line focus steps down the dials, then to the cycle count, then back to the instance uniform.",
               [{"at": at("B17", "Here are all three"), "event": "amplitude line, hint_range label"}, {"at": at("B17", "Time times speed"), "event": "cycles line"}, {"at": at("B17", "Offset is an instance"), "event": "instance uniform line, label"}, {"at": at("B17", "The fourth number"), "event": "the empty line under the three uniforms highlighted: 'a fourth dial waits here: frequency'"}],
               "LectureCodeTrace (it holds about ten lines and this file has thirteen)", "The file is real and fits ShaderLab's code layout (up to fourteen lines); paced focus is exactly 'here are the three'.",
               "lab-shaders/03-dials.gdshader compiles in the Lab; docs: per-instance uniforms in canvas_item")

lab("B18", "five squares, one shader, five offsets: the pulse rolls along the row", V + "rolling-row.mp4",
    "Godot 4.7.2 · Forward+ · five squares share one material",
    "GDScript card at left (the two-line loop that sets each node's offset); at right a real render: five squares in a row, all pulsing, each a fifth of a cycle behind its neighbour, so the brightest square moves along the row like a wave. Labels under the squares: 0, 0.2, 0.4, 0.6, 0.8.",
    "The brightest square travels along the row: a wave rolls from one end to the other.",
    [{"at": 0.08, "event": "five squares pulsing, labelled with their offsets"}, {"at": at("B18", "Each gets"), "event": "the loop lines highlighted"}, {"at": at("B18", "Their pulses no longer"), "event": "the brightest square travels along the row"}],
    "manim: five dots", "Five real squares sharing one material is the evidence for per-node offsets; the rolling wave is visible only in motion.",
    f"C18: {SCENES}/scene_c18_rolling_row.gd. Five ColorRects (0.13 of the width) at x = 0.18, 0.34, 0.50, 0.66, 0.82, y 0.50, sharing ONE ShaderMaterial of {DIALS} (amplitude 0.5, speed 0.5); each node gets set_instance_shader_parameter('offset', i / 5.0). 12 s, 30 fps, Forward+. In the capture the bright crest moves toward the left end.",
    "verify2 B and the Movie Maker run: all five squares match the formula within 0.5 steps in Forward+ and Compatibility",
    code='for i in 5:\n\tget_child(i).set_instance_shader_parameter("offset", i / 5.0)', code_file="scene script (GDScript)",
    cues=[{"at": at("B18", "Each gets"), "lines": [1, 2]}],
    readouts=[{"at": 0.08, "text": "0", "x": 0.18, "y": 0.78}, {"at": 0.08, "text": "0.2", "x": 0.34, "y": 0.78}, {"at": 0.08, "text": "0.4", "x": 0.50, "y": 0.78},
              {"at": 0.08, "text": "0.6", "x": 0.66, "y": 0.78}, {"at": 0.08, "text": "0.8", "x": 0.82, "y": 0.78}])

# ═════════════════════════════ ACT III · Loops and Curves ═════════════════════════════
manim("B19", "fract: the cycle count becomes a ramp that restarts", "Restart",
      "Act title 'Loops and Curves' (serif 40) top-left. A rising straight line (the cycle count TIME × speed, which never stops) with whole-number ticks 0, 1, 2, 3 up the side. A copy of the line is cut at every whole number and drops back to 0, becoming a sawtooth between 0 and 1. A ramp strip with a marker under it jumps back to the left at every restart. Labels (glossary wording): 'fract(x): the part after the point: x minus floor(x)' and 'ramp: a smooth run of values from 0 up to 1'.",
      "The straight line is cut at each whole number and folds back to zero; the strip's marker restarts every time.",
      [{"at": 0.1, "event": "the never-ending count line"}, {"at": at("B19", "use fract"), "event": "the cut copy drops to zero at each whole number: the sawtooth"}, {"at": at("B19", "so the cycle count"), "event": "the ramp strip with its restarting marker; labels"}],
      "ShaderLab capture of a loading bar", "A line cut at every whole number shows exactly what fract keeps; the restarting marker makes the loop visible.",
      "Docs: fract = x - floor(x); Lab twins: 04-three-shapes sawtooth reads 0.25, 0.50, 0.75 at tv 0.5, 1.0, 1.5 (twin-summary.txt)")

manim("B20", "fold the ramp into a triangle", "Fold",
      "The sawtooth from the previous picture transforms in four small steps, each labelled: '× 2' (it now runs 0 to 2), '− 1' (−1 to 1), 'abs' (a V shape), '1 −' (flipped into a triangle). The strip marker now moves back and forth at a steady pace. Caption: 'abs(x): drops the minus sign'.",
      "The sawtooth folds step by step into a triangle and the marker turns around at each end.",
      [{"at": 0.1, "event": "the sawtooth"}, {"at": at("B20", "double it"), "event": "× 2 then − 1"}, {"at": at("B20", "take the absolute"), "event": "abs: the V shape"}, {"at": at("B20", "You get a triangle"), "event": "1 − : the triangle; marker moves back and forth"}],
      "LectureCodeTrace of the formula", "Four visible transforms are the recipe; a transform keeps the shape's identity from step to step.",
      "Docs: abs; Lab twins: 04-three-shapes triangle reads 0.50, 1.00, 0.50, 0.10 at tv 0.5, 1.0, 1.5, 1.9")

lab("B21", "sine, triangle and sawtooth at the same pace, as three bars", V + "three-shapes.mp4",
    "Godot 4.7.2 · Forward+ · live clock",
    "Code card at left (04-three-shapes.gdshader); at right a real render of three horizontal teal bars on light tracks, separated by thin gaps, each filling from the left to its wave's value: top sine, middle triangle, bottom sawtooth, all with the same two-second period. Labels at the left of the rows: 'sine', 'triangle', 'sawtooth'. Caption: 'sawtooth: a ramp that restarts'.",
    "The sine bar eases at each end, the triangle bar turns sharply, the sawtooth bar fills and snaps back to empty.",
    [{"at": at("B21", "The sine eases"), "event": "sine line highlighted; top bar eases at each end"}, {"at": at("B21", "The triangle turns"), "event": "triangle line highlighted; middle bar turns sharply"},
     {"at": at("B21", "The sawtooth never"), "event": "sawtooth line highlighted; bottom bar jumps back"}],
    "manim: three plots with three markers", "A bar's edge is a one-number motion: ease, steady and snap are visible as the edge moves; three rows in one shader prove the three share one count.",
    f"C21: Lab rect, lab-shaders/{SHAPES}, 12 s (six loops), 30 fps, Forward+, no input.",
    "Lab twins: the bar edges equal the three values within 1.5 steps at tv 0.5, 1.0, 1.5, 1.9; verify2 C: within 0.5 px over 90 frames",
    code=code_of(SHAPES), code_file=f"lab-shaders/{SHAPES}",
    cues=[{"at": at("B21", "The sine eases"), "lines": [ln(SHAPES, "float sine")]}, {"at": at("B21", "The triangle turns"), "lines": [ln(SHAPES, "float tri")]}, {"at": at("B21", "The sawtooth never"), "lines": [ln(SHAPES, "float saw")]}],
    readouts=[{"at": 0.06, "text": "sine", "x": 0.08, "y": 0.16}, {"at": 0.06, "text": "triangle", "x": 0.10, "y": 0.50}, {"at": 0.06, "text": "sawtooth", "x": 0.10, "y": 0.84}],
    caption="sawtooth: a ramp that restarts")

manim("B22", "a CurveTexture: a curve baked into a strip of pixels", "CurveStrip",
      "A drawn curve (the breath: a slow rise, a short hold, a long fall) above a thin horizontal strip whose brightness follows the curve (drawn in greys: dark where the curve is 0, light where it is 1). A vertical scan line slides along the strip with a dot on the curve at the same position. Labels: 'CurveTexture: a curve baked into a strip of pixels' and the call 'texture(curve, vec2(t, 0.0)).r' in monospace.",
      "The scan line slides along the strip and the dot follows the curve: the strip's brightness equals the curve's height.",
      [{"at": 0.1, "event": "the curve and its strip"}, {"at": at("B22", "Draw it as a curve"), "event": "the curve is drawn"}, {"at": at("B22", "A curve texture bakes"), "event": "the strip lights up beneath it; the scan line slides along"}],
      "ShaderLab capture of a scripted CurveTexture", "The mechanism is a mapping from height to brightness; the scan line shows both at one position.",
      "Docs: CurveTexture; verify3 A: the strip equals the curve within 2.35 steps over all 256 pixels")

lab("B23", "the lookup line: the restarting ramp plays the curve on a loop", V + "curve-loop.mp4",
    "Godot 4.7.2 · Forward+ · a CurveTexture made in a script",
    "Code card at left (05-curve-loop.gdshader); at right a real render: a square whose color follows the breath curve (a slow rise to cream, a short hold, a long fall back to teal), looping every two seconds. The lookup line is highlighted first, then the ramp line.",
    "The square follows the curve's shape, loop after loop.",
    [{"at": at("B23", "The lookup"), "event": "the texture lookup line highlighted"}, {"at": at("B23", "Feed it the restarting"), "event": "the fract ramp line highlighted; the loop restarts visibly"}],
    "manim: a dot riding the curve", "The real lookup driving a real color shows that the shape you drew is the shape you see.",
    f"C23: {SCENES}/scene_c23_curve_loop.gd. A square (0.5 of the height, centred) with lab-shaders/{CURVE}; the 'curve' uniform is a CurveTexture of the breath curve (points (0,0), (0.40,1), (0.55,1), (1,0), flat tangents). 12 s, 30 fps, Forward+, no input.",
    "verify3 D and the Movie Maker run: the pixel follows mix(teal, cream, curve(fract(TIME * 0.5))) within 1.6 steps",
    code=code_of(CURVE), code_file=f"lab-shaders/{CURVE}",
    cues=[{"at": at("B23", "The lookup"), "lines": [ln(CURVE, "float k")]}, {"at": at("B23", "Feed it the restarting"), "lines": [ln(CURVE, "float t")]}])

manim("B24", "a sine-fed curve plays forward then backward; a ramp-fed curve plays one way", "SineOrRamp",
      "Two tracks, each with a copy of the breath curve and a dot on it, and the input drawn as a strip above each. Top track: the input is a sine, the dot runs along the curve to its end and then back along it. Bottom track: the input is the restarting ramp, the dot runs to the end and jumps back to the start. Labels: 'sine input: forward, then backward' and 'ramp input: one way, then restart'.",
      "The top dot goes out and comes back; the bottom dot goes out and jumps back.",
      [{"at": 0.1, "event": "two tracks, two dots"}, {"at": at("B24", "Feed the same curve"), "event": "top dot runs out and back"}, {"at": at("B24", "Feed it from the ramp"), "event": "bottom dot runs out and jumps back"}],
      "ShaderLab two squares", "Out-and-back against out-and-jump is a path, and a path is best drawn as a moving dot.",
      "verify3 E: the sine-fed sequence over one cycle is palindromic, the ramp-fed one is not")

rem("B25", "one count, four looks", "LectureEvidenceTable",
    {"title": "One count, four looks", "headers": ["Look", "It feels like", "In code (c = TIME × speed)"],
     "rows": [["sine", "smooth swing", "0.5 + 0.5 * sin(TAU * c)"], ["triangle", "steady back and forth", "1.0 - abs(fract(c) * 2.0 - 1.0)"],
              ["sawtooth", "one way, restart", "fract(c)"], ["curve", "whatever you draw", "texture(curve, vec2(fract(c), 0.0)).r"]],
     "note": "lab-shaders/04-three-shapes.gdshader and 05-curve-loop.gdshader · checked in Godot 4.7.2",
     "cues": [at("B25", "Sine swings"), at("B25", "Triangle swings"), at("B25", "Sawtooth restarts"), at("B25", "And a curve")], "durationSeconds": "__AUDIO__"},
    "A four-row table, one row ringed as each look is named, with the code that makes it.", "The ring steps down the rows with the voice.",
    [{"at": at("B25", "Sine swings"), "event": "sine row"}, {"at": at("B25", "Triangle swings"), "event": "triangle row"}, {"at": at("B25", "Sawtooth restarts"), "event": "sawtooth row"}, {"at": at("B25", "And a curve"), "event": "curve row"}],
    "manim: four small plots", "Four parallel facts with a line of code each is a reference card; the previous beats already supplied the pictures.", "twins and verify3 (see B19 to B24)")

# ═════════════════════════════ ACT IV · Waves on a Shape ═════════════════════════════
manim("B26", "from five offsets to an offset at every pixel", "FiveToEvery",
      "Act title 'Waves on a Shape' (serif 40) top-left. The five squares from the row, each with its offset label (0, 0.2, 0.4, 0.6, 0.8) and the pulse curve under it shifted accordingly. The squares merge into one continuous strip; the row of labels becomes the address strip 0 to 1 (U V x) and the five curves become one wave across the strip, each pixel column carrying its own offset. Caption: 'offset from the address'.",
      "Five separate offsets blur into a continuous strip in which every pixel column has its own offset from where it sits.",
      [{"at": 0.1, "event": "five squares with offsets and curves"}, {"at": at("B26", "A shape has"), "event": "the squares merge into one strip"}, {"at": at("B26", "So let the address"), "event": "the label row becomes the address 0 to 1; one wave across the strip"}],
      "ShaderLab capture of the stripes", "The step from five offsets to a continuous one is a morph, and a morph keeps the connection between the two pictures.",
      "Lab twins: 06-stripes (the continuous case); verify2 B (the five-square case)")

lab("B27", "the address as the count: stripes; frequency is cycles across the shape", V + "stripes.png",
    "Godot 4.7.2 · Forward+ · frequency 3",
    "Code card at left (06-stripes.gdshader); at right a real still: the banner crossed by three bright cream stripes on teal, with three terracotta rings landing on the stripes in turn. Caption: 'frequency: how many cycles fit across the shape'.",
    "The cycles line is highlighted, then the frequency line, and the rings count the three stripes one by one.",
    [{"at": at("B27", "Use the address"), "event": "the cycles line highlighted"}, {"at": at("B27", "The number of stripes"), "event": "the frequency uniform highlighted; caption"}, {"at": at("B27", "Three cycles"), "event": "rings count the three bright stripes"}],
    "manim: a plot of three cycles over the strip", "A real render is the proof that three cycles make three stripes, and the rings count them against the voice.",
    f"C27: Lab rect, lab-shaders/{STRIPES} at frequency 3 (the default), still PNG 1920x1080 (rect = the banner). Bright stripe centres at x = 0.083, 0.417, 0.750 (the rings).",
    "Lab twins: 06-stripes crests at (0.25 + k) / frequency for frequency 2, 3, 5 (twin-summary.txt)",
    code=code_of(STRIPES), code_file=f"lab-shaders/{STRIPES}",
    cues=[{"at": at("B27", "Use the address"), "lines": [ln(STRIPES, "float cycles")]}, {"at": at("B27", "The number of stripes"), "lines": [ln(STRIPES, "uniform float frequency")]}],
    rings=[{"at": at("B27", "Three cycles"), "box": [0.0, 0.0, 0.17, 1.0]}, {"at": at("B27", "three bright"), "box": [0.33, 0.0, 0.50, 1.0]}, {"at": at("B27", "stripes", nth=-1), "box": [0.67, 0.0, 0.83, 1.0]}],
    caption="frequency: how many cycles fit across the shape")

lab("B28", "subtract time from the address: the stripes slide at speed", V + "travel.mp4",
    "Godot 4.7.2 · Forward+ · speed 0.5, then -0.5 · scripted",
    "Code card at left (07-travel.gdshader); at right the same stripes now sliding to the right, with a readout 'speed 0.5' at the top; in the last seconds the speed flips to minus one half and they slide left ('speed -0.5').",
    "The stripes slide right at half the shape each second, then reverse.",
    [{"at": at("B28", "Now subtract time"), "event": "the cycles line with TIME * speed highlighted; stripes slide right"}, {"at": at("B28", "A negative speed"), "event": "speed -0.5: the stripes slide left"}],
    "manim: a plot with a crest tracked", "Real stripes sliding at a measured pace prove 'exactly speed shape-widths each second' better than a drawn arrow.",
    f"C28: {SCENES}/scene_c28_travel.gd. A full-frame rect (the Lab rect) with lab-shaders/{TRAVEL}, frequency 3, speed 0.5 until frame 330 (11.0 s), then -0.5 (a step: no pop, because 2 x 0.5 x 3 x 11 = 33 whole cycles). 13 s, 30 fps, Forward+. The step lands on the spoken words 'A negative speed'.",
    "Lab twins: crests at speed * t + (0.25 + k) / frequency for speeds -0.5, 0, 0.5, 1.0 and frequencies 1, 2, 3, 5; verify2 D within 1.7 px; Movie Maker: the crest moves +10.67 px per frame, then -10.67 after the step",
    code=code_of(TRAVEL), code_file=f"lab-shaders/{TRAVEL}",
    cues=[{"at": at("B28", "Now subtract time"), "lines": [ln(TRAVEL, "float cycles")]}, {"at": at("B28", "Speed is how far"), "lines": [ln(TRAVEL, "uniform float speed")]}],
    readouts=[{"at": 0.06, "text": "speed 0.5", "x": 0.5, "y": 0.08}, {"at": at("B28", "A negative speed"), "text": "speed -0.5", "x": 0.5, "y": 0.08}])

lab("B29", "distance from the middle as the count: rings", V + "rings.mp4",
    "Godot 4.7.2 · Forward+ · square shape",
    "Code card at left (08-rings.gdshader); at right a real render of rings spreading outward from the middle of a square. The distance call is highlighted; caption 'distance(a, b): how far apart two points are'.",
    "Rings are born at the middle and spread outward to the edge.",
    [{"at": at("B29", "On a square shape"), "event": "the distance call highlighted"}, {"at": at("B29", "and the stripes become"), "event": "rings spreading outward"}],
    "manim: concentric circles growing", "The rings are the real output of the same four numbers fed a different count; only motion shows 'spread outward'.",
    f"C29: Lab sprite (square, texture ignored: --sprite-tex white), lab-shaders/{RINGS}, frequency 4, speed 0.25, 10 s, 30 fps, Forward+. A circle on a square only: on a wide shape the rings squash.",
    "Lab twins: ring radii at speed * t + (0.25 + k) / frequency; run_images.py: the picture equals the formula within 0.5 steps (0.86 in Compatibility; the check allows 3) and is the same along the x and y axes",
    code=code_of(RINGS), code_file=f"lab-shaders/{RINGS}",
    cues=[{"at": at("B29", "On a square shape"), "lines": [ln(RINGS, "float cycles")]}],
    caption="distance(a, b): how far apart two points are")

manim("B30", "the four numbers are independent", "FourKnobs",
      "A wide strip showing a traveling wave (stripes) and four sliders in a row: amplitude, frequency, speed, offset, each captioned in one to three words ('how tall', 'how many', 'how fast', 'where it starts'). Each slider moves alone while the other three stay put, and only its own property of the wave changes: the height, the number of cycles across, the sliding pace, the starting shift.",
      "Each slider moves alone and only its own property of the wave changes.",
      [{"at": 0.1, "event": "strip and four sliders at rest"}, {"at": at("B30", "Amplitude is how tall"), "event": "amplitude slider moves: height changes"}, {"at": at("B30", "Frequency is how many"), "event": "frequency slider: cycle count changes"},
       {"at": at("B30", "Speed is how fast"), "event": "speed slider: sliding pace changes"}, {"at": at("B30", "Offset is where"), "event": "offset slider: the pattern shifts"}],
      "LectureEvidenceTable", "Independence is a motion claim: four sliders moved one at a time, with the other three visibly still.",
      "Lab twins: 07-travel crest shift = speed * time for frequency 1, 2, 3, 5 (the two do not interact)")

lab("B31", "add the wave to the lookup address: the picture ripples", V + "ripple.mp4",
    "Godot 4.7.2 · Forward+ · amplitude 0.05",
    "Code card at left (09-ripple.gdshader, the lookup line labelled 'TEXTURE: the node's own picture; texture() reads it'); at right a real render of the teal-and-cream checker picture rippling vertically in waves that slide across it, with a terracotta ring around the picture's rectangle (the rectangle itself never moves). Readout 'same rectangle'.",
    "The squares of the checker wobble up and down in a wave while the rectangle around them stays still.",
    [{"at": at("B31", "Add the wave"), "event": "the wave line then the lookup line highlighted; the ripple runs"}, {"at": at("B31", "No new corners"), "event": "ring around the rectangle: it does not move"}],
    "manim: a grid whose rows shift", "A real render shows exactly what 'the picture itself ripples' looks like and that the outline stays; a drawing would have to invent the ripple.",
    f"C31: Lab sprite with the Lab's checker picture (--sprite-tex checker), lab-shaders/{RIPPLE}, amplitude 0.05, frequency 3, speed 0.5, offset 0, 10 s, 30 fps, Forward+. The ring marks the 288 px picture rectangle (0.275 to 0.725 of the width, 0.10 to 0.90 of the height in a 640x360 window).",
    "run_images.py: the picture equals the formula render (reference renderer) with 0 pixels different (amplitudes 0.08 and 0.20, offset 0.25)",
    code=code_of(RIPPLE), code_file=f"lab-shaders/{RIPPLE}",
    cues=[{"at": at("B31", "Add the wave"), "lines": [ln(RIPPLE, "float wave"), ln(RIPPLE, "COLOR =")], "label": "TEXTURE: the node's own picture; texture() reads it"}],
    rings=[{"at": at("B31", "No new corners"), "box": [0.275, 0.10, 0.725, 0.90]}],
    readouts=[{"at": at("B31", "No new corners"), "text": "same rectangle", "x": 0.5, "y": 0.96}])

lab("B32", "multiply the wave by the address across: the left edge is pinned", V + "flag.mp4",
    "Godot 4.7.2 · Forward+ · amplitude 0.05",
    "Code card at left (10-flag.gdshader); at right the checker picture waving, the left edge perfectly still and the ripple growing toward the right end. A ring on the left edge ('pinned') and a ring on the right end ('free').",
    "The left edge holds still while the ripple grows to the right, like a flag on a pole.",
    [{"at": at("B32", "Multiply the wave"), "event": "the wave line with * UV.x highlighted"}, {"at": at("B32", "and the left edge"), "event": "ring on the left edge: pinned"}, {"at": at("B32", "The right end"), "event": "ring on the right end: free"}],
    "manim: a grid pinned at one side", "A flag is its motion: a real render shows the pinned edge and the growing ripple in one take.",
    f"C32: Lab sprite with the checker picture, lab-shaders/{FLAG}, amplitude 0.05, frequency 3, speed 0.5, 10 s, 30 fps, Forward+. Rings: left edge box [0.275, 0.10, 0.31, 0.90], right end box [0.69, 0.10, 0.725, 0.90].",
    "run_images.py: left 12 columns move less than a tenth of the right 60; the movement grows quarter by quarter; equals the formula render",
    code=code_of(FLAG), code_file=f"lab-shaders/{FLAG}",
    cues=[{"at": at("B32", "Multiply the wave"), "lines": [ln(FLAG, "float wave")]}],
    rings=[{"at": at("B32", "and the left edge"), "box": [0.275, 0.10, 0.31, 0.90]}, {"at": at("B32", "The right end"), "box": [0.69, 0.10, 0.725, 0.90]}],
    readouts=[{"at": at("B32", "and the left edge"), "text": "pinned", "x": 0.29, "y": 0.96}, {"at": at("B32", "The right end"), "text": "free", "x": 0.71, "y": 0.96}])

lab("B33", "the limit: a big ripple smears the edge pixels", V + "smear.png",
    "Godot 4.7.2 · Forward+ · amplitude 0.20 · still",
    "Code card at left (09-ripple.gdshader); at right a real still of the checker picture with a very large amplitude: the top and bottom edges are smeared into tall stretched bars. A ring on the top edge and a readout 'edge pixels stretch'.",
    "A ring settles on the smeared top edge while the voice says the edges smear.",
    [{"at": at("B33", "so a big ripple"), "event": "ring on the smeared top edge; readout"}],
    "manim: a grid pushed past its frame", "The smear is a visual artefact: a real still shows it exactly as it looks, and the same shader at a small amplitude (previous beat) shows what it looks like without.",
    f"C33: Lab sprite with the checker picture, lab-shaders/{RIPPLE}, amplitude 0.20, frequency 3, speed 0.5, tv 0.3 (still), PNG 1920x1080, Forward+. Ring around the top 12 percent of the picture rectangle.",
    "run_images.py: at amplitude 0.20 rows near the top repeat the edge row (smear); equals the formula render",
    code=code_of(RIPPLE), code_file=f"lab-shaders/{RIPPLE}",
    cues=[{"at": at("B33", "so a big ripple"), "lines": [ln(RIPPLE, "COLOR =")]}],
    rings=[{"at": at("B33", "so a big ripple"), "box": [0.275, 0.10, 0.725, 0.22]}],
    readouts=[{"at": at("B33", "so a big ripple"), "text": "edge pixels stretch", "x": 0.5, "y": 0.05}])

lab("B34", "two waves added: the pattern stops repeating so plainly", V + "two-waves.mp4",
    "Godot 4.7.2 · Forward+ · two waves added",
    "Code card at left (11-two-waves.gdshader); at right the checker picture rippling with a slow wide wave and a fast narrow wave added together, so the pattern no longer looks like a plain repeat. The two wave lines are highlighted in turn, then the line that adds them.",
    "Two ripples of different size and pace pass through each other and the picture's motion never settles into an obvious repeat.",
    [{"at": at("B34", "Add two waves"), "event": "the big wave line highlighted"}, {"at": at("B34", "Each wave has"), "event": "the small wave line highlighted"}, {"at": at("B34", "and the shader adds"), "event": "the lookup line that adds both"}],
    "manim: two curves summed", "Two real waves summed on a real picture is the claim; the plot would show the sum but not how it looks in use.",
    f"C34: Lab sprite with the checker picture, lab-shaders/{TWO}, 10 s, 30 fps, Forward+.",
    "run_images.py: equals the formula render of the two summed sines",
    code=code_of(TWO), code_file=f"lab-shaders/{TWO}",
    cues=[{"at": at("B34", "Add two waves"), "lines": [ln(TWO, "float big")]}, {"at": at("B34", "Each wave has"), "lines": [ln(TWO, "float small")]}, {"at": at("B34", "and the shader adds"), "lines": [ln(TWO, "COLOR =")]}])

# ═════════════════════════════ ACT V · One Clock, Two Effects ═════════════════════════════
lab("B35", "the finished scene: a logo that breathes above a banner that waves", V + "together.mp4",
    "Godot 4.7.2 · Forward+ · wind 1 · scripted",
    "Act title 'One Clock, Two Effects' (serif 40) top-left. A real render: the teal test sprite (a blob with two cream eyes) swelling and settling above a striped banner whose wave travels, pinned at the left. Labels 'logo' and 'banner'.",
    "The logo swells and settles while the banner's wave travels: two effects running together.",
    [{"at": 0.0, "event": "logo breathing, banner waving"}, {"at": at("B35", "Two shaders"), "event": "labels: both read the same clock"}],
    "manim: a drawing of the two effects", "The payoff has to be seen working, so the real two-effect scene opens the act.",
    f"C35: {SCENES}/scene_c35_together.gd (--part together). Logo (12-breath, the breath CurveTexture) centred (0.50, 0.30) at 0.5 of the height; banner (13-banner, wind 1.0) centred (0.50, 0.72) at 0.55 of the width. 12 s, 30 fps, Forward+, no input.",
    "Movie Maker run: logo width swings 108 to 136 px, within 1 px of the formula; the banner's top edge moves 18 px peak to peak",
    layout="video", title=N.ACTS[4][1],
    readouts=[{"at": 0.1, "text": "logo", "x": 0.30, "y": 0.30}, {"at": 0.1, "text": "banner", "x": 0.18, "y": 0.72}])

manim("B36", "the breath is a curve; the restarting ramp plays it; size = 1 + a quarter of the curve", "BreathCurve",
      "The breath curve (a slow rise, a short hold, a long fall) drawn on axes, with the restarting ramp as a strip above it feeding a dot that rides the curve. Beside the plot, the teal logo blob whose size follows 1 + 0.25 × curve: it swells as the dot rises, holds, and settles as the dot falls. Caption: 'size = 1 + 0.25 × curve'.",
      "The dot rides the curve as the ramp restarts, and the logo swells and settles in step with it.",
      [{"at": 0.1, "event": "the curve, the ramp strip and the logo"}, {"at": at("B36", "The restarting ramp"), "event": "the dot rides the curve once per ramp cycle"}, {"at": at("B36", "The logo's size"), "event": "caption: size = 1 + 0.25 × curve"}],
      "ShaderLab capture of the logo alone", "The relation between a curve and a size is clearest with both drawn side by side and moving together.",
      "verify3 F: the logo's width follows 76.8 px * (1 + 0.25 k) within 1.2 px over 300 frames")

manim("B37", "bigger picture = look it up from closer in", "LookCloser",
      "A picture (the blob with eyes) in a square frame with a five-by-five grid of small dots on it showing where the shader looks up the picture. The dots pull in toward the middle (the address measured from the middle, divided by the scale 1.25) and the part of the picture they read now fills the frame, so the picture appears a quarter bigger. Caption: 'bigger picture = look up closer in'. Readout: 'scale 1.25'.",
      "The lookup dots draw in toward the middle and the picture seen through them grows.",
      [{"at": 0.1, "event": "the picture and the lookup dots at scale 1"}, {"at": at("B37", "Measure the address"), "event": "the dots pull toward the middle: divide by the scale"}, {"at": at("B37", "A scale of one"), "event": "readout scale 1.25; the picture is a quarter bigger"}],
      "ShaderLab capture with code", "Scaling by changing where you look is counter-intuitive; moving the lookup points makes the inversion visible.",
      "run_images.py: at k = 0.5 and 0.8 the blob is 87 and 93 px wide against 86.4 and 92.2 expected from 76.8 * (1 + 0.25 k), centre unchanged")

lab("B38", "the breathing logo live: curve texture, ramp, scale about the middle", V + "breath.mp4",
    "Godot 4.7.2 · Forward+ · a CurveTexture made in a script",
    "Code card at left (12-breath.gdshader); at right a real render of the teal blob swelling and settling about its middle on the stage, with a ring around its rectangle showing the margin around the art.",
    "The logo swells and settles about its middle and never touches the edge of its rectangle.",
    [{"at": at("B38", "The curve is a texture"), "event": "the curve lookup line highlighted"}, {"at": at("B38", "and the logo swells"), "event": "the scale lines highlighted"}, {"at": at("B38", "The art keeps"), "event": "ring around the rectangle: empty margin, nothing smears"}],
    "manim: the logo and a plot", "The finished shader in action: code and result together are the payoff of Acts II and III.",
    f"C38: {SCENES}/scene_c35_together.gd (--part logo). Logo centred (0.50, 0.50) at 0.5 of the height, lab-shaders/{BREATH} with the breath CurveTexture. 10 s, 30 fps, Forward+, no input.",
    "verify3 F and the Movie Maker run: width 108 to 136 px (at this scale), within 1 px of 76.8 * scale * (1 + 0.25 k)",
    code=code_of(BREATH), code_file=f"lab-shaders/{BREATH}",
    cues=[{"at": at("B38", "The curve is a texture"), "lines": [ln(BREATH, "float k")]}, {"at": at("B38", "and the logo swells"), "lines": [ln(BREATH, "float scale"), ln(BREATH, "vec2 uv")]}],
    rings=[{"at": at("B38", "The art keeps"), "box": [0.359, 0.25, 0.641, 0.75]}])

lab("B39", "the banner live: the traveling wave, pinned, scaled by wind", V + "banner.mp4",
    "Godot 4.7.2 · Forward+ · wind 1",
    "Code card at left (13-banner.gdshader); at right a real render of the striped banner with a wave that travels along it, the left end still. The pinned line is highlighted, then the wind uniform; a readout 'wind 1'.",
    "The wave travels along the banner from the pinned end while the voice describes it.",
    [{"at": at("B39", "The banner is"), "event": "the wave line highlighted (the pinned travelling wave)"}, {"at": at("B39", "A wind uniform"), "event": "the wind uniform highlighted; readout wind 1"}],
    "manim: the banner drawn flat then waved", "A banner is its motion, so the real render carries it; the code shows where wind multiplies in.",
    f"C39: {SCENES}/scene_c35_together.gd (--part banner). Banner centred (0.50, 0.50) at 0.55 of the width, lab-shaders/{BANNER}, wind 1.0, amplitude 0.06, frequency 3, speed 0.5. 10 s, 30 fps, Forward+, no input.",
    "run_images.py: wind 0 equals amplitude 0; at wind 1 the left edge holds and the right end moves; equals the formula render",
    code=code_of(BANNER), code_file=f"lab-shaders/{BANNER}",
    cues=[{"at": at("B39", "The banner is"), "lines": [ln(BANNER, "float wave")]}, {"at": at("B39", "A wind uniform"), "lines": [ln(BANNER, "uniform float wind")]}],
    readouts=[{"at": at("B39", "A wind uniform"), "text": "wind 1", "x": 0.5, "y": 0.10}])

lab("B40", "a click sets wind to one; a tween brings it back to zero", V + "wind-click.mp4",
    "Godot 4.7.2 · Forward+ · scripted input: one click at 4.5 s",
    "GDScript card at left (the click handler, five lines, word for word the handler in scene_c40_wind_click.gd); at right a real render: the striped banner hangs still, a scripted click lands, the banner snaps into motion and settles over four seconds. A label 'scripted input' stays on screen. Caption: 'tween: Godot's way to change a value smoothly over time from GDScript'.",
    "The banner is still until the click, then waves and settles back to still.",
    [{"at": 0.0, "event": "the banner hangs still; label scripted input"}, {"at": at("B40", "When the player"), "event": "the handler lines highlighted"}, {"at": at("B40", "The banner snaps"), "event": "the click lands; the banner waves, then settles"}],
    "manim: a timeline with an event marker", "Cause (the click) and effect (the wave that dies down) together, with the scripted input labelled, are the whole point of a uniform you drive.",
    f"C40: {SCENES}/scene_c40_wind_click.gd. Banner (13-banner, wind 0.0) centred (0.50, 0.50) at 0.55 of the width; one scripted left click pushed at frame 135 (4.5 s) sets wind to 1.0 and tweens it to 0.0 over 4.0 s. 14 s, 30 fps, Forward+. The label 'scripted input' is an overlay.",
    "verify4 and the Movie Maker run: the click reaches the handler in the same frame; the banner's wave falls 19, 17, 14, 11, 8, 5, 2, 0 px peak to peak across the four seconds",
    code='func _unhandled_input(event):\n\tif event is InputEventMouseButton and event.pressed:\n\t\tvar m = banner.material\n\t\tm.set_shader_parameter("wind", 1.0)\n\t\tcreate_tween().tween_property(m, "shader_parameter/wind", 0.0, 4.0)',
    code_file="scene script (GDScript)",
    cues=[{"at": at("B40", "When the player"), "lines": [4, 5]}],
    readouts=[{"at": 0.02, "text": "scripted input", "x": 0.5, "y": 0.06}], caption="tween: Godot's way to change a value smoothly over time from GDScript")

# ═════════════════════════════ write lanes + SHOTLIST ═════════════════════════════
for e in E:
    pr = e["entry"].get("props", {}) if isinstance(e["entry"].get("props", {}), dict) else {}
    for c in pr.get("cues", []) if isinstance(pr.get("cues"), list) else []:
        if isinstance(c, dict) and "label" in c:
            assert len(c["label"]) <= 60, (e["bid"], c["label"], len(c["label"]))
    if e["entry"].get("pattern") == "ShaderLab":
        assert len(pr.get("caption", "")) <= 80, (e["bid"], pr.get("caption"))
(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(len(N.ACTS)):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

ids = [e["bid"] for e in E]
assert ids == [bid for bid, _, _ in N.BODY], "lane entries must follow the body beat order exactly"
lanes_hist = {}
for e in E:
    lanes_hist[e["entry"]["lane"]] = lanes_hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
sl = ["# Shot list: Time and Waves\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab render or a scene capture of a tested file in `lab-shaders/`; no editor frame is needed. Six things must exist before the build (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component with `layout` `side`, `video` and `code` (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`; B17 uses the `code` layout). 2. **`shader_kit.py`** Manim helpers (`plot`, `ramp_strip`, `ramp_marker`, `pixel_grid`; same file). "
      "3. **Capture harness** `lab/capture.gd` + `capture_shader.sh`, plus support for the eight **scene scripts** (ten captures) in `evidence/planning-checks/scene-project/scenes/` (a scene root script, a frame counter, a scripted click, `Engine.time_scale`, `paused`, a CurveTexture made in code; every one already runs under Movie Maker at 30 fps: `scene-project/logs/`). "
      "4. **Film-local Manim helpers** (not in the shared kit; promote them if another film wants them): `knob_slider(label, lo, hi)` for B14 to B16 and B30, `time_ruler(label, zero_offset)` for B05 and B06, `curve_strip(curve)` for B22 and B24, `bracket(a, b, label)`. "
      "5. **Docs screenshot D1** for B02 via Playwright. 6. **No editor frames**: nothing in this film shows the Inspector (B22 to B24 show the CurveTexture as an idea and a script-made resource).\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
