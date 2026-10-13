#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md (the pilot's way).

Why a generator: the code shown on screen must be the tested file text, and the shot list must say exactly what the lanes say.
Re-run after any edit:   python3 _gen_lanes.py && python3 make_sheet.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
PUB = "local-world-and-screen-space"          # public/<PUB>/ holds this film's captures and stills in the toolkit
E = []                                         # entries in beat order


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, ramp=None, title=None, code=None, code_file=None, lane="capture", caption=""):
    props = {"layout": layout, "code": code if code is not None else (code_of(shader) if shader else ""),
             "codeFile": code_file if code_file is not None else (f"lab-shaders/{shader}" if shader else ""), "cues": cues,
             "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption,
             "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    add(bid, act, about, {"lane": lane, "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": intent,
                          "motion_claim": motion, "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


def rem(bid, act, about, pattern, props, intent, motion, show, runner, why, evidence, lane="remotion"):
    add(bid, act, about, {"lane": lane, "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


# ═════════════════════════════ ACT I · Three Addresses ═════════════════════════════
lab("B01", 0, "same texture, same motion: stars that ride along against stars that stay put", None, f"{PUB}/hook.mp4",
    "Godot 4.7.2 · Forward+ · same texture, same motion · scripted run", [],
    "Act title 'Three Addresses' (serif 40) top-left. A real Godot render in a framed window: a faint copy of a star sky (indigo, cream stars, a ringed planet) "
    "behind two test sprites in one row. Both slide right together, slowly. Stars inside the left sprite travel with it; the right sprite "
    "uncovers the planet and stars that stay where they are, lining up with the faint copy. Labels: 'from the sprite' under the left, 'from the world' under the right.",
    "Both sprites make the same slide, but only the left one's stars move with it; the right one uncovers a planet that does not move.",
    [{"at": 0.0, "event": "two sprites on a faint sky, labelled"}, {"at": 0.1, "event": "both slide right while the voice describes the left, then the right"},
     {"at": 0.33, "event": "the right sprite is over the planet; its picture matches the faint copy, the left one's does not"}],
    "manim drawing of two sprites with dots inside",
    "A real render is the honest picture of 'carries its stars' against 'slides over fixed stars'; a drawing would only claim it.",
    "C01: scene script capture-scenes/capture-c01.gd (CAPTURE-PLAN.md): faint backdrop ColorRect (02-sky-world, alpha 0.35), blob sprites (256 px art, scale 1) at y=240, "
    "left with 01-sky-local.gdshader from x=220, right with 02-sky-world.gdshader from x=700; both slide +300 over 10 to 56 % of the beat (ease in-out) and rest; 14 s, 30 fps, Forward+, no input (CAPTURE-PLAN.md).",
    "verify12.gd C01 and verify5.gd W1, W2, W4 (colours identical before and after the slide; planet shows only in the world sprite)",
    layout="video", title="Three Addresses",
    readouts=[{"at": 0.08, "text": "from the sprite", "x": 0.29, "y": 0.88}, {"at": 0.08, "text": "from the world", "x": 0.66, "y": 0.88}])

manim("B02", 0, "a position is numbers from a zero; move the zero, the numbers change", "MoveTheZero",
      "A plane of outline cells (pixel grid, no fill). A terracotta dot sits fixed at one cell. A zero marker (a ring with a right arrow and a down arrow) "
      "sits at the top-left with a live readout '5 across · 4 down'. The zero marker then slides to a cell four across and one down; the readout counts "
      "to '1 across · 3 down' while the dot never moves.",
      "The zero slides across the grid and the two numbers change continuously while the dot stays where it is.",
      [{"at": 0.1, "event": "grid, dot, zero marker, '5 across · 4 down'"}, {"at": 0.4, "event": "the zero starts to slide"}, {"at": 0.7, "event": "'1 across · 3 down', dot unmoved"}],
      "LectureEvidenceTable (two coordinate pairs)",
      "The claim is that the numbers change and the dot does not; a moving zero with a live readout shows both at once, a table only lists them.",
      "Arithmetic: dot (5,4) from the first zero, second zero at (4,1) from the first, so the dot is (1,3) from the second (FACTCHECK row 2)")

manim("B03", 0, "three zeros: the sprite's center, the world's origin, the window's corner", "ThreeZeros",
      "One scene on the cream stage: a large outlined rectangle for the world with a zero marker at its top-left labelled 'world space'; inside it a smaller outlined "
      "rectangle for the window; inside that a sprite (square outline with the test blob) with a zero marker at its center labelled 'local space'; a third zero marker "
      "at the window's top-left labelled 'screen space'. Short definitions appear with each label: 'from the node's own zero', 'from the world's origin' and, for the third, "
      "the glossary wording 'pixels of the window, counted from the top left, y growing downward'. A terracotta dot marks the sprite's top-left corner and stays through the act.",
      "The three zero markers land one by one, each with its label, in the same picture.",
      [{"at": 0.08, "event": "world, window and sprite outlines"}, {"at": 0.2, "event": "local zero at the sprite's center"}, {"at": 0.4, "event": "world zero lands before the midpoint"},
       {"at": 0.62, "event": "screen zero at the window's corner"}, {"at": 0.82, "event": "the corner dot, one corner with an address in each"}],
      "DesignPipelineClaim, show-tell isometric",
      "Three origins have to be seen in one picture to be compared; a diagram with the world, the window and the sprite nested is the claim.",
      "T1 (verify3.gd): world (536, 336), screen (286, 236), local (-64, -64); geometry from the docs (canvas space origin = upper-left of the screen)")

manim("B04", 0, "the corner in local space: minus sixty-four, minus sixty-four, wherever the sprite goes", "LocalAddress",
      "The same diagram zoomed on the sprite: its center zero marker with a right arrow and a down arrow, a '128' dimension across the top, and a grey arrow from the "
      "zero to the terracotta corner dot with the tag '(-64, -64)'. The sprite, its zero and its arrow then slide to the right across the world; the tag does not change.",
      "The sprite slides away with its zero and its arrow; the tag '(-64, -64)' stays exactly the same.",
      [{"at": 0.1, "event": "sprite, local zero, arrow to the corner, tag"}, {"at": 0.38, "event": "dimension '128' lands"}, {"at": 0.62, "event": "sprite slides right, tag unchanged"}],
      "ShaderLab capture of a color-coded sprite",
      "Local numbers are about one sprite and its own zero; a sprite sliding off with its tag unchanged shows 'that answer holds' as motion.",
      "T1, V4d (sprite moved: local corner stays (-64, -64)); docs: Sprite2D centered = true; VERTEX local space (FACTCHECK rows 4, 5, 6)")

manim("B05", 0, "the corner in world space: five thirty-six, three thirty-six, and it changes when the sprite slides", "WorldAddress",
      "The world rectangle with its zero marker at the top-left. A long grey arrow runs from the world zero to the terracotta corner dot with the tag '(536, 336)'; "
      "a small grey tag '(-64, -64)' stays beside the sprite. The sprite slides right by a hundred: the arrow stretches and the world tag counts up to '(636, 336)' "
      "while the small local tag does not move.",
      "The long arrow from the world's origin stretches as the sprite slides; its tag counts up while the local tag stays put.",
      [{"at": 0.1, "event": "arrow from the world zero, tag (536, 336)"}, {"at": 0.4, "event": "sprite starts to slide"}, {"at": 0.65, "event": "tag (636, 336); local tag unchanged"}],
      "LectureEvidenceTable (two rows)",
      "The world address is a distance from far away; an arrow that stretches while a number counts is that distance as motion.",
      "T1 (536, 336), V4d (sprite at 700: 636, 336); GDScript global_transform agrees (verify1.gd S2)")

manim("B06", 0, "the corner on screen: two eighty-six, two thirty-six; the camera decides which part of the world the window shows", "ScreenAddress",
      "The world rectangle, with the window rectangle (the camera's view) drawn on it and its own top-left zero marker labelled 'screen space'. A grey arrow runs from the "
      "window's zero to the terracotta corner dot with the tag '(286, 236)'. A small camera mark sits at the window's center; the world zero and its '(536, 336)' tag stay faintly visible.",
      "The arrow from the window's corner draws out to the dot and its tag lands; the world tag stays where it was.",
      [{"at": 0.1, "event": "window frame with its own zero and a camera mark"}, {"at": 0.4, "event": "arrow from the window's corner to the dot"}, {"at": 0.65, "event": "tag (286, 236)"}],
      "ShaderLab capture of the same scene",
      "The window and the camera are diagram objects; showing the window as a frame laid over the world is the only way to see 'zero is the window's corner'.",
      "T1: camera at (890, 460), canvas origin (-250, -100), corner at screen (286, 236); docs: Camera2D, CANVAS_MATRIX")

lab("B07", 0, "pan the camera: the screen address changes, the world address does not", None, f"{PUB}/pan.mp4",
    "Godot 4.7.2 · Forward+ · 1280 by 720 window · camera pans right by 100 · scripted run", [],
    "A real Godot render: a faint star sky as the world, a 128 px test sprite in a thin cream box with a terracotta dot on its top-left corner, and a camera that pans right by a hundred. "
    "Readouts: 'world 536, 336' stays; 'screen 286, 236' changes to 'screen 186, 236' as the sprite and the whole sky slide left.",
    "The corner dot slides left on screen while its world readout never changes.",
    [{"at": 0.04, "event": "sprite, corner dot, readouts world 536, 336 and screen 286, 236"}, {"at": 0.12, "event": "camera pans right by 100; everything slides left"},
     {"at": 0.42, "event": "readout becomes screen 186, 236; world readout unchanged"}],
    "manim: a window sliding over the world with ticking numbers",
    "A real camera pan in a real render is the evidence; the numbers are measured, and the sky makes the sliding visible.",
    "C02: scene script capture-scenes/capture-c02.gd: Camera2D (890,460) to (990,460) over 12 to 40 % of the beat (ease in-out), sprite (600,400) 128 px art scale 1 with a drawn cream box and a terracotta corner dot (radius 6), "
    "backdrop sky ColorRect (alpha 0.5) covering world (0,0) to (2000,1000); 13 s (CAPTURE-PLAN.md).",
    "verify12.gd C02 and verify3.gd T1, T2 (camera 890 to 990: screen (286,236) to (186,236), world (536,336) both)", layout="video",
    readouts=[{"at": 0.04, "text": "world 536, 336", "x": 0.5, "y": 0.1}, {"at": 0.04, "text": "screen 286, 236", "x": 0.5, "y": 0.2},
              {"at": 0.42, "text": "screen 186, 236", "x": 0.5, "y": 0.2}])

# ═════════════════════════════ ACT II · From Local to World ═════════════════════════════
manim("B08", 1, "vertex() hands you the corner in local space; the zero is the node's own", "CornersInLocalSpace",
      "Act title 'From Local to World' (serif 40) top-left. On the left a sprite (square outline, test blob) with a zero marker at its center; its four corners flash in turn with the "
      "tags '(-64,-64)', '(64,-64)', '(-64,64)', '(64,64)', a chip 'VERTEX' riding each tag, and a small card 'vertex(): runs once for each vertex; places the corners' with a counter 'run 1, 2, 3, 4' that steps as "
      "each corner flashes. On the right a color rect (outlined rectangle) with its zero marker at its top-left "
      "corner and the tags '(0, 0)', '(300, 0)', '(0, 200)', '(300, 200)'. A second small card: 'built-in: a value the engine hands to a function, or collects from it'.",
      "The four corners of the sprite flash one after another, each with its local numbers; then the color rect's zero sits at its corner instead.",
      [{"at": 0.08, "event": "sprite with center zero; corners flash 1 to 4"}, {"at": 0.36, "event": "built-in card"}, {"at": 0.62, "event": "color rect with zero at its corner"}],
      "ShaderLab",
      "Four corners flashing in turn is 'once for each corner'; putting the two zeros side by side is the contrast the sentence names.",
      "V4a (ColorRect local zero is its top-left: (0,0) to (299,199)); T1 (sprite corner (-64,-64)); docs: VERTEX 'local space (pixel coordinates, relative to the Node2D's origin)'")

manim("B09", 1, "why a matrix: a plain shift is not enough once the node is turned and resized", "WhyAMatrix",
      "A sprite outline at the world's zero with its corner dot. Step one: it is shifted to (600, 400) and a grey ghost corner lands at (536, 336), labelled 'add the position'. "
      "Step two: the sprite is also turned and doubled in size; the true corner dot lands somewhere else at (553, 225) while the ghost stays at (536, 336), with a short grey "
      "arrow between them. A small 4x4 table appears with the card 'matrix: a grid of numbers that moves a point when you multiply by it' and the caption 'one matrix holds shift, turn and size'.",
      "The ghost corner stays where 'add the position' puts it while the real corner swings away once the sprite is turned and doubled.",
      [{"at": 0.1, "event": "shift only: ghost and true corner agree"}, {"at": 0.38, "event": "turn and size added: the true corner swings away from the ghost"}, {"at": 0.66, "event": "one matrix table"}],
      "LectureEvidenceTable (add the position against the real answer)",
      "The failure of 'add the position' is the reason for the matrix; the ghost and the real corner drifting apart shows it, a table of two answers does not.",
      "verify3.gd T5 (sprite at (600,400), scale 2, turned 30 degrees: engine corner (553.15, 225.15); shift only gives (536, 336))")

manim("B10", 1, "model matrix: local numbers go in, world numbers come out; it holds the whole placement, parents included", "ModelMatrix",
      "A labelled table (4 by 4 outline cells) captioned 'model matrix: local to world' in the middle. At the left, a dimmed sprite sits at the world's zero with the tag '(-64, -64)'. "
      "The sprite travels along an arrow through the table and lands at its place at the right with the tag '(536, 336)'. A small 'parents included' chip appears under the table.",
      "The sprite is carried from the world's zero through the table to its place; its corner tag changes on the way.",
      [{"at": 0.1, "event": "table and the dimmed sprite at the zero, tag (-64, -64)"}, {"at": 0.38, "event": "sprite travels through the table"}, {"at": 0.66, "event": "lands at its place, tag (536, 336); chip"}],
      "DesignPipelineClaim, show-tell isometric (a machine on a conveyor)",
      "Putting the matrix between 'before' and 'after' with the same sprite in both places shows 'multiply and the world numbers come out'.",
      "docs: MODEL_MATRIX 'Local space to world space transform'; verify2.gd f (child of a moved, turned parent: world read through MODEL_MATRIX equals the engine's global transform)")

lab("B11", 1, "the editor shows the position relative to the parent", None, f"{PUB}/editor-parent-child.mp4",
    "Godot 4.7.2 editor · scripted editor session", [],
    "Two real frames of the Godot editor (a scripted editor session), the Scene dock reading Scene, Parent, Child and the Inspector open on Node2D, Transform, Position: the Child (a Sprite2D) selected shows Position x 50.0 px, y 0.0 px; the Parent (a Node2D) selected shows x 500.0 px, y 300.0 px. "
    "A slow cross-dissolve between them; a terracotta ring on the Position row being named in each frame; a readout 'world 550, 300' lands last.",
    "The ring moves from the child's Position row to the parent's, and the world number lands last.",
    [{"at": 0.14, "event": "child selected: Position 50, 0 ringed"}, {"at": 0.58, "event": "cross-dissolve to the parent"}, {"at": 0.64, "event": "parent: Position 500, 300 ringed"},
     {"at": 0.84, "event": "readout world 550, 300"}],
    "manim: a parent platform sliding right while the child's editor tag stays 50, 0 and its world tag counts up",
    "SHOW-THE-THING: the claim is about what the editor shows, so the editor's own Inspector, recorded by script, is the evidence; a Manim parent diagram would only describe it.",
    "E1 (DONE by script, 2026-10-13, editor driver; README 2.5): two whole frames from `_godot-shaders-series/editor-capture/png/1920x1080/local-world-and-screen-space/` (native 3456x1944 twins in png/3456x1944/local-world-and-screen-space/): local-world_E1-1_child-selected-clean-root and local-world_E1-2_parent-selected-clean-root. Cross-dissolve at 0.58 of the beat; the ring boxes are fractions of the whole 1920x1080 frame (no crop). Real labels: category Node2D, group Transform, row Position with fields x and y and a px suffix, then Rotation, Scale (with a link toggle), Skew; the Scene dock reads Scene, Parent, Child. Use the clean-root pair. The plan-exact pair (`..._plan-exact-root-is-Parent`, where the root node itself is the transformed Parent) shows a warning triangle on the root, 'The root node of a scene is recommended to not be transformed, since instances of the scene will usually override this.', and is not used. No pointer is visible (Movie Maker records the window): label 'scripted editor session'.",
    "V4b (child at (50,0) in a parent at (500,300): global (550,300)); docs: Node2D.position 'Position, relative to the node's parent'. Editor frames E1 DONE by script (_godot-shaders-series/editor-capture/png/1920x1080/local-world-and-screen-space/); verify11.gd (Node2D property list: group Transform, row Position); FACTCHECK row 23",
    layout="video", lane="editor",
    rings=[{"at": 0.14, "box": [0.841, 0.427, 0.996, 0.494]}, {"at": 0.64, "box": [0.841, 0.247, 0.996, 0.312]}],
    readouts=[{"at": 0.84, "text": "world 550, 300", "x": 0.3, "y": 0.8}])

manim("B12", 1, "the one line: wrap the corner in a vec4, multiply by the model matrix, keep two numbers", "BuildTheLine",
      "The line world_position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy; assembled token by token in monospace. Under it a data strip: the corner '(-64, -64)' becomes "
      "'(-64, -64, 0, 1)' as vec4 closes round VERTEX, then '(536, 336, 0, 1)' as MODEL_MATRIX multiplies in, then '(536, 336)' as .xy keeps two. A grey bracket moves under each token as it lands, and a small grey label 'vector: a bundle of two to four numbers' appears under vec4 as the two numbers become four.",
      "The corner's two numbers grow to four, get multiplied, and shrink back to two as each token of the line lands.",
      [{"at": 0.12, "event": "vec4(VERTEX, 0.0, 1.0) lands; two numbers become four"}, {"at": 0.36, "event": "MODEL_MATRIX * lands; the numbers change"}, {"at": 0.66, "event": ".xy lands; two numbers remain"}],
      "LectureCodeTrace",
      "A paced line focus shows which part is named but not that the corner's numbers pad, multiply and shrink; the build-up shows the data moving through the line.",
      "lab-shaders/05-world-field.gdshader line 6 (compiled in the Lab); T1 numbers; docs: the skip_vertex_transform example uses this exact form")

manim("B13", 1, "the zero and the one: the matrix's last column holds the shift; the one switches it on", "TheLastColumn",
      "A 4 by 4 grid of outline cells with the last column outlined and filled with the node's numbers '600, 400, 0, 1' beside the vector '(-64, -64, 0, w)'. With w = 1 a terracotta ring "
      "sits on the one and the result reads '(536, 336)' labelled 'a place'. The one then flips to zero: the last column dims and the result falls back to '(-64, -64)' labelled 'a direction'.",
      "The final one flips to zero, the last column dims, and the answer drops from (536, 336) to (-64, -64).",
      [{"at": 0.1, "event": "matrix with its last column, the vector with w = 1, result (536, 336)"}, {"at": 0.36, "event": "the last column lights: the shift lives here"},
       {"at": 0.64, "event": "w flips to 0: column dims, result (-64, -64)"}],
      "ShaderLab (03-direction-not-place on the sprite)",
      "The last column and the final one are a picture of a matrix; flipping the one to a zero and watching the answer fall back is the claim as motion.",
      "verify9.gd M1 (the plain sprite's MODEL_MATRIX: identity plus last column (600,400,0,1)); verify3.gd T4 (w=1 world (536,336); w=0 (-64,-64)); T5 (scaled and turned: w=0 keeps scale and turn, drops the shift); docs: m[3] is the 4th column of a mat4 transform")

rem("B14", 1, "fragment cannot read the model matrix: the compiler says unknown identifier", "CCPlainShell",
    {"title": "zsh · a scratch project · Godot 4.7.2 log, trimmed",
     "lines": ["$ godot --path . --script res://broken.gd",
               "Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org",
               "Metal 4.0 - Forward+ - Using Device #0: Apple - Apple M4 Pro (Apple9)",
               "",
               "fragment() runs once for each pixel the shape covers; sets its color",
               "--Main Shader--",
               "    2 | ",
               "    3 | void fragment() {",
               "E   4->  vec2 world = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;",
               "    5 |  COLOR.rgb = vec3(world / vec2(1280.0, 720.0), 0.8);",
               "    6 | }",
               "SHADER ERROR: Unknown identifier in expression: 'MODEL_MATRIX'."],
     # frames at 30 fps, laid out for the estimated 13.6 s (408 frames); retime to the measured audio (BUILD-PROMPT.md) and keep every
     # cue out of 45 to 55 % of the beat (frames 184 to 224 here). The definition line lands as the voice says "Fragment runs once".
     "lineCues": [6, 12, 16, 18, 24, 56, 62, 68, 84, 92, 98, 150],
     "rings": [{"line": 8, "cue": 100}, {"line": 11, "cue": 162}],
     "startCue": 6, "lineGap": 12, "fontSize": 32, "windowMargin": 48, "durationSeconds": "__AUDIO__"},
    "A plain terminal window with the real output of the broken-shader script: the command, the engine banner, the script's one printed line "
    "'fragment() runs once for each pixel the shape covers; sets its color' (the definition, in full ink), then the engine's own five marked source lines "
    "with the offending line flagged E and ringed, and the line 'SHADER ERROR: Unknown identifier in expression: MODEL_MATRIX.' with a second ring. "
    "The title says the log was trimmed of its backtrace.",
    "The log lines land one after another; the offending line gets a ring, then the error line lands and gets one.",
    [{"at": 0.1, "event": "command, banner, and the definition line as the voice says fragment"}, {"at": 0.22, "event": "the marked source lines; the offending line flagged and ringed"},
     {"at": 0.4, "event": "the error line lands and is ringed (settled before 45 %)"}],
    "editor capture of the shader editor's own error panel (E2, optional)",
    "A real compile log from a real run is exact, free and reproducible; it is rung one of SHOW-THE-THING. The editor panel would need a driver.",
    "evidence/planning-checks/run-16-broken-shader-with-definition-line-raw-log.log (the script's one printed line and the engine's own lines, run 2026-10-13 on Apple M4 Pro, Forward+; "
    "run-9-broken-shader-raw-log.log is the first run without the printed line, engine lines identical); the build re-runs broken.gd and pastes the lines verbatim (trimmed of the GDScript backtrace)",
    lane="terminal")


manim("B15", 1, "varying: a value set at each corner, blended across the shape", "Varying",
      "A rectangle with four terracotta corner dots; each corner shows its world number ('536, 336', '664, 336', '536, 464', '664, 464'). Inside, a pixel grid of outline cells tints "
      "from the corners inward: the red channel as a smooth ramp from the left pair to the right pair, each cell showing a tiny blended value. Card: 'varying: a value set at each "
      "corner, blended across the shape for fragment() to read'.",
      "The four corner values flow inward and the cells between them fill with smoothly blended values.",
      [{"at": 0.1, "event": "quad with four corner values"}, {"at": 0.36, "event": "definition card"}, {"at": 0.66, "event": "cells fill with blended values"}],
      "ShaderLab (05-world-field video)",
      "Four known values becoming a value for every pixel in between is the mechanism; the real render comes in the next beat.",
      "docs: 'set for every primitive vertex in the vertex processor, and the value is interpolated for every pixel in the fragment processor'; verify3.gd T5 (interpolated world position within 0.07 px of exact)")

lab("B16", 1, "world position as a color: the sprite is a window onto a color field that stays put", "05-world-field.gdshader", f"{PUB}/world-field.mp4",
    "Godot 4.7.2 · Forward+ · scripted slide", [{"at": 0.12, "lines": [3, 6]}, {"at": 0.28, "lines": [10]}],
    "Code card at the left with the varying and the vertex line highlighted, then the fragment line; at the right a real Godot window: a faint color field (red grows left to right, green top to bottom) "
    "and a test sprite sliding over it, filled with the same field at full strength. Readouts '0' and '1' at the field's edges.",
    "As the sprite slides right it turns redder, because it shows the part of the field that is at its new place.",
    [{"at": 0.12, "event": "varying and the vertex line"}, {"at": 0.28, "event": "fragment line: world position becomes color"}, {"at": 0.52, "event": "sprite slides right and turns redder"}],
    "Manim color-field plane",
    "Code and its live result side by side: the colors change as the sprite slides, which is exactly 'a window onto a field that stays put'.",
    "C03: scene script capture-scenes/capture-c03.gd: faint backdrop ColorRect (05-world-field, alpha 0.35), blob sprite (256 px art) at y=360 with 05-world-field.gdshader, resting at x=300 then sliding to x=980 over 52 to 80 % of the beat; 13 s (CAPTURE-PLAN.md).",
    "verify12.gd C03; Lab probes 05-world-field ((672,392) -> 0.5255, 0.5451, 0.8 = world / (1280, 720), blue 0.8); frame evidence/planning-checks/png/scene-world-field.png",
    readouts=[{"at": 0.1, "text": "0", "x": 0.03, "y": 0.92}, {"at": 0.1, "text": "1", "x": 0.97, "y": 0.92}])

# ═════════════════════════════ ACT III · Locked to the World ═════════════════════════════
manim("B17", 2, "U V is local space squeezed to zero to one", "UVIsLocalToo",
      "Act title 'Locked to the World' (serif 40) top-left. A sprite square with local numbers on its axes (-64 to 64) and a zero marker at its center; a second set of numbers "
      "'0 to 1' along its top and left edge. The zero marker slides from the center to the top-left corner while the center's numbers squeeze: '(-64,-64)' becomes '(0, 0)' and "
      "'(64, 64)' becomes '(1, 1)'. Card: 'UV: a point's address on the shape: 0 to 1 across, 0 to 1 down'. A small 'stuck to the sprite' chip.",
      "The zero slides from the sprite's center to its corner and the numbers squeeze from minus sixty-four to sixty-four down to zero to one.",
      [{"at": 0.1, "event": "sprite with local numbers"}, {"at": 0.36, "event": "zero slides to the corner, numbers squeeze"}, {"at": 0.66, "event": "card and chip: stuck to the sprite"}],
      "LectureEvidenceTable (local pixels against U V)",
      "U V is local space with its zero moved and its scale squeezed; the zero sliding while the numbers rescale shows that, a table does not.",
      "V4g (UV at the corner pixel 0.0039 and at the far corner 0.99608 = (local + 64) / 128); docs: UV 'Normalized texture coordinates. Range from 0.0 to 1.0.'")

manim("B18", 2, "one line changes: the varying comes from the model matrix instead of from vertex", "OneLineChanges",
      "Two code lines morph. 'position = VERTEX;' transforms into 'position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;' while the fragment line "
      "'COLOR.rgb = texture(sky, position / tile_size).rgb;' stays grey and unchanged beneath. A chip over the changing line flips from 'local' to 'world'; a grey bracket outlines the unchanged line, with the small grey label 'texture(sky, address): reads the sky picture at that address' under it.",
      "The right side of the first line transforms into the matrix expression while the fragment line below does not change at all.",
      [{"at": 0.1, "event": "both lines, chip 'local'"}, {"at": 0.36, "event": "the first line morphs"}, {"at": 0.66, "event": "chip 'world'; the fragment line unchanged"}],
      "LectureCodeTrace (a diff)",
      "One line becoming another shows 'one line changes' literally, and the untouched line below shows what did not.",
      "lab-shaders/01-sky-local.gdshader and 02-sky-world.gdshader differ in exactly one line (diff); Lab probes at the same pixel: 0.0627 against 0.3137")

manim("B19", 2, "world position divided by a tile size makes an address that wraps", "TileAddress",
      "A horizontal world axis from 0 to about 1500 with tick marks at 512 and 1024. A terracotta dot travels along it; below, a plot of 'address' against world x: a sawtooth that rises from "
      "0 to 1 and wraps back to 0 at every 512, with the dot's current address as a live readout. Label: 'tile size 512'.",
      "The dot rides along the world axis while the address ramps from zero to one and wraps back to zero at every five hundred twelve.",
      [{"at": 0.1, "event": "axis, ticks at 512 and 1024, the address plot"}, {"at": 0.4, "event": "the dot travels, the address climbs to 1"}, {"at": 0.68, "event": "wraps to 0 at 512 and climbs again"}],
      "ShaderLab (02-sky-world with a gradient)",
      "A divide and a wrap are a function reshaping a ramp; the dot on the sawtooth is that function in motion.",
      "Lab probes 02-sky-world on a rect: (800, 100) reads 0.5647 = texel 144 of 256 = fract(800.5 / 512) * 256")

lab("B20", 2, "repeat enable tiles the picture; without it the edge pixels smear", "02-sky-world.gdshader", f"{PUB}/repeat.mp4",
    "Godot 4.7.2 · Forward+ · the same view, one setting changed", [{"at": 0.28, "lines": [2], "label": "repeat_enable: the picture tiles forever"}, {"at": 0.66, "lines": [5], "label": "repeat_disable: edge pixels smear outward"}],
    "A code card at the left with the two setting lines, each tagged with what it does (comments name the files); at the right a real Godot window filled by the star sky read by world position: first the picture tiles across the whole "
    "view (the ringed planet repeats every 512 pixels); at the switch the setting changes to repeat_disable and everything beyond the first tile smears into horizontal and vertical streaks.",
    "The picture tiles, then at the switch it collapses into streaks past the first copy.",
    [{"at": 0.04, "event": "the view tiles"}, {"at": 0.28, "event": "repeat_enable line highlighted"}, {"at": 0.64, "event": "the shader switches to repeat_disable; streaks past the first tile"}],
    "two stills side by side",
    "The same view switching from tiling to smearing is the only picture where 'like this' can be pointed at.",
    "C04: scene script capture-scenes/capture-c04.gd: full-view ColorRect with 02-sky-world.gdshader, switched to 06-sky-no-repeat.gdshader at 64 % of the beat; 10 s (CAPTURE-PLAN.md).",
    "verify12.gd C04; Lab probes 02-sky-world (800,100) = 0.5647 and 06-sky-no-repeat (800,100) = 1.0; a hint-less sampler also clamps (lab-try run); frames scene-sky-repeat-on.png and scene-sky-repeat-off.png",
    code=("// 02-sky-world.gdshader\nuniform sampler2D sky : repeat_enable;\n\n// 06-sky-no-repeat.gdshader\nuniform sampler2D sky : repeat_disable;"),
    code_file="lab-shaders/02-sky-world.gdshader · 06-sky-no-repeat.gdshader (the one line that differs)", layout="side")

lab("B21", 2, "a sprite sliding over a sky that stays put", "02-sky-world.gdshader", f"{PUB}/sky-window.mp4",
    "Godot 4.7.2 · Forward+ · scripted slide", [{"at": 0.2, "lines": [13]}, {"at": 0.62, "lines": [9]}],
    "Code card at the left (the world-locked sky shader); at the right a real Godot window: a faint star sky and a test sprite filled with the same sky at full strength, sliding "
    "right across the ringed planet and coming to rest over it. The stars and the planet inside the sprite line up exactly with the faint copy behind it, all the way to the sprite's edge.",
    "The sprite slides over the planet and its stars never shift against the faint copy behind it.",
    [{"at": 0.12, "event": "sprite starts to slide over the sky"}, {"at": 0.2, "event": "the sky lookup line"}, {"at": 0.5, "event": "sprite at rest over the planet; its picture continues the faint copy at the edge"},
     {"at": 0.62, "event": "position line"}],
    "Manim",
    "The picture of the claim is a window sliding over a fixed sky with a faint copy proving the alignment; a drawing would need the stars to be believed.",
    "C05: scene script capture-scenes/capture-c05.gd: one sprite at y=240, x 640 to 880 over 10 to 50 % of the beat, then at rest over the planet (the planet and most of its ring sit inside the sprite, the ring's left tip outside it); faint backdrop (alpha 0.35); 12 s (CAPTURE-PLAN.md).",
    "verify12.gd C05; verify5.gd W1 (identical colours at fixed screen pixels, equal to the reference sky), W4 (planet cream (215,204,177) over the world sprite, indigo (91,106,163) over the local one)")

lab("B22", 2, "turn and stretch the sprite: the sky does not care", "02-sky-world.gdshader", f"{PUB}/turn-stretch.mp4",
    "Godot 4.7.2 · Forward+ · scripted turn and stretch", [],
    "A real Godot window: the faint star sky and a plain white square sprite (a window) over the ringed planet. The square turns forty-five degrees, then stretches wide and low; "
    "the planet and stars inside it never move. Readouts 'turned' and 'stretched' appear as each happens.",
    "The square's corners swing around and its shape stretches while the stars and the planet inside it stay exactly where they are.",
    [{"at": 0.05, "event": "square over the planet"}, {"at": 0.1, "event": "turns 45 degrees; readout 'turned'"}, {"at": 0.26, "event": "stretches; readout 'stretched'"}],
    "Manim",
    "A square turning and stretching over unchanged stars is the claim; a plain square rather than the blob makes the turn visible.",
    "C06: scene script capture-scenes/capture-c06.gd: white 128 px art at (852,240), scale 2; rotation 0 to 45 degrees over 6 to 22 % of the beat, then scale (2,2) to (2.5,1.6) over 24 to 38 %; 12 s (CAPTURE-PLAN.md).",
    "verify12.gd C06; verify5.gd W3 (the same colours at the same five screen pixels before and after the turn and stretch); frame scene-world-square-turned.png", layout="video",
    readouts=[{"at": 0.1, "text": "turned", "x": 0.5, "y": 0.9}, {"at": 0.26, "text": "stretched", "x": 0.5, "y": 0.9}])

lab("B23", 2, "texture pixel size ties the pattern to the sprite's art", "07-pattern-texel-size.gdshader", f"{PUB}/texel-size.mp4",
    "Godot 4.7.2 · Forward+ · the art is swapped near the end · scripted", [{"at": 0.1, "lines": [12], "label": "TEXTURE_PIXEL_SIZE: 1 over the art's width and height"}],
    "Code card at the left (position times texture pixel size); at the right a real Godot window: a test sprite filled with a checker pattern by world position. At the swap its art changes "
    "from 128 pixels to 64 pixels (drawn at the same size on screen) and the checks shrink to half. Readouts '128 px art' then '64 px art'.",
    "The sprite stays the same size on screen but the checks halve as the art is swapped.",
    [{"at": 0.1, "event": "texture pixel size line; 128 px art, large checks"}, {"at": 0.78, "event": "art swapped to 64 px; the checks halve"}],
    "Manim: two sprites with different art sizes and their tiles",
    "Swapping the art for a smaller image and watching the checks shrink is the pitfall itself, shown rather than said.",
    "C07: scene script capture-scenes/capture-c07.gd: blob sprite, art 128 px at scale 2, 07-pattern-texel-size with a checker texture; at 78 % of the beat the texture is swapped to a 64 px blob drawn at scale 4; 12.6 s (CAPTURE-PLAN.md).",
    "verify12.gd C07; verify4.gd V4e (TEXTURE_PIXEL_SIZE 1/128 and 1/64), verify6.gd T1 (9 and 17 colour changes along 140 px); frame scene-texel-size.png",
    readouts=[{"at": 0.1, "text": "128 px art", "x": 0.5, "y": 0.9}, {"at": 0.8, "text": "64 px art", "x": 0.5, "y": 0.9}])

lab("B24", 2, "discard by world position: a hole that stays where it is", "08-world-hole.gdshader", f"{PUB}/hole.mp4",
    "Godot 4.7.2 · Forward+ · scripted slide", [{"at": 0.12, "lines": [11], "label": "distance(a, b): how far apart two points are"}, {"at": 0.27, "lines": [12], "label": "discard: throw this pixel away"}],
    "Code card at the left (the distance test and discard); at the right a real Godot window: a thin grey circle marks a hole fixed in the world; a test sprite slides across it: a bite appears "
    "at its edge, grows into a round hole inside the sprite while the two overlap, and slides out of the other side, whole again.",
    "The hole stays still while the sprite slides across it: a bite, then a round hole inside the sprite, then whole again.",
    [{"at": 0.12, "event": "distance test line; the ring marks the hole"}, {"at": 0.4, "event": "sprite enters; a bite, then a round hole in its middle"}, {"at": 0.85, "event": "sprite leaves the hole whole"}],
    "Manim",
    "The hole is a thing in the world; a sprite cut by a circle that does not move is the effect itself.",
    "C08: scene script capture-scenes/capture-c08.gd: blob sprite (256 px art) at y=360 sliding x 440 to 840 over 40 to 92 % of the beat across a hole at (640,360) radius 60; a thin grey ring (3 px, #8F8A7B) drawn by the scene; 11.5 s (CAPTURE-PLAN.md).",
    "verify12.gd C08; Lab probes 08-world-hole: (699,360) discarded, (700,360) kept (radius 60 from (640,360)); verify8.gd S5 and verify6.gd H1 (frame scene-hole-partial.png)")

lab("B25", 2, "the payoff: a mix amount turns the character into a window onto the stars", "09-spacing-out.gdshader", f"{PUB}/spacing-out.mp4",
    "Godot 4.7.2 · Forward+ · scripted walk, amount animated 0 to 1", [{"at": 0.14, "lines": [4], "label": "amount: 0 keeps the sprite, 1 shows only the sky"}, {"at": 0.3, "lines": [13], "label": "mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b"}],
    "Code card at the left (the mix amount and the sky lookup); at the right a real Godot window: the faint star sky and the test sprite walking right across the ringed planet. As it walks "
    "the sprite's teal and eyes dissolve into stars: when it passes the planet it is a sprite-shaped window onto the sky.",
    "The sprite's own color dissolves into the stars as the amount climbs, while it walks across the fixed sky.",
    [{"at": 0.14, "event": "amount uniform; the sprite is itself"}, {"at": 0.3, "event": "mix line"}, {"at": 0.52, "event": "the sprite walks and the amount climbs: teal dissolves"}, {"at": 0.8, "event": "over the planet it is a window onto the sky"}],
    "LectureCodeTrace alone",
    "The payoff must be the real thing: all the earlier ideas working together on the real sprite.",
    "C09: scene script capture-scenes/capture-c09.gd: one sprite at y=240, x 560 to 1000 over 50 to 95 % of the beat; amount set to 0.0 from code first, then a tween 0 to 1 over 52 to 78 %; 12 s (CAPTURE-PLAN.md).",
    "verify12.gd C09; Lab probes 09-spacing-out at amount 0, 0.5, 1 (teal, mixed, sky); verify7.gd N3 (set_shader_parameter first, then tween: teal (95,163,145) to planet cream (215,204,177))")

# ═════════════════════════════ ACT IV · Where Is the Screen? ═════════════════════════════
manim("B26", 3, "effects that stay on the glass: the screen address", "StaysOnTheGlass",
      "Act title 'Where Is the Screen?' (serif 40) top-left. A window frame (the glass) with a soft grey tint along its four inner edges and a small terracotta flash mark in a corner, "
      "over a field of dots that is the world. The world slides left and right behind the window; the tint and the flash mark do not move. Label 'stays on the glass'.",
      "The world's dots slide behind the window while the edge tint and the flash mark stay fixed on the glass.",
      [{"at": 0.1, "event": "window with edge tint and flash mark over a field of dots"}, {"at": 0.36, "event": "the world slides left; the tint stays"}, {"at": 0.66, "event": "label 'stays on the glass'"}],
      "ShaderLab capture of a vignette",
      "A window over a scrolling world with a tint that does not scroll shows 'stays on the glass wherever the camera points'; the capture of the same idea comes in the last act.",
      "docs: Camera2D scrolls 'the screen (current layer)'; canvas layers keep UI 'fixed in screen-space'; verify6.gd A1 (screen stripes unchanged by a camera pan)")

manim("B27", 3, "canvas matrix: world numbers to screen numbers; the camera lives there", "CanvasMatrix",
      "Two labelled 4 by 4 tables side by side: 'model matrix' with its last column '600, 400, 0, 1' ringed and 'canvas matrix' with its last column '-250, -100, 0, 1' ringed. The window slides right "
      "over the world (a camera pan); the canvas table's last column ticks to '-350, -100, 0, 1' while the model table does not change. Then the camera zooms in: the canvas table's two diagonal "
      "ones become twos while the model table stays. A card: 'canvas matrix: world to screen (Godot calls it canvas space)'.",
      "The window pans and zooms and only the canvas matrix's numbers change; the model matrix's numbers stay put.",
      [{"at": 0.1, "event": "two tables with their last columns"}, {"at": 0.3, "event": "the window pans; canvas numbers tick, model numbers still"}, {"at": 0.42, "event": "zoom: the diagonal ones become twos"},
       {"at": 0.66, "event": "definition card"}],
      "LectureEvidenceTable (matrix, what it does, what changes it)",
      "Which matrix changes when the camera moves is the whole point; the camera moving while one table ticks and the other does not shows it.",
      "verify9.gd M1, M3a to M3c (model last column (600,400,0,1) before and after the zoom; canvas last column (-250,-100,0,1), then (-350,-100,0,1) after the pan; zoom 2 gives diagonal 2 and (-560,-440,0,1)); "
      "verify4.gd V4c; docs: CANVAS_MATRIX, Camera2D")

manim("B28", 3, "chain the matrices right to left: the corner meets the model matrix first", "RightToLeft",
      "The expression CANVAS_MATRIX * MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0) across the middle, with a grey arrow under it pointing right to left. A small token '(-64, -64)' starts at the right, "
      "passes into the model matrix box and comes out '(536, 336)', passes into the canvas matrix box (the camera zoomed in on the sprite) and comes out '(512, 232)' inside a window frame.",
      "The corner's token passes through the model matrix, then the canvas matrix, from right to left, and ends inside the window at (512, 232).",
      [{"at": 0.1, "event": "expression and the right-to-left arrow"}, {"at": 0.34, "event": "token through the model matrix: (536, 336)"}, {"at": 0.66, "event": "through the canvas matrix: (512, 232) in the window"}],
      "LectureCodeTrace line focus",
      "Order is a path, not a sentence: a token passing through two boxes shows which comes first.",
      "verify3.gd T3 (camera zoomed 2x on the sprite: corner at screen (512, 232)); docs: transform functions are 'directed from right to left'")

manim("B29", 3, "the wrong order lands far outside the window", "WrongOrder",
      "The same picture with the two boxes swapped in the expression MODEL_MATRIX * CANVAS_MATRIX * vec4(VERTEX, 0.0, 1.0). The token '(-64, -64)' now passes the canvas box first and "
      "then the model box and flies out beyond the window's left and top edges to '(-88, -168)', outside the frame, with a grey 'outside the window' mark.",
      "The token leaves the window and lands far off its top-left corner.",
      [{"at": 0.1, "event": "swapped boxes"}, {"at": 0.36, "event": "token through the canvas box first"}, {"at": 0.66, "event": "it lands at (-88, -168), outside the window"}],
      "ShaderLab capture of 11-wrong-order under a zoomed camera",
      "The token flying out of the window is the wrong order as motion; the wrong shader's picture would be a flat blue field, which says less.",
      "verify3.gd T3 (swapped order reads (-88, -168) at the corner pixel); lab-shaders/11-wrong-order.gdshader compiles in the Lab")

manim("B30", 3, "vertex in fragment is a different thing: the pixel's screen position", "SameNameTwoSpaces",
      "Two function boxes stacked, vertex() above and fragment() below, each holding a chip with the same name VERTEX. A pixel on a small sprite icon (the corner pixel) has two grey arrows: "
      "to vertex(), where the chip reads '(-64, -64)' with the tag 'local'; to fragment(), where the chip reads '(286.5, 236.5)' with the tag 'screen, in pixels'.",
      "The same name VERTEX sits in both boxes and changes its number and its tag as it moves from one to the other.",
      [{"at": 0.1, "event": "two boxes, same name"}, {"at": 0.36, "event": "in vertex(): (-64, -64), local"}, {"at": 0.66, "event": "in fragment(): (286.5, 236.5), screen"}],
      "LectureEvidenceTable (two rows)",
      "The same chip hopping between two boxes and changing its number is 'same name, different space'; two table rows only list it.",
      "verify7.gd N1 (VERTEX in fragment at the corner pixel = (286.5, 236.5), the pixel centre); docs: fragment VERTEX 'Pixel position in screen space'")

rem("B31", 3, "frag coord: the docs say one, one; the engine counts pixels", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html",
     "image": f"{PUB}/docs-canvas-item-shader.png",
     "caption": "Godot 4.7 documentation · canvas item shader · FRAGCOORD · measured in Godot 4.7.2 on Forward+: last pixel of a 1280 by 720 window reads 1279.5, 719.5",
     "frame": "browser", "moves": [{"at": 0, "x": 0.5, "y": 0.5, "scale": 1}, {"at": 0.22, "x": 0.5, "y": 0.5, "scale": 2.2, "ring": [0.25, 0.46, 0.8, 0.54]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 canvas item shader reference in a browser window, scrolled to the FRAGCOORD row; the camera pushes in on the sentence about the bottom-right corner being one, one "
    "and a terracotta ring marks it. The caption carries the measured reading.",
    "The camera pushes in on the one-one sentence and the ring closes on it; the caption holds the measured number.",
    [{"at": 0, "event": "the reference page, FRAGCOORD row in view"}, {"at": 0.22, "event": "push-in and ring on the bottom-right sentence"}, {"at": 0.7, "event": "caption with the measured reading"}],
    "manim: a quoted line beside a measured number",
    "SHOW-THE-THING: the claim is about what the documentation says, so the documentation page itself is the evidence; the measurement goes in the caption.",
    "D2: Playwright capture of the live page (1600x900 at 2.4x) scrolled to the FRAGCOORD row, at build time; verify1.gd S1 (FRAGCOORD at the last pixel = 1279.5, 719.5 in a 1280 by 720 window)")

manim("B32", 3, "screen U V is the same place as a fraction; screen pixel size converts", "PixelsToFraction",
      "A window frame with a terracotta dot at a pixel and its tag '(286.5, 236.5) pixels'. Beside it a small card 'screen pixel size = (1/1280, 1/720)'. The tag multiplies down through the card "
      "and becomes '(0.2238, 0.3285)', labelled 'SCREEN_UV'; the dot gets a second tag in the same place. A ramp strip from 0 to 1 along the window's top shows the fraction.",
      "The pixel tag multiplies by the pixel-size card and shrinks into the fraction tag at the same dot.",
      [{"at": 0.1, "event": "dot with the pixel tag"}, {"at": 0.36, "event": "the pixel-size card; the tag multiplies"}, {"at": 0.66, "event": "fraction tag 0.2238, 0.3285 = SCREEN_UV"}],
      "LectureEvidenceTable",
      "A conversion is a function acting on a number; the tag shrinking through a card shows it, a table only lists the pair.",
      "verify4.gd V4f (SCREEN_UV at pixel (286,236) = (0.22382, 0.32846); SCREEN_PIXEL_SIZE = (1/1280, 1/720)); docs: SCREEN_PIXEL_SIZE 'Equal to the inverse of resolution'")

lab("B33", 3, "four ways, one picture: four tiles grow into a single seamless gradient", None, f"{PUB}/four-tiles.mp4",
    "Godot 4.7.2 · Forward+ · 1920 by 1080 window · one shader per tile, switched on in turn", [{"at": 0.2, "lines": [2]}, {"at": 0.32, "lines": [4]}, {"at": 0.42, "lines": [6]}, {"at": 0.58, "lines": [8]}],
    "Code card at the left (the key line of each of the four shaders, comments name the method); at the right a real Godot window in four tiles outlined in thin grey. Each tile starts flat grey and "
    "switches on in turn, painting itself red-green-blue by its own screen address; after the fourth the whole window is one seamless gradient. Tile labels 'canvas matrix', 'vertex', 'frag coord', 'screen UV'.",
    "Each tile joins the gradient in turn with no seam.",
    [{"at": 0.2, "event": "tile one (canvas matrix) switches on"}, {"at": 0.32, "event": "tile two (vertex)"}, {"at": 0.42, "event": "tile three (frag coord)"}, {"at": 0.58, "event": "tile four (screen UV); one seamless gradient"}],
    "LectureEvidenceTable of four probe values",
    "A gradient that grows tile by tile with no seam is the agreement as a picture; a table of numbers would ask for trust.",
    "C10: scene script capture-scenes/capture-c10.gd: four 960x540 ColorRects on a 1920x1080 canvas (top-left 10, top-right 12, bottom-left 13, bottom-right 14) on flat grey (#BDB8AA), switched on in that order at 20, 32, 42 and 58 % of the beat; "
    "thin grey tile outlines (3 px) drawn by the scene; 11.6 s. ROUTE: 1920x1080 at scale 1, not the 3x SubViewport route, because shaders 10, 12 and 13 read window pixels (series rule; CAPTURE-PLAN.md).",
    "verify12.gd C10 at 1920x1080 scale 1 (worst difference 0 of 255 over 128 pixels off the seams and over 8 beside them); verify13.gd B (the same tiles, 144 pixels, worst 0) and A (the 3x route also gives worst 0, so the picture is the same on both routes); verify6.gd F1 (each shader against the exact gradient, worst difference 0 of 255, in five setups: plain, camera panned, zoomed 2x, rect turned 20 degrees, window stretched 2x); Lab probes 10 to 14 identical",
    code=("// canvas matrix, from vertex()\nCOLOR.rgb = vec3(screen_position * SCREEN_PIXEL_SIZE, 0.8);\n// vertex, read in fragment()\n"
          "COLOR.rgb = vec3(VERTEX * SCREEN_PIXEL_SIZE, 0.8);\n// frag coord\nCOLOR.rgb = vec3(FRAGCOORD.xy * SCREEN_PIXEL_SIZE, 0.8);\n// screen U V\nCOLOR.rgb = vec3(SCREEN_UV, 0.8);"),
    code_file="lab-shaders/10, 12, 13, 14 (the key line of each)", layout="side",
    readouts=[{"at": 0.2, "text": "canvas matrix", "x": 0.25, "y": 0.25}, {"at": 0.32, "text": "vertex", "x": 0.75, "y": 0.25},
              {"at": 0.42, "text": "frag coord", "x": 0.25, "y": 0.75}, {"at": 0.58, "text": "screen UV", "x": 0.75, "y": 0.75}])

manim("B34", 3, "screen pixels are real window pixels; a fraction does not care", "RealPixels",
      "A small window and the same window doubled with a small chip 'stretch mode: canvas items', side by side, each holding the same sprite. Under each: 'world 128' and 'screen 128' for the small one; "
      "for the large one 'world 128' stays and 'screen 256' counts up as the window grows. A ramp strip labelled 'SCREEN_UV' under both stays at 0 to 1 in each.",
      "The window doubles; the sprite's screen width counts from 128 to 256 while its world width stays 128 and the 0-to-1 strip stays 0-to-1.",
      [{"at": 0.1, "event": "small window, sprite, tags world 128, screen 128"}, {"at": 0.38, "event": "window grows to twice the size"}, {"at": 0.66, "event": "screen 256, world 128; the fraction strip unchanged"}],
      "capture of a stretched window",
      "A window doubling in size while one number counts up and another does not is the contrast; a real stretched capture would need a second render at another scale for the same sentence.",
      "verify7.gd N2 (base 640x360 shown in 1280x720: world span 127.5, screen span 255 between first and last pixel centres); verify6.gd F1 window-stretched-2x (screen-fraction shaders unchanged)")

# ═════════════════════════════ ACT V · Choosing a Space ═════════════════════════════
manim("B35", 4, "which space? ask what the effect should stay stuck to", "StuckTo",
      "Act title 'Choosing a Space' (serif 40) top-left. Three columns, each a small drawing with a terracotta pin: 'the sprite' (a sprite square, the pin on it), 'a place in the level' (a map "
      "outline with the pin on a spot), 'the glass' (a window frame with the pin on the glass). Under them two grey arrows appear: 'slide the sprite' and 'pan the camera'.",
      "The pin lands on the sprite, then on a place in the level, then on the glass; the two test arrows appear last.",
      [{"at": 0.1, "event": "three columns"}, {"at": 0.3, "event": "pins land one by one: sprite, level, glass"}, {"at": 0.66, "event": "the two test arrows"}],
      "LibraryIconRow (three marks)",
      "Three things a pattern can be stuck to are three tethers; a pin landing on each in turn shows the choice, and the arrows foreshadow the test.",
      "design; the test itself is verify6.gd A1")

lab("B36", 4, "slide the sprites: the local stripes ride along; world and screen stripes stay put", None, f"{PUB}/anchors-slide.mp4",
    "Godot 4.7.2 · Forward+ · the three sprites slide right by 160 · scripted", [],
    "A real Godot window: three test sprites in a row, each filled with white stripes by a different shader; column labels 'local', 'world' and 'screen' above them. "
    "At the start the three stripe patterns look identical. The three sprites slide right by 160; the left one's stripes move with it, the middle and right stripes stay put on the screen and each sprite slides over them.",
    "At the end of the slide the left sprite's stripes are the opposite phase of the other two.",
    [{"at": 0.0, "event": "three identical-looking striped sprites, labelled"}, {"at": 0.24, "event": "all three slide right by 160"}, {"at": 0.62, "event": "left sprite's stripes shifted against the other two"}],
    "Manim stripes",
    "Moving things in a real scene and watching which stripes move is the experiment itself.",
    "C11a: scene script capture-scenes/capture-c11a.gd: three blob sprites (256 px art, scale 1) at x = 256, 640, 1024 (y 360) with 15-anchor-local, 16-anchor-world, 17-anchor-screen; Camera2D at (640,360); slide +160 over 24 to 60 % of the beat; 10.5 s (CAPTURE-PLAN.md).",
    "verify12.gd C11a; verify6.gd A1 (local: pattern relative to the sprite unchanged; world and screen: changed, identical to each other); frames scene-anchors-start.png, scene-anchors-after-slide.png", layout="video",
    readouts=[{"at": 0.02, "text": "local", "x": 0.2, "y": 0.16}, {"at": 0.02, "text": "world", "x": 0.5, "y": 0.16}, {"at": 0.02, "text": "screen", "x": 0.8, "y": 0.16}])

lab("B37", 4, "pan the camera: local and world stripes travel with their sprites; only the screen stripes stay", None, f"{PUB}/anchors-pan.mp4",
    "Godot 4.7.2 · Forward+ · the camera pans right by 160 · scripted", [],
    "The same three sprites at their start positions, same column labels. The camera pans right by 160, so the sprites slide left on screen; the left and middle sprites carry their stripes with them, "
    "the right sprite slides left over stripes that stay where they were on the glass.",
    "The left and middle sprites keep their stripes as they slide left; the right sprite slides over stripes that do not move.",
    [{"at": 0.0, "event": "three identical-looking striped sprites, labelled"}, {"at": 0.22, "event": "camera pans right by 160; the sprites slide left"}, {"at": 0.62, "event": "the right sprite's stripes shifted against the other two"}],
    "Manim stripes",
    "The second move is the one that separates world from screen; only a real camera pan shows it without any doubt.",
    "C11b: scene script capture-scenes/capture-c11b.gd: the camera goes from (640,360) to (800,360) over 22 to 60 % of the beat; 12.6 s (CAPTURE-PLAN.md).",
    "verify12.gd C11b; verify6.gd A1 (local and world: pattern relative to the sprite unchanged by the pan; screen: changed); frame scene-anchors-after-pan.png", layout="video",
    readouts=[{"at": 0.02, "text": "local", "x": 0.2, "y": 0.16}, {"at": 0.02, "text": "world", "x": 0.5, "y": 0.16}, {"at": 0.02, "text": "screen", "x": 0.8, "y": 0.16}])

rem("B38", 4, "the map: which numbers come from where", "LectureEvidenceTable",
    {"title": "Which space, and where the numbers come from", "headers": ["Space", "Stuck to", "Numbers come from"],
     "rows": [["local", "the sprite", "VERTEX, in vertex()"], ["world", "a place in the level", "MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)"],
              ["screen", "the window", "CANVAS_MATRIX, or SCREEN_UV"]],
     "note": "Godot 4.7 shader reference · every row checked in Godot 4.7.2", "cues": [0.14, 0.4, 0.66], "durationSeconds": "__AUDIO__"},
    "A three-row table, one row ringed as each space is named: local, world, screen, with what each is stuck to and where its numbers come from.", "The ring moves down the rows with the voice.",
    [{"at": 0.14, "event": "local row"}, {"at": 0.4, "event": "world row"}, {"at": 0.66, "event": "screen row"}],
    "manim",
    "A summary of three parallel facts is exactly what the table component is for; the pictures came in the acts.",
    "verify1.gd, verify3.gd, verify6.gd; docs")

manim("B39", 4, "one line picks the space", "OneLineDecides",
      "Three code cards stacked: the stripe shader's key lines for local ('position = VERTEX;'), world ('position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;') and screen "
      "('float stripe = step(0.5, fract(SCREEN_UV.x * 20.0));'). In each the line that picks the space is highlighted with a grey bracket and the rest is grey. A chip names each: local, world, screen. Under the screen card two small grey labels give the glossary wording "
      "of the two small words that line uses (they are not spoken): 'fract(x): the part after the point' and 'step(edge, x): 0 below the edge, 1 from the edge up'.",
      "A bracket moves down the three cards and lands on the one line that differs in each.",
      [{"at": 0.1, "event": "local card, its line bracketed"}, {"at": 0.36, "event": "world card, its line bracketed"}, {"at": 0.66, "event": "screen card: SCREEN_UV in fragment"}],
      "LectureCodeTrace",
      "Three versions of one shader with the deciding line moving down them shows 'the line that sets the position picks the space'.",
      "lab-shaders/15, 16 (differ in one line, diff) and 17; Lab probes 15 to 17 compile and agree at the start")

manim("B40", 4, "check an AI's shader with two moves", "TwoMoves",
      "A short checklist drawn as outline rows: 'compiles' (check mark drawn), 'looks right in a still' (check mark drawn), 'survives the two moves' (empty box). A small striped sprite icon to the right "
      "slides right (a grey arrow) and then a window frame slides over it (a second grey arrow): after both the third box gets its check mark, or a cross drawn in grey.",
      "The first two boxes tick at once; the third waits while the sprite slides and the camera pans, and only then settles.",
      [{"at": 0.1, "event": "checklist; two ticks"}, {"at": 0.36, "event": "slide arrow: the third box waits"}, {"at": 0.66, "event": "pan arrow, then the third box settles"}],
      "ClaudeCodeBeat (a prompt and a reply)",
      "The advice is about a habit, not a tool screen; a checklist whose last box waits for a test shows why a still is not enough.",
      "verify6.gd A1: at the start the three striped sprites look identical (scene-anchors-start.png): a still cannot tell the spaces apart; the two moves can")

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(5):
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
sl = ["# Shot list: Local, World and Screen Space\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab, scene-script or editor capture of a tested file in `lab-shaders/`. Six things must be built or recorded first (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`; shared, built once). 2. **`shader_kit.py`** Manim helpers (same file) **plus four film-local helpers** "
      "this film needs and the kit does not list: `world_window_scene` (the world rectangle, the window frame and the sprite with its corner dot, used by B03 to B07 and B26 to B34), `origin_marker` "
      "(a ring with a right arrow and a down arrow), `address_tag` (a number pair that attaches to a point and can count), `matrix_table` (a 4 by 4 grid of outline cells with one column or row highlightable). "
      "3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` with the scene-script route (same file); the reference scene scripts are `evidence/planning-checks/capture_scenes.gd` (contract `build` / `at(t)` / `route()`, one wrapper per capture in `capture-scenes/`), built on `scenes_lib.gd` and `sky_lib.gd`; `route()` says whether a capture goes through the 4K SubViewport route or, for shaders that read window pixels (C10 only), 1920 by 1080 at scale 1 (the series rule). "
      "4. **Editor frame E1** (B11) is already recorded by script (copy it; E2 is optional for B14) and the **docs screenshot D2** (B31) is taken with Playwright (see `CAPTURE-PLAN.md`). 5. **The sky texture** (procedural, seed 7: `sky_lib.gd`) and the **checker** (B23). "
      "6. **The broken-shader log** for B14 (`broken.gd`, re-run at build time).\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
