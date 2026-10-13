#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text, the cue times must follow the words of the narration, and
the shot list must say exactly what the lanes say. Re-run after any edit:
    python3 _gen_lanes.py && python3 make_sheet.py
Cue times are computed from the narration (T(bid, phrase) = where the phrase starts, as a fraction of the beat, by word count) and
nudged out of the 45 to 55 percent window, where no cue may start (the midpoint frame must be a settled still).
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
spec = importlib.util.spec_from_file_location("narration", HERE / "narration.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
TEXT = {bid: t for bid, _, t in N.BODY}
E = []          # entries in beat order
PUB = "patterns-and-pixelation"      # folder under runtime/remotion/public/ for this film's captures


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def ln(fn, needle):
    """1-based line number of the first line of the shader file that contains `needle`."""
    for i, line in enumerate(code_of(fn).split("\n"), 1):
        if needle in line:
            return i
    raise SystemExit(f"{fn}: no line contains {needle!r}")


def T(bid, phrase, lead=0.0):
    """Fraction of the beat at which `phrase` starts being spoken (by word count), nudged out of 0.45-0.55."""
    words = TEXT[bid].replace("\n", " ").split()
    low = TEXT[bid].replace("\n", " ")
    i = low.find(phrase)
    if i < 0:
        raise SystemExit(f"{bid}: phrase not found: {phrase!r}")
    before = len(low[:i].split())
    f = round(min(0.95, max(0.02, before / max(1, len(words)) + lead)), 2)
    if 0.38 <= f <= 0.55:                 # an animation starting here would still be moving at the 50 % frame
        f = 0.36 if f < 0.47 else 0.57
    return f


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


# What the 45 to 55 percent frame must show for each Manim beat (the midpoint rule: a settled still with the labels that matter).
MID = {
    "B02": "the strip is stretched and labelled 0 to 4, caption 'UV.x × 4'; the ticks have not appeared yet.",
    "B03": "the dot is settled at 2.9 with the readout 'floor = 2' (it runs there between 36 and 44 %); the label 'floor: rounds down' is on screen.",
    "B04": "the dot is paused at 2.9, height 0.9, with the label 'fract(2.9) = 0.9'; the curve is drawn as far as 2.9.",
    "B05": "the dot sits at (2.3, 1.7), cell (2, 1) has its heavy outline and the label 'cell (2, 1)'; the magnified cell has not opened yet.",
    "B09": "the strip has split into the two panels and the floor panel is full (block and checker icons); the fract panel is still empty.",
    "B11": "all sixteen lines have converged on the one lookup point; the cell has not taken its color yet.",
    "B14": "the line, the staircase and the double arrow 'half a block' are all settled; the two labels arrive after the midpoint.",
    "B16": "the stack shows '0.6 × 4 = 2.4' and 'floor gives 2'; the marker is at 0.6; the '+ 0.5' line has not typed yet.",
    "B18": "both rows are settled: sixteen equal blocks above, seventeen blocks below with half-width ends; the rings arrive after the midpoint.",
    "B20": "the pixel grid with the eight-pixel block outlined and labelled 'a block: 8 pixels across'; the question has not landed yet.",
    "B25": "the 128-pixel strip with its first block of six outlined and labelled 'block = 6'; the remaining blocks fill in after the midpoint.",
    "B26": "the dot has stepped one cell to the right and the number shows '+1'; the step down comes after the midpoint.",
    "B27": "the remainders are under the sums and the plain checkerboard beside the grid is complete; the line '3 mod 2 = 1' has not typed yet.",
    "B28": "the dot sits on cell (1, 1) with the '+2' label, two flip marks on the way and the bracket joining the pair; the corner mark arrives after the midpoint.",
    "B30": "the dot is held at the middle of the diagonal with the label 'UV.x + UV.y = 1.0' (it slides there between 36 and 44 %); the far corner comes after the midpoint.",
    "B31": "the full sawtooth of eight teeth is drawn and labelled 'sawtooth'; the threshold line and the stripe bar arrive after the midpoint.",
    "B35": "the dot is held inside the cell with its two numbers (0.3, 0.7) and the corner labels still read 0 and 1; the re-centering comes after the midpoint.",
    "B36": "the dot, its line to the middle and the circle of radius r are all settled with the label 'length'; the dot crosses the edge after the midpoint.",
}


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects)"):
    intent = intent + (f" Midpoint still (45 to 55 %): {MID[bid]}" if bid in MID else "")
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


FWD = "Godot 4.7.2 · Forward+ · nearest filter"

# ═════════════════════════════ ACT I · Which Cell, and Where in It ═════════════════════════════
lab("B01", 0, "four patterns, none of them an image", "01-showcase.gdshader", f"{PUB}/hook.mp4",
    f"{FWD} · one shader · value swept by script", [],
    "Act title 'Which Cell, and Where in It' (serif 40) top-left. A real Godot render in a framed window on the cream stage: one square "
    "split in four panels, all drawn by one shader: top left the teal test sprite going from smooth to chunky blocks, top right a "
    "teal-and-cream checkerboard scrolling, bottom left gold-and-cream diagonal stripes sliding, bottom right a grid of teal dots that "
    "swell and shrink. One-word labels land beside each panel as the voice names it.",
    "All four panels are alive at once: blocks coarsen, the checkerboard scrolls, the stripes slide, the dots pulse.",
    [{"at": T("B01", "Chunky"), "event": "label 'blocks' beside the top-left panel"}, {"at": T("B01", "A checkerboard"), "event": "label 'checker'"},
     {"at": T("B01", "Moving stripes"), "event": "label 'stripes'"}, {"at": T("B01", "A grid of dots"), "event": "label 'dots'"},
     {"at": T("B01", "All four"), "event": "label 'one trick' under the whole square"}],
    "manim drawing of four small pattern icons", "The claim is that one shader draws four different effects; only a real render of all four "
    "at once, moving, shows that. A drawing would only assert it.",
    "C01: Lab sprite scene (teal test sprite, scale to fit), lab-shaders/01-showcase.gdshader with the uniform phase swept linearly "
    "0 to 1 over 12 s (--animate phase:0:1), 30 fps, Forward+, nearest filter, no input. At 50 %: all four panels visible, pixelation "
    "mid-way. At 85 %: blocks coarse, dots mid-swell.",
    "Lab renders 01-showcase at phase 0, 0.25, 0.5, 0.75, 1.0 (compiled, looked at)", layout="video", title=N.ACTS[0][1], code="",
    code_file="lab-shaders/01-showcase.gdshader",
    readouts=[{"at": T("B01", "Chunky"), "text": "blocks", "x": 0.15, "y": 0.30}, {"at": T("B01", "A checkerboard"), "text": "checker", "x": 0.85, "y": 0.30},
              {"at": T("B01", "Moving stripes"), "text": "stripes", "x": 0.15, "y": 0.70}, {"at": T("B01", "A grid of dots"), "text": "dots", "x": 0.85, "y": 0.70},
              {"at": T("B01", "All four"), "text": "one trick", "x": 0.5, "y": 0.95}])
manim("B02", 0, "the address, stretched by four", "StretchTheAddress",
      "The series ramp strip across the stage (a bar of light-to-mid greys, never near-black), end labels 0 and 1, caption 'UV.x' above it. "
      "It stretches: the right end label counts 1, 2, 3, 4 and the caption becomes 'UV.x × 4'; vertical tick lines grow at 1, 2 and 3, "
      "cutting the bar into four spans, and the whole numbers 0, 1, 2, 3 appear under the left end of each span.",
      "The right label counts up to 4 while the ticks grow at each whole number.",
      [{"at": T("B02", "Start with"), "event": "ramp strip, labels 0 and 1, caption UV.x"},
       {"at": T("B02", "Multiply it by four"), "event": "right label counts to 4; caption becomes UV.x × 4"},
       {"at": T("B02", "Each whole number"), "event": "ticks at 1, 2, 3; span numbers 0 to 3"}],
      "ShaderLab: a Lab gradient render", "The idea is the whole numbers appearing along the ramp; a render would show a gradient but not "
      "where the whole numbers fall.")
