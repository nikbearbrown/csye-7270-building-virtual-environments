#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text, the cue times must follow the narration (they are computed from where a
phrase starts in the beat's words, then nudged out of the 45 to 55 % window), and the shot list must say exactly what the lanes say.
Re-run after any edit:  python3 _gen_lanes.py && python3 make_sheet.py
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_godot-shaders-series"))
spec = importlib.util.spec_from_file_location("narration", HERE / "narration.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
SH = HERE / "lab-shaders"
TEXT = {bid: t for bid, _, t in N.BODY}
E = []          # entries in beat order
NOTES = []      # cue computations, printed at the end


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def nl(fn):
    return len(code_of(fn).splitlines())


def at(bid, phrase, nudge=True):
    """Fraction of the beat (by words) at which `phrase` starts, kept out of the 45 to 55 % window."""
    words = TEXT[bid].split()
    target = phrase.split()
    for i in range(len(words) - len(target) + 1):
        if [re.sub(r"[^\w']", "", w).lower() for w in words[i:i + len(target)]] == [re.sub(r"[^\w']", "", w).lower() for w in target]:
            f = i / len(words)
            g = f
            if nudge and 0.45 <= f <= 0.55:
                g = 0.43 if f < 0.5 else 0.57
            g = round(min(max(g, 0.02), 0.96), 2)
            NOTES.append(f"{bid} '{phrase}' -> {f:.2f}" + (f" (nudged to {g})" if g != round(f, 2) else ""))
            return g
    raise SystemExit(f"phrase not found in {bid}: {phrase!r}")


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects)"):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, title=None, code=None, code_file=None, lane="capture", caption=""):
    props = {"layout": layout, "code": code if code is not None else (code_of(shader) if shader else ""),
             "codeFile": code_file or (f"lab-shaders/{shader}" if shader else ""), "cues": cues,
             "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption,
             "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    add(bid, act, about, {"lane": lane, "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": intent,
                          "motion_claim": motion, "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


def rem(bid, act, about, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, act, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


LABEL = "Godot 4.7.2 · Forward+ · scripted"
GAME_SCRIPT = ('func _process(_delta):\n\tvar size := get_viewport_rect().size\n'
               '\tvar on_screen: Vector2 = $Player.get_global_transform_with_canvas().origin\n'
               '\t$Layer/Filter.material.set_shader_parameter("player", on_screen / size)')

# ───────────────────────────── ACT I · A Copy of the Screen ─────────────────────────────
lab("B01", 0, "the finished pool: a shader reading what is behind it", "12-pool.gdshader", "reading-the-screen/pool.mp4",
    "Godot 4.7.2 · Forward+ · live", [],
    "Act title 'A Copy of the Screen' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a meadow of green checker tiles, a sand path, flowers, and in the lower left a pool whose wavy top edge ripples and whose water bends the checker lines and the path behind it. The teal player stands to the right. A terracotta ring settles on the pool.",
    "The water ripples and the checker lines behind it wobble, live; the ring marks where the picture behind is being read.",
    [{"at": 0.0, "event": "meadow with the live pool; act title top-left"}, {"at": 0.44, "event": "terracotta ring settles on the pool"}, {"at": 0.66, "event": "label 'reads the screen'"}],
    "manim drawing of a glass pane over a scene", "The finished effect running is the question the film answers; a drawing would only claim it.",
    "C01: scene_c01_pool.gd (evidence/planning-checks), canvas 1280 x 720 through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Nothing moves but the water (TIME). Same capture serves B28.",
    "Scene C01; shader 12-pool compiled in the Lab and in the scene runner", layout="video", title=N.ACTS[0][1],
    readouts=[{"at": 0.66, "text": "reads the screen", "x": 0.26, "y": 0.47}], rings=[{"at": 0.44, "box": [0.05, 0.52, 0.47, 0.93]}])
manim("B02", 0, "why a copy exists, and what it is", "TheCopy",
      "On the cream stage a 16:9 screen frame, left, fills in the order the game draws it: the green checker ground, a tree, a flower, then a small rectangle labelled 'shader'. Just before that rectangle is drawn, a camera-flash snapshot copies the whole frame into a second frame on the right, labelled 'screen texture: a copy of everything drawn so far'. A drawn arrow runs from the shader rectangle to the copy.",
      "The frame is copied in one flash and the shader's arrow reads from the copy, not from the live frame.",
      [{"at": 0.10, "event": "screen frame; ground, tree, flower drawn in order"}, {"at": 0.34, "event": "flash: the frame is copied to the right"},
       {"at": 0.46, "event": "settled: two frames, label 'screen texture'"}, {"at": 0.66, "event": "arrow from the shader rectangle to the copy"}],
      "DesignPipelineClaim, show-tell isometric", "A snapshot being taken is a motion, and the arrow into the copy is the claim; an isometric flow would show boxes, not a copy of a picture.")
lab("B03", 0, "the smallest reader: a rectangle that shows only what is behind it", "01-window.gdshader", "reading-the-screen/window.mp4",
    "Godot 4.7.2 · Forward+ · shader switched on mid-clip (58 percent)",
    [{"at": at("B03", "In the fragment function"), "lines": [5], "label": "fragment(): runs once for each pixel"}, {"at": at("B03", "each pixel's color"), "lines": [6]}],
    "Code card at left with the @NL(01-window.gdshader)@-line shader; at right a real Godot window on the meadow: a plain teal rectangle in a cream frame. At 58 percent the shader switches on and the teal fill vanishes, leaving the cream frame around meadow. Label: 'still there'.",
    "The teal rectangle vanishes at the cue; the cream frame stays, empty, showing the meadow.",
    [{"at": 0.14, "event": "COLOR line highlighted"}, {"at": 0.58, "event": "the shader switches on; the teal fill vanishes"}, {"at": 0.72, "event": "label 'still there'"}],
    "LectureCodeTrace alone", "Code and its result side by side, with the vanishing as the proof; code alone cannot show that the rectangle is still there.",
    "C02: scene_c02_window.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. A teal rectangle (0.38, 0.22, 0.30 x 0.30 of the canvas) in a cream frame; 01-window is assigned at u = 0.58. Verified: the rectangle's interior equals the meadow exactly (8,820 samples, worst channel difference 0).",
    "verify1 A and B (window vanishes, exact); Lab probe 01-window",
    readouts=[{"at": 0.72, "text": "still there", "x": 0.53, "y": 0.15}])
manim("B04", 0, "the declaration, piece by piece", "ThePieces",
      "The line `uniform sampler2D screen_texture : hint_screen_texture;` set in monospace on the cream stage, each token its own object at explicit coordinates. A bracket is drawn under `uniform` with the label 'from outside'; one under `sampler2D` with 'sampler2D: the type of a texture a shader reads'; one under `screen_texture` with 'your name'. The `hint_screen_texture` token stays grey until the next beat.",
      "Each bracket is drawn under its token on the word that names it, so the line is read left to right.",
      [{"at": 0.14, "event": "line typed; bracket under uniform"}, {"at": 0.40, "event": "bracket under sampler2D"}, {"at": 0.46, "event": "settled: two brackets and labels"}, {"at": 0.78, "event": "bracket under the name"}],
      "ShaderLab", "The pieces of one line need brackets under tokens; ShaderLab highlights whole lines only.")
manim("B05", 0, "the hint fills the uniform, every frame", "FilledEveryFrame",
      "The same line again with the `hint_screen_texture` token ringed (terracotta ring, grey backing) and the labels 'hint: the word after a colon that tells Godot how to treat a uniform' and 'this one: fill it with the screen'. Below, a slot labelled `screen_texture`. On three frame ticks (a small counter 1, 2, 3) a fresh miniature of the meadow drops into the slot, replacing the last one; in each the flower has moved a little. A small cursor arrow outside the slot is crossed out: 'you never set it'.",
      "A new copy drops into the slot on every tick, replacing the old one, with nobody placing it.",
      [{"at": 0.14, "event": "hint token ringed; label"}, {"at": 0.40, "event": "first copy drops into the slot"}, {"at": 0.46, "event": "settled: copy in the slot"}, {"at": 0.66, "event": "second copy replaces it"}, {"at": 0.82, "event": "third copy; crossed-out cursor"}],
      "DesignPipelineClaim, show-tell isometric", "Replacement on every tick is the claim 'Godot refreshes it every frame'; a static diagram could not show that the copy changes.")
manim("B06", 0, "texture(): an address in, a color out", "AddressToColor",
      "The screen texture drawn as a 12 by 7 grid of outline cells in the meadow colours (cells are never filled behind text). A terracotta probe ring sits on one cell with a live label 'address (0.62, 0.40)'; a drawn arrow runs to a swatch showing that cell's colour. The probe hops to two more cells and the swatch follows. After the third hop the swatch splits into four chips R, G, B, A; the A chip carries 'alpha: how visible a pixel is (0 invisible, 1 solid)'.",
      "The probe hops from cell to cell and the swatch changes colour to match; then the swatch splits into four numbers.",
      [{"at": 0.12, "event": "grid of the copy"}, {"at": 0.30, "event": "probe and swatch; first address"}, {"at": 0.46, "event": "settled: probe, label, swatch"}, {"at": 0.62, "event": "swatch splits into R, G, B, A"}],
      "LectureCodeTrace", "An address going in and a color coming out is a lookup, and a lookup is a probe on a grid; code would only name it.")
manim("B07", 0, "two addresses for one pixel", "TwoAddresses",
      "A 16:9 screen outline with a smaller 4:3 shape inside it and one pixel dot on the shape. Two live labels follow the dot: 'UV (0.5, 0.5)', measured on the shape ('UV: a point's address on the shape'), and 'screen UV (0.31, 0.62)', measured on the screen ('SCREEN_UV: a pixel's address on the whole screen, not on its own shape'). The shape then slides right: the first label stays (0.5, 0.5) while the second counts up to (0.62, 0.62).",
      "The shape slides and one label never changes while the other counts up.",
      [{"at": 0.12, "event": "screen outline, shape, pixel dot"}, {"at": 0.20, "event": "label 'UV' on the shape"}, {"at": 0.40, "event": "label 'screen UV' on the screen"}, {"at": 0.46, "event": "settled: both labels"}, {"at": 0.68, "event": "the shape slides; screen UV counts up"}],
      "ShaderLab with the two colour pictures", "Two numbers changing at different rates is exactly a pair of live labels; the real render comes in the next beat.")
lab("B08", 0, "UV against screen UV: a tiny copy, and a window", None, "reading-the-screen/addresses.mp4", "Godot 4.7.2 · Forward+ · scripted slide", [],
    "Two 16:9 rectangles in cream frames, one above the other, slide right together over the meadow. The top one (UV) holds a tiny copy of the whole screen that does not move with the picture; the bottom one (screen UV) is a window onto the meadow. Right-margin labels 'UV' and 'screen UV'.",
    "Both rectangles slide; the top one keeps showing the same tiny copy, the bottom one shows different parts of the meadow.",
    [{"at": 0.08, "event": "label 'UV' by the top rectangle"}, {"at": 0.43, "event": "label 'screen UV' by the bottom rectangle"}, {"at": 0.80, "event": "both rectangles near the right"}],
    "manim drawing of the two cases", "The consequence of the wrong address is a tiny copy of the screen inside a rectangle, and that is only convincing as a real render.",
    "C03: scene_c03_addresses.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Top rectangle 02-miniature, bottom 01-window, both 0.28 x 0.28, sliding from x = 0.04 to 0.56 between u = 0.15 and 0.90. Verified: inside the miniature the colour at a fraction of the rectangle equals the screen at the same fraction (4 of 4 points); inside the window it equals the screen at the same place.",
    "verify1 C and C2", layout="video",
    readouts=[{"at": 0.08, "text": "UV", "x": 0.94, "y": 0.21}, {"at": 0.43, "text": "screen UV", "x": 0.93, "y": 0.74}])
lab("B09", 0, "flip the colors; the flipped picture stays pinned to the screen", "03-invert.gdshader", "reading-the-screen/invert.mp4",
    "Godot 4.7.2 · Forward+ · scripted slide",
    [{"at": at("B09", "Adding r g b"), "lines": [6], "label": ".rgb: picks red, green and blue (a swizzle)"}, {"at": at("B09", "One minus each of them"), "lines": [7]}],
    "Code card at left (the @NL(03-invert.gdshader)@-line invert shader); at right a real Godot window: one 16:9 window in a cream frame holds the meadow with every colour flipped (greens turn purple, the sand path turns navy). It sits still, then slides diagonally across the meadow; the flipped picture inside stays pinned to the screen while the opening moves. Label 'pinned to screen'.",
    "The window slides and the flipped picture inside does not slide with it; only the opening moves.",
    [{"at": 0.02, "event": "behind line highlighted"}, {"at": 0.30, "event": "1.0 - behind highlighted"}, {"at": 0.56, "event": "window starts to slide"}, {"at": 0.78, "event": "label 'pinned to screen'"}],
    "manim sliding frame over a picture", "The sliding window over a fixed picture is the claim, shown on the real result next to the one line that flips it.",
    "C04: scene_c04_invert.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. 03-invert in a 0.28 x 0.28 window that is still until u = 0.56, then slides from (0.08, 0.10) to (0.62, 0.58) by u = 0.96. Verified: every sampled pixel equals 1 minus the meadow (worst channel difference 0).",
    "verify1 D (invert is exact)", readouts=[{"at": 0.78, "text": "pinned to screen", "x": 0.5, "y": 0.94}])
rem("B10", 0, "the Godot 3 shortcut, and the real error", "LectureCodeTrace",
    {"title": "A line from older tutorials", "code": code_of("04-godot3-screen-texture.gdshader"),
     "note": "Godot 4.7.2 compiler: SCREEN_TEXTURE has been removed in favor of using hint_screen_texture with a uniform.",
     "cues": [0.02, 0.02, 0.04, 0.10, 0.10], "durationSeconds": "__AUDIO__"},
    "A cream code card with the five-line shader that uses the capital-letters shortcut; focus lands on the line that uses it. Under the card the engine's own message, verbatim from a real run, is the note.",
    "Focus steps down to the old line and stays on it while the compiler's message is read.",
    [{"at": 0.04, "event": "focus on the shader's first lines"}, {"at": 0.10, "event": "focus on the old line"}, {"at": 0.50, "event": "settled: old line and the compiler's message"}],
    "BrowserCapture of the docs row 'SCREEN_TEXTURE: Removed in Godot 4'", "The real message from a real run is the thing a viewer will actually see; the docs row says the same but is not what appears when it fails.",
    "04-godot3-screen-texture.gdshader run in the Lab and in a scratch project: the same message, verbatim")

# ───────────────────────────── ACT II · Full-Screen Effects ─────────────────────────────
manim("B11", 1, "a color rect with Full Rect covers the whole window", "FullRect",
      "Act title 'Full-Screen Effects' (serif 40) top-left. A screen outline (the game screen) with a small teal rectangle labelled 'ColorRect' inside it. Four terracotta anchor dots on the rectangle's corners fly out to the screen's four corners and the rectangle stretches to fill it; the label 'Layout > Anchors Preset: Full Rect' (the editor's own words) appears. The screen outline then grows wider and narrower in turn and the rectangle follows.",
      "Four dots fly to the four corners, the rectangle fills the screen, and it keeps filling it when the screen is resized.",
      [{"at": 0.12, "event": "screen outline, small rectangle; act title"}, {"at": 0.34, "event": "corner dots fly out; rectangle fills the screen"}, {"at": 0.46, "event": "settled: filled screen, label 'Full Rect'"}, {"at": 0.72, "event": "screen resizes; rectangle follows"}],
      "an editor capture of the Layout menu (E1, optional)", "Corners snapping to corners is a motion, and the follow-on resize is the point of anchors; the editor frame is an optional upgrade, recorded in CAPTURE-PLAN.",
      "verify3 K5 and K5b: set_anchors_and_offsets_preset gives the viewport's size and follows a resize")
manim("B12", 1, "a canvas layer is drawn after the game", "LayerStack",
      "Two panes in an exploded side view: the lower pane 'game · 0' with a tiny meadow and player; the upper pane 'canvas layer 1' holding the full-rect colour rect, tinted pale grey, with the definition 'canvas layer: a group drawn together, with a number; higher is drawn later'. The lower pane slides in first, then the upper one is drawn on top of it with its number. A drawn arrow runs from the upper pane down through the lower: 'reads everything below'.",
      "The panes arrive in order, zero then one, and the arrow shows the upper layer reading everything beneath it.",
      [{"at": 0.12, "event": "color rect inside a layer pane"}, {"at": 0.34, "event": "layer pane with its number"}, {"at": 0.46, "event": "settled: layer 1 pane"}, {"at": 0.58, "event": "game pane below it, number 0"}, {"at": 0.76, "event": "arrow: reads everything below"}],
      "LibraryIconRow of layer icons", "Layers are a stack, and a stack with a drawing order is clearest as panes sliding into place.",
      "docs CanvasLayer (index 0 default scene, higher drawn above); verify2 M6, verify3 K6")
manim("B13", 1, "a full-screen color rect eats mouse clicks", "ClicksStop",
      "The two panes again, side view: the game pane below, the full-rect colour rect pane above, labelled 'Mouse > Filter: Stop' (the editor's own words). A click (a drawn arrow tip with an expanding ring) comes down from above and stops at the colour rect, which flashes. The label changes to 'Mouse > Filter: Ignore' and the next click passes through the colour rect to the game pane, which flashes.",
      "The first click stops at the rect; after the label changes the second click passes straight through.",
      [{"at": 0.12, "event": "two panes, label Stop"}, {"at": 0.30, "event": "click 1 stops at the rect"}, {"at": 0.46, "event": "settled: click stopped"}, {"at": 0.70, "event": "label Ignore; click 2 reaches the game"}],
      "ShaderLab with a scripted click", "A click that stops or passes is a path, and a path is a drawn arrow; a Godot capture would need an input log nobody can see.",
      "verify5 N1: a full-screen ColorRect left the game with 0 clicks; with Pass or Ignore it received 1")
manim("B14", 1, "gray: a weighted sum of red, green and blue", "WeightedSum",
      "One meadow pixel as a green swatch. Three horizontal bars show its red, green and blue values. Each bar is multiplied by a weight chip (0.299, 0.587, 0.114) and shrinks to a partial bar; the three partial bars then slide together end to end into one gray bar and a gray swatch appears beside the green one. The 0.587 chip is ringed last. Caption 'dot(a, b): multiply the matching parts and add them' (the GLOSSARY's wording).",
      "Three bars shrink by their weights and join end to end into one gray bar, and the gray swatch appears.",
      [{"at": 0.10, "event": "pixel swatch; three channel bars"}, {"at": 0.30, "event": "weight chips; bars shrink"}, {"at": 0.42, "event": "bars join into one gray bar"}, {"at": 0.50, "event": "settled: gray bar and swatch"}, {"at": 0.74, "event": "the 0.587 chip ringed"}],
      "plot of luma against green", "A sum is three pieces becoming one, and that is a shape change, which Manim transforms rather than cuts.",
      "docs: dot and mix; Wikipedia Grayscale (weights); verify3 K2 (matches within 1/255)")
lab("B15", 1, "mix: one dial from color to gray", "05-gray.gdshader", "reading-the-screen/gray.mp4", "Godot 4.7.2 · Forward+ · amount swept by script",
    [{"at": 0.02, "lines": [9], "label": "mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b"}, {"at": at("B15", "Make the amount a uniform"), "lines": [4], "label": "hint_range: a slider from 0 to 1"}, {"at": at("B15", "drain the color"), "lines": [9]}],
    "Code card at left (the @NL(05-gray.gdshader)@-line gray shader); at right a real Godot window: the meadow and the teal player under a full-screen filter. The amount uniform sweeps from 0 to 1 and the colour drains out of the whole picture, grass, path, flowers and player together.",
    "The colour drains from everything at once as the dial turns.",
    [{"at": 0.02, "event": "mix line highlighted"}, {"at": 0.43, "event": "amount line highlighted"}, {"at": 0.62, "event": "colour starts to drain"}, {"at": 0.95, "event": "fully gray"}],
    "ShaderLab stills of amount 0 and 1", "A dial turning is a continuous change and the whole picture draining is the claim; two stills would lose the dial.",
    "C05: scene_c05_gray.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Meadow + player, 05-gray on a full-screen ColorRect in a CanvasLayer (layer 1); amount 0 until u = 0.62, then 1 by u = 0.95. Verified: amount 0, 0.5, 1 match the weights and mix exactly (within 1/255, 9 of 9).",
    "verify3 K2", readouts=[{"at": 0.30, "text": "amount 0", "x": 0.5, "y": 0.94}, {"at": 0.92, "text": "amount 1", "x": 0.5, "y": 0.94}])
lab("B16", 1, "the spotlight: color near the player, gray elsewhere", "06-spotlight-oval.gdshader", "reading-the-screen/spot-oval.mp4", "Godot 4.7.2 · Forward+ · scripted walk",
    [{"at": at("B16", "where the player is"), "lines": [3]}, {"at": at("B16", "how big the circle is"), "lines": [4]}],
    "Code card at left (the @NL(06-spotlight-oval.gdshader)@-line spotlight shader with the plain distance test); at right a real Godot window: the meadow in gray with a coloured area around the teal player, who walks one lap of a flat ellipse. The uniform lines light up as the voice names them.",
    "The coloured area follows the walking player.",
    [{"at": 0.40, "event": "player uniform line highlighted"}, {"at": 0.70, "event": "radius uniform line highlighted"}],
    "ShaderLab stills", "The effect following the player is the picture the next four beats take apart; a still would hide that it follows.",
    "C06: scene_c06_spot_oval.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. The player walks one lap of an ellipse (0.20 x 0.12 of the canvas) round the middle; every frame the scene's _process sends player position / canvas size to the filter; radius 0.25. The same capture serves B17. Route check: the spotlight scenes look the same on the 4K route as in a plain 1280 x 720 window (verify10 B, within 1 canvas pixel).",
    "verify3 K3 and K4", )
lab("B17", 1, "distance and radius: gray outside, color inside", "06-spotlight-oval.gdshader", "reading-the-screen/spot-oval.mp4", "Godot 4.7.2 · Forward+ · scripted walk",
    [{"at": 0.02, "lines": [8], "label": "distance: the gap between two addresses"}, {"at": at("B17", "If it is more than the radius"), "lines": [9]}, {"at": at("B17", "Otherwise"), "lines": [11]}],
    "The same capture as the previous beat with different lines lit: the distance test, the gray line, the final colour line.",
    "The coloured area keeps following the player while the lines of the test light up in order.",
    [{"at": 0.02, "event": "distance test highlighted"}, {"at": 0.58, "event": "gray line highlighted"}, {"at": 0.82, "event": "colour line highlighted"}],
    "LectureCodeTrace alone", "Code with its running result beats code alone: the viewer sees which pixels each line decides.",
    "C06 again (see B16): reuse the same video file.", "verify3 K3 (06 inside and outside radius)")
manim("B18", 1, "why the circle stretches: addresses are not pixels", "StretchedAddresses",
      "A unit square labelled 'addresses: 0 to 1 across, 0 to 1 down' with a circle of radius 0.25 drawn inside it. The square stretches sideways into a 16:9 screen rectangle and the circle becomes an ellipse. Two measurements appear along the ellipse: sideways '0.25 × 1280 = 320 px', up and down '0.25 × 720 = 180 px'. Caption 'oval'.",
      "The square stretches into the wide screen and the circle stretches with it into an oval.",
      [{"at": 0.12, "event": "unit square with a circle"}, {"at": 0.34, "event": "the square stretches into the 16:9 screen"}, {"at": 0.46, "event": "settled: ellipse"}, {"at": 0.64, "event": "the two measurements"}],
      "ShaderLab with readouts on the oval capture", "The cause is the stretch from a square of addresses to a wide screen, which is a transformation; the numbers then name it.",
      "verify3 K3: radius 0.25 on a 1280 x 720 canvas reaches 320 px sideways and 180 px up and down (measured 321/320 and 181/180)")
lab("B19", 1, "the fix: scale both addresses by width over height", "07-spotlight.gdshader", "reading-the-screen/spot-swap.mp4", "Godot 4.7.2 · Forward+ · shader swapped at 72 percent",
    [{"at": 0.02, "lines": [8, 9], "label": "SCREEN_PIXEL_SIZE: one pixel, as a fraction of the screen"}, {"at": at("B19", "Its y divided"), "lines": [9], "label": "aspect ratio: width divided by height"}, {"at": at("B19", "Stretch both addresses"), "lines": [9, 10]}],
    "Code card at left (the @NL(07-spotlight.gdshader)@-line fixed spotlight); at right the same walk: the coloured area is an oval until 72 percent of the beat, when the shader is swapped and it becomes a circle.",
    "The oval snaps to a circle at the cue.",
    [{"at": 0.02, "event": "the pixel size and aspect lines highlighted"}, {"at": at("B19", "Its y divided"), "event": "label defines 'aspect ratio'"}, {"at": 0.72, "event": "the multiply lines highlighted"}, {"at": 0.72, "event": "the oval becomes a circle"}],
    "ShaderLab with a split view of both shaders", "A before and after on the same walk is the proof; the swap makes the cause (the extra two lines) and the effect (round) one event.",
    "C07: scene_c07_spot_swap.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. As C06; at u = 0.72 the material is swapped from 06-spotlight-oval to 07-spotlight (radius 0.25 carried over). Verified: 07 reaches 180 px both ways. Route check: the spotlight scenes look the same on the 4K route as in a plain 1280 x 720 window (verify10 B, within 1 canvas pixel).",
    "verify3 K1 (screen pixel size is one over the resolution) and K3")
lab("B20", 1, "the game sends the player's position every frame", None, "reading-the-screen/spot-game.mp4", "Godot 4.7.2 · Forward+ · scripted walk",
    [{"at": at("B20", "So every frame"), "lines": [1]}, {"at": at("B20", "takes the player's position"), "lines": [3]}, {"at": at("B20", "divides it"), "lines": [2, 4]}, {"at": at("B20", "and sends it"), "lines": [4], "label": "set_shader_parameter: sends a value to a uniform"}],
    "Code card at left with the four-line GDScript _process; at right the finished circular spotlight following the walking player.",
    "The lines light up as the voice names them while the circle follows the player.",
    [{"at": 0.18, "event": "func line highlighted"}, {"at": 0.30, "event": "the on-screen position line highlighted"}, {"at": 0.50, "event": "the division lines highlighted"}, {"at": 0.62, "event": "the call highlighted"}],
    "LectureCodeTrace on the GDScript", "The cause (four lines) and the effect (the circle following) together.",
    "C08: scene_c08_spot_game.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. The scene's own _process is exactly the four lines shown. Verified: the centroid of the lit area sits on the player within 1 px (verify7 C08); with a moved Camera2D the canvas-transform version lands on the player while plain position / size does not (verify8). Route check: the spotlight scenes look the same on the 4K route as in a plain 1280 x 720 window (verify10 B, within 1 canvas pixel).",
    "verify3 K4; verify7 C08; verify8 Q", code=GAME_SCRIPT, code_file="scene script (GDScript)")

# ───────────────────────────── ACT III · Bend What Is Behind ─────────────────────────────
lab("B21", 2, "read somewhere else: add a small number to the address", "08-shift.gdshader", "reading-the-screen/shift.mp4", "Godot 4.7.2 · Forward+ · shift swept by script",
    [{"at": at("B21", "Read somewhere else"), "lines": [7]}, {"at": at("B21", "a small number"), "lines": [4]}],
    "Act title 'Bend What Is Behind' (serif 40) top-left. Code card at left (the @NL(08-shift.gdshader)@-line shift shader); at right a real Godot window: one large window in a cream frame over the meadow. The shift uniform sweeps from 0 to 0.1 and the picture inside the frame slides sideways against the picture outside; the sand path breaks at the frame's edges. Label 'shift 0.1'.",
    "The picture inside the frame slides to the left while the picture outside stays put.",
    [{"at": 0.30, "event": "spot line highlighted"}, {"at": 0.57, "event": "shift uniform highlighted; the sweep begins"}, {"at": 0.90, "event": "label 'shift 0.1'"}],
    "manim arrow on a picture", "A real window sliding against its surroundings shows the break at the frame's edge, which an arrow only implies.",
    "C09: scene_c09_shift.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Window 0.52 x 0.42 at (0.20, 0.12); shift 0 until u = 0.56, then 0.10 by u = 0.90. Verified: 3,640 of 3,640 sampled pixels show the meadow at x + shift (for 0.1 and for -0.05).",
    "verify4 L1", title=N.ACTS[2][1], readouts=[{"at": 0.90, "text": "shift 0.1", "x": 0.5, "y": 0.94}])
lab("B22", 2, "a sine of the row: each row pushed by a different amount", "09-ripple-still.gdshader", "reading-the-screen/ripple-still.mp4", "Godot 4.7.2 · Forward+ · amount grown by script",
    [{"at": at("B22", "Sine is a smooth wave"), "lines": [7], "label": "sin: a smooth wave between -1 and 1"}, {"at": at("B22", "each row gets"), "lines": [8]}],
    "Code card at left (the @NL(09-ripple-still.gdshader)@-line ripple shader without time); at right a real Godot window: a large window in a cream frame; as the amount grows the straight tile edges inside become a chevron of ripples and the flowers stretch sideways.",
    "Straight lines inside the frame start to ripple as the amount grows.",
    [{"at": 0.20, "event": "sine line highlighted"}, {"at": 0.64, "event": "the push line highlighted"}, {"at": 0.92, "event": "ripples at full amount"}],
    "manim plot of sin(y) with rows shifted", "The real ripple is the claim; the plot would explain the function but not what a viewer will see in a game.",
    "C10: scene_c10_ripple_still.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Window 0.56 x 0.52 at (0.20, 0.08); amount 0 until u = 0.44, then 0.012 by u = 0.92. Verified: the tile edge in ten rows sits at 560 minus 0.01 sin(60 y) times 1280, within 0.5 px (0.6 in Compatibility; the edge is found to a whole pixel).",
    "verify4 L2")
lab("B23", 2, "add TIME inside the sine and the ripples travel", "10-ripple.gdshader", "reading-the-screen/ripple-time.mp4", "Godot 4.7.2 · Forward+ · live clock",
    [{"at": 0.02, "lines": [7], "label": "TIME: seconds on one clock shared by the whole game"}],
    "Code card at left (the @NL(10-ripple.gdshader)@-line ripple shader with TIME); at right the same large window with the ripples now travelling, live. Label 'time: one clock'.",
    "The ripples travel through the window, in step across it.",
    [{"at": 0.02, "event": "the sine line with TIME highlighted"}, {"at": 0.60, "event": "label 'time: one clock'"}],
    "ShaderLab stills", "Travel is motion; stills cannot show it.",
    "C11: scene_c11_ripple_time.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps (fixed tick, so TIME is repeatable), Forward+, length = the beat's audio. Same window as C10, amount 0.01.",
    "verify4 L3 (472 sampled pixels changed in 0.4 s in Forward+, 449 in Compatibility)", readouts=[{"at": 0.60, "text": "time: one clock", "x": 0.5, "y": 0.94}])
lab("B24", 2, "keep the push small", "10-ripple.gdshader", "reading-the-screen/amount.mp4", "Godot 4.7.2 · Forward+ · amount swept by script",
    [{"at": 0.02, "lines": [4]}],
    "Code card at left with the amount line lit; at right the travelling-ripple window while amount sweeps: calm ripples at 0.01, then the picture shears into streaks at 0.06. Readouts '0.01' then '0.06'.",
    "The ripples grow from calm to torn as the number grows.",
    [{"at": 0.02, "event": "amount line highlighted"}, {"at": 0.40, "event": "readout 0.01: ripples read as water"}, {"at": 0.90, "event": "readout 0.06: the picture tears"}],
    "manim plot of amplitude", "Seeing the picture tear is the lesson; a number alone does not say how much is too much.",
    "C12: scene_c12_amount.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. As C11; amount 0.002 rising to 0.01 by u = 0.30, held to u = 0.60, then to 0.06 by u = 0.95.",
    "verify4 L2 (the formula); design advice shown by the capture",
    readouts=[{"at": 0.40, "text": "0.01", "x": 0.5, "y": 0.94}, {"at": 0.90, "text": "0.06", "x": 0.5, "y": 0.94}])
lab("B25", 2, "mipmaps and textureLod: a blurred copy", "14-blur.gdshader", "reading-the-screen/blur.mp4", "Godot 4.7.2 · Forward+ · blur level swept by script",
    [{"at": at("B25", "Add the hint"), "lines": [4], "label": "mipmap: smaller, blurrier copies of a texture"}, {"at": at("B25", "Read a higher level"), "lines": [8], "label": "textureLod: reads one chosen level"}],
    "Code card at left (the @NL(14-blur.gdshader)@-line blur shader; the declaration runs over two lines); at right a real Godot window: a large window in a cream frame; as the blur level rises from 0 to 4 the meadow inside turns to frosted glass while the picture outside stays sharp. Label 'level 4' once the level has reached it.",
    "The picture inside the frame blurs progressively as the level rises.",
    [{"at": 0.22, "event": "filter_linear_mipmap highlighted"}, {"at": 0.62, "event": "textureLod line highlighted; the sweep begins"}, {"at": 0.88, "event": "label 'level 4'"}],
    "manim stack of shrinking images", "Frosted glass appearing is the whole claim; the stack of smaller copies is explained by the narration.",
    "C13: scene_c13_blur.gd, NATIVE route: a 1920 x 1080 SubViewport at scale 1, the scene built for a 1920 x 1080 canvas (--native; NOT the 4K route, see CAPTURE-PLAN.md 'Routes'), 30 fps, Forward+, length = the beat's audio. Window 0.56 x 0.56 at (0.20, 0.14); blur 0 until u = 0.58, then exactly 4.0 by u = 0.84, held. Verified: largest step between neighbouring pixels 0.377 at level 0, 0.012 at level 2, 0.008 at level 4 (1280 x 720 window, verify4 L8a); mean difference between the level-4 picture and the sharp one inside the window 0.028 on this route, 0.017 on the 4K route, 0.037 in a plain 1280 x 720 window (verify10 A).",
    "verify4 L8a (Forward+); verify10 A (the route); Compatibility renders it less blurred but alike", readouts=[{"at": 0.88, "text": "level 4", "x": 0.5, "y": 0.94}])
lab("B26", 2, "which address drives the waves: the window's own, or the screen's", None, "reading-the-screen/ride-glued.mp4", "Godot 4.7.2 · Forward+ · the world scrolls (scripted)",
    [], "Two windows in cream frames over a meadow that scrolls down and back. Left: ripples from the window's own address (UV.y); right: ripples from the screen address (SCREEN_UV.y). Both ripple fields are frozen. Labels 'UV: rides along' and 'screen UV: stays'; small labels 'UV.y' and 'SCREEN_UV.y' under the windows.",
    "On the left the ripples move down with the window; on the right they stay at the same screen rows while the window slides over them.",
    [{"at": 0.18, "event": "label 'UV: rides along' on the left window"}, {"at": 0.60, "event": "label 'screen UV: stays' on the right window"}, {"at": 0.88, "event": "the scroll returns"}],
    "manim two sine plots", "Relative motion between a window and its ripples is the claim and needs the real thing moving; plots would not show it.",
    "C14: scene_c14_ride_glued.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. WorldRoot (meadow with a 2-cell bleed + both windows) moves down 140 px between u = 0.12 and 0.52 and back by u = 0.96. Windows 0.30 x 0.46 at (0.08, 0.14) with 13-ripple-ride and at (0.58, 0.14) with 09-ripple-still; no TIME. Verified: after a 100 px move the glued window's edge offsets are unchanged in 6 of 6 rows; the ride window's changed in 6 of 6.",
    "verify4 L6", layout="video",
    readouts=[{"at": 0.18, "text": "UV: rides along", "x": 0.23, "y": 0.08}, {"at": 0.60, "text": "screen UV: stays", "x": 0.73, "y": 0.08},
              {"at": 0.18, "text": "UV.y", "x": 0.23, "y": 0.92}, {"at": 0.60, "text": "SCREEN_UV.y", "x": 0.73, "y": 0.92}])
lab("B27", 2, "tint the bent picture toward water; the color picker", "11-water.gdshader", "reading-the-screen/pool-tint.mp4", "Godot 4.7.2 · Forward+ · live; colour changed by script at the end",
    [{"at": 0.02, "lines": [8, 9]}, {"at": at("B27", "Mix the bent picture"), "lines": [11]}, {"at": at("B27", "The source color hint"), "lines": [4], "label": "source_color: shows a color picker"}],
    "Code card at left (the @NL(11-water.gdshader)@-line water shader); at right a real Godot window: the pool, a plain rectangle in the lower left, tinted blue over the bent meadow, rippling live. Near the end the water colour changes blue to violet, as an artist would with the colour picker.",
    "The pool ripples and, at the end, its colour changes from blue to violet.",
    [{"at": 0.02, "event": "wave and spot lines highlighted"}, {"at": 0.30, "event": "mix line highlighted"}, {"at": 0.58, "event": "water uniform highlighted"}, {"at": 0.84, "event": "water colour changes"}],
    "manim blend diagram", "The tinted, rippling pool is the result and the colour change is the reason for the hint; both are only real in a render.",
    "C15: scene_c15_pool_tint.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps (fixed tick), Forward+, length = the beat's audio. Pool 0.40 x 0.40 at (0.06, 0.52) with 11-water; water = (0.2, 0.5, 0.8) until u = 0.78, then to (0.6, 0.3, 0.8) by u = 0.94. Verified: pool pixel = 0.5 x meadow + 0.5 x water (both renderers); the shader reports a colour hint (no alpha) for water.",
    "verify4 L4, verify6 R1")
lab("B28", 2, "the pool's top edge: discard above a wavy line", "12-pool.gdshader", "reading-the-screen/pool.mp4", "Godot 4.7.2 · Forward+ · live",
    [{"at": at("B28", "Compare the pool's own"), "lines": [7]}, {"at": at("B28", "Above that wavy line"), "lines": [7, 8, 9]}, {"at": at("B28", "Discard throws"), "lines": [8], "label": "discard: throws the pixel away"}],
    "Code card at left (the @NL(12-pool.gdshader)@-line pool shader); at right the same pool capture as the opening: the wavy top edge ripples, and above it the grass shows through.",
    "The top edge of the pool undulates while the grass above it stays untouched.",
    [{"at": 0.16, "event": "the edge test highlighted"}, {"at": 0.58, "event": "the whole discard block highlighted"}, {"at": 0.76, "event": "the discard line highlighted"}],
    "ShaderLab stills", "A wavy edge is only an edge when it moves.",
    "C01 again (see B01): reuse the same video file. Verified: the first changed row down the pool is a different UV.y at five columns (0.080 to 0.115 in Forward+) and the meadow above it is untouched.",
    "verify4 L5")
lab("B29", 2, "the payoff: the pool scrolls with the world and its waves go with it", None, "reading-the-screen/pan.mp4", "Godot 4.7.2 · Forward+ · the world scrolls (scripted)",
    [], "A real Godot window: the meadow, the finished pool and the player all scroll down together and back. The pool's ripples travel with the pool. Label 'pool scrolls too'.",
    "The whole scene pans and the pool stays glued to the ground, rippling.",
    [{"at": 0.54, "event": "the pan starts"}, {"at": 0.62, "event": "label 'pool scrolls too'"}, {"at": 0.90, "event": "the pan returns"}],
    "ShaderLab stills", "A pan is motion and the pool riding the ground is the claim.",
    "C16: scene_c16_pan.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps (fixed tick), Forward+, length = the beat's audio. WorldRoot (meadow with a 2-cell bleed, the 12-pool pool, the player) moves down 110 px between u = 0.54 and 0.74 and back between u = 0.80 and 0.98.",
    "verify5 N3 (a window that is a child of a moving world still reads at its screen position)", layout="video",
    readouts=[{"at": 0.62, "text": "pool scrolls too", "x": 0.5, "y": 0.94}])

# ───────────────────────────── ACT IV · What It Can See ─────────────────────────────
manim("B30", 3, "the copy is taken once per layer, before the first reader", "OnceBeforeTheFirstReader",
      "Act title 'What It Can See' (serif 40) top-left. A row of draw-step tiles inside a bracket 'layer 0': ground, tree, reader 1 (a window), player, reader 2 (a second window); 'reader: a node whose shader reads the screen texture'. A camera flash fires just before 'reader 1' and a copy tile drops below the row, labelled 'the copy'. Tiles before the flash get a check mark; the tiles after it do not. An arrow from reader 2 points at the same copy tile, not a new one.",
      "The flash fires once, before the first reader; checks land on the earlier tiles only; the second reader's arrow points at the same copy.",
      [{"at": 0.10, "event": "tiles in a layer bracket; act title"}, {"at": 0.36, "event": "flash before reader 1; the copy tile drops"}, {"at": 0.46, "event": "settled: row and the copy tile"}, {"at": 0.60, "event": "arrow from reader 2 to the same copy"}, {"at": 0.78, "event": "checks on the earlier tiles"}, {"at": 0.90, "event": "later tiles stay unchecked"}],
      "BrowserCapture of the docs 'Behind the scenes' paragraph", "The rule is an order of events, which a timeline shows as motion; the docs paragraph is quoted in FACTCHECK.",
      "docs Screen-reading shaders, 'Back-buffer logic'; verify2 M2, verify2b P1 to P5")
lab("B31", 3, "an X-ray of the copy: a miniature lens", "02-miniature.gdshader", "reading-the-screen/xray.mp4", "Godot 4.7.2 · Forward+ · the lens is moved later in the tree at 76 percent",
    [], "A real Godot window: the meadow with a big mustard block at lower left (drawn before the lens) and a violet block at lower centre (drawn after it); top right, a lens in a cream frame shows a tiny copy of the screen, with the mustard block in it and no violet block. Labels 'drawn before' and 'drawn after'. At 76 percent the lens moves later in the tree and the violet block appears inside it.",
    "The violet block appears inside the lens when the lens moves later in the draw order.",
    [{"at": 0.42, "event": "label 'drawn before'"}, {"at": 0.62, "event": "label 'drawn after'"}, {"at": 0.76, "event": "the lens moves later; the violet block appears in it"}],
    "manim two copies side by side", "The lens is the film's one instrument for looking inside the copy, and the change at 76 percent is the proof that draw order decides.",
    "C17: scene_c17_xray.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Tree order World, X (mustard block, 0.16 x 0.26 at (0.08, 0.60)), Lens (02-miniature, 0.30 x 0.30 at (0.60, 0.06)), Y (violet block at (0.52, 0.58)); at u = 0.76 the lens is moved to the end of the tree. Verified: before the move the lens shows X and not Y (red and blue test blocks in verify2 M1 give the same result).",
    "verify2 M1", layout="video",
    readouts=[{"at": 0.42, "text": "drawn before", "x": 0.16, "y": 0.55}, {"at": 0.62, "text": "drawn after", "x": 0.60, "y": 0.53}])
lab("B32", 3, "two overlapping windows that each flip: the overlap stays flipped", "03-invert.gdshader", "reading-the-screen/overlap.mp4", "Godot 4.7.2 · Forward+ · the second window appears at 30 percent",
    [], "A real Godot window: window A (cream frame) flips the colours over the meadow. At 30 percent window B (cream frame) appears, overlapping A's lower right. The overlap looks exactly like the rest of A and B, flipped once. A terracotta ring settles on the overlap; labels 'expected: original' and 'got: flipped'.",
    "B appears over A and the overlap is flipped once, not twice.",
    [{"at": 0.30, "event": "window B appears over A"}, {"at": 0.43, "event": "label 'expected: original'"}, {"at": 0.60, "event": "ring on the overlap"}, {"at": 0.64, "event": "label 'got: flipped'"}],
    "manim two layered panes", "The unexpected result is the lesson, and a real overlap that does not flip back is more convincing than a diagram that says it.",
    "C18: scene_c18_overlap.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. A = 03-invert at (0.16, 0.12), B = 03-invert at (0.38, 0.30), both 0.34 x 0.46, same canvas; B hidden until u = 0.30. Overlap region (0.38, 0.30) to (0.50, 0.58). Verified: the overlap reads inverted once (1 minus meadow), in both renderers.",
    "verify2b P1 (same canvas), P3 (same layer), P5 (nested)", layout="video",
    readouts=[{"at": 0.43, "text": "expected: original", "x": 0.84, "y": 0.50}, {"at": 0.64, "text": "got: flipped", "x": 0.84, "y": 0.58}],
    rings=[{"at": 0.60, "box": [0.37, 0.29, 0.51, 0.59]}])
lab("B33", 3, "BackBufferCopy, copy mode Viewport, between them: the overlap restores", "03-invert.gdshader", "reading-the-screen/overlap-fix.mp4", "Godot 4.7.2 · Forward+ · the node is switched on at 76 percent",
    [], "The same two windows from the start; a BackBufferCopy node sits between them in the tree and is switched on at 76 percent. Before it, the overlap is flipped once; after it, the overlap shows the original meadow colours. Label 'Back Buffer Copy · Viewport' appears early; a ring settles on the overlap at the end.",
    "The overlap snaps back to the original colours at the cue.",
    [{"at": 0.10, "event": "label 'Back Buffer Copy · Viewport'"}, {"at": 0.76, "event": "the node switches on; the overlap restores"}, {"at": 0.84, "event": "ring on the overlap"}],
    "manim node between two panes", "The restoring overlap is the proof of the fix, in the very frame where the bug was shown.",
    "C19: scene_c19_overlap_fix.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. As C18 with both windows visible from the start and a BackBufferCopy (copy_mode Viewport) between A and B, visible (switched on) from u = 0.76. Verified: with it the overlap reads as the original meadow; with a default BackBufferCopy (Rect mode) it does not.",
    "verify2b P2 and P6", layout="video",
    readouts=[{"at": 0.10, "text": "Back Buffer Copy", "x": 0.5, "y": 0.06}], rings=[{"at": 0.84, "box": [0.37, 0.29, 0.51, 0.59]}])
lab("B34", 3, "a layer of its own takes its own copy: the filter sees the pool", "05-gray.gdshader", "reading-the-screen/fresh-layer.mp4", "Godot 4.7.2 · Forward+ · amount swept by script",
    [], "A real Godot window: the meadow, the live pool and the player on the game layer; a gray filter on its own layer starts at amount 0. At 72 to 90 percent the amount rises and the whole picture, pool and player included, turns gray together. Label 'own layer'; a ring on the pool.",
    "Pool, player and grass all go gray together.",
    [{"at": 0.26, "event": "label 'own layer'"}, {"at": 0.57, "event": "ring on the pool"}, {"at": 0.72, "event": "the filter amount rises"}, {"at": 0.90, "event": "everything gray"}],
    "manim layered panes", "The pool turning gray with the grass is the proof that the filter saw it, and nothing but the render shows that.",
    "C20: scene_c20_fresh_layer.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps (fixed tick), Forward+, length = the beat's audio. Meadow, 12-pool, player on layer 0; 05-gray on a full-screen ColorRect in a CanvasLayer (layer 1), amount 0 until u = 0.72, then 1 by u = 0.90. No BackBufferCopy. Verified: the player's pixel and the pool's pixel equal their luma grays (player 0.5529 against 0.5514; pool 0.5804 against 0.5795).",
    "verify2 M4 and M5; verify4 L9; verify2b P4", layout="video",
    readouts=[{"at": 0.26, "text": "own layer", "x": 0.5, "y": 0.94}], rings=[{"at": 0.57, "box": [0.05, 0.50, 0.47, 0.93]}])
lab("B35", 3, "a layer above the filter is untouched", "05-gray.gdshader", "reading-the-screen/hud.mp4", "Godot 4.7.2 · Forward+ · the health bar's layer is set to two at 58 percent",
    [], "A real Godot window: the game is already gray. The health bar, top left, starts on layer 0 and is gray with it; at 58 percent its layer index is set to 2 and it turns mustard while the game stays gray. Labels 'layer 0: gray' and 'layer 2: color'.",
    "The health bar regains its colour at the cue while the game stays gray.",
    [{"at": 0.30, "event": "label 'layer 0: gray' on the bar"}, {"at": 0.58, "event": "the bar's layer is set to 2; it turns mustard"}, {"at": 0.74, "event": "label 'layer 2: color'"}],
    "manim stacked panes", "The bar regaining its colour in the same frame is the proof; a pane diagram would only say it.",
    "C21: scene_c21_hud.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Meadow + player; 05-gray on layer 1 at amount 1 from the first frame; the health bar in its own CanvasLayer, index 0 until u = 0.58, then 2. Verified: a bar on layer 2 keeps its colour (0.902, 0.722, 0.251), a bar below the filter is flipped or grayed.",
    "verify2 M6; verify3 K6", layout="video",
    readouts=[{"at": 0.30, "text": "layer 0: gray", "x": 0.14, "y": 0.16}, {"at": 0.74, "text": "layer 2: color", "x": 0.14, "y": 0.16}])
lab("B36", 3, "repeat disable and filter nearest: two more hints, and the renderer that obeys one", "15-edge-clamp.gdshader", "reading-the-screen/edge.mp4", "Godot 4.7.2 · Forward+ · shift swept by script",
    [{"at": 0.02, "lines": [3, 4]}, {"at": at("B36", "Repeat disable means"), "lines": [4], "label": "repeat_disable: past the edge, the edge pixel"}, {"at": at("B36", "Filter nearest asks"), "lines": [4], "label": "filter_nearest: the exact pixel, no blending"},
     {"at": at("B36", "The Forward Plus renderer"), "lines": [4], "label": "renderer: how Godot draws; your project picks one of three"}],
    "Code card at left (the @NL(15-edge-clamp.gdshader)@-line shader with the full declaration over two lines); at right a real Godot window: a window flush with the right edge of the screen; as the shift grows its right part reads past the edge and fills with horizontal streaks, the edge pixels repeated. The third label defines 'renderer' where the narration first says it; the capture is Forward+ (the video label says so), so the Compatibility half of the sentence is carried by the narration alone.",
    "The window's right part smears into streaks as it reads past the edge of the screen.",
    [{"at": 0.02, "event": "the declaration highlighted"}, {"at": at("B36", "Repeat disable means"), "event": "repeat_disable highlighted"}, {"at": 0.28, "event": "the smear begins"}, {"at": at("B36", "Filter nearest asks"), "event": "filter_nearest highlighted"}, {"at": 0.62, "event": "full smear"}, {"at": at("B36", "The Forward Plus renderer"), "event": "label defines 'renderer'"}],
    "BrowserCapture of the docs declaration", "The smear is what repeat_disable does, in the one place it shows; filter_nearest changes nothing visible at this size, so it gets a label and a sentence, not a picture.",
    "C22: scene_c22_edge.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Window 0.40 x 0.44 at (0.60, 0.20) flush with the right edge, 15-edge-clamp; shift 0 until u = 0.28, then 0.30 by u = 0.62. Verified: with repeat_disable (and with no repeat hint) a read past the edge returns the edge pixel in both renderers. filter_nearest is a Forward+ result only: magnified 50 times, Forward+ gives a hard step where filter_linear gives 35 distinct colours; Compatibility reads all three alike (34), so the narration names the renderer (verify4 L7b, verify9). This capture does not show that difference.",
    "verify4 L7a and L7b; verify9")
lab("B37", 3, "everything at once", None, "reading-the-screen/finale.mp4", "Godot 4.7.2 · Forward+ · scripted walk",
    [], "A real Godot window: the pool, the player walking a wide flat ellipse, the spotlight following him (gray outside, colour inside), the health bar above everything in colour. Where the player passes the pool, the pool turns to colour as the light arrives and the water keeps rippling.",
    "The light follows the player across the pool, which turns to colour and ripples under it, while the health bar never changes.",
    [{"at": 0.10, "event": "the player near the pool; the pool in colour"}, {"at": 0.45, "event": "the player far right; the pool gray"}, {"at": 0.90, "event": "the player returns to the pool"}],
    "manim three icons", "The three effects living together, with the order rules holding, is the closing proof.",
    "C23: scene_c23_finale.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps (fixed tick), Forward+, length = the beat's audio. Layer 0: meadow, 12-pool, the player on a wide ellipse (0.34 x 0.10 of the canvas around (0.50, 0.62)); layer 1: 07-spotlight (radius 0.25) fed by the scene's _process; layer 2: the health bar. Route check: the spotlight scenes look the same on the 4K route as in a plain 1280 x 720 window (verify10 B, within 1 canvas pixel).",
    "verify3 K4, verify2 M6, verify4 L9", layout="video")
rem("B38", 3, "four symptoms and their causes", "LectureEvidenceTable",
    {"title": "When a screen shader misbehaves", "headers": ["What you see", "Why", "Fix"],
     "rows": [["Error naming SCREEN_TEXTURE", "a Godot 3 shortcut", "hint_screen_texture"],
              ["A sprite missing from the copy", "drawn after the reader", "draw it earlier"],
              ["A second effect ignores the first", "one copy per layer", "Back Buffer Copy"],
              ["Health bar turns gray", "below the filter", "a higher layer"]],
     "note": "Godot 4.7 docs and runs on Godot 4.7.2", "cues": [at("B38", "The old name"), at("B38", "The draw order"), at("B38", "The copy for each layer"), at("B38", "And which layer")],
     "durationSeconds": "__AUDIO__"},
    "A four-row table, one row ringed as the voice names each cause.", "The ring steps down the rows with the voice.",
    [{"at": 0.28, "event": "the old name row"}, {"at": 0.43, "event": "the draw order row"}, {"at": 0.62, "event": "the copy for each layer row"}, {"at": 0.80, "event": "the health bar row"}],
    "manim checklist", "Four parallel facts, each a symptom and a cause, are exactly what the table component is for.", "rows 22, 23, 55, 56 and 58 to 62 of FACTCHECK.md")

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
for e in E:
    vi = e["entry"]["visual_intent"]
    e["entry"]["visual_intent"] = re.sub(r"@NL\(([^)]+)\)@", lambda m: str(nl(m.group(1))), vi)
    e["entry"]["show"] = sorted(e["entry"]["show"], key=lambda x: x["at"])

(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(len(N.ACTS)):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

ids = [e["bid"] for e in E]
assert ids == [b for b, _, _ in N.BODY], "lane entries must follow the narration's beat ids"
lanes_hist = {}
for e in E:
    lanes_hist[e["entry"]["lane"]] = lanes_hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
distinct_caps = sorted({e["entry"]["props"]["video"] for e in E if e["entry"]["lane"] == "capture"})
sl = [f"# Shot list: {N.TITLE}\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      f". The {len(distinct_caps)} Godot captures (C01 to C23) are all small scene scripts that already run: `evidence/planning-checks/scene_c*.gd`, tested through `scene_runner.gd`. Every shader shown is a tested file in `lab-shaders/`. Eleven Manim scenes and the shared components below must be built.\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`). 2. **`shader_kit.py`** Manim helpers (same file). 3. **Capture driver**: this film brings its own, already tested: `evidence/planning-checks/scene_capture.gd` (see `CAPTURE-PLAN.md`: the scene contract). The shared `lab/capture.gd` is not needed for this film. 4. Eleven Manim scenes (the rows below with a `manim` lane): `B02_TheCopy`, `B04_ThePieces`, `B05_FilledEveryFrame`, `B06_AddressToColor`, `B07_TwoAddresses`, `B11_FullRect`, `B12_LayerStack`, `B13_ClicksStop`, `B14_WeightedSum`, `B18_StretchedAddresses`, `B30_OnceBeforeTheFirstReader`.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist, f"; {len(distinct_caps)} distinct capture videos")
print("\n".join(NOTES))
