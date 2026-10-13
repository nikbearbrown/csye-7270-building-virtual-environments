# Checks report (PROOF GATE): SubViewports

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the choices that need explaining (the spoken title, the replaced opening line, the terms card), the risks for the build, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render. It also records, in one place, what a reviewer might otherwise think is a mistake.
**Found.** 40 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: capture 22, Manim 16, editor 2. Estimated 10.4 minutes (46 beats, 1,831 words by the sheet; 1,840 words and 10.5 minutes by the lint's count, which adds the terms card). The lint is clean. Four risks for the build, the new one first: every Godot recording must run with the window on top, because a covered window is drawn on only some frames and Movie Maker then writes repeated frames (`evidence/planning-checks/RESULTS.md`, the covered window).

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 40 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | the act titles are labels on each act's first picture; the bookends are the mandated cards |
| PUNT | 0 | B16 (the prediction question) is a Manim figure of two pictures and a turn, not a text card |

Lane histogram (information, not a quota): capture 22 · manim 16 · editor 2 · remotion 0.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: "Shaders cannot see each other's work", corrected to "can build on").
- [x] The central idea (draw into a picture off to the side, then shade the picture a second time) is shown before it is named in code: B01 is the finished effect, B02 to B05 build the picture.
- [x] Every term the film teaches is defined on screen where it is first spoken, in the GLOSSARY wording where the GLOSSARY has the term (fragment, UV, uniform, COLOR, TIME, texture, fract, step, mix, abs); the terms card holds prerequisites only (Shader, Texture, Viewport, UV, Alpha).
- [x] Concrete before abstract: the real picture first (B13, B14), the rule second (B17); the stripe formula is built in four small steps (B21 to B24) before the code is shown together.
- [x] Predict before reveal: B16 asks which effect turns with the sprite; B17 answers.
- [x] A surprise is demonstrated by a real run: dark edges (B10, run-5), what turns (B17, run-2), the upside-down mesh (B35, run-4).
- [x] Payoff uses every earlier idea together: B36 (the chain) and B37 (three shaders in a row).
- [x] Honest limits: B19 (flattened pixels), B38 (not free; no cost figure, none was measured), B39 (input does not reach a standalone viewport); scripted motion is labelled; the editor beats say "three real frames".
- [x] A measured claim says machine and renderer; every pixel value in FACTCHECK.md is Forward+ unless it says otherwise.
- [x] Standalone: no other film, book or course is mentioned in anything a viewer sees or hears (lint).
- [x] No number on any viewer-facing surface that names a film or an order.

## Choices that need a reason

