#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text, and the shot list must say exactly what the lanes say.
Re-run after any edit:
    python3 _gen_lanes.py && python3 make_sheet.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
E = []          # entries in beat order

DOCS_COMPARE = "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#flow-control"
DOCS_BBC = "https://docs.godotengine.org/en/stable/classes/class_backbuffercopy.html#enumerations"


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects; see SHOTLIST 'Must exist')"):
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


FW = "Godot 4.7.2 · Forward+ · scripted"
SCENES = "evidence/planning-checks/capture_scenes.gd"

# ───────────────────────────── ACT I · A Map Nobody Sees ─────────────────────────────
lab("B01", 0, "the finished effect: a walk with a reflection that vanishes over the sand", "02-reflection.gdshader", "reflections/hook-walk.mp4",
    FW + " walk", [],
    "Act title 'A Map Nobody Sees' (serif 40) top-left. A real Godot render in a framed window on the cream stage: the teal blob walks along the shoreline from left to right and its flipped reflection follows in the water, thins out over the sandbar until it is gone, and returns on the far side. Readouts 'over water' and 'over sand'.",
    "The reflection follows the walker, disappears over the sandbar and comes back.",
    [{"at": 0.0, "event": "blob on the shore, reflection under it"}, {"at": 0.10, "event": "readout 'over water'"},
     {"at": 0.44, "event": "readout 'over sand'; reflection thinning over the sandbar"}, {"at": 0.50, "event": "reflection gone (settled by the midpoint)"}, {"at": 0.85, "event": "reflection back on the far side"}],
    "manim drawing of a character and its mirror image",
    "The film's claim is that a hidden map drives a real effect; the real render of the effect is the honest hook, a drawing would only claim it.",
    "C01: capture_scenes.gd id C01 (the pond: LabelMap, BackBufferCopy in viewport mode, Ground, Player with RemoteTransform2D, Reflection with lab-shaders/02-reflection.gdshader); the Player walks x 150 to 1200 over 11.5 s; 13.5 s, 30 fps, Forward+, 4K SubViewport route, scripted walk, fresh process.",
    "run-11 scene runner C01 (reflection 16,380 px over water, 0 over the sand, back on the far side at the 85 % mark; 0 label-map-coloured pixels)", layout="video", title="A Map Nobody Sees",
    readouts=[{"at": 0.10, "text": "over water", "x": 0.50, "y": 0.88}, {"at": 0.44, "text": "over sand", "x": 0.50, "y": 0.88}])
manim("B02", 0, "a shader decides per pixel: show or hide", "PixelAsks",
      "A framed flat picture of the pond (grass band, water, sand spit, teal blob with its reflection area under it). Over the reflection area a grid of 8 by 6 cells appears (the pixel grid); a terracotta dot visits the cells one by one asking 'water?'; each cell then fills teal (show) where it lies over water and stays empty (hide) where it lies over the sand. Label 'show or hide?'.",
      "A dot visits cell after cell and each answer decides the cell: teal where yes, empty where no.",
      [{"at": 0.1, "event": "picture and the empty pixel grid"}, {"at": 0.4, "event": "dot asks 'water?' cell by cell"}, {"at": 0.74, "event": "cells over water filled, cells over sand empty"}],
      "ShaderLab capture with a probe overlay", "The question is asked per pixel and answered per pixel; a grid of cells filled one by one shows the decision itself, which a render of the result cannot.")
lab("B03", 0, "a label map: flat colors, each one a label", None, "reflections/label-map-only.mp4", "Godot 4.7.2 · the label map alone · Forward+ · scripted fade",
    [],
    "The real label map layer alone on the stage colour: the water region flat red, a ring of flat green around the sandbar, everything else empty. It fades in over 2.5 s. Labels land in turn: 'water' on the red, 'coast' on the green ring (with one terracotta ring around the ring), 'empty' on the bare stage.",
    "The map fades in and its labels land on the red, the green and the empty part in the order the voice says them.",
    [{"at": 0.0, "event": "empty stage"}, {"at": 0.2, "event": "label 'water' on the red"}, {"at": 0.34, "event": "label 'coast' + ring on the green ring"}, {"at": 0.62, "event": "label 'empty' on the bare stage"}],
    "manim drawing of the same map", "A label map is a real image; showing the real layer, flat colors and all, is more convincing than a drawing of it.",
    "C02: capture_scenes.gd id C02 (LabelMap node only; Ground, Player, Reflection hidden; LabelMap modulate alpha 0 to 1 over 2.5 s); 13 s, 30 fps, Forward+, scripted fade.",
    "run-11 scene runner C02 (407,248 label-map-coloured pixels once faded in)", layout="video", caption="a label map: a layer of flat colors, each color a label",
    readouts=[{"at": 0.2, "text": "water", "x": 0.25, "y": 0.82}, {"at": 0.34, "text": "coast", "x": 0.69, "y": 0.90}, {"at": 0.62, "text": "empty", "x": 0.30, "y": 0.25}],
    rings=[{"at": 0.36, "box": [0.49, 0.48, 0.89, 0.83]}])
manim("B04", 0, "why read the screen: it is already lined up with every pixel", "LinedUp",
      "Two panels on the cream stage. Left, 'an ordinary texture': a pixel of the pond in the world, a camera frame sliding sideways, and a chain of arrows from the pixel through a box 'your math' to a spot on the map. Right, 'the screen': the same pixel with one straight arrow to the same spot in a screen-sized copy, no box. A small label 'texture: an image a shader can read'.",
      "The camera frame slides and the left chain stretches and re-routes through the math box; the right arrow stays straight.",
      [{"at": 0.1, "event": "both panels, same pixel"}, {"at": 0.42, "event": "camera frame slides; left chain re-routes through 'your math'"}, {"at": 0.74, "event": "right arrow stays straight"}],
      "DesignPipelineClaim, show-tell isometric", "A flow with a moving camera and a recalculation box against a straight line is a structure with a shape; Manim can slide the camera and show only one side needing to re-route.")
lab("B05", 0, "the map drawn over the game: the player sees a red and green sea", None, "reflections/label-map-over-art.mp4", FW + " walk",
    [],
    "The real pond with the label map drawn on top of the Ground: a red and green sea covers the water area and the ring around the sandbar, while the blob keeps walking and its reflection still works. Readout 'player sees this'.",
    "The red and green sea sits over the game while the blob keeps walking.",
    [{"at": 0.0, "event": "the pond with the map on top"}, {"at": 0.18, "event": "readout 'player sees this'"}],
    "manim drawing of the stacked layers in the wrong order", "A real frame of the mistake is more persuasive than a drawing of it, and the walking blob shows it is a live game.",
    "C03: capture_scenes.gd id C03 (tree order Ground, LabelMap, BackBufferCopy, Player, Reflection; shader 02); the Player walks x 300 to 620 over 10 s; 10.5 s, 30 fps, Forward+, scripted walk.",
    "run-04 case C2b (409,604 pixels changed by the label map) and run-11 C03", layout="video",
    readouts=[{"at": 0.18, "text": "player sees this", "x": 0.30, "y": 0.10}])