manim("B03", 0, "floor: which cell you are in", "FloorSteps",
      "The same ramp, now 0 to 4 with ticks at 1, 2, 3 (cast continues). A terracotta dot rides it with a live value above it; at the right "
      "a large readout 'floor = 0' (monospace) steps up only when the dot crosses a tick. The dot pauses at 0.7 (readout shows 0.7 and 0), "
      "runs on, pauses at 2.9 (readout shows 2.9 and 2). The span under the dot is underlined by a terracotta bar. Label under the bar: "
      "'floor: rounds down'.",
      "The dot slides and the floor readout changes only at the ticks: 0, 1, 2, 3.",
      [{"at": T("B03", "Floor tells you"), "event": "dot at 0.7, floor = 0, span 0 underlined"},
       {"at": T("B03", "Floor rounds down"), "event": "label 'floor: rounds down'; the dot holds at 0.7: readout 0.7 gives 0"},
       {"at": 0.36, "event": "the dot runs on quickly to 2.9, the readout stepping 1, 2 as it crosses the ticks (finished by 44 %)"},
       {"at": 0.62, "event": "span 2 underlined; the cell numbers 0, 1, 2, 3 light in turn"}],
      "plot of the staircase floor(x)", "The claim is 'which step you are on': a dot crossing ticks with a readout that changes only there "
      "says it directly; a staircase plot comes next, for fract.",
      "Manim only; spoken values checked in the Lab: floor(2.9) = 2, floor(0.7) = 0 (chk-floor-fract-values)")
manim("B04", 0, "fract: where inside the cell", "FractSawtooth",
      "Axes on the cream stage: x from 0 to 4 along the bottom with ticks at the whole numbers, y from 0 to 1. A terracotta dot travels along "
      "x and draws the sawtooth of fract(x) behind it: a ramp from 0 to 1 that drops back to 0 at each whole number. At x = 2.9 the dot "
      "pauses at height 0.9 with the label 'fract(2.9) = 0.9'. The formula 'fract(x) = x − floor(x)' sits above the plot.",
      "The curve draws itself, climbing from 0 to 1 and snapping back to 0 at every whole number.",
      [{"at": T("B04", "Fract keeps"), "event": "axes; the sawtooth starts to draw; formula above"},
       {"at": T("B04", "Two point nine"), "event": "dot pauses at 2.9, height 0.9, label fract(2.9) = 0.9"},
       {"at": T("B04", "Inside every cell"), "event": "the last teeth draw; every drop marked at a whole number"}],
      "ramp strip with a second strip below", "A sawtooth is the exact picture of 'climbs, then starts over'; two strips would hide the reset.",
      "Docs: fract returns x - floor(x); Lab: fract(2.9) = 0.9 (chk-floor-fract-values)")
manim("B05", 0, "both numbers name one spot", "WhichAndWhere",
      "A square 4 by 4 grid of outline cells at left (no fill behind text), column numbers 0 to 3 along the top, row numbers 0 to 3 down "
      "the left side. A terracotta dot travels to the point 2.3 across and 1.7 down. Cell (2, 1) gets a heavy outline. At right, that one "
      "cell is magnified as a unit square with the dot inside it. Labels: 'cell (2, 1)' beside the grid and 'inside (0.3, 0.7)' beside the "
      "magnified cell.",
      "The dot lands, its cell lights up, and the cell opens out to show where inside it the dot sits.",
      [{"at": T("B05", "Together"), "event": "grid; dot travels to (2.3, 1.7)"}, {"at": T("B05", "Floor says"), "event": "cell (2, 1) outlined; label 'cell (2, 1)'"},
       {"at": T("B05", "Fract says"), "event": "cell magnified, dot inside; label 'inside (0.3, 0.7)'"}],
      "ShaderLab with a Lab render", "A dot with both numbers read off live is the idea; the two spoken pairs land on two visible labels.")
lab("B06", 0, "floor drawn as colors", "02-cells-floor.gdshader", f"{PUB}/cells-floor.png", f"{FWD} · the shader on the left",
    [{"at": T("B06", "which Godot calls"), "lines": [1], "label": "canvas_item: a shader for 2D drawing"},
     {"at": T("B06", "The address is a pair"), "lines": [ln("02-cells-floor.gdshader", "vec2 p"), ln("02-cells-floor.gdshader", "floor(p)")], "label": "vec2: a pair of numbers"},
     {"at": T("B06", "Red follows"), "lines": [ln("02-cells-floor.gdshader", "COLOR")], "label": "COLOR: the pixel's color"}],
    "Code card at left (the stretched address, floor, the color line); at right a real Godot window: a square of sixteen flat-colored cells, "
    "red growing with the column and green with the row. The highlighted lines carry short labels: canvas_item, vec2, COLOR.",
    "The floor line is highlighted, then the color line, while sixteen flat cells sit in the window.",
    [{"at": T("B06", "which Godot calls"), "event": "first line highlighted, label canvas_item: a shader for 2D drawing"},
     {"at": T("B06", "The address is a pair"), "event": "stretch and floor lines highlighted, label vec2: a pair of numbers"},
     {"at": T("B06", "Red follows"), "event": "COLOR line highlighted, label COLOR: the pixel's color; red and green steps traced across and down"}],
    "LectureCodeTrace alone", "Code and its picture side by side is the claim: the same two numbers for every pixel of a cell.",
    "C02: Lab sprite, white 128 px texture (--sprite-tex white), lab-shaders/02-cells-floor.gdshader, still PNG. Verified: 16 distinct colors; "
    "cell (0,0) = 0.25, 0.25, 0.55; cell (3,3) = 1.0, 1.0, 0.55; every pixel matches the formula (verify-patterns.py).",
    "Lab probes 02-cells-floor (360x360 rect and sprite renders)",
    ramp={"at": T("B06", "Red follows"), "from": 0, "to": 1})
lab("B07", 0, "fract drawn as colors", "03-cells-fract.gdshader", f"{PUB}/cells-fract.png", f"{FWD} · the shader on the left",
    [{"at": T("B07", "Now fract"), "lines": [ln("03-cells-fract.gdshader", "fract(p)")]},
     {"at": T("B07", "Red grows"), "lines": [ln("03-cells-fract.gdshader", "COLOR")]}],
    "Code card at left; at right a real Godot window: the square of four by four cells again, but every cell holds the same small gradient "
    "(red growing left to right, green top to bottom), restarting at each border.",
    "The fract line, then the color line, are highlighted while sixteen identical gradients fill the window.",
    [{"at": T("B07", "Now fract"), "event": "fract line highlighted"}, {"at": T("B07", "Every cell holds"), "event": "ring on one cell, then its copy in another"},
     {"at": T("B07", "Red grows"), "event": "COLOR line highlighted"}],
    "manim drawing of sixteen gradients", "Sixteen identical gradients are only convincing as a real render, with the code that makes them.",
    "C03: Lab sprite, white texture, lab-shaders/03-cells-fract.gdshader, still PNG. Verified: all sixteen 90 px tiles of the 360x360 render are "
    "pixel-identical; the render matches the formula at every pixel.", "Lab 03-cells-fract (tiles identical)",
    rings=[{"at": T("B07", "Every cell holds"), "box": [0.27, 0.10, 0.50, 0.40]}])
lab("B08", 0, "fract as the address into a picture: tiling", "04-tile.gdshader", f"{PUB}/tile.png", f"{FWD} · the shader on the left",
    [{"at": T("B08", "Read a picture"), "lines": [ln("04-tile.gdshader", "fract(")]},
     {"at": T("B08", "Here:"), "lines": [ln("04-tile.gdshader", "COLOR")], "label": "texture(): read the picture at an address"}],
    "Code card at left; at right a real Godot window: the teal test sprite repeated three times across and three down inside its square, "
    "the stage showing through its transparent padding.",
    "Nine copies of the sprite sit in a three by three grid; the fract line is highlighted, then the texture line.",
    [{"at": T("B08", "Read a picture"), "event": "fract line highlighted"}, {"at": T("B08", "Here:"), "event": "texture line; the 3 by 3 grid of copies traced"}],
    "manim drawing of nine copies", "A tiled floor is best seen as the real result of two lines.",
    "C04: Lab sprite (sprite texture), lab-shaders/04-tile.gdshader, still PNG. Verified: nine copies; tiles differ from the first by at most 21 of "
    "9,216 pixels (edge pixels).", "Lab 04-tile (nine copies)")
manim("B09", 0, "a map of the film: floor pixelates, fract repeats", "WhatComesNext",
      "A map diagram. At left a ramp strip splits (two drawn arrow shapes) into two panels. Panel one, title 'floor', text 'one per cell', "
      "with two small drawn icons: pixel blocks and a checkerboard. Panel two, title 'fract', text 'repeats', with two small drawn icons: "
      "diagonal stripes and a dot grid. Below, both panels send an arrow to one last icon, a dot screen, labelled 'both'.",
      "The strip splits, each panel fills with its icons in turn, and the two arrows merge on the dot screen.",
      [{"at": T("B09", "Here is the map"), "event": "ramp strip splits into the two panels"},
       {"at": T("B09", "Floor gives"), "event": "floor panel: block and checker icons"},
       {"at": T("B09", "Fract gives"), "event": "fract panel: stripe and dot icons"},
       {"at": T("B09", "Use both"), "event": "arrows merge on the dot screen, label 'both'"}],
      "FormBCard with library icons", "The point is a structure with a shape (two roles, one merge); drawn arrows and small pictures beat "
      "a card of words.")