- **`SPOKEN_TITLE = "Sub Viewports"`.** The title is "SubViewports". Kokoro would read the capital V as part of one word, so the opening and closing cards are voiced as "Sub Viewports". The body says "Sub Viewport" everywhere; the screen keeps `SubViewport` (the node's real name, as in the Inspector).
- **The brief's opening line was replaced.** The brief proposed "Each node gets one shader." with the correction "two shaders in a row". After the correction that sentence reads wrongly (the writer would be un-saying something true: each node still has one Material) and it names no misconception a newcomer actually holds. The film's BIDEA is "Shaders cannot see each other's work", corrected to "can build on", which is what the film then demonstrates (run-6 X3).
- **The terms card holds five prerequisites** (Shader, Texture, Viewport, UV, Alpha). Texture, UV and Alpha are earned again in the beats that use them; SubViewport, ViewportTexture, premultiplied alpha, fract, step, hue, vertex, mesh, uniform and TIME are defined where first spoken, not on the card. The wording of Shader, Texture, UV and Alpha is the GLOSSARY's, word for word (the lint compares them). "Viewport" has no GLOSSARY row; the wording ("a rectangle the engine draws into") is this film's own and is listed in the report to Bear so it can be added.
- **B04 says "under New choose Viewport Texture", not "choose New Viewport Texture".** The documentation words it the second way; the real Texture slot menu has the heading New and the entry ViewportTexture (frame `subviewports_E2-1`, run-15). FACTCHECK row 15 is CORRECTED for this.
- **UV is spelled `UV` on screen and "U V" in narration**, never a lone "U" or "V" (GLOSSARY).
- **Premultiplied alpha (B10) is in the film although neither the brief nor the source teaches it.** Running the source's own fade exposed it: a transparent picture stores half-transparent pixels premultiplied, so the default blend darkens soft edges and the source's `COLOR.a = UV.x` leaves a haze (FACTCHECK rows 25 to 27 and 36). A viewer who pastes the source's code into their own project meets it within a minute.
- **The sprite's turn is scripted** and always labelled so; the inner shader is a fragment gradient. The source's inner vertex shader (scale and rotation matrices) belongs to the Matrices film.
- **Window-pixel built-ins.** The capture route (a 3840 x 2160 SubViewport over the 1280 x 720 logical canvas) changes the numbers of shaders that read window pixels. `grep -E "FRAGCOORD|SCREEN_UV|SCREEN_PIXEL_SIZE|LIGHT_POSITION|LIGHT_VERTEX"` over `lab-shaders/` and `evidence/planning-checks/capture_scene.gd` finds nothing; the shaders read `UV`, `TIME`, `TEXTURE` and `VERTEX` only. So all 22 captures (C01 to C21, with C04 in two parts) use that route, and run-12 checked it against scale 1 for all 22 scenes in both renderers (CAPTURE-PLAN.md, section 1).

## Risks for the build (not defects of the layout)

1. **Window on top, always.** On this Mac a Godot window that other windows cover is drawn on only some frames (137, 136, 108, 125 of 299 were seen; 73 distinct frames of 400 in one Movie Maker run). Every recording uses `--always-on-top` (or `--position 0,0`), including the editor frames; a movie whose frames repeat is a failed recording. A probe script forces one draw per step. Update Mode Once, the beat that depends on the number of draws, is the first thing to go wrong (run-11), and shader `TIME` advances only in a draw. A harness that saves SubViewport textures itself can avoid the problem entirely with recipe B (render loop disabled, one `force_draw(false, 1/30)` per step; CAPTURE-PLAN.md rule 4, verified in run-16 and run-12c).
2. **Frame 0 lacks the pictures.** In 14 of 22 scenes the first recorded frame has no SubViewport picture (run-13b). Drop frame 0 or record with `skip=1` (CAPTURE-PLAN.md).
3. **The shared pieces do not exist yet**: `ShaderLab`, `shader_kit.py`, the capture harness (`../_godot-shaders-series/COMPONENT-SPECS.md`), plus nine Manim kit objects this film adds. If the first film's build has not run, Phase 0 builds them.
4. **GATE T on soft content.** The glow ring (c06) and the clear-coloured picture box are mid-tones on the cream stage; the hue strip (c15) is saturated. Frame captures in the ShaderLab window on the cream stage and check the 50 and 85 percent marks. Rings are grey-backed, never ink; terracotta is never text.
5. **Editor frames** are real, recorded by the series' editor driver from this film's six state scripts (run-15: 0 driver errors, 36 frames, the whole editor window with its title bar and bottom strip). At the default dock width some labels truncate ("Transparent" for Transparent BG, "Subdivide Wi"); the `-wide` frames read in full. The click itself and the mouse pointer are not shown. If the driver fails in the build session, CAPTURE-PLAN.md section 5 lists the fallbacks and the short recording to ask Bear for.
6. **Pace.** The longest beats are B06 and B15 (45 words, about 15 seconds). Nothing is near the 40-second limit; if the voice runs long the cut line in ACTS.md saves about 1 minute 45 seconds.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py subviewports` at the time of writing: no errors, no warnings (46 beats, 1,840 words, 10.5 minutes). See `../_godot-shaders-series/LINT-REPORT.md` for the series run.
