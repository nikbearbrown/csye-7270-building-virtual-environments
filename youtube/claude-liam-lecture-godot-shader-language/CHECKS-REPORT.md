# Checks report (PROOF GATE): Godot Shader Language

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks the build will meet, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 41 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: Manim 22, ShaderLab capture 8, Remotion 6 (two code panels, two evidence tables, two documentation captures), terminal 5. Estimated 10.9 minutes by the lint's cautious figure (1,918 words by the lint's count: every spoken word plus the terms card); `lint_series.py` is clean, with no errors and no warnings. Three things the build must watch: the shared `ShaderLab` component, GATE T on the dark terminal windows, and the pale phase of the opening pulse.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 41 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | no text-only card names a visual |

Lane histogram (information, not a quota): manim 22 · capture 8 · remotion 6 · terminal 5.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: one number → a bundle of numbers).
- [x] The central idea ("say the type of each piece") is shown in motion on one line (B19, type brackets widening from the inside) before it is applied to a whole file (Act V).
- [x] Every term the film teaches is defined on screen where first spoken (uniform, const, varying, shader type, vertex/fragment/light, built-in, vector, swizzle, signature, hint, UV, TIME, COLOR, alpha, abs, mix); BDEFS holds prerequisites only (shader, pixel, type, function, argument).
- [x] Concrete before abstract: each rule is shown by a real render or the engine's real message before it is summarized (recap in BVDT).
- [x] A framework beat comes before the examples: the three zones of a file (B02) and the signature (B20) are drawn before any rule is applied.
- [x] A worked example uses the framework visibly: Act V reads the opening file line by line with the method on screen.
- [x] A falsifiability / edge-case beat: B32 (a legal comparison that draws nothing) and B41 (one changed word, caught by reading and refused by the engine).
- [x] A measured claim says machine and renderer: pixel values are quoted only as Forward+ on this Mac; B32 says it is a 1920-pixel-wide frame.
- [x] What the film does not claim is stated: B33 says nothing was measured; B31 does not run an infinite loop; the Lab cannot show the missing-`shader_type` error, so the film cites the documentation.
- [x] Every refusal on screen is the engine's own words, from a run (`evidence/planning-checks/logs/`).
- [x] Payoff uses every earlier idea together: the 14-line `breathe` file has a header, two globals, a function with a signature and a return, a swizzle, a constructor, vector arithmetic and a built-in function.
- [x] Scaffolded handoff: the Your Turn prompt asks for a type for every expression and a one-sentence summary; the two checks are the viewer's own (say a line's type; run the shader).
- [x] Standalone: no reference to any other film, book or course (lint).
- [x] No number on any viewer-facing surface that numbers a film or a part.

## Risks for the build (not defects of the layout)

1. **`ShaderLab`, `shader_kit.py` and the capture harness may not exist yet** (`../_godot-shaders-series/COMPONENT-SPECS.md`). Ten beats use `ShaderLab`; B02 and B34 show the whole 14-line file (code layout) because a Manim card at the 32-point floor holds only about 8 lines.
2. **GATE T on the terminal windows.** `CCPlainShell` draws a dark window with small mono text; the lines land before 50 % of each beat. If the gate flags it, use the cream `ClaudeCodeBeat` card with the same lines (stated in each lane's `why`). Ink rings fail the overlap rule: ring with gray.
3. **The opening pulse passes through pale gray** on the cream stage; Gate V samples the 50 % and 85 % frames. Each of the two clips (B01 and B40) needs its own `--time-origin` from its own measured audio (`CAPTURE-PLAN.md`, C01a and C01b). One origin cannot serve both beats (the best common value leaves the wave at 0.79).
4. **Even-width renders only** for B32 (`CAPTURE-PLAN.md`, C10): at some odd widths one column of the "equals" picture lights.
5. **Type width.** Menlo at Manim size 32 is about 0.25 unit per character (12.4 units usable, so about 49 characters). The squeezed line of B07 is 48 characters and fills the width; B39's widest line is 45. Measured with Manim 0.20.1, no rendering.
6. **Two film-specific helpers** (`lab_window`, a type-tag helper) are listed in `SHOTLIST.md` and `BUILD-PROMPT.md`.
7. **Pace.** The longest beats are B01 (47 words), B09 and B10 (45), then B11, B17, B33 and B35 (44); none is over 48. If the voice runs long, trim B01 or B09 first. The cut line in `ACTS.md` removes about 47 seconds.
8. **Words to listen for** at the voice check: "G L S L", "U V", "R G B A", "S T P Q", "swizzling", "vec two/three/four", "sampler two D", "bool", "const", "varying", "ternary", "in out", "G L frag color", "float of i", "pi" (said "pie"). Phonemes were checked offline with Kokoro's phonemizer (no audio was made); all read as intended.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py godot-shader-language` → no errors, no warnings at the time of writing. The lint's minutes figure counts every spoken word at 0.34 s plus 4 s, bookends included, so it errs long on purpose; the real length is known after the voice is generated.
