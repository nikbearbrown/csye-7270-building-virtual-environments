# Checks report (PROOF GATE): Trigonometry for Shaders

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks for the build, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 40 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: Manim 23, ShaderLab capture 13, Remotion 4 (two docs captures and two code-only ShaderLab cards). Estimated 9.9 minutes, 1,744 words. `lint_series.py` prints no errors and no warnings. The two biggest risks for the build: the amount of Manim (23 scenes, seven film-local objects) and getting paper and screen orientation right in each of them.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 40 | every body beat has a motion that carries its claim (the lane entries say which) |
| HOLD | 0 | no archival photograph is needed |
| CARD | 0 | act titles are labels on each act's first picture; the bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): manim 23 · capture 13 · remotion 4. Acts I and II are paper geometry (triangle, circle, wave), which is Manim's job; Acts III to V are about running shaders, so most of those beats are real renders.

## BEST-BEAT audition (SHOTLIST.md has every row)

Every beat names a runner-up from another lane. The picks that were closest calls: B12 (Manim sweep with the docs credited, against a docs capture of the constants), B18 and B27 (code-only `ShaderLab` card, against `LectureCodeTrace`, which holds about ten lines and a different look), B20 (a Manim flip, against the Vector2 docs capture, which B08 already uses), B34 (Manim walk with a live number, against the angular picture, which B35 shows).

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: triangles on paper, then turning angles into positions).
- [x] FRAMEWORK before the first example: the point `(cos a, sin a)` on a circle is on screen in B06 and B07, before the by-hand example (B10) and the first shader (B16 to B19).
- [x] WORKED EXAMPLES that use the framework: B10 (a point by hand, then the real render lands on it in B19) and B37 (one pixel carried through three operations, then a threshold check).
- [x] FALSIFIABILITY and edge cases, each a full beat: the degrees-for-radians trap (B13), the moon below the middle and why (B19, B20), the oval on a wide shape (B24), the one-argument arc tangent slip (B36), the seam (B34, B35).
- [x] Every term the film teaches is defined on screen where first spoken (labels and captions are in the lane entries: hypotenuse, opposite and adjacent in B02; sine, cosine and tangent in B04; unit circle in B07; radian in B11; `PI`, `TAU` in B12; `length` in B17; `distance` and `COLOR` in B18; `TIME` in B21; uniform in B24 and B38; arc tangent in B32 and B33; seam in B34; `mix` in B35; `texture` in B38; `fract` in B39). BDEFS holds prerequisites only (angle, radian, hypotenuse, vec2, UV).
- [x] Concrete before abstract: a moving triangle before the ratios, a circle before the shader, a render before the code of each effect.
- [x] A measured claim says machine and renderer; scripted values are labelled "scripted" in the clip label (C06, C11, C12); drawings say they are drawings ('on paper', credit lines). The film makes no frame-rate or GPU-time claim.
- [x] The payoff uses every earlier idea together: the orbit with a meteor (B26 to B29), the clock-hand reveal (B37 to B39), the flower (B40).
- [x] SCAFFOLDED viewer task: BHTF gives a prompt to paste and two checks the viewer makes on the result (a lap in about four seconds; clockwise, and negating reverses it), each of which catches a common wrong answer (degrees for radians, a forgotten tau, the wrong direction).
- [x] No source, no verdict: every beat that makes a factual claim carries a source or artifact on screen (a Lab render, a Godot docs page or a credit line to it, or a drawing labelled as a drawing); FACTCHECK.md has 66 rows, zero OPEN.
- [x] Standalone: no reference to any other film, book, course or school (lint). No film number, "part" or "episode" anywhere.

## Risks for the build (not defects of the layout)

1. **Shared pieces.** `ShaderLab`, `shader_kit.py` and the capture harness may not exist yet (`../_godot-shaders-series/COMPONENT-SPECS.md`); Phase 0 of `BUILD-PROMPT.md` checks and builds them. `ShaderLab` needs the layouts `code` and `stack` and a piecewise `--animate` schedule.
2. **Twenty-three Manim scenes.** The heaviest part of the build. They share seven film-local objects (listed in `SHOTLIST.md` and `BUILD-PROMPT.md`), so write those first.
3. **Orientation.** Paper (y up, counterclockwise) in B06 to B15, screen (y down, clockwise) from B16 on, both in B20. A scene drawn with the wrong orientation teaches the wrong direction while looking fine. The prompt says to check every still against its beat's words.
4. **GATE T.** The picture colours are mid-tones on purpose; the terracotta is only dots, thick arcs and rings (never a filled wedge, never text). The angle picture (B35, B36) is teal to amber with no dark field.
5. **Docs screenshots.** B08 and B33 need real captures and coordinates set from them; the quoted sentences were read from the live pages on 2026-10-13 and may be reworded later (BUILD-PROMPT says to re-check FACTCHECK rows 11 and 49 if so).
6. **Pace.** The longest beats are B24 (43 words), B23 (42), and B07, B11 and B40 (41 each). If the voice check runs long, B24 is the one to trim (its cut-line item is the oval limit as a whole).
7. **Pronunciation.** Lowercase `pi` is written on purpose (all-caps PI is read as the letters P, I); `tau`, `fract`, `vec two` and the S O H letters need a listen.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py trigonometry-for-shaders` prints no errors and no warnings (46 beats, 1,752 words by the checker's count, which adds three words per term on the terms card, 10.0 estimated minutes, 40 body beats in five acts of 5, 10, 10, 5 and 10).
