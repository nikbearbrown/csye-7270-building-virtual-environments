#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text, and the shot list must say exactly what the lanes say.
Re-run after any edit:   python3 _gen_lanes.py && python3 make_sheet.py
(Never re-run make_sheet.py after `art final`: it clears the build stamps.)
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
E = []          # entries in beat order
RUN = "evidence/planning-checks"


def file_text(fn):
    return (SH / fn).read_text().rstrip("\n")


def code_of(fn, start=None, end=None):
    """The real text of a lab shader, optionally lines start..end (1-based, inclusive). Returns (code, codeFile caption)."""
    lines = file_text(fn).split("\n")
    if start is None:
        return "\n".join(lines), f"lab-shaders/{fn}"
    chunk = lines[start - 1:end]
    assert chunk, (fn, start, end)
    return "\n".join(chunk), f"lab-shaders/{fn} · lines {start}–{end}"


def fragment_range(fn):
    """1-based (start, end) of the fragment() function of a shader file."""
    lines = file_text(fn).split("\n")
    s = next(i for i, l in enumerate(lines) if l.startswith("void fragment()")) + 1
    e = next(i for i in range(s, len(lines) + 1) if lines[i - 1] == "}")
    return s, e


def _scene_lengths():
    """seconds of each capture scene, read from capture_scene.gd (the one source of truth)"""
    text = (HERE / RUN / "capture_scene.gd").read_text()
    build = text[text.index("func build("):text.index("func _outline(")]
    lens = {}
    for m in re.finditer(r'^\t\t(\"c\d\d[ab]?\"(?:, \"c\d\d[ab]?\")*):\n\t\t\tduration = ([0-9.]+)', build, re.M):
        for sid in re.findall(r'c\d\d[ab]?', m.group(1)):
            lens[sid] = float(m.group(2))
    return lens


LEN = _scene_lengths()


