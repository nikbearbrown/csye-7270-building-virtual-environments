#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text, the cue line numbers must point at the right lines, and the shot
list must say exactly what the lanes say. Re-run after any edit:
    python3 _gen_lanes.py && python3 make_sheet.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
E = []          # entries in beat order
PUB = "godot-textures-and-color"      # folder under runtime/remotion/public/ for this film's captures


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def L(fn, sub):
    """1-based line number of the first line of lab-shaders/<fn> that contains <sub>."""
    for i, line in enumerate((SH / fn).read_text().splitlines(), 1):
        if sub in line:
            return i
    raise KeyError((fn, sub))


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects)", sparse=True):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": sparse}, evidence)


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


EV = "evidence/planning-checks/"

# ═════════════════════════════ ACT I · Reading a Texture ═════════════════════════════
lab("B01", 0, "the finished effect, shown first", "18-dissolve.gdshader", f"{PUB}/dissolve-preview.mp4",
    "Godot 4.7.2 · Forward+ · progress swept by script", [],
    "Act title 'Reading a Texture' (serif 40) top-left. A real Godot render in a framed window on the cream stage: the teal test sprite sits whole, then burns away from the edges in, a yellow-orange-red rim around every hole, while a thin 0 to 1 strip under the window carries a marker labelled 'progress' that rides from 0 to 1 with the burn.",
    "The sprite burns away as the progress marker rides from 0 to 1.",
    [{"at": 0.0, "event": "sprite whole, marker at 0"}, {"at": 0.25, "event": "the first holes open at the darkest clouds"}, {"at": 0.6, "event": "most of the sprite gone"}, {"at": 0.88, "event": "gone, marker at 1"}],
    "manim drawing of a sprite dissolving", "A real render of the finished effect is the honest promise for the next ten minutes; a drawing would only claim it.",
    "C01: Lab sprite (teal test sprite, scale to fit 640x360), lab-shaders/18-dissolve.gdshader; noise_tex = NoiseTexture2D (FastNoiseLite seed 7, frequency 0.02, 256 x 256: the Lab's 'noise' kind); ramp_tex = GradientTexture1D (#8A2A12, #F08A2C, #F7D46B, 256 wide); `--animate progress:0.05:0,0.97:1` (fractions of the beat), 30 fps, Forward+, scripted sweep (label it). Verified frames: evidence/planning-checks/png/plus-a3-18-dissolve-*.png (sprite 23,512 px whole at 0; 0 px at 1).",
    "plus-results a3-18-dissolve-0.0 .. 1.0; plus-analysis.txt", layout="video", title="Reading a Texture",
    ramp={"at": 0.1, "from": 0, "to": 1}, readouts=[{"at": 0.1, "text": "progress", "x": 0.5, "y": 0.97}])
manim("B02", 0, "a texture is a table; an address returns a color", "LookupTable",
      "A 6-by-6 grid of cells: the cream letter F on teal (the film's tiny table), with a one-cell teal margin. Beside it a swatch box with four numbers under it, and under the grid an address readout '(u, v)'. A terracotta dot (the address) starts at the top-left cell, a thin line runs from the dot to the swatch, the swatch takes that cell's color and the four numbers fill in (0.98, 0.98, 0.96, 1.0). Labels: 'texture', 'address', 'color'.",
      "The address dot hops from cell to cell and, each time, the swatch changes to that entry's color.",
      [{"at": 0.12, "event": "the grid and its labels"}, {"at": 0.25, "event": "dot on a cream cell: swatch cream, four numbers"}, {"at": 0.38, "event": "dot on a teal cell: swatch teal (0.37, 0.64, 0.57, 1.0); settles through 60 %"}, {"at": 0.64, "event": "dot on the next cream cell"}, {"at": 0.84, "event": "numbers pulse once"}],
      "ShaderLab with a Lab render", "A grid with a moving address and a swatch that answers is the whole idea of a lookup, as motion; a render would show the result but not the asking.",
      "tiny F table drawn from the same texel colors as the Lab-run F (cream #FAF9F5, teal #5FA391)")
lab("B03", 0, "the lookup in code", "01-lookup.gdshader", f"{PUB}/lookup-checker.png", "Godot 4.7.2 · Forward+ · a ColorRect with no image of its own",
    [{"at": 0.12, "lines": [L("01-lookup.gdshader", "void fragment")], "label": "fragment(): runs once for each pixel the shape covers"},
     {"at": 0.32, "lines": [L("01-lookup.gdshader", "COLOR = ")], "label": "COLOR: the color of the pixel being drawn"},
     {"at": 0.62, "lines": [L("01-lookup.gdshader", "COLOR = ")], "label": "texture(table, address): returns a color"}],
    "Code card at left (the four-line lookup shader); at right a real Godot window: a plain Color Rect that now shows the 8-by-8 teal and cream checker picture. A terracotta ring moves to one cream cell and then one teal cell, each with its address as a readout.",
    "The ring hops to a cell, and its address and color are read out.",
    [{"at": 0.12, "event": "fragment line highlighted with its meaning"}, {"at": 0.32, "event": "COLOR defined on the lookup line"}, {"at": 0.42, "event": "ring on a cream cell, address (0.06, 0.06)"}, {"at": 0.62, "event": "texture(table, address) label"}, {"at": 0.7, "event": "ring on a teal cell, address (0.19, 0.06)"}],
    "LectureCodeTrace alone", "Code and its result side by side is the claim: one line fills the whole shape from a table the shape never owned.",
    "C02: Lab rect 360x360 logical, lab-shaders/01-lookup.gdshader, --tex tex=checker, still PNG at 4K. Verified probes: (0.06, 0.06) = (0.980, 0.977, 0.961) cream; (0.19, 0.06) = (0.372, 0.639, 0.569) teal.",
    "plus-results a1-01-lookup-checker; run-lab-checks 01-lookup",
    rings=[{"at": 0.42, "box": [0.0, 0.0, 0.125, 0.125]}, {"at": 0.7, "box": [0.125, 0.0, 0.25, 0.125]}],
    readouts=[{"at": 0.42, "text": "0.06, 0.06", "x": 0.2, "y": 0.2}, {"at": 0.7, "text": "0.19, 0.06", "x": 0.33, "y": 0.2}])
lab("B04", 0, "the sampler2D slot; any table fits", "01-lookup.gdshader", f"{PUB}/swap-tables.mp4", "Godot 4.7.2 · Forward+ · same shader, three tables, switched by script",
    [{"at": 0.1, "lines": [L("01-lookup.gdshader", "uniform")], "label": "uniform: a value your game sets from outside"},
     {"at": 0.3, "lines": [L("01-lookup.gdshader", "uniform")], "label": "sampler2D: the type of a texture a shader reads"}],
    "Code card at left with the uniform line highlighted. At right the same real Godot window shows three tables in turn with no change to the code: the small cream F on teal (smeared, because it is tiny), the red-green gradient, the grey noise. A caption under the window says 'same code'.",
    "The window's picture changes from table to table while the code stays put.",
    [{"at": 0.1, "event": "uniform line: set from outside"}, {"at": 0.3, "event": "sampler2D: a texture slot"}, {"at": 0.35, "event": "gradient replaces the F"}, {"at": 0.68, "event": "noise replaces the gradient"}],
    "manim: a slot with three tables plugging in", "Three real renders of one unchanged shader are the proof that the table is the variable; the drawing would only say so.",
    "C03: three Lab stills of lab-shaders/01-lookup.gdshader on a 360x360 rect, joined with ffmpeg, one third of the clip each: tex = tiny_f (the 6x6 F, default filter: smeared), gradient, noise (Lab kinds). Verified: F centre probes (0.25, 0.25) cream, (0.0833, 0.0833) teal; the F at (0.15, 0.25) blends to (0.608, 0.769, 0.722).",
    "plus-results a1-01-lookup-f-linear, -gradient, -noise",
    readouts=[{"at": 0.2, "text": "same code", "x": 0.5, "y": 0.95}])
lab("B05", 0, "filter: between two entries", "02-nearest.gdshader", f"{PUB}/filter-compare.mp4", "Godot 4.7.2 · Forward+ · two renders of the same table",
    [{"at": 0.12, "lines": [L("02-nearest.gdshader", "uniform")], "label": "filter_nearest: a hint; reads the closest entry only"}],
    "Code card at left with the hint highlighted. At right two real panels of the small F table side by side: on the left the smeared default, on the right the crisp blocks after the hint. Panel labels 'default' and 'filter_nearest'.",
    "The right panel snaps from smeared to crisp blocks next to the unchanged left one.",
    [{"at": 0.12, "event": "hint highlighted"}, {"at": 0.2, "event": "left panel labelled default (smeared)"}, {"at": 0.4, "event": "right panel appears: crisp blocks, labelled filter_nearest"}],
    "ShaderLab with one panel and a toggle", "A smeared F beside a crisp F is the whole difference; the voice points at the left, then the right.",
    "C04: two Lab renders of the 6x6 F table on 360x360 rects, side by side (ffmpeg hstack): left lab-shaders/01-lookup.gdshader, right lab-shaders/02-nearest.gdshader; right panel revealed at 40 % of the beat. Verified at (0.15, 0.25): linear (0.608, 0.769, 0.722) blend, nearest (0.372, 0.639, 0.569) the closest entry.",
    "plus-results a1-01-lookup-f-linear, a1-02-nearest-f",
    readouts=[{"at": 0.2, "text": "default", "x": 0.25, "y": 0.95}, {"at": 0.4, "text": "filter_nearest", "x": 0.75, "y": 0.95}])