# ═════════════════════════════ ACT II · Pixelate Without the Drift ═════════════════════════════
lab("B10", 1, "pixelate: the goal, big blocks", "06-pixelate-center.gdshader", f"{PUB}/pixelate-goal.mp4",
    f"{FWD} · blocks 128, 64, 32, 16, 8 · scripted sweep", [],
    "Act title 'Pixelate Without the Drift' (serif 40) top-left. A real Godot render: the teal test sprite, smooth at first, then coarser in "
    "five steps until it is a chunky grid of blocks. Caption: 'pixelate: show a picture as big blocks'.",
    "The sprite loses detail in steps, each step a coarser grid of flat blocks.",
    [{"at": 0.02, "event": "act title, caption 'pixelate: show a picture as big blocks'; sprite at full detail"},
     {"at": T("B10", "Inside a block"), "event": "coarser steps as the voice says every pixel has the same color"},
     {"at": T("B10", "So how"), "event": "chunkiest step held"}],
    "manim drawing of blocks", "The beat names the goal; the real sprite going chunky is the goal, and the code comes next.",
    "C05: Lab sprite (teal sprite, fit scale), lab-shaders/06-pixelate-center.gdshader; blocks stepped 128, 64, 32, 16, 8, each held 1.6 s (8 s), "
    "30 fps, Forward+, nearest filter. Verified still renders at all five values (06-center-n128 to n8-sprite-fit).",
    "Lab renders 06-center at 128, 64, 32, 16, 8 blocks", layout="video", title=N.ACTS[1][1],
    caption="pixelate: show a picture as big blocks")
manim("B11", 1, "one lookup per cell", "OneLookupPerCell",
      "A cell drawn as a four by four grid of pixel dots above a horizontal strip that stands for the picture (a teal-to-cream gradient bar). "
      "Sixteen thin curved lines run from the pixel dots down to ONE terracotta lookup point on the strip, with the words 'which spot?' beside "
      "it. Then the cell's pixels all take the one color found there. Label: 'one cell, one spot'.",
      "All sixteen lines converge on a single point and the cell takes one color.",
      [{"at": T("B11", "Make every"), "event": "cell of pixels over the picture strip; the sixteen lines converge on one point (finished by 38 %)"},
       {"at": 0.57, "event": "the cell's pixels all take the one color found there; label 'one cell, one spot'"},
       {"at": T("B11", "The only question"), "event": "'which spot?' beside the point"}],
      "ShaderLab render of a pixelated sprite", "Many pixels sending their lookups to one spot is a geometry of arrows; motion shows the convergence.")
lab("B12", 1, "first guess: look up the cell's top left corner", "05-pixelate-corner.gdshader", f"{PUB}/pixelate-corner.png", f"{FWD} · 16 blocks",
    [{"at": T("B12", "First guess"), "lines": [ln("05-pixelate-corner.gdshader", "floor(UV")]},
     {"at": T("B12", "All the pixels"), "lines": [ln("05-pixelate-corner.gdshader", "COLOR")]}],
    "Code card at left (uniform blocks, the snapped address, the texture lookup); at right a real Godot window: the sprite pixelated into sixteen "
    "by sixteen blocks.",
    "The floor-and-divide line is highlighted, then the texture line, with the blocky sprite in the window.",
    [{"at": T("B12", "First guess"), "event": "snap line highlighted"}, {"at": T("B12", "All the pixels"), "event": "texture line highlighted"}],
    "LectureCodeTrace alone", "Code and its result side by side: one line of snapping and the picture is in blocks.",
    "C06: Lab sprite (fit scale), lab-shaders/05-pixelate-corner.gdshader, blocks = 16, still PNG. Verified: 16 blocks of 8 picture pixels each way.",
    "Lab 05-pixelate-corner (blocks 8 px, all equal)")
lab("B13", 1, "the drift: the picture jumps down and to the right", "05-pixelate-corner.gdshader", f"{PUB}/pixelate-corner-switch.mp4",
    f"{FWD} · same scene, shader switched on · scripted",
    [{"at": T("B13", "Watch the sprite"), "lines": [ln("05-pixelate-corner.gdshader", "floor(UV")]}],
    "Code card at left; at right a real Godot window: the plain teal sprite sits still for a few seconds with a terracotta ring (grey backing) on its "
    "silhouette, then the shader switches on and the sprite jumps down and to the right out of the ring. Readouts '3.5 px right' and '3.5 px down' "
    "land beside it.",
    "The sprite is still, then jumps down and to the right the moment the shader switches on.",
    [{"at": 0.0, "event": "plain sprite with a ring on its silhouette"}, {"at": T("B13", "It jumps"), "event": "shader switches on; the sprite jumps down and right"},
     {"at": T("B13", "That is half"), "event": "readouts: 3.5 px right, 3.5 px down"}],
    "manim animation of an arrow shifting a sprite", "A real jump measured against a fixed ring is the evidence; a drawing would only illustrate it.",
    f"C07: Lab sprite (fit scale), lab-shaders/05-pixelate-corner.gdshader, blocks = 16, no material until the voice says \"It jumps\" (about {T('B13', 'It jumps') * 100:.0f} % of the beat) then the shader is assigned "
    "(--material-at, set from the audio), about 12 s, 30 fps, Forward+, nearest filter. Verified (verify-patterns.py): the sprite's centre moves +3.5, +3.5 picture "
    "pixels at 8-pixel blocks (+7.5 at 16-pixel blocks, +1.5 at 4-pixel blocks): half a block, less the half-pixel of the measurement. "
    "At 50 %: shader on. At 85 %: shader on.",
    "analysis: centroid shift +3.5, +3.5 px (blocks 8 px); +7.5 (16 px); +1.5 (4 px)",
    readouts=[{"at": T("B13", "That is half"), "text": "3.5 px right", "x": 0.80, "y": 0.35}, {"at": T("B13", "That is half") + 0.03, "text": "3.5 px down", "x": 0.80, "y": 0.55}],
    rings=[{"at": 0.0, "box": [0.36, 0.25, 0.64, 0.75]}])
manim("B14", 1, "why the corner lookup drifts", "WhyItDrifts",
      "One dimension, drawn large. A straight diagonal line (the picture, a ramp) over eight cells marked on the axis. A terracotta dot sits on the "
      "line at the left edge of each cell with a short drop line down to a flat tread: together the treads form a staircase under the line. "
      "A double-headed arrow shape between the line and the middle of a tread is labelled 'half a block'. Labels: 'the picture', "
      "'what the blocks show'.",
      "The lookup dots drop one by one, the staircase builds under the line, and the half-block gap is marked.",
      [{"at": T("B14", "Why?"), "event": "line over eight cells"}, {"at": T("B14", "A block shows"), "event": "lookup dots at each left edge drop to treads; staircase builds (finished by 33 %)"},
       {"at": T("B14", "So the picture"), "event": "double arrow 'half a block' between line and tread middle (finished by 44 %)"},
       {"at": 0.57, "event": "labels 'the picture' and 'what the blocks show' appear"}],
      "ShaderLab with an overlay", "A staircase lying half a step off the line is exactly 'arrives late by half a block'; the picture needs "
      "no pixels, so a clean one-dimensional drawing wins.",
      "Derivation (x/8 staircase of left-edge values is the line shifted half a cell); analysis: first block shows picture pixel 0, last shows 120 (verify-patterns.py)")
lab("B15", 1, "the fix: look up the middle of the cell", "06-pixelate-center.gdshader", f"{PUB}/pixelate-center-switch.mp4",
    f"{FWD} · same scene, shader switched on · scripted",
    [{"at": T("B15", "The fix"), "lines": [ln("06-pixelate-center.gdshader", "floor(UV")]}, {"at": T("B15", "Now a block"), "lines": [ln("06-pixelate-center.gdshader", "COLOR")]}],
    "Code card at left (the snapped address now with + 0.5 added to the floor before the divide); at right the same scene: the plain sprite with its "
    "ring, then the shader switches on and the sprite turns blocky but stays inside the ring. Readout 'stays put'.",
    "The sprite turns blocky at the switch but does not move: it stays inside its ring.",
    [{"at": 0.0, "event": "plain sprite with ring"}, {"at": T("B15", "Add one half"), "event": "plus-half highlighted; the shader switches on, the sprite stays put"},
     {"at": T("B15", "Now a block"), "event": "readout 'stays put'"}],
    "manim animation of a sprite staying put", "A non-event needs a fixed reference: the ring that the earlier jump left makes 'stays put' visible.",
    f"C08: Lab sprite (fit scale), lab-shaders/06-pixelate-center.gdshader, blocks = 16, material assigned at the voice's 'Add one half' (about {T('B15', 'Add one half') * 100:.0f} % of the beat, "
    "--material-at, set from the audio), about 11 s, 30 fps, Forward+, nearest filter. Verified: the sprite's centre moves -0.5, -0.5 picture pixels (less than one pixel). At 50 %: shader on. At 85 %: shader on.",
    "analysis: centroid shift -0.5, -0.5 px", readouts=[{"at": T("B15", "Now a block"), "text": "stays put", "x": 0.80, "y": 0.45}],
    rings=[{"at": 0.0, "box": [0.36, 0.25, 0.64, 0.75]}])
