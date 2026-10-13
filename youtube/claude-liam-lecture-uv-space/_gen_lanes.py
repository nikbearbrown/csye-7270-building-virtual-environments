#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md (same approach as the pilot film).

Why a generator: the code shown on screen must be the tested file text, and the shot list must say exactly what the lanes say.
Re-run after any edit:
    python3 _gen_lanes.py && python3 make_sheet.py
Never re-run make_sheet.py after `art final` (it clears build stamps).
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
spec = importlib.util.spec_from_file_location("narration", HERE / "narration.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
WORDS = {bid: len(t.split()) for bid, _, t in N.BODY}
E = []          # entries in beat order

SPR = "Godot 4.7.2 · Forward+ · Sprite2D · scripted values"
RECT = "Godot 4.7.2 · Forward+ · full-window ColorRect · 640 × 360"
QUAD = [0.275, 0.1, 0.725, 0.9]            # the sprite's square (0.8 of the window height) inside a 16:9 capture window
QUAD_TL = [0.275, 0.1, 0.5, 0.5]           # its top-left quarter


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def secs(bid):
    return round(WORDS[bid] * 0.34, 1)


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects)"):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, ramp=None, title=None, code=None, code_file=None, lane="capture", caption="", sparse=False, sparse_reason=None):
    props = {"layout": layout, "code": code if code is not None else (code_of(shader) if shader else ""),
             "codeFile": code_file or (f"lab-shaders/{shader}" if shader else ""), "cues": cues,
             "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption,
             "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    entry = {"lane": lane, "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": intent,
             "motion_claim": motion, "show": show, "runner_up": runner, "why": why, "sparse": sparse}
    if sparse_reason:
        entry["sparse_reason"] = sparse_reason
    add(bid, act, about, entry, evidence)


