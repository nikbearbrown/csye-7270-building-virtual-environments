#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text, the terminal cards must quote the engine's log word for word,
and the shot list must say exactly what the lanes say. Re-run after any edit:
    python3 _gen_lanes.py && python3 make_sheet.py
(Never re-run make_sheet.py after `art final`.)
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_godot-shaders-series"))
_spec = importlib.util.spec_from_file_location("narration", HERE / "narration.py")
N = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(N)
WORDS = {bid: len(txt.split()) for bid, _, txt in N.BODY}
SH = HERE / "lab-shaders"
EV = HERE / "evidence" / "planning-checks"
E = []          # entries in beat order
NS = "godot-shader-language"      # folder under runtime/remotion/public/ for this film's captures


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def log_lines(name, compact=False):
    """The engine's own excerpt for one failing shader: from '--Main Shader--' through the 'at: (null)' line."""
    txt = (EV / "logs" / f"{name}.log").read_text().splitlines()
    i0 = txt.index("--Main Shader--")
    out = []
    for ln in txt[i0:]:
        out.append(ln.rstrip())
        if ln.strip().startswith("at: (null)"):
            break
    if compact:
        keep = [out[0]] + [x for x in out if x.startswith("E ")] + [x for x in out if x.startswith("SHADER ERROR")]
        return keep
    return out


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence, sparse=True):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": sparse}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, title=None, caption="", lane="capture"):
    props = {"layout": layout, "code": code_of(shader) if shader else "", "codeFile": f"lab-shaders/{shader}" if shader else "",
             "cues": cues, "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption,
             "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    entry = {"lane": lane, "pattern": "ShaderLab", "props": props, "visual_intent": intent, "motion_claim": motion, "show": show,
             "runner_up": runner, "why": why, "sparse": False}
    if spec:
        entry["capture_spec"] = spec
    add(bid, act, about, entry, evidence)


def rem(bid, act, about, pattern, props, intent, motion, show, runner, why, evidence, lane="remotion", spec=None):
    entry = {"lane": lane, "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion, "show": show,
             "runner_up": runner, "why": why, "sparse": False}
    if spec:
        entry["capture_spec"] = spec
    add(bid, act, about, entry, evidence)


