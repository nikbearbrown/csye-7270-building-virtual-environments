#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text (lab-shaders/), the cue times must follow the narration, and
the shot list must say exactly what the lanes say. Re-run after any edit:
    python3 _gen_lanes.py && python3 make_sheet.py
Cue times (`at`) come from `at(bid, phrase)`: the fraction of the beat's words that come before the phrase, nudged out of the
45 to 55 percent window (no cue may start there: the midpoint frame must be a settled still). They are estimates until the audio is
measured; the build session may nudge them but must keep them out of that window.
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
TEXT = {bid: t for bid, _, t in N.BODY}
SH = HERE / "lab-shaders"
E = []            # entries in beat order
V = "shaders-in-3d/"   # folder under runtime/remotion/public/ for this film's captures


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def at(bid, phrase, lag=0.02):
    """Fraction of the beat at which `phrase` starts, estimated from word counts, kept out of the 45-55 % window."""
    t = TEXT[bid]
    i = t.lower().find(phrase.lower())
    assert i >= 0, f"{bid}: phrase {phrase!r} not in narration"
    f = round(len(t[:i].split()) / max(1, len(t.split())) + lag, 2)
    if 0.45 <= f <= 0.55:
        f = 0.44 if f < 0.5 else 0.56
    return round(min(max(f, 0.04), 0.94), 2)


def add(bid, act, about, entry, evidence=""):
    entry["show"] = sorted(entry["show"], key=lambda x: x["at"])
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects)", sparse_reason=None):
    ent = {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
           "show": show, "runner_up": runner, "why": why, "sparse": True}
    if sparse_reason:
        ent["sparse_reason"] = sparse_reason
    add(bid, act, about, ent, evidence)


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


FP = "Godot 4.7.2 · Forward+"

# ═════════════════════════════ ACT I · Same Shape, New Names ═════════════════════════════
lab("B01", 0, "the hook: the pad shader charging a flat square, ten lines", "12-signal-pad.gdshader", V + "pad-angled-sweep.mp4",
    FP + " · the shader on a flat square · scripted sweep", [],
    "Act title 'Same Shape, New Names' (serif 40) top-left. Left: the ten-line pad shader on a cream code card, no line focus. Right: a framed window holding a real Godot render of a flat square lying flat, seen from the game's camera angle, charging from striped rust-brown to flat green as activation climbs. Caption: 'a shader from a small game'.",
    "The square charges from striped rust to flat green while its ten lines of code sit beside it.",
    [{"at": 0.0, "event": "striped rust square, code card beside it"}, {"at": 0.5, "event": "half charged: greener, stripes fading"}, {"at": 0.9, "event": "flat green"}],
    "manim drawing of a pad charging", "A real render is the honest picture of the payoff, and the viewer sees the whole effect and its whole source at once; a drawing would only claim it.",
    "C01: custom scene 'pad on a flat square' (CAPTURE-PLAN S1): lab-shaders/12-signal-pad.gdshader on a 1.55 x 1.55 QuadMesh lying flat, orthographic camera size 2.6 from (5.8, 9, 11) toward the origin, activation 0 to 1 across 0 to 0.86 of the clip then held at 1 (the clip is as long as the longer of its two beats), 30 fps, Forward+, stage #D9D5CA. Frame at the 50 % mark reads activation 0.5 (mid-tone), at 85 % reads 0.85.",
    "Lab pad shader, probes at five activations (lab-results.jsonl)", title="Same Shape, New Names", caption="a shader from a small game")

manim("B02", 0, "what a shader is; the shape every drawing shader has", "Anatomy",
      "The compiled skeleton file lab-shaders/03-skeleton-3d.gdshader drawn as a cream code card (Menlo, 12 lines). Brackets draw in on the voice's words and each carries a one-word label: 'a first line' brackets line 1 (label 'type'), 'up to three functions' brackets lines 5 to 12, the three empty functions (label 'functions'), 'dials' brackets line 3 where a small dial (a circle with a turning tick) sits at the card's right (label 'dials'). Caption at the top, GLOSSARY wording: 'shader: a small program the graphics card runs to decide how something is drawn'.",
      "A dot steps down the lines like a program, then three brackets draw in one after another, each with its label, and a small dial turns.",
      [{"at": 0.0, "event": "card and shader caption; a terracotta dot steps down the lines like a program counter"}, {"at": at("B02", "a first line"), "event": "bracket 1: type"}, {"at": at("B02", "up to three functions"), "event": "bracket 2: functions"}, {"at": at("B02", "dials your game"), "event": "bracket 3 and the turning dial"}],
      "LectureCodeTrace on the skeleton", "Brackets growing around real code show the SHAPE (the parts and their order), which paced line focus alone cannot.")
manim("B03", 0, "the first line names the type: canvas_item or spatial", "TwoTypes",
      "The line `shader_type canvas_item;` in Menlo over a flat teal square (outline icon). On the cue the word canvas_item slides out and spatial slides in, while the flat square turns into an isometric cube in the same teal with faint triangle edges; a one-word label 'mesh' points at the cube. Caption, GLOSSARY wording: 'shader type: the first line; says what the shader is for'.",
      "The word canvas_item is replaced by spatial and the flat square turns into a cube.",
      [{"at": 0.0, "event": "first line over the flat square"}, {"at": 0.56, "event": "spatial replaces canvas_item; square becomes a cube (starts after the midpoint, so the 50 % frame is the settled first line over the flat square)"}, {"at": at("B03", "mesh"), "event": "'mesh' label on the cube"}],
      "LectureEvidenceTable", "Two worlds, each with its own first line, is the contrast the sentence names; a replaced word plus a square that becomes a cube says it with motion.")
manim("B04", 0, "vertex once per vertex, fragment once per pixel, light once per lamp", "ThreeFunctions",
      "Left: the test rectangle (a flat square) with four terracotta corner dots. Right: a 12-by-8 pixel grid of outline cells with the square's footprint over it. The four dots flash in order with a counter 1 to 4 and the label 'vertex()'; the covered cells tint one by one, each with a tiny 'fragment()' tag, then all hold; a small lamp icon (drawn bulb with rays) appears and the covered cells brighten once per lamp, two lamps in turn, with the label 'light()'. Captions, GLOSSARY wording: 'vertex: a corner point of a shape' and 'pixel: one dot of the picture on screen'.",
      "Four dots flash in turn, then the covered cells tint one by one, then the cells brighten once for each lamp.",
      [{"at": 0.0, "event": "square with four dots; both captions"}, {"at": at("B04", "Vertex runs"), "event": "dots flash 1 to 4"}, {"at": at("B04", "Fragment runs"), "event": "covered cells tint one by one"}, {"at": at("B04", "Light runs"), "event": "lamp 1 then lamp 2 brighten the cells"}],
      "LectureCodeTrace on the skeleton", "'Once for each vertex', 'once for each pixel' and 'once per light' are counts; four dots, a tinting grid and two lamps are those counts as motion.",
      "verify1-mesh-uv.gd (a QuadMesh has four vertices); Godot 4.7 docs, introduction")
manim("B05", 0, "the output changes: COLOR (four numbers) becomes ALBEDO (three)", "CodeMorph",
      "Two code cards, lab-shaders/01-flat-teal-2d.gdshader at left and lab-shaders/02-flat-teal-3d.gdshader at right (Menlo, 5 lines each), the same positions line for line. The first lines already differ (canvas_item and spatial: label 'type', the idea of the previous beat). On the cues the changed pieces get a terracotta ring in turn: 'COLOR' becomes 'ALBEDO' as the voice says 'the output' (label 'output'); a short ring goes round the four numbers of the two-D color as the voice says 'four numbers'; as it says 'and alpha' the ring moves to the last number, 1.0, and a caption lands, GLOSSARY wording: 'alpha: how visible a pixel is: 0 invisible, 1 solid'; as it says 'three numbers' 'vec4(' becomes 'vec3(' and ', 1.0' dissolves (label 'three numbers'); as it says 'Alpha becomes a separate output' a small 'ALPHA' chip appears beside the card. The unchanged text stays still.",
      "The output and the number of numbers change in turn while everything else stays exactly where it was.",
      [{"at": 0.0, "event": "both cards side by side; the first lines differ (label 'type')"}, {"at": at("B05", "The output"), "event": "COLOR becomes ALBEDO; label 'output'"}, {"at": at("B05", "four numbers"), "event": "a short ring round the four numbers of the two-D color (done by 0.44)"}, {"at": at("B05", "and alpha"), "event": "the ring moves to the last number, 1.0; the alpha caption lands"}, {"at": at("B05", "three numbers"), "event": "vec4 becomes vec3 and ', 1.0' dissolves; label 'three numbers'"}, {"at": at("B05", "Alpha becomes"), "event": "an 'ALPHA' chip appears beside the card: alpha is its own output"}],
      "ShaderLab", "Most of the two programs is identical; a morph that moves only three tokens is the claim 'same shape, new names' made visible.")
rem("B06", 0, "the two real compile errors a mix-up produces", "CCPlainShell",
    {"title": "Godot 4.7.2 · what the compiler says", "fontSize": 32, "windowMargin": 48,
     "lines": ["# COLOR = vec4(0.37, 0.64, 0.57, 1.0);", "SHADER ERROR: Constants cannot be modified.", "ERROR: Shader compilation failed.", "",
               "# ALBEDO = vec4(0.37, 0.64, 0.57, 1.0);", "SHADER ERROR: Invalid arguments to operator '=': 'vec3, vec4'.", "ERROR: Shader compilation failed."],
     "lineCues": [6, 54, 66, 80, 150, 190, 202], "rings": [{"line": 1, "cue": 70}, {"line": 5, "cue": 205}], "durationSeconds": "__AUDIO__"},
    "A plain terminal window (CCPlainShell, 32 pt) with two real runs, verbatim from the Lab's log. Each run is a comment line with the line that was wrong, then the compiler's two output lines. A terracotta ring (grey-backed) rings each 'SHADER ERROR' line as the voice reads the message. Title: 'Godot 4.7.2 · what the compiler says'. Line cues are frames at 24 fps and are approximate: re-time them to the measured audio.",
    "Each wrong line lands, then the compiler's reply appears under it and is ringed.",
    [{"at": 0.0, "event": "first wrong line"}, {"at": at("B06", "constants cannot"), "event": "first error ringed"}, {"at": at("B06", "Give albedo four"), "event": "second wrong line and its error"}],
    "LectureCodeTrace with the message as its note", "Real command-line output plays on CCPlainShell, verbatim (SHOW-THE-THING rung 1); two separate runs are labelled as such by their comment lines.",
    "evidence/planning-checks/lab-results.jsonl, checks 04 and 05 (exit 1 on purpose)")