manim("B16", 1, "a worked example of the formula", "WorkedExample",
      "A number line from 0 to 1 cut into four cells (ticks at 0.25, 0.5, 0.75). A terracotta marker sits at the address 0.6. Beside it an "
      "arithmetic stack types in line by line (monospace): '0.6 × 4 = 2.4', 'floor gives 2' (a word, never an arrow glyph), "
      "'+ 0.5 = 2.5', '÷ 4 = 0.625'. The third cell (0.5 to 0.75) gets a heavy outline and a terracotta lookup dot lands at its middle, 0.625.",
      "The marker's number is carried through the four steps and the lookup dot lands exactly in the middle of its cell.",
      [{"at": T("B16", "Address point six"), "event": "number line, four cells, marker at 0.6"}, {"at": T("B16", "Times four"), "event": "stack: 0.6 × 4 = 2.4"},
       {"at": T("B16", "Floor gives"), "event": "stack: floor gives 2"}, {"at": T("B16", "Add a half"), "event": "stack: + 0.5 = 2.5"},
       {"at": T("B16", "Divide by four"), "event": "÷ 4 = 0.625; dot lands in the middle of the third cell"}],
      "LectureCodeTrace with annotations", "A number carried through four operations and landing in a cell is arithmetic made visible; "
      "code alone hides the numbers.",
      "Lab: chk-worked-example (0.6 × 4 / 4 = 0.6; floor(2.4) / 4 = 0.5; (2 + 0.5) / 4 = 0.625)")
lab("B17", 1, "the tempting variant: half inside the floor", "07-pixelate-round.gdshader", f"{PUB}/pixelate-round.png", f"{FWD} · 16 blocks",
    [{"at": T("B17", "Here is a tempting"), "lines": [ln("07-pixelate-round.gdshader", "floor(UV")]}, {"at": T("B17", "The picture no longer"), "lines": [ln("07-pixelate-round.gdshader", "COLOR")]}],
    "Code card at left (the half is now inside the floor); at right a real Godot window: the sprite pixelated, centered where the original was, "
    "with the terracotta ring (grey backing) around the original silhouette.",
    "The plus-half is highlighted inside the floor while the sprite sits inside its ring: no drift.",
    [{"at": T("B17", "Here is a tempting"), "event": "floor(UV * blocks + 0.5) line highlighted"}, {"at": T("B17", "The picture no longer"), "event": "ring around the sprite: it did not move"}],
    "manim code trace without the render", "The variant is code, and it looks right on the sprite: the real render with its ring is the honest 'looks fixed'.",
    "C09: Lab sprite (fit scale), lab-shaders/07-pixelate-round.gdshader, blocks = 16, still PNG. Verified: the sprite's centre -0.5, -0.5 px (no drift); "
    "the edge problem is not visible on the sprite (transparent padding) and is shown in B18 from the gradient run.",
    "Lab 07-pixelate-round (no drift: -0.5, -0.5 px)", rings=[{"at": T("B17", "The picture no longer"), "box": [0.36, 0.25, 0.64, 0.75]}])
manim("B18", 1, "the rounding variant makes half-size edge blocks", "HalfSizeEdges",
      "Two rows of blocks across a bracket labelled 'picture, 128 px' (the pixel-grid cast; outline cells with padding, no fill behind text). "
      "Top row, 'middle of the cell': sixteen equal blocks, each labelled 8 px at the first one. Bottom row, 'nearest grid line': the same grid shifted half "
      "a block, so seventeen blocks: the first and last are half width and wear terracotta rings with the label '4 px'; a middle block is labelled '8 px'. "
      "A small grey credit: 'Godot 4.7.2 · Forward+ · 16 blocks'.",
      "The grid slides half a block and the first and last blocks are cut to half width inside their rings.",
      [{"at": T("B18", "Look at the edges"), "event": "bracket and the top row of sixteen equal blocks"},
       {"at": T("B18", "The grid is shifted"), "event": "bottom row slides half a block; seventeen blocks, ends half width"},
       {"at": T("B18", "Measured"), "event": "rings on both end blocks: 4 px; a middle block: 8 px; credit line"}],
      "ShaderLab on a gradient render", "A row of blocks with the end cells cut in half is a pixel-grid picture; the dark corner of the real gradient "
      "render would also fail the type gate.",
      "analysis (gradient run): rounding variant block widths 4, 8 (fifteen times), 4; the other two variants sixteen blocks of 8 (verify-patterns.py)")
rem("B19", 1, "the three lookups compared", "LectureEvidenceTable",
    {"title": "Three places to look up", "headers": ["Look up", "Formula", "What you get"],
     "rows": [["the cell's top left corner", "floor(UV * n) / n", "drifts: 3.5 px right and down"],
              ["the nearest grid line", "floor(UV * n + 0.5) / n", "no drift, half-size edge blocks"],
              ["the middle of the cell", "(floor(UV * n) + 0.5) / n", "no drift, all blocks equal"]],
     "note": "Godot 4.7.2 · Forward+ · 128 px picture, n = 16 blocks across", "cues": [T("B19", "The corner"), T("B19", "The nearest"), T("B19", "The middle")],
     "durationSeconds": "__AUDIO__"},
    "A three-row table, the row for each lookup ringed as the voice names it; the last row (the middle) ends ringed in terracotta.",
    "The ring steps down the three rows with the voice and settles on the last.",
    [{"at": T("B19", "The corner"), "event": "row one"}, {"at": T("B19", "The nearest"), "event": "row two"}, {"at": T("B19", "The middle"), "event": "row three"}],
    "manim table drawn on cue", "A summary of three parallel results is exactly what the table component is for; each row was already shown moving.",
    "analysis rows: shifts +3.5 / -0.5 / -0.5 px; block widths all 8 / 4 at the ends / all 8 (verify-patterns.py)")

# ═════════════════════════════ ACT III · Blocks of Any Size ═════════════════════════════
manim("B20", 2, "a block is a number of picture pixels", "BlockInPixels",
      "Act title 'Blocks of Any Size' (serif 40) top-left. A pixel grid of 16 by 8 outline cells for the picture (the series pixel-grid cast). "
      "An eight-by-eight group of the pixels is outlined heavily and labelled 'a block: 8 pixels across'. Beside the grid a terracotta question mark "
      "with the words 'how many pixels does the picture have?'.",
      "The heavy outline grows over eight pixels of the grid and the question lands beside it.",
      [{"at": 0.04, "event": "act title; pixel grid"}, {"at": T("B20", "But you think"), "event": "eight-pixel block outlined, label 'a block: 8 pixels across'"},
       {"at": T("B20", "For that"), "event": "question 'how many pixels does the picture have?'"}],
      "LectureCodeTrace", "The thought is 'a block is a count of pixels'; a grid with a block outlined is that picture.")