lab("B06", 0, "any address: flip the picture", "03-flip.gdshader", f"{PUB}/flip-compare.mp4", "Godot 4.7.2 · Forward+ · same table, new address",
    [{"at": 0.15, "lines": [L("03-flip.gdshader", "vec2 address")], "label": "one minus u: flips it"}, {"at": 0.35, "lines": [L("03-flip.gdshader", "COLOR = ")]}],
    "Code card at left with the address line highlighted. At right two real panels: the F table as it is, then, beside it, the same table flipped left to right (the F's stem moves from left to right). Labels 'same table' and 'new address'.",
    "The F's stem jumps from the left side to the right side as the new address is applied.",
    [{"at": 0.15, "event": "address line highlighted"}, {"at": 0.2, "event": "left panel labelled same table"}, {"at": 0.4, "event": "right panel appears: the F flipped, labelled new address"}],
    "manim: a flipped grid", "A real flipped F next to the original is the evidence that the lookup, not the table, changed.",
    "C05: two Lab renders of the F table (filter_nearest) on 360x360 rects, hstack: left lab-shaders/02-nearest.gdshader, right lab-shaders/03-flip.gdshader; right panel revealed at 40 %. Verified: stem texel (0.25, 0.4167) cream in the original and teal when flipped; (0.75, 0.4167) teal in the original and cream when flipped.",
    "plus-results a1-02-nearest-f, a1-03-flip-f",
    readouts=[{"at": 0.2, "text": "same table", "x": 0.25, "y": 0.95}, {"at": 0.42, "text": "new address", "x": 0.75, "y": 0.95}])
lab("B07", 0, "off the end of the table: repeat", "05-repeat-on.gdshader", f"{PUB}/repeat-compare.mp4", "Godot 4.7.2 · Forward+ · two renders, UV times two",
    [{"at": 0.12, "lines": [L("05-repeat-on.gdshader", "COLOR = ")], "label": "UV * 2: past the end"}, {"at": 0.4, "lines": [L("05-repeat-on.gdshader", "uniform")], "label": "repeat_enable: a hint; the table starts over"}],
    "Code card at left (repeat enable). At right two real panels of the F table asked for twice the address: on the left with repeat disabled a half-size F in the top-left corner with the edge entries smeared out to the right and downward; on the right with repeat enabled a two-by-two tiling of F. Labels 'repeat_disable' and 'repeat_enable'.",
    "The left panel streaks outward; the right panel tiles.",
    [{"at": 0.12, "event": "UV * 2 line highlighted"}, {"at": 0.3, "event": "left panel appears, labelled repeat_disable: edges stretched"}, {"at": 0.7, "event": "right panel appears, labelled repeat_enable: four tiles"}],
    "manim: a table with an arrow running off its edge", "Streaks beside tiles show both settings at once; a diagram would need to explain what the render simply shows.",
    "C06: two Lab renders of the F table on 360x360 rects, hstack: left lab-shaders/04-repeat-off.gdshader (revealed at 25 %), right lab-shaders/05-repeat-on.gdshader (revealed at 65 %). Verified probes (0.625, 0.2083) and (0.125, 0.625): repeat off = teal, teal; repeat on = cream, cream.",
    "run-12-plus-extras 'repeat'; plus-results a1-04/05",
    readouts=[{"at": 0.3, "text": "repeat_disable", "x": 0.25, "y": 0.95}, {"at": 0.7, "text": "repeat_enable", "x": 0.75, "y": 0.95}])

# ═════════════════════════════ ACT II · Color Is Math ═════════════════════════════
manim("B08", 1, "a color is four numbers", "FourNumbers",
      "Act title 'Color Is Math' (serif 40) top-left. A large orange swatch (1.0, 0.5, 0.0, 1.0) with four labelled bars beside it, R G B A, each an outline track with a terracotta dot at its value. A label 'vec4: a bundle of four numbers'. The G bar slides up to 0.9 and the swatch turns yellow-orange; the B bar slides to 0.4 and it pales.",
      "Sliding one bar changes the swatch: the color is nothing but the four numbers.",
      [{"at": 0.12, "event": "swatch, four bars, vec4 label"}, {"at": 0.3, "event": "orange: 1, 0.5, 0, 1"}, {"at": 0.38, "event": "G bar slides to 0.9: swatch yellow-orange; settles through 60 %"}, {"at": 0.64, "event": "B bar slides to 0.4: swatch pales"}, {"at": 0.85, "event": "hold"}],
      "ShaderLab", "Only a picture of numbers moving a swatch shows that the swatch IS the numbers; a render has no numbers to point at.")
lab("B09", 1, "COLOR starts as TEXTURE times modulate", "07-own-texture.gdshader", f"{PUB}/modulate-compare.mp4", "Godot 4.7.2 · Forward+ · node modulate 50 % gray · two renders",
    [{"at": 0.1, "lines": [L("07-own-texture.gdshader", "COLOR = ")], "label": "TEXTURE: the node's own picture"},
     {"at": 0.62, "lines": [L("07-own-texture.gdshader", "COLOR = ")], "label": "a plain lookup: the modulate is gone"}],
    "Code card at left (COLOR = texture(TEXTURE, UV)). At right two real panels of the four-patch picture on a sprite whose modulate is 50 % gray: on the left an empty fragment (the picture is darker), on the right the plain lookup (the picture is full bright). Labels 'empty: keeps modulate' and 'plain lookup: drops it'.",
    "The right panel jumps to full brightness as the plain lookup throws the modulate away.",
    [{"at": 0.1, "event": "TEXTURE line highlighted"}, {"at": 0.25, "event": "left panel: dark (picture times modulate)"}, {"at": 0.62, "event": "right panel appears: full bright"}],
    "manim: COLOR box with two inputs multiplied", "Two real panels with different brightness make the gotcha visible; the diagram of 'times modulate' cannot show the surprise.",
    "C07: two Lab renders of the swatch picture on a Sprite2D at fit scale with modulate #808080, hstack: left lab-shaders/06-empty.gdshader (revealed at 20 %), right lab-shaders/07-own-texture.gdshader (revealed at 62 %); label 'scripted'. Verified (rose patch): left (0.451, 0.176, 0.275), right (0.902, 0.349, 0.549) (the picture untouched is the same as the right).",
    "plus-results a2-06-empty-modulated, a2-07-own-texture-modulated, a2-00",
    caption="COLOR starts as the picture times modulate, the node's tint color",
    readouts=[{"at": 0.25, "text": "keeps modulate", "x": 0.25, "y": 0.95}, {"at": 0.64, "text": "drops it", "x": 0.75, "y": 0.95}])
lab("B10", 1, "tint = multiply", "08-tint.gdshader", f"{PUB}/tint.mp4", "Godot 4.7.2 · Forward+ · shader switched on by script",
    [{"at": 0.15, "lines": [L("08-tint.gdshader", "COLOR.rgb")], "label": ".rgb: picks red, green and blue; alpha stays"}],
    "Code card at left (a tint color multiplied into COLOR.rgb). At right the real four-patch picture, untouched, then the shader is switched on and every patch warms: the rose deepens, the sky patch turns slate. A readout '1.0, 0.7, 0.5' (the tint) appears.",
    "The picture turns warm the moment the tint is switched on.",
    [{"at": 0.15, "event": "COLOR.rgb line highlighted"}, {"at": 0.3, "event": "shader switches on; readout 1.0, 0.7, 0.5"}],
    "manim: a bar of each channel shrinking", "The warm shift on the real patches is what a tint is; bars could only show the arithmetic.",
    "C08: Lab sprite (swatches kind: rose, leaf, sky, sand), shader lab-shaders/08-tint.gdshader switched on with `--material-at` at 25 % of the beat, 30 fps, Forward+, label 'scripted'. Verified patch centres: rose (0.902, 0.349, 0.549) -> (0.902, 0.243, 0.275); leaf (0.400, 0.651, 0.349) -> (0.400, 0.455, 0.176); sky (0.400, 0.502, 0.851) -> (0.400, 0.353, 0.427); sand (0.878, 0.690, 0.290) -> (0.878, 0.482, 0.145).",
    "plus-results a2-08-tint",
    readouts=[{"at": 0.3, "text": "1.0, 0.7, 0.5", "x": 0.5, "y": 0.95}])
lab("B11", 1, "invert = one minus", "09-invert.gdshader", f"{PUB}/invert.mp4", "Godot 4.7.2 · Forward+ · shader switched on by script",
    [{"at": 0.15, "lines": [L("09-invert.gdshader", "COLOR.rgb")], "label": "one minus"}],
    "Code card at left (COLOR.rgb = 1.0 - COLOR.rgb). At right the real four-patch picture, untouched, then switched: rose becomes green, leaf becomes purple, sky becomes brown, sand becomes blue. A readout '0.90 → 0.10' on the rose patch.",
    "Every patch flips to its opposite the moment the shader switches on.",
    [{"at": 0.15, "event": "line highlighted"}, {"at": 0.3, "event": "shader switches on; every patch flips"}, {"at": 0.4, "event": "readout 0.90 -> 0.10 on the rose patch"}],
    "manim: a channel bar flipping", "The opposite colors on the real patches are the claim; the arithmetic is one line.",
    "C09: Lab sprite (swatches), lab-shaders/09-invert.gdshader switched on with `--material-at` at 25 % of the beat, 30 fps, Forward+, 'scripted'. Verified: rose (0.902, 0.349, 0.549) -> (0.098, 0.651, 0.451); leaf -> (0.600, 0.349, 0.651); sky -> (0.600, 0.498, 0.149); sand -> (0.122, 0.310, 0.710).",
    "plus-results a2-09-invert",
    readouts=[{"at": 0.4, "text": "0.90 → 0.10", "x": 0.38, "y": 0.3}])