lab("B07", 0, "a two-D shader on a three-D mesh is silently ignored", "18-two-d-shader-on-a-mesh.gdshader", V + "wrong-type.mp4",
    FP + " · two flat squares · scripted hand-over", [{"at": at("B07", "Give a three-D mesh"), "lines": [1], "label": "canvas_item: shaders for 2D and UI"}],
    "A wide result strip (layout 'stack': result above, and under it a one-line excerpt, the two-D shader's first line `shader_type canvas_item;`, with a tag on that line: 'canvas_item: shaders for 2D and UI'). Real Godot render: two flat squares side by side, both plain grey at first. At the hand-over (0.12 of the clip, as the voice says 'Give a three-D mesh a two-D shader') each is given a red shader: the left one gets the canvas_item shader above, the right one a spatial shader that paints red. The right square turns red; the left stays exactly as it was. Labels land under them: 'canvas_item: ignored' and 'spatial: red'.",
    "Both squares are handed a red shader; only the right one changes.",
    [{"at": 0.0, "event": "two plain grey squares"}, {"at": at("B07", "Give a three-D mesh"), "event": "first line focused; the shaders are handed over; the right square turns red"}, {"at": at("B07", "It draws the mesh"), "event": "'canvas_item: ignored' label on the left square"}, {"at": at("B07", "check the first line"), "event": "'spatial: red' label on the right"}],
    "CCPlainShell showing an empty log", "A non-event is hard to show; two squares given the same instruction, one of which visibly does nothing, makes it visible, and the empty log is told in words.",
    "C18: custom scene 'wrong type' (CAPTURE-PLAN S6): two QuadMesh 1.4 x 1.4 at x -0.95 and +0.95 on the stage, no WorldEnvironment and no lamp (as verify8); both start with no material; at 0.12 of the clip the scene script gives the left lab-shaders/18-two-d-shader-on-a-mesh.gdshader and the right lab-shaders/19-three-d-shader-on-a-mesh.gdshader as material_override (--call-at); the clip is as long as the beat; orthographic size 2.6; Forward+. Verified: no engine error; left stays (0.612, 0.600, 0.569) (the no-material look), right reads (1.0, 0.0, 0.0).",
    "verify8-wrong-shader-type.gd (no error line; the 2D shader is ignored)", layout="stack",
    code="shader_type canvas_item;", code_file="lab-shaders/18-two-d-shader-on-a-mesh.gdshader (line 1 of 5)",
    readouts=[{"at": at("B07", "It draws the mesh"), "text": "canvas_item: ignored", "x": 0.29, "y": 0.9}, {"at": at("B07", "check the first line"), "text": "spatial: red", "x": 0.71, "y": 0.9}])
lab("B08", 0, "UV is the mesh's own address: three meshes, one shader", "06-uv-colors-3d.gdshader", V + "uv-meshes-turn.mp4",
    FP + " · one shader on three meshes · scripted swing", [{"at": at("B08", "Paint it as a color"), "lines": [1], "label": "red = UV.x (across), green = UV.y (down)"}],
    "A wide result strip (layout 'stack': result above, and under it a one-line excerpt: line 5 of the six-line shader, `ALBEDO = vec3(UV.x, UV.y, 0.0);`, with a tag 'red = UV.x (across), green = UV.y (down)'). Real Godot render: a flat square, a box and a sphere in a row, all swinging side to side about the vertical axis (plus or minus 50 degrees, one swing in eight seconds), every one painted with red-across, green-down address colors. The square shows the whole red-green gradient, the box shows a different patch on each face, the sphere wraps its map around itself. One-word labels land under them: 'square', 'box', 'sphere'. Caption, GLOSSARY wording: 'UV: a point's address on the shape: 0 to 1 across, 0 to 1 down'.",
    "The colors stay glued to each surface as the meshes swing, and each mesh shows a different map.",
    [{"at": 0.0, "event": "three meshes turning"}, {"at": at("B08", "Paint it as a color"), "event": "ALBEDO line highlighted"}, {"at": at("B08", "A square"), "event": "'square' label"}, {"at": at("B08", "a box"), "event": "'box' label"}, {"at": at("B08", "a sphere"), "event": "'sphere' label"}],
    "manim UV unwrap drawing", "Real renders show that UV is glued to the surface and differs per mesh; the swing is the proof, and a drawing could only illustrate it.",
    "C02: custom scene 'three meshes' (CAPTURE-PLAN S2): lab-shaders/06-uv-colors-3d.gdshader on QuadMesh 1x1 (x -1.35), BoxMesh 1x1x1 (x 0), SphereMesh r 0.5 (x +1.35); each swings about Y by plus or minus 50 deg (a sine, period 8 s) with a fixed -20 deg tilt about X (NOT a full turn: with default culling the flat square vanishes while its back faces the camera, verify9 run 9a); orthographic size 2.6; the clip is as long as the beat; 30 fps; Forward+. Verified mesh data: quad UV (0,0) top-left; box 3 x 2 cells; sphere U wraps once.",
    "verify1-mesh-uv.gd (mesh arrays and rendered UV); verify9 (the picture at -50, 0, +50 degrees)", layout="stack",
    code="ALBEDO = vec3(UV.x, UV.y, 0.0);", code_file="lab-shaders/06-uv-colors-3d.gdshader (line 5 of 6)",
    readouts=[{"at": at("B08", "A square"), "text": "square", "x": 0.21, "y": 0.9}, {"at": at("B08", "a box"), "text": "box", "x": 0.5, "y": 0.9}, {"at": at("B08", "a sphere"), "text": "sphere", "x": 0.79, "y": 0.9}],
    caption="UV: a point's address on the shape: 0 to 1 across, 0 to 1 down")
manim("B09", 0, "how a shader gets onto a 3D node", "AttachChain",
      "Three boxes slide in left to right and link: a cube icon over 'mesh instance', then 'ShaderMaterial', then 'shader' (a small file icon marked .gdshader). The link between the first two carries a small tab 'material override'. A dot travels from the shader back to the mesh instance (meaning: look here). Captions: 'mesh instance: the node that draws a mesh' (docs: MeshInstance3D is the main node that draws a mesh) and, GLOSSARY wording, 'ShaderMaterial: a material that holds your shader and its settings'.",
      "Each box slides in as it is named, the slot tab lands on the first link, and the dot travels back to the node.",
      [{"at": 0.0, "event": "mesh instance box"}, {"at": at("B09", "a shader material"), "event": "ShaderMaterial box slides in and links"}, {"at": at("B09", "material override"), "event": "'material override' tab lands on the link"}, {"at": at("B09", "The material holds"), "event": "shader box; dot travels back to the node"}],
      "a real editor frame of the MeshInstance3D Inspector (not recorded)", "Three nested things is a structure with a shape, and a drawn chain with a travelling dot shows it without claiming an Inspector label or layout this film did not capture; the property name material_override is run-verified, and a real frame is the labelled upgrade if an editor driver exists.",
      "verify3-attach-set-tween.gd (ATTACH); Godot 4.7 docs, GeometryInstance3D.material_override")
lab("B10", 0, "one flat albedo on a sphere is not flat: Godot lit it", "02-flat-teal-3d.gdshader", V + "lamp-0.mp4",
    FP + " · one lamp · scripted lamp switch", [{"at": at("B10", "one-line albedo"), "lines": [4]}],
    "Left: the five-line shader (ALBEDO = vec3(0.37, 0.64, 0.57)) with its ALBEDO line focused. Right: a real Godot render of one teal sphere, centred. At first the lamp is off and the sphere is a flat dim disc (the 'flat teal disc' the voice says you might expect). At the reveal the lamp switches on, from the upper left: bright on one side, dim on the other, and it stays that way. Labels land on the sphere: 'bright', then 'dim'; a 'lamp' tag lands in the upper left as the voice names the scene's lamp.",
    "A flat dim disc becomes a sphere with a bright side and a dim side the moment the lamp switches on, although the code names one flat color.",
    [{"at": 0.0, "event": "ALBEDO line focused; the sphere is a flat dim disc (lamp off)"}, {"at": at("B10", "one side is bright"), "event": "lamp switches on at yaw -65 degrees; 'bright' label"}, {"at": at("B10", "one is dim"), "event": "'dim' label"}, {"at": at("B10", "scene's lamp"), "event": "'lamp' tag in the upper left"}],
    "manim sphere with shading", "A real render makes the surprise honest: nothing in the code says 'shade', and the sphere is shaded.",
    "C03a: custom scene 'lamp' (CAPTURE-PLAN S3), one sphere: lab-shaders/02-flat-teal-3d.gdshader on a SphereMesh r 0.5 at the origin, orthographic size 1.8; white ambient light energy 0.25; one DirectionalLight3D tilted 30 deg down at yaw -65 deg, switched off until 0.56 of the clip and on from then (scripted switch, held there); Forward+. Verified: lamp off, the sphere reads one dim value everywhere (0.337, 0.435, 0.412); lamp on at -65 deg, the left side reads about 0.65 to 0.68 red and the right 0.337 (verify4, verify10).",
    "verify4-lamp.gd (lamp off 0.34, in front 0.68); verify10-lamp-start.gd (-65 degrees: bright left, dim right)",
    readouts=[{"at": at("B10", "one side is bright"), "text": "bright", "x": 0.42, "y": 0.4}, {"at": at("B10", "one is dim"), "text": "dim", "x": 0.58, "y": 0.62}, {"at": at("B10", "scene's lamp"), "text": "lamp", "x": 0.26, "y": 0.24}])

