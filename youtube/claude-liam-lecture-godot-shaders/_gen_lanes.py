#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text, and the shot list must say exactly what the lanes say.
Other films may write lanes/*.json and SHOTLIST.md by hand; this is just the pilot's way. Re-run after any edit:
    python3 _gen_lanes.py && python3 make_sheet.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
E = []          # entries in beat order


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects)"):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, ramp=None, title=None, code=None, code_file=None, lane="capture", caption=""):
    props = {"layout": layout, "code": code if code is not None else (code_of(shader) if shader else ""),
             "codeFile": code_file or (f"lab-shaders/{shader}" if shader else ""), "cues": cues,
             "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption,
             "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    add(bid, act, about, {"lane": lane, "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": intent,
                          "motion_claim": motion, "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


def rem(bid, act, about, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, act, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


# ───────────────────────────── ACT I · One Pixel, All at Once ─────────────────────────────
lab("B01", 0, "a game that works but looks flat", "02-hook-wobble.gdshader", "godot-shaders/hook.mp4",
    "Godot 4.7.2 · same scene, shader switched on at 2 s · scripted", [],
    "Act title 'One Pixel, All at Once' (serif 40) top-left. A real Godot render in a framed window on the cream stage: the teal test sprite sits flat and still for two seconds, then a shader is switched on and it wobbles. Label: 'same scene, shader switched on'.",
    "The sprite is still, then comes alive the moment the shader switches on.",
    [{"at": 0.0, "event": "flat sprite, window labelled"}, {"at": 0.22, "event": "shader switches on; the sprite starts to wobble"}],
    "manim drawing of a flat versus lively sprite", "A real render is the honest picture of 'looks flat' versus 'looks alive'; a drawing would only claim it.",
    "C01: Lab sprite scene (teal test sprite, scale to fit), shader lab-shaders/02-hook-wobble.gdshader assigned at t=2.0 s (--material-at 2.0), 10 s, 30 fps, Forward+, no input.",
    "Lab render (C01); shader compiled in Lab", layout="video", title="One Pixel, All at Once")
manim("B02", 0, "what a shader is; what game code vs shader decide", "WhatAndWhere",
      "Two boxes on the cream stage. Left, 'your game code · CPU' with a small teal sprite icon and the words 'what exists, where'. Right, 'the shader · GPU' with the same icon, now with a wobble drawn around it, and 'how each part looks'. One arrow, left to right.",
      "The sprite icon is placed on the left, travels along the arrow and arrives restyled on the right.",
      [{"at": 0.1, "event": "left box + icon"}, {"at": 0.42, "event": "icon travels along the arrow"}, {"at": 0.7, "event": "restyled icon in the right box"}],
      "DesignPipelineClaim, show-tell isometric", "A two-box handoff is the whole claim; an icon that visibly changes on arrival says it with motion.")
manim("B03", 0, "CPU as a few fast workers, GPU as a crowd", "ManyWorkers",
      "A 12-by-6 grid of outline cells. Top: one dot-worker colours the cells one after another, a counter ticking. Bottom: a crowd of dots colours all 72 cells in the same instant. Labels: 'CPU: one job after another', 'GPU: the same job at once'.",
      "One worker sweeps the grid cell by cell while the whole second grid fills at once.",
      [{"at": 0.1, "event": "single worker starts sweeping"}, {"at": 0.45, "event": "crowd fills the second grid at once"}, {"at": 0.78, "event": "first grid still filling"}],
      "isometric workers on a conveyor (show-tell)", "A grid filled one cell at a time versus all at once is the CPU/GPU difference, as motion.")
rem("B04", 0, "the slow way: a GDScript loop over every pixel", "LectureCodeTrace",
    {"title": "The slow way: a GDScript loop",
     "code": "var big := Image.create_empty(\n\t\t1920, 1080, false, Image.FORMAT_RGBA8)\nfor y in range(1080):\n\tfor x in range(1920):\n\t\tbig.set_pixel(x, y, Color(x / 1919.0, 0.0, 0.0))",
     "note": "2,073,600 calls for one 1920 by 1080 picture · Godot 4.7.2", "cues": [0.06, 0.2, 0.34, 0.62], "durationSeconds": "__AUDIO__"},
    "The real loop from evidence/planning-checks/verify.gd on a cream code card, with the call count underneath.",
    "Line focus steps down the loop as it is described; the count lands last.",
    [{"at": 0.06, "event": "image line"}, {"at": 0.34, "event": "inner loop"}, {"at": 0.62, "event": "set_pixel line + count note"}],
    "CCPlainShell", "LectureCodeTrace's paced line focus matches the sentence; the shell has no per-line cue.",
    "verify.gd (naive loop, run 2026-10-13)")
manim("B05", 0, "55 ms against a 16.7 ms frame", "FrameBudget",
      "A horizontal time axis from 0 to 60 ms. A vertical budget line at 16.7 ms labelled 'one frame at 60 per second'. A bar grows along the axis, passes the line and stops at about 55, labelled 'the loop · about 55 ms'. Small grey credit: 'Apple M4 Pro · Godot 4.7.2 · five runs: 52 to 58 ms'.",
      "The bar grows past the budget line and keeps going.",
      [{"at": 0.15, "event": "axis + budget line"}, {"at": 0.4, "event": "bar grows"}, {"at": 0.72, "event": "bar stops near 55; credit line"}],
      "LectureEvidenceTable", "A bar crossing a line shows 'over budget'; a table only lists the numbers.",
      "verify.gd D (53.8 and 58.4 ms) and run 2")
lab("B06", 0, "the shader way: one line describes one pixel", "01-gradient.gdshader", "godot-shaders/gradient.png",
    "Godot 4.7.2 · Forward+ · the shader on the left", [{"at": 0.1, "lines": [3]}, {"at": 0.62, "lines": [4]}],
    "Code card with the four-line shader at left; at right a real Godot window showing a black-to-red gradient with a thin 0 to 1 ramp under it.",
    "The line is highlighted, then the red ramp is traced left to right under the gradient.",
    [{"at": 0.1, "event": "function line highlighted"}, {"at": 0.62, "event": "COLOR line highlighted; ramp marker sweeps"}],
    "LectureCodeTrace alone", "Code and its result side by side is the claim: one line, the whole picture.",
    "C02: Lab rect, lab-shaders/01-gradient.gdshader, still PNG 1920x1080 (probes: 0.0196 / 0.498 / 0.9804 at x = 0.02 / 0.5 / 0.98).",
    "Lab probes 01-gradient", ramp={"at": 0.62, "from": 0, "to": 1}, readouts=[{"at": 0.2, "text": "0", "x": 0.03, "y": 0.9}, {"at": 0.2, "text": "1", "x": 0.97, "y": 0.9}])
manim("B07", 0, "what the shader way cost the processor", "HandOver",
      "'game code · CPU' box at left, 'shader · GPU' box at right. An arrow between them labelled 'hands over the job · about 0.04 ms'. Under the GPU box, in grey: 'its own time: not readable on this setup'. Small credit: 'Apple M4 Pro · Godot 4.7.2'.",
      "A tiny package travels the arrow; the GPU box fills with pixels while the CPU box stays nearly empty.",
      [{"at": 0.12, "event": "boxes + arrow"}, {"at": 0.4, "event": "package travels; GPU box fills"}, {"at": 0.75, "event": "grey 'not readable' note"}],
      "LectureEvidenceTable, two rows", "A handoff arrow with a speck of a cost label shows the idea; the grey note keeps the claim honest.",
      "verify2.gd E (0.035 to 0.038 ms CPU; GPU timer returned 0)")
manim("B08", 0, "the flip: describe one pixel, run it everywhere", "OnePixelThenAll",
      "A 16-by-9 pixel grid of outline cells. One cell gets a terracotta ring and a small code card beside it ('COLOR = …'). Then every cell takes its ramp color at once, left to right, the card staying put. Label: 'one pixel's rule → every pixel'.",
      "One ringed pixel, then the whole grid changes in the same instant.",
      [{"at": 0.12, "event": "grid, one cell ringed, code card"}, {"at": 0.6, "event": "all cells take their color at once"}],
      "ShaderLab", "This is the film's central claim; only a grid shows 'one rule, every pixel' at a glance.")
rem("B11", 1, "Godot's shader language, in the docs", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html",
     "image": "godot-shaders/docs-shading-language.png", "caption": "Godot 4.7 documentation · Shading language · captured at build time",
     "frame": "browser", "moves": [{"at": 0, "x": 0.5, "y": 0.3, "scale": 1}, {"at": 0.22, "x": 0.42, "y": 0.28, "scale": 1.5}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 shading-language page in a browser window; the camera pushes in on the sentence that says it is similar to GLSL ES 3.0 and a terracotta ring marks it.",
    "The camera pushes in on the sentence the voice is describing.",
    [{"at": 0, "event": "page"}, {"at": 0.22, "event": "push-in + ring on the GLSL sentence"}],
    "manim: GDScript line beside a shader line", "The language claim is a documentation claim; the documentation itself is the evidence (SHOW-THE-THING).",
    "Playwright capture of the live docs page (1600x900 at 2.4x) at build time; read 2026-10-13: 'similar to GLSL ES 3.0'")
manim("B09", 1, "node, ShaderMaterial, Shader", "ThreeBoxes",
      "Act title 'Setting Up a Shader' (serif 40) top-left. Three boxes slide in left to right and link: 'a node (Sprite2D, ColorRect…)' → 'ShaderMaterial' → 'your shader (.gdshader file)'. A small dot travels from the shader back to the node.",
      "Each box slides in as it is named; the dot travels back to the node, meaning 'look'.",
      [{"at": 0.12, "event": "node box"}, {"at": 0.42, "event": "ShaderMaterial box"}, {"at": 0.66, "event": "shader box + dot travels back"}],
      "DesignPipelineClaim, show-tell isometric", "Three nested things is a structure with a shape; a drawn chain with a travelling dot is clearer than prose.")
lab("B10", 1, "the editor clicks that attach a shader", None, "godot-shaders/editor-attach.mp4",
    "Godot 4.7.2 editor · four real frames", [],
    "Four real frames of the Godot editor's Inspector for a Sprite2D, one per state: Material empty; ShaderMaterial added; a Shader added; the shader editor open. Slow cross-dissolves between them; a terracotta ring on the slot being named.",
    "The ring moves slot to slot as the voice names each click.",
    [{"at": 0.1, "event": "Material slot ringed (empty)"}, {"at": 0.38, "event": "ShaderMaterial in the slot"}, {"at": 0.66, "event": "Shader slot ringed"}, {"at": 0.86, "event": "shader editor open"}],
    "GodotDevWorkbench (labelled reconstruction)", "Real editor frames are the rung-1 SHOW-THE-THING answer; the reconstruction is the labelled fallback.",
    "E1: four real editor states recorded by the editor driver (editor-capture/README.md): Material empty; Shader Material in the slot (menu: heading New, then ShaderMaterial); a Shader added (New Shader..., Create Shader dialog, mode Canvas Item); the shader editor open in the bottom panel. Scripted editor session; the clicks themselves are not shown.",
    "Editor capture E1 (recorded by script: _godot-shaders-series/editor-capture/png/1920x1080/godot-shaders/)", layout="video", lane="editor")

# ───────────────────────────── ACT II · The Three Functions ─────────────────────────────
manim("B12", 1, "the first line: shader types", "TwoWorlds",
      "Left: the line `shader_type canvas_item;` over a flat teal sprite icon. Right: `shader_type spatial;` over a small isometric cube. Three small tiles fade in underneath: particles, sky, fog.",
      "The two first lines type in, each over its picture, then the three small tiles arrive.",
      [{"at": 0.1, "event": "canvas_item line + flat sprite"}, {"at": 0.36, "event": "spatial line + cube"}, {"at": 0.66, "event": "particles, sky, fog tiles"}],
      "LectureEvidenceTable", "Two worlds side by side, each with its own first line, is the contrast the sentence names.")
lab("B13", 1, "the smallest working shader", "03-red.gdshader", "godot-shaders/red.png", "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.12, "lines": [3]}, {"at": 0.6, "lines": [4]}],
    "Code card with the five-line shader at left; a real Godot window filled with pure red at right.",
    "The function line then the COLOR line are highlighted; the window is red the whole time.",
    [{"at": 0.12, "event": "fragment line"}, {"at": 0.6, "event": "COLOR line; four numbers called out"}],
    "LectureCodeTrace alone", "The whole shader fits on screen with its result; nothing else teaches it faster.",
    "C03: Lab rect, lab-shaders/03-red.gdshader, still (probe 0.5,0.5 = 1.0, 0.0, 0.0).", "Lab probe 03-red")
rem("B14", 1, "vertex, fragment, light: the engine calls them", "LectureCodeTrace",
    {"title": "A shader's special functions",
     "code": code_of("14-skeleton.gdshader"), "note": "The engine calls these for you · Godot 4.7 shader reference",
     "cues": [0.04, 0.04, 0.2, 0.2, 0.3, 0.36, 0.36, 0.38, 0.58, 0.6], "durationSeconds": "__AUDIO__"},
    "A cream code card with the three empty function bodies (ten lines); focus lands on vertex, then fragment, then light as each is named.",
    "Focus steps down the three functions on their names.",
    [{"at": 0.2, "event": "vertex"}, {"at": 0.36, "event": "fragment"}, {"at": 0.6, "event": "light"}],
    "manim", "The skeleton is real code; paced line focus is exactly 'here are the three'.", "lab-shaders/14-skeleton.gdshader compiles in the Lab")
manim("B15", 2, "vertex runs once per corner; a rectangle has four", "FourCorners",
      "Act title 'The Three Functions' (serif 40) top-left. A rectangle with four terracotta corner dots, each labelled in turn 'vertex() runs' with a counter 1, 2, 3, 4. Caption: 'its job: place the corners'.",
      "The four corners flash one after another and the counter ticks.",
      [{"at": 0.12, "event": "rectangle"}, {"at": 0.3, "event": "corners flash in order"}, {"at": 0.7, "event": "caption"}],
      "ShaderLab", "Four dots flashing in turn is the literal meaning of 'once for each vertex'.")
lab("B16", 2, "a real vertex() leaning a rectangle by fifty pixels", "04-lean.gdshader", "godot-shaders/lean.mp4",
    "Godot 4.7.2 · Forward+ · shader switched on at 1 s · scripted", [{"at": 0.2, "lines": [4]}],
    "Code card at left; at right a real Godot window with a teal-and-cream checker square (128 px) that, at 1 s, leans: the bottom edge slides 50 px right while the top stays. A terracotta ring on the bottom edge, a readout '+50 px'.",
    "The square shears sideways the moment the shader switches on.",
    [{"at": 0.2, "event": "VERTEX line highlighted"}, {"at": 0.34, "event": "ring on the bottom edge; +50 px"}],
    "manim", "A real shear measured to the pixel; a drawing could only illustrate it.",
    "C03b: Lab sprite, checker 128 px at scale 1.0 (--sprite-scale 1.0), lab-shaders/04-lean.gdshader assigned at 1.0 s; measured edge shift 50 px (evidence/planning-checks/lean-edge.txt, white-square render).",
    "Lab + analyze-lean.py (shift 50 px over 128 rows)", readouts=[{"at": 0.34, "text": "+50 px", "x": 0.68, "y": 0.78}], rings=[{"at": 0.34, "box": [0.4, 0.7, 0.9, 0.82]}])
manim("B17", 2, "the GPU fills between corners; even steps", "EvenSteps",
      "The leaning square's left edge drawn as a slanted line with five sample dots at 2, 25, 50, 75 and 98 percent of the height, labelled with the real measured shifts +1, +12, +25, +37, +49 px. A caption: 'four corners → straight edges'.",
      "The five dots land one after another down the edge, each with its measured number, evenly spaced.",
      [{"at": 0.14, "event": "slanted edge"}, {"at": 0.4, "event": "five dots with numbers"}, {"at": 0.72, "event": "caption"}],
      "ShaderLab with readouts", "The even spacing of five real measurements is the proof that nothing was calculated between the corners.",
      "evidence/planning-checks/lean-edge.txt (edge x = 257, 268, 281, 293, 305 from 256)")
manim("B18", 2, "fragment runs once per covered pixel", "FillIn",
      "A pixel grid with the rectangle drawn over it. The covered cells tint one by one, each carrying a tiny 'fragment()' tag; then all covered cells hold their tint at once while the tags stay.",
      "Covered cells tint one by one, then the whole shape is filled.",
      [{"at": 0.12, "event": "grid + rectangle"}, {"at": 0.36, "event": "cells tint with tags"}, {"at": 0.7, "event": "all covered cells filled"}],
      "ShaderLab", "The covered-cell grid is the only way to see 'each pixel the shape covers'.")
manim("B19", 2, "pixel shader and fragment shader are two names", "TwoNames",
      "Two labels, 'pixel shader' and 'fragment shader', point to one box. Then a strip: 'fragment' → 'tests, blending' → 'pixel', with the caption 'a fragment is a pixel-to-be'. No company names or logos on screen; the voice names the graphics systems.",
      "Both labels slide into the same box, then a fragment travels through the strip and becomes a pixel.",
      [{"at": 0.12, "event": "two labels, one box"}, {"at": 0.5, "event": "strip appears"}, {"at": 0.74, "event": "fragment becomes pixel"}],
      "LectureEvidenceTable", "Two names for one thing, and a pixel-to-be travelling to a pixel, are both motions.")
lab("B20", 2, "discard: a fragment that never becomes a pixel", "05-discard-half.gdshader", "godot-shaders/discard.png",
    "Godot 4.7.2 · Forward+ · the shader on the left", [{"at": 0.2, "lines": [4, 5]}],
    "Code card at left with the discard lines; at right a real Godot window: the left half a green-orange gradient, the right half the plain stage color, as if the shape were cut in half.",
    "The discard lines are highlighted and a ring settles on the empty right half.",
    [{"at": 0.2, "event": "if + discard lines"}, {"at": 0.62, "event": "ring on the empty half: the background shows through"}],
    "manim", "A real render with half the shape gone, and the code that did it.",
    "C04: Lab rect, lab-shaders/05-discard-half.gdshader, still (probes: left colored; right = stage color 0.851, 0.835, 0.792).",
    "Lab probes 05-discard", readouts=[{"at": 0.62, "text": "no pixel here", "x": 0.75, "y": 0.5}], rings=[{"at": 0.62, "box": [0.5, 0.0, 1.0, 1.0]}])
lab("B21", 2, "light() runs once per light; an empty one replaces the default", "13-light-count.gdshader", "godot-shaders/light-count.mp4",
    "Godot 4.7.2 · Forward+ · dark canvas, white point lights added one by one · scripted", [{"at": 0.1, "lines": [3, 4]}],
    "Code card at left (a light() that outputs a constant 0.2 red); at right a real Godot window on a dark canvas: a square gets brighter in steps as a white light is added at 1 s, 2.5 s and 4 s. Readouts '1 light · 0.2', '2 lights · 0.4', '3 lights · 0.6'.",
    "The square steps up in brightness each time a light appears.",
    [{"at": 0.1, "event": "light function highlighted"}, {"at": 0.3, "event": "1 light · 0.2"}, {"at": 0.6, "event": "2 lights · 0.4"}, {"at": 0.85, "event": "3 lights · 0.6"}],
    "manim", "Three measured steps (0.2, 0.4, 0.6) prove 'once per light, and the results add' better than a sentence.",
    "C05: custom scene from evidence/planning-checks/verify4.gd: CanvasModulate black, white Sprite2D with 13-light-count.gdshader, PointLight2D added at 1.0, 2.5, 4.0 s; 6 s; Forward+. Measured 0.2 / 0.4 / 0.6; empty light() -> black (0.0), no light() -> white (1.0).",
    "verify4.gd run 4b (0.2, 0.4, 0.6)", readouts=[{"at": 0.3, "text": "1 light · 0.2", "x": 0.7, "y": 0.2}, {"at": 0.6, "text": "2 lights · 0.4", "x": 0.7, "y": 0.2}, {"at": 0.85, "text": "3 lights · 0.6", "x": 0.7, "y": 0.2}])
manim("B22", 2, "the fixed order: corners, fill, colors", "Order",
      "A three-stage strip left to right: 'vertex() places the corners' → 'the GPU fills the shape' → 'fragment() colors each pixel'. A token travels the strip; the arrows are drawn shapes pointing only forward.",
      "A token passes through the three stages in order and never goes back.",
      [{"at": 0.12, "event": "stage 1"}, {"at": 0.4, "event": "stage 2"}, {"at": 0.66, "event": "stage 3"}],
      "DesignPipelineClaim, show-tell isometric", "A token moving forward through three stages is the order of work.")
manim("B23", 2, "built-ins: values handed in and out", "FunctionBox",
      "A box labelled 'fragment()'. Arrows come in from the left labelled UV, TIME, TEXTURE (capital letters, in a monospace face) and one arrow goes out to the right labelled COLOR. Caption: 'built-ins · capital letters'.",
      "The inputs slide into the box one by one and the single output leaves on the right.",
      [{"at": 0.12, "event": "box"}, {"at": 0.36, "event": "three inputs arrive"}, {"at": 0.68, "event": "COLOR leaves"}],
      "LectureEvidenceTable", "Inputs arriving and an output leaving makes 'values handed in and out' literal.")
rem("B24", 2, "the three functions in one table", "LectureEvidenceTable",
    {"title": "The three functions", "headers": ["Function", "Runs", "It sets"],
     "rows": [["vertex()", "once per vertex", "where a corner goes"], ["fragment()", "once per pixel", "that pixel's color"], ["light()", "per pixel, per light", "how a light lights it"]],
     "note": "Godot 4.7 shader reference · counts checked in Godot 4.7.2", "cues": [0.12, 0.4, 0.66], "durationSeconds": "__AUDIO__"},
    "A three-row table, one row ringed as each function is named.", "The ring moves down the rows with the voice.",
    [{"at": 0.12, "event": "vertex row"}, {"at": 0.4, "event": "fragment row"}, {"at": 0.66, "event": "light row"}],
    "manim", "A summary of three parallel facts is exactly what the table component is for.", "Run C, verify4.gd, docs")

# ───────────────────────────── ACT III · Dials: Uniforms ─────────────────────────────
manim("B25", 3, "the shader is out of reach of the game", "OutOfReach",
      "Act title 'Dials: Uniforms' (serif 40) top-left. 'your game · GDScript' box at left, 'the shader · GPU' box at right with a pane of glass between them. A terracotta question dot hovers at the glass.",
      "A message dot leaves the game box, stops at the glass and bounces.",
      [{"at": 0.1, "event": "two boxes + glass"}, {"at": 0.5, "event": "dot stops at the glass"}],
      "LectureCodeTrace", "The problem is 'no way through'; a pane of glass is the picture of it.")
lab("B26", 3, "a uniform declared outside the functions", "06-dial.gdshader", "godot-shaders/dial-default.png",
    "Godot 4.7.2 · Forward+ · red = 0.5", [{"at": 0.12, "lines": [3]}, {"at": 0.7, "lines": [6]}],
    "Code card at left with the uniform line highlighted, then the line that uses it; at right a real Godot window colored by red = 0.5.",
    "Focus lands on the uniform line, then on the line that reads it.",
    [{"at": 0.12, "event": "uniform line"}, {"at": 0.7, "event": "COLOR line that reads red"}],
    "LectureCodeTrace alone", "Declaration and use side by side with the result.",
    "C06a: Lab rect, lab-shaders/06-dial.gdshader at the default (probe 0.502, 0.451, 0.451).", "Lab probes 06-dial",
    readouts=[{"at": 0.3, "text": "red = 0.5", "x": 0.5, "y": 0.9}])
lab("B27", 3, "the uniform becomes a slider in the Inspector", None, "godot-shaders/editor-slider.mp4",
    "Godot 4.7.2 editor · three real frames", [],
    "Three real frames of the Inspector's Shader Parameters group with the red slider at 0.2, 0.5 and 0.9, and the sprite beside it in the matching color. Readouts show the value.",
    "The slider knob and the color step through the three real states.",
    [{"at": 0.2, "event": "red = 0.2"}, {"at": 0.5 + 0.12, "event": "red = 0.5"}, {"at": 0.84, "event": "red = 0.9"}],
    "ShaderLab video of the Lab render with the same values", "Real editor frames are the strongest evidence that a slider appears.",
    "E2: three static editor frames of a scratch project with shader_parameter/red saved at 0.2, 0.5, 0.9 in the scene file; Inspector scrolled to the Material's Shader Parameters group. The 'Shader Parameters' group name is confirmed by this capture.",
    "Editor capture E2 (recorded by script: _godot-shaders-series/editor-capture/png/1920x1080/godot-shaders/)", layout="video", lane="editor",
    readouts=[{"at": 0.2, "text": "0.2", "x": 0.5, "y": 0.9}, {"at": 0.62, "text": "0.5", "x": 0.5, "y": 0.9}, {"at": 0.84, "text": "0.9", "x": 0.5, "y": 0.9}])
lab("B28", 3, "three uniforms make a color mixer", "07-mixer.gdshader", "godot-shaders/mixer.mp4", "Godot 4.7.2 · Forward+ · values swept by script",
    [{"at": 0.08, "lines": [3]}, {"at": 0.2, "lines": [4]}, {"at": 0.3, "lines": [5]}, {"at": 0.7, "lines": [8]}],
    "Code card at left (three uniforms, one COLOR line); at right a real Godot window whose color moves as red, then green, then blue sweep from 0 to 1.",
    "Three sweeps in turn, each changing the color.",
    [{"at": 0.08, "event": "red uniform"}, {"at": 0.2, "event": "green uniform"}, {"at": 0.3, "event": "blue uniform"}, {"at": 0.7, "event": "the COLOR line"}],
    "ShaderLab stills", "Motion of the color under three sweeps is the point.",
    "C07: Lab rect, lab-shaders/07-mixer.gdshader; red 0 to 1 over 0-2 s, green 0 to 1 over 2-4 s, blue 0 to 1 over 4-6 s (--animate sequence); 6 s, 30 fps. Probe at (1.0, 0.5, 0.0) = (1.0, 0.502, 0.0).",
    "Lab probe 07-mixer")
rem("B29", 3, "hints: how the editor shows a uniform", "LectureEvidenceTable",
    {"title": "A hint shapes the editor, not the math", "headers": ["Hint", "The editor shows"],
     "rows": [["hint_range(0.0, 1.0)", "a number box with a slider bar"], ["source_color", "a color swatch that opens a picker"]],
     "note": "Godot 4.7 shading language reference · uniform hints", "cues": [0.2, 0.62], "durationSeconds": "__AUDIO__"},
    "A two-row table pairing each hint with the widget it makes.", "Each row lands on its words.",
    [{"at": 0.2, "event": "hint_range row"}, {"at": 0.62, "event": "source_color row"}],
    "editor frames", "Two facts in two rows; the real widgets already appeared in the previous editor beat.", "docs hint list; E2")
manim("B30", 3, "a hint does not clamp a value set from code", "NoClamp",
      "A slider track from 0 to 1 with a knob. A code line sets 7.0. An arrow shoots past the end of the track to a label 'stored: 7.0'. Caption: 'the slider only guards the editor'.",
      "The value arrow overshoots the end of the track and lands on 7.0.",
      [{"at": 0.12, "event": "track + knob"}, {"at": 0.4, "event": "code sets 7.0"}, {"at": 0.7, "event": "arrow overshoots; stored: 7.0"}],
      "ShaderLab", "An arrow leaving the end of a slider is the literal picture of 'does not clamp'.",
      "verify3.gd F (stored 7.0, run 2026-10-13)")
lab("B31", 3, "set_shader_parameter from the game", None, "godot-shaders/set-parameter.mp4",
    "Godot 4.7.2 · scripted run · the call fires at 1 s", [{"at": 0.2, "lines": [1]}],
    "A one-line GDScript card at left; at right a real Godot window that changes color from red = 0.5 to red = 0.9 at the moment the call fires.",
    "The color jumps when the highlighted call fires.",
    [{"at": 0.2, "event": "the call highlighted"}, {"at": 0.62, "event": "color change"}],
    "LectureCodeTrace", "The cause (one line) and the effect (the color) together.",
    "C09: scene with a ColorRect named Rect (06-dial.gdshader); at t=1.0 s a script runs `$Rect.material.set_shader_parameter(\"red\", 0.9)`; 3 s; Forward+.",
    "verify3.gd G (correct name 0.898)", code='$Rect.material.set_shader_parameter("red", 0.9)',
    code_file="scene script (GDScript)", readouts=[{"at": 0.62, "text": "red: 0.5 → 0.9", "x": 0.5, "y": 0.9}])
lab("B32", 3, "a misspelled uniform name is a silent no-op", None, "godot-shaders/typo.mp4",
    "Godot 4.7.2 · scripted run · typo at 1 s, correct name at 2.2 s", [{"at": 0.15, "lines": [1]}, {"at": 0.7, "lines": [2]}],
    "A two-line GDScript card (the typo `rd`, then the correct `red`); at right a real Godot window that does not change after the first line and changes after the second. Readouts: 'no change · no error', then 'now it changes'.",
    "Nothing happens on the typo; the color moves on the correct name.",
    [{"at": 0.15, "event": "typo line"}, {"at": 0.4, "event": "no change · no error"}, {"at": 0.7, "event": "correct line; color changes"}],
    "LectureCodeTrace", "A non-event is hard to show; the two-line contrast with a held frame makes it visible.",
    "C10: same scene as C09; at 1.0 s set_shader_parameter(\"rd\", 0.9) (no change), at 2.2 s set_shader_parameter(\"red\", 0.9) (changes); 3.5 s. Verified: red stays 0.2 after the typo; 0.898 after the correct name; no error in the log.",
    "verify3.gd G", code='$Rect.material.set_shader_parameter("rd", 0.9)   # typo\n$Rect.material.set_shader_parameter("red", 0.9)',
    code_file="scene script (GDScript)", readouts=[{"at": 0.4, "text": "no change · no error", "x": 0.5, "y": 0.9}, {"at": 0.78, "text": "now it changes", "x": 0.5, "y": 0.9}])
lab("B33", 3, "tween a uniform (after setting its start)", None, "godot-shaders/tween.mp4", "Godot 4.7.2 · scripted run", [{"at": 0.1, "lines": [1]}, {"at": 0.3, "lines": [2, 3]}],
    "A three-line GDScript card (set the start value, create the tween, tween the property); at right a real Godot window whose color sweeps smoothly from red = 0 to red = 1 over two seconds.",
    "The color sweeps while the tween lines are highlighted.",
    [{"at": 0.1, "event": "set_shader_parameter start line"}, {"at": 0.3, "event": "tween lines; sweep begins"}],
    "ShaderLab stills", "A smooth sweep is the claim: 'the shader follows, every frame'.",
    "C11: scene as C09; set_shader_parameter(\"red\", 0.0) first, then tween_property(material, \"shader_parameter/red\", 1.0, 2.0); 3 s. Verified start 0.0, mid 0.49 at 0.25 s, end 1.0 (verify3.gd H). A tween on a uniform never set from code fails: 'property does not exist' (run-5a, kept).",
    "verify3.gd H; run-5a (failure) and run-5b (fix)", code='$Rect.material.set_shader_parameter("red", 0.0)\nvar tween := create_tween()\ntween.tween_property($Rect.material, "shader_parameter/red", 1.0, 2.0)',
    code_file="scene script (GDScript)", readouts=[{"at": 0.5 + 0.1, "text": "0 → 1 in 2 s", "x": 0.5, "y": 0.9}])
manim("B34", 4, "uniform: the same for every pixel, unlike the pixel's address", "SameForAll",
      "Act title 'Where Am I, and When?' (serif 40) top-left. Left panel: a dial with lines running to every cell of a small pixel grid, each cell showing the same number 0.5. Right panel: the same grid where each cell shows its own two numbers (u, v). Captions: 'uniform: the same everywhere', 'address: different for each'.",
      "The dial's lines fan out to every cell, then the second grid fills with a different pair per cell.",
      [{"at": 0.12, "event": "dial + fan of lines"}, {"at": 0.55, "event": "second grid with addresses"}],
      "LectureEvidenceTable", "A fan of lines from one dial versus a different label in each cell is the contrast itself.")
rem("B35", 4, "uniform and built-ins compared", "LectureEvidenceTable",
    {"title": "Two kinds of input", "headers": ["Name", "Set by", "Same for every pixel?"],
     "rows": [["uniform", "your game", "yes"], ["UV", "the engine", "no, one per pixel"], ["TIME", "the engine", "yes"]],
     "note": "Godot 4.7 shader reference · uniforms and built-ins", "cues": [0.12, 0.4, 0.66], "durationSeconds": "__AUDIO__"},
    "A three-row table with the answer column ringed as each row is named.", "The ring steps down the rows.",
    [{"at": 0.12, "event": "uniform row"}, {"at": 0.4, "event": "UV row"}, {"at": 0.66, "event": "TIME row"}],
    "manim", "A short comparison table is the right shape; the previous beat already drew the picture.", "docs; run B (UV), A2 (TIME)")

# ───────────────────────────── ACT IV · Where Am I, and When? ─────────────────────────────
manim("B36", 4, "UV: the pixel's address", "Address",
      "A square with a 0 to 1 axis along the top and down the left side, the second axis pointing DOWN. A terracotta dot moves across it with a live label (u, v), passing (0.25, 0.75) and ending near (1, 1). Corner labels (0, 0) and (1, 1).",
      "The dot moves to several positions and its (u, v) label updates each time.",
      [{"at": 0.1, "event": "square + axes"}, {"at": 0.4, "event": "dot at (0.25, 0.75)"}, {"at": 0.72, "event": "dot at the bottom right"}],
      "ShaderLab", "Address is a position; a dot with a live label is the clearest picture of it.",
      "run B: UV.y about 0.04 at the top, 0.96 at the bottom (canvas_item)")
lab("B37", 4, "UV used as a color", "08-uv-colors.gdshader", "godot-shaders/uv-colors.png", "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.12, "lines": [4]}],
    "Code card at left; at right a real Godot window showing the red-green UV picture; corner labels land in turn: black (top left), red (top right), green (bottom left), yellow (bottom right).",
    "Corner labels land in the order the voice says the colors.",
    [{"at": 0.12, "event": "COLOR line"}, {"at": 0.62, "event": "black"}, {"at": 0.7, "event": "red"}, {"at": 0.78, "event": "green"}, {"at": 0.86, "event": "yellow"}],
    "manim", "The picture itself is the evidence that the address became a color.",
    "C12: Lab rect, lab-shaders/08-uv-colors.gdshader, still; corner probes 0.0196/0.0196/0 (black), 0.98/0.02/0 (red), 0.02/0.98/0 (green), 0.98/0.98/0 (yellow).",
    "Lab probes 08-uv-colors",
    readouts=[{"at": 0.62, "text": "black", "x": 0.06, "y": 0.08}, {"at": 0.7, "text": "red", "x": 0.94, "y": 0.08}, {"at": 0.78, "text": "green", "x": 0.06, "y": 0.92}, {"at": 0.86, "text": "yellow", "x": 0.94, "y": 0.92}])
lab("B38", 4, "UV used as a fade", "09-uv-fade.gdshader", "godot-shaders/uv-fade.png", "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.2, "lines": [5]}],
    "Code card at left; at right a real Godot window with a cream square that fades from invisible at its left edge to solid at its right edge over the stage color.",
    "The COLOR.a line is highlighted and a 0 to 1 ramp is traced under the fade.",
    [{"at": 0.2, "event": "alpha line"}, {"at": 0.62, "event": "ramp traced"}],
    "manim", "A fade is best seen on the real thing, next to the one line that makes it.",
    "C13: Lab sprite, white 128 px texture (--sprite-tex white), lab-shaders/09-uv-fade.gdshader, still; probes 0.851 (bg) / 0.859 / 0.992.",
    "Lab probes 09-uv-fade", ramp={"at": 0.62, "from": 0, "to": 1})
lab("B39", 4, "TIME inside a sine makes a pulse", "10-pulse.gdshader", "godot-shaders/pulse.mp4", "Godot 4.7.2 · Forward+ · live clock",
    [{"at": 0.15, "lines": [4]}, {"at": 0.34, "lines": [5]}],
    "Code card at left; at right a real Godot window pulsing between red-orange and yellow-orange, with a 0 to 1 ramp whose marker rides the pulse value.",
    "The pulse and the ramp marker move together, back and forth.",
    [{"at": 0.15, "event": "pulse line"}, {"at": 0.34, "event": "COLOR line"}, {"at": 0.7, "event": "pulse keeps running"}],
    "manim sine plot", "A real pulse with its value riding a ramp shows both the result and the number behind it.",
    "C14: Lab rect, lab-shaders/10-pulse.gdshader, 4 s at 30 fps; probes at two times differ (0.6863 and 0.9882 in the green channel).",
    "Lab probes 10-pulse-a/b", ramp={"at": 0.1, "from": 0, "to": 1})
lab("B40", 4, "TIME is one clock: a node added later sees time already gone", "11-time-bar.gdshader", "godot-shaders/time-bar.mp4",
    "Godot 4.7.2 · scripted run · the right-hand node is added at 3 s", [],
    "Two real Godot panels side by side, each a bar that fills from the bottom as time passes: the left present from the start, the right added at 3 s. The instant the right one appears it is already filled to the same height as the left. Readouts: 'present from the start', 'added at 3 s', 'both: 3 s'.",
    "The late bar appears already as full as the early one.",
    [{"at": 0.2, "event": "left bar filling"}, {"at": 0.56, "event": "right bar appears, already at the same height"}, {"at": 0.84, "event": "both: 3 s"}],
    "manim timeline", "A late node appearing already full is the surprising fact; the capture shows it as it happened (the run is the proof).",
    "C15: scene with two ColorRects (left on the start, right added at 3.0 s), both using lab-shaders/11-time-bar.gdshader, 6 s; verified earlier with 32 stripes: both read 12 quarter-seconds (3.0 s) when the late node had existed for two frames (verify2.gd A2).",
    "verify2.gd A2 (12 stripes on both)", layout="video",
    readouts=[{"at": 0.2, "text": "present from the start", "x": 0.25, "y": 0.05}, {"at": 0.62, "text": "added at 3 s", "x": 0.75, "y": 0.05}, {"at": 0.84, "text": "both: 3 s", "x": 0.5, "y": 0.95}])
manim("B41", 4, "one-time effects need a uniform you drive", "ClockVsDial",
      "A horizontal timeline: the game's clock runs from 0 and keeps going (a long grey bar). A terracotta marker 'something happens' sits at about 3. Below, a second short bar 'progress, 0 to 1' starts exactly at the marker and rises to 1. Labels: 'the clock never restarts', 'a uniform you drive'.",
      "The clock bar runs on; at the event marker the progress bar starts from zero.",
      [{"at": 0.12, "event": "clock bar"}, {"at": 0.4, "event": "event marker"}, {"at": 0.7, "event": "progress bar rises from the marker"}],
      "ShaderLab", "The relation between a global clock and an event-started dial is a timeline.")
lab("B42", 4, "the iris: distance, discard and a radius uniform", "12-iris.gdshader", "godot-shaders/iris-sweep.mp4", "Godot 4.7.2 · Forward+ · radius swept by script",
    [{"at": 0.1, "lines": [3]}, {"at": 0.36, "lines": [6]}, {"at": 0.42, "lines": [7]}, {"at": 0.7, "lines": [9]}],
    "Code card at left (the uniform, the distance test, discard, the texture line); at right a real Godot window where a checker square opens from a circle in the middle as radius sweeps from 0 to 0.8.",
    "The circle grows outward while the code lines light up in order.",
    [{"at": 0.1, "event": "radius uniform"}, {"at": 0.36, "event": "distance test"}, {"at": 0.42, "event": "discard"}, {"at": 0.7, "event": "texture line"}],
    "manim", "The film's payoff: all of the earlier ideas working together, shown on the real thing.",
    "C16: Lab sprite, checker 128 px (--sprite-tex checker) at fit scale, lab-shaders/12-iris.gdshader; radius 0.0 to 0.8 over 3 s; probes: radius 0.0 -> centre = stage; 0.3 -> centre cream; 0.8 -> everything visible.",
    "Lab probes 12-iris-0.0/0.3/0.8")
lab("B43", 4, "the game drives the radius on a key press", None, "godot-shaders/iris-key.mp4",
    "Godot 4.7.2 · scripted input: one key press at 1 s", [{"at": 0.12, "lines": [1, 2]}, {"at": 0.3, "lines": [4, 5]}, {"at": 0.4, "lines": [6, 7]}],
    "A seven-line GDScript card at left (set the radius to 0 in _ready, then a key handler that tweens it to 0.8); at right the same iris scene: nothing until a (scripted) key press at 1 s, then the picture opens over 1.5 s. A label 'scripted input' is always on screen.",
    "The picture opens only after the key press.",
    [{"at": 0.12, "event": "_ready sets radius 0"}, {"at": 0.3, "event": "key handler"}, {"at": 0.4, "event": "tween line"}, {"at": 0.7, "event": "picture opens"}],
    "ShaderLab with the earlier capture", "The shader holds the rule and the game holds the moment: cause (key) and effect (iris) together.",
    "C17: iris scene (C16) with this exact script on the scene root; the capture harness sends one physical-key event at t=1.0 s (logged); 4 s; label scripted input. Verified in verify5.gd run 5b: centre goes from the stage color to the sprite color after the key. Run 5a (no _ready line) failed and is kept.",
    "verify5.gd run 5b (key path and tween verified)",
    code='func _ready():\n\t$Sprite.material.set_shader_parameter("radius", 0.0)\n\nfunc _unhandled_key_input(event):\n\tif event.pressed:\n\t\tvar tween := create_tween()\n\t\ttween.tween_property($Sprite.material, "shader_parameter/radius", 0.8, 1.5)',
    code_file="scene script (GDScript)")

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
sl = ["# Shot list: Godot Shaders\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab or editor capture of a tested file in `lab-shaders/`. Five things must be built or recorded first (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`). 2. **`shader_kit.py`** Manim helpers (same file). 3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` (same file). 4. **Editor frames E1, E2** (same file, section on capturing the editor; see `CAPTURE-PLAN.md`). 5. **Docs screenshot** for B09 via Playwright.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