lab("B12", 1, "flipping alpha too makes a hole", "10-invert-all.gdshader", f"{PUB}/invert-all.mp4", "Godot 4.7.2 · Forward+ · shader switched on by script",
    [{"at": 0.15, "lines": [L("10-invert-all.gdshader", "COLOR = ")], "label": "all four, alpha too"}],
    "Code card at left (COLOR = vec4(1.0) - COLOR). At right the real teal test sprite on the stage, then switched: the sprite becomes a see-through hole and the empty square around it becomes a solid white card. Readouts 'alpha 1→0' on the sprite and 'alpha 0→1' on the card.",
    "The sprite punches out as a hole in a white card the moment the shader switches on.",
    [{"at": 0.15, "event": "line highlighted"}, {"at": 0.3, "event": "shader switches on: white card with a hole"}, {"at": 0.55, "event": "readouts on the hole and on the card"}],
    "manim: alpha bar flipping", "The hole in a white card is a surprise that the numbers alone would not make you believe.",
    "C10: Lab sprite (the teal test sprite with eyes), lab-shaders/10-invert-all.gdshader switched on with `--material-at` at 25 % of the beat, 30 fps, Forward+, 'scripted'. Verified: centre of the sprite = the stage color (0.851, 0.835, 0.792) (alpha 0); a transparent corner = (1.0, 1.0, 1.0) (alpha 1). GATE V note: pale card on a pale stage.",
    "plus-results a2-10-invert-all-sprite",
    readouts=[{"at": 0.58, "text": "alpha 1→0", "x": 0.5, "y": 0.5}, {"at": 0.7, "text": "alpha 0→1", "x": 0.3, "y": 0.2}])
lab("B13", 1, "add: the screen cuts everything off at one", "11-brighten.gdshader", f"{PUB}/brighten.mp4", "Godot 4.7.2 · Forward+ · shader switched on by script",
    [{"at": 0.15, "lines": [L("11-brighten.gdshader", "COLOR.rgb")], "label": "ramp: a smooth run of values from 0 up to 1"}],
    "Code card at left (COLOR.rgb += UV.x). At right the real four-patch picture, untouched, then switched: the left edge is only a little brighter and the right edge is flat white, every patch ending in the same white. A ring on the flat white area and a readout 'cut at 1'.",
    "The picture washes out toward flat white from left to right when the shader switches on.",
    [{"at": 0.15, "event": "line highlighted"}, {"at": 0.3, "event": "shader switches on: brighter, ending in flat white on the right"}, {"at": 0.7, "event": "ring on the white area; readout cut at 1"}],
    "manim: a bar growing past 1 and stopping", "The blown-out real picture shows the consequence of the cut-off, which a bar would only illustrate.",
    "C11: Lab sprite (swatches), lab-shaders/11-brighten.gdshader switched on with `--material-at` at 25 % of the beat, 30 fps, Forward+, 'scripted'. Verified: rose patch (UV.x about 0.25) (1.0, 0.596, 0.796); leaf patch (UV.x about 0.75) (1.0, 1.0, 1.0). A separate script check (verify-clamp.gd): a shader writing 1.5, 1.2, 0.5 reads back 1.0, 1.0, 0.502 with HDR 2D off and 1.5, 1.2, 0.5 with it on.",
    "plus-results a2-11-brighten; run-9-clamp-forward_plus.log",
    readouts=[{"at": 0.7, "text": "cut at 1", "x": 0.62, "y": 0.5}], rings=[{"at": 0.7, "box": [0.5, 0.1, 0.74, 0.9]}])
lab("B14", 1, "gray by copying one channel", "12-gray-red.gdshader", f"{PUB}/gray-red.mp4", "Godot 4.7.2 · Forward+ · shader switched on by script",
    [{"at": 0.15, "lines": [L("12-gray-red.gdshader", "float gray")], "label": "gray = the red channel"}, {"at": 0.3, "lines": [L("12-gray-red.gdshader", "COLOR.rgb")], "label": "vec3(gray): the same number three times"}],
    "Code card at left (gray = COLOR.r, then vec3(gray)). At right the real four-patch picture, untouched, then switched to gray: rose and sand turn light gray, leaf and sky turn a much darker gray. Readouts on three patches: 0.90, 0.40, 0.40.",
    "Three of the patches jump to very different grays the moment the shader switches on.",
    [{"at": 0.15, "event": "gray line highlighted"}, {"at": 0.3, "event": "vec3 line highlighted; shader switches on"}, {"at": 0.62, "event": "readouts 0.90, 0.40, 0.40 land"}],
    "manim: three bars and their grays", "A bright rose beside dark leaf and sky, from colors of similar brightness, is the flaw on show.",
    "C12: Lab sprite (swatches), lab-shaders/12-gray-red.gdshader switched on with `--material-at` at 25 % of the beat, 30 fps, Forward+, 'scripted'. Verified gray values: rose 0.902, leaf 0.400, sky 0.400, sand 0.878.",
    "plus-results a2-12-gray-red",
    readouts=[{"at": 0.62, "text": "0.90", "x": 0.39, "y": 0.3}, {"at": 0.7, "text": "0.40", "x": 0.61, "y": 0.3}, {"at": 0.78, "text": "0.40", "x": 0.39, "y": 0.7}])
lab("B15", 1, "gray by weighing the channels", "13-gray-weighted.gdshader", f"{PUB}/gray-compare.mp4", "Godot 4.7.2 · Forward+ · two renders, both switched on by script",
    [{"at": 0.12, "lines": [L("13-gray-weighted.gdshader", "float gray")], "label": "dot: multiply the matching parts, then add them"}],
    "Code card at left (gray = dot(COLOR.rgb, vec3(0.2126, 0.7152, 0.0722))). At right two real panels of the four-patch picture in gray: on the left the crude red-channel version, on the right the weighted one where the rose, the leaf and the sky land on close grays and sand stays lightest. Readouts 0.48, 0.58, 0.51 on the weighted panel.",
    "The right panel's three patches settle at nearly the same gray while the left panel's do not.",
    [{"at": 0.12, "event": "weights line highlighted"}, {"at": 0.25, "event": "left panel: crude copy of red"}, {"at": 0.6, "event": "right panel appears: close grays; readouts 0.48, 0.58, 0.51"}],
    "manim: a bar of weights", "Two grays of the same picture side by side is the comparison the sentence makes; the weights are in the code.",
    "C13: two Lab renders of the swatch picture, hstack: left lab-shaders/12-gray-red.gdshader, right lab-shaders/13-gray-weighted.gdshader, both switched on with `--material-at` at 12 %; right panel revealed at 40 %. Verified weighted grays: rose 0.482, leaf 0.577, sky 0.506, sand 0.702. The weights follow Rec. 709: derived from the primaries in evidence/planning-checks/derive-bt709-weights.py; Godot's Color.get_luminance() returns the same three weights.",
    "plus-results a2-13-gray-weighted; run-8-luminance-and-curve.log; run-11-derive-bt709-weights.log",
    caption="weights for the Rec. 709 primaries, the ones sRGB uses",
    readouts=[{"at": 0.62, "text": "0.48", "x": 0.69, "y": 0.3}, {"at": 0.7, "text": "0.58", "x": 0.86, "y": 0.3}, {"at": 0.78, "text": "0.51", "x": 0.69, "y": 0.7}])
lab("B16", 1, "mix: blend by an amount", "14-mix.gdshader", f"{PUB}/mix.mp4", "Godot 4.7.2 · Forward+ · amount swept by script",
    [{"at": 0.15, "lines": [L("14-mix.gdshader", "uniform")], "label": "amount: 0 to 1"}, {"at": 0.32, "lines": [L("14-mix.gdshader", "mix(")], "label": "mix: blends from a to b: t of 0 gives a, 1 gives b"}],
    "Code card at left (an amount uniform; mix of the color and its gray). At right the real four-patch picture draining of its color as the amount sweeps from 0 to 1, a thin 0 to 1 strip under the window with a marker riding the amount.",
    "The picture drains from full color to gray while the amount marker rides from 0 to 1.",
    [{"at": 0.15, "event": "amount line highlighted"}, {"at": 0.32, "event": "mix line highlighted; the sweep starts"}, {"at": 0.85, "event": "all gray, marker at 1"}],
    "ShaderLab stills at three amounts", "A sweep with its marker is what 'an amount from zero to one' means; stills would lose the continuity.",
    "C14: Lab sprite (swatches), lab-shaders/14-mix.gdshader, `--animate amount:0.1:0,0.85:1`, 30 fps, Forward+, 'scripted'. Verified patch centres: amount 0.0 the picture untouched; amount 0.5 rose (0.690, 0.416, 0.514), leaf (0.486, 0.612, 0.463), sky (0.451, 0.502, 0.678), sand (0.788, 0.694, 0.494); amount 1.0 the weighted grays (0.482, 0.577, 0.506, 0.702).",
    "plus-results a2-14-mix-0.0, -0.5, -1.0", ramp={"at": 0.1, "from": 0, "to": 1}, readouts=[{"at": 0.1, "text": "amount", "x": 0.5, "y": 0.97}])

# ═════════════════════════════ ACT III · Noise as a Mask ═════════════════════════════
lab("B17", 2, "noise is a table of numbers: a mask", "15-noise-mask.gdshader", f"{PUB}/noise-mask.png", "Godot 4.7.2 · Forward+ · a teal Color Rect, alpha = noise",
    [{"at": 0.2, "lines": [L("15-noise-mask.gdshader", "COLOR.a")], "label": "mask: a number from 0 to 1 per pixel, how much to show"}],
    "Act title 'Noise as a Mask' (serif 40) top-left. Code card at left (COLOR.a = the noise value). At right a real Godot window: a teal Color Rect whose opacity follows the noise, so soft teal clouds fade into the stage. Three readouts on three spots: 0.08 (nearly nothing), 0.50, 0.91 (nearly solid teal).",
    "Readouts land on three spots of the clouds, low, middle and high.",
    [{"at": 0.2, "event": "alpha line: mask, how much to show"}, {"at": 0.3, "event": "readout 0.08 on a pale spot"}, {"at": 0.4, "event": "readout 0.50"}, {"at": 0.65, "event": "readout 0.91 on a solid spot"}],
    "manim: a grey picture turning into numbers", "Real clouds with real numbers at three pixels show that a texture can be a map of amounts; teal-on-stage has no near-black pixels.",
    "C15: Lab rect 360x360 logical with the node color #5FA391 (a ColorRect color, not a shader literal), lab-shaders/15-noise-mask.gdshader, noise_tex = NoiseTexture2D (FastNoiseLite seed 7, frequency 0.02, 256 x 256), still PNG at 4K. Verified noise values at (0.363, 0.454) = 0.082, (0.181, 0.606) = 0.502, (0.637, 0.698) = 0.906; the picture is a normalized noise: min 0.0, max 1.0.",
    "run-12-plus-extras 'noise values'; run-5-noise-facts.log",
    readouts=[{"at": 0.3, "text": "0.08", "x": 0.363, "y": 0.454}, {"at": 0.4, "text": "0.50", "x": 0.181, "y": 0.606}, {"at": 0.65, "text": "0.91", "x": 0.637, "y": 0.698}])
