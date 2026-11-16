# Manim scene build brief (Godot shader films): for the builder of one act's scenes

**What this is.** The instructions for writing the Manim scenes of ONE act of one Godot shader film: `scenes_act<N>.py` in the film's folder, from the layout the earlier session already did.
**Why.** Scenes are mechanical once the layout is fixed; a builder per act lets one film's acts be written in parallel while the machine records captures.
**Found.** The kit (`shader_kit.py`), the preflight script and the assembler exist and were tested on the pilot (2026-10-14). The narration, the beat sheet and every picture's description are fixed: you implement them, you do not redesign them.

All paths are absolute under `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/`.
`S` = `_godot-shaders-series/`   `FILM` = the film folder you are given (`claude-liam-lecture-<slug>/`).

## Read first

1. `S/shader_kit.py` completely: palette, `T()`, `M()` (monospace), `ease_in`, `arrow`, `box`, `ring`, `ramp_strip`/`ramp_marker`, `pixel_grid`/`tint`/`fill_in`, `plot`, `vertex_quad`, `uv_square`, `worker_grid`/`worker_one`, `code_card`, `sprite_icon`, and the pacing helpers `until(self, phrase)`, `done(self)`, `guard`, `ST`. Use these objects so every film looks like one series. Do NOT edit the kit; if you need a new helper, write it in your act file with your act prefix (`a2_ring_label`, ...).
2. `FILM/lanes/act<N>.json` (your beats: `visual_intent`, `motion_claim`, `show` cues with `at` fractions), the matching rows of `FILM/SHOTLIST.md`, `FILM/ACTS.md` (the cast for your act: the same object is the same picture throughout the act), and each beat's narration and MEASURED duration in `FILM/beat_sheet.json` (`narration_text`, `actual_duration_s`; the audio is already made: the measured duration is the clock).
3. `S/GLOSSARY.md` for the wording of any term you put on screen.
4. A finished example of the scene style: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/scenes_act1.py`.

## What to write

`FILM/scenes_act<N>.py` containing ONLY beat classes `class B##_Name(Scene):` (the class names exactly as in the lanes; the literal `(Scene)` base is required) and helpers prefixed `a<N>_`. No imports needed: the kit is pasted above your file by `S/assemble_scenes.py` (`from manim import *`, numpy as `np`, everything in the kit). Every scene:

- sized to the measured duration: end each scene with `done(self)` (it waits out the rest of the audio and prints `[pace]`); never run past `actual_duration_s` (the compiler centre-cuts overruns).
- timed to the words: `until(self, "a phrase from the narration")` waits until that phrase is spoken (character share of the measured audio). Land each `show` cue on its words; cue `at` fractions are estimates, the narration decides.
- one idea, one motion that carries the claim (the voice can point at the motion and say "that is what I mean"). If the scene reads the same as a still, it fails.

## Laws (each cost a compile round before)

- **Gate A (static):** the scene must add at least one new non-text, non-`Rectangle` shape after its first frame (a Dot, Arrow, Line, Circle, RoundedRectangle counts). Forbidden: `ease_in_quad`, `ease_out_cubic` (use `rate_func=ease_in` or the Manim defaults `smooth`, `linear`), `.animate(path_arc=...)`, `MoveAlongPath` plus `.animate` on the same object in one `play`. Stay inside x within +-6.2 and y within +-3.3 (frame is 14.22 by 8).
- **Midpoint rule:** the frame at 45 to 55 percent of the clip must be a settled still containing the labels that matter (nothing half-faded or mid-sweep). `ST.play` (attached automatically) shortens or delays an animation that would cross the midpoint, but design so the key label is already on screen before it.
- **Type:** text at 32 or larger; act titles 40 (Title Case serif, top-left, only on the beats the lane says). Use `T()` (EB Garamond) for words and `M()` (Menlo) for code, 32 minimum. Terracotta is NEVER text, never a thin stroke on its own: dots, rings (with the grey backing, `ring()`), small sparks only. Real numbers on screen are the figures from the lane / FACTCHECK, never invented.
- **No fill behind text.** Outline cells and boxes (`fill=None`); a filled pill behind a label is allowed only when it is white or cream and the text is ink.
- **Dark things fuse:** dark ink shapes packed together read as a text blob to GATE T. Bars and ramps are rows of separate narrow tiles with gaps (`ramp_strip` does this); use teal / grey / cream, not near-black fills; avoid large near-black areas and flat terracotta fields.
- **Pango drops single spaces on this Mac:** after rendering, LOOK at the still. Where words fuse, double the space at that boundary. The `->` glyph is below the type floor: draw arrows as shapes (`arrow()`).
- **Every label on screen is 1 to 3 words** (a hero number or the real text of an artifact is fine); never narration set as type; no bullet lists.
- Same cast per act (see ACTS.md). The test rectangle has four terracotta corner dots; the pixel grid is outline cells; the test sprite is a teal blob with two cream eyes (`sprite_icon`).
- Honesty: say what a demonstration does not show; a drawing is labelled as a drawing where the lane says so; no invented numbers or output.

## Check each scene (this is your job, not the next session's)

```bash
S/preflight.sh FILM <ACT-NUMBER> <Class> [<Class> ...]
```

It runs Gate A and the layout audit and writes a low-resolution last-frame still to `/private/tmp/claude-501/preflight-<slug>-act<N>/stills/<Class>.png`. LOOK at every still with the Read tool. Fix what you see (fused words, off-frame objects, clutter, an empty scene) and re-run only that class. Also check that the printed `[pace]` content time is under the target. Do not render 4K. Do not run `art run` and do not touch `FILM/scenes.py`, `FILM/manim/`, `FILM/media/`, the beat sheet, the narration or the lanes. Do not publish or stage anything.

## Report back (concise)

For each class: written yes/no, Gate A result, audit warnings left, what you saw in the still, anything you could not make work and why. Absolute path of your act file. Anything in the lane you had to deviate from (and why).
