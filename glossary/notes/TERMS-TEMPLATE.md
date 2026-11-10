# Terminology-deck template (proposed, from the Camera pilot)

Pilot file: `18 Camera.html` (19 slides, 15 animated, 65 steps). It covers every row of the glossary's "Camera" table: 22 rows, 20 distinct ideas (two ideas appear under two names: "Dolly in/out" and "Dolly in / dolly out"; "Smoothing (damping)" and "Smoothing/damping").

Source of terms: `interview-bank/csye-7270-building-virtual-environments/GLOSSARY-jargon-midterm.md`. The glossary is broader than the chapter text. That is fine for these decks, and each term carries a tag that says which it is.

> **File names (2026-11-10):** the final decks are named `NN Title.html` (01 to 25, course order, listed in `glossary/decks/`). Sections below written earlier use planned names such as `Terms - X.html`; those are superseded.

## How a deck is built

Copy the shell of the Computational Skepticism review decks (`info-7375-computational-skepticism-for-ai/decks/review/`): CSS variables, Lato, Northeastern palette, 1920 x 1080 stage scaled to the window, nav chrome, thumbnails (G), notes (N), fullscreen (F), print, keyboard, touch swipe, D3 7.9.0 from jsdelivr. Colours and type were checked against `brutalist.art/brands/neu.md` (NU Red `#C8102E`, black, greys, Lato). Do not restyle. The only additions to the review-deck shell are the same four the review template lists (24 px `.source` and `.evidence`, pointer cursor on `.diagram`, click advances a step).

The step engine is unchanged: each slide has `data-build="name"`, `BUILDS[name] = {steps, render}`, and `render(el, k, anim)` draws the whole slide at step `k`, animating only what step `k` adds. `anim` is false under `prefers-reduced-motion`, so every step then draws instantly. Thumbnails and print render step 99, which is clamped to the last step.

Per deck, replace only the slides and the render functions. The Camera deck's own code is the starting point: helpers `run` (time-driven tween on a group), `kf` (keyframes through values), `entries` (glossary column), `pairStrip`, `cone`/`camBody`/`inView` (camera diagrams), and `T` (the term table).

## Slide types, in order

| # | Type | Count in Camera | What it holds |
|---|------|-----------------|---------------|
| 1 | Opening (dark) | 1 | Deck name, "CSYE 7270 · Terminology" |
| 2 | Map | 1 | The terms in 4 to 6 groups, one group per click, with what each group changes |
| 3 | Section (red) | 3 | Part names. Keep one per 3 to 5 term slides |
| 4 | Term slide | 11 | Related terms that are alternatives to tell apart share one slide. 1 to 3 steps, one per term or per idea |
| 5 | Look-alike pairs | 1 | Four pairs students mix up, one per click, both sides animated side by side |
| 6 | Say it exactly | 1 | Five vague requests, each turned into an exact instruction on click, with a graph of what the instruction does |
| 7 | Checklist | 1 | Six checks, drawn one per click |

**Term slide frame** (fixed positions in a 1400 x 700 SVG). Left, x 0 to 760, y 0 to 590: the animation. Right, x 800 to 1400: one glossary entry per step (term name, tag, glossary meaning word for word, alias line if the glossary has a second name). Under the entries, a 28 px caption with the computed numbers for the current step. Bottom, y 598 to 700: "TELL THESE APART" with two boxes. Below the SVG: `Source: CSYE 7270 midterm glossary, "<Section>" section` in 24 px.

## Tags

Every term carries one tag in the entry: **in the book text** (filled) or **glossary only** (outline). A term is "in the book text" only if the chapters (`chapters/*.md`) both use it and explain it. Method: grep every chapter for the term and for its common spellings, read each hit in context, and decide. A passing use is not an explanation. Do not guess. For Camera: 0 terms are "in the book text", 20 of 20 are "glossary only". The only hits were passing: `Camera2D` as a node in Chapter 1 and Chapter 0; "screen shake" in Chapter 0 ("add screen shake later and one of these scores will shake with the world", no definition); "camera zoom" in Chapter 10 (a tween example); "zooms out" in Chapter 2 (mipmaps); "the camera follows" in Chapter 5 (a demo). Those are listed in the slide notes, not tagged. Bear can overrule any tag.