lab("B18", 2, "Godot makes noise textures for you", None, f"{PUB}/editor-noise.mp4", "Godot 4.7.2 editor · scripted editor session",
    [],
    "Five real frames of the Godot editor's Inspector (a scripted editor session) for a Sprite2D whose shader has a Noise Tex slot, joined by slow cross-dissolves: the slot empty; the slot's menu open, a heading New above bare class names, NoiseTexture2D ringed; inside the NoiseTexture2D, its Noise slot's menu open (heading New, FastNoiseLite) with FastNoiseLite ringed; the NoiseTexture2D view with FastNoiseLite in its Noise slot and Width and Height ringed (this view has no preview); then the FastNoiseLite itself, where the grey clouds preview appears, with Seed ringed. One terracotta ring on the row or entry being named.",
    "The ring moves entry to entry as the voice names each step: the slot, NoiseTexture2D, FastNoiseLite, the size, the seed and the clouds.",
    [{"at": 0.06, "event": "E1-1a: the Noise Tex slot ringed (empty)"}, {"at": 0.2, "event": "dissolve to E1-1b: the slot's menu open, heading New"}, {"at": 0.33, "event": "NoiseTexture2D ringed in the list"},
     {"at": 0.58, "event": "dissolve to E1-2c: the Noise slot's menu open"}, {"at": 0.66, "event": "FastNoiseLite ringed under New"}, {"at": 0.74, "event": "dissolve to E1-3a: the NoiseTexture2D with FastNoiseLite in its Noise slot"},
     {"at": 0.86, "event": "Width and Height ringed"}, {"at": 0.9, "event": "dissolve to E1-3b: the FastNoiseLite, clouds preview"}, {"at": 0.94, "event": "Seed ringed"}],
    "GodotDevWorkbench (labelled reconstruction)", "Real editor frames, recorded by script, are the rung-1 SHOW-THE-THING answer; a reconstruction would only claim the labels.",
    "E1 (DONE by script, 2026-10-13, editor driver; README 2.7): five full frames from `_godot-shaders-series/editor-capture/png/1920x1080/textures-and-color/` (native 3456x1944 twins beside them in png/3456x1944/): textures-and-color_E1-1a_noise_tex-slot-empty, E1-1b_noise_tex-dropdown-open, E1-2c_noise-dropdown-open, E1-3a_NoiseTexture2D-width-height-noise-FastNoiseLite, E1-3b_inside-FastNoiseLite-preview-clouds. Join them with ffmpeg cross-dissolves at 0.2, 0.58, 0.74 and 0.9 of the beat (the voice's 'Click it' falls inside 45 to 55 %, so the click state E1-2b, the NoiseTexture2D with its Noise empty, is a spare and is not shown); ring boxes are fractions of the whole 1920x1080 frame (no crop). Real labels: the slot's menu has a Search box, a heading New, 19 bare class names (NoiseTexture2D last), then Quick Load... and Load...; inside the NoiseTexture2D the Noise slot's menu is the heading New, FastNoiseLite, Quick Load..., Load...; the NoiseTexture2D view lists Width, Height, Generate Mipmaps, Noise, Color Ramp, Seamless, Invert, In 3D Space, As Normal Map, Normalize and has NO preview; the grey clouds are in the FastNoiseLite view (preview with a 3D button, Noise Type, Seed, Frequency, Offset). No pointer is visible (Movie Maker records the window only): the clicks are the driver's, so the label says scripted editor session.",
    "Editor capture E1, DONE by script (_godot-shaders-series/editor-capture/png/1920x1080/textures-and-color/E1-*); FACTCHECK row 52 (CORRECTED labels)", layout="video", lane="editor",
    rings=[{"at": 0.06, "box": [0.784, 0.389, 0.996, 0.414]}, {"at": 0.33, "box": [0.836, 0.91, 0.988, 0.934]}, {"at": 0.66, "box": [0.908, 0.382, 0.989, 0.406]},
           {"at": 0.86, "box": [0.783, 0.226, 0.996, 0.283]}, {"at": 0.94, "box": [0.783, 0.416, 0.996, 0.442]}])
lab("B19", 2, "step cuts the clouds at a threshold", "16-step-cut.gdshader", f"{PUB}/step.mp4", "Godot 4.7.2 · Forward+ · threshold swept by script",
    [{"at": 0.2, "lines": [L("16-step-cut.gdshader", "step(")], "label": "step: 0 below the edge, 1 from the edge up"}, {"at": 0.62, "lines": [L("16-step-cut.gdshader", "uniform float")], "label": "threshold: slide it up"}],
    "Code card at left (COLOR.a = step(threshold, n)). At right the teal Color Rect: at threshold 0 solid teal, then as the threshold sweeps up the cloud edges turn hard and the teal shrinks into blobs and disappears. A thin 0 to 1 strip under the window with a marker riding the threshold.",
    "The teal shrinks into hard-edged blobs and vanishes as the threshold marker rides from 0 to 1.",
    [{"at": 0.2, "event": "step line highlighted: 0 below, 1 at or above"}, {"at": 0.35, "event": "the sweep starts: hard edges"}, {"at": 0.62, "event": "threshold line highlighted; blobs shrinking"}, {"at": 0.9, "event": "almost nothing left"}],
    "manim: a number line with a threshold", "A threshold sweeping through real clouds is what 'cut' means; a number line would not show the blobs.",
    "C16: Lab rect 360x360 logical with node color #5FA391, lab-shaders/16-step-cut.gdshader, noise_tex = the same NoiseTexture2D, `--animate threshold:0.1:0,0.97:1`, 30 fps, Forward+, 'scripted'. Verified teal share of the frame: threshold 0.25 = 92.2 %, 0.5 = 51.6 %, 0.75 = 8.4 % (plus-analysis.txt).",
    "plus-analysis.txt (step shares)", ramp={"at": 0.1, "from": 0, "to": 1}, readouts=[{"at": 0.1, "text": "threshold", "x": 0.5, "y": 0.97}])
lab("B20", 2, "discard below the threshold: the sprite is eaten away", "17-dissolve-cut.gdshader", f"{PUB}/dissolve-cut.mp4", "Godot 4.7.2 · Forward+ · progress swept by script",
    [{"at": 0.15, "lines": [L("17-dissolve-cut.gdshader", "if (n"), L("17-dissolve-cut.gdshader", "discard")], "label": "discard: draw nothing here"},
     {"at": 0.62, "lines": [L("17-dissolve-cut.gdshader", "uniform float")], "label": "progress: a uniform your game sets, a dial"}],
    "Code card at left (if the noise is below progress, discard). At right the real teal test sprite on the stage: ragged holes open in the shape of the clouds and grow until the sprite is gone, with the stage showing through every hole. A 0 to 1 strip under the window with a marker riding progress.",
    "Holes open and grow in the shape of the clouds as the progress marker rides from 0 to 1.",
    [{"at": 0.15, "event": "if and discard lines highlighted"}, {"at": 0.3, "event": "the first holes open"}, {"at": 0.62, "event": "progress line highlighted; about half the sprite gone"}, {"at": 0.88, "event": "almost gone"}],
    "manim: a sprite with holes appearing", "The stage showing through real holes is what discard does; a drawing would only claim it.",
    "C17: Lab sprite (teal test sprite, fit scale), lab-shaders/17-dissolve-cut.gdshader, noise_tex = the same NoiseTexture2D, `--animate progress:0.1:0,0.97:1`, 30 fps, Forward+, 'scripted'. Verified sprite pixels left (of 23,512): progress 0.25 = 90.0 %, 0.5 = 46.0 %, 0.75 = 8.7 %, 1.0 = 0 (plus-analysis.txt).",
    "plus-analysis.txt (cut only); plus-results a3-17-cut-*", ramp={"at": 0.1, "from": 0, "to": 1}, readouts=[{"at": 0.1, "text": "progress", "x": 0.5, "y": 0.97}])
manim("B21", 2, "the burning band sits just above the threshold", "Band",
      "A horizontal strip of noise values from 0 to 1 drawn in light-to-mid grays with end labels '0' and '1'. A terracotta marker 'threshold' sits on the strip with a bracket just to its right marking a band one tenth wide, labelled 'band: a strip of noise values, a tenth wide'. Below the strip a row of twelve pixel cells, each holding a noise value: cells whose value is below the marker are drawn as empty outlines, cells inside the band glow yellow-orange-red, cells beyond stay teal. The marker slides right; the band moves with it and cells burn, then vanish, in order.",
      "The marker slides right and the band right behind it lights up the pixels that are next to go.",
      [{"at": 0.12, "event": "strip, marker, bracket, the row of cells"}, {"at": 0.25, "event": "marker slides from 0.2 to 0.45; cells under the band glow"}, {"at": 0.42, "event": "marker settles at 0.45: band and glowing cells shown; held through 60 %"}, {"at": 0.65, "event": "marker slides on to 0.7: glowing cells vanish behind it"}, {"at": 0.88, "event": "hold"}],
      "ShaderLab", "A moving marker with a band behind it is a quantity moving along a number line, which is Manim's job; the Lab render shows the effect, not why those pixels.")