manim("B06", 0, "draw order: later layers cover earlier ones", "Layers",
      "An isometric stack on the cream stage, three flat slabs landing one after another: 'map' (red and green) first, then 'art' (the pond picture), then 'character' (the teal blob). Beside the stack a top-down thumbnail updates after each slab: after the map, red and green; after the art, only the pond (the red and green gone); after the character, the pond with the blob. Label 'later covers earlier'.",
      "The art slab lowers onto the map slab and the thumbnail's red and green vanish.",
      [{"at": 0.1, "event": "map slab lands; thumbnail red and green"}, {"at": 0.4, "event": "art slab lands; thumbnail shows only the pond"}, {"at": 0.74, "event": "character slab lands; blob appears in the thumbnail"}],
      "ShaderLab capture with layers switched on one by one", "Covering is a spatial idea; an isometric stack with a thumbnail of what the player sees shows both the stack and the result.")
manim("B07", 0, "the screen texture is a copy made at one moment", "CopyMoment",
      "The same slab stack. A copy frame (a camera-like rectangle) slides along the stack. Above the art slab its thumbnail shows only the pond ('no map'); slid down between the map and the art, its thumbnail shows the red and green map. Label 'copy of the screen'.",
      "The frame slides down the stack and its thumbnail turns from the pond into the map.",
      [{"at": 0.1, "event": "frame above the art slab; thumbnail shows the pond"}, {"at": 0.42, "event": "frame slides down between map and art"}, {"at": 0.7, "event": "thumbnail now shows the map; label settled"}],
      "LectureEvidenceTable", "The idea is timing; a frame that slides through the stack shows when the copy is made and what is in it.")
manim("B08", 0, "the node that chooses the moment: BackBufferCopy", "CopyNode",
      "The slab stack with a node chip labelled 'BackBufferCopy' sliding in between the map slab and the art slab; the copy frame snaps onto the chip and its thumbnail shows the map. A one-line label from the docs: 'copies the screen for a shader to read'.",
      "The chip slides between the slabs and the copy frame snaps onto it.",
      [{"at": 0.12, "event": "stack, chip enters"}, {"at": 0.44, "event": "chip sits between map and art; frame snaps on"}, {"at": 0.7, "event": "docs label settles"}],
      "BrowserCapture of the BackBufferCopy docs page", "The node is introduced by name at the moment the stack needs it; the docs page itself appears later, where its three modes are the subject.")
lab("B09", 0, "the draw order is the scene tree: map, copy node, art, character, reflection", None, "reflections/editor-scene-dock.png",
    "Godot 4.7.2 editor · Scene dock · real frame", [],
    "A real frame of Godot's Scene dock for the pond scene: Pond, then LabelMap, BackBufferCopy, Ground, Player (with RemoteTransform2D under it) and Reflection, top to bottom. A readout 'drawn first' by the top row, then one terracotta ring moves down the rows as the voice names map, copy node, art, character, reflection.",
    "The ring steps down the rows in the order the voice names them.",
    [{"at": 0.0, "event": "Scene dock frame"}, {"at": 0.3, "event": "readout 'drawn first'"}, {"at": 0.7, "event": "ring on LabelMap"}, {"at": 0.76, "event": "ring on BackBufferCopy"},
     {"at": 0.82, "event": "ring on Ground"}, {"at": 0.88, "event": "ring on Player"}, {"at": 0.94, "event": "ring on Reflection"}],
    "GodotDevWorkbench tree mode (labelled reconstruction)", "SHOW-THE-THING: the Scene dock is the place where the order is set, so the real dock is the evidence; the reconstruction is the labelled fallback.",
    "E1: Godot's own editor on the scratch pond project (evidence/planning-checks/make-editor-project.sh builds it; verified by verify_scene_file.gd): one frame (Pond selected) recorded at 2560 x 1440 with the Light preset and a 2x UI by evidence/planning-checks/record-editor-frames.sh, cropped to the box (0, 60) to (440, 420). The ring boxes are measured on that crop (rows LabelMap, BackBufferCopy, Ground, Player, Reflection); a planning frame of exactly this crop is png/planning-frame-E1-scene-dock.png.",
    "run-12 (pond.tscn tree order verified); planning frame png/planning-frame-E1-scene-dock.png (film frame E1 to be re-recorded by the build)", layout="video", lane="editor",
    readouts=[{"at": 0.3, "text": "drawn first", "x": 0.80, "y": 0.28}],
    rings=[{"at": 0.70, "box": [0.10, 0.32, 0.92, 0.41]}, {"at": 0.76, "box": [0.10, 0.42, 0.92, 0.51]}, {"at": 0.82, "box": [0.10, 0.52, 0.92, 0.61]},
           {"at": 0.88, "box": [0.10, 0.62, 0.92, 0.71]}, {"at": 0.94, "box": [0.10, 0.81, 0.92, 0.90]}])

# ───────────────────────────── ACT II · When the Screen Is Copied ─────────────────────────────
lab("B10", 1, "three sprites and a window that shows the screen texture", "01-screen-preview.gdshader", "reflections/three-sprites-window.mp4", FW,
    [{"at": 0.36, "lines": [6], "label": "UV: 0 to 1 across the window, so it holds the whole screen"},
     {"at": 0.70, "lines": [3], "label": "hint: tells Godot how to treat it: fill with the screen"}],
    "Act title 'When the Screen Is Copied' (serif 40) top-left. Code card at left (the six-line preview shader); at right a real Godot window: three flat overlapping squares A (teal), B (blue), C (lavender), drawn in that order on the stage colour. At about a quarter of the way in a small framed window appears at top right showing a miniature of the whole screen with A, B and C in it.",
    "The window appears and shows the three squares in miniature while the code lines are highlighted.",
    [{"at": 0.06, "event": "A, B, C land by their labels"}, {"at": 0.26, "event": "the window appears with the miniature"}, {"at": 0.36, "event": "COLOR line highlighted"}, {"at": 0.70, "event": "declaration line with the hint highlighted"}],
    "LectureCodeTrace alone", "Code and its live result side by side is the claim: this short shader puts the screen texture in a window.",
    "C04: capture_scenes.gd id C04 (Sprite2D A, B, C, then ColorRect preview with lab-shaders/01-screen-preview.gdshader and a border panel drawn after it; no BackBufferCopy node; the window is switched on at 3.5 s); 14.5 s, 30 fps, Forward+, scripted.",
    "run-01 case A1 (the window shows A, B and C) and run-11 C04", title="When the Screen Is Copied",
    readouts=[{"at": 0.06, "text": "A", "x": 0.14, "y": 0.45}, {"at": 0.10, "text": "B", "x": 0.30, "y": 0.60}, {"at": 0.14, "text": "C", "x": 0.40, "y": 0.83}, {"at": 0.30, "text": "screen texture", "x": 0.77, "y": 0.52}])