## Animation rules

1. Every concept slide has a D3 animation that shows what the term does. No decoration. If the term cannot be shown, say so in the notes and use the closest true picture.
2. Compute every number in code from stated inputs (projection, angles, smoothing, decay). Nothing typed in by hand except the inputs. Check two or three by hand and list them in the hand-over.
3. Steps by arrow keys, space, button or a click on the stage. Each click adds one idea. A slide replays from step 0 on revisit. Going back draws the earlier step instantly.
4. `prefers-reduced-motion`: `anim` is false and every step draws its final pose. The pane cannot test the OS setting; test on a real machine with it on.
5. Poses that go and return (pan left then right) end on the same pose as the static draw, or show a travel line so the static frame still shows the move.
6. Time-driven motion uses `run(g, ms, fn)`: it draws `fn(0)` at once, then tweens `fn(t)`; with reduced motion it draws `fn(1)`. Precompute simulations (smoothing, shake) at load with a fixed seed so replays match.
7. Text at stage scale is 24 px or larger, everywhere, including SVG labels and the source line. Slide content stays inside 1920 x 1080.
8. Label what the data is, top right: Computed, Simulation, Simulation (seeded), or Conceptual illustration.
9. Plain words. No marketing language.

## Content checklist per deck

1. Every row of the section's glossary table appears, with the glossary's meaning word for word. Rows that repeat an idea under two names are one entry with both names.
2. Count rows covered against rows in the section and report both.
3. Terms that are alternatives share a slide and have a look-alike pair at the bottom.
4. One look-alike pairs slide, one say-it-exactly slide, one closing checklist.
5. Each slide cites its glossary section in 24 px.
6. Each term has a tag, decided by grep.
7. Never open any `4TAs/` folder. Do not edit the glossary. Do not commit, stage, push or publish.

## Checks before a deck goes to Bear

- Open at 1920 wide and at 390 wide. Step through every slide and every step (65 states in Camera).
- No console errors. No text under 24 px. No text outside its SVG. No overlapping text (compare text boxes in screen coordinates; group transforms matter). Source line bottom within 1080.
- Screenshots of every animated slide in its final step, and mid-animation for at least a few.
- Thumbnails (G) render the final state for each slide.

## Proposed plan: every glossary section and the deck it becomes

Rule used: up to 40 terms is one deck (about 0.85 slides per term, so up to about 34 slides); 41 to 60 terms are two decks split by topic inside the section; a section under 16 terms merges into its neighbour. This cap is Bear's call. Term counts are table rows, counted from the glossary: 939 rows in total. The "Wrong word, right word" section has no table, only four bullets; they fold into the closing deck.

| Glossary section(s) | Terms | Deck | Decks | Note |
|---|---|---|---|---|
| Camera | 22 | 18 Camera.html | 1 | Built (pilot) |
| Animation | 23 | Terms - Animation.html | 1 |  |
| Game movement and collision | 19 | Terms - Movement.html | 1 |  |
| Shaders and materials, Shader foundations | 40 | Terms - Shaders.html | 1 | merge: 15 is too small alone |
| Shader verification | 29 | 13 Shader verification.html | 1 |  |
| Textures and materials | 43 | Terms - Textures and materials (A, B).html | 2 | 43: split in two |
| Particles | 35 | Terms - Particles.html | 1 |  |
| Animation foundations | 35 | 16 Animation foundations.html | 1 |  |
| Animation and interaction | 40 | 17 Animation and interaction.html | 1 |  |
| Audio and triggers | 33 | Terms - Audio and triggers.html | 1 |  |
| Engine vocabulary | 48 | Terms - Engine vocabulary (A, B).html | 2 | 48: split in two |
| Toolchain | 30 | Terms - Toolchain.html | 1 |  |
| Scenes, nodes and signals | 35 | Terms - Scenes, nodes and signals.html | 1 |  |
| 2D art and sound assets | 48 | Terms - 2D art and sound (A, B).html | 2 | 48: split in two |
| 3D assets and Blender | 44 | Terms - 3D assets and Blender (A, B).html | 2 | 44: split in two |
| Collision and physics | 37 | Terms - Collision and physics.html | 1 |  |
| Game design documents | 38 | 10 Game design documents.html | 1 |  |
| Profiling and optimization | 40 | Terms - Profiling and optimization.html | 1 |  |
| Game AI | 58 | Terms - Game AI (A, B).html | 2 | 58: split in two |
| Agent workflow terms: MCP fundamentals | 58 | Terms - Agent MCP (A, B).html | 2 | 58: split in two |
| Agent workflow terms: Unity workflows | 35 | Terms - Agent Unity.html | 1 |  |
| Agent workflow terms: Unreal workflows | 43 | Terms - Agent Unreal (A, B).html | 2 | 43: split in two |
| Agent workflow terms: security | 48 | Terms - Agent security (A, B).html | 2 | 48: split in two |
| Agent workflow terms: verification | 39 | Terms - Agent verification.html | 1 |  |
| Compress, read and tell apart (sets k01 to k03), Wrong word, right word | 19 | Terms - Say it exactly.html | 1 | merge: 19 rows plus the four wrong-word bullets; becomes the course-wide closing deck |
| **Total** | **939** | | **33** | |