manim("B22", 2, "the color comes from a second table, looked up by a number", "RampLookup",
      "Left, a real Lab crop of the burning edge (a zoomed still of the dissolve at progress 0.5 with a thick yellow-to-dark-red rim); at the bottom the real burn ramp as a horizontal strip labelled 'ramp: a smooth run of colors', end labels '0' and '1' (dark red at 0, yellow at 1). Three sample pixels on the edge crop are boxed in terracotta; from each a thin line runs down to an address on the strip: the pixel nearest the hole to 1.0 (yellow), a middle one to 0.5 (orange), the outermost to 0.0 (dark red), each with a readout 'heat 1.0 / 0.5 / 0.0'.",
      "Lines run from three pixels on the edge to three addresses on the ramp, the nearest pixel to the hottest end.",
      [{"at": 0.12, "event": "edge crop and ramp strip"}, {"at": 0.3, "event": "first boxed pixel (nearest the hole) and its line to 1.0"}, {"at": 0.42, "event": "second pixel to 0.5; settles through 60 %"}, {"at": 0.66, "event": "third pixel to 0.0"}, {"at": 0.85, "event": "all three lines held"}],
      "ShaderLab with the ramp strip", "Real pixels connected to real addresses on a real ramp is the lookup-by-number idea, drawn; the capture alone cannot show the connection.",
      "S1 (edge crop of the Lab render lab-shaders/18-dissolve.gdshader at progress 0.5, sprite scale 4.5) and S2 (the ramp strip: the Lab render of lab-shaders/01-lookup.gdshader with tex = the GradientTexture1D); both Lab stills, stills only")
lab("B23", 2, "the whole shader, twelve lines of code", "18-dissolve.gdshader", f"{PUB}/dissolve.mp4", "Godot 4.7.2 · Forward+ · progress swept by script",
    [{"at": 0.12, "lines": [L("18-dissolve.gdshader", "float n")]},
     {"at": 0.3, "lines": [L("18-dissolve.gdshader", "uniform float progress"), L("18-dissolve.gdshader", "float cut"), L("18-dissolve.gdshader", "discard")]},
     {"at": 0.62, "lines": [L("18-dissolve.gdshader", "uniform sampler2D ramp_tex"), L("18-dissolve.gdshader", "float heat"), L("18-dissolve.gdshader", "vec3 fire"), L("18-dissolve.gdshader", "if (heat")]},
     {"at": 0.85, "lines": [L("18-dissolve.gdshader", "void fragment"), L("18-dissolve.gdshader", "float n"), L("18-dissolve.gdshader", "float cut"), L("18-dissolve.gdshader", "discard"), L("18-dissolve.gdshader", "float heat"), L("18-dissolve.gdshader", "vec3 fire"), L("18-dissolve.gdshader", "if (heat")]}],
    "The full dissolve shader at left (twelve lines of code); at right the real sprite burning away with its yellow-to-red rim as progress sweeps from 0 to 1, a 0 to 1 strip under the window carrying a marker. The highlight walks through the code as the voice names noise, progress and the ramp.",
    "The highlight walks the code while the sprite burns away.",
    [{"at": 0.12, "event": "the noise lookup"}, {"at": 0.3, "event": "progress, cut and discard"}, {"at": 0.62, "event": "heat, the ramp lookup and the color"}, {"at": 0.85, "event": "the whole function"}],
    "LectureCodeTrace alone", "The payoff needs code and its running result together; the ramp-strip marker shows the dial.",
    "C18: Lab sprite (teal test sprite, fit scale), lab-shaders/18-dissolve.gdshader, noise_tex = NoiseTexture2D (seed 7, frequency 0.02, 256), ramp_tex = GradientTexture1D (#8A2A12, #F08A2C, #F7D46B), `--animate progress:0.1:0,0.97:1`, 30 fps, Forward+, 'scripted'. Verified (sprite 23,512 px): progress 0 whole, 0.25 = 20,391 sprite px + 2,371 burning, 0.5 = 8,815 + 4,132, 0.75 = 921 + 1,655, 1.0 = none.",
    "plus-analysis.txt (fixed); plus-results a3-18-dissolve-*", ramp={"at": 0.1, "from": 0, "to": 1}, readouts=[{"at": 0.1, "text": "progress", "x": 0.5, "y": 0.97}])
lab("B24", 2, "swap the table: a gradient makes a wipe", "18-dissolve.gdshader", f"{PUB}/wipe.mp4", "Godot 4.7.2 · Forward+ · gradient where the noise was · progress swept by script",
    [{"at": 0.2, "lines": [L("18-dissolve.gdshader", "uniform sampler2D noise_tex")], "label": "the table you swap"}],
    "The same dissolve shader at left with the noise slot highlighted. At right the real sprite: a straight burning edge sweeps across it from left to right, leaving the right part intact until it arrives. A caption 'gradient, not noise'.",
    "A straight burning edge travels left to right across the sprite.",
    [{"at": 0.2, "event": "noise_tex line highlighted: the table you swap"}, {"at": 0.3, "event": "the straight edge starts to travel"}, {"at": 0.85, "event": "edge near the right side of the sprite"}],
    "ShaderLab with the noise sweep next to it", "The same code with a different table and a different effect is the whole idea; a still frame would hide the travel.",
    "C19: Lab sprite (teal test sprite, fit scale), lab-shaders/18-dissolve.gdshader, noise_tex = the Lab's 'gradient' kind (its red channel runs 0 -> 1 left to right), ramp_tex as C18, `--animate progress:0.1:0.15,0.97:0.85`, 30 fps, Forward+, 'scripted'. Verified left edge of what is left at progress 0.35 / 0.5 / 0.65 = x 258 / 306 / 353 of 640.",
    "plus-analysis.txt (wipe); plus-results a3-18-wipe-*", readouts=[{"at": 0.3, "text": "gradient, not noise", "x": 0.5, "y": 0.95}])
lab("B25", 2, "the first version failed at progress zero", "18-dissolve.gdshader", f"{PUB}/ends-check.mp4", "Godot 4.7.2 · Forward+ · progress 0, two shaders",
    [{"at": 0.15, "lines": [L("18-dissolve.gdshader", "float cut")], "label": "starts a band below zero"}],
    "The fixed shader at left with the cut line highlighted. At right two real panels of the sprite at progress 0: on the left the first version, with a few specks of burning already on it, ringed in terracotta with a readout '160 pixels burning'; on the right the fixed version, perfectly clean. Labels 'first version' and 'fixed'.",
    "The ring lands on the specks in the left panel while the right panel stays clean.",
    [{"at": 0.15, "event": "cut line highlighted"}, {"at": 0.2, "event": "left panel labelled first version"}, {"at": 0.3, "event": "ring on the specks; 160 pixels burning"}, {"at": 0.62, "event": "right panel appears, clean, labelled fixed"}],
    "manim: a band hanging off the noise range", "Real specks on a sprite that should be untouched are the bug in evidence; the number line explains why but does not show it.",
    "C20: two Lab renders of the sprite at progress 0, hstack: left lab-shaders/19-dissolve-first-try.gdshader, right lab-shaders/18-dissolve.gdshader (same noise and ramp as C18); right revealed at 60 %. Verified: first version 160 burning pixels in three specks (boxes in the 640x360 frame: (341,129)-(348,137), (271,160)-(291,175), (287,185)-(308,205)); fixed version 0. At progress 1 both are empty.",
    "plus-analysis.txt (first try); plus-results a3-19-first-try-0.0",
    readouts=[{"at": 0.2, "text": "first version", "x": 0.25, "y": 0.95}, {"at": 0.3, "text": "160 pixels burning", "x": 0.25, "y": 0.12}, {"at": 0.64, "text": "fixed", "x": 0.75, "y": 0.95}],
    rings=[{"at": 0.3, "box": [0.2, 0.34, 0.285, 0.6]}])
lab("B26", 2, "tween progress; set the start value first", None, f"{PUB}/tween.mp4", "Godot 4.7.2 · Forward+ · scripted run: the tween starts at 1 s",
    [{"at": 0.2, "lines": [1], "label": "a start value first"}, {"at": 0.6, "lines": [2, 3], "label": "tween: Godot changes a value smoothly over time"}],
    "A three-line GDScript card at left (set progress to 0.0; create a tween; tween the shader parameter progress to 1.0 over two seconds). At right the real sprite burning away over two seconds. A caption under the window quotes the real error that line one prevents.",
    "The sprite burns away over two seconds once the tween lines run.",
    [{"at": 0.2, "event": "the set line highlighted: a start value first"}, {"at": 0.6, "event": "the tween lines highlighted; the burn starts"}],
    "ShaderLab with only the error text", "Cause (three lines) and effect (the burn) together, with the verbatim error as the price of skipping line one.",
    "C21: scene with a Sprite2D 'Sprite' using lab-shaders/18-dissolve.gdshader (noise and ramp as C18); the scene script runs `start_tween` through `--call-at` at 25 % of the beat: set_shader_parameter(\"progress\", 0.0) then a Tween to 1.0 over 2.0 s; 30 fps, Forward+. Verified in run-10 (verify-tween-progress.gd): with the first line progress 0.4998 at 0.5 s, sprite gone by 1.2 s; without it the console prints 'The tweened property \"shader_parameter/progress\" does not exist' and nothing moves.",
    "run-10-tween-progress.log (both runs; the failing one kept)",
    code='$Sprite.material.set_shader_parameter("progress", 0.0)\nvar tween := create_tween()\ntween.tween_property($Sprite.material, "shader_parameter/progress", 1.0, 2.0)',
    code_file="scene script (GDScript)",
    caption='without line 1: "The tweened property … does not exist"')

