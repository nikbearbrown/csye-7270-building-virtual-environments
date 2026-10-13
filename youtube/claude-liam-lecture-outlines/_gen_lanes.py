#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text, the cue lines must point at the right line numbers, the cue and readout times must
come from where the voice says the words (_sync.py), and the shot list must say exactly what the lanes say. Re-run after any edit:
    python3 _gen_lanes.py && python3 make_sheet.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _sync as Y  # noqa: E402

SH = HERE / "lab-shaders"
CHK = HERE / "evidence" / "planning-checks"
SCENES = CHK / "scenes"
E = []          # entries in beat order


# ───────────────────────────── helpers ─────────────────────────────
def lines_of(path):
    return Path(path).read_text().rstrip("\n").split("\n")


def code_of(fn, a=None, b=None):
    ls = lines_of(SH / fn)
    return "\n".join(ls[(a or 1) - 1:b])


def ln(fn, needle, nth=1, offset=0):
    """1-based number of the nth line of the DISPLAYED code that contains `needle` (offset = first displayed line - 1)."""
    seen = 0
    for i, line in enumerate(lines_of(SH / fn) if not str(fn).startswith("/") else lines_of(fn), 1):
        if needle in line:
            seen += 1
            if seen == nth:
                return i - offset
    raise KeyError(f"{fn}: no line {nth} containing {needle!r}")


def F(bid, phrase, k=0, lead=0.0):
    return Y.frac(bid, Y.when(bid, phrase, k, lead))


def box(cx, cy, w, h):
    return [round((cx - w / 2) / 1280, 3), round((cy - h / 2) / 720, 3), round((cx + w / 2) / 1280, 3), round((cy + h / 2) / 720, 3)]


def scene_info(sid):
    d = json.loads((SCENES / f"{sid}.json").read_text())
    return d


def add(bid, about, entry, evidence=""):
    E.append({"bid": bid, "act": Y.ACT_OF[bid], "about": about, "evidence": evidence, "entry": entry})