def rem(bid, act, about, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, act, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


# ═════════════════════════════ ACT I · The Address Book ═════════════════════════════
lab("B01", 0, "the hook: one picture slides, shrinks and repeats", "01-hook-controls.gdshader", "uv-space/c01-hook.mp4",
    "Godot 4.7.2 · Forward+ · same picture, same file · scripted values", [],
    "Act title 'The Address Book' (serif 40) top-left. A real Godot render in a framed window on the stage: the teal test sprite sits still, then slides left and wraps around, then shrinks into a three by three grid of copies. Label: 'same picture, same file'.",
    "The picture slides, then shrinks and tiles, while the label says the file never changes.",
    [{"at": 0.0, "event": "the sprite at rest, window labelled"}, {"at": 0.19, "event": "the picture slides left and wraps"}, {"at": 0.3, "event": "it shrinks into a three by three grid (settled by 0.42)"}],
    "manim drawing of a picture moving behind a window", "A real render is the honest picture of 'the same picture, a different look'; a drawing would only claim it.",
    f"C01: Lab sprite (--sprite-tex white) with --tex pic=sprite, lab-shaders/01-hook-controls.gdshader. Keyframes as fractions of the beat length L (about {secs('B01'):g} s): shift = 0 until 0.17 L, then 0 to 1.0 over 0.17-0.28 L, hold; zoom = 1 until 0.28 L, then 1 to 3 over 0.28-0.42 L, hold. Render L + 1 s, 30 fps, Forward+, no input. End state (shift 1.0, zoom 3.0): nine whole copies, aligned (probes hook-tiled-fill).",
    "Lab render (C01); Lab probes hook-start / hook-one-wrap / hook-tiled", layout="video", title="The Address Book",
    caption="same picture, same file")
manim("B02", 0, "every pixel has an address: U across, V down, zero to one", "AddressSquare",
      "A square with U labelled along the top (a drawn arrow pointing right) and V labelled down the left side (a drawn arrow pointing down), corner labels (0, 0) at the top left and (1, 1) at the bottom right, and a terracotta dot whose live (u, v) label updates as it moves. Caption (GLOSSARY wording): 'UV: a point's address on the shape: 0 to 1 across, 0 to 1 down'.",
      "The dot slides across (U grows), then down (V grows), then jumps to the top-left corner and to the bottom-right corner, its label updating each time.",
      [{"at": 0.1, "event": "square, axes, U and V labels"}, {"at": 0.28, "event": "dot slides across: U grows"}, {"at": 0.38, "event": "dot slides down: V grows (settled by 0.45)"},
       {"at": 0.66, "event": "dot at the top left, label (0, 0)"}, {"at": 0.84, "event": "dot at the bottom right, label (1, 1)"}],
      "ShaderLab with the address-map render", "A square you can point at, with a dot whose label updates, makes 'two numbers, zero to one, V down' concrete; the real render of the same idea comes next (B04).",
      "Lab probes uv-map-rect (corners 0.02/0.02 and 0.98/0.98), Godot docs ('UV varies between 0-1 from left-right and from top-bottom')")
manim("B03", 0, "V counts down; the range ignores size", "AnySize",
      "Two squares side by side, one small and one large, both labelled with the same corner values (0, 0) and (1, 1) and both carrying a dot at (0.5, 0.8) with an identical label. A grey up arrow marked 'school graph' beside the small square and a terracotta down arrow marked 'V' beside the large one. Caption: 'fraction, not pixels'.",
      "The grey up arrow appears and is replaced by the terracotta down arrow; then the large square grows beside the small one and its dot lands on the same label.",
      [{"at": 0.12, "event": "square with the school-graph up arrow, then the V down arrow"}, {"at": 0.4, "event": "the second, larger square, same corner labels"},
       {"at": 0.66, "event": "both dots at (0.5, 0.8), same label"}, {"at": 0.84, "event": "caption: fraction, not pixels"}],
      "LectureEvidenceTable of three shape sizes", "Two squares of different size carrying identical corner labels show 'a fraction, not a pixel count' at a glance; a table would only list it.",
      "Lab probes uv-map-rect-320x180 / 640x360 / 1280x720 / 640x320 (same colours at the same positions)")
lab("B04", 0, "every address at once, drawn as a color", "02-address-map.gdshader", "uv-space/c02-address-map.png", SPR.replace("scripted values", "still"),
    [{"at": 0.1, "lines": [4]}, {"at": 0.3, "lines": [4], "label": "red = U"}, {"at": 0.62, "lines": [4], "label": "green = V"}, {"at": 0.74, "lines": [4], "label": "blue = half"}],
    "Code card at left with the one-line address-map shader; at right a real Godot window with a centered square showing the red-green picture (red grows to the right, green grows downward, blue held at half), corner labels outside the square landing in turn: (0, 0), (1, 0), (0, 1), (1, 1).",
    "The corner labels land with the words: red grows to the right (top right), green grows downward (bottom left).",
    [{"at": 0.1, "event": "COLOR line highlighted; the address picture on screen"}, {"at": 0.3, "event": "(0, 0) and (1, 0): red grows to the right"}, {"at": 0.62, "event": "(0, 1) and (1, 1): green grows downward"}, {"at": 0.74, "event": "blue held at half"}],
    "manim: a UV square drawn with a colour gradient", "The address map is Godot's own picture of UV (the Godot tutorial's first UV example); the render is the evidence, the Manim square already carried the numbers.",
    "C02: Lab sprite (--sprite-tex white), lab-shaders/02-address-map.gdshader, still PNG 3840x2160 (16:9 window, the square quad centered at 0.45 of the width). Corner colours (probes): top left (0.02, 0.02, 0.50), top right (0.98, 0.02, 0.50), bottom left (0.02, 0.98, 0.50), bottom right (0.98, 0.98, 0.50).",
    "Lab probes uv-map-rect / uv-map-sprite-fill",
    readouts=[{"at": 0.3, "text": "(0, 0)", "x": 0.22, "y": 0.06}, {"at": 0.3, "text": "(1, 0)", "x": 0.78, "y": 0.06}, {"at": 0.62, "text": "(0, 1)", "x": 0.22, "y": 0.94}, {"at": 0.64, "text": "(1, 1)", "x": 0.78, "y": 0.94}])
manim("B05", 0, "the lookup: a pixel asks the picture for the color at its address", "Lookup",
      "Left, a small grid of outline pixel cells labelled 'the shape' with one cell ringed in terracotta and tagged with its address (0.7, 0.5); right, the picture (a cream card with the teal test sprite) labelled 'TEXTURE: the node's own picture' (GLOSSARY wording). An arrow runs from the ringed pixel to the same relative spot on the picture, where a terracotta dot lands; a teal swatch travels back along the arrow and the ringed pixel fills with teal. Small tag on the arrow: 'texture()'.",
      "An arrow goes out from the pixel to a spot on the picture, and the color found there travels back and fills the pixel.",
      [{"at": 0.12, "event": "pixel ringed, address tag"}, {"at": 0.3, "event": "arrow reaches the picture; dot lands"}, {"at": 0.62, "event": "teal swatch returns along the arrow"}, {"at": 0.8, "event": "the pixel is filled teal"}],
      "DesignPipelineClaim, show-tell isometric", "A lookup is a question going out and a colour coming back; a drawn arrow and a returning swatch say exactly that, with the pixel and the picture both visible.",
      "Godot 4.7 shader functions reference ('Retrieves texels from a texture'); Lab probes lookup-sprite-fill")
lab("B06", 0, "the lookup left alone: the picture comes out as it went in", "03-lookup.gdshader", "uv-space/c03-lookup.mp4", SPR,
    [{"at": 0.1, "lines": [3]}, {"at": 0.36, "lines": [4], "label": "TEXTURE: the node's own picture"}, {"at": 0.64, "lines": [4], "label": "COLOR: the color of the pixel being drawn"}],
    "Code card at left with the three-line lookup shader; at right a real Godot window showing the test sprite drawn plainly, with no shader. At 'Nothing is changed' the lookup shader is switched on and the picture does not change at all. A caption defines fragment (GLOSSARY wording): 'fragment(): runs once for each pixel the shape covers; sets its color'. Readout 'shader on' at the switch; then a terracotta ring settles on the sprite's square with the readout 'unchanged'.",
    "The shader switches on and nothing changes: the picture is pixel for pixel the same.",
    [{"at": 0.1, "event": "function line: runs once for every pixel the shape covers"}, {"at": 0.36, "event": "COLOR line: TEXTURE is the node's own picture; read it at the pixel's own address"}, {"at": 0.6, "event": "the lookup shader switches on (readout 'shader on'); COLOR defined"}, {"at": 0.78, "event": "ring on the picture: unchanged"}],
    "LectureCodeTrace alone", "The line and its unchanged result side by side is the claim, and watching the shader switch on with no change is the proof; a code trace alone would not show 'comes out as it went in'.",
    f"C03: Lab sprite (--sprite-tex sprite). No material until 0.58 L, then --material-at assigns lab-shaders/03-lookup.gdshader; the picture must not change. Render L + 1 s (L about {secs('B06'):g} s), 30 fps, Forward+. Verified: with the shader and without it, 0 of 230,400 pixels differ, largest channel difference 0.0 (verify-identity.gd D1). Probes (fill-window): middle (0.372, 0.639, 0.569) teal, eyes (0.980, 0.977, 0.961) at (0.4, 0.44) and (0.6, 0.44), corner (0.851, 0.835, 0.792) = stage.",
    "verify-identity.gd D1 (0 pixels differ) and D2 (the unbent template too); Lab probes lookup-sprite-fill; Godot docs (fragment runs for every pixel covered by the mesh)",
    rings=[{"at": 0.78, "box": QUAD}], readouts=[{"at": 0.6, "text": "shader on", "x": 0.35, "y": 0.95}, {"at": 0.78, "text": "unchanged", "x": 0.65, "y": 0.95}],
    caption="fragment(): runs once for each pixel the shape covers; sets its color")
manim("B07", 0, "the shape is a window onto a fixed picture", "Window",
      "Left, a large cream card labelled 'the picture' holding the teal test sprite and a small terracotta tick at its top-left corner; over it a terracotta-outlined rectangle labelled 'the shape'. Right, a framed panel labelled 'what you see' showing the part of the picture inside the outline. Caption: 'address moves it'.",
      "The outlined window slides right across the fixed picture while the panel's contents shift left, then it slides back.",
      [{"at": 0.1, "event": "picture card, window outline, panel"}, {"at": 0.3, "event": "window slides right; panel content shifts left"}, {"at": 0.72, "event": "window slides back; caption lands"}],
      "ShaderLab: a real render with the quad ringed", "'The shape is a window' is an analogy; only a drawing can slide a window over a fixed picture and show the contents change.",
      "Manim only (shader_kit objects); the effect itself is measured in Act II (Lab probes shift-x)")
rem("B08", 0, "copy, bend, look up: the three-line pattern", "LectureCodeTrace",
    {"title": "Copy, bend, look up", "code": code_of("04-copy-bend-look.gdshader"), "note": "UV is read-only in fragment() · Godot 4.7 documentation, checked in Godot 4.7.2",
     "cues": [0.04, 0.04, 0.1, 0.31, 0.42, 0.58, 0.58], "durationSeconds": "__AUDIO__"},
    "A cream code card with the real seven-line template; focus lands on the function, then the copy line, then the empty bend line, then the lookup line as each is named.",
    "Line focus steps through copy, bend, look up on the words.",
    [{"at": 0.1, "event": "fragment: the address is read-only"}, {"at": 0.31, "event": "copy the address"}, {"at": 0.42, "event": "bend the copy"}, {"at": 0.58, "event": "look up with the copy"}],
    "ClaudeCodeBeat", "Paced line focus lands on 'copy', 'bend', 'look up' as each is spoken; the pattern is real, compiled code.",
    "Lab compile of 04-copy-bend-look; Lab run uv-write-error (UV *= 2.0 fails: 'Constants cannot be modified.'); Godot docs ('In the fragment function you can only read from UV')")

# ═════════════════════════════ ACT II · Move Where You Look ═════════════════════════════
lab("B09", 1, "subtract a quarter from U: the picture slides right", "05-shift-x.gdshader", "uv-space/c04-shift-x.mp4", SPR,
    [{"at": 0.1, "lines": [7]}, {"at": 0.72, "lines": [7], "label": "picture goes right"}],
    "Act title 'Move Where You Look' (serif 40) top-left. Code card at left with the shift shader; at right a real Godot window: the teal test sprite sits still while the voice asks which way it will go, then, on 'Watch', slides right inside its square while the readout counts amount 0 to 0.25. A terracotta ring marks the sprite's fixed square.",
    "The picture slides right, clipped by the square's edge, though the code subtracts.",
    [{"at": 0.1, "event": "subtract line highlighted; amount = 0; ring on the fixed square"}, {"at": 0.52, "event": "the slide begins on 'Watch' (video, no cue)"}, {"at": 0.72, "event": "amount = 0.25; the picture is a quarter to the right"}],
    "manim: the window slides over the picture (as B07)", "A real render of a surprising result (subtract, and it moves right) beats a drawing: the viewer predicts, then sees the real picture move.",
    f"C04: Lab sprite (--sprite-tex sprite), lab-shaders/05-shift-x.gdshader. Keyframes (L about {secs('B09'):g} s): amount = 0 until 0.52 L, then 0 to 0.25 over 0.52-0.72 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.3, 0.5) stage, (0.9, 0.5) teal, eyes at (0.65, 0.44) and (0.85, 0.44).",
    "Lab probes shift-x-0.25-sprite-fill (and the gradient version: red 0.243 at the middle)",
    title="Move Where You Look", rings=[{"at": 0.1, "box": QUAD}],
    readouts=[{"at": 0.1, "text": "amount = 0", "x": 0.5, "y": 0.95}, {"at": 0.72, "text": "amount = 0.25", "x": 0.5, "y": 0.95}])
manim("B10", 1, "worked numbers: the middle pixel reads 0.25 and shows what lives there", "WorkedNumbers",
      "Two horizontal rulers from 0 to 1 with ticks at 0, 0.25, 0.5, 0.75, 1: the top one labelled 'the picture' with a teal dot at 0.25, the bottom one labelled 'the shape' with a terracotta pixel marker at 0.5. An arrow runs from the pixel marker up to 0.25 on the picture ruler (tag 'looks up 0.25'), and the teal dot then slides down the arrow to land at 0.5 on the shape ruler (tag 'lands at 0.5').",
      "The pixel at 0.5 reaches back to 0.25, and the teal dot found there lands at 0.5: everything moved a quarter right.",
      [{"at": 0.12, "event": "rulers, ticks, the teal dot at 0.25"}, {"at": 0.3, "event": "pixel marker at 0.5; arrow back to 0.25"}, {"at": 0.62, "event": "the dot lands at 0.5"}, {"at": 0.8, "event": "tag: a quarter right"}],
      "LectureEvidenceTable of the lookup", "Two rulers with an arrow from 0.5 back to 0.25 turn the worked numbers into motion: the feature slides to where it lands.",
      "Lab probes shift-x-0.25-gradient-fill (middle reads red 0.243, the nearest texel to 0.25) and shift-x-0.25-sprite-fill")
manim("B11", 1, "the rule: change the address one way, the picture goes the other", "Reversal",
      "Two stacked horizontal rulers as in the previous drawing: the picture (with a teal dot) above, what the shape shows below. First a terracotta arrow pointing right labelled 'subtract from U' with the dot moving right on the lower ruler; then an arrow pointing left labelled 'add to U' with the dot moving left. Persistent small tag: 'the opposite way'.",
      "On 'subtract' the dot moves right; on 'add' it moves left, always against the arrow.",
      [{"at": 0.12, "event": "rulers and dot at rest"}, {"at": 0.3, "event": "subtract: arrow right, dot moves right"}, {"at": 0.68, "event": "add: arrow left, dot moves left"}],
      "ShaderLab with both signs swept", "Both directions side by side with opposing arrows is the rule itself; the real render of one direction was the previous beats.",
      "Lab probes shift-x-0.25 (picture right) and shift-x-neg0.25-gradient-fill (picture left: middle reads 0.745)")
lab("B12", 1, "the same for V, which counts downward: subtract from both", "06-shift-xy.gdshader", "uv-space/c05-shift-xy.mp4", SPR,
    [{"at": 0.1, "lines": [8]}, {"at": 0.34, "lines": [8], "label": "down"}, {"at": 0.72, "lines": [8], "label": "right and down"}],
    "Code card at left with the two-shift shader; at right a real Godot window where the teal sprite first slides straight down inside its fixed square (shift_y from 0 to 0.25), then also slides right (shift_x from 0 to 0.25), ending right and down. Two readouts count the shifts.",
    "The picture slides down first, then right as well.",
    [{"at": 0.1, "event": "uv -= vec2(shift_x, shift_y) highlighted"}, {"at": 0.36, "event": "the picture slides straight down"}, {"at": 0.66, "event": "it slides right as well: right and down"}],
    "manim: a diagonal arrow", "V's downward direction is the surprise; the real sprite sliding down, then right too, shows it on the real picture in the order the voice says it.",
    f"C05: Lab sprite (--sprite-tex sprite), lab-shaders/06-shift-xy.gdshader. Keyframes (L about {secs('B12'):g} s): shift_y = 0 until 0.36 L, then 0 to 0.25 over 0.36-0.56 L, hold; shift_x = 0 until 0.66 L, then 0 to 0.25 over 0.66-0.86 L, hold. Render L + 1 s, 30 fps, Forward+. Probes (fill-window): shift_y only: eyes cream at (0.4, 0.69) and (0.6, 0.69), (0.4, 0.44) stage; both: eyes at (0.65, 0.69) and (0.85, 0.69).",
    "Lab probes shift-y-0.25-sprite-fill / shift-xy-0.25-sprite-fill / shift-xy-0.25-gradient-fill (both channels read 0.243)",
    rings=[{"at": 0.1, "box": QUAD}], readouts=[{"at": 0.6, "text": "shift_y = 0.25", "x": 0.5, "y": 0.95}, {"at": 0.88, "text": "shift_x = 0.25", "x": 0.5, "y": 0.95}])
lab("B13", 1, "scale by two: the picture shrinks into the top-left corner", "07-scale.gdshader", "uv-space/c06-scale.mp4", SPR,
    [{"at": 0.1, "lines": [6]}, {"at": 0.58, "lines": [6], "label": "zoom = 2"}],
    "Code card at left with the scale shader; at right a real Godot window where the teal sprite shrinks, pinned toward the top left of its fixed square, as zoom grows from 1 to 2. A terracotta ring settles on the top-left quarter of the square (readout 'one quarter'), then on the empty rest (readout 'nothing to read').",
    "The picture shrinks toward the top-left corner and ends in the quarter of its square.",
    [{"at": 0.1, "event": "uv = UV * zoom highlighted"}, {"at": 0.2, "event": "shrinking begins (video)"}, {"at": 0.58, "event": "zoom = 2: the picture fills the top-left quarter"}, {"at": 0.64, "event": "ring on the quarter"}, {"at": 0.82, "event": "ring on the empty rest"}],
    "manim: a ramp doubling", "The picture shrinking into the corner as the dial turns is the claim; the explanation gets its own drawing next (B14).",
    f"C06: Lab sprite (--sprite-tex sprite), lab-shaders/07-scale.gdshader. Keyframes (L about {secs('B13'):g} s): zoom = 1 until 0.12 L, then 1 to 2 over 0.12-0.45 L, hold. Render L + 1 s, 30 fps, Forward+. End state: blob area = 0.2506 of the zoom-1 area (22,865 to 5,731 teal pixels, 640x360 look run), blob centre at (0.25, 0.25) of its square.",
    "Lab probes scale-2-sprite-fill; measure.py bbox scale-1 / scale-2 (area ratio 0.2506)",
    rings=[{"at": 0.1, "box": QUAD}, {"at": 0.64, "box": QUAD_TL}, {"at": 0.82, "box": [0.5, 0.1, 0.725, 0.9]}],
    readouts=[{"at": 0.58, "text": "zoom = 2", "x": 0.5, "y": 0.95}, {"at": 0.66, "text": "one quarter", "x": 0.37, "y": 0.3}, {"at": 0.84, "text": "nothing to read", "x": 0.62, "y": 0.5}])
manim("B14", 1, "why smaller: the shape now spans addresses zero to two", "WhySmaller",
      "Two equal-length horizontal rulers: the top one labelled 'the shape' from 0 to 1, the bottom one labelled 'the address' whose scale grows from 0-1 to 0-2 as the dial turns. The first half of the address ruler (0 to 1) is filled teal and labelled 'the picture'; the second half (1 to 2) is grey and labelled 'no picture'. A dashed vertical line joins the middle of the shape ruler to 1 on the address ruler.",
      "The address ruler's labels stretch from 0-1 to 0-2, the teal part is squeezed into the left half and the dashed line lands on 1 at the middle.",
      [{"at": 0.12, "event": "the two rulers, the picture filling the address ruler"}, {"at": 0.3, "event": "the address labels grow to 0-2; teal squeezes to the left half"}, {"at": 0.66, "event": "dashed line from the middle to address 1; 'no picture' on the right half"}],
      "ShaderLab with an address ramp underneath", "Two rulers (shape position, address) with the picture's extent marked show why only half of each side is filled; a real render shows the shrinking but not the numbers.",
      "Lab probes scale-address-as-colour (UV * 2: the ramp fills the top-left quarter, then reads 1.0) and scale-2-sprite-fill")
lab("B15", 1, "beyond one: edge pixels, or repeat when asked", "09-tile.gdshader", "uv-space/c07-repeat.mp4", SPR.replace("Sprite2D", "Sprite2D + texture uniform"),
    [{"at": 0.12, "lines": [8], "label": "outside: edge pixels"}, {"at": 0.4, "lines": [3], "label": "repeat enable"}, {"at": 0.74, "lines": [7], "label": "zoom = 3"}],
    "Code card at left with the tile shader; at right a real Godot window where the sprite first shrinks alone into the top-left quarter (nothing repeats), then, when the repeat switch comes on, the copies appear at once as a two by two grid and grow to three by three as zoom reaches 3.",
    "The empty space fills with copies the moment repeat switches on.",
    [{"at": 0.12, "event": "default: the lookup returns edge pixels (the quarter stays alone)"}, {"at": 0.4, "event": "repeat enable highlighted"}, {"at": 0.6, "event": "copies appear (material switches)"}, {"at": 0.74, "event": "zoom 3: a three by three grid"}],
    "LectureCodeTrace for the one hint line", "The switch from no-repeat to repeat in the same render is the event; the copies appear at the moment the voice says the picture starts over.",
    f"C07: Lab sprite (--sprite-tex white) with --tex pic=sprite. Material A (lab-shaders/08-tile-no-repeat.gdshader) until 0.60 L, then --material-at assigns material B (lab-shaders/09-tile.gdshader). Keyframes (L about {secs('B15'):g} s): zoom = 1 until 0.02 L, then 1 to 2 over 0.02-0.30 L, hold at 2 until 0.72 L, then 2 to 3 over 0.72-0.84 L, hold. Render L + 1 s, 30 fps, Forward+. Probes: no-repeat at zoom 2 shows one blob in the top-left quarter and stage elsewhere; repeat at zoom 3 shows nine teal centres.",
    "Lab probes tile-no-repeat-2-sprite-fill / tile-2-sprite-fill / tile-3-sprite-fill (and the gradient pair: 1.000 against 0.247 at address 1.254)",
    rings=[{"at": 0.64, "box": QUAD}])
rem("B16", 1, "the node's own texture has the same switch: texture_repeat", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/classes/class_canvasitem.html#enum-canvasitem-texturerepeat",
     "image": "uv-space/docs-canvasitem-texturerepeat.png", "caption": "Godot 4.7 documentation · CanvasItem · TextureRepeat · captured at build time",
     "frame": "browser", "moves": [{"at": 0, "x": 0.5, "y": 0.3, "scale": 1}, {"at": 0.2, "x": 0.45, "y": 0.4, "scale": 1.6, "ring": [0.05, 0.36, 0.9, 0.07]},
                                    {"at": 0.62, "x": 0.45, "y": 0.5, "scale": 1.6, "ring": [0.05, 0.5, 0.9, 0.09]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 CanvasItem page scrolled to the TextureRepeat list in a browser window; the camera pushes in on TEXTURE_REPEAT_ENABLED, a terracotta ring marks it, then it moves to TEXTURE_REPEAT_MIRROR. (Ring fractions are estimates: the build sets them from the real capture.)",
    "The camera pushes in on the line the voice names, then moves to the mirror line.",
    [{"at": 0, "event": "the page at the TextureRepeat enum"}, {"at": 0.2, "event": "push-in and ring on TEXTURE_REPEAT_ENABLED"}, {"at": 0.62, "event": "ring on TEXTURE_REPEAT_MIRROR"}],
    "LectureCodeTrace: texture_repeat = TEXTURE_REPEAT_ENABLED", "The setting is documented API: the real docs page shows the list and its wording; no editor frame is invented.",
    "D1: Playwright capture of the live docs page (1600x900 at 2.4x) at build time; read 2026-10-13. Measured: verify-repeat.gd R1 (Sprite2D) and R2 (TextureRect) in evidence/planning-checks")
lab("B17", 1, "add TIME times a tenth: the picture scrolls left", "10-scroll.gdshader", "uv-space/c08-scroll.mp4", SPR.replace("scripted values", "live TIME").replace("Sprite2D", "Sprite2D + texture uniform"),
    [{"at": 0.16, "lines": [7], "label": "TIME * 0.1"}, {"at": 0.72, "lines": [7], "label": "scrolls left"}],
    "Code card at left with the scroll shader; at right a real Godot window where the sprite grid slides steadily to the left and wraps around forever. A caption defines TIME (GLOSSARY wording): 'TIME: seconds on one clock shared by the whole game'.",
    "The grid slides left at a steady speed, a tenth of a picture each second.",
    [{"at": 0.16, "event": "uv.x += TIME * 0.1 highlighted"}, {"at": 0.72, "event": "scrolls left, a tenth of its width per second"}],
    "manim: a ruler sliding", "A live TIME scroll is the claim; the code line and the moving picture together.",
    f"C08: Lab sprite (--sprite-tex white) with --tex pic=sprite, lab-shaders/10-scroll.gdshader, live TIME, repeat enabled by the shader, zoom fixed by the sprite fit (the picture repeats once per quad width). Render L + 1 s (L about {secs('B17'):g} s), 30 fps, Forward+. Measured: the picture position under a fixed pixel advances about 0.10 per second (run-3-scroll.log: 0.100 on each of three steps; an earlier run read 0.095 to 0.105).",
    "run-3-scroll.log (single process: 0.1 pictures per second, direction left); Lab compile 10-scroll",
    caption="TIME: seconds on one clock shared by the whole game")
rem("B18", 1, "four moves: subtract, add, multiply up, multiply down", "LectureEvidenceTable",
    {"title": "Four moves", "headers": ["Change the address", "The picture"],
     "rows": [["subtract from U", "moves right"], ["add to U", "moves left"], ["multiply by more than one", "shrinks"], ["multiply by less than one", "grows"]],
     "note": "Measured in Godot 4.7.2 · Forward+ · always the opposite of the address", "cues": [0.1, 0.28, 0.42, 0.64], "durationSeconds": "__AUDIO__"},
    "A four-row table, one row ringed as each move is named.", "The ring steps down the four rows with the voice.",
    [{"at": 0.1, "event": "subtract row"}, {"at": 0.28, "event": "add row"}, {"at": 0.42, "event": "multiply by more than one row"}, {"at": 0.64, "event": "multiply by less than one row"}],
    "manim: four arrows", "Four parallel move-and-effect facts: the table component is built for exactly that.",
    "Lab probes shift-x / shift-x-neg0.25 / scale-2 / zoom-0.5-corner (rows 3 and 4 are shown in the next act)")

# ═════════════════════════════ ACT III · Center and Mirror ═════════════════════════════
lab("B19", 2, "scale by one half: the picture swells away from the corner", "07-scale.gdshader", "uv-space/c09-corner-zoom.mp4", SPR,
    [{"at": 0.1, "lines": [6]}, {"at": 0.82, "lines": [6], "label": "toward the corner"}],
    "Act title 'Center and Mirror' (serif 40) top-left. Code card at left with the scale shader; at right a real Godot window where, as zoom falls from 1 to 0.5, the sprite swells and slides toward the bottom right of its fixed square until only an arc with one eye remains.",
    "The picture grows but drifts away from the top left corner and out of frame.",
    [{"at": 0.1, "event": "uv = UV * zoom highlighted"}, {"at": 0.3, "event": "zoom falls to 0.5; the picture swells toward the bottom right"}, {"at": 0.82, "event": "an arc and one eye remain: toward the corner"}],
    "manim: the corner pivot (B20)", "The unwelcome result (the picture swelling out of frame) is best seen on the real picture before the explanation.",
    f"C09: Lab sprite (--sprite-tex sprite), lab-shaders/07-scale.gdshader. Keyframes (L about {secs('B19'):g} s): zoom = 1 until 0.24 L, then 1 to 0.5 over 0.24-0.66 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.5, 0.5) stage, (0.9, 0.9) teal, (0.8, 0.88) cream (the left eye).",
    "Lab probes zoom-0.5-corner-sprite-fill",
    title="Center and Mirror", rings=[{"at": 0.1, "box": QUAD}], readouts=[{"at": 0.3, "text": "zoom = 0.5", "x": 0.5, "y": 0.95}])
manim("B20", 2, "scaling pivots on zero: corner against middle", "Pivot",
      "Two side-by-side panels. Left, labelled 'corner is zero': a small pattern (a cream square with the teal sprite icon) at the panel's top-left corner with a terracotta pivot dot on the corner. Right, labelled 'middle is zero': the same pattern centered with the pivot dot at its middle. Tag on each pivot: 'zero'.",
      "On the left the pattern grows away from the corner; on the right the same pattern grows in place.",
      [{"at": 0.1, "event": "left panel with the pivot at the corner"}, {"at": 0.25, "event": "the pattern scales up, away from the corner"}, {"at": 0.62, "event": "right panel with the pivot in the middle"}, {"at": 0.76, "event": "the same pattern scales in place"}],
      "ShaderLab with an overlay dot at zero", "Scaling about two different pivots side by side is a geometric mechanism; only a drawing can show the same pattern growing away from the corner and in place.",
      "Lab probes zoom-0.5-corner (picture centre moves toward the bottom right) and zoom-0.5-centered (centre stays)")
lab("B21", 2, "subtract a half, scale, add the half back: zoom in place", "11-zoom-centered.gdshader", "uv-space/c10-centered-zoom.mp4", SPR,
    [{"at": 0.1, "lines": [6], "label": "subtract a half"}, {"at": 0.4, "lines": [6], "label": "scale"}, {"at": 0.58, "lines": [6], "label": "add it back"}],
    "Code card at left with the centered zoom shader; at right a real Godot window where, as zoom falls from 1 to 0.5, the sprite grows in place around the middle of its square until the two eyes are large.",
    "The picture grows around its own middle and stays put.",
    [{"at": 0.1, "event": "subtract a half"}, {"at": 0.4, "event": "scale"}, {"at": 0.58, "event": "add it back; then the picture grows in place"}],
    "LectureCodeTrace on the one line", "The fix on the same picture, side by side with the corner version: it now grows in place, with the line in view.",
    f"C10: Lab sprite (--sprite-tex sprite), lab-shaders/11-zoom-centered.gdshader. Keyframes (L about {secs('B21'):g} s): zoom = 1 until 0.62 L, then 1 to 0.5 over 0.62-0.92 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.5, 0.5) teal, eyes at (0.3, 0.38) and (0.7, 0.38).",
    "Lab probes zoom-0.5-centered-sprite-fill / zoom-1-centered-sprite-fill",
    rings=[{"at": 0.1, "box": QUAD}], readouts=[{"at": 0.8, "text": "zoom = 0.5", "x": 0.5, "y": 0.95}])
manim("B22", 2, "centered coordinates: UV * 2 - 1 puts zero in the middle", "Centered",
      "A square with 0 to 1 labels at its corners, (0, 0) top left and (1, 1) bottom right. A tag 'x 2' then 'minus 1' appears; the labels animate to (-2..2) then to (-1, -1) top left, (1, -1) top right, (-1, 1) bottom left, (1, 1) bottom right, with a terracotta dot at the middle labelled (0, 0). The left half and the top half get a small 'negative' tag.",
      "The corner labels slide from 0-1 to minus one to one and the dot settles at the middle, labelled zero, zero.",
      [{"at": 0.1, "event": "the square with 0 to 1 labels"}, {"at": 0.28, "event": "labels double (x 2)"}, {"at": 0.38, "event": "labels shift (minus 1): minus one to one"}, {"at": 0.66, "event": "middle dot (0, 0); left and top tagged negative"}],
      "ShaderLab with the sign shader", "Labels morphing from 0..1 to minus one..one with the middle becoming zero is the transform; the sign shader adds nothing the labels do not already say.",
      "Lab probes centered-signs (quadrant colours) and centered-range (abs(p) is 0 in the middle, 1 at the edges)")
lab("B23", 2, "length is the distance from the middle: a circle is one comparison", "12-disc.gdshader", "uv-space/c11-disc.mp4", SPR.replace("Sprite2D", "Sprite2D (white square)"),
    [{"at": 0.1, "lines": [8], "label": "length: the length of a vector; of an offset, the distance"}, {"at": 0.42, "lines": [8], "label": "closer: inside"}, {"at": 0.82, "lines": [3], "label": "radius"}],
    "Code card at left with the disc shader; at right a real Godot window where a teal disc grows in the centered square as the radius readout sweeps from 0.15 to 0.8.",
    "The disc grows from the middle as the radius dial turns.",
    [{"at": 0.1, "event": "if (length(p) < radius) highlighted"}, {"at": 0.42, "event": "closer than the radius is inside"}, {"at": 0.82, "event": "the radius dial; radius = 0.8"}],
    "manim: a circle from a distance", "A disc growing as the radius sweeps, beside the one-line test, shows 'length is distance from the middle' on real pixels.",
    f"C11: Lab sprite (--sprite-tex white), lab-shaders/12-disc.gdshader. Keyframes (L about {secs('B23'):g} s): radius = 0.15 until 0.10 L, then 0.15 to 0.8 over 0.10-0.85 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.5, 0.5) and (0.85, 0.5) teal, (0.95, 0.5) and (0.9, 0.9) stage.",
    "Lab probes disc-0.8-sprite-fill; length-grey (length 0 in the middle, 1.0 at the edge midpoints, 1.41 in the corners)",
    readouts=[{"at": 0.82, "text": "radius = 0.8", "x": 0.5, "y": 0.95}])
lab("B24", 2, "one test finds only the right eye", "13-face-one-eye.gdshader", "uv-space/c12-one-eye.mp4", SPR.replace("Sprite2D", "Sprite2D (white square)"),
    [{"at": 0.12, "lines": [9], "label": "one eye test"}, {"at": 0.66, "lines": [9], "label": "second test?"}],
    "Code card at left with the one-eye shader; at right a real Godot window with a teal head and one white eye on the right; as eye x sweeps from 0.3 to 0.5 the right eye drifts outward and the left side stays empty. A terracotta ring on the empty left side with the readout 'nothing here'.",
    "The right eye moves; the left stays empty.",
    [{"at": 0.12, "event": "the eye test highlighted; one eye visible"}, {"at": 0.36, "event": "ring on the empty left side"}, {"at": 0.66, "event": "second test? highlighted"}],
    "manim: two circles, one crossed out", "One eye present and the other missing is the problem as it really looks.",
    f"C12: Lab sprite (--sprite-tex white), lab-shaders/13-face-one-eye.gdshader. Keyframes (L about {secs('B24'):g} s): eye_x = 0.3 until 0.30 L, then 0.3 to 0.5 over 0.30-0.75 L, hold. Render L + 1 s, 30 fps, Forward+. Probes (fill-window, eye_x 0.3): (0.65, 0.425) white, (0.35, 0.425) teal (head, no eye).",
    "Lab probes face-one-eye-fill / face-one-eye-wide-fill",
    rings=[{"at": 0.36, "box": [0.275, 0.25, 0.5, 0.6]}], readouts=[{"at": 0.36, "text": "nothing here", "x": 0.38, "y": 0.82}])
lab("B25", 2, "absolute value: one test draws both eyes", "14-face-two-eyes.gdshader", "uv-space/c13-two-eyes.mp4", SPR.replace("Sprite2D", "Sprite2D (white square)"),
    [{"at": 0.1, "lines": [7], "label": "drop the minus"}, {"at": 0.2, "lines": [7], "label": "minus becomes plus"}, {"at": 0.6, "lines": [10], "label": "both eyes"}],
    "Code card at left with the two-eye shader (one added line, p.x = abs(p.x)); at right the real Godot window: the head with one white eye, then, on 'the left half reads exactly like the right', the left eye appears and, as eye x sweeps from 0.3 to 0.5, the two eyes slide apart together. Readouts: '-0.3 to 0.3', then 'both eyes'.",
    "The left eye appears when abs is applied, and both eyes move apart together under one test.",
    [{"at": 0.1, "event": "p.x = abs(p.x) highlighted; one eye still"}, {"at": 0.2, "event": "minus 0.3 becomes 0.3"}, {"at": 0.44, "event": "the left eye appears (material switches)"}, {"at": 0.6, "event": "the eye test: one test, both eyes; the eyes slide apart"}],
    "LectureCodeTrace on the abs line", "The left eye appearing the moment abs is applied, then both eyes moving apart together, is the payoff of the previous beat.",
    f"C13: Lab sprite (--sprite-tex white). Material A (lab-shaders/13-face-one-eye.gdshader) until 0.44 L, then --material-at assigns material B (lab-shaders/14-face-two-eyes.gdshader). Keyframes (L about {secs('B25'):g} s): eye_x = 0.3 until 0.60 L, then 0.3 to 0.5 over 0.60-0.90 L, hold. Render L + 1 s, 30 fps, Forward+. Probes (fill-window): eye_x 0.3: (0.65, 0.425) and (0.35, 0.425) white; eye_x 0.5: (0.75, 0.425) and (0.25, 0.425) white.",
    "Lab probes face-one-eye-fill / face-two-eyes-fill / face-two-eyes-wide-fill; abs-fold-red (0.600 at 0.2 and at 0.8)",
    readouts=[{"at": 0.2, "text": "-0.3 to 0.3", "x": 0.5, "y": 0.95}, {"at": 0.84, "text": "both eyes", "x": 0.5, "y": 0.95}])
manim("B26", 2, "abs folds the shape down its middle", "Fold",
      "A square (the shape) with a dashed vertical line down its middle and two small white eye circles at minus 0.3 and 0.3 on a horizontal centered axis. The left half hinges over the dashed line and lands on the right half; the left eye lands exactly on the right eye. Tag: 'abs: fold'. A small caption 'mirror twins' lands at the end.",
      "The left half swings over the middle line and the left eye lands on the right eye.",
      [{"at": 0.12, "event": "the square, the centre line, two eyes at plus and minus 0.3"}, {"at": 0.3, "event": "the left half folds over the middle line"}, {"at": 0.4, "event": "the left eye lands on the right eye (settled by 0.45)"}, {"at": 0.74, "event": "caption: mirror twins"}],
      "ShaderLab with a fold marker", "Folding the shape down its middle is a geometric move; a drawing can show the left half landing on the right.",
      "Lab probes abs-fold-red (the same value at 0.2 and 0.8) and face-two-eyes-fill")
lab("B27", 2, "scale the centered address by minus one: the picture flips", "15-flip.gdshader", "uv-space/c14-flip.mp4", SPR,
    [{"at": 0.1, "lines": [6]}, {"at": 0.36, "lines": [6], "label": "flip = -1"}],
    "Code card at left with the flip shader; at right a real Godot window where the sprite sits upright, then at the words 'turns upside down' it flips in one step: the two eyes drop below the middle. Readouts 'flip = 1', then 'flip = -1', and a ring on the lowered eyes.",
    "The picture turns upside down in one step and the eyes land below the middle.",
    [{"at": 0.1, "event": "the scale line highlighted; flip = 1; upright"}, {"at": 0.36, "event": "flip = -1; the picture turns upside down"}, {"at": 0.58, "event": "ring on the lowered eyes"}],
    "manim: the sprite icon mirrored across a line", "The real picture turns upside down at the moment the scale becomes minus one; the eyes dropping below the middle is checkable.",
    f"C14: Lab sprite (--sprite-tex sprite), lab-shaders/15-flip.gdshader. Keyframes (L about {secs('B27'):g} s): flip = 1 until 0.34 L, then a one-frame step to -1, hold. Render L + 1 s, 30 fps, Forward+. Probes (fill-window): flip 1: eye at (0.4, 0.44); flip -1: eyes at (0.4, 0.56) and (0.6, 0.56), (0.4, 0.44) teal. (A sweep through zero is NOT used: at flip 0 the picture is one stretched row, see flip-v-0-look.)",
    "Lab probes flip-v-1 / flip-v-neg1 (sprite) and flip-u-gradient-fill (U: red reads 0.902 at 0.1, 0.102 at 0.9)",
    rings=[{"at": 0.58, "box": [0.34, 0.45, 0.66, 0.65]}],
    readouts=[{"at": 0.1, "text": "flip = 1", "x": 0.5, "y": 0.95}, {"at": 0.36, "text": "flip = -1", "x": 0.5, "y": 0.95}])
# ═════════════════════════════ ACT IV · Fixing the Squash ═════════════════════════════
lab("B28", 3, "the circle test on a wide shape comes out an oval", "12-disc.gdshader", "uv-space/c15-oval.mp4", RECT,
    [{"at": 0.14, "lines": [8], "label": "same test"}, {"at": 0.28, "lines": [3], "label": "same radius"}],
    "Act title 'Fixing the Squash' (serif 40) top-left. Code card at left with the same disc shader as before; at right a real Godot window filling a 16:9 frame, empty at first, ringed as 'the wide shape' (readout '16 : 9'); then, as the voice reveals the result, a teal oval grows as the radius readout sweeps from 0 to 0.8. A terracotta ring settles around the oval.",
    "The oval grows from nothing on the wide shape, as wide-to-tall as the shape itself.",
    [{"at": 0.14, "event": "the same disc line highlighted"}, {"at": 0.38, "event": "ring on the wide empty frame: 16 : 9"}, {"at": 0.56, "event": "the radius grows; an oval grows"}, {"at": 0.84, "event": "ring around the oval"}],
    "manim: an ellipse over a rectangle", "The oval appearing from the same code on a wide shape, after the viewer has predicted, is the problem; a real render proves it is not a drawing artifact.",
    f"C15: Lab rect (ColorRect filling a 640x360 logical canvas, rendered at 3840x2160), lab-shaders/12-disc.gdshader. Keyframes (L about {secs('B28'):g} s): radius = 0 until 0.56 L, then 0 to 0.8 over 0.56-0.80 L, hold. Render L + 1 s, 30 fps, Forward+. End state: teal bounding box 512 x 288 of 640 x 360 (measure.py bbox disc-640x360-oval; the same in Compatibility).",
    "measure.py bbox disc-640x360-oval and -COMPAT (512 x 288 in both renderers); disc-640x640-round (512 x 512 on a square)",
    title="Fixing the Squash", rings=[{"at": 0.38, "box": [0.02, 0.02, 0.98, 0.98]}, {"at": 0.84, "box": [0.1, 0.1, 0.9, 0.9]}], readouts=[{"at": 0.38, "text": "16 : 9", "x": 0.5, "y": 0.95}],
    sparse=True, sparse_reason="The wide result window is deliberately empty and ringed until the oval grows (the viewer predicts first); the code card fills the other half.")
manim("B29", 3, "an address step is a wide box: a tenth is 64 pixels across and 36 down", "AddressCell",
      "A 16:9 rectangle labelled 'the shape' with tick marks every tenth along its top and left edges. The first tenth by tenth cell at the top left is outlined in terracotta: a wide box. A bracket over the top edge reads '64 px', a bracket down the left edge reads '36 px'. Small grey credit: 'Godot 4.7.2 · Forward+ · 640 × 360 window'.",
      "The ticks draw in, the first cell lights up as a wide box and its two brackets measure it.",
      [{"at": 0.12, "event": "the rectangle and the tenth ticks"}, {"at": 0.3, "event": "the first cell outlined: wide"}, {"at": 0.66, "event": "brackets: 64 px across, 36 px down"}, {"at": 0.84, "event": "the cell hops to two more places: every cell is the same wide box"}],
      "ShaderLab with ruler overlays", "Tick marks every tenth with pixel counts make the unequal steps countable.",
      "measure.py first on step-tenth-640x360 (red edge at pixel 64, green edge at pixel 36); on 640x320 the second is 32")
manim("B30", 3, "the oval, measured: radius 0.8 reaches 256 px sideways and 144 px up", "OvalMeasured",
      "The same 16:9 rectangle with the teal oval drawn over it, centered. A terracotta arrow from the middle to the right end of the oval tagged '0.8 = 256 px' and one from the middle up tagged '0.8 = 144 px'; then outer brackets '512 px' across and '288 px' down. Small grey credit: 'Godot 4.7.2 · Forward+ and Compatibility · 640 × 360 window'.",
      "The oval grows, the two radius arrows reach out unequally, and the outer brackets read 512 and 288.",
      [{"at": 0.12, "event": "the oval grows from the middle"}, {"at": 0.3, "event": "radius arrow right: 256 px"}, {"at": 0.38, "event": "radius arrow up: 144 px (settled by 0.45)"}, {"at": 0.66, "event": "outer brackets 512 and 288"}],
      "LectureEvidenceTable of radii", "A radius arrow in each direction with its pixel length, then the measured box, turns 'oval' into numbers.",
      "measure.py bbox disc-640x360-oval: width 512, height 288 (half-sizes 256 and 144); same in gl_compatibility")
manim("B31", 3, "pixels are square: the address step is what is uneven", "SquareCells",
      "A grid of equal outline squares labelled 'square pixels' (each drawn square stands for four pixels, noted in a grey credit line). Two terracotta brackets cross the grid: a long one across, tagged '64 px', and a short one down, tagged '36 px', both for one tenth of the address.",
      "The squares settle; the long bracket and the short bracket then measure the same address step differently.",
      [{"at": 0.12, "event": "the grid of equal squares"}, {"at": 0.3, "event": "the long bracket across"}, {"at": 0.66, "event": "the short bracket down: fewer squares for the same step"}],
      "ShaderLab zoomed on pixels", "A grid of equal squares crossed by a long and a short bracket separates 'pixels are square' from 'address steps are not'.",
      "measure.py first step-tenth-640x360 (64 and 36); a pixel is a square of the framebuffer by definition (EXEMPT, FACTCHECK)")
manim("B32", 3, "the fix: multiply U by the aspect ratio so a step covers the same pixels both ways", "CellToSquare",
      "The wide address cell from the previous drawing (64 by 36 px) with a tag 'x aspect' and a definition line 'aspect ratio: width divided by height = 640 / 360'. The wide cell squeezes horizontally into a square cell labelled '36 × 36 px'.",
      "The wide cell squeezes into a square while the definition of aspect ratio lands.",
      [{"at": 0.12, "event": "the wide cell (64 by 36)"}, {"at": 0.28, "event": "the x aspect tag; the cell squeezes into a square (settled by 0.45)"}, {"at": 0.64, "event": "definition: aspect ratio = width divided by height"}, {"at": 0.84, "event": "label: 36 × 36 px"}],
      "ShaderLab with aspect swept", "The wide address cell squeezing into a square is the fix as a transformation; the render follows in B33.",
      "Lab probes disc-aspect-640x360-round (288 x 288); arithmetic 640 / 360 = 1.7778")
lab("B33", 3, "p.x *= aspect: the oval becomes a circle", "16-disc-aspect.gdshader", "uv-space/c16-circle.mp4", RECT,
    [{"at": 0.1, "lines": [8], "label": "x times aspect"}, {"at": 0.36, "lines": [10], "label": "length, as before"}, {"at": 0.6, "lines": [8], "label": "aspect rises"}],
    "Code card at left with the corrected disc shader; at right a real Godot window filling a 16:9 frame showing the oval from before, which turns into a circle as the aspect readout sweeps from 1 to 1.78. A terracotta ring settles on the circle with the readout '288 × 288'.",
    "The oval turns into a circle as aspect goes from one to one point seven eight.",
    [{"at": 0.1, "event": "p.x *= aspect highlighted; the oval"}, {"at": 0.36, "event": "the length test, as before"}, {"at": 0.6, "event": "aspect rises; the oval turns into a circle"}, {"at": 0.82, "event": "a circle; ring; 288 x 288"}],
    "LectureCodeTrace on the one line", "The oval becoming a circle as aspect rises, beside the one line that does it.",
    f"C16: Lab rect (640x360 logical canvas, rendered at 3840x2160), lab-shaders/16-disc-aspect.gdshader, radius 0.8. Keyframes (L about {secs('B33'):g} s): aspect = 1.0 until 0.50 L, then 1.0 to 1.7778 over 0.50-0.76 L, hold. Render L + 1 s, 30 fps, Forward+. End state: teal bounding box 288 x 288 (measure.py bbox disc-aspect-640x360-round; the same in Compatibility).",
    "measure.py bbox disc-aspect-640x360-round and -COMPAT (288 x 288); disc-aspect-1-640x360 (512 x 288, the start)",
    rings=[{"at": 0.8, "box": [0.275, 0.1, 0.725, 0.9]}],
    readouts=[{"at": 0.78, "text": "aspect = 1.78", "x": 0.5, "y": 0.95}, {"at": 0.84, "text": "288 × 288", "x": 0.5, "y": 0.5}])
rem("B34", 3, "the shader has no direct way to ask the size: set a uniform from the node, again on resize", "LectureCodeTrace",
    {"title": "Tell the shader the shape's size", "code": 'extends ColorRect\n\nfunc _update_aspect():\n\tmaterial.set_shader_parameter("aspect", size.x / size.y)\n\nfunc _ready():\n\tresized.connect(_update_aspect)\n\t_update_aspect()',
     "note": "GDScript on the ColorRect · checked in Godot 4.7.2 (verify-aspect.gd, case A5)", "cues": [0.04, 0.04, 0.2, 0.24, 0.3, 0.6, 0.64, 0.7], "durationSeconds": "__AUDIO__"},
    "A cream code card with the real GDScript (the exact text verified in verify-aspect.gd): focus lands on the function that sets aspect from size, then on the lines that call it again whenever the node is resized.",
    "Line focus lands on the set line, then on the resize hook.",
    [{"at": 0.2, "event": "set aspect from width over height"}, {"at": 0.6, "event": "set it again on resized"}],
    "ClaudeCodeBeat", "Real GDScript with paced line focus: set it, then set it again on resize; the cues follow the spoken order.",
    "verify-aspect.gd A5 (round at 400x200, round again at 200x320 after resize, stale aspect gives 40 x 128); GDScript text is the verified text")
rem("B35", 3, "where aspect can come from, measured on two nodes", "LectureEvidenceTable",
    {"title": "Where aspect comes from", "headers": ["Aspect from", "ColorRect", "Sprite2D"],
     "rows": [["no fix", "2.00", "2.00"], ["texture pixel size", "2.00", "1.00"], ["screen pixel size", "1.13", "1.14"], ["a uniform you set", "1.00", "1.00"]],
     "note": "Circle width over height, 1.00 is round · 2:1 shapes · Godot 4.7.2 · Forward+", "cues": [0.08, 0.22, 0.58, 0.8], "durationSeconds": "__AUDIO__"},
    "A four-row, three-column table of measured circle width over height, one row ringed as each source is named; 1.00 means round.", "The ring steps down the rows: the uniform row is the only one that reads 1.00 in both columns.",
    [{"at": 0.08, "event": "no fix row"}, {"at": 0.22, "event": "texture pixel size row"}, {"at": 0.58, "event": "screen pixel size row"}, {"at": 0.8, "event": "uniform row: 1.00 and 1.00"}],
    "manim: bars", "A measured grid (four sources of aspect, two nodes) is exactly what the evidence table is for; the 1.00 cells are the answer.",
    "run-1-aspect.log cases A (ColorRect 400x200 in a 640x360 window: 320x160, 180x160, 320x160, 160x160) and C (Sprite2D 256x128: 204x102, 102x102, 116x102, 102x102); pixel-size-probe-640x320 (TEXTURE_PIXEL_SIZE on a ColorRect is 1 by 1)")

# ═════════════════════════════ ACT V · Staying Inside the Picture ═════════════════════════════
lab("B36", 4, "a picture with a solid edge smears when the address leaves 0 to 1", "07-scale.gdshader", "uv-space/c17-smear.mp4", SPR.replace("Sprite2D", "Sprite2D (checker picture)"),
    [{"at": 0.1, "lines": [6]}, {"at": 0.7, "lines": [7], "label": "last row, column"}],
    "Act title 'Staying Inside the Picture' (serif 40) top-left. Code card at left with the scale shader; at right a real Godot window where a teal-and-cream checker picture shrinks toward the top left as zoom goes from 1 to 2 and its edge rows and columns stretch into stripes across the rest of the square. A terracotta ring on the stripes with the readout 'edge pixels'.",
    "The picture shrinks and its edge pixels streak across the space it leaves.",
    [{"at": 0.1, "event": "uv = UV * zoom highlighted; the checker at full size"}, {"at": 0.34, "event": "zoom grows; stripes stream out of the edges"}, {"at": 0.7, "event": "the lookup keeps returning the last row and column; ring on the stripes"}],
    "manim: an edge row streaking", "The smear is an artifact on a real picture: the viewer should see the real thing before the mechanism.",
    f"C17: Lab sprite (--sprite-tex checker), lab-shaders/07-scale.gdshader. Keyframes (L about {secs('B36'):g} s): zoom = 1 until 0.30 L, then 1 to 2 over 0.30-0.62 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.25, 0.25) cream, (0.6, 0.05) and (0.9, 0.05) the same teal (constant along the row), (0.9, 0.9) cream (the corner pixel).",
    "Lab probes scale-2-checker-fill; Godot docs (CanvasItem TextureRepeat: sampling outside the extents stretches the edge pixels)",
    title="Staying Inside the Picture", rings=[{"at": 0.7, "box": [0.5, 0.1, 0.725, 0.9]}], readouts=[{"at": 0.7, "text": "edge pixels", "x": 0.62, "y": 0.95}])
manim("B37", 4, "why a sprite's transparent border hides the smear", "EdgeSmear",
      "Two rows of edge pixels at the right edge of two pictures. Top row: a column of solid teal and cream edge pixels with horizontal stripes streaming outward to the right, labelled 'solid edge: stripes'. Bottom row: the same column drawn as dashed transparent cells, with nothing streaming outward, labelled 'transparent edge: nothing'. Small grey credit: 'Godot docs: a one pixel transparent border'.",
      "Stripes stream out of the solid edge; from the transparent edge nothing streams.",
      [{"at": 0.12, "event": "the two edge columns"}, {"at": 0.3, "event": "stripes stream out of the solid edge"}, {"at": 0.7, "event": "nothing streams from the transparent edge; the docs tip lands"}],
      "ShaderLab with a transparent-border texture", "Edge pixels streaking outward, against transparent edge pixels streaking into nothing, is a mechanism drawing (and the docs' own tip).",
      "Lab probes scale-2-sprite-fill ((0.75, 0.25) is stage: transparent edge, no smear) against scale-2-checker-fill; Godot docs TEXTURE_REPEAT_DISABLED text")
manim("B38", 4, "step: a mask is a number from zero to one", "StepFunction",
      "A plot with the horizontal axis from -1 to 2 and the vertical axis from 0 to 1: the curve of step(0, x), flat at 0 for x below 0 and flat at 1 from 0 on, with a terracotta dot travelling along it. Definition lines (GLOSSARY wording): 'mask: a number from 0 to 1 per pixel saying how much of something to show' and 'step(edge, x): 0 below the edge, 1 from the edge up'.",
      "The dot travels along the flat line at 0, jumps to 1 at the edge, and stays at 1.",
      [{"at": 0.12, "event": "axes and the step curve"}, {"at": 0.3, "event": "the dot travels and jumps to 1 at zero (settled by 0.45)"}, {"at": 0.66, "event": "the mask definition lands"}],
      "LectureCodeTrace on the step function", "A plotted step with a dot jumping from 0 to 1 at the edge is what 'step' means.",
      "Lab probes step-edge-cases (step(0.5, 0.4999) = 0, step(0.5, 0.5) = 1); Godot docs (step: 0.0 if b < a, otherwise 1.0)")
manim("B39", 4, "two steps multiply into a gate: one only between zero and one", "Gate",
      "The same plot axes. The first step (turns on at 0) and the second step (turns off at 1) are drawn in two greys; they multiply into a terracotta box of height 1 between x = 0 and x = 1. Then a square picture-frame in the plane: ones inside, zeros outside, labelled 'both axes'.",
      "The two steps slide together and the product is a box between zero and one; the box then becomes a square in the plane.",
      [{"at": 0.12, "event": "the step that turns on at 0 and the step that turns off at 1"}, {"at": 0.3, "event": "they multiply into a box (settled by 0.45)"}, {"at": 0.68, "event": "the box becomes a square: both axes, multiply again"}],
      "ShaderLab with the mask line", "Two steps multiplying into a one-only-between-zero-and-one gate is a function being built; a Manim plot does it with motion.",
      "Lab probes mask-2-checker-fill ((0.495, 0.495) inside, (0.505, 0.505) outside the gate)")
lab("B40", 4, "multiply alpha by the mask: one clean picture", "17-mask.gdshader", "uv-space/c18-mask.mp4", SPR.replace("Sprite2D", "Sprite2D (checker picture)"),
    [{"at": 0.1, "lines": [9]}, {"at": 0.25, "lines": [9], "label": "inside: times one"}, {"at": 0.42, "lines": [9], "label": "outside: times zero"}],
    "Code card at left with the mask shader (ten lines); at right the real Godot window with the same checker picture as the smear beat: as zoom goes from 1 to 2 it shrinks into the top-left quarter and the space it leaves stays empty, with no stripes. A terracotta ring on the empty space with the readout 'no smear'. A caption defines alpha (GLOSSARY wording): 'alpha: how visible a pixel is: 0 invisible, 1 solid'.",
    "The picture shrinks and the space it leaves stays clean.",
    [{"at": 0.1, "event": "COLOR.a *= inside.x * inside.y highlighted"}, {"at": 0.25, "event": "inside: nothing changes"}, {"at": 0.42, "event": "outside: alpha is zero; the picture shrinks cleanly"}, {"at": 0.8, "event": "ring on the clean space: no smear"}],
    "LectureCodeTrace on the mask line", "The smear disappearing while the picture still shrinks is the proof the mask works.",
    f"C18: Lab sprite (--sprite-tex checker), lab-shaders/17-mask.gdshader. Keyframes (L about {secs('B40'):g} s): zoom = 1 until 0.40 L, then 1 to 2 over 0.40-0.66 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.25, 0.25) cream, (0.75, 0.25) and (0.9, 0.9) stage colour (0.851, 0.835, 0.792), (0.495, 0.495) cream, (0.505, 0.505) stage.",
    "Lab probes mask-2-checker-fill (identical picture, no smear) and mask-1-checker-fill (zoom 1 unchanged)",
    rings=[{"at": 0.8, "box": [0.5, 0.1, 0.725, 0.9]}], readouts=[{"at": 0.8, "text": "no smear", "x": 0.62, "y": 0.95}],
    caption="alpha: how visible a pixel is: 0 invisible, 1 solid")
lab("B41", 4, "the opening shader, now readable line by line", "01-hook-controls.gdshader", "uv-space/c19-decode.mp4", SPR.replace("Sprite2D", "Sprite2D + texture uniform"),
    [{"at": 0.27, "lines": [9], "label": "slide"}, {"at": 0.36, "lines": [10], "label": "scale"}, {"at": 0.42, "lines": [11, 3], "label": "look up"}],
    "Code card at left with the opening shader (twelve lines); at right the real Godot window repeating the opening render: the sprite slides left and wraps, then shrinks into a three by three grid, while the highlighted lines follow the voice.",
    "The highlighted line moves from slide to scale to lookup as the picture slides, shrinks and tiles.",
    [{"at": 0.27, "event": "uv.x += shift: the picture slides"}, {"at": 0.36, "event": "uv *= zoom: it shrinks"}, {"at": 0.42, "event": "the lookup with repeat on: a three by three grid"}],
    "LectureCodeTrace alone", "The opening shader's real code beside its real result: every line now has a meaning, which is the film's payoff.",
    f"C19: the same shader and capture setup as C01 (lab-shaders/01-hook-controls.gdshader, --tex pic=sprite) with timing re-keyed to this beat (L about {secs('B41'):g} s): shift = 0 until 0.26 L, then 0 to 1.0 over 0.26-0.34 L; zoom = 1 until 0.35 L, then 1 to 3 over 0.35-0.55 L, hold. Render L + 1 s, 30 fps, Forward+. End state: nine whole copies (probes hook-tiled-fill).",
    "Lab probes hook-start / hook-one-wrap / hook-tiled (same as B01)")
rem("B42", 4, "four usual causes when a UV effect looks wrong", "LectureEvidenceTable",
    {"title": "Four usual causes", "headers": ["It looks like", "Usual cause"],
     "rows": [["moves the wrong way", "added, not subtracted"], ["zooms to a corner", "zero is not in the middle"], ["smears at the edges", "no repeat, no mask"], ["a circle is an oval", "no aspect fix"]],
     "note": "Each row was reproduced and fixed on the real shader · Godot 4.7.2", "cues": [0.26, 0.44, 0.68, 0.86], "durationSeconds": "__AUDIO__"},
    "A four-row symptom-and-cause table, one row ringed as each is named.", "The ring steps down the four rows with the voice.",
    [{"at": 0.26, "event": "moves the wrong way"}, {"at": 0.44, "event": "zooms to a corner"}, {"at": 0.68, "event": "smears at the edges"}, {"at": 0.86, "event": "circle is an oval"}],
    "manim: a checklist", "Four symptom-and-cause pairs are a lookup table, and the viewer will come back to it.",
    "Rows 1 to 4 are the findings of B09, B19, B36 and B28 (Lab probes and measure.py)")

# ═════════════════════════════ write lanes + SHOTLIST ═════════════════════════════
(HERE / "lanes").mkdir(exist_ok=True)
n_acts = len(N.ACTS)
for ai in range(n_acts):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

lanes_hist = {}
for e in E:
    lanes_hist[e["entry"]["lane"]] = lanes_hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in sorted(E, key=lambda x: x["bid"]):
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
n_manim_classes = sorted(e["entry"]["class"] for e in E if e["entry"]["lane"] == "manim")
sl = ["# Shot list: UV Space\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab render of a tested file in `lab-shaders/`; no editor frames are needed. Seventeen Manim scenes, nineteen ShaderLab captures and one docs screenshot must be built or recorded (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`). Props used here: `layout` side and video, `code`, `codeFile`, `cues` with `label`, `video` (MP4 or PNG), `videoLabel`, `readouts`, `rings`, `title`, and `caption`, which carries GLOSSARY definition lines here (B06, B17, B40) as one static line under the result window.",
      "2. **`shader_kit.py`** Manim helpers (same file): `ramp_strip`, `pixel_grid`, `plot`, `uv_square`, `code_card`; this film also needs two scene-local drawings: a labelled **ruler** (ticks, brackets, a marker) and a **window over a picture** (an outline sliding over a card with a clipped copy beside it).",
      "3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` with `--animate` float keyframes, `--material-at` (C07 and C13), `--tex`, `--sprite-tex`, `--set`, `--size`; see `CAPTURE-PLAN.md`.",
      "4. **Docs screenshot D1** for B16 via Playwright.",
      "5. **Manim classes** (one per Manim beat): " + ", ".join(n_manim_classes) + ".\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
