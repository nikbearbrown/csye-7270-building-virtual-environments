# Checks report (PROOF GATE): Shaders in 3D

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, what the build must watch, and the mechanical lint result with every warning read.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 44 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: ShaderLab capture 24, Manim 14, Remotion 5 (a terminal, two tables, two docs screenshots), editor 1 (B43: four real frames of Project Settings recorded by script). Estimated 10.3 minutes by the lint (about 1,800 words with the bookends; 1,496 in the body). `lint_series.py` prints **no errors and no warnings** (the spoken title is "Shaders in three D", the card keeps "3D"; details below). Eleven notes for the build are listed below; the three that matter most are the type gate on the pad's rust frames, the long code lines in `ShaderLab`, and the three shared components (which an earlier film's build may already have made).

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 44 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): capture 24 · manim 14 · remotion 5 · editor 1.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: "a different, harder thing" becomes "the same shape, new names").
- [x] The central idea ("same shape, new names") is shown in motion before any three-D result: the anatomy brackets (B02) and the code morph where only a few tokens change (B05).
- [x] The whole effect is shown first (the pad charging, B01) and read last (Act IV), so the viewer knows what they are working toward.
- [x] Every term the film teaches is defined on screen where first spoken, in GLOSSARY wording (as of 2026-10-13): shader (B02), shader type and mesh (B03), vertex and pixel (B04), alpha (B05, caption), canvas_item (B07, tag on the code line), UV (B08), mesh instance and ShaderMaterial (B09), render mode (B14, the docs' sentence as a tag), light() (B16, two tags), cull_disabled (B17, tag), ramp (B20), fract and floor (B21), step (B22), mix (B24), uniform (B25), hint (B26, the widened wording), tween (B28), swizzle (B33, tag), channel (B38, caption), linear and sRGB (B40, two captions). The word "built-in" is not used in the narration, so it needs no definition. BDEFS holds prerequisites only (mesh, material, albedo, lighting, renderer); the lint compares the card with the GLOSSARY, and mesh, material and renderer use its exact words (albedo and lighting have no row there). One deliberate difference: `source_color` is tagged with the docs' own words ("this vec4 is a color", docs: "Used as color") in B26 and B31, not with the GLOSSARY's longer form ("numbers are sRGB: convert to light first"), because sRGB and linear are not defined until B40; B31's narration only says that the colors are marked source color.
- [x] Predict, then reveal: the flat teal that is not flat (B10), the same instruction given to two squares (B07), the same file in two renderers (B37).
- [x] Concrete before abstract: each idea is on a real render before it is named in a table or a formula (the lit sphere before the surface outputs; the stripes before the pad's lines).
- [x] A measured claim says machine and renderer ("Measured on this Mac", credit line "Apple M4 Pro · Godot 4.7.2", Forward+ or Compatibility on every number).
- [x] Every surprise is demonstrated by a real run: a 2D shader ignored on a mesh (B07, verify8), a shaded sphere (B10), a vanishing square (B17), an empty `light()` that silences the lamp (B16), the box's six stripes against the square's sixteen (B36), two greens (B37).
- [x] The payoff uses the earlier ideas together: Act IV reads the pad with `fract`, `step`, `mix`, a uniform, a hint, `ALBEDO` and `unshaded`; Act V runs the same file in two renderers.
- [x] Honest limits: every scripted motion or call is labelled (lamp switch, lamp turn, swing, turn, sweep, call, tween: the video labels say "scripted"); only B43 shows the editor (real frames, labelled "scripted editor session"), and no Inspector widget is claimed; GPU time and frame rate are not claimed; the box-versus-square ring and the docs ring boxes are marked as estimates until captured; Compatibility's few-step endpoint offset is in FACTCHECK even though the film does not say it.
- [x] Standalone: no reference to another film, book or course in anything viewer-facing (lint).
- [x] No number on any viewer-facing surface that was not read from a run or a docs page; narration spells numbers as words.

## What the Lab cannot do (and what was done instead)

- **Lit versus unshaded.** The Lab's `quad3d` scene has white ambient light at energy 1 and no lamp, so a lit and an unshaded shader read the same pixel there (checks 02 and 07: 0.6431, 0.8196, 0.7804). Lit versus unshaded is therefore shown by the scene scripts (verify4, S3), as the brief's "verify in the Lab" could not work.
- **Meshes other than a quad, a lamp, culling, GDScript calls, tweens**: scene scripts S1 to S6 (CAPTURE-PLAN), each with a verified reference script and a kept log.
- **Brief probes.** The brief's stripe probes at UV.x 0.0625 and 0.1875 both read the dark stripe (half-pixel offset); the film uses 0.03125 and 0.09375 (kept: `12-signal-pad-brief-probes`).

## Risks for the build (not defects of the layout)

1. **Shared components.** `ShaderLab`, `shader_kit.py` and the capture harness (`../_godot-shaders-series/COMPONENT-SPECS.md`) may already exist from an earlier film's build; check before building (BUILD-PROMPT Phase 0).
2. **GATE T on the pad.** The rust frames (0.40, 0.16, 0.09 and the 65 % stripes) are within 48 RGB of ink. Captures are timed so the 50 % and 85 % frames are mid-tone (CAPTURE-PLAN); the held stills of the pad are at 0.3, where its stripes can be seen (`evidence/planning-checks/stripe-contrast.txt`: at 0.5 they are only 3.5 apart on the CIE76 scale); if a frame is still flagged, hold 0.4, then 0.5, for that beat. In Compatibility the dark stripe stays near ink until about 0.5, so the two-renderer frames (C15, C16) are the ones to watch. The stage and the teal spheres were chosen to stay clear of ink.
3. **Long code lines.** The pad's two `uniform vec4` lines are 70 characters. `ShaderLab` must wrap them (pre-wrap) or give the code panel half the width; never shrink below the type floor.
4. **Gate V underfill.** The spheres and the flat squares are small objects on a light stage. Frame them by lowering the capture camera's orthographic size, not by cropping past the window; the beats are declared `sparse: false`, so a major underfill must be fixed in the capture.
5. **Two-renderer composites.** C15 to C17 join two harness runs by ffmpeg; check that the two panes have the same size, the same frame count and the Forward+ pane on the left.
6. **Docs pages.** D1 and D2 quote two sentences the narration paraphrases; if the live wording has changed since 2026-10-13, stop and report. (D3 was dropped: B43 shows the editor.)
7. **Pace.** B08 (45 words), B10 (44), B06 (43), B18 (42) and B04 (41) are the longest beats; if a voice check runs long, split B08 at "Paint it as a color" or B18 after "Add unshaded and see". The longest sentence is 23 words (B42).
8. **Voice.** Listen for "Forward Plus", "vec three, vec four", "s R G B" (B40 and B42), "U V" (B08), "albedo", "unshaded", "fract", "tween", and B24's letters ("Mix of a, b and t is a times one minus t, plus b times t"). Checked with the toolkit's phonemizer, text only, no audio: "Shaders in three D" reads as three D; "U V" as two letters; "t" as "tee"; the single letter "a" is read like the article ("uh"), so B24's formula may sound muddy: if it does, report it (the screen shows the formula in full). Do not edit `liam.json`; report any mispronunciation.
9. **`×` and `−` glyphs** in the Manim formula captions (B21, B24): look at the still; double the space at a fused boundary if Pango drops it.
10. **ShaderLab features this film leans on** (all in `../_godot-shaders-series/COMPONENT-SPECS.md`): cue `label` tags of at most 60 characters (nine beats), `ramp.period` (B25, B34), and a `stack` layout with a one-line excerpt (B07, B08). If the component is built before these features exist, add them there; the lanes assume them.
11. **Lab batch integrity (checked 2026-10-13 after another session ran `pkill -f run-lab-checks.sh`).** `run-lab-checks.sh` has 50 `run` lines (loops expanded); `lab-results.jsonl` has 50 rows with the same 50 labels, no missing and no extra; 48 exit 0 with a `RESULT` line and a PNG each, and the two labelled failures (04 and 05) exit 1 with the compiler's `SHADER ERROR`; the batch log ends with its `wrote ...` line, and every `run-*.log` ends with an `exit` line. Nothing had to be re-run. The extra batch (`run-lab-checks-extra.sh`, added later) has 3 `run` lines and 3 rows, all exit 0.

## Review pass (2026-10-13, a read-only review of this layout, every item checked against the files)

A reviewer cross-checked numbers, beat ids, lanes against code, narration against evidence, teaching and the handoff. All 23 items held up on checking; what was done:

| Finding | Resolution |
|---|---|
| B10's reveal ("one side is bright and one is dim") played over a lamp that had swung behind the sphere | B10 has its own clip (C03a): the lamp is off (a flat dim disc), switches on at 0.56 of the clip at yaw -65 degrees and stays; B11 keeps the swinging lamp (C03). The narration now names the lamp ("with the scene's lamp") and a 'lamp' tag lands |
| The audio-first re-timing contradicted the shown tween (2.0 s), hard-coded seconds in video labels, and C18 had no fraction | CAPTURE-PLAN gives every schedule as a fraction of the clip (C18 hand-over at 0.12, the lamp switch at 0.56, the call in C10 at 0.34, C11 set at 0.04 and tween at 0.19 keeping its 2.0 s); the video labels say "scripted" without seconds |
| FACTCHECK row for B06 (the one CORRECTED row) cited a scratch-only run | `verify14-color-in-spatial.gd` and its log are now in the evidence folder; the row cites them |
| B17's 50 % frame would have been edge-on | C06 turns 0 to 360 degrees across the first 0.8 of the clip (225 degrees at 50 %, front-facing at 85 %) |
| B02 text said 10 lines; the skeleton file has 12 | corrected (functions on lines 5 to 12) |
| B44 motion claim said the ring settles on the left | the ring hops from the left pane to the right pane |
| B28 verified-result text mixed a color channel and an activation | now states the pixel values (red 0.4, (0.298, 0.541, 0.384), flat green) |
| An arrow glyph in a Manim label (B40) and in a readout (B27) | the Manim label is 'linear to sRGB' with the arrows drawn as shapes; the readout is 'activation = 1' |
| The audio-first build order was only in the pilot's build prompt | `patch_build_prompts.py` was run for this film: the "HOW TO RUN THIS BUILD" section is in BUILD-PROMPT.md |
| The terms card differed from the GLOSSARY (three lint warnings) | Mesh, Material and Renderer use the GLOSSARY's exact words; the lint now prints no warnings |
| BUILD-PROMPT used `$R`, `$S`, `$TK` without defining them; no save path for the scene scripts; no description of how `--set-at` and `--call-at` reach a scene script's material | an `export` block, `$R/capture-scenes/`, and a stated scene-script interface (CAPTURE-PLAN) |
| Stale comments in two evidence scripts | corrected, comments only (noted in RESULTS.md) |
| B40 said Compatibility "draws the number as written" though the pad's low channels read a few steps off | the narration claims the verified plain case: "a half stays a half"; FACTCHECK's fix cell says what the film does not claim |
| Paperwork counts and wording (four against six brief changes, three against eleven risks, two different lists of seven facts, "captured at build time", provenance lines for the GDScript cards, "QuadMesh named Pad", B24's example values, two-sentence recap lines, "flat square" over a wide Lab quad) | each fixed: ACTS and CHECKS-REPORT summaries, one list of eight facts in FACTCHECK and RESULTS, captions end "captured YYYY-MM-DD" (the build fills the date), `codeFile` points at `verify3-attach-set-tween.gd`, the node is a MeshInstance3D named Pad, an EXEMPT row for B24's numbers, one sentence per recap line, B19's picture is a true square (the other Lab pictures are the Lab's full-frame quad and the lane text says so) |
| The pad's stripes are almost invisible at half charge (3.5 on the CIE76 scale) where the film asks the viewer to count them; B33's percentages sat on a render whose real ratio is 0.81 | the held stills are at activation 0.3 (5.7 apart; measured in `lab-results-extra.jsonl`, `stripe-contrast.txt`); B33's readouts say 'x 0.65' and 'x 1.0', the code's multipliers |
| B40 and B41 never said why Forward+ does not lift the pad's own colors | B41 now says the colors are marked source color, so Forward+ turns them into linear light first, blends, then converts back; B40 names sRGB and defines linear and sRGB in the GLOSSARY's words; B41 carries the GLOSSARY's short form for `source_color` (B26 and B31 keep the docs' shorter "used as color" because sRGB is not defined until B40) |
| B42 said "s R G B" with no definition | B40 now says "converts it to s R G B" and defines it on screen |
| `channel` (B38) is now a GLOSSARY term | B38 carries the caption "channel: one of red, green, blue or alpha" |
| B27's `$Pad` and B28's `material` were unexplained on the cards | a tag on each: "$Pad: the node named Pad, the pad's mesh instance" and "material: the pad's ShaderMaterial" |
| B03's morph straddled the 50 % frame | it starts at 0.56, after the midpoint |

Held back on purpose: nothing from the review was left open. One judgment call: B31's colors are named on the two code lines ("rust at activation 0, green at activation 1") instead of on the held render, whose blend at 0.3 is olive.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py shaders-in-3d` → **0 errors, 0 warnings** (run last, after every edit). Two history notes, kept because they shaped the files:

- The shared lint first fired on the digit in the title "Shaders in 3D" (the brief mandates that title). The coordinator changed the rule to accept "3D" and added `SPOKEN_TITLE`; `narration.py` now sets `SPOKEN_TITLE = "Shaders in three D"` and builds `BOPEN` from it, and the closing line says it the same way. `TITLE` and `TITLE_LINES` keep "3D" for the card.
- The same update made an unspaced "UV" in narration an error: B08 now says "U V is a point's address" (the on-screen caption keeps `UV`), and the BHTF prompt already said "U V address". No narration line has an uppercase PI or TAU, a parenthesized call such as `fragment()`, or a lone "U" or "V".

## Editor-frame reconciliation 2026-10-13

**What changed.** Beat B43 (narration, lane picture, capture spec) was reconciled with the real Godot 4.7.2 editor frames recorded by script on 2026-10-13 (`../_godot-shaders-series/editor-capture/README.md`, section 11). **Why.** The first plan took the docs' sentence "In the editor, you can always switch between renderers by clicking on the renderer name in the upper-right corner of the editor" as true and showed the docs page (capture D3). The shipped 4.7.2 editor hides that name by default; it appears only after Editor > Editor Settings > Interface > Editor > Appearance > Show Renderer Selector is turned on. A viewer who followed the sentence on a fresh install would find nothing in the corner. Nothing was voiced, rendered or published.

- **B43 narration.** "Its name sits in the upper right corner of the editor, and you can switch it there" became "Open Project Settings, then Rendering, Renderer. Rendering Method shows it, and changing it there needs Save and Restart." The second sentence ("Switching can change how a scene looks, so test again afterwards.") is unchanged and now also rests on this film's own measurements (rows 86 and 88).
- **B43 picture.** The docs screenshot D3 is dropped (the beat does not carry a "the docs say X, the editor shows Y" comparison; the title-bar frames stay unused in the series folder). The lane is now an editor lane: four real frames of the editor (the Project menu; Project Settings on Rendering, Renderer; the Rendering Method menu; the restart note), cross-dissolved, with the ring moving step by step, labelled "scripted editor session".
- **FACTCHECK.** Row 97 is CORRECTED (docs versus run); row 104 is new (the Project Settings path, PASS from the frames); row 98 gained this film's own runs as evidence. No row is OPEN.

Beat ids, beat count (44 body), lane types of every other beat, and acts are unchanged. The line grew from 32 to 33 spoken words; `lint_series.py` counts 1,814 words and 10.3 minutes, no errors, no warnings.
