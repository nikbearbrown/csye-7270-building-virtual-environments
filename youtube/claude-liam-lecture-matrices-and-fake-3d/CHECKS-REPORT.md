# Checks report (PROOF GATE): Matrices and Fake 3D

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 41 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: Manim 22, ShaderLab capture 15, Remotion 4 (docs capture, evidence table, two code traces, one of them on ShaderLab's code layout). Estimated about 10 minutes (the lint's ceiling estimate is 10.2; exact figures in `SCRIPT.md`), about 1,785 spoken words. Risks for the build: the three shared components if no earlier film built them, matrix tables that drop spaces or signs in Manim, and getting the y-down grids right.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 41 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): manim 22 · capture 15 · remotion 4. The router for this film sent the table, grid and arrow beats to Manim (a coordinate system warping, a ring walking down a table), every "what does the engine really do" beat to a real Godot capture, the documentation claim to a browser capture, and the two lists to the table and code components. No lane was chosen for variety; the five-beat run of Manim in Act I is five beats about the same grid.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: "advanced math you can skip" becomes "a saved move").
- [x] The central idea ("a matrix is a saved move: a table that moves points") is shown in motion before it is named in code (B01 hook, B02, B07 to B10), and is the thread of every act.
- [x] Every term the film teaches is defined on screen where first spoken (table, row and column in B02 and B04; identity in B08; cosine and sine in B12; TAU in B13; pivot in B35; origin and VERTEX in B11, B39); BDEFS holds prerequisites only (vector, matrix, vertex, uniform, radian).
- [x] Concrete before abstract: the flip is shown first (B01); the arithmetic is worked on one point before any rule is stated; each table is shown on a real render before it is combined.
- [x] A framework beat comes before the examples: B07 (columns are where the arrows land) is the picture every later table reuses (B12, B15, B28).
- [x] A worked example uses the framework on screen: (5, 6) becomes (23, 34) by rows (B02) and by columns (B07); (30, 20, 1) becomes (130, 20, 1) (B15); the slide times turn product is filled in entry by entry (B20).
- [x] A stress-test beat: the two ways to be wrong give the same plausible answer (B06); the order swap gives two different places (B22); the flip has no perspective and fails for a box (B32, B33).
- [x] A measured claim says machine and renderer (this file and `FACTCHECK.md`); what a demonstration does not show is said aloud (no perspective, no depth: B32, B33; the back is the front mirrored: B29).
- [x] A thing that surprises is demonstrated by a real run (a card with no thickness draws nothing at a quarter turn, B29; the same two tables in two orders, B22).
- [x] Payoff uses every earlier idea together (the door: columns, the flip table, the pivot sandwich and its order, B35 to B41).
- [x] Scaffolded viewer task: BHTF is a prompt to paste with two checks the viewer runs on the result (identity at zero, the hinge edge stays put), each verified (FACTCHECK).
- [x] Standalone: no reference to any other film, book or course (lint); terms the film needs from elsewhere (vertex, uniform, sine and cosine) are taught or defined where needed.
- [x] No film number on any viewer-facing surface (the 3D in the title is a figure, not a count); the voice says the title as "Matrices and Fake Three D" (`SPOKEN_TITLE`).
- [x] Honest limits: scripted sweeps are labelled; the capture is offline and says nothing about frame rate; the fact-check has no OPEN rows (the docs sentence was fetched twice and is proven by a run; screenshot D1 is compared with it at build time).

## Risks for the build (not defects of the layout)

1. **Shared components.** `ShaderLab`, `shader_kit.py` and the capture harness may not exist yet; this film also needs a card scene script and eased breakpoints on top of the harness spec (`BUILD-PROMPT.md`, Phase 0).
2. **Matrix drawings in Manim.** Tables full of small numbers, minus signs and "x" multiplication signs are exactly where a Pango `Text()` drops spaces; LOOK at each still. Every grid points y DOWN.
3. **GATE T and Gate V on captures.** The cards are light on purpose and the terracotta hinge dot is small; the 50 % and 85 % frames of every capture are settled holds by design (`CAPTURE-PLAN.md`); B09 and B14 are sparse by design (declared).
4. **Pace.** The longest beats are B11, B15 and B19 (44 words each); if the voice runs long, trim B11 (drop its middle sentence) before cutting.
5. **tau** may be mispronounced by the voice; the build session reports it.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py matrices-and-fake-3d` prints 0 errors and 0 warnings at the time of writing, after the shared lint's update of 2026-10-13 (uppercase `PI`/`TAU`, code calls with parentheses and unspaced acronyms in narration are errors; the title may carry `3D` when `SPOKEN_TITLE` is set). Nothing was waived: the fact-check has no OPEN row, and no beat is over 44 words.