Build order suggestion: Camera (done), then Animation, Game movement and collision, Shaders, so the three nearest the midterm come first. Each deck takes one session.

## Open decisions for Bear

- Slide size: Camera runs 19 slides for 22 rows. A 40-row deck would run about 34 slides. Keep the 40-term cap, or lower it to 30 (about 46 decks)?
- Section slides (3 of 19): keep for rhythm, or drop.
- Tags: with 0 "in the book text" for Camera, the tag is uniform there. It will carry more information in the chapters-heavy sections (Shaders, Particles, Audio).
- The glossary's "Wrong word, right word" bullet "Pan closer is a dolly in" fits the Camera deck's say-it-exactly slide. It is not used yet, since it is not a table row.

## Revision 2026-11-10: what is built, and what the Riot series adds

**Built (4 decks):** Camera (22 glossary rows), Game design A (22 terms), B (19), C (19). Slide counts 19, 14, 14, 15. Game design decks use three tags: in the book text, in the glossary, video only. Their source lists are in `GAME-DESIGN-TERMS-source-crashcourse.md`.

**New reference:** `RIOT-SERIES-TERMS.md` lists 171 terms from Riot's "So You Wanna Make Games??" episodes 1 to 9 (art, character art, environment art, technical art, character animation, VFX, sound, UI). 43 are already in the glossary (some only partly), 128 are not. I spot-checked eight of the terms against the transcripts and all eight are there. Captions are garbled in places; uncertain terms are marked in the file.

**Use in the plan:** when a glossary-section deck is built, also cover that section's Riot terms (episode-to-deck map is inside the file). Tag them "video only" unless the glossary or chapters have them.
- Animation foundations: Ep 6 character animation.
- Particles: Ep 7 VFX.
- Audio and triggers: Ep 8 sound design (or its own deck, see below).
- Textures and materials, shader decks, 3D assets and Blender: Ep 3, 4, 5.

**New decks the Riot series suggests (not in the 33-deck plan; Bear to decide):**
1. Art principles and concept art (Ep 1, 2; about 30 terms): clarity, visual hierarchy, contrast, constraints, mood board.
2. Character and environment art workflow (Ep 3, 4, 5; about 25 terms): proxy, high-poly sculpt, texture baking, block-out, modular kit, naming conventions.
3. Sound design (Ep 8; about 14 terms): frequency, envelope, EQ, Foley, sound library. Could fold into Audio and triggers.
4. UI and UX design (Ep 9; about 20 terms): the glossary has no UI section.

Left to build: about 36 (the 32 glossary decks other than Camera and Game design documents, plus up to 4 new). The Game design documents section (38 rows) is only partly covered by Game design A to C (Mechanic, Player verb, Core loop, Level design, Goal); its remaining rows (GDD, Pitch, Brief and others) still need a deck or a merge into A.