# ═════════════════════════════ ACT II · Lit or Unlit ═════════════════════════════
lab("B11", 1, "the same albedo, a moving lamp: the pixel changes, the albedo does not", "02-flat-teal-3d.gdshader", V + "lamp-1.mp4",
    FP + " · scripted lamp", [{"at": at("B11", "The albedo never changes"), "lines": [4]}],
    "Act title 'Lit or Unlit' (serif 40) top-left. Left: the same five-line shader, ALBEDO line focused. Right: the real lit sphere while a lamp swings once around it: the bright patch travels around the sphere and the dim side follows. Labels: 'same albedo' (while the lamp moves), then 'new pixel'.",
    "The bright patch travels around the sphere while the code stays put.",
    [{"at": 0.0, "event": "lamp starts to turn"}, {"at": at("B11", "The albedo never changes"), "event": "ALBEDO line focused; 'same albedo'"}, {"at": at("B11", "The lighting does"), "event": "'new pixel' label"}],
    "manim sphere with a lamp icon", "The lamp's turn against fixed code is the claim 'the color you write is a starting point'; only a real render shows it with true shading.",
    "C03: custom scene 'lamp' (CAPTURE-PLAN S3), one sphere as C03a but the lamp is on throughout and turns: yaw = -65 deg + 360 deg over 14 s at its own pace (scripted), so the clip opens on the pose B10 ended on; the clip is as long as the beat; Forward+. Half-lit at yaw 90 and 270, dim with the lamp behind.", "verify4-lamp.gd (four lamp yaws, two renderers)",
    title="Lit or Unlit",
    readouts=[{"at": at("B11", "The albedo never changes"), "text": "same albedo", "x": 0.5, "y": 0.88}, {"at": at("B11", "The lighting does"), "text": "new pixel", "x": 0.5, "y": 0.88}])
rem("B12", 1, "the surface outputs fragment sets in 3D", "LectureEvidenceTable",
    {"title": "What fragment sets in 3D", "headers": ["Output", "What it sets"],
     "rows": [["ALBEDO", "its base color"], ["ALPHA", "how visible: 0 invisible, 1 solid"], ["EMISSION", "light it gives off"], ["ROUGHNESS, METALLIC", "its finish"]],
     "note": "Godot 4.7 spatial shader reference · fragment built-ins", "cues": [at("B12", "Albedo is"), at("B12", "Alpha is"), at("B12", "Emission is"), at("B12", "Roughness and")], "durationSeconds": "__AUDIO__"},
    "A four-row table on the cream stage, one row ringed as each output is named: ALBEDO, ALPHA, EMISSION and ROUGHNESS with METALLIC (the last two share a row), each with a short plain meaning. The note names the docs page.",
    "The ring steps down the four rows with the voice.",
    [{"at": at("B12", "Albedo is"), "event": "ALBEDO row"}, {"at": at("B12", "Alpha is"), "event": "ALPHA row"}, {"at": at("B12", "Emission is"), "event": "EMISSION row"}, {"at": at("B12", "Roughness and"), "event": "ROUGHNESS and METALLIC row"}],
    "four spheres, one output changing on each", "A table of kinds is the right shape for five parallel names; the sphere row was tried and METALLIC = 1 reads near-black without an environment to reflect, which would teach the wrong thing (verify6-outputs.gd).",
    "verify6-outputs.gd; Godot 4.7 docs, spatial shaders (fragment built-ins)")
manim("B13", 1, "you describe the surface, Godot's lighting does the rest", "LitPipeline",
      "A left-to-right flow on the cream stage. A box 'fragment()' emits a small card of five monospace chips (ALBEDO, ALPHA, EMISSION, ROUGHNESS, METALLIC) labelled 'surface'. The card travels into a box 'Godot's lighting'. Two lamp icons drop beams into the same box from above. A single teal pixel (a small outlined square) comes out on the right. All arrows are drawn shapes that point only forward.",
      "A surface card enters Godot's lighting, two lamps feed it from above, and one pixel comes out.",
      [{"at": 0.0, "event": "fragment() box and its surface card"}, {"at": at("B13", "Then Godot's own"), "event": "card enters the lighting box; lamps feed it"}, {"at": at("B13", "You describe"), "event": "pixel appears"}],
      "DesignPipelineClaim, show-tell isometric", "A flow of work with a token moving forward through named stages is what a Manim flow shows best, and the two lamps joining the card are the 'every lamp' of the sentence.",
      "Godot 4.7 docs: 'set the proper parameters'; verify4-lamp.gd")
lab("B14", 1, "render_mode unshaded: the lamp is ignored", "07-flat-teal-3d-unshaded.gdshader", V + "lamp-2.mp4",
    FP + " · the same lamp · scripted lamp", [{"at": at("B14", "Add a second line"), "lines": [2], "label": "render mode: alters the way Godot applies the shader"}],
    "Left: the six-line shader with line 2, `render_mode unshaded;`, focused and tagged (docs wording: 'render mode: alters the way Godot applies the shader'). Right: a real render of two spheres under the same turning lamp: the lit one on the left keeps changing, the unshaded one beside it stays one flat teal. Labels: 'lit', 'unshaded'.",
    "One sphere keeps changing as the lamp turns; the one beside it never changes.",
    [{"at": 0.0, "event": "two spheres, lamp turning"}, {"at": at("B14", "Add a second line"), "event": "line 2 focused"}, {"at": at("B14", "Add a second line"), "event": "'unshaded' label on the flat sphere"}, {"at": at("B14", "Watch the lit"), "event": "'lit' label"}],
    "LectureCodeTrace", "The flat sphere beside the changing one is the whole meaning of 'the lamp is ignored'.",
    "C04: custom scene 'lamp' (S3), two spheres: lit 02-flat-teal-3d at x -0.7 and unshaded 07-flat-teal-3d-unshaded at x +0.7, orthographic size 2.4, same lamp turn, 14 s, Forward+.",
    "verify4-lamp.gd (unshaded centre 0.643 / 0.82 / 0.78 at every lamp yaw)",
    readouts=[{"at": at("B14", "Add a second line"), "text": "unshaded", "x": 0.66, "y": 0.8}, {"at": at("B14", "Watch the lit"), "text": "lit", "x": 0.34, "y": 0.8}])