# ═════════════════════════════ ACT IV · Two Ways to Count Light ═════════════════════════════
lab("B27", 3, "one 3D shader, two renderers, two middles", "20-blend-3d.gdshader", f"{PUB}/two-renderers.mp4", "Godot 4.7.2 · unshaded 3D quad · Forward+ above, Compatibility below · Apple M4 Pro",
    [{"at": 0.12, "lines": [L("20-blend-3d.gdshader", "shader_type"), L("20-blend-3d.gdshader", "render_mode")], "label": "spatial: a 3D shader; unshaded: no lighting"},
     {"at": 0.32, "lines": [L("20-blend-3d.gdshader", "ALBEDO")], "label": "ALBEDO: the color a 3D shader outputs"}],
    "Act title 'Two Ways to Count Light' (serif 40) top-left. Code card at left (a spatial unshaded shader that mixes two source-color grays by UV.x). At right two real horizontal gray strips stacked, the same shader in two renderers: top labelled 'Forward+', bottom 'Compatibility'. A readout at the middle of the top strip '0.60', then at the middle of the bottom strip '0.50'.",
    "The two strips differ visibly at the middle, and the readouts land top then bottom.",
    [{"at": 0.12, "event": "spatial and unshaded lines highlighted"}, {"at": 0.2, "event": "labels Forward+ and Compatibility"}, {"at": 0.32, "event": "ALBEDO line highlighted"}, {"at": 0.68, "event": "readout 0.60 on the top strip"}, {"at": 0.85, "event": "readout 0.50 on the bottom strip"}],
    "LectureEvidenceTable with the two numbers", "The two strips side by side let the eye see the gap before the numbers say it; this is the film's central surprise.",
    "C22: two Lab renders of lab-shaders/20-blend-3d.gdshader (quad3d, 1280x360 logical each), vstack: top --renderer forward_plus, bottom --renderer gl_compatibility; stills. Verified at the middle (0.5, 0.5): Forward+ 0.600, Mobile 0.600, Compatibility 0.502; at 0.1: 0.329 / 0.333 / 0.259; at 0.9: 0.765 / 0.765 / 0.741. GATE T note: the 0.2 gray end is dark; strips are tall, so they are not text-shaped.",
    "plus-results a4-20-blend-3d-*",
    caption="Forward+: default on desktop · Compatibility: widest hardware, default on web",
    readouts=[{"at": 0.2, "text": "Forward+", "x": 0.1, "y": 0.06}, {"at": 0.24, "text": "Compatibility", "x": 0.14, "y": 0.56}, {"at": 0.68, "text": "0.60", "x": 0.5, "y": 0.28}, {"at": 0.85, "text": "0.50", "x": 0.5, "y": 0.78}])
manim("B28", 3, "what a pixel probe measures", "Probe",
      "A left-to-right chain of four outline boxes: 'numbers you typed', 'shader math', 'the renderer', 'pixel on screen'. A terracotta token travels the chain. A magnifier (a circle and a handle) lands on the last box with the label 'probe: reads one pixel's color'. Under the chain a second, shorter chain 'no window' leads to a box 'no pixels' that is struck through, labelled 'null'.",
      "The token travels the chain and the magnifier lands at its end; the lower chain stops at an empty box.",
      [{"at": 0.12, "event": "the four boxes"}, {"at": 0.3, "event": "token travels the chain"}, {"at": 0.46, "event": "magnifier on the last box: a probe reads here; settled through 60 %"}, {"at": 0.74, "event": "second chain: no window, no pixels, null"}],
      "LectureEvidenceTable", "A pipeline with the probe at its very end shows that a probe sees only the last box's output; a table cannot show where the magnifier sits.",
      "run-13-headless.log (headless get_image() is null, windowed reads 0.2, 0.4, 0.6)")
manim("B29", 3, "two ways to count brightness", "TwoScales",
      "Axes: the horizontal axis 'typed number (sRGB: the scale color pickers use)' from 0 to 1, the vertical 'light (linear: numbers that add up like light)' from 0 to 1. A dashed diagonal marked 'if the two agreed'. The real sRGB curve is drawn from (0, 0) to (1, 1), bending under the diagonal. Rings on the two ends where it meets the diagonal. A dot slides along the curve to x = 0.5 and drops a dashed line to y = 0.21 with the label '0.5 typed = 0.21 light'.",
      "The curve draws itself under the diagonal; a dot rides it and drops to 0.21 at 0.5.",
      [{"at": 0.12, "event": "axes and the dashed diagonal"}, {"at": 0.3, "event": "the curve draws; rings on both ends"}, {"at": 0.45, "event": "dot at x = 0.5 drops to 0.21; settled through 60 %"}, {"at": 0.78, "event": "hold with the gap between curve and diagonal labelled"}],
      "ShaderLab", "A curve under a diagonal is exactly 'the two scales agree at the ends and disagree between'; a render could not show a scale.",
      "run-8-luminance-and-curve.log (srgb_to_linear: 0.5 -> 0.214, 0.2 -> 0.0331, 0.8 -> 0.6038)")
manim("B30", 3, "the same two grays, two midpoints", "TwoMidpoints",
      "The same axes and curve. Two dots on the curve at typed 0.2 and 0.8 (light 0.03 and 0.60) joined by a thin chord. Path A: a dashed vertical from typed 0.5 marks the average of the typed numbers, a marker on the horizontal axis labelled '0.5'. Path B: a dashed horizontal at light 0.32 (the average of the two lights) runs to the curve and drops to the horizontal axis at '0.6'. Both markers stay on the axis, labelled 'average the typed numbers' and 'average the light'.",
      "Two dashed paths trace to two different markers on the axis, 0.5 and 0.6.",
      [{"at": 0.12, "event": "the curve with the two grays on it and their chord"}, {"at": 0.28, "event": "path A: typed average, marker 0.5"}, {"at": 0.44, "event": "path B: light average, marker 0.6; settled through 60 %"}, {"at": 0.78, "event": "hold: 0.5 and 0.6 labelled"}],
      "ShaderLab", "Two paths to two numbers on one axis make 'same colors, two answers' visible; the renders in the previous beat show the pixels, this shows why.",
      "run-8-luminance-and-curve.log (typed midpoint 0.5; light midpoint 0.3185 shown as typed 0.5999)")
rem("B31", 3, "which renderer blends in what (3D)", "LectureEvidenceTable",
    {"title": "The same blend, three renderers", "headers": ["Renderer", "Blends in", "Middle reads", "Default on"],
     "rows": [["Forward+", "light", "0.60", "desktop"], ["Mobile", "light", "0.60", "mobile devices"], ["Compatibility", "typed numbers", "0.50", "web"]],
     "note": "Unshaded 3D quad · grays 0.2 and 0.8 · Apple M4 Pro · Godot 4.7.2 · docs: OUTPUT_IS_SRGB", "cues": [0.14, 0.42, 0.7], "durationSeconds": "__AUDIO__"},
    "A three-row table, one row ringed as each renderer is named, the third column carrying the real measured pixel and the fourth saying where each renderer is the default (desktop, mobile devices, web), which defines Mobile where it is first spoken.", "The ring steps down the rows with the voice.",
    [{"at": 0.14, "event": "Forward+ row"}, {"at": 0.42, "event": "Mobile row"}, {"at": 0.7, "event": "Compatibility row"}],
    "manim", "Three parallel facts with a measured number each is what the table component is for; the previous beat already showed the picture.",
    "plus-results a4-20-blend-3d-forward_plus, -mobile, -gl_compatibility; docs spatial reference OUTPUT_IS_SRGB")
rem("B32", 3, "the same blend in 2D: default and HDR 2D", "LectureEvidenceTable",
    {"title": "The same blend in 2D", "headers": ["2D setting", "Forward+ and Mobile", "Compatibility"],
     "rows": [["default", "0.50", "0.50"], ["HDR 2D on", "0.60", "not supported"]],
     "note": "HDR 2D: 2D drawn in light, numbers past one kept · M4 Pro · Godot 4.7.2", "cues": [0.16, 0.62], "durationSeconds": "__AUDIO__"},
    "A two-row table, the default row ringed first, then the HDR 2D row.", "The ring moves from the first row to the second.",
    [{"at": 0.16, "event": "default row: 0.50 everywhere"}, {"at": 0.62, "event": "HDR 2D row: 0.60 and not supported"}],
    "ShaderLab with the HDR 2D project setting", "Two facts in two rows; the picture for the same blend was the previous Act's.",
    "plus-results a4-21-blend-2d-*; run-3-hdr2d-*.log; run-9-clamp-*.log")