def term(bid, act, about, logname, title, intent, motion, show, runner, why, evidence, compact_logs=None, ring_at=190, ring_marked=False):
    """A real engine log on CCPlainShell, verbatim. `compact_logs`: several logs shown as short excerpts in one window."""
    if compact_logs:
        lines = []
        for k, nm in enumerate(compact_logs):
            if k:
                lines.append("")
            lines += log_lines(nm, compact=True)
    else:
        lines = log_lines(logname)
    key = "E " if ring_marked else "SHADER ERROR"
    # ring cues are frames at the sheet's 24 fps, placed at about 68 percent of the ESTIMATED beat (words x 0.34 s): outside the 45-55 percent
    # window. Recompute from the measured audio: cue = 0.68 x durationSeconds x 24.
    ring_at = round(0.68 * WORDS[bid] * 0.34 * 24)
    rings = [{"line": i, "cue": ring_at + 8 * n} for n, i in enumerate([i for i, l in enumerate(lines) if l.startswith(key)])]
    props = {"title": title, "lines": lines, "startCue": 10, "lineGap": 12, "fontSize": 36, "windowMargin": 90,
             "rings": rings, "durationSeconds": "__AUDIO__"}
    add(bid, act, about, {"lane": "terminal", "pattern": "CCPlainShell", "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


GLOSS_UV = "UV: a point's address on the shape: 0 to 1 across, 0 to 1 down"

# ═════════════════════════════ ACT I · The Shape of a File ═════════════════════════════
lab("B01", 0, "a real 14-line shader and its pulse; why reading matters", "01-breathe.gdshader", f"{NS}/breathe-b01.mp4",
    "Godot 4.7.2 · Forward+ · tint set to teal", [],
    "Act title 'The Shape of a File' (serif 40) top-left. The real 14-line file `lab-shaders/01-breathe.gdshader` in the code panel at left with line numbers; at right a framed real Godot render that breathes between pale gray and teal. Window label: 'Godot 4.7.2 · Forward+ · tint set to teal'.",
    "The render swings from pale gray to teal and back while the file stays still beside it.",
    [{"at": 0.0, "event": "file and window on the stage; window labelled"}, {"at": 0.2, "event": "the pulse swings: gray to teal and back"}],
    "LectureCodeTrace alone", "The promise of the film is that this file can be read; the real file beside its real result is the claim, and nothing drawn could be as honest.",
    "C01a: Lab rect, lab-shaders/01-breathe.gdshader, --set tint=#5FA391 (the Inspector would set it), live TIME, a clip a little longer than this beat's measured audio (about 16 s) at 30 fps, Forward+, no input. Verified: the pulse swings between about 0.90 gray and (0.38, 0.64, 0.57); period about 3.2 s (evidence/planning-checks/pulse-range.txt). Gate V samples the 50 and 85 percent frames and fails a pale fill on the cream stage, so set --time-origin t0 so that wave = 0.5 + 0.5 * sin(2 * (t0 + t)) is 0.4 or less at t = 0.5 and 0.85 times this beat's measured audio (for 16.0 s, t0 about 0.98 s gives 0.11 at both). B40 needs its OWN clip (C01b): one origin cannot serve both beats.",
    "Lab run 01-breathe + pulse-range.txt; clean log (no warning)", layout="side", title="The Shape of a File")

lab("B02", 0, "the three zones of a shader file", "01-breathe.gdshader", "", "",
    [{"at": 0.33, "lines": [1], "label": "header"}, {"at": 0.58, "lines": [3, 4], "label": "globals"},
     {"at": 0.82, "lines": [6, 7, 8, 9, 10, 11, 12, 13, 14], "label": "functions"}],
    "The same 14-line file alone on the stage (layout 'code', line numbers on). Three bands light in turn with a one-word chip beside each: line 1 'header', lines 3 to 4 'globals', lines 6 to 14 'functions'.",
    "A highlight band slides down the file and stops on each zone as the voice names it.",
    [{"at": 0.33, "event": "band on line 1: header"}, {"at": 0.58, "event": "band on lines 3 and 4: globals"}, {"at": 0.82, "event": "band on lines 6 to 14: functions"}],
    "manim code card with bands", "A Manim card at the 32-point type floor holds about 8 lines of code (measured: Menlo at 32 is 0.25 unit per character, 0.6 per line); ShaderLab's code layout shows all 14 real lines.",
    "", "lab-shaders/01-breathe.gdshader (compiled in the Lab)", layout="code", lane="remotion")

manim("B03", 0, "the header: shader type, optional render mode", "Header",
      "`shader_type canvas_item;` in monospace (size 40) upper center. Under it a row of tiles: `canvas_item` captioned '2D + interface' and `spatial` captioned '3D' (both outlined), and three small tiles `particles`, `sky`, `fog` under a bracket labelled 'more'. A terracotta ring settles on canvas_item, in the line and on its tile. Serif 32 caption: 'shader type: the first line; says what the shader is for'. Last, a dimmer second line `render_mode blend_add;` slides in below with a tag 'optional' and a drawn pair of overlapping outlined squares whose overlap is tinted lighter, labelled 'blend'.",
      "The first line types in and the tiles line up under it; a ring picks canvas item; then an optional second line slides in below.",
      [{"at": 0.08, "event": "first line types in"}, {"at": 0.22, "event": "five tiles appear under it"}, {"at": 0.36, "event": "ring on canvas_item"},
       {"at": 0.62, "event": "render_mode line slides in, tagged optional"}, {"at": 0.78, "event": "overlapping squares: blend"}],
      "LectureEvidenceTable of shader types", "The first line is the picture; tiles under the real line show what the line chooses, which a table would only list.",
      "docs (Introduction to shaders: shader types, render modes); Lab 21-blend-add vs 22-blend-mix (additive blend measured)")

manim("B04", 0, "globals: uniform, const, varying", "Globals",
      "A band labelled 'globals' with three rows stacked, each a declaration copied from lab-shaders/04-globals.gdshader in monospace with a serif 32 caption beneath in the GLOSSARY wording: `uniform float level = 0.8;` / 'a value your game sets from outside; every pixel sees the same one'; `const vec3 TEAL = vec3(0.37, 0.64, 0.57);` / 'a named value that never changes'; `varying vec2 corner_uv;` / 'a value set at each corner, blended across the shape for fragment() to read'. Below the band a thin bar labelled 'functions' and a drawn downward arrow from the band into it, labelled 'readable below'. Captions may wrap to two lines.",
      "The three declarations land one by one as they are named; a downward arrow then runs from them into the functions bar.",
      [{"at": 0.13, "event": "uniform row"}, {"at": 0.36, "event": "const row"}, {"at": 0.56, "event": "varying row"}, {"at": 0.84, "event": "arrow into the functions bar"}],
      "LectureEvidenceTable with three rows", "Three declarations with their one-line meanings, and the direction they are visible in, are a structure drawn on cue; a table cannot show the arrow.",
      "Lab 04-globals compiles (uniform, const and varying together); 56-err-uniform-below (declared below use: unknown identifier); 55-err-const-modified")

rem("B05", 0, "the functions Godot calls: vertex, fragment, light", "LectureEvidenceTable",
    {"title": "The functions Godot calls", "headers": ["Function", "Runs", "Its job"],
     "rows": [["vertex()", "once for each vertex", "places the corners"], ["fragment()", "once for each pixel the shape covers", "sets that pixel's color"],
              ["light()", "once per pixel, for each light that touches it", "replaces the default lighting"]],
     "note": "Godot 4.7 shader reference · canvas item", "cues": [0.27, 0.36, 0.58], "durationSeconds": "__AUDIO__"},
    "A three-row table in the GLOSSARY wording, one row ringed as each function is named: vertex(), fragment(), light().",
    "The ring steps down the rows with the voice; fragment() stays ringed longest.",
    [{"at": 0.27, "event": "vertex() row"}, {"at": 0.36, "event": "fragment() row"}, {"at": 0.58, "event": "light() row"}],
    "ShaderLab code layout with two labelled ranges", "Three terms are defined here for the first time, and a table of kinds is exactly what the evidence-table component is for.",
    "docs (Canvas item shaders; Introduction to shaders: processor functions); GLOSSARY wording")

term("B06", 0, "a missing semicolon, in the engine's own words", "40-err-semicolon", "Godot 4.7.2 · shader compile error · printed by the engine",
     "A terminal window titled 'Godot 4.7.2 · shader compile error · printed by the engine' holding the engine's own log of lab-shaders/40-err-semicolon.gdshader, word for word: the source lines around the error with the offending line marked, then the error message. A terracotta ring lands on the marked line (the line AFTER the one missing its semicolon) late in the beat.",
     "The log lines land one by one; a ring then settles on the marked line.",
     [{"at": 0.1, "event": "log lines land"}, {"at": 0.65, "event": "ring on the marked line: the next line, where Godot noticed"}],
     "ClaudeCodeBeat (cream code card)", "The engine's real message beats any retelling; CCPlainShell plays real output verbatim (SHOW-THE-THING). If GATE T flags the dark window, fall back to the cream code card with the same lines.",
     "Lab 40-err-semicolon (exit 1); evidence/planning-checks/logs/40-err-semicolon.log (verbatim)", ring_marked=True)

manim("B07", 0, "spacing and line breaks are free", "ThreeSpellings",
      "Top region: one code card that holds one shader in three spellings in turn: neat (the five lines of 02-spacing-neat), squeezed (two lines: `shader_type canvas_item;` then `void fragment(){COLOR=vec4(0.4+0.6*UV,0.7,1.0);}`, 48 characters, the widest line), and spread (the seven lines of 02-spacing-spread). The characters slide and the line breaks collapse and reopen as one spelling becomes the next. Bottom region, never changing: ONE framed real Godot render (lab_window of png/02-spacing-neat.png, a pastel gradient) captioned 'Godot 4.7.2 · Forward+', with a drawn equals sign (two short bars) between code and picture, labelled 'same picture'. Type at least 32; keep the card inside 12 units.",
      "The code is rewritten three times while the picture below it never changes.",
      [{"at": 0.1, "event": "neat spelling and the picture"}, {"at": 0.3, "event": "neat collapses into the squeezed spelling"}, {"at": 0.62, "event": "squeezed opens into the spread spelling"}, {"at": 0.84, "event": "equals sign: same picture"}],
      "ShaderLab stack layout with one spelling", "Three spellings and one unchanging picture can only be told by a transformation; a static code panel shows one spelling.",
      "Lab 02-spacing-neat / -squeezed / -spread / -oneline: png-analysis.txt, 0 of 230,400 pixels differ (640x360, Forward+)")

manim("B08", 0, "comments: two kinds, and a commented-out line does nothing", "CommentOut",
      "Left: the nine-line card of lab-shaders/03-comment-on.gdshader with a block comment above the function and a trailing `// soften` comment: both comment spans are grayed from the first frame. Right: a framed real render (lab_window of png/03-comment-on.png, the pastel gradient). Then `//` is typed at the start of the line `c = 0.4 + 0.6 * c;` (the line grays out, as in lab-shaders/03-comment-off.gdshader) and the render cross-fades to the real png/03-comment-off.png (the same colors, much more saturated, dark top-left corner). Captions: 'line comment', 'block comment'.",
      "Typing two slashes grays a line out and the picture beside the code changes at once.",
      [{"at": 0.12, "event": "code with both comment kinds grayed; pastel render"}, {"at": 0.4, "event": "`//` typed at the start of the c line"}, {"at": 0.62, "event": "render cross-fades to the saturated picture"}],
      "LectureCodeTrace", "A commented-out line changing the picture is the claim, and it needs code and a real result changing together.",
      "Lab 03-comment-on vs 03-comment-off: png-analysis.txt, every pixel differs (largest channel difference 102/255); 03-comment-on equals 05-pastel")

manim("B09", 0, "names must match; Godot's names are its own", "NamesMustMatch",
      "Two panels. Left: two name tags in monospace, `level` with a drawn check and `Level` with a drawn cross, a drawn capital-L highlight on the difference. Right: `gl_FragColor` with a drawn cross, a drawn arrow to `COLOR` with a drawn check, captioned 'Godot's name for the output'. Top caption in serif 32: 'GLSL: the OpenGL Shading Language; Godot's is close to GLSL ES 3.0'. No engine messages on screen (the narration says unknown identifier).",
      "A cross lands on the wrong-case name and on the other language's name; the check lands on Godot's.",
      [{"at": 0.12, "event": "caption and the left tags"}, {"at": 0.3, "event": "cross on Level, capital L highlighted"}, {"at": 0.64, "event": "gl_FragColor crossed; arrow to COLOR; check"}],
      "CCPlainShell with two logs", "Two kinds of wrong name (wrong case, other language) are a contrast of name tags with marks; the logs for both were run and are in the evidence.",
      "Lab 41-err-case: Unknown identifier in expression: 'Level'.; scratch q01 (gl_FragColor): Unknown identifier; docs 'Converting GLSL to Godot shaders': gl_FragColor is COLOR; shading language reference: 'similar to GLSL ES 3.0'")

# ═════════════════════════════ ACT II · Types and Vectors ═════════════════════════════
manim("B10", 1, "every value has a type; declaring a variable", "ThreeTypes",
      "Act title 'Types and Vectors' (serif 40) top-left. Four outlined tiles in a row, each a type with a sample value in monospace: `float` / 0.5, `int` / 3, `bool` / true, `sampler2D` / a small drawn picture icon (a framed square with a hill shape). Under each tile a plain label: 'a decimal number', 'a whole number', 'true or false', 'the type of a texture a shader reads'. A one-line serif 32 caption under the row, in the GLOSSARY wording: 'texture: an image a shader can read by address'. Below, the declaration `float level = 0.5;` (a line of lab-shaders/32-declaration.gdshader) with three drawn brackets under it labelled 'type', 'name', 'value'.",
      "The tiles pop in as each type is named; the declaration types in and its three parts are bracketed.",
      [{"at": 0.06, "event": "act title; float, int, bool tiles pop in"}, {"at": 0.3, "event": "sampler2D tile"}, {"at": 0.6, "event": "declaration types in"}, {"at": 0.78, "event": "type, name, value brackets"}],
      "LectureEvidenceTable of types", "A declaration with its parts bracketed cannot be done in a table; the tiles and the bracketed line are one picture.",
      "docs (Data types table: bool, int, float, sampler2D descriptions; Casting examples); Lab 32-declaration compiles; GLOSSARY (sampler2D, texture)")

term("B11", 1, "Godot will not convert an int to a float", "42-err-int-to-float", "Godot 4.7.2 · two compile errors · excerpts of the engine's log",
     "A terminal window holding two short excerpts of the engine's own log, word for word and separated by a blank line: the marked line `float a = 2;` with 'Invalid assignment of 'int' to 'float'.' and the marked line `float a = 1 + 1.0;` with 'Invalid arguments to operator '+': 'int, float'.' A ring lands on each message.",
     "Each marked line lands with its message; a ring settles on the type names in the message.",
     [{"at": 0.1, "event": "first excerpt lands"}, {"at": 0.4, "event": "second excerpt lands"}, {"at": 0.7, "event": "rings on both messages"}],
     "Manim code line with a refusal mark", "Two refusals in the engine's own words (assignment and arithmetic) make the strictness concrete; excerpts keep both on one screen.",
     "Lab 42-err-int-to-float and 43-err-int-plus-float (exit 1); logs/42-*.log and logs/43-*.log (verbatim); 52-err-vec3-times-int; scratch: sin(1) and mix(..., 1) compile (not claimed)",
     compact_logs=["42-err-int-to-float", "43-err-int-plus-float"])

manim("B12", 1, "vectors: vec2, vec3, vec4; a color is a vec4; a texture lookup returns a vec4", "Bundles",
      "Rows of outlined cells (the bundle cast), stacked: `vec2` two cells, `vec3` three cells, `vec4` four cells labelled r g b a, the vec4 cells holding 0.37, 0.64, 0.57, 1.0 with a plain teal swatch to its right labelled 'a color'. Far left of the vec4 row, a framed small drawn texture (gradient square) with a drawn arrow into the row, labelled 'texture lookup'. Serif 32 caption: 'vector: a bundle of two to four numbers'. Under the last cell, in the GLOSSARY wording, 'alpha: how visible a pixel is: 0 invisible, 1 solid'.",
      "Rows of cells pop in one after another as the sizes are named; the texture arrow feeds the vec4 row last.",
      [{"at": 0.1, "event": "vec2 row"}, {"at": 0.2, "event": "vec3 row"}, {"at": 0.3, "event": "vec4 row with r g b a and swatch"}, {"at": 0.7, "event": "texture arrow into the vec4 row"}],
      "LectureEvidenceTable", "Cells whose count IS the size are the clearest picture of a bundle; the series' bundle cast starts here.",
      "docs (Data types); Lab 08-texture-vec4 (texture(TEXTURE, UV) assigned to a vec4: compiles, sprite center (0.3725, 0.6392, 0.5686)); GLOSSARY (vector, colors are vec4)")

manim("B13", 1, "building a vector: one number fills it; parts join; sizes must add up", "BuildAVector",
      "Three mini-diagrams stacked, using the bundle cells. (1) `vec3(0.5)`: one cell [0.5] sprouts two copies to make [0.5][0.5][0.5]. (2) `vec4(c, 1.0)`: a three-cell bundle c and a one-cell [1.0] slide together into a four-cell bundle, a drawn counter 3 + 1 = 4. (3) `vec3(0.1, 0.2)`: two cells and a dashed empty cell with a drawn cross, counter 2 of 3, labelled 'too few'.",
      "Cells copy, slide together and join into a bundle of the right size; the short one is refused.",
      [{"at": 0.1, "event": "one number fills three cells"}, {"at": 0.36, "event": "three plus one join into four"}, {"at": 0.66, "event": "two cells and a gap: crossed"}],
      "ShaderLab", "Constructing a vector is cells joining; the sizes adding up is a counter you can watch.",
      "docs (Constructing); Lab 24-fill-vec3 (0.5 fills: (0.502, 0.502, 0.502)); 28-ctor-vec2-vec2; 59-err-constructor-too-few and 60-err-constructor-too-many (refused)")

manim("B14", 1, "operators work on every part at once", "AllAtOnce",
      "Top: a three-cell bundle (0.2, 0.3, 0.4), a drawn times sign, a single cell 2.0; three parallel drawn arrows leave the 2.0 for each cell at the same instant; the result bundle (0.4, 0.6, 0.8) appears. Bottom: the same bundle times a second bundle (2.0, 1.0, 0.5); three short drawn arrows pair cell to cell, top to bottom; the result (0.4, 0.3, 0.2). Labels in monospace: `* 2.0`, `* vec3(2.0, 1.0, 0.5)`.",
      "Three arrows fire at the same instant and all three numbers change together; then each part meets its partner.",
      [{"at": 0.1, "event": "bundle times 2.0"}, {"at": 0.28, "event": "three arrows at once; result (0.4, 0.6, 0.8)"}, {"at": 0.62, "event": "bundle times bundle, cell to cell"}, {"at": 0.82, "event": "result (0.4, 0.3, 0.2)"}],
      "LectureCodeTrace", "'Every part at once' is simultaneous motion; three arrows leaving one cell in the same frame is the claim.",
      "Lab 07b-vec-times-float: (0.4, 0.6, 0.8); Lab 07-vec-times-vec: (0.4, 0.302, 0.2); docs (Operators: component-wise)")

lab("B15", 1, "vectors in use: a pastel gradient from UV", "05-pastel.gdshader", f"{NS}/pastel.png", "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.12, "lines": [4]}],
    "Code panel at left with the five-line shader; at right a framed real render: a pastel gradient, red growing to the right and green growing downward, blue constant. Short readouts 'more red' near the top-right corner and 'more green' near the bottom-left corner. Caption under the render: 'UV: a point's address on the shape: 0 to 1 across, 0 to 1 down'.",
    "The vector line is highlighted; the two readouts then name the directions the colors grow.",
    [{"at": 0.12, "event": "vec3 line highlighted"}, {"at": 0.78, "event": "readouts: more red, more green"}],
    "manim with the render inset", "Code and its real result side by side is the evidence for 'scale and shift every part at once'.",
    "C04: Lab rect, lab-shaders/05-pastel.gdshader, still PNG 1920x1080, Forward+. Probes: (0.02,0.02) (0.4118, 0.4118, 0.702); (0.98,0.02) (0.9882, 0.4118, 0.702); (0.02,0.98) (0.4118, 0.9843, 0.702); (0.98,0.98) (0.9882, 0.9843, 0.702).",
    "Lab 05-pastel corner probes", readouts=[{"at": 0.78, "text": "more red", "x": 0.86, "y": 0.1}, {"at": 0.78, "text": "more green", "x": 0.16, "y": 0.9}],
    caption=GLOSS_UV)

manim("B16", 1, "swizzling: picking parts by name", "Swizzle",
      "A four-cell vec4 row with THREE label rows: x y z w above the cells, r g b a below them, and a fainter s t p q under those (the third set, for texture coordinates). A drawn bracket over the first three cells labelled `.rgb` lifts them out into a three-cell vec3 row; then a bracket over the first two labelled `.xy` lifts them into a two-cell vec2 row. Serif 32 caption: 'swizzle: picking or reordering a vector's parts'.",
      "A bracket closes round the first three cells and lifts them out as a new, smaller bundle; then the first two.",
      [{"at": 0.1, "event": "vec4 row with both label rows"}, {"at": 0.3, "event": ".rgb bracket lifts three cells out"}, {"at": 0.58, "event": ".xy bracket lifts two cells out"}, {"at": 0.8, "event": "caption: swizzle"}],
      "LectureCodeTrace", "Picking parts is cells lifting out of a row; the two names for the same cells are the key fact.",
      "docs (Swizzling: .rgb, .xyz, .stp, equivalents); Lab 33-swizzle-pick (c.rgb and c.xy compile and give (0.4, 0.7, 0.6)); GLOSSARY (swizzle)")

lab("B17", 1, "swizzling: reordering parts changes the picture", "06-pastel-bgr.gdshader", f"{NS}/pastel-to-bgr.mp4", "Godot 4.7.2 · Forward+ · two real renders, dissolved",
    [{"at": 0.12, "lines": [5]}],
    "Code panel at left with the five-line shader whose COLOR line reads `vec4(c.bgr, 1.0)`; at right a framed real render that starts as the pastel gradient of the previous picture and dissolves into the same gradient with its colors turned over (top-left salmon, top-right violet, bottom-left lime, bottom-right cyan). Readout 'bgr' on the picture.",
    "The picture dissolves from the earlier colors to the reversed ones while the swizzle is highlighted.",
    [{"at": 0.12, "event": "COLOR line with .bgr highlighted"}, {"at": 0.36, "event": "the picture dissolves to the reversed colors"}],
    "manim with both pictures", "Seeing the same gradient with red and blue swapped is the effect of `.bgr`; both frames are real renders.",
    "C05: ffmpeg video, 14 s at 30 fps: 1.8 s hold of the real render of 05-pastel, 0.7 s dissolve, then a hold of the real render of 06-pastel-bgr to the end (both Lab stills 1920x1080, Forward+; re-time the dissolve to start at about 14 percent of the beat once the audio is measured). Probes of the second: (0.02,0.02) (0.702, 0.4118, 0.4118); (0.98,0.02) (0.702, 0.4118, 0.9882); (0.02,0.98) (0.702, 0.9843, 0.4118); (0.98,0.98) (0.702, 0.9843, 0.9882).",
    "Lab 06-pastel-bgr corner probes (reversed order of 05-pastel); 51-err-swizzle-sets",
    readouts=[{"at": 0.4, "text": "bgr", "x": 0.5, "y": 0.1}])

term("B18", 1, "the type on the left must match the type on the right", "44-err-vec3-to-color", "Godot 4.7.2 · shader compile error · printed by the engine",
     "A terminal window with the engine's own log of lab-shaders/44-err-vec3-to-color.gdshader, word for word: the source lines around `COLOR = c;` with that line marked, then 'Invalid arguments to operator '=': 'vec4, vec3'.' A ring lands on 'vec4, vec3'.",
     "The log lands line by line; a ring settles on the two type names that disagree.",
     [{"at": 0.1, "event": "log lines land"}, {"at": 0.65, "event": "ring on vec4, vec3"}],
     "Manim: a vec4 slot refusing a vec3 bundle", "The most common slip in a shader is a type that does not match; the engine's own words name both types.",
     "Lab 44-err-vec3-to-color (exit 1); logs/44-err-vec3-to-color.log (verbatim)")

manim("B19", 1, "the method: say the type of each piece, inside out", "TypeChain",
      "The expression `0.4 + 0.6 * vec3(UV, 0.5)` (35 characters) centered in monospace with `vec3 c =` to its left. Beneath it nested drawn brackets grow from the inside out, each landing a small type tag: under `UV` a bracket tagged vec2; under `vec3(UV, 0.5)` tagged vec3; under `0.6 * vec3(UV, 0.5)` tagged vec3; under the whole right-hand side tagged vec3; a final arrow into `c` tagged vec3.",
      "Brackets widen outward from UV, and a type tag lands on each as the voice says it.",
      [{"at": 0.1, "event": "the expression"}, {"at": 0.24, "event": "bracket on UV: vec2"}, {"at": 0.36, "event": "bracket on vec3(UV, 0.5): vec3"}, {"at": 0.62, "event": "bracket on 0.6 * ...: vec3"}, {"at": 0.8, "event": "whole right-hand side: vec3"}],
      "LectureCodeTrace", "Inside-out nesting IS the method; widening brackets with tags show it as shape, which a highlighted line cannot.",
      "Lab 05-pastel (the line compiles and draws the gradient); docs (operators and constructors)")

# ═════════════════════════════ ACT III · Your Own Functions ═════════════════════════════
manim("B20", 2, "a function's signature: return type, name, arguments", "Signature",
      "Act title 'Your Own Functions' (serif 40) top-left. The line `vec3 soften(vec3 c) {` in monospace (size 40) centered, with the body line `return 0.4 + 0.6 * c;` and a closing brace beneath it. Three drawn brackets under the first line land in order, each with a plain label: under `vec3` 'hands back', under `soften` 'name', under `(vec3 c)` 'arguments, each with a type'. Serif 32 caption: 'signature: the first line of a function'.",
      "Three brackets close in turn round the type, the name and the argument list.",
      [{"at": 0.08, "event": "act title; the function"}, {"at": 0.4, "event": "bracket: hands back"}, {"at": 0.62, "event": "bracket: name"}, {"at": 0.8, "event": "bracket: arguments"}],
      "LectureCodeTrace", "A signature is three parts of one line; brackets that close on each part in order are the clearest way to separate them.",
      "docs (Functions: syntax `ret_type func_name(args)`); Lab 09-soften-function compiles")

manim("B21", 2, "a call hands values in; return hands one value back, of the promised type", "CallAndReturn",
      "At left the call `soften(vec3(UV, 0.5))`; a small three-cell token travels along a drawn path into the argument slot `c` of a rounded box that holds `return 0.4 + 0.6 * c;`; the box pulses; a new three-cell token leaves the box and returns to the call, tagged 'vec3, as promised'. Then a four-cell token leaves the box instead and bounces off a drawn bar with a cross, with the engine's message in two short lines under it: `Expected return with an expression` / `of type 'vec3'.`",
      "A bundle goes into the function and a bundle comes back out; a bundle of the wrong size bounces.",
      [{"at": 0.1, "event": "call and box"}, {"at": 0.26, "event": "token travels into the argument"}, {"at": 0.4, "event": "token returns, tagged vec3"}, {"at": 0.66, "event": "wrong-size token bounces, message appears"}],
      "LectureCodeTrace", "In and out is a flow; a token entering and leaving the box makes 'hands values in, hands one value back' literal.",
      "Lab 45-err-return-type: Expected return with an expression of type 'vec3'.; 46-err-missing-return; 49-err-argument-type; docs (Functions)")

term("B22", 2, "define a function above the one that calls it", "47-err-call-before-define", "Godot 4.7.2 · shader compile error · printed by the engine",
     "A terminal window with the engine's own log of lab-shaders/47-err-call-before-define.gdshader, word for word: the source lines around the call `COLOR = vec4(soften(vec3(UV, 0.5)), 1.0);` with that line marked, then 'No matching function found for: 'soften'.' A ring lands on the message.",
     "The log lands line by line; a ring settles on the message that does not mention order.",
     [{"at": 0.1, "event": "log lines land"}, {"at": 0.68, "event": "ring on the message"}],
     "Manim: two function boxes with an arrow pointing up", "The order rule is about what Godot SAYS; the real message (which never mentions order) is the point.",
     "Lab 47-err-call-before-define (exit 1); logs/47-err-call-before-define.log; docs (Functions: 'only use functions that have been defined above')")

manim("B23", 2, "your function cannot see per-pixel built-ins", "TheWall",
      "Two rounded boxes: right, `fragment()` containing three outlined chips `UV`, `COLOR`, `TEXTURE`; left, a box `soften()` of your own. A thick gray vertical wall stands between them. The UV chip leaves fragment, crosses toward the function, hits the wall and bounces back; a small drawn bubble near the bounce reads 'unknown identifier'. Serif 32 caption: 'built-in: a value the engine hands to a function, or collects from it'.",
      "A chip travels toward the function, strikes the wall and is thrown back.",
      [{"at": 0.1, "event": "the two boxes, the wall, the chips"}, {"at": 0.34, "event": "caption: built-in"}, {"at": 0.62, "event": "UV chip bounces off the wall"}],
      "ShaderLab with the failing file", "A wall between two boxes is the picture of 'cannot see'; the bounce is the event.",
      "Lab 48-err-uv-in-function (Unknown identifier in expression: 'UV'.); scratch g-batch: UV, COLOR, TEXTURE, TEXTURE_PIXEL_SIZE, FRAGCOORD, SCREEN_UV, SCREEN_PIXEL_SIZE unknown inside a function; TIME, PI, TAU, E visible; docs (Built-ins)")

lab("B24", 2, "pass what you need in; a few built-ins are global", "10-pass-uv-in.gdshader", f"{NS}/pass-uv.png", "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.15, "lines": [3]}, {"at": 0.34, "lines": [8]}],
    "Code panel at left with the nine-line fixed shader: `vec3 soften(vec2 address)` and the call `soften(UV)`; at right a framed real render: the same pastel gradient as before. Caption under the render (one line, 72 characters): 'global: TIME (seconds on one clock shared by the whole game), PI, TAU, E'.",
    "The parameter line is highlighted, then the call; the same gradient sits beside them.",
    [{"at": 0.15, "event": "parameter line highlighted"}, {"at": 0.34, "event": "call line highlighted"}, {"at": 0.6, "event": "caption: global built-ins"}],
    "manim: UV passing through the wall", "The fix is code; the real file next to the unchanged picture proves it works.",
    "C06: Lab rect, lab-shaders/10-pass-uv-in.gdshader, still PNG 1920x1080, Forward+ (identical to the 05-pastel render: 0 pixels differ).",
    "Lab 10-pass-uv-in = 05-pastel (png-analysis); 11-global-time compiles (TIME inside a function); g-batch: PI, TAU, E compile",
    caption="global: TIME (seconds on one clock shared by the whole game), PI, TAU, E")

manim("B25", 2, "argument modes: in (a copy), inout (the original), out (write back)", "InOutInout",
      "Top strip: three chips with one-to-three-word captions, `in` 'a copy', `inout` 'the original', `out` 'writes back'; the active chip is ringed. Middle: the caller's variable box `a = 0.25`. Bottom: the function signature card, which changes with the active mode. IN (`float bump(float x)`): a ghost copy of 0.25 goes into the function, becomes 0.75 and returns to `b`; the box a still reads 0.25. INOUT (`void bump(inout float x)`): a double-headed drawn arrow ties the function to the box a itself, which changes to 0.75. OUT (`void make(out vec3 c)`): the function writes (0.1, 0.5, 0.9) into an empty three-cell box c in the caller.",
      "A copy changes and the original does not; then the original itself changes; then an empty box is filled.",
      [{"at": 0.1, "event": "in: copy goes in, a stays 0.25, b = 0.75"}, {"at": 0.4, "event": "inout: a becomes 0.75"}, {"at": 0.7, "event": "out: c filled with (0.1, 0.5, 0.9)"}],
      "LectureEvidenceTable of three modes", "Copy versus original is a thing moving or not moving; the table would list the words but not the difference.",
      "Lab 12-in-copy (0.25 stays, 0.75 returned), 13-inout (0.75), 14-out ((0.102, 0.502, 0.898)); docs (Functions: qualifiers; CORRECTED wording of 'in')")

rem("B26", 2, "built-in functions have signatures too (sin: a vec_type in, the same vec_type out)", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shader_functions.html",
     "image": f"{NS}/docs-shader-functions.png", "caption": "Godot 4.7 documentation · Built-in shader functions · captured at build time", "frame": "browser",
     "moves": [{"at": 0, "x": 0.5, "y": 0.4, "scale": 1}, {"at": 0.3, "x": 0.4, "y": 0.5, "scale": 1.6}], "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 'Built-in shader functions' page in a browser window, scrolled to the 'Trigonometric functions' table: three columns 'Return Type', 'Function', 'Description / Return value' with the rows radians, degrees, sin, cos, tan. The camera pushes in on the sin row, `vec_type` / `sin(vec_type x)` / 'Sine.', and a terracotta ring marks the signature.",
    "The camera pushes in on the sin row and the ring marks the type going in and the type coming out.",
    [{"at": 0, "event": "the docs page, trigonometric table"}, {"at": 0.3, "event": "push-in and ring on the sin signature"}],
    "LectureEvidenceTable of sin, mix, length signatures", "The signature belongs to the documentation, and the documentation itself is the evidence (SHOW-THE-THING).",
    "D1: Playwright capture of the live docs page (1600x900 at 2.4x) of the 'Trigonometric functions' table, read 2026-10-13: 'vec_type | sin(vec_type x) | Sine.'; the page's alias table (further up) says vec_type is float, vec2, vec3 or vec4, which the narration states", lane="remotion")

lab("B27", 2, "overloading: the argument type picks the function", "15-overload.gdshader", f"{NS}/overload.png", "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.1, "lines": [3, 6]}, {"at": 0.4, "lines": [11]}, {"at": 0.62, "lines": [12]}],
    "Code panel at left with the 14-line shader: two functions named get_color (one taking an int, one a float) and two calls, `get_color(1)` and `get_color(1.0)`; at right a framed real render: the left half teal, the right half sand. Readouts 'int: teal' on the left half and 'float: sand' on the right.",
    "The two function lines light, then each call lights as the matching half of the picture is named.",
    [{"at": 0.1, "event": "the two same-named functions"}, {"at": 0.4, "event": "get_color(1) highlighted; left half teal"}, {"at": 0.62, "event": "get_color(1.0) highlighted; right half sand"}],
    "manim: one name, two doors", "The result is a picture: one name, two different colors from the same-looking call, with the code that did it beside it.",
    "C07: Lab rect, lab-shaders/15-overload.gdshader, still PNG 1920x1080, Forward+. Probes: (0.25, 0.5) (0.3686, 0.6392, 0.5686) teal; (0.75, 0.5) (0.949, 0.8, 0.502) sand.",
    "Lab 15-overload probes; docs (Functions: overloading, int to float not implicit)",
    readouts=[{"at": 0.42, "text": "int: teal", "x": 0.25, "y": 0.1}, {"at": 0.66, "text": "float: sand", "x": 0.75, "y": 0.1}])

# ═════════════════════════════ ACT IV · Choices and Loops ═════════════════════════════
lab("B28", 3, "if/else needs a bool; scope ends at the closing brace", "16-split-if.gdshader", f"{NS}/split-if.png", "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.14, "lines": [7]}, {"at": 0.72, "lines": [6]}],
    "Act title 'Choices and Loops' (serif 40) top-left. Code panel at left with the 13-line shader: `vec3 c;` then an if/else on `UV.x < 0.5`; at right a framed real render: the left half teal, the right half pale. Readouts 'true' over the left half and 'false' over the right half.",
    "The condition line is highlighted and the left half is tagged true; then the declaration above the if is highlighted.",
    [{"at": 0.14, "event": "condition line highlighted; true on the left, false on the right"}, {"at": 0.72, "event": "vec3 c; line highlighted (declared above)"}],
    "manim: a branching arrow", "A bool deciding which half is which color is best shown on the real picture next to the exact condition.",
    "C08: Lab rect, lab-shaders/16-split-if.gdshader, still PNG 1920x1080, Forward+. Probes: (0.25, 0.5) (0.3686, 0.6392, 0.5686) teal; (0.75, 0.5) (0.949, 0.949, 0.949) pale.",
    "Lab 16-split-if probes; 50-err-if-float (Expected a boolean expression.); 54-err-scope (Unknown identifier in expression: 'c'.)",
    title="Choices and Loops", readouts=[{"at": 0.3, "text": "true", "x": 0.25, "y": 0.12}, {"at": 0.3, "text": "false", "x": 0.75, "y": 0.12}])

manim("B29", 3, "the ternary is a one-line if", "Collapse",
      "Top region: the six-line choice from lab-shaders/16-split-if (`vec3 c;` / `if (UV.x < 0.5) {` / `c = teal;` / `} else {` / `c = pale;` / `}`) collapses into the single line `vec3 c = UV.x < 0.5 ? teal : pale;` (34 characters) with thin drawn brackets labelled 'condition', 'if true', 'if false' under its three parts, the `?` and `:` ringed, and a serif 32 caption 'ternary: a one-line if'. Bottom region, never changing: ONE framed real render (lab_window of png/16-split-if.png: left half teal, right half pale) captioned 'Godot 4.7.2 · Forward+ · same pixels', with a drawn equals sign.",
      "Six lines fold into one while the picture below never changes.",
      [{"at": 0.1, "event": "the six-line choice and the picture"}, {"at": 0.32, "event": "the lines fold into one line"}, {"at": 0.62, "event": "brackets: condition, if true, if false"}, {"at": 0.82, "event": "equals sign: same pixels"}],
      "ShaderLab stack layout", "A fold from six lines to one with the picture held still is the claim 'same picture, one line'.",
      "Lab 17-split-ternary = 16-split-if (png-analysis: 0 of 230,400 pixels differ); docs (Flow control: ternary)")

lab("B30", 3, "a for loop with an int counter; float(i)", "18-stripes.gdshader", f"{NS}/stripes.png", "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.06, "lines": [5]}, {"at": 0.3, "lines": [7, 8, 9], "label": "abs: drops the minus sign: -0.3 becomes 0.3"}, {"at": 0.64, "lines": [6]}],
    "Code panel at left with the 12-line shader; at right a framed real render: five teal stripes on a pale field, evenly spaced. Readout 'five stripes' near the picture. The cue on the stripe test carries the label 'abs: drops the minus sign: -0.3 becomes 0.3' (the GLOSSARY wording; abs is on screen but not spoken).",
    "The loop line is highlighted, then the stripe test, then the float(i) line as the voice moves on.",
    [{"at": 0.06, "event": "for line highlighted"}, {"at": 0.3, "event": "stripe test highlighted; five stripes in the picture"}, {"at": 0.64, "event": "float(i) line highlighted"}],
    "manim: a counter stepping 0 to 4", "Five stripes from one loop is the payoff of the loop and is best shown as the real picture beside the loop.",
    "C09: Lab rect, lab-shaders/18-stripes.gdshader, still PNG 1920x1080, Forward+. Five stripes centered at 0.1, 0.3, 0.5, 0.7, 0.9 of the height (measured at 640x360: rows 25-46, 97-118, 169-190, 241-262, 313-334).",
    "Lab 18-stripes probes + png-analysis; 53-err-float-times-int-loop (Invalid arguments to operator '*': 'float, int'.)",
    readouts=[{"at": 0.34, "text": "five stripes", "x": 0.5, "y": 0.05}])

rem("B31", 3, "for when the count is known; while when it is not; infinite loops freeze", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html",
     "image": f"{NS}/docs-flow-control.png", "caption": "Godot 4.7 documentation · Flow control · captured at build time", "frame": "browser",
     "moves": [{"at": 0, "x": 0.5, "y": 0.35, "scale": 1}, {"at": 0.6, "x": 0.45, "y": 0.62, "scale": 1.6}], "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 'Flow control' section in a browser window: the for and while snippets with their comments, and the paragraph below them about infinite loops. The camera pushes in on that paragraph and a terracotta ring marks the sentence about freezing the application, including the editor.",
    "The camera drifts from the for and while snippets to the warning paragraph and rings it.",
    [{"at": 0, "event": "the for and while snippets"}, {"at": 0.6, "event": "push-in and ring on the infinite-loop warning"}],
    "manim: a loop arrow that never ends", "An infinite loop cannot be run safely, so the documentation's own warning is the honest evidence (SHOW-THE-THING).",
    "D2: Playwright capture of the live docs page (1600x900 at 2.4x), read 2026-10-13; the warning is not demonstrated by a run (it would freeze the machine)", lane="remotion")

manim("B32", 3, "compare floats against a range: nothing lands exactly on one half", "NoPixelLands",
      "Top: a schematic row of 12 outlined pixel cells with a dot at each cell center, an axis 0 to 1 and a vertical line at 0.5 that falls BETWEEN cells 6 and 7; the row is labelled 'schematic: 12 pixels'. Two code lines in monospace under it: `if (UV.x == 0.5)` and `if (abs(UV.x - 0.5) < 0.005)`, the second with a serif 32 label in the GLOSSARY wording, 'abs: drops the minus sign: -0.3 becomes 0.3'. A probe sweeps the row for the first test and no cell lights (label 'no pixel center is exactly 0.5'); for the second the two cells nearest 0.5 light teal. Bottom: two framed REAL renders side by side (lab_window of png/19-float-equals-1920.png, a pale field with nothing on it, and png/20-float-range-1920.png, the same field with a thin teal line), each captioned 'Godot 4.7.2 · Forward+ · 1920 pixels wide'.",
      "A probe finds no cell exactly on one half; the range test lights the two nearest; the real renders confirm it.",
      [{"at": 0.1, "event": "pixel row and the 0.5 line between two cells"}, {"at": 0.3, "event": "== test: probe sweeps, nothing lights"}, {"at": 0.62, "event": "range test: two cells light"}, {"at": 0.82, "event": "the two real renders"}],
      "ShaderLab with the two renders", "WHY nothing is drawn is a geometry fact (a line between cell centers); the real renders prove it on the real thing.",
      "Lab 19-float-equals at 640, 1280 and 1920 wide: no teal column; 20-float-range: 6, 12, 20 columns; at 641 and 1001 wide one column lit, at 321 none (png-analysis); docs (Flow control: compare against a range)")

rem("B33", 3, "two performance notes: discard has a cost; many branches can slow a shader", "LectureEvidenceTable",
    {"title": "Two performance notes", "headers": ["Keyword", "The documentation says"],
     "rows": [["discard (throws a pixel away)", "it has a performance cost"],
              ["if", "handled well when every pixel takes the same path; too many branches can slow a shader down"]],
     "note": "Godot 4.7 documentation · Shading language (Discarding) and Shader preprocessor (#if versus if) · not measured in this film",
     "cues": [0.15, 0.38], "durationSeconds": "__AUDIO__"},
    "A two-row table in the documentation's own words, each row ringed as it is spoken: 'discard (throws a pixel away)', 'it has a performance cost'; if, 'handled well when every pixel takes the same path; too many branches can slow a shader down'. The note line names the two documentation pages and says nothing here was measured.",
    "The ring moves from the discard row to the if row as the voice moves on.",
    [{"at": 0.15, "event": "discard row"}, {"at": 0.38, "event": "if row"}],
    "BrowserCapture of the preprocessor page", "Two short sourced statements with their pages named are what the evidence table is for; the 'if is slow' rumour is answered by the page that actually discusses branches.",
    "docs: Shading language > Discarding ('Beware that discard has a performance cost'); Shader preprocessor > '#if preprocessor versus if statement: Performance caveats' ('Modern GPUs are quite effective at performing static branching' ... 'too many branches ... can still slow down shader execution significantly'); text search of all shader tutorial pages 2026-10-13")

# ═════════════════════════════ ACT V · Read One Aloud ═════════════════════════════
lab("B34", 4, "the file again, read from the top", "01-breathe.gdshader", "", "",
    [{"at": 0.15, "lines": [1]}, {"at": 0.62, "lines": [3]}],
    "Act title 'Read One Aloud' (serif 40) top-left. The 14-line file alone on the stage, line numbers prominent (the next beats say 'line three', 'line six'). A focus box rests on line 1, then moves to line 3 where the reading will start.",
    "The focus box leaves the header and settles on line three, ready to read.",
    [{"at": 0.15, "event": "focus on line 1"}, {"at": 0.62, "event": "focus moves to line 3"}],
    "LectureCodeTrace", "The file with its line numbers is the stage for the next eight beats; ShaderLab shows all 14 lines at once.",
    "", "lab-shaders/01-breathe.gdshader (compiled in the Lab)", layout="code", title="Read One Aloud", lane="remotion")

manim("B35", 4, "reading the two uniform lines", "ReadUniforms",
      "Two lines in monospace (size 36), lines 3 and 4 of the file: `uniform vec4 tint : source_color;` and `uniform float speed = 2.0;`. Drawn tags land beneath their pieces: under `uniform` 'set from outside'; under `vec4` 'a color'; a bracket under `: source_color` labelled 'hint' with a small outlined round swatch and the label 'treated as a color'; a tag at the end of line 3 'no default: black'; under `float` 'a decimal number'; a bracket under `= 2.0` labelled 'default'. Serif 32 caption, in the GLOSSARY wording: 'hint: the word after a colon that tells Godot how to treat a uniform'.",
      "Tags fly out to the pieces of line three, then to the pieces of line four, as each is read.",
      [{"at": 0.06, "event": "line three; uniform and vec4 tags"}, {"at": 0.28, "event": "hint bracket, picker swatch"}, {"at": 0.56, "event": "no default: black"}, {"at": 0.8, "event": "line four: float and default tags"}],
      "ShaderLab with a label per cue", "Each piece of two real lines gets its own small tag in place; the whole-file panel can only label a line as a whole.",
      "Lab 27-unset-tint (an unset vec4 source_color uniform reads (0, 0, 0)); verify1.gd (ShaderMaterial.get_property_list: tint is a Color property, a plain vec4 is not; group 'Shader Parameters'); docs (hints table: source_color is 'Used as color')")

manim("B36", 4, "reading the signature of breathe", "ReadSignature",
      "Line 6 `vec3 breathe(vec3 base, float t) {` in monospace (size 36), centered. Drawn tags land beneath: `vec3` 'hands back a vec3'; `breathe` 'name'; `vec3 base` 'argument: vec3'; `float t` 'argument: float'. Below, a small three-cell token and a one-cell token flow into the parentheses and a three-cell token leaves, with the note 'the body must return a vec3'.",
      "Tags land on the four pieces of the signature, then a token flows through.",
      [{"at": 0.1, "event": "line six; return type tag"}, {"at": 0.3, "event": "name tag"}, {"at": 0.58, "event": "argument tags"}, {"at": 0.8, "event": "tokens in and out; must return vec3"}],
      "ShaderLab with a label per cue", "The same four pieces of one real line, read in place.",
      "Lab 01-breathe compiles; docs (Functions)")

manim("B37", 4, "reading the wave line", "ReadWave",
      "Line 7 `float wave = 0.5 + 0.5 * sin(t);` in monospace (size 36). Nested drawn brackets from the inside out with tags: `t` float; `sin(t)` float; `0.5 * sin(t)` float; `0.5 + 0.5 * sin(t)` float; into `wave` float. At the right (or below), a small drawn sine curve on axes marked -1 and 1, then squeezed and lifted to span 0 to 1, with a dot riding the curve.",
      "Brackets widen outward with a float tag on each; a sine curve is squeezed from -1..1 into 0..1.",
      [{"at": 0.1, "event": "the line"}, {"at": 0.26, "event": "brackets and float tags, inside out"}, {"at": 0.62, "event": "the sine curve squeezed into 0 to 1"}, {"at": 0.84, "event": "into wave"}],
      "LectureCodeTrace", "The range change from -1..1 to 0..1 is a curve being squeezed and lifted; the tags show the type never leaves float.",
      "Lab pulse-range.txt (the gray channel of the pulse stays within about 0.38 to 0.90); math: sine is between -1 and 1, so 0.5 + 0.5 * sine is between 0 and 1")

manim("B38", 4, "reading the return line with mix", "ReadReturn",
      "Line 8 `return mix(vec3(0.9), base, wave);` in monospace (size 36). Tags: `vec3(0.9)` 'fills all three: a pale gray' with a small gray swatch; `base` 'vec3'; `wave` 'float: 0 to 1'; the whole `mix(...)` 'vec3'; `return` 'matches the signature'. A serif 32 label in the GLOSSARY wording, 'mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b'. Below, a horizontal ramp strip from pale gray (left) to teal (right) with a terracotta dot that rides from the gray end to the teal end as wave goes from 0 to 1, labelled '0 gives the gray, 1 gives base'.",
      "A dot rides a gray-to-teal ramp as wave goes from zero to one while the tags land on the pieces.",
      [{"at": 0.1, "event": "the line"}, {"at": 0.24, "event": "vec3(0.9) tag and swatch; base; wave"}, {"at": 0.62, "event": "dot rides the ramp from gray to teal"}, {"at": 0.84, "event": "return matches the signature"}],
      "ShaderLab with a label per cue", "The ramp strip with a riding marker is the series' picture of a blend; the tags show the types fit.",
      "docs (mix: linear interpolation, `vec_type mix(vec_type a, vec_type b, float c)`); Lab pulse-range.txt (pale 0.90 to teal); 24-fill-vec3")

manim("B39", 4, "reading the two fragment lines", "ReadFragment",
      "Lines 12 and 13 in monospace (size 32): `vec3 color = breathe(tint.rgb, TIME * speed);` (45 characters) and `COLOR = vec4(color, tint.a);`. Tags land inside out: `tint.rgb` vec3 (swizzle); `TIME * speed` float; `breathe(...)` vec3; into `color` vec3; then `vec4(color, tint.a)` vec4 into `COLOR`, a vec4. Captions in serif 32: 'TIME: seconds on one clock shared by the whole game' and 'COLOR: the color of the pixel being drawn; fragment() sets it'.",
      "Tags land inside out on line twelve, then on line thirteen, ending on COLOR.",
      [{"at": 0.1, "event": "line twelve"}, {"at": 0.22, "event": "tint.rgb, TIME * speed, breathe(...) tags"}, {"at": 0.62, "event": "line thirteen: vec4(color, tint.a)"}, {"at": 0.82, "event": "COLOR takes a vec4"}],
      "ShaderLab with a label per cue", "Two real lines read inside out, with the types landing on each piece, are the film's method applied.",
      "Lab 01-breathe compiles; docs (swizzling; Fragment built-ins: COLOR, TIME)")

lab("B40", 4, "run it: every piece has a type and every type fits", "01-breathe.gdshader", f"{NS}/breathe-b40.mp4", "Godot 4.7.2 · Forward+ · tint set to teal",
    [{"at": 0.2, "lines": [7, 8]}, {"at": 0.6, "lines": [12, 13]}],
    "The same file and the same pulsing render as the opening picture, side by side. The wave and mix lines light first, then the two fragment lines.",
    "The pulse keeps running while the lines that make it light up.",
    [{"at": 0.2, "event": "wave and mix lines highlighted"}, {"at": 0.6, "event": "the two fragment lines highlighted"}],
    "manim: the file with all tags at once", "Closing the loop on the opening picture: the same real pulse, now readable.",
    "C01b: the same capture as C01a (same shader, same --set tint=#5FA391, live TIME) as a separate clip, with its OWN --time-origin chosen from THIS beat's measured audio by the same rule (for 11.6 s, t0 about 2.38 s gives 0.20 at both sample times).", "Lab 01-breathe + pulse-range.txt")

term("B41", 4, "one change, one refusal, caught by reading", "57-err-alpha-on-vec3", "Godot 4.7.2 · shader compile error · printed by the engine",
     "A terminal window with the engine's own log of lab-shaders/57-err-alpha-on-vec3.gdshader (the same file with the uniform changed to `vec3 tint`), word for word: the source lines around `COLOR = vec4(color, tint.a);` with that line marked, then 'Invalid member for 'vec3' expression: '.a'.' A ring lands on the message.",
     "The log lands line by line; a ring settles on the message about the missing member.",
     [{"at": 0.1, "event": "log lines land"}, {"at": 0.66, "event": "ring on 'Invalid member for vec3'"}],
     "ShaderLab with the changed file", "The film's method pays off as a caught mistake; the engine's own words are the proof.",
     "Lab 57-err-alpha-on-vec3 (exit 1); logs/57-err-alpha-on-vec3.log (verbatim)")

# ═════════════════════════════ write lanes + SHOTLIST ═════════════════════════════
(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(5):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

lanes_hist = {}
for e in E:
    lanes_hist[e["entry"]["lane"]] = lanes_hist.get(e["entry"]["lane"], 0) + 1
rows = []
for en in E:
    x = en["entry"]
    pick = f"{x['lane']} · {x.get('class') or x.get('pattern')}"
    rows.append(f"| {en['bid']} | {en['about']} | {pick} | {x['runner_up']} | {x['why']} | {en['evidence']} |")
sl = ["# Shot list: Godot Shader Language\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab capture of a tested file in `lab-shaders/`; every error shown is the engine's own log, word for word, from `evidence/planning-checks/logs/`. Seven things must be built or recorded first (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`; reused if the first shader film's build already made it). 2. **`shader_kit.py`** Manim helpers (same file). 3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` (same file; this film needs `--set`, `--time-origin`, a still PNG mode and two live-TIME clips of about 16 s and 12 s, nothing scripted). "
      "4. **`lab_window(png, width, caption)`** in the film's `scenes.py` (or `shader_kit.py`): an outlined frame holding a real Lab PNG with a one-line caption, used by B07, B08, B29 and B32. "
      "5. **Type-tag helper** in the film's `scenes.py`: a small outlined tag placed under a span of a code line with a bracket (B19, B35 to B39). "
      "6. **Docs screenshots D1 and D2** via Playwright (BrowserCapture convention). 7. **Terminal logs**: no capture needed; the lanes already carry the engine's lines verbatim from `evidence/planning-checks/logs/`.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