manim("B11", 1, "by default the copy is made at the first reader", "FirstReader",
      "A stack of three flat sprites A, B, C (the act's three colours) with a window-shaped 'shader' chip hovering above. As the chip drops toward the stack a copy frame appears automatically right under the chip and captures A, B and C; a thumbnail shows all three. Caption 'the first shader that reads the screen triggers the copy'.",
      "The shader chip drops toward the stack and, just before it lands, a copy frame appears under it and captures A, B and C.",
      [{"at": 0.12, "event": "stack and chip"}, {"at": 0.4, "event": "chip drops; the copy frame appears under it"}, {"at": 0.7, "event": "thumbnail shows A, B, C; caption settles"}],
      "BrowserCapture of the screen-reading docs page", "The claim is about timing in the draw order; the docs paragraph states it, but a moving stack with a frame appearing exactly when the reader arrives shows it.")
lab("B12", 1, "a Back Buffer Copy after C, then between B and C", None, "reflections/copy-moves-1.mp4", FW + " (the node is moved in the tree at run time)",
    [],
    "The same three squares and window. At 2.5 s a BackBufferCopy node is added after C: the window still shows A, B and C. At 5.5 s the node is moved between B and C: C vanishes from the window while C stays in the main picture. Readouts 'copy after C' then 'B copy C' (the draw order, copy node between the two); one terracotta ring on the window after the change.",
    "C vanishes from the window while it stays on the screen.",
    [{"at": 0.0, "event": "window shows A, B, C"}, {"at": 0.22, "event": "readout 'copy after C'"}, {"at": 0.43, "event": "readout 'B copy C'; C gone from the window"}, {"at": 0.64, "event": "ring on the window"}],
    "ShaderLab with the preview code", "The result is the proof; a real window losing C while C stays visible beside it carries 'it only changes what the copy contains'.",
    "C05: capture_scenes.gd id C05 (three squares and window; BackBufferCopy in viewport mode added after C at 2.5 s, move_child to between B and C at 5.5 s); 14 s, 30 fps, Forward+, scripted tree changes.",
    "run-01 cases A2 and A3; run-11 C05 (C missing from the window after the move)", layout="video",
    readouts=[{"at": 0.22, "text": "copy after C", "x": 0.45, "y": 0.93}, {"at": 0.43, "text": "B copy C", "x": 0.45, "y": 0.93}],
    rings=[{"at": 0.64, "box": [0.57, 0.06, 0.96, 0.47]}])
lab("B13", 1, "between A and B only A is left; before A nothing", None, "reflections/copy-moves-2.mp4", FW + " (the node is moved in the tree at run time)",
    [],
    "The same scene continued: the node starts between B and C, is moved between A and B at 1 s (only A is left in the window) and before A at 3.6 s (the window is empty), while the main picture never changes. Readouts 'A copy B' then 'before A'.",
    "The window empties step by step while the main picture stays full.",
    [{"at": 0.0, "event": "window shows A and B"}, {"at": 0.12, "event": "readout 'A copy B'; only A in the window"}, {"at": 0.37, "event": "readout 'before A'; window empty"}],
    "ShaderLab with the preview code", "Two more positions of the same node, as the same window emptying, finish the idea without a second drawing.",
    "C06: capture_scenes.gd id C06 (three squares and window; BackBufferCopy starts between B and C, move_child to between A and B at 1.0 s and to first at 3.6 s); 10.5 s, 30 fps, Forward+, scripted.",
    "run-01 cases A4 and A5; run-11 C06", layout="video",
    readouts=[{"at": 0.12, "text": "A copy B", "x": 0.45, "y": 0.93}, {"at": 0.37, "text": "before A", "x": 0.45, "y": 0.93}])
lab("B14", 1, "only the first shader that reads the screen triggers a copy; a new node between them refreshes it", None, "reflections/two-readers.mp4", FW + " (a node is added at run time)",
    [],
    "The three squares with two windows on the right, one above the other. The first window sits between B and C in the tree, the second after C; with no copy node both windows miss C. At 10.5 s a BackBufferCopy is added between C and the second window: the second window now shows A, B and C, the first still does not. Readouts 'first reader', 'second reader', 'new copy'.",
    "The second window gains C the moment a copy node appears; the first window never does.",
    [{"at": 0.1, "event": "readout 'first reader' on the top window"}, {"at": 0.14, "event": "readout 'second reader' on the lower window; both miss C"}, {"at": 0.73, "event": "readout 'new copy'; the lower window gains C"}],
    "BrowserCapture of the Back-buffer logic paragraph", "Only a run shows the second window reusing the first copy and then changing at the exact moment a node appears.",
    "C07: capture_scenes.gd id C07 (tree A, B, preview 1 with border, C, preview 2 with border; BackBufferCopy added between C and preview 2 at 10.5 s); 15 s, 30 fps, Forward+, scripted. The lower window's miniature also shows the upper window (it is part of the screen by then): expected.",
    "run-01 and run-02 (case B5, B6: the second reader reuses the first copy); run-11 C07", layout="video",
    readouts=[{"at": 0.10, "text": "first reader", "x": 0.77, "y": 0.03}, {"at": 0.14, "text": "second reader", "x": 0.77, "y": 0.50}, {"at": 0.73, "text": "new copy", "x": 0.77, "y": 0.50}])
manim("B15", 1, "z index and canvas layers set the order too; a copy serves its own canvas layer", "CanvasSheets",
      "Three transparent sheets stacked in isometric view, labelled 'layer -1', 'layer 0', 'layer 1' (a small note 'a CanvasLayer node'). On layer -1 the map; on layer 0 the copy node, the art and the reflection (a window chip); on layer 1 a second window chip. A glowing arrow runs from the copy node to the reflection on its own sheet; an arrow toward the chip on layer 1 stops at the sheet edge with a cross. A side chip 'z index' reorders items inside one sheet.",
      "The copy's arrow reaches the reflection on its own sheet and the arrow to the other sheet stops at the edge.",
      [{"at": 0.12, "event": "three sheets with their contents"}, {"at": 0.4, "event": "z index chip reorders two items on layer 0"}, {"at": 0.72, "event": "arrow reaches the reflection; arrow to layer 1 is crossed"}],
      "LectureEvidenceTable (z index, layers, same layer)", "Sheets are a spatial idea and the blocked arrow is the claim; a table would only list it.",
      "run-08 cases Z1, Z2, Z3, Z5, Z6 (both renderers)")
