#!/usr/bin/env python3
"""make_scenes.py: writes scenes/*.json, the capture specs of the outline film (one per capture in CAPTURE-PLAN.md).

Spec format and the player that reads it: scene_player.gd (header comment). Canvas 1280 x 720, sprites drawn at whole-number scales, centres rounded
to whole pixels. Every spec's "duration" is the beat's ESTIMATED audio length (words x 0.34 s) and its keyframe times are PLANNED against the narration
(see ../../_sync.py: the second a phrase is spoken, estimated from word counts). The build stretches the timeline to the measured audio:
    scene_time = audio_time x duration / measured_audio_seconds
so a keyframe stays on its phrase even when Kokoro runs faster or slower than the estimate.
Run: python3 make_scenes.py   (re-writes every spec; CAPTURE-PLAN.md lists them)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
import _sync as Y  # noqa: E402

OUT = HERE / "scenes"
OUT.mkdir(exist_ok=True)
INDIGO = [0.25, 0.25, 0.75, 1.0]
MAGENTA = [0.80, 0.25, 0.55, 1.0]
AMBER = [0.95, 0.70, 0.10, 1.0]
CX, CY = 640, 360
W = Y.when


def keys(*kv, interp="linear"):
    return {"keys": [[round(t, 2), v] for t, v in kv], "interp": interp}


def blob(shader, uniforms=None, scale=4, center=(CX, CY), tex=None, **extra):
    sp = {"name": extra.pop("name", "blob"), "texture": tex or {"kind": "blob"}, "scale": scale, "center": list(center), "filter": "nearest",
          "shader": shader, "uniforms": {"line_color": INDIGO, **(uniforms or {})}}
    sp.update(extra)
    return sp


SCENES = {}


def scene(sid, beat, sprites, still=False, note="", **extra):
    d = {"id": sid, "beat": beat, "canvas": [1280, 720], "duration": Y.EST[beat], "fps": 30, "still": still, "note": note, "sprites": sprites}
    d.update(extra)
    SCENES[sid] = d


# ---------------------------------------------------------------- Act I
sw = W("B01", "Watch what an outline does", 3)
scene("C01-hook", "B01", [blob(None, shader_at=keys((0.0, None), (sw, "08-loop.gdshader"), interp="step"), uniforms={"thickness": 3.0})],
      note="the same sprite; the outline shader (08-loop, thickness 3) switches on as the voice says 'outline'")
g0, g1 = W("B02", "Scale a plus sign up a fifth"), W("B02", "the tips get a thick border")
scene("C02-bigcopy", "B02", [
    {"name": "copy", "texture": {"kind": "plus", "size": 64, "white": True}, "scale": keys((g0, 6.0), (g1, 7.2)), "center": [CX, CY], "filter": "nearest", "modulate": [0.25, 0.25, 0.75, 1.0]},
    {"name": "plus", "texture": {"kind": "plus", "size": 64}, "scale": 6.0, "center": [CX, CY], "filter": "nearest"}],
      note="a plus-shaped sprite (drawn 6x) with a tinted copy behind it that grows by a fifth (6x to 7.2x): tips thick, sides thin")
# the bug-and-fix beats are clips: the result changes the moment the voice names the change (a shader switch), so the picture itself carries the claim
sw7 = W("B07", "Look what happens")
scene("C07-paints-the-sprite", "B07", [blob(None, shader_at=keys((0.0, None), (sw7, "02-paints-the-sprite.gdshader"), interp="step"))],
      note="the plain sprite; the first try (02-paints-the-sprite) switches on as the voice says 'look what happens': almost the whole sprite turns line colour")
sw8 = W("B08", "Multiply by one minus my own alpha")
scene("C08-one-question", "B08", [blob(None, shader_at=keys((0.0, "02-paints-the-sprite.gdshader"), (sw8, "03-one-question.gdshader"), interp="step"))],
      note="the blue sprite of the first try; as the voice says 'multiply by one minus my own alpha' the fix (03-one-question) switches on: the blue drains off, a line on the left only")
sw9 = W("B09", "all four sides")
scene("C09-lighter-diagonals", "B09", [blob(None, shader_at=keys((0.0, "03-one-question.gdshader"), (sw9, "04-lighter-diagonals.gdshader"), interp="step"))],
      note="the one-sided line; as the voice says 'all four sides' the four reads (04-lighter-diagonals) switch on: a ring with lighter stretches on the diagonals")
sw10 = W("B10", "so mix never overshoots")
scene("C10-four-questions", "B10", [blob(None, shader_at=keys((0.0, "04-lighter-diagonals.gdshader"), (sw10, "05-four-questions.gdshader"), interp="step"))],
      note="the ring with lighter stretches; as the voice says 'so mix never overshoots' the cap (05-four-questions) switches on: a uniform ring")

# ---------------------------------------------------------------- Act II
t2, t3, t4 = W("B13", "Thickness one, two, three, four", 3), W("B13", "Thickness one, two, three, four", 4), W("B13", "Thickness one, two, three, four", 5)
scene("C13-thickness-steps", "B13", [blob("06-pixel-steps.gdshader", {"thickness": keys((0.0, 1), (t2, 2), (t3, 3), (t4, 4), interp="step")})],
      note="thickness 1, then 2, 3, 4 as the voice counts; the line is that many image pixels wide (x4 on the canvas)")
c1, c2 = W("B14", "Change the value"), W("B14", "and the line follows")
scene("C14-line-color", "B14", [blob("06-pixel-steps.gdshader", {"thickness": 3.0, "line_color": keys((0.0, INDIGO), (c1, MAGENTA), (c2, AMBER), interp="step")})],
      note="the same shader, the line_color uniform changing: indigo, magenta, amber")
s2, s3 = W("B16", "twice as big"), W("B16", "Three times as big")
scene("C16-scales", "B16", [blob("06-pixel-steps.gdshader", {"thickness": 2.0}, scale=keys((0.0, 1.0), (s2, 2.0), (s3, 3.0), interp="step"))],
      note="thickness 2 at sprite scale 1, 2, 3: the line is 2, 4, 6 canvas pixels")
k2, k3 = W("B17", "On a square sprite"), W("B17", "at thickness three")
th_c = keys((0.0, 1), (k2, 2), (k3, 3), interp="step")
scene("C17-corners", "B17", [
    blob("06-pixel-steps.gdshader", {"thickness": th_c}, scale=4, center=(340, CY), tex={"kind": "crate"}, name="four"),
    blob("07-eight-reads.gdshader", {"thickness": th_c}, scale=4, center=(940, CY), tex={"kind": "crate"}, name="eight")],
      note="left four reads, right eight reads, thickness 1 to 3: the four-read corners stay empty (3 x 3 image pixels each at thickness 3)")

# ---------------------------------------------------------------- Act III
swb = W("B18", "the four corners")
scene("C18-eight-reads", "B18", [blob(None, {"thickness": 3.0}, scale=4, tex={"kind": "crate"}, shader_at=keys((0.0, "06-pixel-steps.gdshader"), (swb, "07-eight-reads.gdshader"), interp="step"))],
      note="the square sprite at thickness 3: with the four sides only, the corners of the line stay empty; as the voice says 'the four corners' the eight reads (07-eight-reads) switch on and the corners fill in")
scene("C19-loop", "B19", [blob("08-loop.gdshader", {"thickness": 3.0}, scale=4, tex={"kind": "crate"})], still=True,
      note="08-loop at thickness 3 on the square sprite: the same complete frame the eight written-out reads drew")
e = "at thickness one, two, three, four and eight"
th_s = keys((0.0, 1), (W("B21", e, 3), 2), (W("B21", e, 4), 3), (W("B21", e, 5), 4), (W("B21", e, 7), 8), interp="step")
scene("C21-same-picture", "B21", [
    blob("07-eight-reads.gdshader", {"thickness": th_s}, scale=3, center=(340, CY), name="eight reads"),
    blob("08-loop.gdshader", {"thickness": th_s}, scale=3, center=(940, CY), name="loop")],
      note="left eight written-out reads, right the loop; thickness 1, 2, 3, 4, 8 as the voice counts; zero pixels differ at every step")
z0 = W("B25", "thickness zero", 1)
th_z = keys((0.0, 2), (z0, 0), interp="step")
scene("C25-zero-means-zero", "B25", [
    blob("08-loop.gdshader", {"thickness": th_z}, center=(330, CY), tex={"kind": "blob_soft"}, name="no guard"),
    blob("09-guard.gdshader", {"thickness": th_z}, center=(950, CY), tex={"kind": "blob_soft"}, name="guard")],
      note="soft-edged sprites; thickness 2 (both ringed) then 0: the unguarded one keeps a tinted rim, the guarded one is clean")
scene("C26-select", "B26", [blob("09-guard.gdshader", {"thickness": 1.0}, name="Sprite")], script="select_snippet.gd",
      input=[{"t": W("B26", "When the unit is selected", 4), "key": "SPACE"}, {"t": W("B26", "When it is not", 3), "key": "SPACE"}],
      note="the script on screen sets thickness 0 in _ready; a scripted key press selects (thickness 2) as the voice says 'selected', another deselects on 'not'")
l_on, i_on = W("B27", "so every unit lights up at once", 3), W("B27", "Declare the uniform as instance", 4)
scene("C27-shared-material", "B27", [
    blob(None, {"thickness": keys((0.0, 0), (l_on, 2), interp="step")}, scale=3, center=(340, CY), name="left",
         shader_at=keys((0.0, "09-guard.gdshader"), (i_on, "13-instance.gdshader"), interp="step"),
         instance_uniforms={"thickness": 2.0}, instance_from=i_on),
    blob(None, {"thickness": 0.0}, scale=3, center=(940, CY), name="right", share_with="left",
         shader_at=keys((0.0, "09-guard.gdshader"), (i_on, "13-instance.gdshader"), interp="step"),
         instance_uniforms={"thickness": 0.0}, instance_from=i_on)],
      note="two units share one material. Until the voice says 'instance' the dial is an ordinary uniform: setting thickness 2 on the left outlines both. After it, an instance uniform: left 2, right 0, one material, one ring")

# ---------------------------------------------------------------- Act IV
d0, d1 = W("B28", "Read a step to the right", 0, 0.8), W("B28", "far enough", 0, 0.8)
scene("C28-slide-clip", "B28", [blob("01-look-right.gdshader", {"look": keys((d0, 0.0), (d1, 0.4))})],
      note="the picture slides left as look goes 0 to 0.4; past about 0.2 the left of the sprite is cut flat by the rectangle")
u0, u1 = W("B29", "Turn the outline up to four", 0), W("B29", "Turn the outline up to four", 5, 0.2)
scene("C29-tight", "B29", [blob("08-loop.gdshader", {"thickness": keys((0.0, 0.0), (u0, 0.0), (u1, 4.0))}, tex={"kind": "blob", "crop": True})],
      note="the sprite trimmed to its shape (77 x 77): thickness 0 to 4; nothing appears where the shape touches the edge")
p0 = 0.6
th_p = keys((0.0, 0.0), (p0, 0.0), (p0 + 1.2, 4.0))
scene("C31-padding", "B31", [
    blob("08-loop.gdshader", {"thickness": th_p}, scale=3, center=(240, CY), tex={"kind": "blob", "crop": True, "pad": 0}, name="pad 0"),
    blob("08-loop.gdshader", {"thickness": th_p}, scale=3, center=(640, CY), tex={"kind": "blob", "crop": True, "pad": 2}, name="pad 2"),
    blob("08-loop.gdshader", {"thickness": th_p}, scale=3, center=(1040, CY), tex={"kind": "blob", "crop": True, "pad": 4}, name="pad 4")],
      note="the trimmed sprite with 0, 2 and 4 pixels of padding (the add_padding function on screen), thickness 0 to 4")
r0, r1 = W("B32", "A read past a frame's edge"), W("B32", "draws a stray line", 0, 0.3)
scene("C32-sheet", "B32", [
    {"name": "whole sheet", "texture": {"kind": "sheet"}, "scale": 3, "center": [340, CY], "filter": "nearest"},
    blob("08-loop.gdshader", {"thickness": keys((0.0, 0.0), (r0, 0.0), (r1, 4.0))}, scale=4, center=(900, CY), tex={"kind": "sheet"}, hframes=2, frame=1, name="frame 1")],
      note="left: the whole packed sheet; right: frame 1 only, outlined at thickness 4: a stray line along its left edge is frame 0's pixels")
q0 = W("B33", "Clamp each read into it", 0, 0.5)
scene("C33-sheet-clamp", "B33", [
    {"name": "whole sheet", "texture": {"kind": "sheet"}, "scale": 3, "center": [340, CY], "filter": "nearest"},
    blob(None, {"thickness": 4.0}, scale=4, center=(900, CY), tex={"kind": "sheet"}, hframes=2, frame=1, name="frame 1",
         shader_at=keys((0.0, "08-loop.gdshader"), (q0, "12-sheet-safe.gdshader"), interp="step"))],
      note="the same frame; as the voice says 'clamp' the reads are clamped into REGION_RECT and the stray line disappears; the disc's own ring stays")

# ---------------------------------------------------------------- Act V
b0, b1 = W("B34", "Now push the thickness"), W("B34", "At eight", 0, 0.8)
bs = keys((b0, 1), (b1, 8))
scene("C34-brushes", "B34", [
    blob("06-pixel-steps.gdshader", {"thickness": bs}, scale=3, center=(215, CY), name="four"),
    blob("07-eight-reads.gdshader", {"thickness": bs}, scale=3, center=(640, CY), name="eight"),
    blob("10-ring.gdshader", {"thickness": bs}, scale=3, center=(1065, CY), name="sixteen")],
      note="four reads, eight reads, a ring of sixteen; thickness 1 to 8 as the voice says 'push the thickness ... at eight'")
y0, y1 = W("B36", "The ring is the loop"), W("B36", "sixteen angles around a full turn", 0, 1.0)
scene("C36-ring", "B36", [blob("10-ring.gdshader", {"thickness": keys((y0, 1), (y1, 8))})], note="the ring of sixteen reads, thickness 1 to 8")
m0, m1 = W("B37", "At thickness eight", 0), W("B37", "At thickness eight", 2, 2.0)
sb = keys((0.0, 1), (m0, 1), (m1, 8))
scene("C37-stem", "B37", [
    blob("08-loop.gdshader", {"thickness": sb}, center=(330, CY), tex={"kind": "mascot"}, name="eight reads"),
    blob("10-ring.gdshader", {"thickness": sb}, center=(950, CY), tex={"kind": "mascot"}, name="ring of sixteen")],
      note="a sprite with a 3-pixel stem: eight reads come apart into floating copies at thickness 6 to 8, the ring of sixteen holds")
RIM = [20, 20, 32, 32]      # a 32 x 32 piece of the rim (upper left of the disc), drawn 12x: each image pixel is 12 canvas pixels
swc = W("B38", "Compute the alpha yourself")
scene("C38-soft-edges", "B38", [
    blob("06-pixel-steps.gdshader", {"thickness": 1.0}, scale=12, center=(330, CY), tex={"kind": "blob_soft", "cut": RIM}, name="mix"),
    blob(None, {"thickness": 1.0}, scale=12, center=(950, CY), tex={"kind": "blob_soft", "cut": RIM}, name="composite",
         shader_at=keys((0.0, "06-pixel-steps.gdshader"), (swc, "11-soft-edges.gdshader"), interp="step"))],
      note="a 12x look at the rim of the soft-edged sprite: plain mix leaves pale, see-through rim pixels (alpha 0.75 at worst) on both sides; as the voice says 'compute the alpha yourself' the right side switches to the composite, which makes them opaque")
swf = W("B39", "nearest made none")
scene("C39-filter", "B39", [
    blob("08-loop.gdshader", {"thickness": 1.0}, scale=12, center=(330, CY), tex={"kind": "blob", "cut": RIM}, name="nearest",
         filter=keys((0.0, "linear"), (swf, "nearest"), interp="step")),
    blob("08-loop.gdshader", {"thickness": 1.0}, scale=12, center=(950, CY), tex={"kind": "blob", "cut": RIM}, name="linear", filter="linear")],
      note="a 12x look at the rim, both sides on the default linear filter and blurred; as the voice says 'nearest made none' the left side switches to nearest: crisp one-pixel steps, while the right stays a blurred line")

f0, f1 = W("B40", "Fade a sprite"), W("B40", "nothing fades", 0, 0.4)
fade = keys((0.0, [1, 1, 1, 1.0]), (f0, [1, 1, 1, 1.0]), (f1, [1, 1, 1, 0.5]))
scene("C40-modulate", "B40", [
    blob("06-pixel-steps.gdshader", {"thickness": 2.0}, scale=4, center=(340, CY), name="color from texture", modulate=fade),
    blob("14-modulate.gdshader", {"thickness": 2.0}, scale=4, center=(940, CY), name="vertex color kept", modulate=fade)],
      note="two sprites with the node's modulate faded to alpha 0.5: the left shader assigns COLOR from the texture and ignores the fade, the right passes the vertex COLOR on as a varying and fades with its line")

for sid, d in SCENES.items():
    (OUT / f"{sid}.json").write_text(json.dumps(d, indent=1) + "\n")
print(len(SCENES), "scenes written to", OUT)
