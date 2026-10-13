#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text (excerpts are cut from the files by line numbers, and the cue line
numbers are found by searching for text, so they cannot drift), and the shot list must say exactly what the lanes say.
Re-run after any edit:   python3 _gen_lanes.py && python3 make_sheet.py
"""
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
spec = importlib.util.spec_from_file_location("narration", HERE / "narration.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
WORDS = {bid: len(t.split()) for bid, _, t in N.BODY}
E = []          # entries in beat order


def secs(bid):
    """Capture length to record: the estimated narration time plus 15 %, rounded up to a whole second."""
    return math.ceil(WORDS[bid] * 0.34 * 1.15)


def file_lines(fn):
    return (SH / fn).read_text().rstrip("\n").split("\n")


def code_of(fn, a=None, b=None):
    ls = file_lines(fn)
    return "\n".join(ls[(a or 1) - 1:(b or len(ls))])


def find_line(code, needle):
    for i, ln in enumerate(code.split("\n"), 1):
        if needle in ln:
            return i
    raise ValueError(f"{needle!r} not in code")


def start_of_vertex(fn):
    for i, ln in enumerate(file_lines(fn), 1):
        if ln.startswith("void vertex()"):
            return i
    raise ValueError("no vertex()")


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects + the film-local helpers listed in SHOTLIST.md)"):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, code, code_file, video, label, cues, intent, motion, show, runner, why, spec_text, evidence, layout="side",
        readouts=None, rings=None, title=None, caption=""):
    props = {"layout": layout, "code": code, "codeFile": code_file, "cues": cues, "video": video, "videoLabel": label,
             "readouts": readouts or [], "rings": rings or [], "caption": caption, "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    add(bid, act, about, {"lane": "capture", "pattern": "ShaderLab", "props": props, "capture_spec": spec_text, "visual_intent": intent,
                          "motion_claim": motion, "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


def rem(bid, act, about, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, act, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


CARD = ("card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), "
        "node scale k/8 with k = {k} in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U")
BASE = "4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input"
ORIGIN = "a small grey cross at the node's origin drawn by the scene"

# ═══════════════════════════ ACT I · A Table That Moves Points ═══════════════════════════
lab("B01", 0, "a flat card turns over: the hook", code_of("08-flip.gdshader"), "lab-shaders/08-flip.gdshader", "godot-shaders/matrices-hook-flip.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweep of flip", [],
    "Act title 'A Table That Moves Points' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a cream card with a teal arrow pointing right and a small teal square in its top left corner sits still, then turns over like a card: it narrows to an edge, comes back mirrored (the arrow now points left, the square sits top right), then turns back to the front. Label under the window: 'scripted sweep'.",
    "The flat card turns over, narrows to nothing, comes back mirrored, and turns to the front again.",
    [{"at": 0.0, "event": "card at rest, window labelled"}, {"at": 0.14, "event": "card starts to turn"}, {"at": 0.38, "event": "back side: the arrow points left"},
     {"at": 0.64, "event": "card turns back"}, {"at": 0.82, "event": "front again"}],
    "manim drawing of a card turning", "A real render is the honest picture of 'a flat picture that turns over'; a drawing would only claim it.",
    f"C01: 08-flip.gdshader on a Sprite2D; {CARD.format(k='2.0')}; {BASE}; {secs('B01')} s. flip keyframes (fraction of the beat, ease in-out on each move): 0.0 at 0.00 to 0.10, 0.5 at 0.38, 0.5 until 0.62, 1.0 at 0.80, 1.0 to the end. "
    "At the 50 % mark: the mirrored back, fully visible (arrow points left). At 85 %: the front. Verified: widths 128 x |cos(TAU x flip)|, mirrored at 0.5 (geometry-summary.txt).",
    "Lab renders f1, f2 (width = 128 x abs(cos), mirrored at 0.5); planning still png/still-flip-0.5-mirrored.png", layout="video", title="A Table That Moves Points")

manim("B02", 0, "table times point, row by row: (5, 6) becomes (23, 34)", "RowsTimesPoint",
      "Left to right on the cream stage: a bracketed two-by-two table (1 3 over 2 4) labelled 'table', a bracketed column (5 over 6) labelled 'point', an equals sign and an empty bracketed result column. A terracotta ring outlines the table's top row (labelled 'row'); the small products '1 x 5' and '3 x 6' appear beneath and add up to '23', which lands in the first result slot. The ring drops to the bottom row: '2 x 5' and '4 x 6' add up to '34'. Last, a drawn arrow runs from the point column to the result column.",
      "A ring walks down the table one row at a time, and each row collapses into one number of the answer.",
      [{"at": 0.08, "event": "table, point, equals sign, empty result"}, {"at": 0.22, "event": "ring on the top row; products 1 x 5 and 3 x 6"}, {"at": 0.40, "event": "23 lands in the first slot"},
       {"at": 0.60, "event": "ring drops to the bottom row; products 2 x 5 and 4 x 6"}, {"at": 0.78, "event": "34 lands in the second slot"}, {"at": 0.90, "event": "arrow from the point to the result"}],
      "Remotion card with the arithmetic typed out", "A ring that walks down the rows shows 'row against point' as an action; typed arithmetic would only list it.",
      "Arithmetic 1x5+3x6 = 23 and 2x5+4x6 = 34; Lab unit test u1 row 0 (the shader agrees)")

code01 = code_of("01-table-check.gdshader")
lab("B03", 0, "the shader checks the hand calculation", code01, "lab-shaders/01-table-check.gdshader", "godot-shaders/matrices-table-check.mp4",
    "Godot 4.7.2 · Forward+ · shader switched on at 60 % of the beat",
    [{"at": 0.10, "lines": [find_line(code01, "mat2 table")], "label": "mat2: a table of four numbers"}, {"at": 0.28, "lines": [find_line(code01, "vec2 moved")]},
     {"at": 0.62, "lines": [find_line(code01, "if (moved"), find_line(code01, "COLOR = vec4(0.37")]}],
    "Code card at left with the real ten-line shader; at right a framed Godot window that is the plain stage colour at first, then turns teal when the check line is highlighted. A small readout 'teal: agrees' lands under the window.",
    "Focus steps from the table line to the multiplication to the check, and then the window turns teal.",
    [{"at": 0.10, "event": "mat2 table line"}, {"at": 0.28, "event": "multiplication line"}, {"at": 0.62, "event": "check lines; window turns teal; readout lands"}],
    "LectureCodeTrace alone", "The claim is 'the shader agrees with my hand calculation'; code beside a result that changes colour on the check line shows it, a bare code card does not.",
    f"C02: a ColorRect filling the result window; no material for the first 60 % of the beat, then 01-table-check.gdshader assigned (harness option --material-at); {secs('B03')} s; {BASE}. "
    "At the 50 % mark: the plain stage colour (shader not yet on) with line 5 in focus. At 85 %: teal. Verified: probe (0.3686, 0.6392, 0.5686); the disagree colour is (0.85, 0.2, 0.2).",
    "Lab probe s1 (teal); unit test u1 rows 0, 10 (answer equals (23, 34); controls red)", readouts=[{"at": 0.64, "text": "teal: agrees", "x": 0.5, "y": 0.88}])

manim("B04", 0, "each vec2 is a column, so the top row is 1, 3", "VecTwoIsAColumn",
      "On the left a code card (Menlo, at least 32) holds the real line mat2(vec2(1.0, 2.0), vec2(3.0, 4.0)); the two vec2 groups are outlined, one solid and one dashed. On the right an empty bracketed two-by-two table. The first vec2 (1, 2) lifts out of the code and stands upright as the table's left column, labelled 'column'; the second (3, 4) becomes the right column. Then the top row is outlined and labelled 'row: 1, 3'.",
      "Each vec2 lifts out of the code and stands upright as a column of the table.",
      [{"at": 0.10, "event": "code line with its two vec2 groups outlined"}, {"at": 0.28, "event": "(1, 2) stands up as the left column; label 'column'"}, {"at": 0.40, "event": "(3, 4) stands up as the right column"},
       {"at": 0.68, "event": "top row outlined: 'row: 1, 3'"}],
      "LectureCodeTrace alone", "The surprise is that the order in the code and the order on paper differ; only a drawing that moves the numbers from one to the other shows it.",
      "Lab unit test u1 rows 1, 2 (m[0] = (1, 2); m[1][0] = 3)")

rem("B05", 0, "the documentation says: vectors, interpreted as columns", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html", "image": "godot-shaders/matrices-docs-constructing.png",
     "caption": "Godot 4.7 documentation · Shading language · captured at build time", "frame": "browser",
     "moves": [{"at": 0, "x": 0.5, "y": 0.3, "scale": 1}, {"at": 0.2, "x": 0.45, "y": 0.5, "scale": 1.6, "ring": [0.2, 0.46, 0.6, 0.07]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 shading-language page in a browser window, scrolled to the 'Constructing' section; the camera pushes in on the sentence that says matrix types are built from vectors 'interpreted as columns' and one terracotta ring marks it.",
    "The camera pushes in on the sentence the voice is quoting.",
    [{"at": 0, "event": "page, scrolled to Constructing"}, {"at": 0.2, "event": "push-in; ring on the 'interpreted as columns' sentence"}],
    "manim: a quote card", "The claim is a documentation claim; the documentation itself is the evidence (SHOW-THE-THING).",
    "D1: Playwright capture of the live docs page (1600x900 at 2.4x), scrolled to the Constructing section; the build session sets x, y and the ring from the real screenshot (the lane values are a starting guess). "
    "Read 2026-10-13: 'Construction of matrix types requires vectors of the same dimension as the matrix, interpreted as columns.'")

manim("B06", 0, "two mistakes that both give (17, 39)", "TwoWrongReadings",
      "Three stacked lines on the cream stage. Top (ink): the right reading, table x point = (23, 34). Middle (grey, with a terracotta strike line): the numbers read as ROWS, so the table becomes 1 2 over 3 4 (the 2 and the 3 swap places) and the result is (17, 39); label 'rows'. Bottom (grey, with a strike line): the point written on the LEFT of the table, (5, 6) x table, result (17, 39); the code label 'p * table' beside it. At the end the top line is ringed and a label 'table first' lands.",
      "The 2 and the 3 swap places, and the answer changes to (17, 39); then the point hops to the other side of the table and gives the same wrong answer.",
      [{"at": 0.06, "event": "correct line: (23, 34)"}, {"at": 0.24, "event": "the 2 and 3 swap; result (17, 39); strike"}, {"at": 0.40, "event": "line settled"},
       {"at": 0.62, "event": "point jumps to the left of the table; result (17, 39); strike"}, {"at": 0.86, "event": "top line ringed; label 'table first'"}],
      "LectureEvidenceTable", "A swap of two numbers and a hop of the point are motions; a table of wrong answers would hide how little it takes to get them.",
      "Lab unit test u1 rows 3, 4, 10, 11 (point on the left = (17, 39); table read as rows = (17, 39); controls red)")

manim("B07", 0, "columns are where the arrows land: 5 of the first plus 6 of the second", "WhereArrowsLand",
      "A grid in Godot's screen directions (x to the right, y DOWN; small axis labels). The unit square with an 'across' arrow (solid) and a 'down' arrow (dashed). At the top right the table 1 3 over 2 4 with its first column outlined solid and its second dashed. The grid warps: the across arrow lands at (1, 2), the down arrow at (3, 4), the square becomes a parallelogram with corners (0,0), (1,2), (4,6), (3,4); tip labels '1, 2' and '3, 4'. Then the view zooms out and a staircase of five across-steps then six down-steps walks from the origin to a terracotta dot labelled '23, 34'.",
      "The square warps into a parallelogram on the two columns, then a staircase of five and six steps walks to (23, 34).",
      [{"at": 0.08, "event": "grid, unit square, two arrows, table with outlined columns"}, {"at": 0.22, "event": "grid warps; arrows land on (1, 2) and (3, 4)"}, {"at": 0.40, "event": "tip labels settled"},
       {"at": 0.60, "event": "view zooms out"}, {"at": 0.74, "event": "five across-steps then six down-steps walk out"}, {"at": 0.90, "event": "dot at (23, 34)"}],
      "ShaderLab", "The idea is a transformation of a whole grid; only a warping grid shows 'where the arrows land' at a glance.",
      "Math: 5 x (1, 2) + 6 x (3, 4) = (23, 34); Lab unit test u1 row 8 (column view)")

manim("B08", 0, "the identity table moves nothing", "IdentityMovesNothing",
      "The warped grid of the previous picture on the same screen-direction axes, with the table 1 3 over 2 4. The four entries change to 1 0 over 0 1 and the grid relaxes back into the plain unit square while both arrows spring back onto (1, 0) and (0, 1). A label 'identity: moves nothing'. A small code card then shows mat2(1.0).",
      "The warped grid relaxes back into a square as the numbers settle to one, zero, zero, one.",
      [{"at": 0.08, "event": "warped grid with the table 1 3 / 2 4"}, {"at": 0.28, "event": "entries morph to 1 0 / 0 1; grid straightens"}, {"at": 0.40, "event": "plain square, arrows on (1, 0) and (0, 1)"},
       {"at": 0.62, "event": "label 'identity: moves nothing'; code card mat2(1.0)"}],
      "ShaderLab with the identity table", "'Moves nothing' is the grid coming to rest; the same table numbers changing live make the point that the numbers ARE the move.",
      "Lab unit test u1 rows 5, 6 (mat2(1.0) times p equals p; mat2(1.0) equals the table 1 0 / 0 1)")

manim("B09", 0, "stretch the arrows and the table scales", "ScaleStretchesArrows",
      "The same screen-direction grid. The table 1 0 over 0 1 becomes 2 0 over 0 2; both arrows stretch to (2, 0) and (0, 2) and the unit square grows into a square twice as wide and tall, centred on the origin's corner. A label 'scale: twice as far' defines the word.",
      "Both arrows stretch to twice their length and the square grows with them.",
      [{"at": 0.10, "event": "identity table, unit square"}, {"at": 0.30, "event": "entries become 2 0 / 0 2; arrows stretch; square doubles"}, {"at": 0.42, "event": "settled"}, {"at": 0.68, "event": "label 'scale: twice as far'"}],
      "LectureEvidenceTable", "Scaling is a stretch of the arrows; seeing the arrows grow as the diagonal numbers change is the claim.",
      "Lab unit test u1 row 7 ((5, 6) becomes (10, 12)); Lab g1 (a 128 px square becomes 256 px at 2.0)")

manim("B10", 0, "a shape is its corners; one table moves them all", "ShapeIsItsCorners",
      "The test rectangle (a wide rectangle, 3 by 2 grid units, centred on the origin of the screen-direction grid) with four terracotta corner dots; the table 2 0 over 0 2 at the side. The four dots fly outward one after another to their doubled positions and the rectangle's edges redraw between them; a faint ghost of the old rectangle stays. A label 'one table, four corners'.",
      "Four dots fly outward one after another and the rectangle's edges follow them.",
      [{"at": 0.10, "event": "rectangle, four corner dots, table"}, {"at": 0.22, "event": "dot 1 flies to its new place"}, {"at": 0.28, "event": "dot 2"}, {"at": 0.34, "event": "dot 3"}, {"at": 0.40, "event": "dot 4; edges redraw"},
       {"at": 0.68, "event": "label 'one table, four corners'"}],
      "isometric workers on a conveyor (show-tell)", "The cast of the whole film is the rectangle with four corner dots; dots flying to their new places is the literal meaning of 'multiply every corner'.")

# ═══════════════════════════ ACT II · Three Moves ═══════════════════════════
code02 = code_of("02-grow.gdshader")
lab("B11", 1, "the scale table in vertex(): the picture grows", code02, "lab-shaders/02-grow.gdshader", "godot-shaders/matrices-grow.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweep of grow",
    [{"at": 0.08, "lines": [find_line(code02, "void vertex")], "label": "vertex(): runs once for each corner"}, {"at": 0.26, "lines": [find_line(code02, "VERTEX = ")]}, {"at": 0.64, "lines": [find_line(code02, "mat2 scale_table"), find_line(code02, "VERTEX = ")]}],
    "Act title 'Three Moves' (serif 40) top-left. Code card at left with the real eight-line shader; at right a framed Godot window with the card, a small grey cross at its origin, a readout 'origin' next to the cross, and the line 'VERTEX: a corner's position, in pixels from the node's origin' as the caption. The card grows when the scale line is highlighted.",
    "Focus lands on vertex(), then on VERTEX, then on the scale table, and the card grows.",
    [{"at": 0.08, "event": "void vertex() line"}, {"at": 0.26, "event": "VERTEX line; caption defines VERTEX"}, {"at": 0.34, "event": "readout 'origin'"}, {"at": 0.64, "event": "scale table line; the card grows"}, {"at": 0.74, "event": "readout 'grow 1.5'"}],
    "manim", "A real card that really grows under a real vertex() is the first proof that the table from the previous act works on a shape.",
    f"C03: 02-grow.gdshader on the card; {CARD.format(k='2.0')}; {ORIGIN}; {BASE}; {secs('B11')} s. grow keyframes: 1.0 at 0.00 to 0.58, 1.5 at 0.72 (ease in-out), 1.5 to the end. "
    "At the 50 % mark: the card at its original size. At 85 %: the card grown by half. Verified at node scale 1.0: 128 px becomes 192 px at grow 1.5 (geometry-summary.txt).",
    "Lab g1 (64, 128, 192, 256 px at 0.5, 1.0, 1.5, 2.0); planning still png/still-grow-1.5.png",
    readouts=[{"at": 0.34, "text": "origin", "x": 0.52, "y": 0.58}, {"at": 0.76, "text": "grow 1.5", "x": 0.5, "y": 0.92}],
    title="Three Moves", caption="VERTEX: a corner's position, in pixels from the node's origin")

manim("B12", 1, "the turn table: cosine and sine in the columns", "TurnIsATable",
      "The screen-direction grid with a grey circle of radius one. The across arrow (solid) and the down arrow (dashed) swing together clockwise from the start position to 45 degrees; the across tip is labelled 'cos, sin' with its live numbers 0.71, 0.71 and the down tip 'minus sin, cos' (-0.71, 0.71). At the right the table cos -sin over sin cos with its four live entries (0.71 -0.71 over 0.71 0.71), first column outlined solid and second dashed. A small label under the circle: 'across and down on a circle of radius one'.",
      "The two arrows swing together clockwise round the circle while the table's four entries change with them.",
      [{"at": 0.08, "event": "circle, two arrows at rest, table at the angle 0"}, {"at": 0.20, "event": "arrows swing clockwise to 45 degrees; entries update"}, {"at": 0.40, "event": "tip labels settled"},
       {"at": 0.62, "event": "arrows swing on to 90 degrees; the table reads 0 -1 / 1 0"}, {"at": 0.84, "event": "label 'across and down on a circle'"}],
      "plot of cosine and sine", "Rotation is two arrows turning together, and the table is where they land; one picture shows both, with the numbers updating live.",
      "Lab t1, t2 (corners of a 128 px square turned clockwise match x cos - y sin, x sin + y cos); verify1 R2 (Transform2D columns)")

code03 = code_of("03-turn.gdshader")
lab("B13", 1, "the turn table in vertex(): angles in radians, clockwise on screen", code03, "lab-shaders/03-turn.gdshader", "godot-shaders/matrices-turn.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweep of angle",
    [{"at": 0.08, "lines": [find_line(code03, "uniform float angle")], "label": "radians: Godot's angle unit"}, {"at": 0.62, "lines": [find_line(code03, "VERTEX = mat2")]}],
    "Code card at left with the real nine-line shader; at right a framed Godot window with the card and its origin cross. The caption defines TAU; the card turns clockwise by an eighth of tau (45 degrees) while the readouts 'TAU: full turn', 'angle 0.79' and 'clockwise' land.",
    "The card turns clockwise as the angle sweeps up to an eighth of tau.",
    [{"at": 0.08, "event": "angle uniform line"}, {"at": 0.30, "event": "readout 'TAU: full turn'"}, {"at": 0.62, "event": "VERTEX = mat2(across, down) * VERTEX line; the card turns"}, {"at": 0.74, "event": "readouts 'angle 0.79' and 'clockwise'"}],
    "manim", "A real turn in the engine, the same direction Godot's own rotation uses; the readouts name the three things the voice says.",
    f"C04: 03-turn.gdshader on the card; {CARD.format(k='2.0')}; {ORIGIN}; {BASE}; {secs('B13')} s. angle keyframes: 0.0 at 0.00 to 0.58, 0.7854 at 0.72 (ease in-out), 0.7854 to the end. "
    "At the 50 % mark: the card upright. At 85 %: the card turned 45 degrees clockwise (arrow pointing down and to the right). Verified: bbox of a turned 128 px square matches the corner maths; pixel-identical to Node2D.rotation (verify1 R1).",
    "Lab t1, t2; verify1 R1 (0 differing pixels out of 57,600); docs: rotation is represented clockwise; planning still png/still-turn-0.7854.png",
    readouts=[{"at": 0.30, "text": "TAU: full turn", "x": 0.5, "y": 0.1}, {"at": 0.76, "text": "angle 0.79", "x": 0.5, "y": 0.92}, {"at": 0.80, "text": "clockwise", "x": 0.78, "y": 0.5}],
    caption="TAU: one full turn, about 6.283 radians")

manim("B14", 1, "a two-by-two table can never move the origin", "OriginNeverMoves",
      "The screen-direction grid with the origin pinned by a terracotta dot and a small pin drawn from lines. Three different two-by-two tables act in turn (a scale, a turn, a squash): the grid stretches, spins and squashes, but the origin dot never leaves its spot. At the end the whole grid tries to slide right (a dashed arrow) and snaps back; label '0, 0 stays 0, 0'.",
      "The grid stretches, spins and squashes around a dot that never moves; a slide is attempted and snaps back.",
      [{"at": 0.10, "event": "grid, pinned origin dot"}, {"at": 0.20, "event": "scale warp; dot stays"}, {"at": 0.30, "event": "turn warp; dot stays"}, {"at": 0.40, "event": "squash warp; dot stays"},
       {"at": 0.62, "event": "slide attempt: dashed arrow; grid snaps back"}, {"at": 0.84, "event": "label '0, 0 stays 0, 0'"}],
      "LectureEvidenceTable", "'Cannot slide' is a limit; a pinned dot that survives three different warps shows the limit better than the sentence.",
      "Math: a 2 x 2 table times (0, 0) is (0, 0); Lab unit test u3 row 10")

manim("B15", 1, "the third number: a one, and the slide in the last column", "ThirdNumberIsOne",
      "A bracketed three-by-three table (1 0 100 / 0 1 0 / 0 0 1) with its last column outlined and labelled 'slide'; beside it a bracketed column (30 / 20 / 1) with its last slot ringed, labelled 'point, plus a one'; an equals sign and a result column. The ring walks down: the top row gives 1 x 30 + 0 x 20 + 100 x 1 = 130 (the 100 pairs with the one); the middle row gives 20; the bottom row gives 0 + 0 + 1 = 1, so the result column reads (130 / 20 / 1).",
      "The ring walks down the rows: the slide in the last column is multiplied by the one, and the one survives in the last slot.",
      [{"at": 0.08, "event": "table, point with its one, result slots"}, {"at": 0.22, "event": "ring on the top row; 100 pairs with the one"}, {"at": 0.40, "event": "130 lands; settled"},
       {"at": 0.62, "event": "middle row: 20"}, {"at": 0.78, "event": "bottom row: the one survives"}],
      "LectureEvidenceTable", "The trick is arithmetic: showing the 100 meet the one in the top row, and the bottom row keep the one, is the explanation.",
      "Lab unit test u3 row 9 (the table times (30, 20, 1) = (130, 20, 1)); Lab sl1 (the slide moves the centre by exactly the offset)")

code04 = code_of("04-slide.gdshader")
lab("B16", 1, "the slide table in vertex(): a one on the end, keep the first two", code04, "lab-shaders/04-slide.gdshader", "godot-shaders/matrices-slide.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweep of slide",
    [{"at": 0.10, "lines": [find_line(code04, "VERTEX = (mat3")]}, {"at": 0.60, "lines": [find_line(code04, "vec3 offset")], "label": "offset: a distance added to slide something"}],
    "Code card at left with the real ten-line shader; at right a framed Godot window with the card and its origin cross. When the offset line is highlighted the card slides one hundred pixels to the right; a readout 'slide 100 px' lands.",
    "The card slides to the right when the offset line is highlighted.",
    [{"at": 0.10, "event": "VERTEX = (mat3(...) * vec3(VERTEX, 1.0)).xy line"}, {"at": 0.60, "event": "offset line; the card slides right"}, {"at": 0.78, "event": "readout 'slide 100 px'"}],
    "manim", "A real slide in the engine with the third number visible in the code.",
    f"C05: 04-slide.gdshader on the card; {CARD.format(k='2.0')}; {ORIGIN}; {BASE}; {secs('B16')} s. slide keyframes (x, y): (0, 0) from 0.00 to 0.58, (100, 0) at 0.74 (ease in-out, pass (100 x U, 0)), then hold. "
    "At the 50 % mark: the card at the origin. At 85 %: the card one hundred card-pixels to the right. Verified: centre moves by exactly (100, 0) (geometry-summary.txt).",
    "Lab sl1 (centres (100, 0), (0, 100), (100, -40)); unit test u3 row 9", readouts=[{"at": 0.78, "text": "slide 100 px", "x": 0.5, "y": 0.92}])

rem("B17", 1, "three moves, three tables", "LectureEvidenceTable",
    {"title": "Three moves, three tables", "headers": ["Move", "Where its numbers go"],
     "rows": [["scale", "on the diagonal"], ["turn", "cosine and sine, first two columns"], ["slide", "the offset (a distance), last column"], ["all three", "keep straight edges straight"]],
     "note": "Godot 4.7.2 · each table checked against the pixels of a 128 px square", "cues": [0.08, 0.22, 0.36, 0.62], "durationSeconds": "__AUDIO__"},
    "A four-row table: scale, turn and slide, each with where its numbers go, and a last row 'all three: keep straight edges straight'; one row is ringed as each is named.",
    "The ring steps down the rows with the voice.",
    [{"at": 0.08, "event": "scale row"}, {"at": 0.22, "event": "turn row"}, {"at": 0.36, "event": "slide row"}, {"at": 0.62, "event": "all three row"}],
    "manim", "A summary of three parallel facts, with a fourth that holds for all of them, is exactly what the table component is for.",
    "Lab g1, t1, sl1 (the three tables measured); verify2 V1 (a sprite is drawn from four corners: a non-linear move does not bend its edge)")

# ═══════════════════════════ ACT III · Moves Together ═══════════════════════════
manim("B18", 2, "many moves, one saved table", "ManyMovesOneTable",
      "Act title 'Moves Together' (serif 40) top-left. Three small bracketed grids labelled 'scale', 'turn' and 'slide' drift together from the left and merge, with a drawn multiplication sign between them, into one grid labelled 'one table'. Under the one table the test rectangle's four corner dots each get one arrow from the one table; under the three small grids a ghost of the same corners shows three arrows each, crossed out.",
      "Three small tables slide together and merge into one; then each corner needs one arrow instead of three.",
      [{"at": 0.10, "event": "three small tables"}, {"at": 0.26, "event": "they drift together and merge"}, {"at": 0.40, "event": "one table, labelled"}, {"at": 0.62, "event": "four corners with one arrow each; the three-arrow ghost crossed out"}],
      "DesignPipelineClaim, show-tell isometric", "'Saved move' is three tables becoming one; the merge is the motion, and the crossed-out three-arrow ghost is the saving.",
      "Math and Lab unit test u3 rows 2 (one product equals the two tables one after the other)")

manim("B19", 2, "same size first: a two-by-two inside a three-by-three", "TwoByTwoInAThreeByThree",
      "At the top a small grey strip of the REAL compiler message from the Lab for the line mat3(1.0) * mat2(1.0): SHADER ERROR: Invalid arguments to operator '*': 'mat3, mat2'. Below it, on the left, the quarter-turn table 0 -1 over 1 0 (two by two) and at the right an empty three-by-three frame. The two-by-two slides into its top left corner; zeros fill the rest of the grid in grey and a terracotta ring settles on the bottom right entry, which becomes 1: the table reads 0 -1 0 / 1 0 0 / 0 0 1. A small code card then shows mat3(turn).",
      "The two-by-two table slides into the corner of a three-by-three, grey zeros fill in, and a one lands bottom right.",
      [{"at": 0.08, "event": "the real compiler message for mixed sizes"}, {"at": 0.20, "event": "2 x 2 quarter-turn table and an empty 3 x 3 frame"}, {"at": 0.32, "event": "the 2 x 2 slides into the top left corner"}, {"at": 0.40, "event": "zeros and the ringed 1 settle"}, {"at": 0.66, "event": "code card mat3(turn)"}],
      "LectureCodeTrace", "The embedding is a spatial fact (a block in a corner); only a drawing shows which entries are copied and which are filled in, and the real error shows why it is needed.",
      "Lab e1 (mat3 times mat2 does not compile; message quoted), e2 (mat3 times vec2 likewise); unit tests u1 row 9 and u3 row 14 (mat3 of a mat2 pads with zeros and a one); docs: the rule for building a matrix from another size")

manim("B20", 2, "multiplying two tables: row times column", "TablesMultiply",
      "Three bracketed three-by-three tables in a line: slide (1 0 100 / 0 1 0 / 0 0 1), a multiplication sign, quarter turn (0 -1 0 / 1 0 0 / 0 0 1), an equals sign and an empty result table. A terracotta ring outlines the slide table's top row and the turn table's last column; the arithmetic 1 x 0 + 0 x 0 + 100 x 1 = 100 appears and 100 lands in the result's top right entry. The rest of the result fills in: 0 -1 100 / 1 0 0 / 0 0 1.",
      "A row and a column are ringed, their products add to 100, and the whole result table fills in.",
      [{"at": 0.08, "event": "slide table x turn table = empty table"}, {"at": 0.22, "event": "row and column ringed; the arithmetic"}, {"at": 0.38, "event": "100 lands top right"}, {"at": 0.64, "event": "the rest of the result fills in"}],
      "LectureEvidenceTable", "'The rule you know' is the same row-times-column ring from the first act; showing it ring one entry of a bigger table is the continuity.",
      "Lab unit test u3 row 0 (the product's last column is (100, 0, 1)); math")

manim("B21", 2, "the table nearest the point acts first", "NearestTableFirst",
      "A line: the code-style expression slide x turn x point with the first two as small bracketed boxes and the point as a terracotta dot at the far right. A token (the dot's copy) travels right to left: it passes through the turn box first, where a small card icon spins in place, then through the slide box, where it shifts right; drawn arrow shapes point left between the stages. Labels 'turn first', 'slide second'.",
      "A token starting at the point passes through the turn first, then the slide, travelling right to left.",
      [{"at": 0.10, "event": "expression: slide, turn, point"}, {"at": 0.24, "event": "token enters the turn box; card icon spins"}, {"at": 0.40, "event": "token rests between the boxes; label 'turn first'"},
       {"at": 0.60, "event": "token passes the slide box; card icon shifts right"}, {"at": 0.80, "event": "label 'slide second'"}],
      "LectureCodeTrace", "Order of application is a journey right to left; a token that visibly meets the nearest table first is the claim.",
      "Lab o1, o2 (turn first then slide ends at (100, 0)); docs: 'When multiplying matrices, order matters!'")

order_a = code_of("05-turn-then-slide.gdshader", 19, 19).strip()
order_b = code_of("06-slide-then-turn.gdshader", 19, 19).strip()
lab("B22", 2, "same two tables in two orders end in two places", order_a + "\n" + order_b,
    "lab-shaders/05-turn-then-slide.gdshader (line 19) and lab-shaders/06-slide-then-turn.gdshader (line 19)", "godot-shaders/matrices-order-pair.mp4",
    "Godot 4.7.2 · Forward+ · two scenes side by side · scripted sweeps",
    [{"at": 0.12, "lines": [1], "label": "left card"}, {"at": 0.60, "lines": [2], "label": "right card"}],
    "Result window above (two equal panels, each with its origin cross and its own card) and the two product lines below. Left panel labelled 'turn, then slide': the card spins a quarter in place, then slides right and ends at one hundred card-pixels across. Right panel labelled 'slide, then turn': the card slides right first, then swings round the origin along an arc and ends one hundred card-pixels below the cross.",
    "Both cards start at the origin; the left one spins and slides right, the right one slides right and then swings down along an arc.",
    [{"at": 0.06, "event": "label 'turn, then slide'; left card spins then slides"}, {"at": 0.12, "event": "left product line in focus"}, {"at": 0.56, "event": "label 'slide, then turn'"}, {"at": 0.60, "event": "right product line in focus; right card slides then swings"}, {"at": 0.84, "event": "both final places visible"}],
    "manim", "Two real renders of two real files that differ in one line, ending in two different places, are the whole claim; a drawing would only say it.",
    f"C06: custom scene with two panels (each 640 x 720 logical, origin cross at its centre) inside one 1280 x 720 canvas; left panel 05-turn-then-slide.gdshader, right panel 06-slide-then-turn.gdshader; {CARD.format(k='1.5')}; {BASE}; {secs('B22')} s. "
    "Left keyframes: angle 0 to 1.5708 over 0.10-0.24, then slide (0, 0) to (100, 0) over 0.24-0.38. Right keyframes: slide (0, 0) to (100, 0) over 0.58-0.70, then angle 0 to 1.5708 over 0.70-0.82 (so its card swings round the origin). "
    "All moves eased in-out; everything holds after. At the 50 % mark: left card at (100, 0) with its arrow pointing down, right card still at the origin. At 85 %: right card at (0, 100) with its arrow pointing down. "
    "Verified (end states): centres (100, 0) and (0, 100) (geometry-summary.txt).",
    "Lab o1, o2; unit test u3 rows 0, 1; planning stills png/still-order-A-turn-then-slide.png and png/still-order-B-slide-then-turn.png",
    layout="stack", readouts=[{"at": 0.06, "text": "turn, then slide", "x": 0.25, "y": 0.06}, {"at": 0.56, "text": "slide, then turn", "x": 0.75, "y": 0.06}])

manim("B23", 2, "why: a turn swings round the origin", "TurnSwingsAroundTheMiddle",
      "The screen-direction grid with a small cross at the origin and the card (a small cream rectangle with a terracotta dot at its centre) at the origin. The card slides one hundred units right (an arrow), then a dashed quarter-circle arc around the origin appears and the card travels along it, turning as it goes, to the point one hundred units below the origin. A faint ghost marks where 'turn then slide' would have left it. Labels 'slide first' and 'then turn'.",
      "The card slides out, then swings along an arc around the origin and ends below it.",
      [{"at": 0.10, "event": "card at the origin"}, {"at": 0.20, "event": "card slides right; label 'slide first'"}, {"at": 0.32, "event": "dashed arc; card swings along it, turning"}, {"at": 0.42, "event": "card below the origin; label 'then turn'"},
       {"at": 0.66, "event": "ghost at the other place; label 'a turn swings round the middle'"}],
      "ShaderLab with the earlier capture", "The reason is geometry: a card on an arc around the origin shows 'a turn swings everything round the middle' directly.",
      "Lab o2 (centre ends at (0, 100)); unit test u3 row 1 (turning carries the slide round)")

code07 = code_of("07-three-moves.gdshader")
a07 = start_of_vertex("07-three-moves.gdshader")
ex07 = code_of("07-three-moves.gdshader", a07, a07 + 3)
lab("B24", 2, "scale, turn, slide in one product; the slide stays exact", ex07, "lab-shaders/07-three-moves.gdshader (the vertex function)", "godot-shaders/matrices-three-moves.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweeps",
    [{"at": 0.10, "lines": [find_line(ex07, "mat3 m =")], "label": "scale nearest the point, slide farthest"}, {"at": 0.62, "lines": [find_line(ex07, "VERTEX = ")]}],
    "Code card at left with the four-line vertex function (scale_by, turn_by and slide_by are the small functions of the same file); at right a framed Godot window with the card and its origin cross. Three scripted sweeps in turn: the card grows by half, turns thirty degrees, then slides right and slightly up; readouts 'scale', 'turn', 'slide' land as each begins.",
    "Three sweeps in turn, each changing the picture, ending in one combined pose.",
    [{"at": 0.10, "event": "product line in focus"}, {"at": 0.12, "event": "readout 'scale'; the card grows"}, {"at": 0.24, "event": "readout 'turn'; the card turns"}, {"at": 0.36, "event": "readout 'slide'; the card slides"}, {"at": 0.62, "event": "apply line in focus"}],
    "manim", "The film's 'saved move' made real: one table, three sweeps, one picture that matches the maths to the pixel.",
    f"C07: 07-three-moves.gdshader on the card; {CARD.format(k='1.5')}; {ORIGIN}; {BASE}; {secs('B24')} s. Keyframes (ease in-out each): grow 1.0 to 1.5 over 0.08-0.20; angle 0 to 0.5236 over 0.20-0.32; slide (0, 0) to (100, -40) over 0.32-0.44; hold. "
    "At the 50 % and 85 % marks: the final pose (card 192 px, turned 30 degrees clockwise, centred 100 right and 40 up of the origin). "
    "Verified: bounding box x -31 to 231, y -171 to 91 (expected -31.1, 231.1, -171.1, 91.1) and centre exactly (100, -40) (geometry-summary.txt).",
    "Lab m1; planning still png/still-three-moves.png; unit test u3 rows 11, 12 (a uniform scale commutes with a turn; a non-uniform one does not)",
    readouts=[{"at": 0.12, "text": "scale", "x": 0.2, "y": 0.92}, {"at": 0.24, "text": "turn", "x": 0.5, "y": 0.92}, {"at": 0.36, "text": "slide", "x": 0.8, "y": 0.92}])

# ═══════════════════════════ ACT IV · Fake 3D ═══════════════════════════
manim("B25", 3, "depth: a third axis, and the card sits at zero", "DepthAxis",
      "Act title 'Fake 3D' (serif 40) top-left. Axes drawn obliquely: x to the right, y down, and a z axis crossing the screen plane (solid toward the lower left, dashed the other way, labelled 'z: depth'). A flat card (a rectangle outline in the x-y plane) with four terracotta corner dots; one corner shows its three numbers '(x, y, 0)'.",
      "The z axis grows through the screen plane, and the corner dots take a third number: zero.",
      [{"at": 0.10, "event": "x and y axes, flat card with four corner dots"}, {"at": 0.28, "event": "z axis grows; label 'z: depth'"}, {"at": 0.40, "event": "settled"}, {"at": 0.64, "event": "a corner shows (x, y, 0)"}],
      "DesignPipelineClaim, show-tell isometric", "A third axis is a spatial idea; an axis that visibly grows out of the plane and a card lying flat at zero depth is the picture.")

manim("B26", 3, "the third number means two things: a trick (1) or depth (z)", "TwoKindsOfThirdNumber",
      "Two bracketed three-slot columns side by side. Left: (x / y / 1) with the 1 ringed and the label 'slide trick'. Right: (x / y / z) with the z ringed and the label 'depth'. Between them a drawn double bar (not equal). Under each a small three-by-three outline. The ring pulses on the left 1, then on the right z.",
      "The same three-slot column appears twice, and the ring on its last slot pulses first as a one and then as a depth.",
      [{"at": 0.10, "event": "left column, label 'slide trick'"}, {"at": 0.28, "event": "right column, label 'depth'"}, {"at": 0.40, "event": "settled"}, {"at": 0.62, "event": "ring on the left one"}, {"at": 0.80, "event": "ring on the right z"}],
      "LectureEvidenceTable", "The danger is that two things look alike; two identical-looking columns whose last slots are ringed in turn is that danger drawn.",
      "Math; Lab unit test u3 row 13 (mixing the two kinds of table moves the pivot)")

manim("B27", 3, "from above the card is a line; the screen sees its shadow", "TopViewOfTheTurn",
      "A top view. A horizontal screen line at the bottom (label 'screen'). Above it a thin card drawn as a horizontal line segment centred on a small ring-and-dot that marks the vertical axis end-on (label 'vertical axis'); the segment's left end is a terracotta dot, its right end an ink dot. Light grey vertical lines drop from the two ends to the screen line, where two shadow dots mark the width (label 'the screen sees this'). The segment turns about the centre: the shadow dots slide together, shrink to one point at a quarter turn (label 'edge-on'), with the live caption 'width x cos'.",
      "The card's line turns and its shadow on the screen line shrinks to a point.",
      [{"at": 0.08, "event": "screen line, card line, shadow dots at full width"}, {"at": 0.20, "event": "the line turns; shadow dots slide together"}, {"at": 0.40, "event": "quarter turn: one point; settled"}, {"at": 0.62, "event": "labels 'edge-on' and 'width x cos'"}],
      "ShaderLab", "Seen from above, 'the width the screen sees' is a literal shadow; the shadow shrinking to a point is the cosine.",
      "Lab f1 (widths 118, 90, 48 px and nothing at 22.5, 45, 67.5 and 90 degrees: 128 x abs(cos))")

code08 = code_of("08-flip.gdshader")
lab("B28", 3, "the table for a turn around the vertical axis, and the flip", code08, "lab-shaders/08-flip.gdshader", "godot-shaders/matrices-flip-code.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweep of flip",
    [{"at": 0.06, "lines": [find_line(code08, "vec3 x_arrow"), find_line(code08, "vec3 y_arrow"), find_line(code08, "vec3 z_arrow"), find_line(code08, "mat3 around_y")], "label": "the three columns of the table"},
     {"at": 0.26, "lines": [find_line(code08, "vec3 y_arrow")]}, {"at": 0.62, "lines": [find_line(code08, "VERTEX = ")]}],
    "Code card at left with the real twelve-line shader; at right a framed Godot window with the card turning about its vertical axis. A readout 'y arrow stays' lands when the middle column is highlighted; the card ends at a forty-five degree turn, narrower, with the same height.",
    "The card narrows from the sides as the angle grows, while the middle column stays zero, one, zero.",
    [{"at": 0.06, "event": "the three arrow lines and the table"}, {"at": 0.26, "event": "middle column in focus; readout 'y arrow stays'"}, {"at": 0.62, "event": "VERTEX line; the card is mid-flip"}],
    "manim", "The real flip in the engine next to the real table; the middle column staying put is visible in the code and the card's unchanged height in the picture.",
    f"C08: 08-flip.gdshader on the card; {CARD.format(k='2.0')}; {BASE}; {secs('B28')} s. flip keyframes: 0.0 from 0.00 to 0.10, 0.125 at 0.34 (ease in-out), then hold 0.125. "
    "At the 50 % and 85 % marks: the card at 45 degrees, 90 card-pixels wide and 128 tall. Verified: width 90 x 128 (geometry-summary.txt); planning still png/still-flip-0.125.png.",
    "Lab f1 (flip 0.125 = 90 x 128); unit test u3 row 6 (Ry keeps its y arrow)", readouts=[{"at": 0.28, "text": "y arrow stays", "x": 0.5, "y": 0.92}])

lab("B29", 3, "edge-on at a quarter turn, then the mirrored front", code08, "lab-shaders/08-flip.gdshader", "godot-shaders/matrices-flip-edge-on.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweep of flip",
    [], "A framed Godot window, full width. The card narrows to nothing: for a moment the window shows only the stage and the readout 'edge-on: nothing drawn'; then the card reappears on the far side of the turn, mirrored (arrow pointing left, small square top right) with the readout 'mirrored'.",
    "The card narrows to nothing, the window is empty for a beat, and the card comes back mirrored.",
    [{"at": 0.10, "event": "card narrowing"}, {"at": 0.28, "event": "edge-on: window empty; readout 'edge-on: nothing drawn'"}, {"at": 0.44, "event": "card back, mirrored"}, {"at": 0.60, "event": "readout 'mirrored'"}],
    "manim top view with shadow dots swapping sides", "The strangest fact ('nothing is drawn') is only believable on the real thing; the capture shows the empty window.",
    f"C09: 08-flip.gdshader on the card; {CARD.format(k='2.0')}; {BASE}; {secs('B29')} s. flip keyframes: 0.15 from 0.00 to 0.10, 0.25 at 0.26 (ease), hold 0.25 until 0.34 (empty window), 0.5 at 0.44 (ease), hold 0.5. "
    "At the 50 % and 85 % marks: the mirrored card, fully visible. Verified: nothing drawn at flip 0.25 and 0.75; corner colours swap left to right at 0.5 (gradient texture); planning stills png/still-flip-0.25-edge-on.png and png/still-flip-0.5-mirrored.png.",
    "Lab f1 (empty at 0.25, 0.75), f2 (mirrored at 0.5)", layout="video",
    readouts=[{"at": 0.28, "text": "edge-on: nothing drawn", "x": 0.5, "y": 0.9}, {"at": 0.60, "text": "mirrored", "x": 0.5, "y": 0.9}])

manim("B30", 3, "three axes, three tables; the axis you turn around keeps its column", "ThreeAxesThreeTables",
      "Three small cards side by side, each with its own label under it: 'around x', 'around y', 'around z'. They turn together: the first tips (its height shrinks), the second flips (its width shrinks), the third spins flat. Under each card a small bracketed column of three numbers is ringed: (1 / 0 / 0), (0 / 1 / 0), (0 / 0 / 1), captioned 'stays put'.",
      "Three cards turn at once: one tips, one flips, one spins; the column that stays put is ringed under each.",
      [{"at": 0.10, "event": "three cards, three labels"}, {"at": 0.22, "event": "the cards turn together"}, {"at": 0.42, "event": "settled at 45 degrees"}, {"at": 0.62, "event": "rings on the three columns that stay put"}],
      "LectureEvidenceTable", "Three turns are a comparison of motions; seeing a tip, a flip and a spin together makes the difference between the axes obvious.",
      "Lab f1 (flip: width x abs(cos)), ft1 (tip: height x cos 36 degrees = 104 px); unit test u3 rows 6, 7 (the fixed column of Ry and Rx)")

code09 = code_of("09-flip-and-tip.gdshader")
a09 = start_of_vertex("09-flip-and-tip.gdshader")
ex09 = code_of("09-flip-and-tip.gdshader", a09, a09 + 3)
lab("B31", 3, "two turns multiplied: the card flips and leans", ex09, "lab-shaders/09-flip-and-tip.gdshader (the vertex function)", "godot-shaders/matrices-flip-and-tip.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweeps of flip and tip",
    [{"at": 0.10, "lines": [find_line(ex09, "mat3 m =")], "label": "right to left: flip first, then tip"}, {"at": 0.62, "lines": [find_line(ex09, "VERTEX = ")]}],
    "Code card at left with the four-line vertex function (around_x and around_y are the two small functions of the same file); at right a framed Godot window. The card first flips by an eighth of a turn, then leans forward; its outline ends as a slanted parallelogram. A readout 'a parallelogram' lands.",
    "The card flips and then leans, and its outline slants.",
    [{"at": 0.10, "event": "product line in focus"}, {"at": 0.16, "event": "the card flips"}, {"at": 0.32, "event": "the card leans; outline slants"}, {"at": 0.62, "event": "apply line in focus; readout 'a parallelogram'"}],
    "manim", "A real render of the product of two turns; the slanted outline is the evidence that stacked turns are more than a squeeze.",
    f"C10: 09-flip-and-tip.gdshader on the card; {CARD.format(k='2.0')}; {BASE}; {secs('B31')} s. Keyframes (ease in-out): flip 0 to 0.125 over 0.12-0.30; tip 0 to 0.1 over 0.30-0.44; hold. "
    "At the 50 % and 85 % marks: the final pose. Verified: bounding box x -45 to 45, y -78 to 78; left and right edges both 103.6 card-pixels (geometry-summary.txt); planning still png/still-flip-and-tip.png.",
    "Lab ft1 (bbox matches Rx x Ry); the two edges equal in length", readouts=[{"at": 0.64, "text": "a parallelogram", "x": 0.5, "y": 0.92}])

lab("B32", 3, "at an eighth of a turn both edges are the same height: no perspective", code08, "lab-shaders/08-flip.gdshader", "godot-shaders/matrices-flip-45.png",
    "Godot 4.7.2 · Forward+ · flip held at 0.125", [],
    "A framed Godot window with the card held at an eighth of a turn. A terracotta ring settles on the card's left edge and another on its right edge; readouts '128 px' land beside each, then 'no perspective' lands under the window.",
    "Two rings land on the two edges, each with the same number.",
    [{"at": 0.10, "event": "the card at 45 degrees"}, {"at": 0.20, "event": "ring on the left edge; readout '128 px'"}, {"at": 0.34, "event": "ring on the right edge; readout '128 px'"}, {"at": 0.66, "event": "readout 'no perspective'"}],
    "manim comparing a trapezoid with a rectangle", "The honest limit is a measurement: two real edges with the same number beats a drawing of what perspective would do.",
    f"C11: still PNG (3840 x 2160) of 08-flip.gdshader at flip 0.125; {CARD.format(k='2.0')}; Forward+. "
    "Verified: the card is 90 card-pixels wide and its two vertical edges are each 128 card-pixels tall (columns 44.5 px either side of centre measure 128 and 128). The rings and readouts are drawn by ShaderLab, not by the scene.",
    "Lab f1 (the 45 degree columns are 128 and 128); planning still png/still-flip-0.125.png", layout="video",
    rings=[{"at": 0.20, "box": [0.405, 0.30, 0.455, 0.70]}, {"at": 0.34, "box": [0.545, 0.30, 0.595, 0.70]}],
    readouts=[{"at": 0.22, "text": "128 px", "x": 0.37, "y": 0.26}, {"at": 0.36, "text": "128 px", "x": 0.63, "y": 0.26}, {"at": 0.66, "text": "no perspective", "x": 0.5, "y": 0.9}])

manim("B33", 3, "a box would show its sides; the table only turns a flat shape", "WhatABoxWouldShow",
      "The same top view as the earlier picture, now with a box: a square footprint centred on the end-on vertical axis, its front edge a terracotta line and its other three edges grey. The screen line below shows two shadow bars: an ink bar for 'what the table draws' (the front edge only) and a grey bar for 'what a box would show' (the whole footprint). The box turns a quarter turn: the ink bar shrinks to a point while the grey bar stays wide.",
      "The box turns; the table's bar shrinks to nothing while the bar the box should show stays wide.",
      [{"at": 0.08, "event": "box footprint, screen line, two bars the same width"}, {"at": 0.20, "event": "the box turns; the ink bar shrinks"}, {"at": 0.40, "event": "quarter turn: ink bar a point, grey bar still wide; settled"}, {"at": 0.62, "event": "labels 'drawn' and 'should show'"}],
      "ShaderLab", "'Fails for a box' is the gap between two shadows; the picture needs the same top view the flip was explained with.",
      "Math (orthographic shadow of a square footprint); design advice")

lab("B34", 3, "drive the flip from the game: a uniform from zero to one, times tau", code08, "lab-shaders/08-flip.gdshader", "godot-shaders/matrices-flip-sweep.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweep of flip",
    [{"at": 0.06, "lines": [find_line(code08, "uniform float flip")]}, {"at": 0.26, "lines": [find_line(code08, "float a = TAU")], "label": "TAU: one full turn"}],
    "Code card at left with the real twelve-line shader; at right a framed Godot window with the card. Readouts land as the sweep runs: 'flip 0' (front), 'flip 0.5' (the back, mirrored), 'flip 1' (the front again).",
    "The card goes front, back, front as the flip value passes zero, one half and one.",
    [{"at": 0.06, "event": "the uniform line"}, {"at": 0.26, "event": "float a = TAU * flip line"}, {"at": 0.40, "event": "readout 'flip 0'"}, {"at": 0.68, "event": "the back; readout 'flip 0.5'"}, {"at": 0.84, "event": "the front again; readout 'flip 1'"}],
    "manim number line from 0 to 1", "The three values and the three faces are real captures of the same file; the uniform and the tau line are in the code beside them.",
    f"C12: 08-flip.gdshader on the card; {CARD.format(k='2.0')}; {BASE}; {secs('B34')} s. flip keyframes: 0.0 until 0.56, 0.5 at 0.66 (ease), hold, 1.0 at 0.82 (ease), hold. "
    "At the 50 % mark: the front (flip 0). At 85 %: the front again (flip 1). Verified: set_shader_parameter drives the uniform (verify3 D1); flip 1.0 equals flip 0.0 (identity).",
    "Lab f1, f2; verify3 D1, D2", readouts=[{"at": 0.40, "text": "flip 0", "x": 0.5, "y": 0.92}, {"at": 0.68, "text": "flip 0.5", "x": 0.5, "y": 0.92}, {"at": 0.84, "text": "flip 1", "x": 0.5, "y": 0.92}])

# ═══════════════════════════ ACT V · The Pivot ═══════════════════════════
lab("B35", 4, "a door turns around its hinge: the pivot", code_of("11-door.gdshader"), "lab-shaders/11-door.gdshader", "godot-shaders/matrices-door-intro.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweep of flip, pivot on the left edge",
    [], "Act title 'The Pivot' (serif 40) top-left. A framed Godot window: the card swings like a door about its LEFT edge, a terracotta dot marks that edge (the hinge) and does not move while the rest of the card narrows toward it. Readout 'pivot' beside the dot; the caption reads 'pivot: the point it turns around'.",
    "The card swings about its left edge; the terracotta hinge dot never moves.",
    [{"at": 0.10, "event": "card at rest, hinge dot on its left edge"}, {"at": 0.24, "event": "card swings to a door-ajar pose about the hinge"}, {"at": 0.34, "event": "readout 'pivot'; caption defines the pivot"}, {"at": 0.62, "event": "held"}],
    "manim", "The target look first: a real door-like swing with a fixed hinge dot makes 'pivot' something the viewer can see.",
    f"C13: 11-door.gdshader with pivot (-64, 0) x U on the card; {CARD.format(k='2.0')}; a terracotta dot (radius 6 logical px) at the pivot, placed at the card's left edge midpoint; {BASE}; {secs('B35')} s. "
    "flip keyframes: 0.0 from 0.00 to 0.10, 0.15 at 0.36 (ease), hold 0.15. At the 50 % and 85 % marks: the card at 54 degrees, its left edge at the hinge dot. "
    "Verified: left edge stays at -64; right edge at -64 + 128 cos (geometry-summary.txt).",
    "Lab d1 (left edge fixed at -64 for flip 0.0625, 0.125, 0.1875); verify3 D3; planning still png/still-door-0.125-hinge-left.png",
    layout="video", title="The Pivot", caption="pivot: the point it turns around", readouts=[{"at": 0.34, "text": "pivot", "x": 0.40, "y": 0.62}])

manim("B36", 4, "the three steps: slide in, turn, slide back", "SlideTurnSlideBack",
      "The screen-direction grid with a small cross at the origin and a card whose left edge carries a terracotta pivot dot. Step 1 (label '1 slide in'): the card slides so that the pivot dot lands on the origin cross. Step 2 ('2 turn'): the card's width narrows and widens about the origin (a flip). Step 3 ('3 slide back'): the card slides back by the same amount, and the pivot dot returns to its original place; label 'the pivot never moved'.",
      "The card slides so the hinge dot sits on the origin, flips there, then slides back to where it was.",
      [{"at": 0.10, "event": "card with its pivot dot, origin cross"}, {"at": 0.18, "event": "step 1: the card slides; dot on the cross"}, {"at": 0.28, "event": "step 2: the card flips about the cross"}, {"at": 0.38, "event": "step 3: the card slides back; dot home"}, {"at": 0.66, "event": "label 'the pivot never moved'"}],
      "DesignPipelineClaim, show-tell isometric", "Three steps in order is a short animation; the card visibly travelling in, turning and travelling back is the claim.",
      "Lab c1, d1 (the pivot corner or edge stays); unit test u3 rows 4, 5")

a10 = start_of_vertex("10-spin-about-corner.gdshader")
ex10 = code_of("10-spin-about-corner.gdshader", a10, a10 + 5)
rem("B37", 4, "as a product, read right to left: slide in, turn, slide back", "ShaderLab",
    {"layout": "code", "code": ex10, "codeFile": "lab-shaders/10-spin-about-corner.gdshader (the vertex function)",
     "cues": [{"at": 0.10, "lines": [find_line(ex10, "* slide_by(-pivot)")], "label": "first: slide in"}, {"at": 0.30, "lines": [find_line(ex10, "* turn_by(angle)")], "label": "second: turn"},
              {"at": 0.58, "lines": [find_line(ex10, "mat3 m = slide_by(pivot)")], "label": "third: slide back"}, {"at": 0.80, "lines": [2, 3, 4], "label": "one table for all three"}],
     "video": "", "videoLabel": "", "readouts": [], "rings": [], "caption": "read it from the right", "durationSeconds": "__AUDIO__"},
    "A full-frame code card with the real six-line vertex function (the product written over three lines, one table per line). Focus climbs the product from the bottom line (slide in) to the middle (turn) to the top (slide back), then all three lines glow together.",
    "Focus climbs the three lines from the bottom up, the way the point meets the tables.",
    [{"at": 0.10, "event": "bottom table line: slide in"}, {"at": 0.30, "event": "middle table line: turn"}, {"at": 0.58, "event": "top table line: slide back"}, {"at": 0.80, "event": "all three lines together"}],
    "LectureCodeTrace", "The reading order runs bottom to top; LectureCodeTrace's focus only moves downward, so this needs ShaderLab's free line cues.",
    "Lab c1 (bounding boxes match slide x turn x slide); unit test u3 rows 4, 5")

lab("B38", 4, "a flat spin around a corner: the pendulum", ex10, "lab-shaders/10-spin-about-corner.gdshader (the vertex function)", "godot-shaders/matrices-corner-spin.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweep of angle, pivot on the top left corner", [],
    "A framed Godot window: the card swings like a pendulum about its TOP LEFT corner while a terracotta dot marks that corner and does not move. Readout 'pivot' beside the dot early, 'corner stays' when it has swung.",
    "The card swings round its top left corner; the terracotta dot stays put.",
    [{"at": 0.10, "event": "card at rest, dot on its top left corner"}, {"at": 0.22, "event": "readout 'pivot'"}, {"at": 0.30, "event": "card swings clockwise about the corner"}, {"at": 0.72, "event": "readout 'corner stays'"}],
    "manim", "A real swing with a fixed dot at the corner is the claim; the same file with a different pivot is the whole demonstration.",
    f"C14: 10-spin-about-corner.gdshader with pivot (-64, -64) x U on the card; {CARD.format(k='2.0')}; a terracotta dot at the pivot; {BASE}; {secs('B38')} s. "
    "angle keyframes: 0 from 0.00 to 0.10, 0.7854 at 0.36 (ease), hold until 0.62, 1.5708 at 0.80 (ease), hold. At the 50 % mark: the card turned 45 degrees about the corner. At 85 %: a quarter turn. "
    "Verified: bbox x -155 to 26, y -64 to 117 at 0.7854 (expected -154.5, 26.5, -64, 117); the top left corner stays at (-64, -64) (geometry-summary.txt).",
    "Lab c1; planning still png/still-corner-0.7854.png", layout="video",
    readouts=[{"at": 0.22, "text": "pivot", "x": 0.41, "y": 0.30}, {"at": 0.72, "text": "corner stays", "x": 0.5, "y": 0.92}])

manim("B39", 4, "pivot numbers are pixels from the node's origin: 64 or 128", "PixelsFromTheOrigin",
      "Two cards side by side, each with a ruler along its top edge. Left card 'centered': the origin dot in the middle, ruler ticks -64, 0, 64; a terracotta tick on the right edge reads '64'. Right card 'not centered': the origin dot at its top left corner, ticks 0 and 128; its right edge reads '128'. The right card appears later.",
      "Each card shows its origin dot and the number on its right edge: sixty-four for one, one hundred twenty-eight for the other.",
      [{"at": 0.10, "event": "left card, origin dot in the middle, ruler"}, {"at": 0.30, "event": "right edge reads 64"}, {"at": 0.40, "event": "settled"}, {"at": 0.60, "event": "right card: origin dot at its corner"}, {"at": 0.78, "event": "right edge reads 128"}],
      "LectureEvidenceTable", "The point is where the zero is; two cards with the zero in different places and different numbers on the same edge is the point.",
      "Verify2 O1 (a centered sprite's VERTEX runs -64 to 64; a sprite with centered off runs 0 to 128); Lab d3 (pivot (64, 0) holds the right edge)")

code11 = code_of("11-door.gdshader")
a11 = start_of_vertex("11-door.gdshader")
ex11 = code_of("11-door.gdshader", a11, len(file_lines("11-door.gdshader")))
rem("B40", 4, "for the flip: subtract the pivot, turn, add it back", "LectureCodeTrace",
    {"title": "Subtract, turn, add back", "code": ex11, "note": "A turn around y is a three-by-three table, so the slides are plain subtraction and addition · Godot 4.7.2",
     "cues": [0.04, 0.08, 0.14, 0.18, 0.22, 0.58, 0.72, 0.86, 0.92], "durationSeconds": "__AUDIO__"},
    "A cream code card with the real nine-line vertex function of the door shader; focus runs down the three arrow lines, then lands on the subtraction line, the turn line and the add-back line as each is named.",
    "Focus steps down the lines: the three arrows, then subtract the pivot, then turn, then add it back.",
    [{"at": 0.14, "event": "the three arrow lines"}, {"at": 0.58, "event": "subtract the pivot"}, {"at": 0.72, "event": "turn"}, {"at": 0.86, "event": "add the pivot back"}],
    "manim", "The three steps are three real lines of code in the order they run; paced line focus is exactly 'subtract, turn, add'.",
    "Lab d1, d4, verify3 D3 (the hinge edge stays at -64); unit test u3 row 13 (why the slides cannot be folded into the flip table)")

code11b = code_of("11-door.gdshader")
lab("B41", 4, "the door swings: the hinge edge never moves", code11b, "lab-shaders/11-door.gdshader", "godot-shaders/matrices-door-swing.mp4",
    "Godot 4.7.2 · Forward+ · scripted sweep of flip, pivot on the left edge", [],
    "A framed Godot window: the card swings like a door about its left edge, which carries the terracotta hinge dot. It folds toward the hinge to a door-ajar pose, then passes edge-on and ends flat on the far side of the hinge, mirrored (arrow pointing left). Readouts 'edge stays put' and 'far side, mirrored'.",
    "The card folds toward the hinge, vanishes for an instant, and ends lying on the other side, mirrored.",
    [{"at": 0.10, "event": "card at rest, hinge dot at its left edge"}, {"at": 0.22, "event": "card folds toward the hinge"}, {"at": 0.36, "event": "readout 'edge stays put'"}, {"at": 0.70, "event": "card passes edge-on and lands on the far side"}, {"at": 0.84, "event": "readout 'far side, mirrored'"}],
    "manim", "The payoff: the whole film in one render, a real door with a fixed hinge, mirrored on the far side.",
    f"C15: 11-door.gdshader with pivot (-64, 0) x U on the card; {CARD.format(k='2.0')}; a terracotta dot at the pivot; {BASE}; {secs('B41')} s. "
    "flip keyframes: 0.0 from 0.00 to 0.10, 0.125 at 0.30 (ease), hold until 0.60, 0.5 at 0.80 (ease; passes edge-on near 0.68), hold. "
    "At the 50 % mark: the card at 45 degrees with its left edge at the hinge. At 85 %: the card lies on the far side (left of the hinge), mirrored. "
    "Verified: left edge fixed at -64 at flip 0.0625, 0.125, 0.1875; at flip 0.5 the card spans -192 to -64 and its gradient corners are mirrored (geometry-summary.txt).",
    "Lab d1, d2, d4; verify3 D3; planning stills png/still-door-0.125-hinge-left.png and png/still-door-0.5-far-side.png", layout="video",
    readouts=[{"at": 0.36, "text": "edge stays put", "x": 0.5, "y": 0.92}, {"at": 0.84, "text": "far side, mirrored", "x": 0.5, "y": 0.92}])

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(len(N.ACTS)):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

lanes_hist = {}
for e in E:
    lanes_hist[e["entry"]["lane"]] = lanes_hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    cells = [e["bid"], e["about"], pick, en["runner_up"], en["why"], e["evidence"]]
    assert not any("|" in c for c in cells), f"a pipe inside a SHOTLIST cell would break the table: {e['bid']}"
    rows.append("| " + " | ".join(cells) + " |")
ids = [e["bid"] for e in E]
assert ids == [b for b, _, _ in N.BODY], "every body beat needs exactly one lane entry, in order"
sl = ["# Shot list: " + N.TITLE + "\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab capture of a tested file in `lab-shaders/`; the film shows no editor frame. Three shared pieces and four film-local things must exist before the build (below).\n",
      "## Must exist before the build\n",
      "Shared (specs in `../_godot-shaders-series/COMPONENT-SPECS.md`; built once, by whichever film is built first):\n",
      "1. **`ShaderLab`** Remotion component (code left, a moving Godot render right; `layout` side, stack, video or code; `cues`, `readouts`, `rings`, `caption`, `title`). This film also uses its `code` layout alone (B37) and its `caption` line as a one-line definition (B11, B13, B35).",
      "2. **`shader_kit.py`** Manim helpers (`vertex_quad`, `code_card`, `pixel_grid`, `uv_square`).",
      "3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` as the spec describes it (`--animate` schedules, `--scene`, `--material-at`, stills, keyframes as fractions of the clip with `--length`). This film adds only a scene script for the card (the `card` texture drawn at 1024 px, code in `evidence/planning-checks/runner-card.gd`; the unit factor U; the origin cross and hinge dot markers; the two panels of B22) and eased breakpoints (`CAPTURE-PLAN.md`, \"What the harness needs for this film\").\n",
      "Film-local (write them in this film's `scenes.py`, next to the scenes):\n",
      "4. **`screen_plane`**: a grid in Godot's directions, **x to the right and y DOWN** (Manim y = minus game y), with small axis labels; a warp helper that applies a two-by-two table to it (convert the table with y flipped: M' = F M F, F = diag(1, -1)).",
      "5. **`matrix_table`**: a bracketed grid (two vertical bracket lines, ink, stroke 4); every entry its own `Text` (EB Garamond, at least 40 at 2x2, at least 34 at 3x3) so one row or column can be outlined; a ring is a terracotta `RoundedRectangle` outline (no fill, no ink ring over text).",
      "6. **`card`**: a small cream rectangle with a warm grey outline, a teal arrow and a teal corner square drawn from shapes (the same card as in the captures); used in B23, B30, B36, B39.",
      "7. **`top_view`**: the end-on view of B27 and B33 (screen line, end-on axis marker, a turning segment or square, shadow dots or bars).\n",
      "**Docs screenshot** D1 for B05 via Playwright (see `CAPTURE-PLAN.md`).\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