rem("B21", 2, "TEXTURE_PIXEL_SIZE in the docs", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html",
     "image": f"{PUB}/docs-texture-pixel-size.png", "caption": "Godot 4.7 documentation · Canvas item shaders · Fragment built-ins · captured at build time",
     "frame": "browser", "moves": [{"at": 0, "x": 0.5, "y": 0.4, "scale": 1}, {"at": T("B21", "Texture pixel size"), "x": 0.5, "y": 0.45, "scale": 1.5}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 canvas item shader page, Fragment built-ins table, in a browser window; the camera pushes in on the TEXTURE_PIXEL_SIZE row "
    "('Normalized pixel size of the default 2D texture ... 64×32 pixels ... vec2(1.0 / 64.0, 1.0 / 32.0)') and a terracotta ring marks it.",
    "The camera pushes in on the row the voice is describing.",
    [{"at": 0, "event": "the page"}, {"at": T("B21", "Texture pixel size"), "event": "push-in and ring on the TEXTURE_PIXEL_SIZE row"}],
    "manim: a sprite with its pixel size marked", "A claim about a built-in is a documentation claim; the documentation itself is the evidence (SHOW-THE-THING).",
    "Playwright capture of the live docs page (1600x900 at 2.4x) at build time: the second TEXTURE_PIXEL_SIZE row on the page (Fragment built-ins). "
    "Read 2026-10-13: 'Normalized pixel size of the default 2D texture.' Lab: 1 / TEXTURE_PIXEL_SIZE = 128, 128 on the test sprite; 1, 1 on a Color Rect (no texture).")
lab("B22", 2, "block size in picture pixels", "08-pixelate-block.gdshader", f"{PUB}/pixelate-block.png", f"{FWD} · block = 8",
    [{"at": T("B22", "Multiply texture"), "lines": [ln("08-pixelate-block.gdshader", "TEXTURE_PIXEL_SIZE")], "label": "float(): a whole number as a decimal"},
     {"at": T("B22", "Divide, floor"), "lines": [ln("08-pixelate-block.gdshader", "floor(UV / cell)")]}],
    "Code card at left (an int uniform block with a range, the cell in address units, the snapped address with the half); at right a real Godot "
    "window: the sprite pixelated with blocks of eight picture pixels.",
    "The cell line is highlighted, then the snap line, with the blocky sprite in the window.",
    [{"at": T("B22", "Multiply texture"), "event": "cell line highlighted"}, {"at": T("B22", "Divide, floor"), "event": "snap line highlighted"},
     {"at": T("B22", "Eight means"), "event": "readout '8 px'"}],
    "LectureCodeTrace alone", "Two new lines and the picture they make, together; nothing else shows that the recipe is the same.",
    "C10: Lab sprite (fit scale), lab-shaders/08-pixelate-block.gdshader, block = 8, still PNG. Verified: identical to blocks = 16 of the middle-lookup "
    "version (0 of 230,400 pixels differ on the gradient at scale 1.0); the uniform is an int with hint_range(1, 32).",
    "Lab 08-pixelate-block (block 8 = 16 blocks: 0 px differ)", readouts=[{"at": T("B22", "Eight means"), "text": "8 px", "x": 0.80, "y": 0.45}])
lab("B23", 2, "the block size as a uniform, animated", "08-pixelate-block.gdshader", f"{PUB}/pixelate-block-sweep.mp4",
    f"{FWD} · block 1, 2, 4, 8, 16, 32 · scripted sweep",
    [{"at": T("B23", "Make the block size"), "lines": [ln("08-pixelate-block.gdshader", "uniform int block")], "label": "hint_range: the allowed values"}],
    "Code card at left with the uniform line highlighted; at right a real Godot window: the sprite from the original picture (block 1) to six "
    "steps of growing blocks up to 32. A readout shows the current block size.",
    "The picture coarsens in six steps as the block size doubles.",
    [{"at": T("B23", "Make the block size"), "event": "uniform line highlighted; block = 1, the original"}, {"at": T("B23", "One is"), "event": "steps 2, 4, 8"},
     {"at": T("B23", "A pixelating transition"), "event": "steps 16 and 32 held"}],
    "ShaderLab: one still per block size", "The claim is 'one number animates the effect'; only motion through the values shows it.",
    "C11: Lab sprite (fit scale), lab-shaders/08-pixelate-block.gdshader; block stepped 1, 2, 4, 8, 16, 32, each held 1.2 s (7.2 s), 30 fps, "
    "Forward+, nearest filter, scripted. Verified: block 1 is pixel-identical to the untouched sprite; stills at all six values exist.",
    "Lab 08-pixelate-block (block 1 = original: 0 px differ; 2 to 32 rendered)",
    readouts=[{"at": T("B23", "One is"), "text": "1 to 32", "x": 0.80, "y": 0.45}])
lab("B24", 2, "blocks scale with the sprite", "08-pixelate-block.gdshader", f"{PUB}/pixelate-block-scale.mp4",
    "Godot 4.7.2 · Forward+ · nearest filter · sprite scale tweened by script", [],
    "A real Godot window: the pixelated sprite (block 8) grows from its own size to more than twice as large; the blocks grow with it and "
    "there are always sixteen across. One readout, '16 across', stays on screen the whole time.",
    "The sprite swells and its blocks swell with it, but the count stays sixteen.",
    [{"at": T("B24", "Draw it bigger"), "event": "scale tween begins; blocks grow"}, {"at": T("B24", "still sixteen"), "event": "readout '16 blocks across' stays"},
     {"at": T("B24", "This pixelates"), "event": "settled at the larger size"}],
    "manim drawing of growing blocks", "Blocks growing with the sprite while the count holds is the whole claim, and it is a real render.",
    "C12: custom scene (script): Sprite2D with lab-shaders/08-pixelate-block.gdshader, block = 8; the node's scale tweens 1.0 to 2.25 over 5 s, 30 fps, Forward+, "
    "nearest filter, scripted. Verified: blocks are 8 screen pixels at scale 1.0 and 18 at 2.25 (runs of 54, 180, 54 pixels along the middle row).",
    "Lab 08-pixelate-block at scale 1.0 (8 px) and 2.25 (18 px blocks)", layout="video",
    readouts=[{"at": T("B24", "still sixteen"), "text": "16 across", "x": 0.80, "y": 0.45}])
manim("B25", 2, "the last block comes up short", "ShortLastBlock",
      "A horizontal strip 128 pixels wide drawn as outline cells grouped in blocks of six (the series pixel grid, shown as a row). Twenty-one full "
      "blocks fill the strip from the left; at the right end a narrow block of two pixels, wearing a terracotta ring and the label '2 px'. A running "
      "sum under the strip: '21 × 6 + 2 = 128'.",
      "The blocks fill the strip and the last one lands short inside its ring.",
      [{"at": T("B25", "One catch"), "event": "strip of 128 pixels; the first block of six outlined, label 'block = 6'"}, {"at": T("B25", "Blocks of six"), "event": "twenty-one blocks of six fill the strip"},
       {"at": T("B25", "then one of two"), "event": "last block of two pixels, ring, label 2 px; sum 21 × 6 + 2 = 128"}],
      "ShaderLab on the gradient render", "A row of blocks with a short one at the end is the picture of 'does not divide'; the real gradient would "
      "add a dark corner for no gain.",
      "analysis (gradient run): block = 6 gives 21 blocks of 6 and one of 2 (sum 128)")

# ═════════════════════════════ ACT IV · Checkerboards and Stripes ═════════════════════════════
manim("B26", 3, "column plus row", "SumsGrid",
      "Act title 'Checkerboards and Stripes' (serif 40) top-left. A four by four grid of outline cells (no fill behind text) with the sum of "
      "column and row written in each cell: 0 1 2 3 / 1 2 3 4 / 2 3 4 5 / 3 4 5 6; column numbers along the top, row numbers down the left. A terracotta "
      "dot steps one cell right (the number pops from 2 to 3 with '+1') then one cell down (+1 again).",
      "The dot steps right and down and the number in its cell goes up by one each time.",
      [{"at": 0.04, "event": "act title; the grid with its sums"}, {"at": T("B26", "One cell to the right"), "event": "dot steps right: +1"},
       {"at": T("B26", "One cell down"), "event": "dot steps down: +1"}],
      "ShaderLab render of the finished checkerboard", "Numbers in cells that change by one per step are best shown in a grid with a dot moving through it.")
manim("B27", 3, "the remainder after two picks the color", "RemainderColors",
      "The same grid of sums. Under each sum a small remainder after two appears, 0 or 1. Beside the grid a second, text-free four by four checkerboard "
      "fills cell by cell in teal and cream as each remainder is found (teal for 0, cream for 1). The label 'mod(x, y): the remainder after dividing' "
      "and the line '3 mod 2 = 1' sit below.",
      "Each sum gets its remainder and the second grid fills with the checkerboard cell by cell.",
      [{"at": T("B27", "Take the remainder"), "event": "remainders 0 and 1 appear under the sums; label mod"},
       {"at": T("B27", "An even sum"), "event": "the plain checkerboard fills row by row beside the grid (finished by 44 %)"},
       {"at": T("B27", "Three mod two"), "event": "line '3 mod 2 = 1' with the 3 in the grid ringed"}],
      "LectureEvidenceTable", "The checkerboard has to appear from the numbers; a table lists them but cannot fill the pattern.",
      "Lab: mod(3, 2) = 1, mod(4, 2) = 0, mod(5, 2) = 1 (chk-mod-values); checkerboard matches the formula in 64 of 64 cells")
manim("B28", 3, "a diagonal step changes the sum by two", "DiagonalStep",
      "The same grid, now showing the checkerboard colors as outlines (teal and cream rings, no fill behind numbers). A terracotta dot jumps from cell (0, 0) "
      "to cell (1, 1) with the label '+2' on the jump; two flip marks (one per step of one) appear on the way, the two cells carry the same color and a small "
      "bracket joins them. A corner point where four cells meet is marked with a small terracotta dot and the label 'corners touch'.",
      "The dot jumps diagonally and lands on a cell of its own color; the bracket joins the pair.",
      [{"at": T("B28", "Move diagonally"), "event": "dot jumps from (0, 0) to (1, 1): +2"}, {"at": T("B28", "The color flips"), "event": "two flips marked on the two steps; the pair bracketed"},
       {"at": T("B28", "That is why"), "event": "a corner where four cells meet marked 'corners touch'"}],
      "ShaderLab render of the finished checkerboard", "A jump landing on its own color is the argument; it needs the grid and a dot, not pixels.",
      "Lab: diagonal neighbours share a color and edge neighbours differ at every cell of the render (verify-patterns.py)")
lab("B29", 3, "the checkerboard shader", "09-checker.gdshader", f"{PUB}/checker.png", f"{FWD} · the shader on the left",
    [{"at": T("B29", "In the shader"), "lines": [ln("09-checker.gdshader", "floor(UV")]},
     {"at": T("B29", "add them"), "lines": [ln("09-checker.gdshader", "mod(")], "label": "mod(x, y): the remainder of x divided by y"},
     {"at": T("B29", "let that mix"), "lines": [ln("09-checker.gdshader", "COLOR")], "label": "mix(a, b, t): zero gives a, one gives b"}],
    "Code card at left (cell, parity with mod, two colors, the mix); at right a real Godot window: an eight by eight teal-and-cream checkerboard. "
    "The mod and COLOR lines carry short labels: mod(x, y): the remainder of x divided by y; mix(a, b, t): zero gives a, one gives b.",
    "The cell line, the mod line and the mix line are highlighted in turn while the checkerboard sits in the window.",
    [{"at": T("B29", "In the shader"), "event": "cell line highlighted"}, {"at": T("B29", "add them"), "event": "mod line highlighted"},
     {"at": T("B29", "let that mix"), "event": "COLOR line highlighted; caption on mix"}, {"at": T("B29", "Use mod"), "event": "readout 'percent: error on decimals'"}],
    "LectureCodeTrace alone", "Four lines and their result together are the claim; the pattern is the proof the arithmetic worked.",
    "C13: Lab sprite, white texture, lab-shaders/09-checker.gdshader, still PNG. Verified: all 64 cells match mod(column + row, 2); top-left cell teal; "
    "probes (0,0) teal, (1,0) cream, (0,1) cream, (1,1) teal. Lab: percent on decimals is a shader error (chk-percent-on-floats).",
    "Lab 09-checker (64 of 64 cells match)",
    readouts=[{"at": T("B29", "Use mod"), "text": "percent: error", "x": 0.80, "y": 0.45}])
manim("B30", 3, "x plus y is a diagonal ramp", "DiagonalRamp",
      "A square (the shape) shaded with a diagonal gradient in mid-tone greys, with five grey isolines running along the other diagonal at "
      "x + y = 0.5, 1, 1.5 ... and a ramp strip below labelled 0 and 2 with the word 'ramp'. A terracotta dot slides along the main diagonal with a live label 'UV.x + UV.y = ...' "
      "counting from 0 up to 2.",
      "The dot slides corner to corner and the sum counts from zero to two.",
      [{"at": T("B30", "Stripes need"), "event": "square with the diagonal gradient and isolines"}, {"at": T("B30", "Add the two"), "event": "dot slides to the middle of the diagonal; label counts to 1.0 (finished by 44 %)"},
       {"at": T("B30", "from zero in one corner"), "event": "dot slides on to the far corner; ramp strip labelled 0 and 2"}],
      "ShaderLab render of the finished stripes", "A ramp that runs corner to corner is a coordinate picture, and the isolines show where stripes will run.",
      "Docs: UV runs 0 to 1; Lab: the stripe render follows lines of constant x + y (verify-patterns.py)")
manim("B31", 3, "fract of the ramp, cut with step, is a stripe", "SawtoothCut",
      "A plot over the diagonal 0 to 2: the sawtooth of fract(ramp × 4) with eight teeth, drawing left to right. A horizontal threshold line at 0.5 "
      "labelled 'width'. Under the plot a one-dimensional bar fills in gold where a tooth is below the threshold and cream above it. Then the threshold "
      "moves to 0.25 and back to 0.75 and the gold parts thin and thicken. The label 'step(edge, x): 0 below the edge, 1 from the edge' sits above, and the word 'sawtooth' labels the curve.",
      "The sawtooth draws, the threshold cuts every tooth, and the stripe bar below fills; moving the threshold changes the stripe widths.",
      [{"at": T("B31", "Multiply the ramp"), "event": "sawtooth of eight teeth draws"}, {"at": T("B31", "Cut each tooth"), "event": "threshold line and step label; stripe bar fills"},
       {"at": T("B31", "and every tooth"), "event": "threshold moves 0.25, 0.75; the gold parts thin and thicken"}],
      "LectureCodeTrace", "The sawtooth cut by a line into a bar of stripes is a plot with a threshold: a function reshaping a ramp, which is what the "
      "kit's plot object is for.",
      "Docs: step returns b < a ? 0.0 : 1.0; Lab: gold share = width (0.500, 0.253, 0.753 for widths 0.5, 0.25, 0.75)")
lab("B32", 3, "the stripes shader", "10-stripes.gdshader", f"{PUB}/stripes.png", f"{FWD} · the shader on the left",
    [{"at": T("B32", "Run it"), "lines": [ln("10-stripes.gdshader", "fract(")]}, {"at": T("B32", "Width is"), "lines": [ln("10-stripes.gdshader", "step(")], "label": "step(edge, x): 0 below the edge, 1 from it"}],
    "Code card at left (count and width uniforms, the diagonal, fract, step, the mix of gold and cream); at right a real Godot window: gold-and-cream "
    "diagonal stripes, four pairs across. Two readouts 'count 4' and 'width 0.5'.",
    "The fract line, then the step line, are highlighted while four gold stripes run across the square.",
    [{"at": T("B32", "Count is"), "event": "fract line highlighted; readout count 4"}, {"at": T("B32", "Width is"), "event": "step line highlighted; readout width 0.5"}],
    "manim strip of stripes", "The stripes and the two numbers that set them, together, in a real render.",
    "C14: Lab sprite, white texture, lab-shaders/10-stripes.gdshader, count 4, width 0.5, still PNG. Verified: four gold stripes end along the top row; "
    "gold share 0.500 (0.253 at width 0.25, 0.753 at 0.75); edges follow lines of constant x + y.",
    "Lab 10-stripes (gold share = width; four pairs across)",
    readouts=[{"at": T("B32", "Count is"), "text": "count 4", "x": 0.80, "y": 0.35}, {"at": T("B32", "Width is"), "text": "width 0.5", "x": 0.80, "y": 0.55}])
lab("B33", 3, "moving stripes with TIME", "11-stripes-moving.gdshader", f"{PUB}/stripes-moving.mp4", f"{FWD} · live TIME",
    [{"at": T("B33", "To make them move"), "lines": [ln("11-stripes-moving.gdshader", "TIME")], "label": "TIME: seconds on one clock for the game"}],
    "Code card at left with the TIME line highlighted; at right a real Godot window: the same gold-and-cream stripes sliding toward the bottom right. "
    "The highlighted line carries the label 'TIME: seconds on one clock for the game'.",
    "The stripes slide steadily toward the bottom right the whole time.",
    [{"at": T("B33", "To make them move"), "event": "TIME line highlighted; stripes begin to slide"}, {"at": T("B33", "Time is one clock"), "event": "label on TIME stays"},
     {"at": T("B33", "The pattern slides"), "event": "stripes keep sliding toward the bottom right"}],
    "manim animation of sliding stripes", "Sliding stripes are a motion claim; a still could not show it.",
    "C15: Lab sprite, white texture, lab-shaders/11-stripes-moving.gdshader, defaults, 8 s live TIME, 30 fps, Forward+, nearest filter. Verified: the "
    "render equals the formula for the engine's TIME (0.00 % pixels differ in three of four renders; one fit less well, 1.1 %, kept), and the pattern "
    "moves toward larger x + y as TIME grows. fract(-0.25) = 0.75 (chk-negative-fract-mod).",
    "Lab 11-stripes-moving (four renders fit the formula; direction + fract of negatives)")
rem("B34", 3, "one recipe for both patterns", "LectureEvidenceTable",
    {"title": "One recipe, two patterns", "headers": ["Step", "Checkerboard", "Stripes"],
     "rows": [["one number per pixel", "column + row", "UV.x + UV.y"], ["make it repeat", "mod 2", "fract"], ["cut into two colors", "mix", "step, then mix"]],
     "note": "Godot 4.7 shader reference · both patterns checked in Godot 4.7.2", "cues": [T("B34", "Make one number"), 0.58, T("B34", "Cut it")],
     "durationSeconds": "__AUDIO__"},
    "A three-row table with a row per step and a column per pattern; the row for each step is ringed as the voice names it.",
    "The ring steps down the three steps with the voice.",
    [{"at": T("B34", "Make one number"), "event": "row one"}, {"at": 0.58, "event": "row two"}, {"at": T("B34", "Cut it"), "event": "row three"}],
    "manim table drawn on cue", "Two parallel recipes in three steps is a table; both patterns were just shown moving.",
    "FACTCHECK.md rows 41 to 50")

# ═════════════════════════════ ACT V · Dots, and Both Numbers at Once ═════════════════════════════
manim("B35", 4, "the cell's own space, centered", "CellSpace",
      "Act title 'Dots, and Both Numbers at Once' (serif 40) top-left. One cell drawn large as a unit square. Its corner labels read 0 and 1; they change to "
      "-0.5 and +0.5 with a small terracotta origin mark appearing in the middle as the voice says subtract one half. A terracotta dot moves around inside "
      "with a live label giving its two numbers.",
      "The labels shift from 0 to 1 over to minus a half to plus a half and the origin moves to the middle of the cell.",
      [{"at": 0.04, "event": "act title; the unit cell with corner labels 0 and 1"}, {"at": 0.12, "event": "the dot visits three spots inside the cell with its two numbers and holds at (0.3, 0.7) (finished by 44 %)"},
       {"at": T("B35", "Subtract one half"), "event": "labels become -0.5 and +0.5; origin mark in the middle"}],
      "ShaderLab render of one dot in a cell", "A coordinate system being re-centered is exactly the kit's uv-square object in motion.")
manim("B36", 4, "length, radius and step make a circle", "LengthAndRadius",
      "The same cell, centered. A terracotta dot with a line to the middle labelled 'length'. A grey circle of radius r around the middle. As the dot moves "
      "across the circle's edge the label flips between 'inside: step gives 0' and 'outside: step gives 1'. The label 'length: the distance from the middle' is "
      "drawn above.",
      "The dot crosses the circle's edge and the label flips from step gives 0 to step gives 1.",
      [{"at": T("B36", "Length of that"), "event": "dot with a line to the middle; label length"}, {"at": T("B36", "Compare it"), "event": "circle of radius r appears"},
       {"at": T("B36", "Step gives"), "event": "dot crosses the edge; the label flips"}],
      "ShaderLab render of the dot grid", "A distance compared with a radius is a geometric fact, and the flip at the edge is the motion.",
      "Docs: length returns the vector length; step returns b < a ? 0.0 : 1.0")
lab("B37", 4, "the dots shader", "12-dots.gdshader", f"{PUB}/dots.png", f"{FWD} · the shader on the left",
    [{"at": T("B37", "In code"), "lines": [ln("12-dots.gdshader", "fract(UV")]}, {"at": T("B37", "Length of that"), "lines": [ln("12-dots.gdshader", "length(")], "label": "length: distance from the middle"},
     {"at": T("B37", "Step against"), "lines": [ln("12-dots.gdshader", "step("), ln("12-dots.gdshader", "COLOR")]}],
    "Code card at left (cells and radius uniforms, fract minus a half, length, the step-and-mix line); at right a real Godot window: an eight by eight "
    "grid of teal dots on cream.",
    "The fract line, the length line and the color line are highlighted in turn while the dot grid sits in the window.",
    [{"at": T("B37", "In code"), "event": "fract line highlighted"}, {"at": T("B37", "Length of that"), "event": "length line highlighted"},
     {"at": T("B37", "Step against"), "event": "COLOR line highlighted"}],
    "LectureCodeTrace alone", "Three lines and the dot grid they make, together.",
    "C16: Lab sprite, white texture, lab-shaders/12-dots.gdshader, cells 8, radius 0.35, still PNG. Verified: dots cover 38.4 % of the picture (geometry: 38.5 %).",
    "Lab 12-dots (coverage 38.4 % at radius 0.35)")
lab("B38", 4, "dots grow until they touch, then fill", "12-dots.gdshader", f"{PUB}/dots-radius.mp4", f"{FWD} · radius swept by script",
    [{"at": T("B38", "Grow the radius"), "lines": [ln("12-dots.gdshader", "uniform float radius")]}],
    "Code card at left with the radius uniform highlighted; at right a real Godot window: the dot grid with the radius sweeping from small to large, "
    "the dots swelling until they touch and finally fill their cells. Readouts: 'touch: 0.5' and 'full: 0.71'.",
    "The dots swell, touch, and then fill the whole picture.",
    [{"at": T("B38", "Grow the radius"), "event": "radius uniform highlighted; dots begin to swell"}, {"at": T("B38", "At one half"), "event": "dots touch; readout touch 0.5"},
     {"at": T("B38", "By seven tenths"), "event": "cells filled; readout full 0.71"}],
    "manim plot of covered area", "Swelling dots that touch and then fill is the claim, and the corner gap closing at 0.71 is visible only in the real render.",
    "C17: Lab sprite, white texture, lab-shaders/12-dots.gdshader, cells 8; radius swept linearly 0.05 to 0.75 over 8 s (--animate radius:0.05:0.75), 30 fps, "
    "Forward+, nearest filter, scripted. Verified: coverage 12.4 / 38.4 / 78.9 / 95.1 / 100 / 100 % at radius 0.2 / 0.35 / 0.5 / 0.6 / 0.7 / 0.72 "
    "(geometry: 12.6 / 38.5 / 78.5 / 95.1 / 100 / 100); half the diagonal is 0.7071.",
    "Lab 12-dots at six radii (coverage matches geometry)",
    readouts=[{"at": T("B38", "At one half"), "text": "touch: 0.5", "x": 0.80, "y": 0.35}, {"at": T("B38", "By seven tenths"), "text": "full: 0.71", "x": 0.80, "y": 0.55}])
lab("B39", 4, "the trap: dots on a wide rectangle are ovals", "12-dots.gdshader", f"{PUB}/dots-wide.mp4", "Godot 4.7.2 · Forward+ · rectangle widened by script",
    [{"at": T("B39", "The address runs"), "lines": [ln("12-dots.gdshader", "fract(UV")]}],
    "Code card at left (the same dots shader, eight cells each way); at right a real Godot window: a square of round dots whose rectangle widens from square to sixteen "
    "by nine, the dots stretching into ovals. Readouts: 'round' at the start, '1.8 × wider than tall' at the end.",
    "The rectangle widens and the round dots stretch sideways into ovals.",
    [{"at": 0.0, "event": "square: round dots; readout round"}, {"at": T("B39", "On a wide rectangle"), "event": "rectangle widens; dots stretch"},
     {"at": T("B39", "These dots"), "event": "settled at 16:9; readout 1.8 × wider than tall"}],
    "manim drawing of a stretched circle", "The trap is that the shape stretches the cells; a real rectangle widening with its dots is the evidence.",
    "C18: custom scene (script): a ColorRect with lab-shaders/12-dots.gdshader, cells = 8 (its default), height 360, width tweening 360 to 640 over 4 s, 30 fps, "
    "Forward+, scripted. Verified at the end state (640x360): each dot is 56 by 31 pixels (ratio 1.81 on whole pixels; the cells are 80 by 45, ratio 1.78); at the "
    "start (360x360) the dots are round.",
    "Lab 12-dots on 640x360 (dot 56 x 31 px; ratio 1.81); square start round", layout="video",
    readouts=[{"at": 0.04, "text": "round", "x": 0.50, "y": 0.05}, {"at": T("B39", "These dots"), "text": "1.8 × wider", "x": 0.80, "y": 0.55}])
lab("B40", 4, "the fix: a count for each direction", "13-dots-square.gdshader", f"{PUB}/dots-fixed.mp4", "Godot 4.7.2 · Forward+ · shader switched · scripted",
    [{"at": T("B40", "The fix"), "lines": [ln("13-dots-square.gdshader", "uniform vec2 cells")], "label": "vec2: a count for each direction"}],
    "Code card at left (cells is now a vec2, sixteen by nine); at right a real Godot window on the sixteen by nine rectangle: the eight-by-eight oval dots "
    "switch to a sixteen-by-nine grid of round dots. Readout '16 by 9' and 'round again'.",
    "The ovals snap into round dots at the switch.",
    [{"at": 0.0, "event": "oval dots from the previous beat"}, {"at": T("B40", "Sixteen across"), "event": "shader switches; dots become round"},
     {"at": T("B40", "Every dot"), "event": "readout round again"}],
    "manim before-and-after drawing", "A before and after on the same rectangle: the oval-to-round switch is the claim.",
    f"C19: custom scene (script): the 640x360 ColorRect of C18 with lab-shaders/12-dots.gdshader (cells 8, its default) until the voice says 'Sixteen across' (about {T('B40', 'Sixteen across') * 100:.0f} % of the beat, "
    "set from the audio), then lab-shaders/13-dots-square.gdshader (cells 16, 9) assigned; about 11 s, 30 fps, Forward+, scripted. Verified: after the switch each dot is 28 by 28 pixels, ratio 1.00 (cells 40 by 40).",
    "Lab 13-dots-square on 640x360 (dot 28 x 28 px; ratio 1.00)", readouts=[{"at": T("B40", "Sixteen across"), "text": "16 by 9", "x": 0.80, "y": 0.35},
                                                                          {"at": T("B40", "Every dot"), "text": "round again", "x": 0.80, "y": 0.55}])
lab("B41", 4, "the dot screen: floor picks the cell, fract draws the dot", "14-halftone.gdshader", f"{PUB}/halftone.png", f"{FWD} · 24 cells",
    [{"at": T("B41", "Floor picks"), "lines": [ln("14-halftone.gdshader", "floor(p)")]}, {"at": T("B41", "Fract draws"), "lines": [ln("14-halftone.gdshader", "length(fract")]},
     {"at": T("B41", "and the dot takes"), "lines": [ln("14-halftone.gdshader", "COLOR")]}],
    "Code card at left (cells and radius with ranges, the stretched address, the middle of the cell, the picture read there, the distance, the color); at right "
    "a real Godot window: the teal test sprite drawn as a screen of round dots, with its two cream eyes as two cream dots.",
    "The middle-lookup line, the distance line and the color line are highlighted in turn over the dot screen.",
    [{"at": T("B41", "Floor picks"), "event": "middle line and picture line highlighted"}, {"at": T("B41", "Fract draws"), "event": "distance line highlighted"},
     {"at": T("B41", "and the dot takes"), "event": "COLOR line highlighted"}],
    "LectureCodeTrace alone", "The dot screen is the film's two numbers working together in one real render.",
    "C20: Lab sprite (fit scale), lab-shaders/14-halftone.gdshader, cells 24, radius 0.4, still PNG. Verified: on the gradient picture at 16 cells every dot, "
    "including the four corners, is the same size (6 by 6, 32 pixels) and its color equals the picture at the cell's middle in 256 of 256 cells.",
    "Lab 14-halftone (corner dots whole; 256 of 256 colors match the picture)")
lab("B42", 4, "the same trap in dots: rounding cuts the edge dots", "15-halftone-rounded.gdshader", f"{PUB}/halftone-rounded-switch.mp4",
    "Godot 4.7.2 · Forward+ · nearest filter · shader switched · scripted",
    [{"at": T("B42", "Round the cell number"), "lines": [ln("15-halftone-rounded.gdshader", "floor(p + 0.5)"), ln("15-halftone-rounded.gdshader", "fract(p + 0.5)")]},
     {"at": T("B42", "Floor it"), "lines": [ln("15-halftone-rounded.gdshader", "floor(p + 0.5)"), ln("15-halftone-rounded.gdshader", "fract(p + 0.5)")]}],
    "Code card at left: the rounded variant of the dot screen, the half added inside the floor and inside the fract (those two lines highlighted); at right a "
    "real Godot window: an eight by eight dot screen of the teal-and-cream checker picture, drawn first with the rounded variant (the dots along the four "
    "edges cut in half, the corners cut to quarters, a terracotta ring on one edge) and then, when the voice says 'Floor it', with the floored dot screen: "
    "all sixty-four dots whole. Readouts: 'cut in half', then 'whole'.",
    "The edge dots are cut in half, then the shader switches and every edge dot becomes whole.",
    [{"at": 0.02, "event": "rounded dot screen: edge dots cut in half; ring on one edge"}, {"at": T("B42", "Round the cell number"), "event": "both half-lines highlighted; readout cut in half"},
     {"at": T("B42", "Floor it"), "event": "shader switches to the floored version; all sixty-four dots whole; readout whole"}],
    "manim drawing of half dots", "A before and after on the same picture: the cut dots made whole by moving the half is the claim, and the real render is the proof.",
    "C21: custom scene (script): Lab sprite (checker texture, fit scale), cells = 8; lab-shaders/15-halftone-rounded.gdshader until the voice says 'Floor it' "
    "(about " + f"{T('B42', 'Floor it') * 100:.0f}" + " % of the beat, set from the audio), then lab-shaders/14-halftone.gdshader assigned; about 13 s, 30 fps, Forward+, nearest filter, scripted. "
    "Verified (scale 1.0, 128 px picture): the rounded version has 81 separate shapes, 32 of them cut by the picture's edge (areas 31 and 62 against 124); the "
    "floored version has 64 whole dots of 124 pixels each.",
    "Lab 14-halftone and 15-halftone-rounded on the checker picture (64 whole dots against 81 separate shapes, 32 cut)",
    readouts=[{"at": T("B42", "Round the cell number"), "text": "cut in half", "x": 0.16, "y": 0.45}, {"at": T("B42", "Floor it") + 0.03, "text": "whole", "x": 0.16, "y": 0.45}],
    rings=[{"at": 0.02, "box": [0.26, 0.10, 0.40, 0.90]}])
lab("B43", 4, "cells swept: chunky dots to the picture", "14-halftone.gdshader", f"{PUB}/halftone-sweep.mp4", f"{FWD} · cells 8 to 48 · scripted sweep",
    [{"at": T("B43", "One shader"), "lines": [ln("14-halftone.gdshader", "uniform float cells")]}],
    "Code card at left with the cells uniform highlighted; at right a real Godot window: the dot-screen sprite with the cell count sweeping from 8 up to 48, "
    "the dots shrinking and the sprite coming back into focus. A readout shows the count.",
    "The dots shrink and multiply and the picture comes back.",
    [{"at": 0.02, "event": "cells = 8: a few chunky dots"}, {"at": T("B43", "More cells"), "event": "the sweep passes 24 and the picture returns"},
     {"at": T("B43", "One shader"), "event": "cells uniform highlighted; sweep ends at 48"}],
    "ShaderLab: stills at four cell counts", "One number turning chunky into fine is a motion claim.",
    "C22: Lab sprite (fit scale), lab-shaders/14-halftone.gdshader; cells swept linearly 8 to 48 over 8 s (--animate cells:8:48), 30 fps, Forward+, nearest filter, "
    "scripted. Verified: stills at 8, 16, 24, 48 cells exist (14-halftone-c8 to c48-sprite-fit).",
    "Lab 14-halftone at 8, 16, 24, 48 cells", readouts=[{"at": 0.06, "text": "8 to 48", "x": 0.80, "y": 0.45}])

# ═════════════════════════════ write lanes + SHOTLIST ═════════════════════════════
(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(len(N.ACTS)):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

got = [e["bid"] for e in E]
want = [bid for bid, _, _ in N.BODY]
assert got == want, f"lane order differs from BODY: {set(want) ^ set(got)}"
lanes_hist = {}
for e in E:
    lanes_hist[e["entry"]["lane"]] = lanes_hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
sl = [f"# Shot list: {N.TITLE}\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. "
      "Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. "
      "A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab or scene-script capture of a tested file in `lab-shaders/`; no editor frames are needed. "
      "Each `show` time is when a motion starts; the build must finish it before 45 % of the beat or start it after 55 % (the midpoint frame is a settled still), "
      "and the `visual_intent` of each Manim beat ends with the state that midpoint frame must show. "
      "Four things must exist before the build (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`; props used here: `layout` video and side, `code`, `cues`, "
      "`readouts`, `rings`, `ramp`, `caption`, `title`). "
      "2. **`shader_kit.py`** Manim helpers (same file): this film uses `ramp_strip`, `pixel_grid`, `plot`, and `code_card`; it also needs three small "
      "objects that the spec does not list, each a few lines on top of those: a numbered `cell_grid` (outline cells with a number in each), a `block_row` "
      "(a strip of blocks of given widths with rings and labels), and `lookup_lines` (curved lines from pixel dots to one point). "
      "3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` (same file) with these options: `--animate` (linear sweep), a stepped sweep "
      "(values held for a time each), `--material-at SECONDS`, and four small scene scripts (C12 sprite scale tween, C18 rectangle widening, C19 and C21 shader swaps). "
      "4. **Docs screenshot D1** for B21 via Playwright. There are no editor frames in this film.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