def manim(bid, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects)"):
    add(bid, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                     "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, about, sid, *, layout, label, intent, motion, show, runner, why, verified, evidence, shader=None, code=None, code_file=None,
        cues=None, readouts=None, rings=None, title=None, caption="", lane="capture"):
    info = scene_info(sid)
    still = bool(info.get("still"))
    ext = "png" if still else "mp4"
    if layout == "video":
        code, code_file = "", ""
    else:
        code = code if code is not None else code_of(shader)
        code_file = code_file or f"lab-shaders/{shader}"
    props = {"layout": layout, "code": code, "codeFile": code_file, "cues": cues or [], "video": f"godot-outlines/{sid}.{ext}", "videoLabel": label,
             "readouts": readouts or [], "rings": rings or [], "caption": caption, "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    kind = "still PNG" if still else f"{info['duration']:.1f} s clip (stretched to the measured audio), 30 fps"
    filt = "nearest filter" if all(sp.get("filter", "nearest") == "nearest" for sp in info["sprites"]) else "texture filter as the note says"
    spec = (f"{sid}: scene spec evidence/planning-checks/scenes/{sid}.json, {kind}, 1280x720 canvas rendered at 3840x2160, Forward+, {filt}. "
            f"{info['note'][0].upper() + info['note'][1:]}. Verified: {verified}")
    add(bid, about, {"lane": lane, "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": intent, "motion_claim": motion,
                     "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


def rem(bid, about, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                     "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


LABEL = "Godot 4.7.2 · Forward+ · the shader on the left"
GD_CALL = "Godot 4.7.2 · Forward+ · scripted input"
ONE_SPRITE_ROW = 0.93

# ───────────────────────────── ACT I · Ask the Neighbors ─────────────────────────────
lab("B01", "an outline switches on around a plain sprite", "C01-hook", layout="video", title="Ask the Neighbors",
    label="Godot 4.7.2 · Forward+ · same sprite, outline shader switched on",
    readouts=[{"at": 0.04, "text": "shader off", "x": 0.5, "y": ONE_SPRITE_ROW}, {"at": F("B01", "Watch what an outline does", 3, 0.2), "text": "shader on", "x": 0.5, "y": ONE_SPRITE_ROW}],
    intent="Act title 'Ask the Neighbors' (serif 40) top-left. A real Godot render in a framed window on the cream stage: the teal test sprite sits plain, then the outline shader switches on and a clean indigo line appears around its whole shape. Labels under the sprite: 'shader off', then 'shader on'.",
    motion="The sprite is plain, then a line appears around it the moment the shader switches on.",
    show=[{"at": 0.0, "event": "plain sprite, label 'shader off'"}, {"at": F("B01", "Watch what an outline does", 3), "event": "the outline switches on; label 'shader on'"}],
    runner="manim drawing of a sprite gaining a line", why="A real render is the honest picture of 'an outline switches on'; a drawing would only claim it.",
    verified="no outline pixels before the switch, a 12 px (3 image px x 4) line after it (planning check C01)",
    evidence="Lab render (C01); 08-loop compiled in the Lab")
lab("B02", "the bigger-copy trick gives uneven borders", "C02-bigcopy", layout="video",
    label="Godot 4.7.2 · Forward+ · a plus sign with a tinted copy behind it, scaled 6x to 7.2x",
    readouts=[{"at": F("B02", "the tips get a thick border", 0, 0.4), "text": "tip: thick", "x": 0.78, "y": 0.30}, {"at": F("B02", "the sides a thin one", 0, 0.0), "text": "side: thin", "x": 0.58, "y": 0.25}],
    rings=[{"at": F("B02", "the tips get a thick border", 0, 0.6), "box": box(798, 360, 74, 130)}, {"at": F("B02", "the sides a thin one", 0, 0.6), "box": box(740, 307, 110, 40)}],
    intent="A plus-shaped teal sprite on the stage with a tinted (indigo) copy behind it that grows by a fifth as the voice says it. The copy shows as a thick border at the four tips and a thin one along the sides. Labels 'tip: thick' and 'side: thin' with one ring on each.",
    motion="The copy swells out from behind the sprite: the border is fat at the tips and thin along the sides.",
    show=[{"at": F("B02", "Scale a plus sign up a fifth"), "event": "the copy starts to grow"}, {"at": F("B02", "the tips get a thick border"), "event": "tips thick"}, {"at": F("B02", "the sides a thin one"), "event": "sides thin"}],
    runner="manim drawing with measured tick marks", why="A real render of the actual trick, with the thickness measured (10 px at a tip against 3 px at a side), is more convincing than a drawing.",
    verified="tip border 10 px, side border 3 px, ratio about 3 (analyze_bigcopy H1); the scene frame at 6x to 7.2x reads 29 and 9 px (analyze_scenes C02)",
    evidence="verify_h_bigcopy.gd (tip 10 px, side 3 px)")
manim("B03", "each pixel asks: am I empty, with an opaque neighbor?", "TheQuestion",
      "A pixel grid (outline-only cells, no fill behind text) with the teal test sprite's silhouette as filled cells in the middle. One empty cell beside the sprite gets a terracotta ring and four short arrows to its four neighbors; the right neighbor is a filled cell and lights up. The ringed cell takes the line color (indigo) and a label reads 'on the outline'. Then a cell inside the sprite is asked: its own cell is opaque, label 'keeps its color', and it stays teal.",
      "A ring visits one empty cell, four arrows reach out, the right neighbor lights, the cell turns the line color; then a sprite cell is asked and keeps its color.",
      [{"at": F("B03", "The graphics card runs one small program for every pixel"), "event": "grid appears; a small program mark runs over every cell at once"}, {"at": F("B03", "Am I empty"), "event": "one empty cell ringed, four arrows"}, {"at": F("B03", "Then I am on the outline"), "event": "the cell takes the line color"}],
      "ShaderLab result", "The question is the concept: a grid of cells with one cell asking is the shape of the idea before any code appears.")
manim("B04", "reading the image at another address", "NextDoor",
      "The series' uv_square: a square with a 0 to 1 axis across the top and down the left side (the second axis pointing DOWN). A terracotta dot rests at the middle with the glossary line 'UV: a point's address on the shape, 0 to 1 across, 0 to 1 down'. A second dot hops one small step to the right with a short arrow and the label 'UV + step'. A one-line code label 'texture(TEXTURE, UV + step)' types in under the square, with the glossary line 'TEXTURE: the node's own picture; texture(TEXTURE, uv) reads it' beside it.",
      "The address dot hops one small step to the right, and the code line names exactly that hop.",
      [{"at": F("B04", "reads the sprite's image at another address"), "event": "square with axes, address dot at the middle"}, {"at": F("B04", "U V is the pixel's own address"), "event": "'UV' definition label"}, {"at": F("B04", "U V plus a small step"), "event": "the dot hops right; code line types in"}],
      "LectureCodeTrace with the single line", "An address that hops one step is a motion; the code line is the label, not the picture.")
manim("B05", "texture returns four numbers; dot a picks alpha", "FourNumbers",
      "One pixel's color drawn as four outline boxes in a row: r, g, b, a (monospace labels). The fourth box lifts out and drops onto a 0 to 1 scale with two marks: 0 'empty' (a swatch showing stage color through) and 1 'opaque' (a solid teal swatch). The code fragment '.a' is drawn beside the lifted box.",
      "The fourth box lifts out of the row and lands on a 0 to 1 scale, once at 0 and once at 1.",
      [{"at": F("B05", "four numbers, red, green, blue and alpha"), "event": "four boxes r g b a"}, {"at": F("B05", "Dot a picks the last one"), "event": "box a lifts out with '.a'"}, {"at": F("B05", "Alpha zero is empty"), "event": "scale marks 0 and 1 with swatches"}],
      "ClaudeCodeBeat with the line of code", "Four numbers with the last one lifted out is the picture of '.a'.")
manim("B06", "mix slides between two colors; outside zero to one it overshoots", "MixRamp",
      "The series' ramp strip as a color strip: the sprite's teal at the left end, the line indigo at the right end, end labels 0 and 1 and the glossary line 'mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b' above. A terracotta marker rides it to 0, then 0.5 (a blend), then 1. Then it continues past the right end to 2 and a small label 'overshoot' appears where the strip has ended.",
      "A marker rides a color strip from teal to indigo and then keeps going past the end of the strip.",
      [{"at": F("B06", "Mix blends two colors by an amount"), "event": "strip and formula"}, {"at": F("B06", "Amount zero keeps the sprite's color"), "event": "marker at 0, then 1"}, {"at": F("B06", "Outside zero to one, mix overshoots"), "event": "marker leaves the strip at 2"}],
      "LectureEvidenceTable", "A marker riding a strip is mix; overshoot is the marker leaving the strip.")
lab("B07", "first bug: no empty-check paints the sprite", "C07-paints-the-sprite", layout="side", shader="02-paints-the-sprite.gdshader", label=LABEL,
    cues=[{"at": F("B07", "Is the pixel on my right opaque"), "lines": [ln("02-paints-the-sprite.gdshader", "float around")]},
          {"at": F("B07", "mix in the line color"), "lines": [ln("02-paints-the-sprite.gdshader", "COLOR = mix")], "label": "mix: blends from a to b by t"}],
    readouts=[{"at": F("B07", "Look what happens"), "text": "all said yes", "x": 0.5, "y": ONE_SPRITE_ROW}],
    intent="Code card at left (the nine-line shader); at right a real Godot window: the plain sprite, then, as the voice says 'look what happens', the first try switches on and the whole sprite turns indigo except a thin teal crescent on its right edge.",
    motion="The around line is highlighted, then the COLOR line; then the plain sprite turns blue the moment the shader switches on.",
    show=[{"at": F("B07", "Is the pixel on my right opaque"), "event": "the around line"}, {"at": F("B07", "mix in the line color"), "event": "the COLOR line"}, {"at": F("B07", "Look what happens"), "event": "the shader switches on, the sprite turns blue; readout 'all said yes'"}],
    runner="LectureCodeTrace alone", why="The bug appearing: a plain sprite turns blue the moment the shader switches on, beside the code that did it.",
    verified="no outline pixels before the switch, then 95.8 percent of the sprite's pixels (71,112 of 74,192 at x4; 4,406 of 4,637 = 95.0 percent at 1:1) come out line coloured (analyze_scenes C07; analyze_lab A10)", evidence="Lab 02-paints-the-sprite (A10); scene C07")
lab("B08", "fix: multiply by how empty I am", "C08-one-question", layout="side", shader="03-one-question.gdshader", label=LABEL,
    cues=[{"at": F("B08", "Multiply by one minus my own alpha"), "lines": [ln("03-one-question.gdshader", "COLOR = mix")]}],
    readouts=[{"at": F("B08", "Only empty pixels"), "text": "left side only", "x": 0.2, "y": 0.5}],
    rings=[{"at": F("B08", "Only empty pixels"), "box": box(486, 360, 70, 300)}],
    intent="The same code card with the COLOR line highlighted and '* (1.0 - color.a)' marked; at right a real Godot window: the blue sprite of the first try, then, as the voice says 'multiply by one minus my own alpha', the fix switches on, the blue drains off and the sprite keeps its teal with only a thin indigo line along its left edge. One ring on the line, readout 'left side only'.",
    motion="The multiplication is highlighted and the blue fill drains off the sprite, leaving a line on its left edge.",
    show=[{"at": F("B08", "Multiply by one minus my own alpha"), "event": "the COLOR line highlighted; the fix switches on and the blue drains off"}, {"at": F("B08", "Only empty pixels"), "event": "ring on the left-edge line"}],
    runner="manim pixel grid", why="The fix acting: the blue visibly drains off the sprite as the one changed line is highlighted.",
    verified="before the fix 71,112 of 74,192 sprite px are line coloured; after it 3,080 outline px (x4), all left of the sprite's centre, none on the right, none on the sprite (analyze_scenes C08; 231 at 1:1, analyze_lab A2)", evidence="Lab 03-one-question (A2); scene C08")
lab("B09", "second bug: two neighbors give a sum of two", "C09-lighter-diagonals", layout="side", shader="04-lighter-diagonals.gdshader", label=LABEL,
    cues=[{"at": F("B09", "add the answers"), "lines": [ln("04-lighter-diagonals.gdshader", "float around"), ln("04-lighter-diagonals.gdshader", "+ texture(TEXTURE, UV + dy)")]},
          {"at": F("B09", "mix overshoots past the line color"), "lines": [ln("04-lighter-diagonals.gdshader", "COLOR = mix")]}],
    readouts=[{"at": F("B09", "the sum is two"), "text": "sum = 2", "x": 0.74, "y": 0.28}],
    rings=[{"at": F("B09", "the diagonal stretches come out lighter"), "box": box(749, 251, 120, 120)}, {"at": F("B09", "There, two neighbors are opaque"), "box": box(531, 469, 120, 120)}],
    intent="Code card (the four reads added into one number, no cap); at right a real Godot window: the one-sided line of the last beat, then, as the voice says 'all four sides', a ring appears around the sprite, its diagonal stretches visibly lighter (periwinkle) than the rest. Two rings on the lighter stretches, readout 'sum = 2'.",
    motion="The four sides switch on and a ring appears; the sum lines are highlighted, rings land on the lighter diagonal stretches, then the COLOR line.",
    show=[{"at": F("B09", "all four sides"), "event": "the one-sided line becomes a ring"}, {"at": F("B09", "add the answers"), "event": "the four-read sum"}, {"at": F("B09", "the diagonal stretches come out lighter"), "event": "ring on a lighter stretch"}, {"at": F("B09", "the sum is two"), "event": "readout 'sum = 2'"}],
    runner="manim ramp strip (the overshoot)", why="The real wrong color, with the code that causes it; the ramp-strip explanation already came one beat earlier.",
    verified="the one-sided line (3,080 px, all left of the centre) becomes a ring of 8,992 px of which 3,328 (37.0 percent) are (128,128,255) (analyze_scenes C09); at 1:1 252 of 672 (37.5 percent), the line colour doubled and clamped, on the diagonal stretches (analyze_lab A3, A11, A14)", evidence="Lab 04-lighter-diagonals (A3, A11, A14); scene C09")
lab("B10", "fix: cap the sum with min", "C10-four-questions", layout="side", shader="05-four-questions.gdshader", label=LABEL,
    cues=[{"at": F("B10", "Cap the sum with min"), "lines": [ln("05-four-questions.gdshader", "COLOR = mix")], "label": "min(a, b): the smaller of two values"}],
    readouts=[{"at": F("B10", "Now every pixel of the ring"), "text": "same blue", "x": 0.5, "y": ONE_SPRITE_ROW}],
    intent="The same code card with min(around, 1.0) marked; at right a real Godot window: the ring with lighter stretches, which settles, as the voice says 'so mix never overshoots', into a clean ring of one blue all the way round the sprite. Readout 'same blue'.",
    motion="min(...) is highlighted and the lighter stretches settle to the same blue as the rest.",
    show=[{"at": F("B10", "Cap the sum with min"), "event": "min highlighted"}, {"at": F("B10", "so mix never overshoots"), "event": "the lighter stretches settle to the same blue"}, {"at": F("B10", "Now every pixel of the ring"), "event": "readout 'same blue'"}],
    runner="manim 'min' clamp drawing", why="The fix acting: the light stretches visibly settle to the same blue as the cap is named.",
    verified="before the cap 3,328 of 8,992 ring px are the wrong colour, after it 0 (analyze_scenes C10; analyze_lab A3)", evidence="Lab 05-four-questions (A3); scene C10")

# ───────────────────────────── ACT II · Pixel-Sized Steps ─────────────────────────────
manim("B11", "a fraction of the picture is a different number of pixels on each image", "StepInPixels",
      "Act title 'Pixel-Sized Steps' (serif 40) top-left. Three horizontal image strips stacked, drawn the same width and made of 32, 64 and 128 outline cells; on each a terracotta bracket spans two percent of the width and a grey label counts the cells it covers: 0.64, 1.28 and 2.56. The 128 strip's bracket covers two and a half cells; the 32 strip's covers less than one. Caption 'step 0.02'.",
      "A bracket of the same relative width settles on three strips and covers a different number of cells on each.",
      [{"at": F("B11", "So far the step was point oh two"), "event": "act title, strips"}, {"at": F("B11", "two and a half here"), "event": "brackets land, counts 2.56 / 1.28 / 0.64"}, {"at": F("B11", "Pixel art needs steps of whole pixels"), "event": "counts held"}],
      "capture of three real renders at three sizes", "The claim is a unit conversion (fraction to pixels), best shown as cells; the real renders differ only subtly at a glance.",
      evidence="arithmetic: 0.02 x 32, 64, 128 (renders in evidence/planning-checks/png/sizes-*.png)")
rem("B12", "Godot's built-in for the size of one image pixel", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html",
     "image": "godot-outlines/docs-canvas-item-shader.png", "caption": "built-in: a value the engine hands to a function · docs, captured at build time",
     "moves": [{"at": 0, "x": 0.5, "y": 0.45, "scale": 1}, {"at": F("B12", "texture pixel size"), "x": 0.45, "y": 0.5, "scale": 1.6}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 'CanvasItem shaders' page in a browser window, scrolled to the fragment built-ins table; the camera pushes in on the TEXTURE_PIXEL_SIZE row and one terracotta ring marks it. The caption under the window gives the film's definition of a built-in and says where and when the page was captured.",
    "The camera pushes in on the row the voice is naming.",
    [{"at": 0.0, "event": "the page"}, {"at": F("B12", "texture pixel size"), "event": "push-in and ring on the TEXTURE_PIXEL_SIZE row"}],
    "manim: a text card with the formula", "The built-in is a documentation fact; the documentation page itself is the evidence (SHOW-THE-THING).",
    "Playwright capture of the live docs page (1600x900 at 2.4x) at build time; read 2026-10-13: the entry says the built-in is the size of one pixel of the default texture in address units, and gives a 64 x 32 image as its example (1/64 and 1/32)")
lab("B13", "thickness times texture pixel size: exactly N image pixels", "C13-thickness-steps", layout="side", shader="06-pixel-steps.gdshader", label=LABEL,
    cues=[{"at": F("B13", "Multiply it by a thickness"), "lines": [ln("06-pixel-steps.gdshader", "vec2 dx"), ln("06-pixel-steps.gdshader", "vec2 dy")], "label": "texture pixel size: one image pixel"},
          {"at": F("B13", "a uniform"), "lines": [ln("06-pixel-steps.gdshader", "uniform float thickness")]}],
    readouts=[{"at": F("B13", "Thickness one, two, three, four", 1, 0.1), "text": "1 px", "x": 0.2, "y": 0.5}, {"at": F("B13", "Thickness one, two, three, four", 3, 0.1), "text": "2 px", "x": 0.2, "y": 0.5},
              {"at": F("B13", "Thickness one, two, three, four", 4, 0.1), "text": "3 px", "x": 0.2, "y": 0.5}, {"at": F("B13", "Thickness one, two, three, four", 5, 0.1), "text": "4 px", "x": 0.2, "y": 0.5}],
    caption="uniform: a value your game sets from outside; every pixel sees the same one",
    intent="Code card at left (the four-read shader with TEXTURE_PIXEL_SIZE * thickness); at right a real Godot window: the line around the sprite steps from one image pixel wide to two, three and four as the voice counts. Readouts '1 px' ... '4 px'; a caption carries the glossary line for 'uniform'.",
    motion="The dx and dy lines are highlighted, then the thickness uniform; the ring thickens in steps.",
    show=[{"at": F("B13", "Multiply it by a thickness"), "event": "dx and dy lines"}, {"at": F("B13", "a uniform"), "event": "the uniform line"}, {"at": F("B13", "Thickness one, two, three, four", 1), "event": "1 px, 2 px, 3 px, 4 px"}],
    runner="manim ramp strip with a thickness marker", why="The real line widening one image pixel at a time, measured, next to the one multiplication that does it.",
    verified="axis widths exactly 1, 2, 3, 4 canvas px x scale at thickness 1 to 4 (analyze_lab A4; scene C13 measured at x4: 4, 8, 12, 16)", evidence="Lab 06-pixel-steps (A4)")
lab("B14", "the line color is a uniform too", "C14-line-color", layout="side", shader="06-pixel-steps.gdshader", label=LABEL,
    cues=[{"at": F("B14", "The line color is a uniform too"), "lines": [ln("06-pixel-steps.gdshader", "uniform vec4 line_color")]},
          {"at": F("B14", "this vec four is a color"), "lines": [ln("06-pixel-steps.gdshader", "uniform vec4 line_color")], "label": "vec4: a bundle of four numbers: red, green, blue, alpha"}],
    readouts=[{"at": F("B14", "Change the value"), "text": "magenta", "x": 0.5, "y": ONE_SPRITE_ROW}, {"at": F("B14", "and the line follows"), "text": "amber", "x": 0.5, "y": ONE_SPRITE_ROW}],
    caption="hint: the word after a colon that tells Godot how to treat a uniform",
    intent="The same code card with the line_color uniform line highlighted ('source_color' marked); at right a real Godot window: the line around the sprite changes from indigo to magenta to amber while nothing else moves. Caption carries the glossary line for 'hint'.",
    motion="The uniform line is highlighted and the line color changes twice.",
    show=[{"at": F("B14", "The line color is a uniform too"), "event": "line_color line highlighted"}, {"at": F("B14", "Change the value"), "event": "the line turns magenta, then amber"}],
    runner="manim colour chips", why="Changing the value and watching the real line follow is the whole claim.",
    verified="the ring colour read from the frames is the uniform's value each time (scene check C14)", evidence="Lab 06-pixel-steps with line_color changes (C14)")
manim("B15", "each read is a copy of the picture slid by the step", "GhostCopies",
      "The teal test circle drawn in the middle. Four ghost copies (grey circle outlines, each with a small terracotta dot at its center) slide out one step up, down, left and right and overlap. Where the ghosts stick out past the circle, the union is shaded in the line color: a ring. The original circle sits on top, teal, subtracting itself. Labels (1 to 3 words): 'read right', 'copy goes left', 'four copies', 'minus the sprite'.",
      "Four ghost copies slide out of the sprite, overlap, and the part that sticks out past the sprite fills with the line color.",
      [{"at": F("B15", "each read is the whole picture, slid by the step"), "event": "ghost copies slide out"}, {"at": F("B15", "Four reads are four slid copies"), "event": "four copies overlap"}, {"at": F("B15", "wherever the copies stick out"), "event": "the part past the sprite fills with the line color"}],
      "ShaderLab capture of the slid copies", "This is the model behind thickness, brush shape and thin-part gaps; a drawing of copies sliding says it where a render cannot.")
lab("B16", "the step counts image pixels, so the line grows with the sprite", "C16-scales", layout="video",
    label="Godot 4.7.2 · Forward+ · thickness 2 at sprite scale 1, 2, 3",
    readouts=[{"at": F("B16", "thickness two", 0, 0.0), "text": "2 px", "x": 0.5, "y": ONE_SPRITE_ROW}, {"at": F("B16", "four screen pixels", 0, 0.0), "text": "4 px", "x": 0.5, "y": ONE_SPRITE_ROW},
              {"at": F("B16", "Three times as big", 0, 0.8), "text": "6 px", "x": 0.5, "y": ONE_SPRITE_ROW}],
    intent="One real sprite at three sizes in turn (drawn 1x, 2x, 3x) with the same thickness 2: the line around it is two, then four, then six canvas pixels wide. Readouts '2 px', '4 px', '6 px' under it.",
    motion="The sprite doubles, then triples, and its line grows with it.",
    show=[{"at": F("B16", "Draw the sprite twice as big"), "event": "sprite doubles, line 4 px"}, {"at": F("B16", "Three times as big"), "event": "sprite triples, line 6 px"}],
    runner="manim: three sprites in a row", why="A line that visibly grows with the sprite, measured at each size, is the claim; three static sprites would not show growth.",
    verified="thickness 2 reads 2, 4, 6 canvas px at scales 1, 2, 3 (analyze_lab A7)", evidence="Lab 06-pixel-steps at three scales (A7)")
lab("B17", "four reads leave the corners of a square empty", "C17-corners", layout="video",
    label="Godot 4.7.2 · Forward+ · four reads (left) against eight reads (right)",
    readouts=[{"at": F("B17", "On a square sprite"), "text": "four reads", "x": 0.27, "y": ONE_SPRITE_ROW}, {"at": F("B17", "On a square sprite"), "text": "eight reads", "x": 0.73, "y": ONE_SPRITE_ROW},
              {"at": F("B17", "a three by three hole", 0, 0.2), "text": "3×3 hole", "x": 0.15, "y": 0.2}],
    rings=[{"at": F("B17", "a three by three hole"), "box": box(212, 232, 70, 70)}, {"at": F("B17", "Add the four diagonal neighbors"), "box": box(212, 232, 70, 70)}],
    intent="Two real square sprites (teal squares with the two cream eyes) side by side with the outline thickness stepping up to three: the left one (four reads) shows a square notch in each corner of its line, the right one (eight reads) is a complete frame. A ring on one empty corner and the readout '3×3 hole'.",
    motion="The line grows around both squares; the left one's corners stay empty while the right one's fill.",
    show=[{"at": F("B17", "On a square sprite"), "event": "labels 'four reads' and 'eight reads'"}, {"at": F("B17", "a three by three hole"), "event": "ring on an empty corner"}, {"at": F("B17", "Add the four diagonal neighbors"), "event": "the eight-read frame is complete"}],
    runner="manim: a square with the missing corner cells drawn", why="Real renders of the same sprite with both shaders, side by side, with the missing corner counted exactly (t squared pixels per corner).",
    verified="eight reads draw exactly 4 x t x t more pixels than four reads on a square: 4, 16, 36, 64 at t = 1 to 4 (analyze_crate K1)", evidence="verify_k_crate.gd (K1)")

# ───────────────────────────── ACT III · Say It with a Loop ─────────────────────────────
lab("B18", "eight reads written out", "C18-eight-reads", layout="side", shader="07-eight-reads.gdshader", title="Say It with a Loop", label=LABEL,
    cues=[{"at": F("B18", "the four sides"), "lines": [ln("07-eight-reads.gdshader", "float around"), ln("07-eight-reads.gdshader", "+ texture(TEXTURE, UV + dy)")]},
          {"at": F("B18", "the four corners"), "lines": [ln("07-eight-reads.gdshader", "UV + dx + dy"), ln("07-eight-reads.gdshader", "UV - dx + dy")]},
          {"at": F("B18", "eight nearly identical reads"), "lines": [ln("07-eight-reads.gdshader", "float around"), ln("07-eight-reads.gdshader", "UV - dx - dy")]}],
    intent="Act title 'Say It with a Loop' (serif 40) top-left. Code card at left: the eight-read shader (14 lines); the first two lines of reads are marked, then the two lines of corner reads, then all four read lines together. At right a real Godot window with the square sprite: with the four sides only, the corners of its line stay empty; as the voice says 'the four corners' they fill in and the frame is complete.",
    motion="Focus lands on the side reads, then the corner reads, and the empty corners of the line fill in; then all eight reads at once.",
    show=[{"at": F("B18", "the four sides"), "event": "side reads"}, {"at": F("B18", "the four corners"), "event": "corner reads; the empty corners fill in"}, {"at": F("B18", "eight nearly identical reads"), "event": "all eight reads"}],
    runner="manim: eight arrows around a cell", why="The corners filling in as the corner reads are named: the code's effect on the real picture, and the thing the next beat replaces.",
    verified="on the square sprite at thickness 3 the eight reads add exactly 576 canvas px (4 x 3 x 3 x 16) to the four-read line, the corner holes (analyze_scenes C18); same picture as the loop (analyze_lab A6: 0 pixels differ at thickness 1, 2, 3, 4, 8)", evidence="Lab 07-eight-reads (A6); scene C18")
lab("B19", "the loop says the read once", "C19-loop", layout="side", shader="08-loop.gdshader", label=LABEL,
    cues=[{"at": F("B19", "For each y from minus one to one"), "lines": [ln("08-loop.gdshader", "for (int y")]},
          {"at": F("B19", "and each x from minus one to one"), "lines": [ln("08-loop.gdshader", "for (int x")]},
          {"at": F("B19", "read the alpha at that offset"), "lines": [ln("08-loop.gdshader", "around +=")], "label": "offset: an amount added to slide something"},
          {"at": F("B19", "Nine offsets"), "lines": [ln("08-loop.gdshader", "for (int y"), ln("08-loop.gdshader", "around +=")]}],
    caption="for: repeat a block once for each value in a range",
    intent="Code card at left: the loop shader (14 lines); focus lands on the outer for, the inner for, the line that reads and adds, then the loop as a whole. At right the same complete frame on the square sprite, unchanged by rewriting the reads as a loop. A caption carries one plain line for 'for'.",
    motion="Focus steps into the loop: outer for, inner for, the read.",
    show=[{"at": F("B19", "For each y from minus one to one"), "event": "outer for"}, {"at": F("B19", "and each x from minus one to one"), "event": "inner for"}, {"at": F("B19", "read the alpha at that offset"), "event": "the read"}],
    runner="LectureCodeTrace alone", why="Paced line focus on the real code with its real result beside it.",
    verified="draws the same picture as the eight written-out reads: 0 pixels differ from the last frame of the previous capture (analyze_scenes C19; analyze_lab A6)", evidence="Lab 08-loop (A6); scene C19")
manim("B20", "the middle of the block is the pixel itself; float() is required", "ThreeByThree",
      "A 3 by 3 block of outline cells with offsets (-1,-1) to (1,1) written small in each cell and a terracotta center cell labelled 'me'. The nine cells light in loop order, row by row, and a '9 offsets' count ticks up. Beside it the one-line code 'vec2(float(x), float(y))' with the labels 'float: a decimal number' and 'vec2: a bundle of two numbers' on it, and under it a plain-shell box with the message the Shader Lab printed ('SHADER ERROR:' is the Lab's own prefix, the rest is the engine's text): SHADER ERROR: Invalid arguments for the built-in function: \"vec2(int,int)\".",
      "The nine cells light one after another in loop order and the middle one is marked as the pixel itself.",
      [{"at": F("B20", "The block's middle is the pixel itself"), "event": "block, nine cells light, middle marked"}, {"at": F("B20", "those float calls are not decoration"), "event": "code line appears"}, {"at": F("B20", "Here is its message"), "event": "the real compiler message"}],
      "CCPlainShell for the message", "A grid lighting in loop order is the loop; the real compiler text is shown as a boxed artifact inside it.",
      evidence="shaders/err-vec2-from-ints.gdshader through the Lab: exit 1 with the quoted message (lab-shaders-check.log)")
lab("B21", "the loop draws exactly the picture the eight written-out reads drew", "C21-same-picture", layout="video",
    label="Godot 4.7.2 · Forward+ · eight written-out reads (left), the loop (right)",
    readouts=[{"at": F("B21", "I rendered both"), "text": "eight reads", "x": 0.27, "y": ONE_SPRITE_ROW}, {"at": F("B21", "I rendered both"), "text": "loop", "x": 0.73, "y": ONE_SPRITE_ROW},
              {"at": F("B21", "Zero pixels differ"), "text": "0 pixels differ", "x": 0.5, "y": 0.08}],
    intent="Two real sprites side by side, the eight-read shader on the left and the loop on the right, their lines growing together through thickness one, two, three, four and eight; the two pictures stay identical at every step. Labels under each; at the end the readout '0 pixels differ'.",
    motion="Both rings grow in lockstep and stay identical.",
    show=[{"at": F("B21", "I rendered both"), "event": "labels, both rings"}, {"at": F("B21", "Zero pixels differ"), "event": "readout '0 pixels differ'"}],
    runner="manim table of five zeros", why="Watching two real pictures stay identical through the sweep is the evidence; a table of zeros is only the summary.",
    verified="0 pixels differ at thickness 1, 2, 3, 4 and 8, hard-edged sprite (analyze_lab A6; scene C21 frames)", evidence="Lab 07-eight-reads against 08-loop (A6)")
manim("B22", "reads per pixel, and what they cost in a stress test", "CostBars",
      "A horizontal bar chart on the cream stage: four bars grow left to right for a 3 by 3, 5 by 5, 7 by 7 and 9 by 9 block (10, 26, 50 and 82 reads per pixel), labelled with the measured milliseconds per frame (10, 24, 44 and 71, the whole-millisecond medians of the valid runs); a thin dashed floor line at 7.5 ms is labelled 'no shader'. A small grey credit: 'stress test: 403 million pixels a frame · Apple M4 Pro · Godot 4.7.2 · Forward+ · wall-clock, vsync off, median of runs · the card's own timer unreadable'. A last small caption: 'a 300 x 300 sprite: 90,000 pixels'.",
      "The bars grow in turn, each longer than the last, as the read count goes up.",
      [{"at": F("B22", "nine reads in the loop"), "event": "10-read bar grows (nine plus one)"}, {"at": F("B22", "ten reads took about ten milliseconds"), "event": "bar labels, floor line"}, {"at": F("B22", "a nine by nine block"), "event": "the 9 by 9 bar (82 reads), the longest; credit line"}],
      "LectureEvidenceTable", "Bars growing with the read count show 'time follows reads'; a table would only list the numbers.",
      evidence="verify_g_cost.gd: G1 GPU timer 0.0 (unavailable), G2 wall-clock medians (cost-summary.txt)")
manim("B23", "an if on the thickness skips the loop", "Guard",
      "A code card (monospace, 17 lines) of the guard shader with the line 'if (thickness > 0.0) {' and its closing brace highlighted. Beside it a small pixel grid where every cell follows the same arrow: with thickness 0 all cells go to 'skip: one read'; a switch flips to thickness 2 and all cells go to 'read ten'. Under the card a plain-shell box with the message the Shader Lab printed ('SHADER ERROR:' is the Lab's own prefix, the rest is the engine's text): SHADER ERROR: Using 'return' in the 'fragment' processor function is incorrect.",
      "One switch flips and every cell changes its arrow together; the loop lines dim when the guard is false.",
      [{"at": F("B23", "Many outline shaders wrap the loop in an if"), "event": "code card, the if highlighted"}, {"at": F("B23", "Thickness zero means off"), "event": "all cells to 'skip'; loop lines dim"}, {"at": F("B23", "a return inside fragment is a compile error"), "event": "the compiler message"}],
      "ShaderLab with 09-guard code", "The idea is one switch everyone obeys; a grid of cells taking the same arrow shows it where a render cannot.",
      evidence="09-guard in the Lab (exit 0); shaders/err-return-in-fragment.gdshader exit 1 with the quoted message")
manim("B24", "is an if slow? only when neighbors disagree", "Agree",
      "Two pixel grids side by side. Left, titled 'per-pixel test': cells are split in two colors along the sprite's edge and the boundary cells hold different arrows (they disagree) and are ringed in terracotta. Right, titled 'thickness > 0.0': every cell holds the same arrow (they agree). Grey attribution under the left grid: 'GPU Gems 2, chapter 34, 2005'. Grey line under the right: 'shading language docs: no warning for if'.",
      "Arrows appear in each cell; on the left the edge cells point two ways, on the right every arrow is the same.",
      [{"at": F("B24", "Is an if slow"), "event": "two grids"}, {"at": F("B24", "A graphics book from two thousand five"), "event": "left grid: edge cells disagree"}, {"at": F("B24", "so they all agree"), "event": "right grid: all arrows the same"}],
      "LectureEvidenceTable of the two quotes", "Disagreeing neighbors against agreeing ones is a picture of the idea; the quotes are the captions.",
      evidence="Godot 4.7 shading language, flow control and discard sections; NVIDIA GPU Gems 2 chapter 34 (Harris and Buck, 2005)")
lab("B25", "thickness zero should change nothing; without the guard it does", "C25-zero-means-zero", layout="video",
    label="Godot 4.7.2 · Forward+ · soft-edged sprites, thickness 2 then 0",
    readouts=[{"at": F("B25", "Without it"), "text": "no guard", "x": 0.26, "y": ONE_SPRITE_ROW}, {"at": F("B25", "Without it"), "text": "guard", "x": 0.74, "y": ONE_SPRITE_ROW},
              {"at": F("B25", "two hundred and twenty-four pixels"), "text": "224 pixels", "x": 0.26, "y": 0.1}],
    rings=[{"at": F("B25", "half-transparent rim"), "box": box(330, 360, 330, 330)}],
    intent="Two real soft-edged sprites side by side, both ringed at thickness two; then thickness drops to zero: the right one (guard) returns to its plain look, the left one (no guard) keeps a thin tinted rim. Labels 'no guard' and 'guard', one ring round the left sprite's rim, readout '224 pixels'.",
    motion="Both rings switch off; one sprite is clean, the other still has a tinted rim.",
    show=[{"at": F("B25", "Without it"), "event": "labels; both rings go to zero"}, {"at": F("B25", "half-transparent rim"), "event": "ring on the left rim"}],
    runner="manim: pixel row of the rim with alpha values", why="Two real sprites at thickness zero, one clean and one tinted, is the evidence; the count is the readout.",
    verified="no guard: 224 rim pixels change colour (216 change alpha); guard: 0; hard-edged sprite: 0 either way (planning check B2)", evidence="verify_b_soft.gd (B2)")
lab("B26", "the game sets thickness from code", "C26-select", layout="side", shader="08-loop.gdshader", code=(CHK / "select_snippet.gd").read_text().rstrip("\n"),
    code_file="scene script (GDScript) · evidence/planning-checks/select_snippet.gd", label=GD_CALL,
    cues=[{"at": F("B26", "Your game turns the dial"), "lines": [ln(str(CHK / "select_snippet.gd"), "_unhandled_key_input")]},
          {"at": F("B26", "set thickness to two"), "lines": [ln(str(CHK / "select_snippet.gd"), "set_shader_parameter(\"thickness\", 2.0")]},
          {"at": F("B26", "The call is set shader parameter"), "lines": [ln(str(CHK / "select_snippet.gd"), "set_shader_parameter(\"thickness\", 2.0")]}],
    readouts=[{"at": 0.04, "text": "scripted input", "x": 0.5, "y": 0.06}],
    caption="material: tells Godot how to draw a surface; it holds the shader",
    intent="Code card at left: the 11-line GDScript (a selected flag, _ready setting thickness 0, a key handler that sets 2 or 0); at right the real Godot window running it: no line, then a scripted key press at the word 'selected' draws the outline, a second press removes it. A label 'scripted input' stays on screen.",
    motion="The key handler lights up and the line around the sprite appears and disappears with each press.",
    show=[{"at": F("B26", "Your game turns the dial"), "event": "the handler"}, {"at": F("B26", "When the unit is selected", 4), "event": "first scripted press: line on"}, {"at": F("B26", "When it is not", 3), "event": "second scripted press: line off"}],
    runner="LectureCodeTrace with the script alone", why="Cause (one call) and effect (the line) together; the script is the exact text that was run.",
    verified="0 outline px before, 632 after the first key, 0 after the second; thickness reads back 0.0 (verify_j J1)", evidence="verify_j_select.gd (J1)")
lab("B27", "units from one scene share a material; an instance uniform is per node", "C27-shared-material", layout="video",
    label="Godot 4.7.2 · Forward+ · two units, one material",
    readouts=[{"at": F("B27", "so every unit lights up at once"), "text": "both lit", "x": 0.5, "y": ONE_SPRITE_ROW}, {"at": F("B27", "set it on the node instead"), "text": "one lit", "x": 0.5, "y": ONE_SPRITE_ROW}],
    caption="instance uniform: its own value on each node that shares the material",
    intent="Two real units side by side that share one material. The dial is set on the left unit and BOTH light up (readout 'both lit'); then the shader declares the uniform as instance, each node gets its own value, and only the left unit stays lit (readout 'one lit'). A caption gives the film's definition of an instance uniform (the series' wording).",
    motion="One unit is selected and both light up; after the fix, one unit is selected and only it lights up.",
    show=[{"at": F("B27", "so every unit lights up at once"), "event": "both units ringed"}, {"at": F("B27", "Declare the uniform as instance", 4), "event": "the shader switches to the instance uniform; only the left ring stays"}],
    runner="manim: two boxes pointing at one material", why="The real surprise (two nodes, one dial) and its real cure, in one clip.",
    verified="shared material: setting 3 on one unit draws 960 px on it and 960 px on the other; instance uniform on a shared material: 960 px on one, the other keeps its own value (verify_j J2, J3)", evidence="verify_j_select.gd (J2, J3)")

# ───────────────────────────── ACT IV · Room to Draw ─────────────────────────────
lab("B28", "a shader paints only inside the sprite's own rectangle", "C28-slide-clip", layout="side", shader="01-look-right.gdshader", title="Room to Draw", label=LABEL,
    cues=[{"at": F("B28", "Read a step to the right"), "lines": [ln("01-look-right.gdshader", "COLOR = texture")]}],
    readouts=[{"at": F("B28", "cut off flat"), "text": "sliced flat", "x": 0.2, "y": 0.5}],
    rings=[{"at": F("B28", "only inside the sprite's own rectangle"), "box": box(640, 360, 512, 512)}],
    caption="docs: fragment() runs only for pixels the node's shape covers",
    intent="Act title 'Room to Draw' (serif 40) top-left. Code card at left: the seven-line look-right shader. At right a real Godot window: the sprite slides left as the step grows, and when it reaches the left edge of its rectangle it is sliced off flat. A ring marks the whole image rectangle at the end; caption credits the docs.",
    motion="The sprite slides left and the left side of it is cut off flat at the edge of the rectangle.",
    show=[{"at": F("B28", "Read a step to the right"), "event": "the code line; the sprite slides left"}, {"at": F("B28", "cut off flat"), "event": "readout 'sliced flat'"}, {"at": F("B28", "only inside the sprite's own rectangle"), "event": "ring round the image rectangle"}],
    runner="manim: a rectangle with a shape pushed past its edge", why="A real sprite really sliced at its rectangle's edge is the strongest picture of 'a shader paints only inside its rectangle', and it sets up the padding trap.",
    verified="look 0.125 slides the sprite 16 image px left exactly; at 0.25 the left 6.4 image px are cut by the rectangle (analyze_lab A1; scratch A)", evidence="Lab 01-look-right (A1); verify_a_padding.gd")
lab("B29", "a sprite trimmed to its shape has no room for the line", "C29-tight", layout="video",
    label="Godot 4.7.2 · Forward+ · the sprite trimmed to its shape, thickness 0 to 4",
    readouts=[{"at": F("B29", "trimmed to its shape"), "text": "no empty border", "x": 0.5, "y": ONE_SPRITE_ROW}],
    rings=[{"at": F("B29", "nothing appears where the shape touches the edge"), "box": box(640, 206, 130, 56)}, {"at": F("B29", "nothing appears where the shape touches the edge", 0, 0.5), "box": box(794, 360, 56, 130)},
           {"at": F("B29", "The line has nowhere to go"), "box": box(640, 514, 130, 56)}, {"at": F("B29", "The line has nowhere to go", 0, 0.3), "box": box(486, 360, 56, 130)}],
    intent="A real sprite whose image was trimmed to its round shape (no transparent border). The outline is turned up from zero to four; the line shows in the corners but is cut flat where the circle touches the top, right, bottom and left edges of the image. Four rings on those four places, readout 'no empty border'.",
    motion="The outline grows around the circle and is missing at the four places where it touches the edge of the image.",
    show=[{"at": F("B29", "Turn the outline up to four"), "event": "the line grows"}, {"at": F("B29", "nothing appears where the shape touches the edge"), "event": "rings on the four missing places"}],
    runner="manim: a circle inside its square with arrows blocked", why="The real failure, in the real shader, with the real trimmed art.",
    verified="axis widths 0, 0, 0, 0 on the trimmed sprite at thickness 4; 808 line px against 1,296 for the padded art (analyze_padding P1)", evidence="verify_a_padding.gd")
rem("B30", "the padding function", "LectureCodeTrace",
    {"title": "Add transparent padding", "code": "\n".join(lines_of(CHK / "padding_snippet.gd")[2:]), "note": "GDScript · evidence/planning-checks/padding_snippet.gd (the 'extends Node' line left out) · Godot 4.7 Image reference",
     "cues": [F("B30", "The fix is padding"), F("B30", "The fix is padding", 1), F("B30", "transparent pixels around", 0), F("B30", "transparent pixels around", 2), F("B30", "around the image", 2),
              F("B30", "make a bigger transparent image"), F("B30", "bigger transparent image", 2), F("B30", "bigger transparent image", 3), F("B30", "copy the original into the middle"), F("B30", "and make a texture from it")], "durationSeconds": "__AUDIO__"},
    "A cream code card with the ten-line add_padding function: line focus walks through the signature and the get_image line, then the bigger transparent image (create_empty and fill), then the blit_rect copy, then the texture it returns. A caption gives the meaning of blit_rect in the film's own words: 'copy a piece of one image into another'.",
    "Focus steps down the function as the voice describes it.",
    [{"at": F("B30", "The fix is padding"), "event": "signature and get_image"}, {"at": F("B30", "make a bigger transparent image"), "event": "create_empty and fill"}, {"at": F("B30", "copy the original into the middle"), "event": "blit_rect"}, {"at": F("B30", "and make a texture from it"), "event": "return"}],
    "manim code card with an image diagram", "The function is real code that was run (padding result in the next beat); paced line focus is exactly 'here is how'.",
    "padding_snippet.gd run in verify_a_padding.gd: padded size 85 x 85 from 77 x 77 at pad 4")
lab("B31", "pad by at least the thickest line", "C31-padding", layout="video",
    label="Godot 4.7.2 · Forward+ · the trimmed sprite padded by 0, 2 and 4 pixels, thickness 4",
    readouts=[{"at": F("B31", "No padding"), "text": "no padding", "x": 0.19, "y": ONE_SPRITE_ROW}, {"at": F("B31", "Two pixels of padding"), "text": "2 px padding", "x": 0.5, "y": ONE_SPRITE_ROW},
              {"at": F("B31", "Four: the full ring"), "text": "4 px padding", "x": 0.81, "y": ONE_SPRITE_ROW}],
    intent="Three real copies of the trimmed sprite in a row at the same thickness four, padded by none, two and four pixels with the function from the previous beat: the left line is cut off, the middle cut at two pixels, the right a complete ring. Labels under each.",
    motion="The line grows around all three; only the one padded by four gets a full ring.",
    show=[{"at": F("B31", "No padding"), "event": "left cut off"}, {"at": F("B31", "Two pixels of padding"), "event": "middle cut at two"}, {"at": F("B31", "Four: the full ring"), "event": "right full ring"}],
    runner="manim: three squares with a ring growing", why="Three real results of the same function, side by side, with the widths measured.",
    verified="axis widths 0, 2, 4 at thickness 4 with padding 0, 2, 4; line pixels 808, 1,104, 1,296; the padded art matches the original 1,296 (analyze_padding P1); a non-centered Sprite2D moves by the padding (4, 4) (verify_a log)", evidence="verify_a_padding.gd")
lab("B32", "on a sprite sheet the addresses cover the whole sheet", "C32-sheet", layout="video",
    label="Godot 4.7.2 · Forward+ · a packed two-frame sheet, frame 1 outlined at thickness 4",
    caption="docs: with a custom shader, a Sprite2D's UV spans its whole texture",
    readouts=[{"at": F("B32", "A sprite sheet"), "text": "whole sheet", "x": 0.27, "y": ONE_SPRITE_ROW}, {"at": F("B32", "A sprite sheet"), "text": "frame 1", "x": 0.7, "y": ONE_SPRITE_ROW},
              {"at": F("B32", "draws a stray line"), "text": "stray line", "x": 0.55, "y": 0.2}],
    rings=[{"at": F("B32", "draws a stray line", 0, 0.5), "box": box(772, 360, 44, 262)}],
    intent="At left the whole packed sheet (a solid teal frame with two eyes beside the disc frame); at right only frame 1 on its own, outlined at thickness four: a tall stray line runs down its left edge, drawn from the solid frame next door. Ring on the stray line, readouts 'whole sheet', 'frame 1', 'stray line', a caption crediting the docs.",
    motion="The outline switches on and a stray line appears along the frame's left edge.",
    show=[{"at": F("B32", "A sprite sheet"), "event": "the sheet and the single frame"}, {"at": F("B32", "draws a stray line"), "event": "the stray line; ring"}],
    runner="BrowserCapture of the Sprite2D docs", why="The real stray line in the real frame, with the docs sentence as the caption; the docs page alone would not show the damage.",
    verified="UV.x runs 0.506 to 0.996 across frame 1 (the whole sheet's space); a 4 image px (16 canvas px at x4) stray line; the same with region_enabled and with AtlasTexture frames; separate frame images follow the shown frame, outline margin 3 on every side for both (analyze_sheets C3); verify_c C1 to C4", evidence="verify_c_sheets.gd (C1 to C4)")
lab("B33", "clamp each read into the visible frame", "C33-sheet-clamp", layout="side", shader="12-sheet-safe.gdshader", label=LABEL,
    code=code_of("12-sheet-safe.gdshader", 6, 14), code_file="lab-shaders/12-sheet-safe.gdshader · lines 6 to 14",
    cues=[{"at": F("B33", "region rect"), "lines": [1, 2], "label": "REGION_RECT: the part of the texture the sprite shows"}, {"at": F("B33", "Clamp each read into it"), "lines": [8], "label": "clamp(x, lo, hi): keep x between lo and hi"}],
    readouts=[{"at": F("B33", "Clamp each read into it", 0, 0.5), "text": "stray line", "x": 0.55, "y": 0.2}, {"at": F("B33", "the stray line is gone"), "text": "gone", "x": 0.55, "y": 0.2}],
    caption="docs: UV spans the whole texture; REGION_RECT is the visible region",
    intent="Code card at left: eight lines of the sheet-safe shader (the lo and hi corners from REGION_RECT, and the clamp around each read). At right the same two-panel sheet scene: the stray line is there, then as the clamp is named it disappears while the disc's own ring stays. Readout 'stray line' then 'gone'.",
    motion="The clamp line is highlighted and the stray line vanishes from the frame's edge.",
    show=[{"at": F("B33", "region rect"), "event": "lo and hi lines"}, {"at": F("B33", "Clamp each read into it"), "event": "the clamp line; the stray line vanishes"}],
    runner="manim: arrows bent back at the frame border", why="The real stray line really disappearing is the proof; the excerpt of real code shows what did it.",
    verified="REGION_RECT = (0.5, 0, 0.5, 1) (read as 0.502, the 8-bit value of 0.5) for hframes, region_enabled, an AtlasTexture sprite and an AnimatedSprite2D atlas frame; with the clamp the stray line is 0 px and the disc's ring is intact (verify_f F1 to F4, verify_i I3)", evidence="verify_f_region.gd; verify_i_sizes.gd (I3)")

# ───────────────────────────── ACT V · Where It Breaks ─────────────────────────────
lab("B34", "push the thickness: the brush shows its shape", "C34-brushes", layout="video", title="Where It Breaks",
    label="Godot 4.7.2 · Forward+ · four reads, eight reads, a ring of sixteen; thickness 1 to 8",
    readouts=[{"at": F("B34", "the four-read line"), "text": "four reads", "x": 0.17, "y": ONE_SPRITE_ROW}, {"at": F("B34", "The eight-read line"), "text": "eight reads", "x": 0.5, "y": ONE_SPRITE_ROW},
              {"at": F("B34", "A ring of sixteen"), "text": "sixteen reads", "x": 0.83, "y": ONE_SPRITE_ROW}],
    intent="Act title 'Where It Breaks' (serif 40) top-left. Three real sprites in a row, each with a different outline shader, the thickness growing together from one to eight: the left (four reads) pinches in at the diagonals, the middle (eight reads) bulges into a rounded square, the right (sixteen reads) stays round. Labels under each.",
    motion="Three lines grow together and take three different shapes.",
    show=[{"at": F("B34", "the four-read line"), "event": "left pinches"}, {"at": F("B34", "The eight-read line"), "event": "middle becomes a rounded square"}, {"at": F("B34", "A ring of sixteen"), "event": "right stays round"}],
    runner="manim: three outlines drawn from the formula", why="The real shapes, from the real shaders, growing side by side.",
    verified="at thickness 8 the line is 8 px on the axes and about 5.1, 11.4 and 8.1 px on the diagonal for four, eight and sixteen reads, measured on the capture's own frames at x3 (analyze_scenes C34; the 1:1 Lab renders read 5.1, 11.4 and 8.5, analyze_lab A5)", evidence="Lab 06-pixel-steps, 07-eight-reads, 10-ring (A5)")
manim("B35", "the reads are the brush; measured diagonal thickness", "BrushShapes",
      "Three dot patterns around a center pixel: four terracotta dots in a diamond, eight in a square, sixteen on a circle, each with a faint grey ghost footprint behind it. Under each pattern a small disc outline with two tags, one on the axis and one at 45 degrees, carries the measured numbers: 'axis 8' on all three and 'diagonal 5.1' (four), 'diagonal 11.4' (eight), 'diagonal 8.1' (sixteen). Caption 'thickness 8 · measured on this render'.",
      "The dots appear in a diamond, a square and a circle, and the measured numbers land under them.",
      [{"at": F("B35", "The reads are the brush"), "event": "three dot patterns"}, {"at": F("B35", "Four make a diamond"), "event": "diamond, square, circle named in turn"}, {"at": F("B35", "Straight across"), "event": "'axis 8' under each pattern"}, {"at": F("B35", "I measured about five, eleven, and eight"), "event": "the diagonal numbers"}],
      "LectureEvidenceTable of the numbers", "The shape of the brush is the pattern of the reads; drawing the patterns shows why the numbers are what they are.",
      evidence="Lab renders at thickness 8 (analyze_lab A5)")
lab("B36", "the ring of sixteen, and its cost", "C36-ring", layout="side", shader="10-ring.gdshader", label=LABEL,
    cues=[{"at": F("B36", "sixteen angles around a full turn"), "lines": [ln("10-ring.gdshader", "for (int i")]}, {"at": F("B36", "one distance"), "lines": [ln("10-ring.gdshader", "float angle"), ln("10-ring.gdshader", "vec2 dir")]},
          {"at": F("B36", "Seventeen reads"), "lines": [ln("10-ring.gdshader", "around +=")]}],
    readouts=[{"at": F("B36", "thirty-seven milliseconds"), "text": "sin/cos: 37 ms", "x": 0.3, "y": ONE_SPRITE_ROW}, {"at": F("B36", "sixteen with the directions"), "text": "constants: 16 ms", "x": 0.7, "y": ONE_SPRITE_ROW}],
    caption="stress test: 403 million pixels a frame · Apple M4 Pro · wall-clock",
    intent="Code card at left: the 14-line ring shader; focus lands on the for, then the angle and direction lines, then the read. At right the ring on the sprite growing to thickness eight. Two readouts under it, 'sin/cos: 37 ms' and 'constants: 16 ms', with the stress-test credit as caption.",
    motion="Focus lands on the loop, the angle and the read; the line grows round.",
    show=[{"at": F("B36", "sixteen angles around a full turn"), "event": "the for line"}, {"at": F("B36", "one distance"), "event": "angle and direction lines"}, {"at": F("B36", "thirty-seven milliseconds"), "event": "readouts"}],
    runner="manim code card", why="The real code with the real round result; the two timings are labelled with the test that made them.",
    verified="the ring and the constant-directions ring draw identical pictures (0 pixels differ); stress test about 37 ms against about 16 ms per frame (cost-summary.txt)", evidence="Lab 10-ring; verify_g_cost.gd (ring-const)")
lab("B37", "thin parts: eight reads jump over a three-pixel stem", "C37-stem", layout="video",
    label="Godot 4.7.2 · Forward+ · a three-pixel stem: eight reads (left), ring of sixteen (right), thickness 1 to 8",
    readouts=[{"at": F("B37", "This stem is three pixels wide"), "text": "eight reads", "x": 0.26, "y": ONE_SPRITE_ROW}, {"at": F("B37", "This stem is three pixels wide"), "text": "ring of sixteen", "x": 0.74, "y": ONE_SPRITE_ROW},
              {"at": F("B37", "floating copies"), "text": "floating copies", "x": 0.26, "y": 0.06}],
    rings=[{"at": F("B37", "floating copies"), "box": box(330, 156, 150, 120)}],
    intent="Two real sprites, each a disc with a three-pixel-wide stem ending in a small ball, the outline growing from one to eight. On the left (eight reads) the line around the stem comes apart into floating copies of the ball and detached stripes; on the right (ring of sixteen) the line wraps the stem as one piece. Labels under each, a ring on the floating copies.",
    motion="The line grows; on the left it breaks into floating copies around the stem, on the right it holds together.",
    show=[{"at": F("B37", "This stem is three pixels wide"), "event": "labels"}, {"at": F("B37", "floating copies"), "event": "ring on the floating copies"}, {"at": F("B37", "The ring of sixteen holds it together"), "event": "right side whole"}],
    runner="manim: ghost copies of a thin shape", why="The real shapes, from the real shaders, coming apart: this is the ghost-copy model from earlier made visible.",
    verified="at thickness 8, on image row 17 (the stem just under the ball) eight reads leave five empty pixels each side of the stem and the line floats as copies, the ring of sixteen leaves none (analyze_scenes C37); over the whole sprite eight reads draw 96.0 percent of the true outline and sixteen 100.0 percent (analyze_mascot D1); on row 21 the diagonal reads reach the ball and the disc and fill the gap (D2)", evidence="verify_d_mascot.gd (D1, D2)")
lab("B38", "soft edges: mix blends alpha too", "C38-soft-edges", layout="side", shader="11-soft-edges.gdshader", label="Godot 4.7.2 · Forward+ · a 12x look at the rim of a soft-edged sprite: plain mix (left), composite (right)",
    cues=[{"at": F("B38", "Mix blends alpha too"), "lines": [ln("11-soft-edges.gdshader", "float around")]}, {"at": F("B38", "Compute the alpha yourself"), "lines": [ln("11-soft-edges.gdshader", "float edge"), ln("11-soft-edges.gdshader", "float alpha"), ln("11-soft-edges.gdshader", "COLOR = vec4")]}],
    readouts=[{"at": F("B38", "a quarter transparent at worst"), "text": "alpha 0.75", "x": 0.26, "y": 0.85}, {"at": F("B38", "the seam closes"), "text": "alpha 1.0", "x": 0.74, "y": 0.85}],
    intent="Code card at left: the 14-line composite shader (edge, alpha and the vec4 line marked). At right two real 12x close-ups of the rim of a soft-edged sprite, both on the plain mix: pale, see-through pixels sit between the teal and the line. As the voice says 'compute the alpha yourself' the right one switches to the composite and its rim pixels turn solid; the left stays pale. Readouts 'alpha 0.75' and 'alpha 1.0'.",
    motion="Focus lands on the three composite lines and the pale rim on the right turns solid while the left stays pale.",
    show=[{"at": F("B38", "Mix blends alpha too"), "event": "readout 'alpha 0.75' on the left"}, {"at": F("B38", "Compute the alpha yourself"), "event": "the composite lines"}, {"at": F("B38", "the seam closes"), "event": "readout 'alpha 1.0' on the right"}],
    runner="manim: a row of rim cells with alpha values", why="The same rim before and after the one change, with the untouched twin beside it: the cure acting on the real pixels.",
    verified="224 rim pixels all see-through with plain mix (output alpha 0.75 to 0.95, mean 0.82), 0 with the composite (alpha 1.00); on hard-edged art the two give the same picture (analyze_soft B1; analyze_lab A13); in the capture 7,056 canvas px of the right panel change at the switch and none of the left (analyze_scenes C38)", evidence="verify_b_soft.gd (B1); scene C38")
lab("B39", "linear filtering blurs the alpha you read", "C39-filter", layout="video",
    label="Godot 4.7.2 · Forward+ · a 12x look at the rim: nearest (left), linear (right) · counts: whole sprite at 2x",
    readouts=[{"at": F("B39", "nearest made none"), "text": "nearest", "x": 0.26, "y": 0.92}, {"at": F("B39", "Linear filtering"), "text": "linear", "x": 0.74, "y": 0.92},
              {"at": F("B39", "linear made two thousand"), "text": "2,008 half-transparent", "x": 0.74, "y": 0.86}, {"at": F("B39", "nearest made none"), "text": "0 half-transparent", "x": 0.26, "y": 0.86}],
    caption="docs: nearest takes the one closest pixel; linear mixes the four closest",
    intent="Two real 12x close-ups of the same outlined rim, both on the default linear filter and blurred. As the voice says 'nearest made none' the left one switches to the nearest filter: crisp one-pixel steps in one flat blue; the right one stays a blurred, soft-edged line of many shades. Labels 'nearest' and 'linear', the counts '0 half-transparent' and '2,008 half-transparent' (counted over the whole sprite at 2x, as the frame label says), a caption crediting the docs.",
    motion="Both close-ups start blurred; the left one switches to nearest and turns crisp while the right one stays blurred.",
    show=[{"at": F("B39", "Linear filtering"), "event": "both blurred; label 'linear' on the right"}, {"at": F("B39", "linear made two thousand"), "event": "'2,008 half-transparent' on the linear side"}, {"at": F("B39", "nearest made none"), "event": "the left side switches to nearest and turns crisp; label 'nearest', '0 half-transparent'"}],
    runner="manim: four texels blended into one read", why="The same rim before and after one setting, with the untouched twin beside it: the blur is visibly the filter's doing.",
    verified="half-transparent pixels 0 with nearest, 2,008 with linear (86 distinct alpha values at 2.25x); a node with no filter set behaves exactly like linear (analyze_filter E1); in the capture the left panel's blurred pixels go from 10,342 to 0 at the switch, the right stays at 10,342 (analyze_scenes C39)", evidence="verify_e_filter.gd (E1)")
lab("B40", "a shader that assigns COLOR from the texture ignores the node's modulate", "C40-modulate", layout="side", shader="14-modulate.gdshader",
    label="Godot 4.7.2 · Forward+ · modulate faded to alpha 0.5: color from the texture (left), vertex color kept (right)",
    cues=[{"at": F("B40", "Pass the vertex color on through a varying"), "lines": [ln("14-modulate.gdshader", "varying vec4 tint"), ln("14-modulate.gdshader", "void vertex()")], "label": "varying: a value set at each corner, blended across a shape"},
          {"at": F("B40", "multiply it in"), "lines": [ln("14-modulate.gdshader", "COLOR = mix")]}],
    readouts=[{"at": F("B40", "nothing fades"), "text": "fade ignored", "x": 0.27, "y": ONE_SPRITE_ROW}, {"at": F("B40", "multiply it in"), "text": "fade works", "x": 0.73, "y": ONE_SPRITE_ROW}],
    caption="modulate: the node's own tint and fade; it reaches the shader as vertex COLOR",
    intent="Code card at left: the 13-line modulate-safe shader (the varying tint, the one-line vertex function, and the final multiply by tint marked). At right two real sprites whose node modulate fades to half: the left one (its shader assigns color from the texture) stays fully solid with its line, the right one (vertex color kept) fades, line included. Readouts 'fade ignored' and 'fade works'.",
    motion="Both sprites are asked to fade; the left one does not, the right one does.",
    show=[{"at": F("B40", "Fade a sprite"), "event": "the fade starts on both"}, {"at": F("B40", "nothing fades"), "event": "left stays solid; readout 'fade ignored'"}, {"at": F("B40", "multiply it in"), "event": "varying and multiply lines; right fades; readout 'fade works'"}],
    runner="manim: a tint arrow skipping the shader", why="Two real sprites given the same fade, one ignoring it, with the three lines that make the difference.",
    verified="with modulate alpha 0.5: no shader draws alpha 0.50; a shader assigning COLOR from the texture draws 1.00 (sprite) and 1.00 (line); the varying version draws 0.50 and 0.50 (verify_m M1)", evidence="verify_m_modulate.gd (M1)")
rem("B41", "four checks for any outline shader", "LectureEvidenceTable",
    {"title": "Four checks", "headers": ["Check", "Why"],
     "rows": [["Padding at least the thickness", "the line needs pixels to live on"], ["Step in image pixels", "texture pixel size times thickness"],
              ["Reads per pixel", "the cost follows the reads"], ["Filter and modulate", "linear blurs alpha; texture-only COLOR drops modulate"]],
     "note": "measured in Godot 4.7.2 · Forward+ · Apple M4 Pro", "cues": [F("B41", "Is there padding"), F("B41", "Does the step count image pixels"), F("B41", "How many reads per pixel"), F("B41", "Is the filter nearest")], "durationSeconds": "__AUDIO__"},
    "A four-row table, one row ringed as each check is asked.", "The ring moves down the rows with the voice.",
    [{"at": F("B41", "Is there padding"), "event": "padding row"}, {"at": F("B41", "Does the step count image pixels"), "event": "step row"}, {"at": F("B41", "How many reads per pixel"), "event": "reads row"}, {"at": F("B41", "Is the filter nearest"), "event": "filter and modulate row"}],
    "manim", "A summary of four parallel checks is exactly what the table component is for.", "the earlier beats; every row traces to a FACTCHECK row")

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
for e in E:
    pr = e["entry"].get("props", {})
    assert len(pr.get("caption", "")) <= 80, (e["bid"], "caption over 80 characters", len(pr.get("caption", "")))
    for c in pr.get("cues", []) if isinstance(pr.get("cues"), list) else []:
        if isinstance(c, dict) and "label" in c:
            assert len(c["label"]) <= 60, (e["bid"], "cue label over 60 characters", c["label"])
    for r in pr.get("readouts", []):
        assert len(r["text"].split()) <= 3, (e["bid"], "readout over three words", r["text"])
assert [e["bid"] for e in E] == [b for b, _, _ in Y.N.BODY], "lane order must match the narration"
(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(len(Y.N.ACTS)):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

hist = {}
for e in E:
    hist[e["entry"]["lane"]] = hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
n_scenes = len(list(SCENES.glob("*.json")))
sl = ["# Shot list: Outlines\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(hist.items(), key=lambda kv: -kv[1])) +
      f". Every Godot picture is a render of a tested file in `lab-shaders/`, played from a spec in `evidence/planning-checks/scenes/` ({n_scenes} captures, none needs the editor). "
      "The build must create `ShaderLab` and `shader_kit.py` first (below) and extend the capture harness with the scene player.\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`). 2. **`shader_kit.py`** Manim helpers (same file): ramp strip, pixel grid, uv square, code card, ghost copies as plain circles. "
      f"3. **Capture harness with the scene player**: `evidence/planning-checks/scene_player.gd`, `ol_lib.gd`, `padding_snippet.gd`, `select_snippet.gd` and the {n_scenes} JSON specs in `scenes/` (contract in `CAPTURE-PLAN.md`). "
      "4. **Docs screenshot** for B12 via Playwright. No editor frames are needed.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", hist)