# ═════════════════════════════ ACT V · Hint Colors, Not Masks ═════════════════════════════
rem("B33", 4, "the docs say where the hint matters", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#using-source-color",
     "image": f"{PUB}/docs-source-color.png", "caption": "hint: the word after a colon that tells Godot how to treat a uniform",
     "frame": "browser", "moves": [{"at": 0, "x": 0.5, "y": 0.3, "scale": 1}, {"at": 0.3, "x": 0.45, "y": 0.52, "scale": 1.6}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "Act title 'Hint Colors, Not Masks' (serif 40) top-left. The real Godot 4.7 'Using source_color' section in a browser window; the camera pushes in on the paragraph that says where the hint is required and where it is optional, and a terracotta ring marks that paragraph.",
    "The camera pushes in on the paragraph the voice is reading.",
    [{"at": 0, "event": "the documentation page"}, {"at": 0.3, "event": "push-in and ring on the required / optional paragraph"}],
    "ShaderLab: a hint line in code", "The claim is a documentation claim, and the matrix measured in the previous Act agrees with it: the documentation itself is the evidence (SHOW-THE-THING).",
    "D1: Playwright capture of the live docs page at the #using-source-color anchor (1600x900 at 2.4x), read 2026-10-13: 'Using source_color hint is required in the Forward+ and Mobile renderers, and in canvas_item shaders when HDR 2D is enabled. The source_color hint is optional for the Compatibility renderer, and for canvas_item shaders if HDR 2D is disabled.'")
lab("B34", 4, "what the hint does; the Inspector shows a picker", "22-picker.gdshader", f"{PUB}/editor-picker.png", "Godot 4.7.2 editor · scripted editor session",
    [{"at": 0.2, "lines": [L("22-picker.gdshader", "uniform vec4 picked")], "label": "source_color: the numbers are sRGB"},
     {"at": 0.7, "lines": [L("22-picker.gdshader", "uniform vec4 typed")], "label": "no hint: four plain numbers"}],
    "Code card at left (two vec4 uniforms with the same numbers, one with source color, one without). At right a real still of the Inspector's Shader Parameters group from a scripted editor session: Picked is a color swatch (a click on it opens the picker), Typed is four number boxes x, y, z, w (0.2, 0.4, 0.6, 1.0). A terracotta ring on the swatch, then on the four boxes.",
    "The ring moves from the color swatch to the four number boxes.",
    [{"at": 0.2, "event": "picked line highlighted; ring on the swatch"}, {"at": 0.7, "event": "typed line highlighted; ring on the four boxes"}],
    "ShaderLab video of a Lab render with the same values", "Real editor frames, recorded by script, are the strongest evidence that a hinted color becomes a swatch that opens a picker; the type-level check agrees (FACTCHECK).",
    "E2 (DONE by script, 2026-10-13): `_godot-shaders-series/editor-capture/png/3456x1944/textures-and-color/textures-and-color_E2_picked-swatch-and-typed-four-boxes.png` (the 1920x1080 twin is in png/1920x1080/). Crop the Inspector from the native frame: the rectangle x 1275 to 1915, y 195 to 555 in 1920x1080 coordinates, times 1.8 for the native file (1152 x 648 px, 16:9); save as editor-picker.png (a still). The ring boxes below are fractions of that crop. Real labels: group Shader Parameters; Picked is an EditorPropertyColor (swatch, `source_color` vec4); Typed is four number boxes labelled x y z w. No pointer is visible; the clip is a scripted editor session. Type-level check: evidence/planning-checks/run-4-inspector-types.log (Color against Vector4).",
    "Editor capture E2, DONE by script (_godot-shaders-series/editor-capture/png/1920x1080/textures-and-color/E2); FACTCHECK row 94 (PASS); run-4-inspector-types.log (Color against Vector4)", layout="side", lane="editor",
    rings=[{"at": 0.25, "box": [0.683, 0.625, 0.992, 0.7]}, {"at": 0.72, "box": [0.37, 0.797, 0.992, 0.892]}])
lab("B35", 4, "no hint: washed out; node colors are converted for you", "23-patch-hinted.gdshader", f"{PUB}/three-patches.png", "Godot 4.7.2 · Forward+ · HDR 2D on · Apple M4 Pro",
    [{"at": 0.15, "lines": [L("23-patch-hinted.gdshader", "uniform vec4")], "label": "source_color: the numbers are sRGB"}],
    "Code card at left (the hinted flat-color shader; the voice says the third patch has the same line without the hint). At right three real steel-blue patches: a Color Rect, a hinted shader patch, and an unhinted shader patch that is visibly lighter. Readouts under them: 'node color', 'hinted', 'no hint', then the numbers 0.20 0.40 0.60 under the first two and about 0.48 0.66 0.80 under the third.",
    "The third patch is visibly paler than the other two, and its numbers land under it.",
    [{"at": 0.15, "event": "hint line highlighted"}, {"at": 0.3, "event": "labels node color, hinted, no hint"}, {"at": 0.62, "event": "numbers land under the patches"}],
    "manim: three swatches", "Three real patches, two identical and one pale, show the washed-out color at a glance; the voice points at the one that is wrong.",
    "C23: custom scene (reference script evidence/planning-checks/verify-patches.gd): three 96x140 patches on the stage at 320x180 logical, scaled to 4K: a ColorRect with color (0.2, 0.4, 0.6); a ColorRect with lab-shaders/23-patch-hinted.gdshader; a ColorRect with lab-shaders/24-patch-plain.gdshader; Viewport.use_hdr_2d = true, --rendering-method forward_plus; PNG converted from linear to what the screen shows. Verified centres: node (0.1999, 0.3999, 0.5998), hinted (0.1999, 0.3999, 0.5998), plain (0.4845, 0.6651, 0.7975) (an 8-bit capture reads 0.48, 0.66, 0.80). With HDR 2D off, or in Compatibility, all three are (0.2, 0.4, 0.6).",
    "run-14-three-patches.log; plus-results a5-23/24",
    readouts=[{"at": 0.3, "text": "node color", "x": 0.18, "y": 0.95}, {"at": 0.34, "text": "hinted", "x": 0.5, "y": 0.95}, {"at": 0.38, "text": "no hint", "x": 0.82, "y": 0.95},
              {"at": 0.62, "text": "0.20 0.40 0.60", "x": 0.34, "y": 0.5}, {"at": 0.7, "text": "0.48 0.66 0.80", "x": 0.82, "y": 0.5}])
lab("B36", 4, "from code: pass the color as picked", None, f"{PUB}/from-code.png", "Godot 4.7.2 · Forward+ · HDR 2D on · two patches",
    [{"at": 0.15, "lines": [1], "label": "as picked"}, {"at": 0.62, "lines": [2], "label": "converted twice"}],
    "A two-line GDScript card at left (set the tint to the color as picked; set it to color.srgb_to_linear()). At right two real patches: steel blue for the first line, a dark navy for the second. Labels 'as picked' and 'converted first'.",
    "The second patch is far darker than the first.",
    [{"at": 0.15, "event": "the as-picked line"}, {"at": 0.62, "event": "the converted-first line; the navy patch appears"}],
    "ShaderLab stills", "Two patches from two lines of code is cause and effect; the navy one is the double conversion made visible.",
    "C24: custom scene as C23 with two patches using lab-shaders/23-patch-hinted.gdshader and HDR 2D on: the first with tint = Color(0.2, 0.4, 0.6), the second with tint = Color(0.2, 0.4, 0.6).srgb_to_linear() = (0.0331, 0.1328, 0.3184). Verified (runner_plus, HDR 2D, Forward+): (0.196, 0.396, 0.596) against (0.031, 0.129, 0.318). Also on an unshaded 3D quad in Forward+ (run-12 g): (0.200, 0.400, 0.600) against (0.031, 0.133, 0.318).",
    "run-12-plus-extras 'converted first'; run-1-colorspace (3D)",
    code='material.set_shader_parameter("tint", color)\nmaterial.set_shader_parameter("tint", color.srgb_to_linear())', code_file="scene script (GDScript)",
    readouts=[{"at": 0.3, "text": "as picked", "x": 0.28, "y": 0.95}, {"at": 0.66, "text": "converted first", "x": 0.74, "y": 0.95}])
lab("B37", 4, "a color texture needs the hint too", "25-swatch-hinted.gdshader", f"{PUB}/swatch-grid.png", "Godot 4.7.2 · unshaded 3D quad · four real renders",
    [{"at": 0.15, "lines": [L("25-swatch-hinted.gdshader", "uniform sampler2D")], "label": "color texture: hinted"}],
    "Code card at left (a spatial unshaded shader that shows a texture, with the hint). At right a two-by-two grid of real renders of the four-patch picture: top row Forward+ (hinted: true colors; not hinted: pale, washed out), bottom row Compatibility (both true). Labels 'hint' and 'no hint' above the columns, 'Forward+' and 'Compatibility' beside the rows.",
    "Only one cell of four is pale: the Forward+ render without the hint.",
    [{"at": 0.15, "event": "texture line highlighted"}, {"at": 0.3, "event": "column and row labels"}, {"at": 0.65, "event": "ring on the one pale cell"}],
    "manim: a texture passing through two scales", "Four real cells where three agree and one is pale carry both claims, the washed-out look and the way the mistake hides in Compatibility.",
    "C25: four Lab renders of the swatches texture (quad3d, tex = picture) joined with ffmpeg xstack as a 2x2: lab-shaders/25-swatch-hinted.gdshader and 26-swatch-plain.gdshader, each in forward_plus and in gl_compatibility; stills. Verified (rose patch): Forward+ hinted (0.902, 0.349, 0.549), plain (0.957, 0.624, 0.765); Compatibility hinted and plain (0.902, 0.349, 0.549). Mobile matches Forward+ (plain 0.957, 0.627, 0.769).",
    "plus-results a5-25/26-*",
    rings=[{"at": 0.65, "box": [0.5, 0.0, 1.0, 0.5]}],
    readouts=[{"at": 0.3, "text": "hint", "x": 0.25, "y": 0.04}, {"at": 0.34, "text": "no hint", "x": 0.75, "y": 0.04}, {"at": 0.38, "text": "Forward+", "x": 0.04, "y": 0.25}, {"at": 0.42, "text": "Compatibility", "x": 0.06, "y": 0.75}])
lab("B38", 4, "hint a mask and its numbers shift", "28-mask-hinted.gdshader", f"{PUB}/mask-compare.png", "Godot 4.7.2 · unshaded 3D quad · Forward+ · two renders of a gray ramp",
    [{"at": 0.15, "lines": [L("28-mask-hinted.gdshader", "uniform sampler2D")], "label": "a mask with the hint: wrong"}, {"at": 0.4, "lines": [L("28-mask-hinted.gdshader", "step(")], "label": "step at one half"}],
    "Code card at left (the mask shader with the hint, cutting at 0.5). At right two real horizontal strips of the same gray ramp cut at one half: the top one without the hint switches colors at the middle, the bottom one with the hint switches about three quarters of the way across. Readouts 'no hint 0.50' and 'hint 0.74' (where each strip switches), with a terracotta ring on each switch.",
    "The ring jumps from the middle of the top strip to three quarters of the way across the bottom one.",
    [{"at": 0.15, "event": "texture line highlighted: a mask with the hint"}, {"at": 0.4, "event": "step line highlighted"}, {"at": 0.62, "event": "ring on the top strip's cut: 0.50"}, {"at": 0.85, "event": "ring on the bottom strip's cut: 0.74"}],
    "manim: two number lines with a cut", "Two real strips cut in two places is the shifted threshold on screen; a diagram would assert it.",
    "C26: two Lab renders of the gray ramp (the 256-wide ramp_grey texture: value = x / 255) on a 3D unshaded quad, Forward+, vstack: top lab-shaders/27-mask-plain.gdshader, bottom lab-shaders/28-mask-hinted.gdshader (both with source-color cream and teal uniforms); stills. Verified: no hint flips cream -> teal between x = 0.50 and 0.51; hint flips between 0.73 and 0.74. In Compatibility both flip near 0.50. In HDR 2D (canvas_item) the same shift (run-6).",
    "run-12-plus-extras 'mask'; plus-results a5-27/28-*",
    rings=[{"at": 0.62, "box": [0.45, 0.0, 0.56, 0.5]}, {"at": 0.85, "box": [0.7, 0.5, 0.81, 1.0]}],
    readouts=[{"at": 0.3, "text": "no hint 0.50", "x": 0.3, "y": 0.04}, {"at": 0.34, "text": "hint 0.74", "x": 0.5, "y": 0.54}])
rem("B39", 4, "the rule: which numbers get the hint", "LectureEvidenceTable",
    {"title": "Which numbers get the hint", "headers": ["It holds", "source_color?"],
     "rows": [["a color uniform", "yes"], ["a color texture", "yes"], ["a mask, like noise", "no"], ["a plain number", "no"]],
     "note": "Godot 4.7 shading language · name the renderer with every number you measure", "cues": [0.1, 0.28, 0.62, 0.8], "durationSeconds": "__AUDIO__"},
    "A four-row table, the answer column ringed row by row as each kind is named.", "The ring steps down the four kinds.",
    [{"at": 0.1, "event": "color uniform: yes"}, {"at": 0.28, "event": "color texture: yes"}, {"at": 0.62, "event": "mask: no"}, {"at": 0.8, "event": "plain number: no"}],
    "manim", "A short rule over four kinds is the right shape for the table component; every row was demonstrated in the pictures before it.",
    "docs: hint table and 'Using source_color'; run-2 (uniform), run-6 (texture, mask)")
lab("B40", 4, "where a project's renderer is chosen", None, f"{PUB}/editor-renderer.mp4", "Godot 4.7.2 editor · scripted editor session",
    [],
    "Three real frames of the Godot editor's Project Settings dialog (a scripted editor session), joined by cross-dissolves: Rendering, Renderer open, with the Renderer entry in the left tree and then the Rendering Method row (forward_plus) ringed; the Rendering Method menu open, its three entries forward_plus, mobile, gl_compatibility ringed; then the dialog's note 'Changed settings will be applied to the editor after restarting.' with the Save & Restart button ringed.",
    "The ring moves from the Renderer page to the Rendering Method row, to the three entries, to Save & Restart as the voice names each.",
    [{"at": 0.22, "event": "R1-C: the Renderer page ringed in the left tree"}, {"at": 0.3, "event": "the Rendering Method row ringed (forward_plus)"}, {"at": 0.34, "event": "dissolve to R1-D: the Rendering Method menu open"},
     {"at": 0.38, "event": "the three entries ringed: forward_plus, mobile, gl_compatibility"}, {"at": 0.56, "event": "dissolve to R1-E: the restart note"}, {"at": 0.6, "event": "Save & Restart ringed"}],
    "GodotDevWorkbench (labelled reconstruction)", "Real editor frames, recorded by script, are the rung-1 SHOW-THE-THING answer; a reconstruction would only claim the labels, and the first plan's picture (the renderer's name in the upper right corner) is not what the 4.7.2 editor shows by default.",
    "E3 (replaced; DONE by script, 2026-10-13, README section 11): three full frames from `_godot-shaders-series/editor-capture/png/1920x1080/renderer-path/` (native twins in png/3456x1944/renderer-path/): renderer-path_R1-C_Project-Settings_Rendering-Renderer_menu-closed, R1-D_Project-Settings_Rendering-Method_menu-open, R1-E_Project-Settings_restart-note. Cross-dissolve at 0.34 and 0.56 of the beat; ring boxes are fractions of the whole 1920x1080 frame (no crop). Real labels: dialog 'Project Settings (project.godot)'; left tree Rendering > Renderer (a second page named Rendering sits under Internationalization: not that one); rows 'Rendering Method' (forward_plus), 'Rendering Method.web', 'Rendering Method.mobile'; the dropdown lists forward_plus, mobile, gl_compatibility; after a change the note reads 'Changed settings will be applied to the editor after restarting.' with the buttons Save & Restart and X. Save & Restart was never pressed, so the film says nothing about what follows. The frames show the scratch project name, and the editor draws its own menu bar inside the window (Use Embedded Menu on): label the clip 'scripted editor session'. NOT used: the title-bar renderer name (hidden by default in 4.7.2; shown only after Editor > Editor Settings > Interface > Editor > Appearance > Show Renderer Selector, frames R3-A, R3-B and the OFF-vs-ON composite).",
    "Editor capture E3 replaced by the renderer-path frames R1-C, R1-D, R1-E (DONE by script, editor-capture/README.md section 11); FACTCHECK rows 106 (CORRECTED: docs versus run) and 107", layout="video", lane="editor",
    rings=[{"at": 0.22, "box": [0.179, 0.716, 0.264, 0.742]}, {"at": 0.3, "box": [0.279, 0.233, 0.835, 0.261]}, {"at": 0.38, "box": [0.56, 0.27, 0.83, 0.345]}, {"at": 0.6, "box": [0.748, 0.756, 0.815, 0.792]}])
lab("B41", 4, "the dissolve's two hints, checked", "18-dissolve.gdshader", f"{PUB}/dissolve.mp4", "Godot 4.7.2 · Forward+ · progress swept by script",
    [{"at": 0.2, "lines": [L("18-dissolve.gdshader", "uniform sampler2D ramp_tex")], "label": "a color: hinted"},
     {"at": 0.58, "lines": [L("18-dissolve.gdshader", "uniform sampler2D noise_tex")], "label": "a mask: no hint"}],
    "The finished dissolve shader at left; the ramp_tex line highlighted with 'a color: hinted', then the noise_tex line with 'a mask: no hint'. At right the real sprite burning away again.",
    "The highlight lands on the ramp line, then the noise line, while the sprite burns.",
    [{"at": 0.2, "event": "ramp_tex line: a color, hinted"}, {"at": 0.58, "event": "noise_tex line: a mask, no hint"}],
    "LectureCodeTrace alone", "The film's own shader is the worked example of the rule, with its two texture lines marked.",
    "C18 reused (the same capture as B23).",
    "plus-analysis.txt (fixed)", ramp={"at": 0.1, "from": 0, "to": 1}, readouts=[{"at": 0.1, "text": "progress", "x": 0.5, "y": 0.97}])

# ───────────────────────────── guards: ShaderLab limits from COMPONENT-SPECS ─────────────────────────────
for e in E:
    pr = e["entry"].get("props", {})
    for c in pr.get("cues", []):
        if isinstance(c, dict):     # ShaderLab cues; the tables' cues are plain fractions
            assert len(c.get("label", "")) <= 60, (e["bid"], "cue label over 60 characters", c["label"])
            assert not (0.45 <= c["at"] <= 0.55), (e["bid"], "a cue inside 45 to 55 %", c["at"])
        else:
            assert not (0.45 <= c <= 0.55), (e["bid"], "a table cue inside 45 to 55 %", c)
    for k in ("readouts", "rings"):
        for r in pr.get(k, []):
            assert not (0.45 <= r["at"] <= 0.55), (e["bid"], k, "starts inside 45 to 55 %", r["at"])
    if pr.get("caption"):
        assert len(pr["caption"]) <= 80 or e["entry"]["pattern"] != "ShaderLab", (e["bid"], "caption over 80 characters")
    for r in pr.get("readouts", []):
        assert len(r["text"].split()) <= 3, (e["bid"], "readout over three words", r["text"])
    if e["entry"].get("pattern") == "ShaderLab":
        assert len(pr.get("code", "").split("\n")) <= 14, (e["bid"], "ShaderLab code over 14 lines")

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
sl = ["# Shot list: Textures and Color\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab, harness or editor capture of a tested file in `lab-shaders/`; three beats show the real editor, one a real docs page. What must be built or recorded first is listed below; every capture is specified in `CAPTURE-PLAN.md`.\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component, **`shader_kit.py`** Manim helpers and the **capture harness** (`lab/capture.gd` + `capture_shader.sh`): shared with the other shader films, specified in `../_godot-shaders-series/COMPONENT-SPECS.md`. Build them once; if another film's build already made them, reuse them.\n"
      "2. **Harness additions this film needs** (listed in `CAPTURE-PLAN.md` section H): the extra texture kinds (a 6 by 6 F table, a four-patch swatch picture, a burn-ramp GradientTexture1D, a grey ramp, NoiseTexture2D), a ColorRect node color, a switch-on time for a material, HDR 2D, a modulate, composites of two or four renders, and three small custom scenes. A reference implementation (`evidence/planning-checks/runner_plus.gd`, `verify-patches.gd`) is already verified.\n"
      "3. **Editor frames** E1, E2 and the renderer-path frames for B40 are already recorded by script (`CAPTURE-PLAN.md` section E): copy them, no clicks. Then the **docs screenshot D1**.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