def _len_text(text):
    return re.sub(r"@LEN:(c\d\d[ab]?)@", lambda m: ("%g" % LEN[m.group(1)]), text)


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects + the new ones listed in SHOTLIST.md)"):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, video, label, intent, motion, show, runner, why, spec, evidence, layout="video", code="", code_file="", cues=None,
        readouts=None, rings=None, ramp=None, title=None, caption="", lane="capture"):
    props = {"layout": layout, "code": code, "codeFile": code_file, "cues": cues or [], "video": video, "videoLabel": label,
             "readouts": readouts or [], "rings": rings or [], "caption": caption, "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    add(bid, act, about, {"lane": lane, "pattern": "ShaderLab", "props": props, "capture_spec": _len_text(spec), "visual_intent": intent,
                          "motion_claim": motion, "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


FWD = "Godot 4.7.2 · Forward+"
# canvas fractions (the capture is a 1280 x 720 logical canvas): the 512 px picture is centred: x 0.3 to 0.7, y 0.144 to 0.856
LEFT_X, RIGHT_X = 0.278, 0.722          # centres of the two 512 px displays in the two-display captures (x = 100..612 and 668..1180)

# ───────────────────────────── ACT I · A Picture Off to the Side ─────────────────────────────
lab("B01", 0, "the finished effect: a spinning sprite, rainbow stripes, a ripple", "subviewports/c01-hook.mp4", f"{FWD} · scripted spin · offline render",
    "Act title 'A Picture Off to the Side' (serif 40) top-left. A real Godot render on the cream stage: the teal blob turns, rainbow stripes slide across it, and the whole picture ripples like cloth. Nothing is labelled yet; the effect is the hook.",
    "The blob turns, the stripes slide and the picture ripples the whole time.",
    [{"at": 0.0, "event": "the finished effect already running"}, {"at": 0.5, "event": "stripes and ripple keep moving"}],
    "manim drawing of the finished look", "A real render is the honest picture of an effect; a drawing would only claim it.",
    "C01 (scene c01): picture 512, blob 448 with 01-inner-gradient (turned by a script at 0.9 rad/s), shown on a QuadMesh 512 x -512, 31 x 31, with 09-rainbow-wobble. @LEN:c01@ s, 30 fps, Forward+.",
    "C01 · verify7 c01", title="A Picture Off to the Side")
manim("B02", 0, "a SubViewport draws into a picture of its own; off-screen", "OffScreenBox",
      "Two frames on the cream stage. Right: a large outline rectangle labelled 'screen', empty. Left: a smaller dashed square labelled 'SubViewport'. A teal blob fades into the small square, then a text glyph 'Aa', a small button outline and a three-line cube join it. The screen stays empty the whole time. Caption under the square: 'off-screen: drawn, not shown directly'; a one-line definition on the square: 'draws its children into a picture of its own'.",
      "Children drop into the small square one by one while the screen frame stays empty.",
      [{"at": 0.12, "event": "screen frame and the SubViewport square"}, {"at": 0.3, "event": "blob lands inside the square; the screen stays empty"}, {"at": 0.62, "event": "text, button and cube join it"}, {"at": 0.84, "event": "caption: off-screen"}],
      "DesignPipelineClaim, show-tell isometric", "The claim is 'drawn, but not shown': a box that fills while the screen stays empty says it with motion.")
lab("B03", 0, "the Viewport Texture shows the picture on a sprite", "subviewports/c02-texture-appears.mp4", f"{FWD} · texture handed over at 7 s · scripted",
    "Code card with the one real line at left; at right a real Godot window on the cream stage: empty for seven seconds, then the picture appears (a teal blob in a mid-grey box, the viewport's clear colour) at the moment the line runs.",
    "The stage is empty until the texture is handed over, then the picture appears.",
    [{"at": 0.0, "event": "empty stage"}, {"at": 0.6, "event": "line highlighted; the picture appears"}],
    "manim: a drawn box feeding a screen", "Nothing on screen, then the picture on the very line that makes it appear, is the claim as a cause and an effect.",
    "C02 (scene c02): picture 512 opaque (clear colour #A8A090), blob 448, a Sprite2D whose texture is empty until 7.0 s, then `display.texture = sub.get_texture()`. @LEN:c02@ s, 30 fps, Forward+. Verified (run-7a): the centre is the stage (0.851, 0.835, 0.792) at 6 s and the teal blob (0.373, 0.639, 0.569) in the clear-coloured box at 8.5 s.",
    "C02 · verify1 A1, A2 · docs", layout="side", code="display.texture = sub.get_texture()", code_file="scene script (GDScript)",
    cues=[{"at": 0.6, "lines": [1], "label": "ViewportTexture: the viewport's latest picture"}],
    readouts=[{"at": 0.64, "text": "texture handed over", "x": 0.5, "y": 0.08}])
lab("B04", 0, "the editor steps: size, a sprite inside, New, then Viewport Texture", "subviewports/e1-setup.mp4", "Godot 4.7.2 editor · three real frames · scripted editor session",
    "Three real frames of the whole Godot editor window, cross-dissolving: (1) subviewports_E1-1_subviewport-size: Scene dock Main > SubViewport > Sprite2D, Display; the SubViewport selected; the Inspector with its picture preview and Size 512 x 512, ring on Size; (2) subviewports_E2-1_texture-dropdown-new-viewporttexture: the Display sprite's Texture slot menu open (a Search box, the heading New, ViewportTexture highlighted), ring on ViewportTexture; (3) subviewports_E2-4_viewport-path-set: the ViewportTexture with Viewport Path = SubViewport, ring on Viewport Path.",
    "The ring moves slot to slot as the voice names each step.",
    [{"at": 0.08, "event": "SubViewport Size ringed"}, {"at": 0.54, "event": "the Texture slot's menu is open"}, {"at": 0.78, "event": "ViewportTexture ringed under New"}, {"at": 0.89, "event": "Viewport Path = SubViewport ringed"}],
    "GodotDevWorkbench (labelled reconstruction)", "Real editor frames are the first rung of SHOW-THE-THING; every label on them was read from the editor itself (planning evidence).",
    "E1-1, E2-1, E2-4: three static editor frames of the scratch project, recorded by the series' editor driver from this film's state script (evidence/planning-checks/editor-driver/state-scripts/subviewports-E1.json, run-15; the -wide variant widens the Inspector so long labels read in full). The clicks themselves are not shown, only the resulting states; the menu frame is the real Texture slot menu.",
    "Editor frames subviewports_E1-1, E2-1, E2-4 (evidence/planning-checks/editor-frames/series-driver); labels in run-14", lane="editor")
manim("B05", 0, "the same setup in code, line by line", "CodeBuilds",
      "Left: a code card with five real lines (monospace): var sub := SubViewport.new() / sub.size = Vector2i(512, 512) / add_child(sub) / sub.add_child(inner_sprite) / display.texture = sub.get_texture(). Right: a diagram that builds with the focused line: a small tree 'Main' on top, a dashed box, a screen frame at the lower right. Line 1 draws the dashed box ('sub'); line 2 writes '512 x 512' along its edges; line 3 hooks it under 'Main'; line 4 drops a teal blob into it; line 5 draws an arrow from the box to a display sprite on the screen, and the blob appears on the screen.",
      "Each line, when focused, makes its piece appear on the right.",
      [{"at": 0.1, "event": "line 1: the dashed box"}, {"at": 0.27, "event": "line 2: 512 x 512"}, {"at": 0.42, "event": "line 3: hooked under Main"}, {"at": 0.6, "event": "line 4: the blob drops in"}, {"at": 0.78, "event": "line 5: the arrow and the picture on screen"}],
      "LectureCodeTrace beside a static diagram", "A line and its consequence appear together; only a drawing built line by line shows that each line adds one piece.",
      evidence=f"the five lines run as written in {RUN}/verify1_basics.gd (A1, A2, A3)")
lab("B06", 0, "the size is the picture's resolution", "subviewports/c03-size-is-resolution.mp4", f"{FWD} · scripted: Filter switches at 12.5 s",
    "Two real displays of the same blob, both 512 px across on the stage: left a 512 px picture drawn 1:1 (crisp), right a 128 px picture drawn 4x (soft with the Linear filter). Partway, the right display's Filter switches to Nearest and the soft edge turns into hard blocks.",
    "The right picture is soft, then snaps into crisp blocks when the filter changes.",
    [{"at": 0.0, "event": "512 px and 128 px pictures side by side"}, {"at": 0.82, "event": "Filter: Nearest; the edge turns into blocks"}],
    "manim pixel grid", "The softness and the blocks are the claim; only the real render shows what the engine does to a small picture.",
    "C03 (scene c03): two opaque viewports, 512 and 128 px (blob drawn natively at each size), displays at x = 100 and x = 668, the right at scale 4; Filter Linear until 12.5 s (on the words \"Filter to Nearest\"), then Nearest. @LEN:c03@ s, Forward+. Verified (run-7a): soft edge 8 pixels on the blob row with Linear at 7 s, 0 with Nearest at 14 s, runs 104 / 304 / 104 (multiples of 4).",
    "C03 · verify1 B1, verify7 c03", caption="resolution: how many pixels the picture holds",
    readouts=[{"at": 0.1, "text": "512 px", "x": LEFT_X, "y": 0.92}, {"at": 0.1, "text": "128 px ×4", "x": RIGHT_X, "y": 0.92}, {"at": 0.3, "text": "Filter: Linear", "x": RIGHT_X, "y": 0.06}, {"at": 0.82, "text": "Filter: Nearest", "x": RIGHT_X, "y": 0.06}])
lab("B07", 0, "the origin is the top-left corner; a centred sprite at (0, 0)", "subviewports/c04a-origin.mp4", f"{FWD} · scripted slide",
    "A real display of a 512 px picture (mid-grey box). The blob starts in the middle, slides to the top-left corner and settles there: only its bottom-right quarter is in the picture and its eyes are gone. A terracotta ring marks the corner; a readout 'origin (0, 0)'.",
    "The blob slides into the corner and three quarters of it vanish, eyes first.",
    [{"at": 0.0, "event": "blob in the middle"}, {"at": 0.18, "event": "ring on the origin corner"}, {"at": 0.5, "event": "the blob slides into the corner"}, {"at": 0.89, "event": "three quarters out; no eyes"}],
    "manim: axes with a clipped sprite", "The clipping is the claim; the real picture shows exactly which part survives.",
    "C04a (scene c04a): opaque picture 512, blob 448 centred at (256, 256), stays in the middle while the voice explains the origin, slides to (0, 0) between 6.4 s and 8.6 s (on \"placed at zero, zero\"), then holds; @LEN:c04a@ s, Forward+. Verified (run-7a): 55,202 teal and 1,546 eye pixels at 5 s; at (0, 0) from 8.6 s the picture holds 14,187 teal pixels = 25.7 % of the whole blob and 0 eye pixels.",
    "C04a · verify1 C1, verify7 c04a", caption="origin: where the picture's coordinates start, (0, 0)",
    rings=[{"at": 0.18, "box": [0.27, 0.10, 0.34, 0.2]}],
    readouts=[{"at": 0.18, "text": "origin (0, 0)", "x": 0.35, "y": 0.08}, {"at": 0.89, "text": "no eyes", "x": 0.5, "y": 0.92}])
lab("B08", 0, "slide it to the middle, then off the edge: cut off", "subviewports/c04b-cut-off.mp4", f"{FWD} · scripted slide",
    "The same display. The blob slides from the corner to the middle (all of it appears), holds, then slides off the right edge and is cut off sharply at the picture's edge. Readouts 'all of it' then 'cut off'.",
    "The blob arrives whole in the middle, then is sliced by the picture's right edge.",
    [{"at": 0.0, "event": "corner quarter"}, {"at": 0.28, "event": "whole in the middle"}, {"at": 0.62, "event": "cut by the right edge"}],
    "manim", "The cut line is the claim; a real picture shows it cut without a seam.",
    "C04b (scene c04b): opaque picture 512, blob slides from (0, 0) to (256, 256) between 0.3 s and 3.3 s, holds, then to x = 560 between 4.0 s and 7.0 s; @LEN:c04b@ s, Forward+. Verified (run-7a): 14,187 teal pixels at 0.2 s, 55,202 in the middle at 3.7 s, 15,470 when the blob is cut by the right edge at 9 s and at the end (centre at x = 560).",
    "C04b · verify1 C1, verify7 c04b",
    readouts=[{"at": 0.28, "text": "all of it", "x": 0.5, "y": 0.92}, {"at": 0.62, "text": "cut off", "x": 0.78, "y": 0.5}])
lab("B09", 0, "Transparent BG makes the empty parts see-through", "subviewports/c05-transparent.mp4", f"{FWD} · scripted: Transparent BG on at 8 s",
    "Code card with one line at left; at right the display over a faint grey grid: first the picture's mid-grey box hides the grid, then at the moment the line runs the box vanishes and the grid shows through, leaving only the blob.",
    "The box disappears and the grid behind it shows through.",
    [{"at": 0.0, "event": "box over the grid"}, {"at": 0.62, "event": "Transparent BG on; the box vanishes"}],
    "manim", "A box that vanishes to reveal what was behind it is the claim; the grid makes the see-through visible.",
    "C05 (scene c05): grid of 2 px lines every 64 px behind the display, opaque picture until 8.0 s then `transparent_bg = true`; @LEN:c05@ s, Forward+. Verified (run-7a): the empty pixel is the clear colour (0.659, 0.627, 0.565) before and the stage (0.851, 0.835, 0.792) after; the picture's empty pixel alpha goes from 1 to 0.",
    "C05 · verify1 D1 · docs · editor label", layout="side", code="sub.transparent_bg = true", code_file="scene script (GDScript)",
    cues=[{"at": 0.62, "lines": [1], "label": "Transparent BG: empty parts become see-through"}],
    readouts=[{"at": 0.2, "text": "clear color", "x": 0.5, "y": 0.08}, {"at": 0.72, "text": "see-through", "x": 0.5, "y": 0.92}])
lab("B10", 0, "half-transparent pixels are stored premultiplied: Mix goes dark, Premultiplied Alpha is right", "subviewports/c06-premultiplied.mp4", f"{FWD} · scripted: Blend Mode changes at 10.5 s",
    "One real display of a soft gold glow over the faint grid. It starts with Blend Mode Mix: a muddy dark ring surrounds the glow. At the moment the blend mode changes to Premultiplied Alpha the dark ring vanishes and the glow is clean. A terracotta ring marks the dark ring; readouts name the two blend modes.",
    "The dark ring around the glow vanishes the moment the blend mode changes.",
    [{"at": 0.0, "event": "glow with a dark ring (Mix)"}, {"at": 0.18, "event": "ring on the dark band"}, {"at": 0.74, "event": "Premultiplied Alpha: the ring is gone"}],
    "manim: two swatches and arithmetic", "The ring that vanishes is the claim; arithmetic would explain it, but the real glow is what a viewer will meet.",
    "C06 (scene c06): picture 512 transparent, glow image (gold, alpha falling to 0 over the outer 45 % of its radius) over the grid; the display uses a CanvasItemMaterial, Blend Mode Mix until 10.5 s then Premultiplied Alpha; @LEN:c06@ s, Forward+. Verified (run-7a, run-5 G1) at ring pixel (807, 360): Mix (0.655, 0.608, 0.490), Premultiplied (0.890, 0.800, 0.576), the glow drawn directly (0.890, 0.796, 0.576).",
    "C06 · verify5 P1-P3, G1 (both renderers) · docs", caption="premultiplied: each color already multiplied by its alpha",
    rings=[{"at": 0.18, "box": [0.36, 0.2, 0.64, 0.8]}],
    readouts=[{"at": 0.08, "text": "Blend Mode: Mix", "x": 0.5, "y": 0.07}, {"at": 0.74, "text": "Premultiplied Alpha", "x": 0.5, "y": 0.93}])

# ───────────────────────────── ACT II · Two Shaders, One Result ─────────────────────────────
manim("B11", 1, "the inner shader draws first; the outer shader gets the picture", "TwoPlaces",
      "Act title 'Two Shaders, One Result' (serif 40) top-left. Left: the SubViewport square with the teal blob inside and a small tag 'inner shader' on the blob. A wide arrow labelled 'picture' runs right to a display sprite on a screen frame carrying a tag 'outer shader'. A token (a few teal dots) starts on the blob, turns gold passing the inner tag, rides the arrow, and on reaching the display passes the outer tag and is re-tinted. Small words 'first' under the left half and 'then' under the right.",
      "A token passes the inner shader first, travels as a picture, then passes the outer shader.",
      [{"at": 0.1, "event": "square, blob and inner tag"}, {"at": 0.32, "event": "token turns gold at the inner tag"}, {"at": 0.6, "event": "token rides the arrow as a picture"}, {"at": 0.8, "event": "token re-tinted at the outer tag"}],
      "DesignPipelineClaim, show-tell isometric", "Two stations in order, with a token that changes at each, is the order of work as motion.")
lab("B12", 1, "where each shader goes in the editor: the Material slot of each sprite", "subviewports/e4-materials.mp4", "Godot 4.7.2 editor · three real frames · scripted editor session",
    "Three real frames of the whole Godot editor window, cross-dissolving: (1) subviewports_E4-1_inner-sprite-material: the inner Sprite2D selected, its Inspector's Material group open with the Material slot holding a ShaderMaterial, ring on Material; (2) subviewports_E4-2_display-material: the Display sprite selected, the same slot, ring on Material; (3) subviewports_E4-5_shader-editor: the shader editor open at the bottom showing the outer shader's text (04-stripes).",
    "The ring moves from the inner sprite's Material slot to the display's, then to the shader text.",
    [{"at": 0.1, "event": "inner sprite's Material ringed"}, {"at": 0.57, "event": "display's Material ringed"}, {"at": 0.82, "event": "the outer shader's text in the shader editor"}],
    "GodotDevWorkbench (labelled reconstruction)", "A question about where to click is answered by the real editor, with the labels it really shows.",
    "E4-1, E4-2, E4-5: static editor frames of the scratch project (shaders.tscn), recorded by the series' editor driver from evidence/planning-checks/editor-driver/state-scripts/subviewports-E4.json (run-15; the -wide variant widens the Inspector).",
    "Editor frames subviewports_E4-1 to E4-5 (evidence/planning-checks/editor-frames/series-driver)", lane="editor")
code, cf = code_of("01-inner-gradient.gdshader")
lab("B13", 1, "the inner shader: a gradient by the sprite's own UV", "subviewports/c07-inner-shader.mp4", f"{FWD} · scripted: the shader goes on at 7 s",
    "Code card with the seven-line inner shader at left; at right a real display of the picture: a plain teal blob that, at the moment the voice names the gradient, turns teal at the top to gold at the bottom. Readouts 'UV.y 0' at the top of the blob and 'UV.y 1' at its bottom.",
    "The plain blob takes on the teal-to-gold gradient when the shader goes on.",
    [{"at": 0.08, "event": "fragment function highlighted"}, {"at": 0.3, "event": "COLOR line"}, {"at": 0.6, "event": "UV line; the gradient has appeared"}],
    "LectureCodeTrace alone", "Code and its result side by side with the switch-on is the claim: this line makes this look.",
    "C07 (scene c07): picture 512 transparent, blob 448; the plain sprite until 7.0 s, then 01-inner-gradient; the display uses 02-outer-passthrough; @LEN:c07@ s, Forward+. Verified (run-2 F1): the picture's colour at sprite UV.y 0.265 / 0.501 / 0.738 is (0.522, 0.671, 0.510) / (0.651, 0.698, 0.459) / (0.784, 0.729, 0.408) = mix(teal, gold, UV.y).",
    "C07 · verify2 F1, verify7 c07", layout="side", code=code, code_file=cf,
    cues=[{"at": 0.08, "lines": [3], "label": "runs once for each pixel the shape covers; sets its color"},
          {"at": 0.3, "lines": [6], "label": "COLOR: the color of the pixel being drawn; fragment() sets it"},
          {"at": 0.62, "lines": [6], "label": "a point's address on the shape: 0 to 1 across, 0 to 1 down"}],
    readouts=[{"at": 0.7, "text": "UV.y 0", "x": 0.62, "y": 0.25}, {"at": 0.78, "text": "UV.y 1", "x": 0.62, "y": 0.75}])
code, cf = code_of("02-outer-passthrough.gdshader")
lab("B14", 1, "the outer shader gets the picture as TEXTURE; a pass-through matches it exactly", "subviewports/c08-passthrough.mp4", f"{FWD} · scripted: the sprite inside slides",
    "Code card with the six-line pass-through at left; at right two real displays of the same moving picture side by side: the picture shown directly (Premultiplied Alpha) and the picture shown through the pass-through shader. They are identical frame by frame while the blob slides. Readout 'same pixels'.",
    "The two displays follow the sliding blob identically.",
    [{"at": 0.1, "event": "TEXTURE line"}, {"at": 0.3, "event": "render_mode line"}, {"at": 0.58, "event": "copy line; both displays identical"}],
    "LectureCodeTrace alone", "Two identical moving pictures are the claim that a pass-through changes nothing; one picture could not show it.",
    "C08 (scene c08): picture 512 transparent, gradient blob sliding x = 256 + 60 sin(0.9 t); left display a Sprite2D with CanvasItemMaterial Premultiplied Alpha, right display 02-outer-passthrough; @LEN:c08@ s, Forward+. Verified: largest channel difference between the two displays 0.0 (run-7a); and all 262,144 pixels of the display equal the picture (run-2 F2).",
    "C08 · verify2 F2, verify7 c08", layout="side", code=code, code_file=cf,
    cues=[{"at": 0.1, "lines": [5], "label": "the node's own picture; texture(TEXTURE, uv) reads it"},
          {"at": 0.3, "lines": [2], "label": "blend_premul_alpha: colors already carry their alpha"},
          {"at": 0.58, "lines": [5]}],
    readouts=[{"at": 0.2, "text": "shown directly", "x": LEFT_X, "y": 0.92}, {"at": 0.2, "text": "through the shader", "x": RIGHT_X, "y": 0.92}, {"at": 0.76, "text": "same pixels", "x": 0.5, "y": 0.07}])
code, cf = code_of("03-outer-fade.gdshader")
lab("B15", 1, "the outer fade: multiply the whole color by UV.x", "subviewports/c09-fade.mp4", f"{FWD} · scripted: the fade goes on at 4.5 s",
    "Code card with the six-line fade shader at left; at right the display: the full gradient blob until the fade goes on, then it fades from nothing at the picture's left edge to full at its right edge. A thin 0-to-1 ramp strip under the display is traced as the fade appears.",
    "The picture fades left to right the moment the shader goes on, and the ramp underneath is traced.",
    [{"at": 0.3, "event": "COLOR line; the fade appears"}, {"at": 0.62, "event": "the whole color, alpha included"}],
    "manim ramp strip", "The picture itself fading is the claim; the ramp under it shows the multiplier that does it.",
    "C09 (scene c09): picture 512 transparent, gradient blob; the display uses 02-outer-passthrough until 4.5 s then 03-outer-fade; @LEN:c09@ s, Forward+. Verified (run-7b) at picture x = 196 / 256 / 316: the multiplier is 0.389 / 0.500 / 0.622 (expected 0.384 / 0.501 / 0.618); on an opaque white picture it is x / 512 from edge to edge (run-2 F3).",
    "C09 · verify2 F3, verify7 c09 · verify5 P3", layout="side", code=code, code_file=cf,
    cues=[{"at": 0.3, "lines": [5], "label": "UV.x: 0 at the picture's left edge, 1 at its right edge"},
          {"at": 0.64, "lines": [5], "label": "the whole color, alpha included"}],
    ramp={"at": 0.3, "from": 0, "to": 1})
manim("B16", 1, "predict: when the sprite turns, which effect turns with it?", "WhichTurns",
      "The picture frame with the teal blob at the centre. A short vertical ramp strip beside the blob labelled 'inner gradient' (teal at the top, gold at the bottom) and a horizontal ramp strip under the frame labelled 'outer fade' (0 to 1, left to right). A curved arrow circles the blob. Two grey question marks and two terracotta dots hover by the strips.",
      "The curved arrow sweeps around the blob while both strips stay where they are, and the question dots pulse.",
      [{"at": 0.1, "event": "frame, blob and both strips"}, {"at": 0.36, "event": "the turn arrow sweeps around the blob"}, {"at": 0.66, "event": "question dots pulse on both strips"}],
      "FormACard with the question", "The question is about two pictures and a turn; the figure carries it (a card that names a visual is a PUNT).")
lab("B17", 1, "reveal: the gradient turns with the sprite, the fade stays put", "subviewports/c10-turn.mp4", f"{FWD} · the half turn is scripted (a line of script, no shader)",
    "A real display of the faded gradient blob. The sprite inside the viewport turns half a turn: the gold half swings from the bottom to the top and the eyes end up below, while the fade (transparent at the picture's left, solid at its right) does not move. Readouts 'gradient turns' and 'fade stays'.",
    "The gold swings round with the sprite while the fade stays left to right.",
    [{"at": 0.0, "event": "the turn starts with the voice"}, {"at": 0.24, "event": "gradient turns"}, {"at": 0.36, "event": "fade stays"}],
    "manim", "A real turn with the two effects visible is the answer; a drawing could only assert it.",
    "C10 (scene c10): as C09 with the fade on from the start; the sprite turns half a turn (0 to pi) between 0.3 s and 3.3 s by script; @LEN:c10@ s, Forward+. Verified (run-7b): red 100 px above / below the centre goes 0.529 / 0.776 to 0.776 / 0.525 (gold flips); the multiplier at picture x = 196 / 256 / 316 stays 0.387 / 0.500 / 0.612; probes at two rotations in run-2 F4.",
    "C10 · verify2 F4, verify3 H2/H3, verify7 c10",
    readouts=[{"at": 0.24, "text": "gradient turns", "x": 0.5, "y": 0.08}, {"at": 0.36, "text": "fade stays", "x": 0.5, "y": 0.92}])
lab("B18", 1, "two sprites in one viewport share one fade; a fade on each sprite restarts at each", "subviewports/c11-group.mp4", f"{FWD} · scripted: the sprites slide",
    "Two framed panels. Left: two blobs with no viewport, each carrying its own fade shader: every blob fades from its own left edge to its own right edge. Right: a viewport holding the same two blobs, shown with one fade across the whole picture: the left blob is faint, the right blob solid. Both pairs slide left and right: the left fades ride along with their sprites, the right fade stays still and the sprites brighten as they move through it.",
    "On the right the blobs brighten as they slide through a fixed fade; on the left each fade rides along.",
    [{"at": 0.0, "event": "two framed panels, sprites sliding"}, {"at": 0.2, "event": "ring on the right panel: one fade"}, {"at": 0.62, "event": "ring on the left panel: a fade each"}],
    "manim two panels", "A fade that stays while content moves through it, against a fade that rides along, is the claim; only a moving capture shows both at once.",
    "C11 (scene c11): left panel Rect(40, 210, 600, 300): two 200 px blobs, each with 03-outer-fade (premultiplied) directly on the Sprite2D; right panel Rect(660, 210, 600, 300): a 600 x 300 transparent viewport holding the same blobs, shown with 03-outer-fade; sprites slide dx = 70 sin(0.8 t) in both; @LEN:c11@ s, Forward+. Verified (run-7b): per sprite 0.5 and 0.5; on the picture 0.254 and 0.754.",
    "C11 · verify7 c11",
    rings=[{"at": 0.2, "box": [0.516, 0.292, 0.984, 0.708]}, {"at": 0.62, "box": [0.031, 0.292, 0.5, 0.708]}],
    readouts=[{"at": 0.2, "text": "one fade", "x": 0.75, "y": 0.8}, {"at": 0.62, "text": "a fade each", "x": 0.265, "y": 0.8}])
manim("B19", 1, "by the time the outer shader runs the sprites are gone: only flattened pixels", "Flattened",
      "Three overlapping cards in the SubViewport square, drawn as a small exploded stack: the blob, a second blob and a rounded rectangle. They slide together and collapse into one flat picture card on the right. A circle-with-a-dot eye labelled 'outer shader' looks at the flat card; a dashed line from the eye back to the original stack is crossed out by two short bars.",
      "The stack collapses into one flat card; the eye sees only the card, and the line back to the sprites is crossed out.",
      [{"at": 0.12, "event": "stack of three"}, {"at": 0.4, "event": "collapse into one flat card"}, {"at": 0.7, "event": "eye sees the card; the line to the sprites is crossed out"}],
      "LectureEvidenceTable", "A stack that becomes one flat card, with a crossed-out line back to the parts, is the limit as motion.")
lab("B20", 1, "the inner shader works in the picture's pixels; the outer shader in the display's pixels", "subviewports/c12-per-display-pixel.mp4", f"{FWD} · scripted: nothing but the stripes move",
    "A real display of a 64 px picture drawn eight times bigger with the Nearest filter: the blob is built from big square blocks, while moving stripes drawn by an outer shader slide across it with crisp one-pixel edges that cut through the blocks at any position. Readouts 'picture pixels' and 'display pixels'.",
    "The stripes' edges slide smoothly through the blocks of the blob, never snapping to them.",
    [{"at": 0.0, "event": "blocky blob, stripes sliding"}, {"at": 0.2, "event": "picture pixels"}, {"at": 0.62, "event": "display pixels"}],
    "manim pixel grid", "Smooth edges cutting through coarse blocks is the claim; only a live render shows that the two shaders live at different resolutions.",
    "C12 (scene c12): transparent viewport 64 px (blob 64 px wide), display at scale 8 (512 px) with Nearest filter and 05-stripes-moving; @LEN:c12@ s, Forward+. Verified (run-6 X4, run-7b): the blob's own edges fall on multiples of 8 display pixels (x = 104 and 408 in run-6); the stripe edges do not (mod 8 = 7, 2, 5, 7, 2, 5, 7 in run-6; other values in run-7b, since the stripes move with TIME). Numbers are at scale 1; the 3x route multiplies them by 3.",
    "C12 · verify6 X4, verify7 c12",
    readouts=[{"at": 0.2, "text": "picture pixels", "x": 0.36, "y": 0.18}, {"at": 0.62, "text": "display pixels", "x": 0.7, "y": 0.18}])

# ───────────────────────────── ACT III · Stripes and Hue ─────────────────────────────
manim("B21", 2, "a diagonal: add the two UV numbers", "Diagonal",
      "Act title 'Stripes and Hue' (serif 40) top-left. A square picture (the kit's UV square: 0 to 1 axes, y pointing down) with thin grey isolines along its diagonals at u + v = 0.5, 1 and 1.5. A ramp strip along the diagonal reads 0 to 2 with end labels '0' and '2'. A terracotta dot travels from the top-left corner to the bottom-right corner with a live label 'u + v'.",
      "The dot moves along the diagonal while its sum climbs from 0 to 2, lighting each isoline as it crosses.",
      [{"at": 0.12, "event": "square, axes and isolines"}, {"at": 0.4, "event": "dot leaves the top-left corner, sum climbing"}, {"at": 0.75, "event": "dot at the bottom right, sum 2"}],
      "ShaderLab", "A coordinate system and a quantity that climbs along it is exactly what the kit's UV square is for.")
manim("B22", 2, "fract makes a saw wave from a rising number", "Saw",
      "The series' signature object: a ramp strip (0 to 1) at the top; below it a plot of fract(x * 6) as a six-tooth saw wave on grey axes; a terracotta dot rides the ramp and its twin rides the plot. Label 'fract(x × 6)' and a one-line definition 'the part after the point: x minus floor(x)'.",
      "The dot climbs the ramp while its twin climbs a tooth, drops, climbs again, six times.",
      [{"at": 0.1, "event": "ramp strip and empty plot"}, {"at": 0.3, "event": "dot traces both; the saw draws"}, {"at": 0.7, "event": "six teeth counted"}],
      "LectureEvidenceTable", "A ramp going in and a function reshaping it into a saw is the claim as motion.")
manim("B23", 2, "step makes a hard edge; one minus step is a stripe", "StepStripe",
      "One saw tooth drawn large; a horizontal threshold line labelled 'width' at 0.5 with a handle; below it the step result as a square wave (0 then 1) with the definition '0 below the edge, 1 from the edge up'; below that '1 - step' as a bar of alternating on and off segments. The threshold handle slides from 0.25 up to 0.75 and the on segments thicken.",
      "The width line slides up and every stripe on the bar thickens in step.",
      [{"at": 0.1, "event": "tooth and threshold line"}, {"at": 0.35, "event": "step square wave"}, {"at": 0.6, "event": "stripe bar"}, {"at": 0.82, "event": "width slides 0.25 to 0.75; stripes thicken"}],
      "ShaderLab", "A threshold sliding across a saw while the stripes thicken is the relation as motion.")
code, cf = code_of("04-stripes.gdshader")
lab("B24", 2, "stripes as a mask: multiply the picture by the stripe; count and width are uniforms", "subviewports/c13-stripes-dials.mp4", f"{FWD} · scripted: width and count are swept",
    "Code card with the twelve-line stripe shader at left; at right the display: diagonal stripes cut the gradient blob so it shows only inside them; the stripes thicken (width 0.08 up to 0.5), hold, then get finer (count 6 up to 12).",
    "The stripes thicken, then multiply, as the dials move; the empty parts stay empty.",
    [{"at": 0.06, "event": "the diagonal, the saw and the stripe lines"}, {"at": 0.2, "event": "COLOR line: the mask"}, {"at": 0.6, "event": "uniform lines: count and width"}],
    "LectureCodeTrace alone", "A mask whose dials move is the claim; code beside the live stripes shows which line does what.",
    "C13 (scene c13): picture 512 transparent, gradient blob, display uses 04-stripes; width sweeps 0.08 to 0.5 (0.5 s to 4.5 s), count 6 to 12 (8 s to 12 s); @LEN:c13@ s, Forward+. Verified (run-7b) at 2 / 6 / 10 s: width 0.213 / 0.5 / 0.5, count 6 / 6 / 9, 0 stripe mismatches over about 2,900 pixels each; on a plain rectangle the on-fraction equals width (0.500, 0.247, 0.800) and `count` complete stripes fit across.",
    "C13 · verify3 S1, verify7 c13", layout="side", code=code, code_file=cf,
    cues=[{"at": 0.06, "lines": [8, 9, 10]}, {"at": 0.2, "lines": [11], "label": "0 below the edge, 1 from the edge up"},
          {"at": 0.62, "lines": [4, 5], "label": "uniform: a value your game sets from outside"}])
code, cf = code_of("05-stripes-moving.gdshader")
lab("B25", 2, "TIME slides the stripes", "subviewports/c14-moving-stripes.mp4", f"{FWD} · the sprite's turn is scripted",
    "Code card with the twelve-line moving-stripes shader at left; at right the display: diagonal stripes slide down and right across the blob while the blob turns slowly underneath and the stripes keep their direction.",
    "The stripes slide steadily; the sprite turns and the stripes do not.",
    [{"at": 0.15, "event": "the diagonal line with TIME"}, {"at": 0.34, "event": "TIME defined on the line"}],
    "manim sine plot", "A live sliding is the claim; the code line beside it is what makes it slide.",
    "C14 (scene c14): as C13 with 05-stripes-moving (count 6, width 0.5, speed 0.12), the blob turning at 0.8 rad/s by script; @LEN:c14@ s, Forward+. Verified (run-7b): the stripe formula with the TIME read in the same draw predicts every probe (0 mismatches over about 2,900 pixels).",
    "C14 · verify3 H2, verify7 c14", layout="side", code=code, code_file=cf,
    cues=[{"at": 0.15, "lines": [9]}, {"at": 0.34, "lines": [9], "label": "TIME: seconds on one clock shared by the whole game"}])
manim("B26", 2, "hue, saturation and value", "ColorWheel",
      "A colour wheel of 72 coloured wedges (full saturation and value) at the left. A marker arrow rotates around it, labelled 'hue: which color'; a radial bar from the centre to the rim, labelled 'saturation: how far from grey' (white at the centre, vivid at the rim); and a short vertical swatch ramp at the right, labelled 'value: how bright'. Three small terracotta dots mark the three controls.",
      "An arrow sweeps round the wheel, a marker slides from centre to rim, a swatch brightens.",
      [{"at": 0.1, "event": "the wheel"}, {"at": 0.3, "event": "hue arrow sweeps round"}, {"at": 0.58, "event": "saturation marker slides centre to rim"}, {"at": 0.8, "event": "value ramp brightens"}],
      "LibraryIconRow", "Three controls on one colour need a wheel, a radius and a ramp; only drawing them shows what each changes.")
manim("B27", 2, "hue as a number from 0 to 1: the six colors", "HueRamp",
      "A ramp strip filled with the hue spectrum from 0 to 1 with seven ticks labelled 0, 1/6, 1/3, 1/2, 2/3, 5/6, 1 and a terracotta marker riding along. Under the marker a swatch shows its colour and a small triple of numbers updates: (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0). A small wheel beside the strip turns its arrow with the marker. Credit: 'Godot 4.7.2 · same in Forward+ and Compatibility'.",
      "The marker rides the strip and stops at each sixth while the swatch and its numbers change.",
      [{"at": 0.1, "event": "strip, ticks and wheel"}, {"at": 0.3, "event": "stops at 0 (red) and 1/6 (yellow)"}, {"at": 0.62, "event": "1/3 (green) and 1/2 (cyan)"}, {"at": 0.86, "event": "2/3 (blue), 5/6 (magenta), back to red"}],
      "LectureEvidenceTable", "A marker riding a strip that changes colour is the ramp-in, colour-out idea as motion.",
      evidence="run-3 H1b (the six exact hues) and run-lab-checks (both renderers)")
manim("B28", 2, "each of red, green and blue is the same plateau, shifted by a third", "Plateaus",
      "A plot with hue 0 to 1 on x and 0 to 1 on y. One red plateau curve (full for a third, zero for a third, ramps between, wrapping round at the edges) draws first; a ghost copy slides a third to the right and becomes the green curve; another slides two thirds and becomes the blue curve. A vertical marker moves along the hue axis and reads three values off the curves into a swatch.",
      "The red plateau slides along to become green, then blue; a marker reads the three curves.",
      [{"at": 0.12, "event": "red plateau"}, {"at": 0.36, "event": "slides a third: green"}, {"at": 0.62, "event": "slides two thirds: blue"}, {"at": 0.84, "event": "marker reads three values into a swatch"}],
      "ShaderLab", "A curve sliding along to become the next is the claim; the plot is the picture of it.")
code, cf = code_of("06-hsv-strip.gdshader", 3, 12)
lab("B29", 2, "the hue function in code, tested at the six hues", "subviewports/c15-hue-strip-and-swatches.png", f"{FWD} · six exact hues (hue uniform set) · same in Compatibility",
    "Code card with the ten real lines (plateau and hsv_to_rgb) at left; at right a still of the hue strip above six flat swatches. As the voice names each pure colour its swatch gets its RGB triple: 1 0 0, 1 1 0, 0 1 0, 0 1 1, 0 0 1, 1 0 1.",
    "The six swatches take their exact numbers one by one.",
    [{"at": 0.06, "event": "abs defined on the plateau line"}, {"at": 0.17, "event": "clamp defined"}, {"at": 0.27, "event": "fract defined"}, {"at": 0.38, "event": "the mix line"}, {"at": 0.62, "event": "the six triples land"}],
    "LectureCodeTrace alone", "Code beside the six exact colours is the test the viewer can see; a still is enough because each number lands on its word.",
    "C15 (scene c15): the hue strip (06-hsv-strip) on a 1000 x 130 rectangle above six 160 px swatches, each a rectangle with 06b-hsv-probe and `hue` = 0, 1/6, 2/6, 3/6, 4/6, 5/6; one PNG frame (scene time 3 s; the scene is @LEN:c15@ s long), Forward+. Verified (run-3 H1, H1b, run-7c): the six swatches read (1,0,0) (1,1,0) (0,1,0) (0,1,1) (0,0,1) (1,0,1) exactly in both renderers; over 65,536 + 65,536 pixels the function agrees with the engine's Color.from_hsv within 0.002, and over 640 columns with Python's colorsys within 0.0019.",
    "C15 · verify3 H1, H1b · run-lab-checks · analyze-hue.py", layout="side", code=code, code_file=cf,
    cues=[{"at": 0.06, "lines": [2], "label": "abs drops the minus sign: -0.3 becomes 0.3"},
          {"at": 0.17, "lines": [2], "label": "clamp holds a value between 0 and 1"},
          {"at": 0.27, "lines": [2], "label": "the part after the point: x minus floor(x)"},
          {"at": 0.38, "lines": [9], "label": "blends from a to b: t of 0 gives a, 1 gives b"}],
    readouts=[{"at": 0.62, "text": "1 0 0", "x": 0.172, "y": 0.74}, {"at": 0.68, "text": "1 1 0", "x": 0.305, "y": 0.74}, {"at": 0.74, "text": "0 1 0", "x": 0.438, "y": 0.74},
              {"at": 0.8, "text": "0 1 1", "x": 0.57, "y": 0.74}, {"at": 0.86, "text": "0 0 1", "x": 0.703, "y": 0.74}, {"at": 0.92, "text": "1 0 1", "x": 0.836, "y": 0.74}])
fs, fe = fragment_range("07-rainbow-stripes.gdshader")
code, cf = code_of("07-rainbow-stripes.gdshader", fs, fe)
lab("B30", 2, "rainbow stripes: the diagonal is the hue", "subviewports/c16-rainbow-stripes.mp4", f"{FWD} · the sprite's turn is scripted",
    "Code card with the seven-line fragment function at left; at right the display: rainbow stripes slide across the turning gradient blob, the gaps between them showing the gradient, the colours travelling with the stripes.",
    "The rainbow slides with the stripes while the gradient shows through the gaps.",
    [{"at": 0.1, "event": "the diagonal line"}, {"at": 0.24, "event": "the band line: hue from the diagonal"}, {"at": 0.6, "event": "the mix line"}],
    "manim", "The finished look beside its seven lines is the payoff of the act; only a live render shows the colours travelling.",
    "C16 (scene c16): as C14 with 07-rainbow-stripes (count 6, width 0.5, speed 0.12); @LEN:c16@ s, Forward+. Verified (run-3 H4, run-7c): stripe pixels equal Color.from_hsv(fract(diagonal)) within 0.002 over about 2,400 pixels; every gap pixel equals the picture (2,496 of 2,496 in run-3 H4).",
    "C16 · verify3 H4, verify7 c16", layout="side", code=code, code_file=cf,
    cues=[{"at": 0.1, "lines": [3]}, {"at": 0.24, "lines": [5], "label": "the diagonal itself is the hue"}, {"at": 0.62, "lines": [6], "label": "blends from a to b: t of 0 gives a, 1 gives b"}])

# ───────────────────────────── ACT IV · Wobble the Result ─────────────────────────────
manim("B31", 3, "vertex() runs once per corner; four corners can only lean", "FourCorners",
      "Act title 'Wobble the Result' (serif 40) top-left. A rectangle (the sprite) with four terracotta corner dots and the definition 'vertex: a corner point of a shape'. 'vertex' flashes on each dot in turn; the top-right and bottom-right dots slide down and the rectangle leans into a parallelogram with straight edges. A faint dashed curve tries to bend the top edge but the edge stays straight. Caption 'four corners, straight edges'.",
      "Two corners slide and the whole shape leans; the edge between them stays a straight line.",
      [{"at": 0.12, "event": "rectangle with four corner dots"}, {"at": 0.35, "event": "corners flash in turn"}, {"at": 0.62, "event": "two corners slide, the shape leans"}, {"at": 0.85, "event": "dashed curve rejected, edge straight"}],
      "ShaderLab", "Four dots, two of which slide while the edges stay straight, is the limit as motion.",
      evidence="Manim; backed by run-4 M3 and M5 (a plain quad and a Sprite2D keep a straight edge)")
manim("B32", 3, "cut a Quad Mesh into a grid: 31 cuts each way is 1,089 corners", "CutIntoGrid",
      "A rectangle with four corner dots; cut lines appear in steps of 0, 1, 7, 15 and 31 cuts each way, the grid getting finer and a corner counter reading 4, 9, 81, 289 and 1,089 while the dots multiply and shrink. Labels 'Subdivide Width' and 'Subdivide Depth' beside the last two steps; caption 'Quad Mesh, drawn by Mesh Instance 2D'; the definition 'mesh: the set of vertices and triangles that make a shape'.",
      "The grid gets finer in steps and the corner counter climbs to 1,089.",
      [{"at": 0.1, "event": "plain rectangle, 4 corners"}, {"at": 0.3, "event": "1 and 7 cuts: 9 and 81 corners"}, {"at": 0.58, "event": "15 cuts: 289 corners; labels"}, {"at": 0.84, "event": "31 cuts: 1,089 corners"}],
      "editor frame of the QuadMesh Inspector", "The cutting is the idea and the counter is its measure; the Inspector frame only shows where the numbers live.",
      evidence="run-4 M2 (vertex counts 4, 9, 81, 289, 1,089); editor labels read in run-14 (mesh pass)")
lab("B33", 3, "the same wobble on a plain quad and on the grid", "subviewports/c17-plain-vs-grid.mp4", f"{FWD} · offline render",
    "Two real meshes side by side showing one picture (a cream card with a teal frame and the gradient blob), both under the same wobble shader. Left, a plain quad: the card only leans, its edges straight. Right, the 31 x 31 grid: its edges ripple as a wave. Readouts '4 corners' and '1,089 corners'.",
    "The left card tilts with straight edges while the right card ripples.",
    [{"at": 0.0, "event": "two meshes wobbling"}, {"at": 0.2, "event": "corner counts"}],
    "manim", "Straight edges against a wave on the same picture is the claim; a live render makes the difference undeniable.",
    "C17 (scene c17): one transparent 512 px viewport with a card (teal frame 20 px, cream inside) and the gradient blob; two MeshInstance2D, QuadMesh 480 x -480, subdivide 0 at (330, 360) and 31 at (950, 360), both with 08-wobble (amplitude 16, frequency 10, speed 3) and the Linear filter; @LEN:c17@ s, Forward+. Verified (run-7c): plain quad second differences of the top edge in {-1, 0, 1} (straight); grid edge within 0.23 to 0.26 px (rms) of 120 + sin(UV.x * 10 + TIME * 3) * 16 (the shape depends on TIME).",
    "C17 · verify4 M3, M5, verify7 c17", readouts=[{"at": 0.2, "text": "4 corners", "x": 0.26, "y": 0.93}, {"at": 0.2, "text": "1,089 corners", "x": 0.74, "y": 0.93}])
code, cf = code_of("08-wobble.gdshader")
lab("B34", 3, "the wobble is one line in the outer vertex function", "subviewports/c18-wobble.mp4", f"{FWD} · offline render",
    "Code card with the fourteen-line wobble shader at left; at right the 31 x 31 mesh carrying the card and the blob, rippling continuously. The vertex function and the VERTEX.y line are highlighted in turn.",
    "The card ripples continuously while the highlighted line is the one that does it.",
    [{"at": 0.08, "event": "vertex function highlighted"}, {"at": 0.3, "event": "the VERTEX.y line"}, {"at": 0.62, "event": "sin defined on the line"}],
    "LectureCodeTrace alone", "The live ripple beside its one line is the claim; nothing else shows that one line is enough.",
    "C18 (scene c18): the C17 picture on one MeshInstance2D, QuadMesh 512 x -512, 31 x 31, with 08-wobble; @LEN:c18@ s, Forward+. Verified (run-7c): top edge within 0.2 to 0.33 px (rms) of 104 + sin(UV.x * 10 + TIME * 3) * 16 (the shape depends on TIME).",
    "C18 · verify4 M3, verify7 c18", layout="side", code=code, code_file=cf,
    cues=[{"at": 0.08, "lines": [8, 9, 10], "label": "runs once for each vertex; places the corners"}, {"at": 0.3, "lines": [9]},
          {"at": 0.62, "lines": [9], "label": "sin: a smooth back and forth between -1 and 1"}])
lab("B35", 3, "a Quad Mesh lands the picture upside down in 2D; a negative height fixes it", "subviewports/c19-upside-down.mp4", f"{FWD} · scripted: the height changes at 9.5 s",
    "One real mesh showing the card and the blob: first upside down (the eyes below the centre), then at the moment the height goes negative the picture is upright (eyes above). Readouts 'height 512' and 'height -512'.",
    "The face flips from upside down to upright when the height goes negative.",
    [{"at": 0.0, "event": "upside down"}, {"at": 0.1, "event": "height 512"}, {"at": 0.74, "event": "height -512: upright"}],
    "manim vertex arrows", "The flip is the claim; the picture turning right way up is what a viewer will want to see.",
    "C19 (scene c19): the C17 picture on a QuadMesh with size (512, 512) until 9.5 s, then (512, -512), pass-through shader; @LEN:c19@ s, Forward+. Verified (run-4 M1, M4, M6, both renderers; run-7c): with (512, 512) the picture's top-left marker lands at the screen's bottom-left; with a negative height it lands at the top-left; the mesh's own layout puts UV (0, 0) on the vertex with y = +1 (up in 3D, down in 2D).",
    "C19 · verify4 M1, M4, verify7 c19", readouts=[{"at": 0.1, "text": "height 512", "x": 0.5, "y": 0.93}, {"at": 0.74, "text": "height -512", "x": 0.5, "y": 0.07}])
manim("B36", 3, "the whole chain: nodes, inner shader, picture, outer fragment, outer vertex", "WholeChain",
      "A left-to-right chain on the cream stage: a dashed square holding the blob and card icons, then a tag 'inner shader', then the picture card, then a tag 'outer fragment: stripes', then a tag 'outer vertex: bend', then a screen frame with a wobbling frame on it. A token (the blob thumbnail) changes at each stage: plain, gradient, striped, striped and bent.",
      "The token passes each stage and changes its look: plain, gradient, striped, bent.",
      [{"at": 0.1, "event": "the chain drawn"}, {"at": 0.28, "event": "token plain, then gradient"}, {"at": 0.6, "event": "gradient, then striped"}, {"at": 0.82, "event": "striped, then bent"}],
      "DesignPipelineClaim, show-tell isometric", "A token that changes at every stage is the order of work, and the film's whole story, as motion.")
manim("B37", 3, "three shaders in a row: a picture inside another viewport", "StageToStage",
      "Three picture frames in a row: 'viewport' (the blob with an inner shader) leads to a picture, shown inside a second 'viewport' by a sprite with a fade shader, which leads to a second picture, shown on the screen by a sprite with a stripes shader. Three tags 'inner', 'middle' and 'outer'. A token flows along and picks up each shader's look.",
      "The token passes three shaders in a row, each time through a picture.",
      [{"at": 0.1, "event": "three frames and three tags"}, {"at": 0.35, "event": "token through the inner shader"}, {"at": 0.6, "event": "token through the middle shader"}, {"at": 0.82, "event": "token through the outer shader"}],
      "ShaderLab", "A token passing three stations is the generalisation of the chain; the run in evidence proves it works.",
      evidence="run-6 X3 (2,934 probes, 0 stripe mismatches, colour error <= 0.005)")
code, cf = "sub.render_target_update_mode = SubViewport.UPDATE_ONCE", "scene script (GDScript)"
lab("B38", 3, "a viewport draws every frame it is shown; Update Mode Once draws one time and keeps the picture", "subviewports/c21-update-mode.mp4", f"{FWD} · scripted: the right viewport is set to Once at 8.5 s",
    "Code card with one line at left; at right two real displays of two identical viewports whose sprite wanders about in a Lissajous path. Both follow it until the right one is set to Once; from then on the right picture freezes while the left keeps moving. Readouts 'default' and 'Update Mode: Once'.",
    "The right picture freezes while the left one keeps following the wandering sprite.",
    [{"at": 0.3, "event": "default label; both follow"}, {"at": 0.58, "event": "Once: the right picture freezes"}],
    "manim", "One frozen picture beside one live picture is the claim; the pair makes a non-event visible.",
    "C21 (scene c21): two opaque 512 px viewports, a 269 px blob in each moving as (256 + 150 sin 0.9 t, 256 + 90 cos 0.7 t); displays at x = 100 and 668; viewport 1 gets `render_target_update_mode = UPDATE_ONCE` at 8.5 s (on \"set Update Mode to Once\"); @LEN:c21@ s, Forward+. Verified (run-7c, run-11 O1, recorded through Movie Maker in run-13): at 12 s the left picture's first teal pixel is at x = 29 (formula 28); the right is at 323, frozen at its 8.5 s position (formula 322).",
    "C21 · verify1 E1-E5, verify7 c21 · docs", layout="side", code=code, code_file=cf,
    cues=[{"at": 0.58, "lines": [1], "label": "Once: draw one time, then keep the picture"}],
    readouts=[{"at": 0.3, "text": "default", "x": LEFT_X, "y": 0.92}, {"at": 0.66, "text": "Update Mode: Once", "x": RIGHT_X, "y": 0.92}])
manim("B39", 3, "input does not reach a standalone SubViewport; a SubViewportContainer passes it in", "ClickBounces",
      "A screen frame with the display showing the picture of a small SubViewport square that holds a button icon. A cursor arrow (a drawn shape) clicks on the picture; the click ring bounces off the picture's edge and the button icon stays unlit. Then a wrapper frame labelled 'SubViewportContainer' appears around the square; the cursor clicks again, a dotted line carries the click through the container into the square and the button icon lights teal.",
      "The click bounces off a standalone viewport, then passes through the container and lights the button.",
      [{"at": 0.1, "event": "screen, picture, button icon"}, {"at": 0.3, "event": "click bounces; the button stays unlit"}, {"at": 0.6, "event": "SubViewportContainer wraps the square"}, {"at": 0.82, "event": "click passes in; the button lights"}],
      "ShaderLab", "A click that bounces, then passes, is the limit and its fix as motion.",
      evidence="run-6 X5 (standalone false, container true) · docs SubViewport note")
lab("B40", 3, "the picture goes anywhere a texture goes: a sprite, an interface panel, a 3D plane, a shader's sampler", "subviewports/c20-four-places.mp4", f"{FWD} · scripted: the blob turns, the 3D plane sways",
    "Four real panels in a row showing one live picture (a cream card with the turning gradient blob): a Sprite2D, a panel in the interface (a TextureRect inside a teal-bordered panel), a flat plane in a 3D scene (swaying about its vertical axis, rendered by its own 3D viewport), and a plain rectangle whose own shader reads the picture through a sampler uniform. Readouts name each place as the voice does.",
    "The same turning blob appears in all four places at once; the 3D plane sways.",
    [{"at": 0.3, "event": "sprite named"}, {"at": 0.42, "event": "interface panel named"}, {"at": 0.58, "event": "3D plane named"}, {"at": 0.74, "event": "shader sampler named"}],
    "manim: four icons receiving one picture", "One picture alive in four places at once is the claim; a drawing could not show that they all really work.",
    "C20 (scene c20): one 280 px opaque viewport (cream card, gradient blob turning at 0.7 rad/s) shown by a Sprite2D at (40, 220), a TextureRect in a PanelContainer at (332, 212), a flat QuadMesh with an unshaded StandardMaterial3D in a 280 px transparent 3D viewport shown as a Sprite2D at (640, 220), and a ColorRect at (940, 220) whose shader reads the picture through `uniform sampler2D picture`; @LEN:c20@ s, Forward+. Verified (run-7c) at 0 s: gold is below the centre in all four panels (red 0.773 below, 0.533 above in the flat ones; 0.792 / 0.510 in the 3D plane).",
    "C20 · verify7 c20 (run-7c)",
    readouts=[{"at": 0.3, "text": "sprite", "x": 0.14, "y": 0.93}, {"at": 0.42, "text": "interface panel", "x": 0.37, "y": 0.93}, {"at": 0.58, "text": "3D plane", "x": 0.62, "y": 0.93}, {"at": 0.74, "text": "shader sampler", "x": 0.86, "y": 0.93}])

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
(HERE / "lanes").mkdir(exist_ok=True)
ACT_COUNT = max(e["act"] for e in E) + 1
for ai in range(ACT_COUNT):
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
sl = ["# Shot list: SubViewports\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a capture of one verified scene from `evidence/planning-checks/capture_scene.gd` or a real editor frame of the scratch project; every shader shown is a tested file in `lab-shaders/`. Seven things must exist or be recorded first (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`; this film uses `layout` side and video, cue `label`, `readouts`, `rings`, `ramp`, `caption`, a PNG still). 2. **`shader_kit.py`** Manim helpers (same file: ramp strip, plot, UV square, vertex quad, code card). "
      "3. **Capture harness** (same file; the scene-script route, with the adapter this film's CAPTURE-PLAN describes: all 21 scenes on the SubViewport native-size route, window kept on top, one frame of pre-roll). 4. **New Manim kit objects this film needs** (build them into `shader_kit.py` and list them in `BUILD-LOG.md`): `viewport_box(label)`, `picture_card`, `blob_sprite`, `screen_frame`, `shader_tag(text)`, `hue_wheel`, `plateau_plot`, `mesh_grid(n)`, `cursor_arrow`. "
      "5. **Editor frames E1, E2, E2b, E4, E4b, E4c/E4d** (the scratch project and driver plugin are in `evidence/planning-checks/editor-scratch/`; CAPTURE-PLAN section E). 6. **Capture scenes C01 to C21** (CAPTURE-PLAN). 7. **ffmpeg** to cut each capture's PNG sequence to an MP4 and to join frames into `e1-setup.mp4` and `e4-materials.mp4`.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