## Build order (proposed 2026-11-10, follows the Canvas assignment sequence)

Done: Game design A, B, C, Camera (Camera belongs with Assignments 1 and 7 for the camera in Walker Jumpman).

| # | Assignment (due) | Deck |
|---|---|---|
| 1 | A4 GDD (Oct 19) | Game design D: GDD terms (GDD, pitch, brief and the rest of the glossary's Game design documents section) |
| 2 | A1 Walker Jumpman (Sep 24) | Toolchain |
| 3 | A1 | Engine vocabulary A |
| 4 | A1 | Engine vocabulary B |
| 5 | A1 | Scenes, nodes and signals |
| 6 | A1 | Game movement and collision |
| 7 | A1 | Collision and physics |
| 8 | A2 Art, sound, music (Oct 7) | 2D art and sound assets A (with Riot Ep 2, 3 art terms) |
| 9 | A2 | 2D art and sound assets B |
| 10 | A3 Blender (Oct 15) | 3D assets and Blender A |
| 11 | A3 | 3D assets and Blender B |
| 12 | A5 Shaders (Nov 1) | Shaders (Shaders and materials + Shader foundations) |
| 13 | A5 | Textures and materials (with Riot Ep 4, 5) |
| 14 | A5 | Shader verification |
| 15 | A6 Particles (Nov 8) | Particles (with Riot Ep 7 VFX) |
| 16 | A7 Animation (Nov 15) | Animation |
| 17 | A7 | Animation foundations (with Riot Ep 6) |
| 18 | A7 | Animation and interaction |
| 19 | A2 / A7 | Audio and triggers (with Riot Ep 8) |
| 20 | A8 Pitch film (Nov 22) | Optional: Art principles and concept art (Riot Ep 1, 2) |
| 21 | A9 Game AI (Dec 12) | Game AI A |
| 22 | A9 | Game AI B |
| 23 | Final (Dec 20) | Profiling and optimization |
| 24 to 33 | Final | Agent workflow decks (MCP A, B; Unity; Unreal A, B; security A, B; verification), then Game design review deck if wanted |

If current students need help first, move 16 to 18 to the front: Assignment 7 is due Nov 15.

## Build order, revised by Bear (2026-11-10): overview decks, updated with Camera as its own topic

Replaces the 33-deck order above. Terms are the important ones, chosen by what the chapters and assignments use. Sections not named (Audio and triggers, Profiling, the detailed Collision and physics section, the agent workflow sections) wait. The Godot editor interface is taught inside topic 2, so there is no separate Godot interface deck.

| # | Topic | Decks | Status |
|---|---|---|---|
| 1 | Game design | A, B, C | Built |
| 2 | Walker and Godot: important terms and using Godot | Walker and the toolchain; Godot editor and scenes | Built |
| 3 | Art | 2D art and sound assets; Art principles and concept art | Built |
| 4 | Blender: important terms and using Blender | Blender interface and modeling; Blender to Godot | Built |
| 5 | Game design document, the full thing | Game design document | Built |
| 6 | Shaders | Shader foundations; Materials and textures; Shader verification | Built |
| 7 | Particles and VFX | Particles and VFX | Built |
| 8 | Animation | Animation principles; Animation foundations; Animation and interaction | Built |
| 9 | Camera (camera motion matters for understanding animation and film) | Camera | Built, do not rebuild |
| 10 | Game AI | Game AI perception and pathfinding; Game AI decisions and systems | Built |
| 11 | How to make a walkthrough film | Walkthrough film | Built |
| 12 | How to make a trailer for your game | Game trailer | Built |
| 13 | The differences between Godot, Unity and Unreal | Godot Unity Unreal | Built |
| 14 | The Unity editor interface | Unity editor | Built |
| 15 | The Unreal editor interface | Unreal editor | Built |


## Progress log
- 2026-11-10: Deck 2a BUILT: `04 Walker and the toolchain.html` (14 slides, 13 animated, 26 terms; 22 tagged in the book text, 4 glossary only; 60 steps checked at 1920 and 390). Next: deck 2b, Godot editor, scenes, nodes, signals and movement.