rem("B15", 1, "the docs say unshaded is just albedo and faster", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html#render-modes",
     "image": V + "docs-render-modes.png", "caption": "Godot 4.7 documentation · Spatial shaders · Render modes · captured YYYY-MM-DD", "frame": "browser",
     "moves": [{"at": 0, "x": 0.5, "y": 0.5, "scale": 1}, {"at": 0.22, "x": 0.5, "y": 0.5, "scale": 1.7, "ring": [0.08, 0.46, 0.84, 0.07]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 'Spatial shaders' page, Render modes table, in a browser window; the camera pushes in on the row for unshaded ('Result is just albedo. No lighting/shading happens in material, making it faster to render.') and one terracotta ring marks it. The ring box is an estimate: recompute it from the real capture.",
    "The camera pushes in on the unshaded row the voice is describing.",
    [{"at": 0.0, "event": "the render modes table"}, {"at": 0.2, "event": "push-in and ring on the unshaded row"}, {"at": at("B15", "Godot's docs add"), "event": "the ring stays while the voice quotes 'faster to render'"}],
    "manim: the sentence with the word unshaded highlighted", "A docs claim is best shown by the docs themselves (SHOW-THE-THING); the faster-to-render sentence is theirs, not measured here.",
    "D1: Playwright capture of the live docs page at #render-modes, row 'unshaded' scrolled to mid-window, 1600x900 at 2.4x (CAPTURE-PLAN)")
lab("B16", 1, "writing light() yourself replaces Godot's lighting; an empty one silences the lamp", "08-flat-teal-3d-empty-light.gdshader", V + "lamp-3.mp4",
    FP + " · the same lamp · scripted lamp", [{"at": at("B16", "You can write"), "lines": [7, 8], "label": "light(): runs once per pixel for each light that touches it"}, {"at": at("B16", "replaces Godot's lighting"), "lines": [7, 8], "label": "replaces the default lighting, even when empty"}],
    "Left: the eight-line shader with its empty `void light() { }` focused and tagged (GLOSSARY wording: 'light(): runs once per pixel for each light that touches it', then 'replaces the default lighting, even when empty'). Right: a real render of three spheres under the same turning lamp: lit (changing), unshaded (flat) and the one with the empty light() function: it stays dim and flat, ignoring the lamp. Labels: 'lit', 'unshaded', 'own light()'.",
    "The third sphere stays dim however the lamp turns.",
    [{"at": 0.0, "event": "three spheres, lamp turning"}, {"at": at("B16", "You can write"), "event": "light() lines focused; first tag"}, {"at": at("B16", "replaces Godot's lighting"), "event": "second tag"}, {"at": at("B16", "An empty one"), "event": "'own light()' label on the third sphere"}],
    "LectureCodeTrace", "A sphere that ignores a moving lamp is the trap, shown; the sentence alone would not convince.",
    "C05: custom scene 'lamp' (S3), three spheres at x -1.15 / 0 / +1.15: 02-flat-teal-3d, 07-flat-teal-3d-unshaded, 08-flat-teal-3d-empty-light; orthographic size 2.8; same lamp turn; the clip is as long as the beat; Forward+. Verified: the empty-light sphere reads the same dim value as the lit sphere with the lamp off.",
    "verify4-lamp.gd (empty-light 0.337 / 0.435 / 0.412 at every yaw)",
    readouts=[{"at": 0.04, "text": "lit", "x": 0.27, "y": 0.8}, {"at": 0.1, "text": "unshaded", "x": 0.5, "y": 0.8}, {"at": at("B16", "An empty one"), "text": "own light()", "x": 0.73, "y": 0.8}])
lab("B17", 1, "back faces are not drawn by default; cull_disabled draws both", "09-two-sided.gdshader", V + "turnaround.mp4",
    FP + " · two flat squares · scripted turn", [{"at": at("B17", "Add cull disabled"), "lines": [2], "label": "cull_disabled: draw both sides of a surface"}],
    "Left: the six-line shader with `render_mode unshaded, cull_disabled;` focused and tagged 'cull_disabled: draw both sides of a surface'. Right: a real render of two flat teal squares turning once about the vertical axis: the left one (default culling) blinks out while its back faces the camera, the right one (cull disabled) is always there. Labels: 'default', 'cull disabled'.",
    "The left square vanishes while its back faces the camera; the right square never does.",
    [{"at": 0.0, "event": "both squares turning"}, {"at": at("B17", "Turn a flat square"), "event": "the left square vanishes from behind"}, {"at": at("B17", "Add cull disabled"), "event": "render_mode line focused; right square stays"}],
    "manim quad flipping", "A square that disappears and one that does not, turning side by side, is the claim; the shader line then explains it.",
    "C06: custom scene 'turnaround' (S4): two QuadMesh 1.2 x 1.2 at x -0.85 (07-flat-teal-3d-unshaded) and x +0.85 (09-two-sided), both turning about Y from 0 to 360 deg across the first 0.8 of the clip, then held at 360 deg (scripted; 225 deg at the 50 % mark, about 310 deg at the cull_disabled cue, front-facing at 85 %), orthographic size 2.4, camera at z = 5, Forward+. Verified: default shows the stage colour at yaw 120, 180, 240.",
    "verify5-cull-turnaround.gd (default culling vanishes at yaw 120 to 240; cull_disabled never)",
    readouts=[{"at": at("B17", "A three-D surface"), "text": "default", "x": 0.3, "y": 0.8}, {"at": at("B17", "Add cull disabled"), "text": "cull disabled", "x": 0.7, "y": 0.8}])
manim("B18", 1, "two questions to ask of a wrong-looking 3D shader", "TwoChecks",
      "A small decision sketch. At the top a teal square labelled 'looks wrong'. Two branches go down. Left: a lamp icon with a question mark leads to a shaded sphere that turns flat, tagged 'add unshaded'. Right: a flat square seen from behind (empty outline) leads to the same square filled, tagged 'add cull disabled'. A dot travels down each branch in turn; a third tag 'blend add' appears faint at the side with the caption 'more modes in the docs'.",
      "A dot travels down each branch and lights its remedy tag.",
      [{"at": 0.0, "event": "looks wrong"}, {"at": at("B18", "Is a lamp"), "event": "left branch: lamp, then unshaded"}, {"at": at("B18", "Is the back side"), "event": "right branch: back side, then cull disabled"}, {"at": at("B18", "Godot's docs list"), "event": "faint 'blend add' tag"}],
      "LectureEvidenceTable", "Two questions with their one-word remedies are a gate with two exits; a travelling dot walks the viewer through both.",
      "verify4-lamp.gd; verify5-cull-turnaround.gd; lab-shaders/17-more-render-modes.gdshader compiles")

# ═════════════════════════════ ACT III · A Surface That Changes ═════════════════════════════
lab("B19", 2, "the address as a color on a flat square", "06-uv-colors-3d.gdshader", V + "uv-colors-quad.png", FP + " · the shader on the left",
    [{"at": at("B19", "address as a color"), "lines": [5]}],
    "Act title 'A Surface That Changes' (serif 40) top-left. Left: the six-line UV-colors shader with its ALBEDO line focused. Right: a real Godot render of a flat square, red across and green down. Corner labels land in the order the voice says them: 'dark' (top left), 'red' (top right), 'green' (bottom left), 'yellow' (bottom right).",
    "The four corner labels land on the corners in the order the voice names them.",
    [{"at": 0.0, "event": "ALBEDO line focused"}, {"at": at("B19", "dark,"), "event": "'dark' top left"}, {"at": at("B19", "red,"), "event": "'red' top right"}, {"at": at("B19", "green"), "event": "'green' bottom left"}, {"at": at("B19", "yellow"), "event": "'yellow' bottom right"}],
    "manim uv_square from the kit", "The picture itself is the evidence that the address became a color, and the corners prove the orientation (top left is zero, zero).",
    "C07: scene S5 face-on square (QuadMesh 1.8 x 1.8, orthographic size 2.0 at z = 3; the square fills 90 % of the frame height and the middle 51 % of its width), lab-shaders/06-uv-colors-3d.gdshader, still PNG 3840 x 2160, Forward+. (The Lab's own quad3d fills the whole 16:9 frame: a wide rectangle, not the square the voice says.) Corner probes (0.02/0.98 of the quad): dark (0.149, 0.157, 0), red (0.992, 0.157, 0), green (0.149, 0.988, 0), yellow (0.992, 0.988, 0).",
    "Lab probes 06-uv-colors-3d; verify1 (corners decode to 0.011 and 0.991)", title="A Surface That Changes",
    readouts=[{"at": at("B19", "dark,"), "text": "dark", "x": 0.3, "y": 0.12}, {"at": at("B19", "red,"), "text": "red", "x": 0.7, "y": 0.12}, {"at": at("B19", "green"), "text": "green", "x": 0.3, "y": 0.88}, {"at": at("B19", "yellow"), "text": "yellow", "x": 0.7, "y": 0.88}])
manim("B20", 2, "x is a ramp: a smooth run from 0 up to 1", "Ramp",
      "The kit's uv_square (0 to 1 axes, the second axis pointing DOWN) at left, small. Its x axis lights up. Beneath the square a ramp strip in greys grows from the left edge (end labels '0' and '1'); a terracotta dot crosses the square from left to right and a marker rides the strip in step. Caption, GLOSSARY wording: 'ramp: a smooth run of values from 0 up to 1'. Greys only, no near-black field.",
      "A dot crosses the square and its x value rides the strip from 0 to 1.",
      [{"at": 0.0, "event": "uv square, x axis lit"}, {"at": at("B20", "It is a ramp"), "event": "ramp strip grows; marker rides; caption (the ride is done by 0.44)"}, {"at": at("B20", "Everything that follows"), "event": "strip stays as the base of the next beats"}],
      "ShaderLab ramp strip", "The ramp is the series' signature object; a marker riding a strip as a dot crosses the square ties 'x' to 'a smooth run' in one motion.")
manim("B21", 2, "multiply by eight, then fract: eight ramps in a row", "FractRamp",
      "Three stacked strips on the cream stage: 'x' (the ramp, 0 to 1, greys), 'x × 8' (the same strip relabelled 0 to 8 with eight tick marks) and 'fract(x × 8)' drawn as a sawtooth plot with eight teeth, settled by 0.45, with a terracotta dot waiting at its start until 0.56 and then travelling along it, snapping back to zero at every whole number; under the plot, a strip of eight repeated grey ramps. Caption, GLOSSARY wording: 'fract(x): the part after the point: x minus floor(x)', and under it the one-line gloss of the word it uses, GLOSSARY wording: 'floor(x): rounds down to the whole number below'. Double the space at the fused boundary of 'x × 8' and look at the still.",
      "The strip stretches to eight, then the dot traces a sawtooth with eight teeth.",
      [{"at": 0.0, "event": "strip x"}, {"at": at("B21", "Multiply x by eight"), "event": "strip becomes 0 to 8"}, {"at": at("B21", "Fract keeps"), "event": "sawtooth plot draws in (settled by 0.45), the dot waits at its start; captions"}, {"at": 0.56, "event": "the dot travels along the sawtooth, snapping back to zero eight times (as the voice says 'starts over at zero at every whole number')"}, {"at": at("B21", "eight ramps in a row"), "event": "eight repeated ramps strip"}],
      "plot() alone", "Stretch, then restart at every whole number, is a transformation of one strip into another; the sawtooth with a travelling dot shows it.",
      "docs: fract = x - floor(x); evidence/planning-checks/analyze-bands.txt (8 periods; the file's own word for a stripe is 'band')")
manim("B22", 2, "step turns the repeating ramp into on and off, eight times", "StepSwitch",
      "The sawtooth plot (eight teeth) with a horizontal threshold line at 0.5. Under it the output plot of step(0.5, ·): a square wave with eight high and eight low segments. A terracotta dot travels along the sawtooth; each time it crosses the threshold the lower plot flips and a small spark flashes. At the bottom, a strip in two greys (light and dark stripes) fills in as the dot passes. Caption (docs wording): 'step(edge, x): 0 below the edge, 1 from the edge up'.",
      "Every time the dot crosses the threshold the lower plot flips and a stripe appears.",
      [{"at": 0.0, "event": "sawtooth and threshold line"}, {"at": at("B22", "Step of point five"), "event": "lower plot appears; caption"}, {"at": at("B22", "Feed it"), "event": "dot travels; flips; stripe strip fills"}],
      "ShaderLab", "A threshold crossing that flips an output is the definition of step; the dot makes each crossing visible.",
      "docs: step(edge, x); evidence/planning-checks/analyze-bands.txt (8 dark + 8 light stripes)")
lab("B23", 2, "stripes from step and fract, on the real quad", "10-stripes-grey.gdshader", V + "stripes-grey.png", FP + " · the shader on the left",
    [{"at": 0.04, "lines": [5], "label": "step(edge, x): 0 below the edge, 1 from the edge up"}, {"at": at("B23", "fract of eight x"), "lines": [5], "label": "fract(x): the part after the point: x minus floor(x)"}, {"at": at("B23", "Scale that"), "lines": [6]}],
    "Left: the seven-line stripes shader, line 5 (the stripe) focused with a tag for step and then a tag for fract (GLOSSARY wording), then line 6 (ALBEDO) focused. Right: a real Godot render of the Lab's full-frame flat quad (a wide rectangle) with eight dark grey and eight light grey vertical stripes, a dark one first. Labels: '8 dark' and '8 light' land under the picture.",
    "The focus moves from the stripe line to the albedo line while the label counts land.",
    [{"at": 0.0, "event": "stripes visible"}, {"at": 0.04, "event": "stripe line focused; step tag"}, {"at": at("B23", "fract of eight x"), "event": "fract tag"}, {"at": at("B23", "Scale that"), "event": "albedo line focused"}, {"at": at("B23", "eight dark"), "event": "'8 dark' and '8 light' labels"}],
    "manim strip stack", "Code and its real result side by side, with the counts confirmed by a measured render.",
    "C08: Lab render, lab-shaders/10-stripes-grey.gdshader, still PNG 3840 x 2160, Forward+. Verified: 16 stripes, 8 dark and 8 light, dark first; dark centre (UV.x 0.03125) reads 0.584, light centre (0.09375) reads 0.953.",
    "analyze-bands.py (16 stripes); Lab probes 10-stripes-grey",
    readouts=[{"at": at("B23", "eight dark"), "text": "8 dark", "x": 0.3, "y": 0.9}, {"at": at("B23", "and eight light"), "text": "8 light", "x": 0.7, "y": 0.9}])
manim("B24", 2, "mix(a, b, t): a blend steered by a number", "MixLine",
      "Two strips: 't' (0 to 1) above, and 'mix(a, b, t)' below running from a = 0.2 to b = 0.8, each with a terracotta dot. The dot on t slides from 0 to 1 and the dot below slides from 0.2 to 0.8 in step; the end values 0.2 and 0.8 are labelled. Caption from the first frame, GLOSSARY wording: 'mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b'; a formula caption lands with the voice's 'Mix of a': 'a × (1 − t) + b × t'. Greys only. It is plain numbers on purpose: no colors, so no renderer is implied.",
      "The two dots slide together: t from 0 to 1, the blend from a to b.",
      [{"at": 0.0, "event": "both strips"}, {"at": at("B24", "At zero"), "event": "t dot slides; blend dot follows from 0.2 to 0.8 (the slide is done by 0.44)"}, {"at": at("B24", "Mix of a"), "event": "formula caption"}],
      "LectureEvidenceTable", "A weight sliding from 0 to 1 with a value sliding from a to b is mix in motion; the formula is the caption, not the picture.",
      "docs: mix = a * (1 - c) + b * c")
lab("B25", 2, "a uniform dial steers the mix of two colors", "11-mix-dial.gdshader", V + "mix-dial-sweep.mp4", FP + " · activation swept by script",
    [{"at": 0.04, "lines": [9]}, {"at": at("B25", "A uniform is"), "lines": [4]}, {"at": at("B25", "Now one number"), "lines": [9]}],
    "Left: the ten-line mix-dial shader: the ALBEDO = mix line focused on 'Give mix a dial', the activation uniform line focused while the uniform is defined (the caption carries the definition), then the mix line again on 'Now one number'. Right: a real render of the Lab's full-frame flat quad sweeping from rust to green as activation goes 0 to 1, with a thin 0 to 1 strip under it and a marker riding the value. Caption, GLOSSARY wording: 'uniform: a value your game sets from outside; every pixel sees the same one'.",
    "The surface slides from rust to green while a marker rides the 0 to 1 strip.",
    [{"at": 0.0, "event": "surface starts rust"}, {"at": 0.04, "event": "mix line focused"}, {"at": at("B25", "A uniform is"), "event": "uniform line focused"}, {"at": at("B25", "Now one number"), "event": "mix line focused again"}],
    "manim two colors and a slider", "A color that visibly follows one number is the whole point of a uniform, and the strip marker shows the number.",
    "C09: Lab-style render, lab-shaders/11-mix-dial.gdshader on quad3d, activation 0 to 1 across the whole clip (scripted sweep; the clip is as long as the beat), 30 fps, Forward+. Frame at 50 % reads activation 0.5 (0.298, 0.537, 0.380), at 85 % reads 0.85. Verified: a uniform is the same at every pixel (three probes equal).",
    "Lab probes 11-mix-dial (0, 0.5, 1; three probe points)", ramp={"at": 0.0, "from": 0, "to": 1, "period": "__AUDIO__"}, caption="uniform: a value your game sets from outside; every pixel sees the same one")
rem("B26", 2, "a hint tells Godot how to treat a uniform", "LectureEvidenceTable",
    {"title": "Hints: how Godot treats a uniform", "headers": ["Hint", "What it tells Godot"],
     "rows": [["hint_range(0.0, 1.0)", "keep this dial between 0 and 1, in the editor"], ["source_color", "this vec4 is a color"]],
     "note": "hint: the word after a colon that tells Godot how to treat a uniform · Godot 4.7 shading language reference", "cues": [at("B26", "Hint range"), at("B26", "Source color")], "durationSeconds": "__AUDIO__"},
    "A two-row table pairing each hint with what it tells Godot; the table's note line carries the GLOSSARY definition word for word: 'hint: the word after a colon that tells Godot how to treat a uniform', then the docs page. Each row lands on its words.",
    "Each row lands and is ringed on its words.",
    [{"at": at("B26", "Hint range"), "event": "hint_range row"}, {"at": at("B26", "Source color"), "event": "source_color row"}],
    "editor frames of the Inspector", "Two facts in two rows; no editor frame was recorded for this film, and the table claims only what the docs say (a hint tells Godot how to treat a uniform; a range hint shapes the editor), not how a widget looks.",
    "Godot 4.7 docs, shading language: uniform hints")
lab("B27", 2, "one line from the game turns the dial", None, V + "set-parameter.mp4", FP + " · scripted run · scripted call",
    [{"at": 0.34, "lines": [1], "label": "$Pad: the node named Pad, the pad's mesh instance"}],
    "Left: a one-line GDScript card, `$Pad.material_override.set_shader_parameter(\"activation\", 1.0)`. Right: a real render of the striped rust square that jumps to flat green the instant the highlighted call fires. The line is tagged '$Pad: the node named Pad, the pad's mesh instance'. Readout under the square: 'activation = 1'.",
    "The square jumps from striped rust to flat green when the highlighted line fires.",
    [{"at": 0.0, "event": "GDScript line shown; rust square"}, {"at": 0.34, "event": "line highlighted and tagged; the square turns green (the call fires at 0.34 of the clip)"}, {"at": at("B27", "capitals included"), "event": "readout 'activation = 1'"}],
    "LectureCodeTrace", "Cause (one line) and effect (the jump) together; the capture is scripted and says so.",
    "C10: scene 'set from code' (S5): lab-shaders/12-signal-pad.gdshader on a MeshInstance3D named Pad holding a QuadMesh 1.8 x 1.8, with a ShaderMaterial as its material_override; at 0.34 of the clip the scene script runs the shown line (activation 0 to 1; --call-at); the clip is as long as the beat; 30 fps; Forward+. The 50 % and 85 % frames are flat green.",
    "verify3-attach-set-tween.gd (SET and CASE)", code='$Pad.material_override.set_shader_parameter("activation", 1.0)',
    code_file="evidence/planning-checks/verify3-attach-set-tween.gd (the SET line)", readouts=[{"at": 0.62, "text": "activation = 1", "x": 0.5, "y": 0.9}])
lab("B28", 2, "tween the dial; the start value must be set first", None, V + "tween.mp4", FP + " · scripted run · scripted tween",
    [{"at": at("B28", "or tween it"), "lines": [2, 3]}, {"at": at("B28", "Set the starting"), "lines": [1], "label": "material: the pad's ShaderMaterial"}],
    "Left: a three-line GDScript card (set the start value, create the tween, tween the property). Right: a real render of the rust square that slides smoothly to green over two seconds. Caption, GLOSSARY wording: 'tween: Godot's way to change a value smoothly over time from GDScript'. Line 1 is tagged 'material: the pad's ShaderMaterial'; a readout 'set first' lands with it.",
    "The square slides smoothly to green while the tween lines are focused.",
    [{"at": 0.0, "event": "code card, rust square"}, {"at": at("B28", "or tween it"), "event": "tween lines focused; the slide runs (it starts at 0.19 of the clip and keeps its 2.0 s)"}, {"at": at("B28", "Set the starting"), "event": "start line focused"}, {"at": at("B28", "A tween cannot"), "event": "readout 'set first'"}],
    "ShaderLab stills", "A smooth slide is the claim 'the surface follows, every frame'; the failed run is told in words and kept in the evidence.",
    "C11: scene 'set from code' (S5): at 0.04 of the clip `set_shader_parameter(\"activation\", 0.0)`; at 0.19 the tween to 1.0 starts and keeps the 2.0 s the code shows (--set-at, --call-at); the clip is as long as the beat; Forward+. Verified (verify3 TWEEN): red 0.4 at the start, (0.298, 0.541, 0.384) about a second into the tween, flat green (0.122, 0.722, 0.522) at the end; a tween without the first line fails with 'The tweened property ... does not exist' (run 3b, kept).",
    "verify3-attach-set-tween.gd (TWEEN); verify3b (FAILS as expected, kept)",
    code='material.set_shader_parameter("activation", 0.0)\nvar tween := create_tween()\ntween.tween_property(material, "shader_parameter/activation", 1.0, 2.0)',
    code_file="evidence/planning-checks/verify3-attach-set-tween.gd (the TWEEN lines)", caption="tween: Godot's way to change a value smoothly over time from GDScript",
    readouts=[{"at": at("B28", "A tween cannot"), "text": "set first", "x": 0.5, "y": 0.9}])

# ═════════════════════════════ ACT IV · Read a Real One ═════════════════════════════
PAD = "12-signal-pad.gdshader"
lab("B29", 3, "the whole pad shader again, while it charges", PAD, V + "pad-angled-sweep.mp4", FP + " · the shader on a flat square · scripted sweep", [],
    "Act title 'Read a Real One' (serif 40) top-left. The ten-line pad shader on the code card at left, no line focus; at right the same real render as the opening: the flat square charging from striped rust to flat green.",
    "The square charges while the whole shader waits to be read.",
    [{"at": 0.0, "event": "code card and the charging square"}, {"at": 0.5, "event": "half charged"}, {"at": 0.9, "event": "flat green"}],
    "LectureCodeTrace alone", "The viewer sees the same picture as the opening, now with every ingredient known: the return is the beat.",
    "C01 again (pad-angled-sweep.mp4).", "Lab pad shader probes (five activations, three renderers)", title="Read a Real One", caption="a shader from a small game")
lab("B30", 3, "lines one and two: the type and the render mode", PAD, V + "pad-face-held.png", FP + " · activation 0.3",
    [{"at": at("B30", "Line one"), "lines": [1]}, {"at": at("B30", "Line two"), "lines": [2]}],
    "Left: the ten-line pad code with line 1 then line 2 focused. Right: a real render of the pad face-on at activation 0.3 (held still; the stripes are visible there, see stripe-contrast.txt). Readout on the render when line 2 is focused: 'no lamp'.",
    "The focus steps from line 1 to line 2 on their names.",
    [{"at": at("B30", "Line one"), "event": "line 1"}, {"at": at("B30", "Line two"), "event": "line 2; 'no lamp' readout"}],
    "LectureCodeTrace alone", "Code with its result is the claim; the held still keeps the result calm so the line focus carries the motion.",
    "C13: Lab render, lab-shaders/12-signal-pad.gdshader at --set activation=0.3, still 3840 x 2160, Forward+. Verified light stripe (0.345, 0.435, 0.306), dark stripe (0.282, 0.428, 0.302): a color difference of 5.7 (CIE76), the dark stripe 52 RGB from the ink color.",
    "Lab probes 12-signal-pad at 0.3 (lab-results-extra.jsonl); stripe-contrast.txt", readouts=[{"at": at("B30", "No lamp"), "text": "no lamp", "x": 0.5, "y": 0.9}])
lab("B31", 3, "lines three to five: three dials", PAD, V + "pad-face-held.png", FP + " · activation 0.3",
    [{"at": at("B31", "Lines three to five"), "lines": [3, 4, 5]}, {"at": at("B31", "Activation,"), "lines": [3]}, {"at": at("B31", "And two colors"), "lines": [4, 5], "label": "rust at activation 0, green at activation 1"}, {"at": at("B31", "each marked"), "lines": [4, 5], "label": "source_color: this vec4 is a color"}],
    "Left: the pad code with lines 3 to 5 focused, then line 3 alone, then lines 4 and 5 tagged 'rust at activation 0, green at activation 1' and, as the voice says 'each marked source color', 'source_color: this vec4 is a color'. Right: the same held render (no color readouts: the held picture is the olive blend at 0.3, so 'rust' and 'green' belong on the code lines that hold them).",
    "The focus narrows to the activation line, then to the two color lines, which are tagged in turn.",
    [{"at": at("B31", "Lines three to five"), "event": "lines 3 to 5"}, {"at": at("B31", "Activation,"), "event": "line 3"}, {"at": at("B31", "And two colors"), "event": "lines 4 and 5; 'rust at activation 0, green at activation 1'"}, {"at": at("B31", "each marked"), "event": "'source_color' tag"}],
    "LectureCodeTrace alone", "Three parallel declarations are best read as a block, then one at a time.",
    "C13 again (pad-face-held.png).", "Lab 11-mix-dial and 12-signal-pad probes: activation 0 reads rust (0.400, 0.161, 0.090), activation 1 reads green (0.122, 0.722, 0.522)")
lab("B32", 3, "lines six and seven: fragment and the stripe", PAD, V + "pad-face-held.png", FP + " · activation 0.3",
    [{"at": at("B32", "Fragment runs"), "lines": [6], "label": "fragment(): runs once for each pixel the shape covers"}, {"at": at("B32", "Its first line"), "lines": [7]}],
    "Left: the pad code with line 6 (tagged with the GLOSSARY wording for fragment()) then line 7 focused. Right: the held render; a terracotta ring (grey-backed) hops across the first four stripes, one stripe per spoken number in 'zero, one, zero, one'.",
    "The ring hops across the first four stripes as the voice counts them.",
    [{"at": at("B32", "Fragment runs"), "event": "line 6"}, {"at": at("B32", "Its first line"), "event": "line 7"}, {"at": at("B32", "Zero, one"), "event": "ring hops across four stripes"}],
    "manim strip stack", "The stripes are already on the real render; a ring hopping across them is the 'zero, one, zero, one'.",
    "C13 again (pad-face-held.png).", "analyze-bands.txt (stripe edges at multiples of 0.0625; the file calls a stripe a band)",
    rings=[{"at": at("B32", "Zero, one", 0.0), "box": [0.0, 0.0, 0.0625, 1.0]}, {"at": at("B32", "Zero, one", 0.05), "box": [0.0625, 0.0, 0.125, 1.0]}, {"at": at("B32", "Zero, one", 0.1), "box": [0.125, 0.0, 0.1875, 1.0]}, {"at": at("B32", "Zero, one", 0.15), "box": [0.1875, 0.0, 0.25, 1.0]}])
lab("B33", 3, "line eight: base, the rust color times a mix", PAD, V + "pad-face-held.png", FP + " · activation 0.3",
    [{"at": at("B33", "Next, base"), "lines": [8]}, {"at": at("B33", "Dot r g b"), "lines": [8], "label": "swizzle: picking or reordering a vector's parts: c.rgb"}],
    "Left: the pad code with line 8 focused; when the voice says 'dot r g b' the line is tagged (GLOSSARY wording: 'swizzle: picking or reordering a vector's parts: c.rgb'). Right: the held render with a ring on the first dark stripe and then on the first light stripe; readouts 'x 0.65' and 'x 1.0' land with them (multipliers in the code, not pixel ratios).",
    "A ring moves from a dark stripe to a light stripe, carrying x 0.65 then x 1.0.",
    [{"at": at("B33", "Next, base"), "event": "line 8"}, {"at": at("B33", "point six five"), "event": "ring on a dark stripe, 'x 0.65'"}, {"at": at("B33", "full strength"), "event": "ring on a light stripe, 'x 1.0'"}, {"at": at("B33", "Dot r g b"), "event": "swizzle tag on line 8"}],
    "manim two stripes with weights", "The two weights belong on the two stripes they weigh; the ring moving between them is the 'mix'.",
    "C13 again (pad-face-held.png).", "Lab probes 12-signal-pad at 0.3 (lab-results-extra.jsonl)",
    rings=[{"at": at("B33", "point six five"), "box": [0.0, 0.0, 0.0625, 1.0]}, {"at": at("B33", "full strength"), "box": [0.0625, 0.0, 0.125, 1.0]}],
    readouts=[{"at": at("B33", "point six five"), "text": "x 0.65", "x": 0.03, "y": 0.9}, {"at": at("B33", "full strength"), "text": "x 1.0", "x": 0.09, "y": 0.9}])
lab("B34", 3, "line nine: the last mix; at one the stripes are gone", PAD, V + "pad-face-sweep.mp4", FP + " · activation swept by script",
    [{"at": at("B34", "The last line"), "lines": [9]}],
    "Left: the pad code with line 9 (`ALBEDO = mix(base, active_color.rgb, activation);`) focused. Right: a real face-on render sweeping activation 0 to 1: the rust stripes fade into flat green; a thin 0 to 1 strip under it carries a marker. A readout 'stripes gone' lands at the end.",
    "The stripes fade out as the marker reaches 1, and the surface ends flat green.",
    [{"at": 0.0, "event": "surface starts striped rust"}, {"at": at("B34", "At zero"), "event": "stripes fading"}, {"at": at("B34", "stripes are gone"), "event": "'stripes gone': flat green"}],
    "ShaderLab stills at 0, 0.5 and 1", "Stripes that visibly dissolve are the claim; stills would need three panes and the dark one would fail the type gate.",
    "C12: Lab-style render of lab-shaders/12-signal-pad.gdshader on quad3d, activation 0 to 1 across the whole clip (scripted sweep; the clip is as long as the beat), Forward+. Verified at activation 1: dark and light stripes read the same (0.1216, 0.7216, 0.5216).",
    "Lab probes 12-signal-pad (0 and 1)", ramp={"at": 0.0, "from": 0, "to": 1, "period": "__AUDIO__"}, readouts=[{"at": at("B34", "stripes are gone"), "text": "stripes gone", "x": 0.5, "y": 0.9}])
manim("B35", 3, "the pad uses one of the three function slots", "MissingSlots",
      "The pad's fragment function as a cream code box in the middle (the real lines 6 to 10, Menlo). Above it a dashed empty slot labelled 'vertex(): Godot's default', below it a dashed empty slot labelled 'light(): skipped by unshaded'. The dashes draw in, the two slots pulse once, and the fragment box gets a solid outline. All three slots share one alignment, as in the skeleton card from the first act.",
      "Two dashed slots draw in around the one filled function.",
      [{"at": 0.0, "event": "fragment box"}, {"at": at("B35", "There is no vertex"), "event": "upper dashed slot draws in"}, {"at": at("B35", "no light function"), "event": "lower dashed slot draws in"}, {"at": at("B35", "The pad needs"), "event": "fragment box outlined solid"}],
      "ShaderLab", "The pad is the skeleton with only one slot filled; dashed empty slots make the missing functions visible.",
      "lab-shaders/12-signal-pad.gdshader (no vertex() or light()); docs: default vertex shader; unshaded skips light")
lab("B36", 3, "the same ten lines on a thin box and on a flat square", None, V + "box-vs-square.mp4", FP + " · same shader file on both · activation 0.3",
    [], "Real Godot render, game camera angle: on the left a thin box (the pad's own shape), on the right a flat square, both wearing the same shader at activation 0.3 (stripes visible, stripe-contrast.txt). The box's top shows wide stripes (about six), the square shows sixteen narrow ones. Labels: 'thin box', 'flat square', then '6 stripes' and '16 stripes'.",
    "The two surfaces wear the same colors but different stripes, side by side.",
    [{"at": 0.0, "event": "box and square, same stripes shader"}, {"at": at("B36", "A box keeps"), "event": "'6 stripes' and '16 stripes'"}, {"at": at("B36", "Same ten lines"), "event": "labels 'thin box' and 'flat square'"}],
    "manim drawing of a box's six UV cells", "The mismatch between the two renders is the evidence, and the earlier turntable already showed the box's map in pieces.",
    "C14: custom scene 'pad on its box' (S1): lab-shaders/12-signal-pad.gdshader on BoxMesh 1.55 x 0.10 x 1.55 at x -1.1 and on QuadMesh 1.55 x 1.55 lying flat at x +1.1, orthographic size 3.2 from (5.8, 9, 11), activation held at 0.3, the clip as long as the beat, Forward+. Verified: flat quad 16 stripes, box top 6 stripes (activation 0); at size 3.2 the two fill x 0.15 to 0.85 and y 0.20 to 0.78 of the frame.",
    "verify2-pad-on-quad-and-box.gd (A: 16 and 6 stripes; B: angled pictures)", layout="video",
    readouts=[{"at": at("B36", "In the game"), "text": "thin box", "x": 0.32, "y": 0.1}, {"at": at("B36", "not a flat square"), "text": "flat square", "x": 0.68, "y": 0.1}, {"at": at("B36", "A box keeps"), "text": "6 stripes", "x": 0.32, "y": 0.9}, {"at": at("B36", "so its top"), "text": "16 stripes", "x": 0.68, "y": 0.9}],
    caption="the game's pad is a thin box; its camera looks from the same direction")

# ═════════════════════════════ ACT V · Which Renderer? ═════════════════════════════
lab("B37", 4, "the pad in two renderers, side by side", None, V + "pad-two-renderers.mp4", "Godot 4.7.2 · Apple M4 Pro · same file in two renderers · scripted sweep", [],
    "Act title 'Which Renderer?' (serif 40) top-left. A real two-pane render: the same pad file charging face-on from activation 0 to 0.7 (done by 0.44 of the clip) and then held there, Forward+ on the left, Compatibility on the right, in step. Labels: 'Forward+' above the left pane, 'Compatibility' above the right. Once they stop the greens differ visibly: the left is the lighter green.",
    "Two squares charge side by side and stop on two different greens.",
    [{"at": 0.0, "event": "two panes charging, rust to green"}, {"at": 0.44, "event": "both panes reach activation 0.7 and hold: two different greens (nothing moves at the midpoint)"}, {"at": at("B37", "Forward Plus on the left"), "event": "'Forward+' label"}, {"at": at("B37", "Compatibility on the right"), "event": "'Compatibility' label"}],
    "two stills", "Two panes charging in step and stopping on different greens show the mismatch as a picture before B38 puts a number on it.",
    "C15: two harness runs of lab-shaders/12-signal-pad.gdshader on quad3d, one with --renderer forward_plus and one with --renderer gl_compatibility, activation 0 to 0.7 across 0 to 0.44 of the clip, then held at 0.7, in both (the clip is as long as the beat), 30 fps, joined side by side (ffmpeg hstack) into one 3840 x 2160 video, each pane 1920 x 2160 scaled to fit the pane. 50 % and 85 % frames: activation 0.7, where the Compatibility dark stripe is well clear of the ink color (it is not below about 0.5).",
    "Lab pad probes: at 0.75 Forward+ light stripe (59, 162, 117) against Compatibility (47, 148, 105) in 8 bits (lab-results.jsonl, stripe-contrast.txt); at 0.5 (0.298, 0.537, 0.380) against (0.259, 0.439, 0.306)", layout="video", title="Which Renderer?",
    readouts=[{"at": at("B37", "Forward Plus on the left"), "text": "Forward+", "x": 0.25, "y": 0.06}, {"at": at("B37", "Compatibility on the right"), "text": "Compatibility", "x": 0.75, "y": 0.06}])
lab("B38", 4, "half charge: two greens, measured", None, V + "pad-two-renderers-half.png", "Godot 4.7.2 · Apple M4 Pro · activation 0.5 · green channel of a light stripe", [],
    "The same two panes held at activation 0.5. A terracotta ring (grey-backed) marks the first light stripe in the left pane, then in the right pane, with a readout beside each: 'G 0.54' and 'G 0.44'. Caption, GLOSSARY wording, there from the first frame: 'channel: one of red, green, blue or alpha'. Credit line: 'Apple M4 Pro · Godot 4.7.2'.",
    "A ring and a number land first on the left stripe, then on the right.",
    [{"at": at("B38", "reads point five four"), "event": "left ring and 'G 0.54'"}, {"at": at("B38", "point four four"), "event": "right ring and 'G 0.44'"}],
    "LectureEvidenceTable, two rows", "The two panes next to each other with a number on each is the claim 'they do not match', and the table would lose the picture.",
    "C16: the two renderers held at activation 0.5: Forward+ light stripe (0.298, 0.537, 0.380), Compatibility (0.259, 0.439, 0.306) at UV.x 0.09375; composite as C15.",
    "Lab probes 12-signal-pad-forward_plus-0.5 and -gl_compatibility-0.5", layout="video",
    rings=[{"at": at("B38", "reads point five four"), "box": [0.03125, 0.0, 0.0625, 1.0]}, {"at": at("B38", "point four four"), "box": [0.53125, 0.0, 0.5625, 1.0]}],
    readouts=[{"at": at("B38", "reads point five four"), "text": "G 0.54", "x": 0.25, "y": 0.92}, {"at": at("B38", "point four four"), "text": "G 0.44", "x": 0.75, "y": 0.92}],
    caption="channel: one of red, green, blue or alpha")
lab("B39", 4, "albedo one half: Forward+ draws 0.74, Compatibility 0.50", None, V + "grey-two-renderers.png", "Godot 4.7.2 · Apple M4 Pro · unshaded ALBEDO = vec3(0.5)", [],
    "Two big grey swatches, real Lab renders of lab-shaders/14-grey-3d.gdshader: Forward+ on the left (the lighter grey), Compatibility on the right (the mid grey). Readouts '0.74' and '0.50' land on them, then a third small readout '2D: both 0.50' below.",
    "The lighter swatch and the mid swatch land with their numbers.",
    [{"at": at("B39", "Forward Plus draws"), "event": "left swatch and '0.74'"}, {"at": at("B39", "Compatibility draws"), "event": "right swatch and '0.50'"}, {"at": at("B39", "In two-D"), "event": "'2D: both 0.50'"}],
    "manim swatches drawn from the numbers", "Real renders of the plainest shader; drawing swatches from a number would be a reconstruction of a Godot result.",
    "C17: Lab stills of lab-shaders/14-grey-3d.gdshader (--renderer forward_plus, --renderer gl_compatibility), side by side with labels. Verified: Forward+ 0.7373, Mobile 0.7373, Compatibility 0.502; 2D COLOR 0.5 reads 0.502 in all three.",
    "Lab probes 14-grey-3d and 13-grey-2d (three renderers)", layout="video",
    readouts=[{"at": at("B39", "Forward Plus draws"), "text": "0.74", "x": 0.25, "y": 0.5}, {"at": at("B39", "Compatibility draws"), "text": "0.50", "x": 0.75, "y": 0.5}, {"at": at("B39", "In two-D"), "text": "2D: both 0.50", "x": 0.5, "y": 0.92}])
manim("B40", 4, "why: linear light and a curve on the way to the screen", "TwoLanes",
      "Two horizontal lanes. Top lane 'Forward+': the number chip 0.5 enters, passes a block labelled 'linear to sRGB' (the arrows between the parts are drawn shapes, never a glyph), and leaves as 0.74. Bottom lane 'Compatibility': the same chip passes straight through and leaves as 0.50. Above the lanes a small plot: the diagonal y = x and the screen curve (the standard one that lifts dark and middle values); a dot at x = 0.5 rises to 0.74 on the curve and stays at 0.50 on the diagonal. Two captions, GLOSSARY wording, there from the first frame: 'linear: the scale light adds up on, in a straight line' and, under it, 'sRGB: the scale a color picker's numbers use, spaced for the eye'. Credit: 'measured · Apple M4 Pro · Godot 4.7.2'.",
      "The same chip comes out lighter in one lane and unchanged in the other.",
      [{"at": 0.0, "event": "two lanes, chip 0.5 enters both"}, {"at": at("B40", "Forward Plus treats"), "event": "top lane: curve block, output 0.74; plot dot rises"}, {"at": at("B40", "Compatibility skips"), "event": "bottom lane: straight through, 0.50"}],
      "plot() alone", "Two lanes with one chip going through different machinery is the explanation; the plot shows the curve once.",
      "evidence/planning-checks/linear-mix-check.txt (0.7354 predicted, 0.7373 measured)")
manim("B41", 4, "the same dial lands on two midpoints", "TwoMidpoints",
      "A number line for the red channel of the pad's two colors: rust 0.40 at the left end, green 0.12 at the right end. A terracotta dot slides between them. At the middle two markers drop: 'as written 0.26' (labelled 'Compatibility') and 'in linear light 0.30' (labelled 'Forward+'), with a small gap between them. A tag by the two ends, GLOSSARY short form for a label, lands as the voice says 'marked source color': 'source_color: numbers are sRGB: convert to light first'. Credit: 'measured 0.26 and 0.30 · Apple M4 Pro · Godot 4.7.2'. Greys and the one terracotta only.",
      "The dot slides to the middle and two different midpoints drop, a small gap apart.",
      [{"at": 0.0, "event": "number line, rust and green ends"}, {"at": at("B41", "marked source color"), "event": "'source_color' tag by the two ends"}, {"at": at("B41", "Forward Plus turns"), "event": "Forward+ midpoint 0.30"}, {"at": at("B41", "Compatibility blends"), "event": "Compatibility midpoint 0.26"}, {"at": at("B41", "One dial"), "event": "the gap between them ringed"}],
      "ShaderLab", "One channel on one line keeps the two midpoints readable; the full color pair is already on the real render two beats earlier.",
      "linear-mix-check.txt (typed average 0.26, linear mix 0.2998; measured 0.2588 and 0.2980); Lab 11-mix-dial and 12-signal-pad: the endpoints read as typed in Forward+")
T42 = at("B42", "output is s R G B")
rem("B42", 4, "the docs: output_is_srgb tells a shader which renderer it is in", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html#global-built-ins",
     "image": V + "docs-global-builtins.png", "caption": "Godot 4.7 documentation · Spatial shaders · Global built-ins · captured YYYY-MM-DD", "frame": "browser",
     "moves": [{"at": 0, "x": 0.5, "y": 0.5, "scale": 1}, {"at": T42, "x": 0.5, "y": 0.5, "scale": 1.7, "ring": [0.08, 0.5, 0.84, 0.07]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 'Spatial shaders' page, Global built-ins table, in a browser window; the camera pushes in on the row `in bool OUTPUT_IS_SRGB` ('true when output is in sRGB color space (this is true in the Compatibility renderer, false in Forward+ and Mobile)') and one terracotta ring marks it. The ring box is an estimate: recompute it from the real capture.",
    "The camera pushes in on the OUTPUT_IS_SRGB row the voice is reading.",
    [{"at": 0.0, "event": "the global built-ins table"}, {"at": T42, "event": "push-in and ring on the OUTPUT_IS_SRGB row"}],
    "ShaderLab of a shader that paints red or blue by renderer", "The sentence is the documentation's own; the page is the evidence. The red-or-blue run is kept in the evidence (15-which-renderer).",
    "D2: Playwright capture of the live docs page at #global-built-ins, row OUTPUT_IS_SRGB scrolled to mid-window, 1600x900 at 2.4x")
lab("B43", 4, "where to see and change which renderer you are on", None, V + "editor-renderer.mp4", "Godot 4.7.2 editor · scripted editor session", [],
    "Four real frames of the Godot editor (a scripted editor session), joined by cross-dissolves: the Project menu open with Project Settings... ringed; the Project Settings dialog on Rendering, Renderer, with the Renderer entry in the left tree and then the Rendering Method row (forward_plus) ringed; the Rendering Method menu open with its three entries forward_plus, mobile, gl_compatibility ringed; then the dialog's note 'Changed settings will be applied to the editor after restarting.' with the Save & Restart button ringed. The ring moves as the voice names each step.",
    "The ring moves from the Project menu to the Renderer page, the Rendering Method row, the three entries and Save & Restart.",
    [{"at": at("B43", "Open Project Settings"), "event": "R1-A: the Project menu open, Project Settings... ringed"}, {"at": at("B43", "then Rendering, Renderer", lag=-0.02), "event": "dissolve to R1-C: Rendering, Renderer"},
     {"at": at("B43", "then Rendering, Renderer", lag=0.06), "event": "the Renderer entry in the left tree ringed"}, {"at": at("B43", "Rendering Method shows it"), "event": "the Rendering Method row ringed (forward_plus)"},
     {"at": 0.42, "event": "dissolve to R1-D: the Rendering Method menu open; the three entries ringed"}, {"at": 0.56, "event": "dissolve to R1-E: the restart note"},
     {"at": at("B43", "needs Save and Restart", lag=0.04), "event": "Save & Restart ringed"}],
    "BrowserCapture of the docs page (the first plan: its sentence about the renderer name in the upper right corner)", "The real editor frames show where the setting lives and what it is called; the docs sentence about a name in the editor's upper right corner is not what the 4.7.2 editor shows by default (hidden until Show Renderer Selector is on), so a docs capture would point the viewer at the wrong place.",
    "E1 (DONE by script, 2026-10-13, editor driver; README section 11): four full frames from `_godot-shaders-series/editor-capture/png/1920x1080/renderer-path/` (native 3456x1944 twins in png/3456x1944/renderer-path/): renderer-path_R1-A_Project-menu-open, R1-C_Project-Settings_Rendering-Renderer_menu-closed, R1-D_Project-Settings_Rendering-Method_menu-open, R1-E_Project-Settings_restart-note. Cross-dissolves at the `show` fractions (R1-A to R1-C, then 0.42 to R1-D, then 0.56 to R1-E); ring boxes are fractions of the whole 1920x1080 frame (no crop). Real labels, read from the live UI: menu Project > Project Settings...; dialog 'Project Settings (project.godot)'; left tree Rendering > Renderer (a second page named Rendering sits under Internationalization: not that one); rows 'Rendering Method' (forward_plus), 'Rendering Method.web', 'Rendering Method.mobile'; the dropdown lists forward_plus, mobile, gl_compatibility; after a change the note 'Changed settings will be applied to the editor after restarting.' with Save & Restart and X. Save & Restart was never pressed. The editor draws its own menu bar inside the window (Use Embedded Menu on): label the clip 'scripted editor session'. NOT used: the title-bar frames R3-A, R3-B and the OFF-vs-ON composite (the docs say the renderer's name always sits in the editor's upper right corner; in 4.7.2 it is hidden until Editor > Editor Settings > Interface > Editor > Appearance > Show Renderer Selector is on).",
    "Editor capture E1, DONE by script (editor-capture/README.md section 11; frames R1-A, R1-C, R1-D, R1-E); FACTCHECK row 97 (CORRECTED: docs versus run) and row 98", layout="video", lane="editor",
    rings=[{"at": at("B43", "Open Project Settings", lag=0.04), "box": [0.09, 0.044, 0.35, 0.068]}, {"at": at("B43", "then Rendering, Renderer", lag=0.06), "box": [0.179, 0.716, 0.264, 0.742]},
           {"at": at("B43", "Rendering Method shows it"), "box": [0.279, 0.233, 0.835, 0.261]}, {"at": 0.43, "box": [0.56, 0.27, 0.83, 0.345]},
           {"at": at("B43", "needs Save and Restart", lag=0.04), "box": [0.748, 0.756, 0.815, 0.792]}])
lab("B44", 4, "a pixel is true for one renderer: name it when you test", None, V + "pad-two-renderers-half.png", "Godot 4.7.2 · Apple M4 Pro · activation 0.5", [],
    "The two held panes again. A ring moves from the left pane to the right pane as the voice says 'one renderer' then 'the wrong one'. Caption at the end: 'a pixel is true for one renderer'. Labels 'Forward+' and 'Compatibility' stay above the panes.",
    "A ring hops from the left pane to the right pane.",
    [{"at": at("B44", "one renderer"), "event": "ring on one pane"}, {"at": at("B44", "the wrong one"), "event": "ring on the other pane"}, {"at": 0.9, "event": "caption"}],
    "manim card with the sentence", "The same pair of panes is the closing proof, now with the lesson attached; a text card would be narration set as type.",
    "C16 again (pad-two-renderers-half.png).", "Lab pad probes (0.5, two renderers)", layout="video",
    rings=[{"at": at("B44", "one renderer"), "box": [0.0, 0.0, 0.5, 1.0]}, {"at": at("B44", "the wrong one"), "box": [0.5, 0.0, 1.0, 1.0]}],
    readouts=[{"at": 0.1, "text": "Forward+", "x": 0.25, "y": 0.06}, {"at": 0.1, "text": "Compatibility", "x": 0.75, "y": 0.06}],
    caption="a pixel is true for one renderer")

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
(HERE / "lanes").mkdir(exist_ok=True)
for old in (HERE / "lanes").glob("act*.json"):
    old.unlink()
for ai in range(len(N.ACTS)):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

# guard: ids in order, every body beat has a lane, no cue in the 45-55 % window
assert [e["bid"] for e in E] == [b for b, _, _ in N.BODY], "lane order must match the narration"
for e in E:
    ent = e["entry"]
    if ent["lane"] == "manim":     # a Manim scene must be a settled still at its midpoint: no event may start in the 45-55 % window
        for s in ent.get("show", []):
            assert not (0.45 <= s["at"] <= 0.55), f"{e['bid']}: show cue inside 45-55 %: {s}"
    p = ent.get("props", {})
    for c in p.get("cues", []):
        if isinstance(c, dict):
            assert not (0.45 <= c["at"] <= 0.55), f"{e['bid']}: cue inside 45-55 %: {c}"
        elif isinstance(c, (int, float)):
            assert not (0.45 <= c <= 0.55), f"{e['bid']}: table cue inside 45-55 %: {c}"
    for r in p.get("readouts", []) + p.get("rings", []):
        if "at" in r:     # (CCPlainShell rings are {line, cue} in frames: re-timed at build)
            assert not (0.45 <= r["at"] <= 0.55), f"{e['bid']}: readout/ring inside 45-55 %: {r}"

# guard: the ShaderLab limits in COMPONENT-SPECS.md (label <= 60 characters, caption <= 80, readout <= 3 words, code <= 14 lines,
# a stack layout quotes at most 3 lines, every cue line exists in the code shown)
for e in E:
    p = e["entry"].get("props", {})
    if e["entry"].get("pattern") != "ShaderLab":
        continue
    code_lines = p["code"].split("\n") if p.get("code") else []
    assert len(code_lines) <= 14, f"{e['bid']}: ShaderLab code over 14 lines"
    if p["layout"] == "stack":
        assert 1 <= len(code_lines) <= 3, f"{e['bid']}: a stack layout quotes 1 to 3 lines, has {len(code_lines)}"
    assert len(p.get("caption", "")) <= 80, f"{e['bid']}: caption over 80 characters ({len(p['caption'])})"
    for c in p.get("cues", []):
        assert len(c.get("label", "")) <= 60, f"{e['bid']}: cue label over 60 characters ({len(c['label'])}): {c['label']}"
        for ln in c.get("lines", []):
            assert 1 <= ln <= len(code_lines), f"{e['bid']}: cue line {ln} is not in the {len(code_lines)}-line code shown"
    for r in p.get("readouts", []):
        assert len(r["text"].split()) <= 3, f"{e['bid']}: readout over 3 words: {r['text']}"

lanes_hist = {}
for e in E:
    lanes_hist[e["entry"]["lane"]] = lanes_hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
sl = ["# Shot list: Shaders in 3D\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab render or a scripted scene capture of a tested file in `lab-shaders/`; six small scene scripts (S1 to S6, in `CAPTURE-PLAN.md`) and two docs screenshots must be produced before the build. One beat (B43) shows Godot's own editor: four frames already recorded by script, to be copied (no click, no recording by hand).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`; shared with every shader film, so check whether an earlier film's build already made it). 2. **`shader_kit.py`** Manim helpers (same file). 3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` (same file), with a scene-script option for S1 to S6. 4. **Docs screenshots** D1 and D2 via Playwright. 5. **Two-renderer composites** C15 to C17 (ffmpeg hstack of two harness runs). 6. **Editor frames** for B43 (E1): already recorded by script, copy them (`CAPTURE-PLAN.md`).\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