rem("B16", 1, "Back Buffer Copy has three modes", "BrowserCapture",
    {"url": DOCS_BBC, "image": "reflections/docs-backbuffercopy.png", "caption": "Godot 4.7 documentation · BackBufferCopy · captured at build time", "frame": "browser",
     "moves": [{"at": 0, "x": 0.5, "y": 0.35, "scale": 1}, {"at": 0.2, "x": 0.5, "y": 0.62, "scale": 1.5, "ring": [0.12, 0.52, 0.88, 0.80]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 BackBufferCopy class page in a browser window; the camera pushes in on the three CopyMode constants (Disabled, Rect, Viewport) with their one-line descriptions and one terracotta ring marks the list. The ring box is a placeholder: set it from the real capture.",
    "The camera pushes in on the three modes the voice is naming.",
    [{"at": 0, "event": "the class page"}, {"at": 0.2, "event": "push-in + ring on the three copy-mode constants"}],
    "manim: three small boxes (whole screen, a box, nothing)", "The three modes are a documentation fact; the documentation itself is the evidence (SHOW-THE-THING).",
    "D1: Playwright capture of https://docs.godotengine.org/en/stable/classes/class_backbuffercopy.html#enumerations (1600x900 at 2.4x) at build time; read 2026-10-13: COPY_MODE_DISABLED, COPY_MODE_RECT, COPY_MODE_VIEWPORT")
lab("B17", 1, "rect mode copies only a box, and the default box is a corner", None, "reflections/rect-trap.mp4", "Godot 4.7.2 · Forward+ · fresh process · scripted",
    [],
    "The three squares and the window, with the node in Rect mode at its defaults: the window is black except a tiny stage-coloured patch at its top-left corner (the only part copied). At 9 s the mode is switched to Viewport and the window fills with A, B and C. Readouts 'Rect mode' then 'Viewport'; one terracotta ring on the tiny patch.",
    "A black window with a tiny patch fills with the three squares when the mode becomes Viewport.",
    [{"at": 0.12, "event": "readout 'Rect mode'; window black"}, {"at": 0.3, "event": "ring on the corner patch"}, {"at": 0.66, "event": "readout 'Viewport'; window shows A, B, C"}],
    "ShaderLab with the pond and the reflection", "The black window shows 'undefined' literally and keeps this act's cast; the pond version is verified too but shows only a missing reflection.",
    "C08: capture_scenes.gd id C08 (three squares and window; BackBufferCopy with copy_mode Rect at its default rect, node at (100,100); copy_mode set to Viewport at 9.0 s); 14.5 s planned, 30 fps, Forward+. MUST run in a fresh Godot process (the black needs an empty back buffer). 1:1 ROUTE, not the 4K route: a Rect box is measured in render pixels (run-13: on the 4K route the default box is only 34 canvas units), so capture_scene.sh renders C08 in the 1280 x 720 window itself, where the default box is the 100 px corner of the screen (run-10), and enlarges the frames 3x by whole pixels. The corner patch is 38 x 38 px in the window (0.578 to 0.608 of the frame's width, 0.078 to 0.131 of its height); the rect does not follow the node.",
    "run-03 (black, then stale pixels), run-10 (the copied region for eight node positions, 1:1), run-13 (the same on the 4K route: render pixels), run-11b C08", layout="video",
    readouts=[{"at": 0.12, "text": "Rect mode", "x": 0.575, "y": 0.52}, {"at": 0.66, "text": "Viewport", "x": 0.575, "y": 0.52}],
    rings=[{"at": 0.30, "box": [0.56, 0.05, 0.625, 0.16]}])
lab("B18", 1, "the setting in the editor: Copy Mode, Viewport", None, "reflections/editor-inspector-copy-mode.png", "Godot 4.7.2 editor · Inspector · real frame", [],
    "A real frame of Godot's Inspector with the BackBufferCopy node selected: the Copy Mode property reads Viewport. One terracotta ring settles on the Copy Mode row.",
    "The ring settles on the Copy Mode row.",
    [{"at": 0.0, "event": "Inspector frame"}, {"at": 0.3, "event": "ring on Copy Mode: Viewport"}],
    "GodotDevWorkbench inspector mode (labelled reconstruction)", "SHOW-THE-THING: the Inspector is where the viewer will change it, so the real Inspector is the evidence.",
    "E2: Godot's own editor on the scratch pond project, BackBufferCopy selected, recorded with record-editor-frames.sh and cropped to the box (2140, 60) to (2560, 420) of the 2560 x 1440 frame; the ring is measured on that crop. The planning frame png/planning-frame-E2-inspector-copy-mode.png already shows 'Copy Mode: Viewport' (label and value confirmed, and the options Disabled, Rect, Viewport are in the ClassDB list of run-07).",
    "run-07 case E6 (ClassDB property list); planning frame png/planning-frame-E2-inspector-copy-mode.png (film frame E2 to be re-recorded by the build)", layout="video", lane="editor",
    rings=[{"at": 0.30, "box": [0.03, 0.60, 0.97, 0.73]}])

# ───────────────────────────── ACT III · Building the Reflection ─────────────────────────────
lab("B19", 2, "the reflection: the character flipped, placed under its feet", None, "reflections/flip-and-place.mp4", FW,
    [],
    "Act title 'Building the Reflection' (serif 40) top-left. The real pond with the blob standing on the shoreline. At about 2 s a flipped copy of the blob fades in right under its feet (the copy has no shader yet); a terracotta ring marks where the feet meet the copy and a label 'Flip V' lands beside the copy.",
    "A flipped copy fades in directly under the feet.",
    [{"at": 0.0, "event": "blob on the shore, no copy"}, {"at": 0.18, "event": "the flipped copy fades in"}, {"at": 0.3, "event": "ring where feet meet the copy"}, {"at": 0.62, "event": "label 'Flip V'"}],
    "manim drawing of a blob and its mirror image", "The viewer sees the real node settings' result: the same picture, flipped and placed, exactly as the Inspector would produce it.",
    "C09: capture_scenes.gd id C09 (pond; Reflection is a plain flipped copy, no material, modulate alpha 0 to 1 over 2.0 to 3.0 s; Player static at x 520); 11 s, 30 fps, Forward+, scripted.",
    "run-11 C09 (copy invisible before 2 s, then 16,237 px under the feet)", layout="video", title="Building the Reflection",
    readouts=[{"at": 0.62, "text": "Flip V", "x": 0.405, "y": 0.80}], rings=[{"at": 0.30, "box": [0.33, 0.47, 0.48, 0.71]}],
    caption="Flip V: turns the picture upside down, top to bottom")
manim("B20", 2, "a Remote Transform 2D keeps the reflection in step", "FollowsAlong",
      "A small scene-tree diagram: 'Player' (teal blob icon) with a child chip 'RemoteTransform2D'; a separate branch 'Reflection' (a flipped blob icon); a dashed line from the chip to the Reflection node. Under the diagram, a strip of shoreline: the blob slides right along it and the flipped blob under it follows in lockstep while the dashed line pulses each time. A label from the docs: 'pushes its transform to another node'.",
      "The blob slides right and the flipped blob under it follows in lockstep, the dashed line pulsing.",
      [{"at": 0.1, "event": "tree diagram: Player, RemoteTransform2D, separate Reflection branch"}, {"at": 0.38, "event": "dashed line drawn from the chip to Reflection"}, {"at": 0.7, "event": "blob slides; the flipped blob follows"}],
      "GodotDevWorkbench tree mode (labelled reconstruction)", "The claim is 'follows without being its child'; two separate branches with a moving pair show exactly that.",
      "run-07 case E5 (reflection equals player plus offset every frame) and run-04 case C5 (90 frames, no lag)")
lab("B21", 2, "without the map the reflection hangs in the sand", None, "reflections/copy-in-the-sand.mp4", FW + " walk",
    [],
    "The real pond with the plain flipped copy following the blob along the shoreline: over the open water it looks right, but when the blob passes the sandbar the copy is drawn right over the sand. Readouts 'no map yet' then 'in the sand'; one terracotta ring on the copy over the sand.",
    "The copy slides over the sandbar and stays visible on the sand.",
    [{"at": 0.2, "event": "readout 'no map yet'; copy over water"}, {"at": 0.68, "event": "ring on the copy over the sand"}, {"at": 0.7, "event": "readout 'in the sand'"}],
    "manim drawing of the failure", "The failure is easiest to feel as the real mistake happening: a flipped copy sitting on dry sand.",
    "C10: capture_scenes.gd id C10 (pond; Reflection plain flipped sprite, no material; Player walks x 300 to 1000 over 10.5 s); 11.5 s, 30 fps, Forward+, scripted walk.",
    "run-11 C10 (copy fully visible at x 447 and x 779, over the sand)", layout="video",
    readouts=[{"at": 0.2, "text": "no map yet", "x": 0.50, "y": 0.90}, {"at": 0.7, "text": "in the sand", "x": 0.50, "y": 0.90}],
    rings=[{"at": 0.68, "box": [0.57, 0.47, 0.71, 0.70]}])
manim("B22", 2, "screen U V gives the same address in the copy", "SameAddress",
      "Two linked panels of the pond: left 'the screen' with a terracotta dot on one pixel of the reflection, right 'the copy' (the red and green map) with its twin dot at the same place; a dashed link between the dots and the tag 'screen UV: the same address in both'. The dot moves along the reflection and its twin moves with it; the colour under the twin changes the small label from 'water' to 'sand' as the dot crosses onto the sandbar. A label 'screen UV: a pixel's address on the whole screen'.",
      "The dot on the reflection moves and its twin on the map moves with it; the label under the twin turns from 'water' to 'sand'.",
      [{"at": 0.1, "event": "two panels, dot and twin"}, {"at": 0.4, "event": "dot moves; twin follows; label 'water'"}, {"at": 0.72, "event": "dot over the sandbar; label 'sand'"}],
      "ShaderLab with the preview window", "The same address in two pictures is a correspondence; two linked panels with moving twin dots show it.")
lab("B23", 2, "the reflection shader: look up the label, keep water, hide the rest", "02-reflection.gdshader", "reflections/reflection-walk.mp4", FW + " walk",
    [{"at": 0.10, "lines": [7], "label": "SCREEN_UV: a pixel's address on the whole screen"}, {"at": 0.30, "lines": [8], "label": "distance: how far apart two colors are"},
     {"at": 0.64, "lines": [9], "label": "alpha: how visible a pixel is: 0 invisible, 1 solid"}],
    "Code card at left (the ten-line reflection shader); at right the real pond with the shader on the reflection: the blob walks, the reflection shows over water and is gone over the sandbar. The lines light up as the voice reads: the lookup line, the water test, the alpha line. Readouts 'keep' over water and 'alpha zero' near the sandbar.",
    "The lookup, test and alpha lines light up in turn while the reflection shows over water and vanishes over the sand.",
    [{"at": 0.10, "event": "label lookup line"}, {"at": 0.30, "event": "water test line"}, {"at": 0.38, "event": "readout 'keep' over water"}, {"at": 0.64, "event": "COLOR.a line"}, {"at": 0.70, "event": "readout 'alpha zero' near the sandbar"}],
    "LectureCodeTrace alone", "The three lines are the whole effect; the real result next to them, and the lines lighting with the voice, is the claim.",
    "C11: capture_scenes.gd id C11 (pond; shader lab-shaders/02-reflection.gdshader; Player walks x 300 to 1000 over 11.5 s); 12.5 s, 30 fps, Forward+, scripted walk.",
    "run-04 (16,237 px over water, 0 over the sand, mismatch 0 in 90 frames); run-11 C11",
    readouts=[{"at": 0.38, "text": "keep", "x": 0.35, "y": 0.80}, {"at": 0.70, "text": "alpha zero", "x": 0.65, "y": 0.80}])
lab("B24", 2, "the proof that the map is hidden but used: switch the Label Map node off", None, "reflections/label-map-toggle.mp4", FW + " (the Label Map node is switched at run time)",
    [],
    "The real pond with the blob walking over open water. At 4.5 s the LabelMap node is switched off: the picture does not change except that the reflection disappears. At 9.5 s it is switched on again and the reflection returns. Readouts 'Map on', 'Map off', 'Map on'.",
    "The reflection vanishes and returns as the LabelMap node is switched off and on, and nothing else in the picture changes.",
    [{"at": 0.06, "event": "readout 'Map on'; reflection present"}, {"at": 0.37, "event": "readout 'Map off'; reflection gone, picture otherwise identical"}, {"at": 0.76, "event": "readout 'Map on'; reflection back"}],
    "manim drawing of two frames and what differs between them", "A real switch with an identical rest of the picture is the evidence; a drawing could only claim it.",
    "C12: capture_scenes.gd id C12 (pond; shader 02; Player walks x 180 to 620 over 12.5 s over open water; LabelMap.visible false from 4.5 s to 9.5 s); 13 s, 30 fps, Forward+, scripted.",
    "run-07 case E1 (hiding the label map changed 16,237 px, exactly the reflection's, and 0 outside it)", layout="video",
    readouts=[{"at": 0.06, "text": "Map on", "x": 0.12, "y": 0.06}, {"at": 0.37, "text": "Map off", "x": 0.12, "y": 0.06}, {"at": 0.76, "text": "Map on", "x": 0.12, "y": 0.06}])
lab("B25", 2, "wrong orders: copy after the art, map over the art", None, "reflections/wrong-orders.mp4", FW + " (the order is changed in the tree at run time)",
    [],
    "The real pond. State one: map, copy, art (the reflection shows). At 4 s the copy node is moved after the art: the reflection disappears and nothing else changes. At 9.5 s the LabelMap is moved over the art: a red and green sea covers the pond and the reflection is back. Readouts show the order ('map · copy · art', 'map · art · copy', 'art · map · copy') and the outcome ('reflection', 'no reflection', 'red sea').",
    "The reflection disappears when the copy moves after the art; a red sea covers the pond when the map moves over it.",
    [{"at": 0.06, "event": "order map, copy, art; reflection shows"}, {"at": 0.33, "event": "order map, art, copy; no reflection"}, {"at": 0.72, "event": "order art, map, copy; red sea, reflection back"}],
    "manim stack with the copy frame moving", "Two real failures, one after the other in one scene, show what each wrong order looks like to the person debugging it.",
    "C13: capture_scenes.gd id C13 (pond; shader 02; Player walks x 300 to 560; move_child(BackBufferCopy, Ground's index) at 4.0 s; move_child(LabelMap, Ground's index) at 9.5 s); 13.5 s, 30 fps, Forward+, scripted.",
    "run-04 cases C2a, C2b, C2c; run-11 and run-11b C13", layout="video",
    readouts=[{"at": 0.06, "text": "map · copy · art", "x": 0.15, "y": 0.06}, {"at": 0.33, "text": "map · art · copy", "x": 0.15, "y": 0.06}, {"at": 0.72, "text": "art · map · copy", "x": 0.15, "y": 0.06},
              {"at": 0.06, "text": "reflection", "x": 0.40, "y": 0.80}, {"at": 0.34, "text": "no reflection", "x": 0.40, "y": 0.80}, {"at": 0.72, "text": "red sea", "x": 0.40, "y": 0.80}])
lab("B26", 2, "the art must be opaque or the map leaks", None, "reflections/see-through-art.mp4", FW + " (the art's opacity is changed at run time)",
    [],
    "The real pond. At 3 s the art layer's opacity eases from 100 to 90 percent: the water turns a faint periwinkle and a pale green ring shows around the sandbar, the map leaking through. At 9.5 s it returns to 100 percent and the leak is gone. Readouts 'art 100%', 'art 90%', 'art 100%'; a terracotta ring on the leaking green ring while it shows.",
    "A faint purple tint and a green ring appear when the art drops to ninety percent and disappear when it returns to full.",
    [{"at": 0.06, "event": "readout 'art 100%'"}, {"at": 0.3, "event": "readout 'art 90%'; the leak appears"}, {"at": 0.62, "event": "ring on the leaking green ring"}, {"at": 0.76, "event": "readout 'art 100%'; the leak is gone"}],
    "manim drawing of an overlay with alpha", "The leak is a visible change in a real frame, with the exact opacity labelled; the viewer sees how little transparency is enough.",
    "C14: capture_scenes.gd id C14 (pond; shader 02; Ground modulate alpha 1.0, eased to 0.9 over 3.0 to 4.0 s, back to 1.0 at 9.5 s); 13 s, 30 fps, Forward+, scripted. The stage colour shows through the art at 0.9, so the whole picture lightens a little: expected.",
    "run-07 case E4 (largest channel change 0.086 at 90 percent; 0.169 at 80 percent); run-11 C14", layout="video",
    readouts=[{"at": 0.06, "text": "art 100%", "x": 0.12, "y": 0.06}, {"at": 0.30, "text": "art 90%", "x": 0.12, "y": 0.06}, {"at": 0.76, "text": "art 100%", "x": 0.12, "y": 0.06}],
    rings=[{"at": 0.62, "box": [0.49, 0.47, 0.89, 0.84]}])

# ───────────────────────────── ACT IV · Compare With a Range ─────────────────────────────
rem("B27", 3, "the docs warn against comparing decimals with equals", "BrowserCapture",
    {"url": DOCS_COMPARE, "image": "reflections/docs-shading-language-compare.png",
     "caption": "Godot 4.7 documentation · Shading language · captured at build time", "frame": "browser",
     "moves": [{"at": 0, "x": 0.5, "y": 0.35, "scale": 1}, {"at": 0.25, "x": 0.5, "y": 0.5, "scale": 1.6, "ring": [0.10, 0.40, 0.92, 0.60]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "Title 'Compare With a Range' (serif 40) on the real Godot 4.7 shading-language page, scrolled to the Flow control paragraph that says to compare floating-point values against a range instead of an exact number; the camera pushes in and one terracotta ring marks the sentence. The ring box is a placeholder: set it from the real capture.",
    "The camera pushes in on the warning the voice is describing.",
    [{"at": 0, "event": "the page at the Flow control section"}, {"at": 0.25, "event": "push-in + ring on the warning sentence"}],
    "manim: 'a == b' with a cross over it", "The warning is a documentation claim; the documentation itself, in its own words, is the evidence (SHOW-THE-THING).",
    "D2: Playwright capture of https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#flow-control (1600x900 at 2.4x) at build time; read 2026-10-13: 'when comparing floating-point values against a number, make sure to compare them against a range instead of an exact number'")
lab("B28", 3, "equals fails on a map painted at half strength", "04-compare-equal.gdshader", "reflections/equals-half-red.mp4", FW + " walk · water painted at 128",
    [{"at": 0.60, "lines": [7], "label": "==: true only when every part matches exactly"}],
    "Title 'Compare With a Range'. Code card at left (the nine-line equals shader, the compare line lit as the voice says 'exactly point five'); at right the real pond whose water was painted at half strength: the blob walks and no reflection ever appears. Readouts 'water: half red' at the top and 'no reflection' below the blob.",
    "The blob walks and the reflection never appears while the equals line is lit.",
    [{"at": 0.14, "event": "readout 'water: half red'"}, {"at": 0.60, "event": "compare line lit"}, {"at": 0.78, "event": "readout 'no reflection'"}],
    "LectureCodeTrace alone", "A non-event needs the code that causes it and a held, walking frame with a label that says what is missing.",
    "C15: capture_scenes.gd id C15 (pond with the water painted (128,0,0); shader lab-shaders/04-compare-equal.gdshader; Player walks x 250 to 700 over 10.5 s); 12 s, 30 fps, Forward+, scripted walk.",
    "run-06 case D2a (0 of 16,237 px visible, both renderers); run-11 C15",
    readouts=[{"at": 0.14, "text": "water: half red", "x": 0.50, "y": 0.06}, {"at": 0.78, "text": "no reflection", "x": 0.30, "y": 0.80}], caption="equals · the map's water is painted at 128 of 255")
lab("B29", 3, "a distance finds the same half-red water", "05-compare-distance.gdshader", "reflections/distance-half-red.mp4", FW + " walk · water painted at 128",
    [{"at": 0.22, "lines": [7], "label": "distance: how far apart two colors are"}],
    "Code card at left (the same nine lines with a distance test, the changed line lit); at right the same half-strength pond: the reflection is there as the blob walks. Readouts 'water: half red' and 'reflection back'.",
    "The reflection shows as the blob walks while the distance line is lit.",
    [{"at": 0.12, "event": "readout 'water: half red'"}, {"at": 0.22, "event": "distance line lit"}, {"at": 0.62, "event": "readout 'reflection back'"}],
    "LectureCodeTrace alone", "The same pond and the same walk with one line changed is the fair comparison; the contrast with the previous beat is the proof.",
    "C16: capture_scenes.gd id C16 (the same half-red pond; shader lab-shaders/05-compare-distance.gdshader; Player walks x 250 to 700 over 10 s); 10.5 s, 30 fps, Forward+, scripted walk.",
    "run-06 case D2b (16,237 of 16,237 px visible, both renderers); run-11 C16",
    readouts=[{"at": 0.12, "text": "water: half red", "x": 0.50, "y": 0.06}, {"at": 0.62, "text": "reflection back", "x": 0.30, "y": 0.80}], caption="distance within 0.1 · the map's water is painted at 128 of 255")
manim("B30", 3, "eight bits: half is stored as step 128 and reads 0.502", "EightBits",
      "The series' 0 to 1 ramp strip zoomed around 0.5 so tick marks are visible at k/255, with the ticks 127 and 128 labelled 0.498 and 0.502. A terracotta marker 'asked for 0.5' sits between the two ticks, on no tick. The painted value snaps to the 128 tick and a readout shows '0.502'. A small label '256 steps per channel' and a grey credit 'Apple M4 Pro · Godot 4.7.2 · Forward+ and Compatibility read the same'.",
      "The marker lands between two ticks while the painted value snaps to the 128 tick and reads 0.502.",
      [{"at": 0.12, "event": "zoomed ramp with ticks"}, {"at": 0.4, "event": "marker 'asked for 0.5' lands between two ticks"}, {"at": 0.72, "event": "painted value snaps to tick 128; readout 0.502"}],
      "LectureEvidenceTable", "'Not one of the steps' is spatial; a marker sitting in the gap between two ticks shows it at a glance.",
      "run-06 cases D3c and D3a (painted 128 reads 0.502; pure 255 reads 1.0)")
rem("B31", 3, "equals against 128 over 255: one renderer passes, the other fails", "LectureEvidenceTable",
    {"title": "Writing 128 over 255", "headers": ["Renderer", "equals 128/255", "distance < 0.1"],
     "rows": [["Forward+", "match", "match"], ["Compatibility", "no match", "match"]],
     "note": "Apple M4 Pro · Godot 4.7.2 · water painted at 128 · evidence/planning-checks (run-06)", "cues": [0.2, 0.62], "durationSeconds": "__AUDIO__"},
    "A two-row table, one row ringed as each renderer is named.", "The ring moves down the rows with the voice.",
    [{"at": 0.2, "event": "Forward+ row"}, {"at": 0.62, "event": "Compatibility row"}],
    "manim", "Two measured results in two rows with the machine and renderer stated is exactly what the table component is for.", "run-06 cases D2d and D2b, in both renderer logs")
manim("B32", 3, "a color is a point: a radius of a tenth around red and around green", "ColorDistance",
      "A square colour plane (red channel across, green channel up) with the red point at the bottom right and the green point at the top left, each with a terracotta circle of radius 0.1 (labelled 'water' and 'coast'). A small dot, the pixel's colour, slides from red toward green: inside the red circle the label reads 'water', outside both 'neither', inside the green circle 'coast'. A tiny ruler shows the radius 0.1 and the distance between red and green, about 1.4.",
      "The dot slides from red toward green and the label changes as it enters and leaves the two circles.",
      [{"at": 0.12, "event": "plane with the two points and circles"}, {"at": 0.4, "event": "dot leaves the water circle: 'neither'"}, {"at": 0.74, "event": "dot enters the coast circle: 'coast'"}],
      "LectureEvidenceTable", "A tolerance is a region; a dot moving through two circles shows what 'close enough' means.")
rem("B33", 3, "pure values read back the same everywhere; half values do not", "LectureEvidenceTable",
    {"title": "What the screen texture reads back", "headers": ["Painted", "Default 2D", "HDR 2D on (Forward+)"],
     "rows": [["full · 255", "1.0", "1.0"], ["half · 128", "0.502", "0.216"]],
     "note": "Both renderers read the Default column the same · Apple M4 Pro · Godot 4.7.2 · evidence/planning-checks (run-06)", "cues": [0.2, 0.62], "durationSeconds": "__AUDIO__"},
    "A two-row table, one row ringed as each painted value is named.", "The ring moves from the full row to the half row with the voice.",
    [{"at": 0.2, "event": "full row"}, {"at": 0.62, "event": "half row"}],
    "manim ramp strip", "Four measured numbers in a table with the machine named; the ramp picture was used in the previous eight-bit beat.", "run-06 cases D3a, D3b, D3c in both renderer logs")

# ───────────────────────────── ACT V · Polish and Limits ─────────────────────────────
lab("B34", 4, "the coast: a lower alpha, added to the water's", "03-reflection-final.gdshader", "reflections/coast-alpha.mp4", FW + " walk · tint neutral",
    [{"at": 0.12, "lines": [6], "label": "COAST: the coast's label, pure green"}, {"at": 0.30, "lines": [11]}, {"at": 0.58, "lines": [12]}],
    "Title 'Polish and Limits' (serif 40). Code card at left (the fourteen-line final shader; the coast constant, the coast test and the alpha sum lit in turn); at right the real pond: the reflection stands in open water at half strength, then the blob walks toward the sandbar and the reflection grows fainter across the green ring before the sand hides it. Readouts 'open water' and 'coast'.",
    "The reflection is stronger in open water and fainter as it crosses the ring around the sandbar.",
    [{"at": 0.12, "event": "coast constant lit"}, {"at": 0.30, "event": "coast test lit"}, {"at": 0.58, "event": "alpha sum lit"}, {"at": 0.62, "event": "readout 'open water'"}, {"at": 0.78, "event": "readout 'coast'; reflection fainter over the ring"}],
    "LectureCodeTrace alone", "The faint-over-the-ring crossing is the claim and only a real moving frame shows the two strengths side by side.",
    "C17: capture_scenes.gd id C17 (pond; shader lab-shaders/03-reflection-final.gdshader with the tint uniform set to the sprite's own colour so only the alpha shows; Player static at x 420 until 7.0 s, then walks to x 900 by 12.5 s); 13 s, 30 fps, Forward+, scripted.",
    "run-06 cases D1a and D1c (alpha 0.5 over water, 0.3 on the coast, both renderers); run-11 C17", title="Polish and Limits",
    readouts=[{"at": 0.62, "text": "open water", "x": 0.33, "y": 0.80}, {"at": 0.78, "text": "coast", "x": 0.55, "y": 0.88}])
lab("B35", 4, "the tint: mix halfway toward blue", "03-reflection-final.gdshader", "reflections/tint-toggle.mp4", FW + " (the tint is switched at run time)",
    [{"at": 0.22, "lines": [13], "label": "mix: blends from a to b: t of 0 gives a, 1 gives b"},
     {"at": 0.62, "lines": [4], "label": "uniform: a value your game sets; same for every pixel"}],
    "Code card at left (the same fourteen lines; the mix line lit, then the tint uniform); at right the real pond with the blob standing still: the reflection is teal-grey, then turns a clearer blue as the tint is switched on, off, and on again. Readouts 'no tint' and 'tint'.",
    "The reflection's color shifts toward blue each time the tint is switched on.",
    [{"at": 0.03, "event": "readout 'no tint'"}, {"at": 0.20, "event": "readout 'tint'; reflection bluer"}, {"at": 0.22, "event": "mix line lit"}, {"at": 0.34, "event": "readout 'no tint'"}, {"at": 0.44, "event": "readout 'tint'"}, {"at": 0.62, "event": "tint uniform lit"}],
    "LectureCodeTrace alone", "A hue shift is only visible in a flicker between states; the real frames alternate with the line that causes it lit.",
    "C18: capture_scenes.gd id C18 (pond; shader 03; Player static at x 420; the tint uniform set to the sprite colour (no effect) or to (0.2, 0.5, 1.0): blue from 1.8 s to 3.2 s and from 4.6 s on); 10.5 s, 30 fps, Forward+, scripted.",
    "run-06 case D1b (the default tint is mixed raw, no color conversion: measured (0.373, 0.6, 0.78) against (0.416, 0.631, 0.671)); run-11 C18",
    readouts=[{"at": 0.03, "text": "no tint", "x": 0.30, "y": 0.80}, {"at": 0.20, "text": "tint", "x": 0.30, "y": 0.80}, {"at": 0.34, "text": "no tint", "x": 0.30, "y": 0.80}, {"at": 0.44, "text": "tint", "x": 0.30, "y": 0.80}],
    )
manim("B36", 4, "limit: the character only; the sky and shore are not reflected", "NoScenery",
      "The pond picture with a waterline drawn across it: sky, grass and the blob above; below it the reflection area. Under the line a flipped teal blob stays; dashed flipped outlines of the sky band and the grass band try to appear under the line and are each crossed out. A small label 'the character only'.",
      "Dashed flipped outlines of the sky and the grass appear under the waterline and are crossed out; only the flipped blob stays.",
      [{"at": 0.1, "event": "pond picture with waterline and the flipped blob"}, {"at": 0.4, "event": "dashed flipped sky and grass appear"}, {"at": 0.7, "event": "each is crossed out; label settles"}],
      "ShaderLab capture of the mirror-the-screen technique", "A limit is a negative and a drawing that crosses out what is missing says it; a capture would show only what is there.",
      "run-09 (a flipped read of the screen texture mirrors the scenery and the character: the other technique exists and works)")
lab("B37", 4, "limit: a jump lifts the reflection too, and the shoreline cuts it off", "03-reflection-final.gdshader", "reflections/jump.mp4", FW + " (scripted jump)",
    [],
    "The real pond with the blob standing at the shore. It jumps 80 px up, twice. Each time the reflection also moves up (where a real one would move down) and the top part of it is cut off at the shoreline. Readouts 'jump' and a terracotta ring on the cut part.",
    "The blob jumps up and the reflection rises with it and is cut off at the shoreline.",
    [{"at": 0.3, "event": "first jump: reflection rises and is clipped"}, {"at": 0.34, "event": "ring on the cut part"}, {"at": 0.64, "event": "second jump"}],
    "manim drawing of a mirror image dropping", "The honest picture of the limit is the real effect misbehaving; a drawing could only say a real one would drop.",
    "C19: capture_scenes.gd id C19 (pond; shader 03; Player static at x 300; Player.y lifted 80 px by a half sine over 3.0 to 4.0 s and again over 6.5 to 7.5 s); 10.5 s, 30 fps, Forward+, scripted.",
    "run-07 case E3 (reflection moved by -80 px with the player; visible pixels 6,903 of 16,237); run-11 C19", layout="video",
    readouts=[{"at": 0.3, "text": "jump", "x": 0.50, "y": 0.12}],
    rings=[{"at": 0.34, "box": [0.17, 0.46, 0.30, 0.60]}, {"at": 0.66, "box": [0.17, 0.46, 0.30, 0.60]}])

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
sl = ["# Shot list: Reflections\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a capture of a scene in `evidence/planning-checks/capture_scenes.gd` (nineteen scripted scenes, each checked by `scene_runner.gd`) or a real editor frame of a scratch project; every shader shown is a tested file in `lab-shaders/`. Seven things must be built or recorded first (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`). 2. **`shader_kit.py`** Manim helpers (same file), **plus the objects this film adds**: the pond picture (flat shapes), the slab stack with a thumbnail and a copy frame, node chips, isometric sheets, a ramp strip zoomed to ticks, a colour plane with two circles. 3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` (same file); it must load `evidence/planning-checks/capture_scenes.gd` (contract at the top of that file; `scene_runner.gd` is the checked stand-in). Every capture in a FRESH Godot process. 4. **Editor frames E1 and E2** from the scratch pond project (`make-editor-project.sh`). 5. **Docs screenshots D1 and D2** via Playwright. 6. `BrowserCapture`, `LectureEvidenceTable`, `LectureCodeTrace` exist and are registered. 7. The five tested shader files in `lab-shaders/`.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
