# Assignment 2 - Generate Walker Jumpman's Art, Sound, and Music

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies.

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

**In one paragraph:** you will design your game's look and sound on paper first, then use generative models to make them, then put them in the game without breaking how it plays. The design lives in a storyboard and a character sheet. The generation is logged prompt by prompt, including what you threw away and why. The result is judged in the running game, not in the image folder. Your Frictional log is where the design thinking shows: what you wanted, what the model gave you, and what you decided.

## Your task

Start from **your own Assignment 1 project** (your `walker-` repository). Replace its placeholder presentation with generated art, sound effects, and music, integrated into the actual Godot game. Before generating anything, make a **storyboard** of the play experience and a **character sheet** for your main character. Use them as the specification that your prompts and edits must meet.

This is a new revision of your Assignment 1 game, not a new game. Keep Assignment 1's controls, movement and jump tuning, collider, level geometry, retry, pause, and completion unless you explicitly justify a change and test it. Tag or otherwise identify your Assignment 1 submitted revision so the difference is traceable.

Claude Code assistance is expected. Use your Northeastern access and free or locally run generative models; **no purchased API credits or paid generation service is required**, and paid output earns no bonus. Claude can write code, prompts, and scripts, but it is not itself an image or audio generator: code-drawn or SVG art written by Claude is welcome in your game, and it does not satisfy the generative-model requirement below.

### What counts as a generated asset

Each of the three categories needs **at least one asset in the running game that a generative model produced**:

| Category | Minimum in the running game |
|---|---|
| Art | Your main character's in-game appearance (sprite frames or a sprite sheet) **or** at least two environment assets (background, tiles, hazard, finish marker). |
| Sound effects | At least **four** game events, each with its own sound: jump, landing, failure (hazard or fall), and finish. |
| Music | At least **one** loop that plays during play and repeats without an audible click or gap. |

You may edit any generated output by hand (cleanup, recolor, trim, loop point, slicing into frames, background removal). Record every edit. A model output that you redraw completely is your art, which is fine, and the log must say so.

Walker's asset tools include free local helpers you may use: background removal (`rembg_matting.py`), sheet slicing (`grid_slice.py`), and loop-frame finding (`find_loop_frame.py`). Its image, video, and 3D generation commands call paid services. They are optional and not required.

### Rights and responsible use

- Do not prompt with, or feed in as reference, a named living artist's style, a copyrighted character, a brand, or existing music or recordings.
- Do not clone or imitate a real person's voice. Synthetic voices from a free local text-to-speech model are allowed if you choose to add voice.
- Record each model's name, version, and license or terms of use in `SOURCES.md`. Some open models carry non-commercial or attribution terms. That is acceptable for coursework, and you must state it.
- Never commit API keys or account credentials.

## 1. Predict — design before you generate

Commit these before your first generation. Retain the original versions; add later revisions rather than rewriting the record.

### `STORYBOARD.md` — the play experience, in order

A storyboard shows the key moments of play in sequence: what the player sees, hears, and does. Make **at least six panels**, covering at least: the start screen or spawn, a first jump, a failure and retry, a landing in your Assignment 1 extension, the finish, and one moment you care about. Hand sketches photographed from paper are fine and often faster.

For each panel record:

- **The picture:** a sketch or thumbnail, in `design/storyboard/`.
- **Player action and game state:** what the player is doing, and which existing state the game is in.
- **What the player should see:** the character pose and the environment elements on screen.
- **What the player should hear:** the sound event and the music state (playing, paused, quieter, stopped).
- **Asset IDs:** the asset or assets this panel depends on, matching your asset log.
- **The design reason:** the one thing this moment should communicate to the player.

### `CHARACTER-SHEET.md` — the specification for your character

The character sheet is the contract your generated character must meet. Put the image or images in `design/character/`. Include:

- **Silhouette test:** the character filled solid black at actual in-game size. The starter's logical viewport is 640 × 360; your character must read at that size.
- **Facing:** right-facing and left-facing. Plan to flip one direction at runtime rather than generating both.
- **States:** one pose per state your game shows (for example idle, walk or run, jump, failure, celebrate). Note which poses are single frames and which loop.
- **Collider overlay:** your current collision box drawn over each pose at the same scale, with a note on any art that extends beyond it and why that is fair to the player.
- **Palette:** three to six colors with hex values, checked against your level's background so the character stays visible.
- **Consistency rules:** what must stay identical across every frame (proportions, eye position, outline weight), so you can judge generated frames against it.

### `CHANGE-BRIEF.md` — the plan and the predictions

Add an Assignment 2 section to your existing brief:

- The art style you chose and why it serves your game, in two or three sentences.
- The event-to-sound map: each sound, the exact game event that triggers it, and how you will prevent double triggers.
- Music behavior on pause, failure, retry, and finish.
- What must remain unchanged from Assignment 1.
- **At least three predicted failure cases** and how you will check them. For example: the jump sound fires twice on a held jump; the character's frames drift in proportion from one pose to the next; the music loop clicks at the seam; the new art hides a hazard edge; the game is no longer readable with sound muted.

## 2. Build It — generate against the design

### Generate in inspectable steps

Work from the character sheet and storyboard, not from a blank prompt box. Keep an **asset log** (a table in `SOURCES.md` or a separate `ASSET-LOG.md`) with one row per generation you kept or seriously considered:

| Field | What to record |
|---|---|
| Asset ID | Matches your storyboard and character sheet. |
| Model and version | Where it ran (local or institution-provided) and its license or terms. |
| Prompt and settings | The exact prompt, negative prompt if any, seed, size, duration, and other settings needed to reproduce it. |
| Outcome | Accepted, edited, or rejected, with the reason judged against the sheet or storyboard. |
| Edits | What you changed by hand or with which tool. |
| Where used | The file path in the game and the storyboard panel it serves. |

Keep rejected outputs as small thumbnails or a contact sheet, not full-size files. The rejections are evidence of design judgment, and graders will read them.

Practical guidance:

- For characters, generate one reference image first, check it against the character sheet, then derive every pose from it. Consistency comes from the reference, not from repeating the text prompt.
- Prompt for a solid background color and remove it afterwards. Prompting for "transparent" usually produces a drawn checkerboard.
- Scale art to in-game size before judging it. Detail that disappears at 640 × 360 is not detail.
- For sound effects, keep them short and trim silence from the front so they feel immediate.
- For music, generate longer than you need and cut a loop at a bar boundary. Check the seam by listening to at least three repetitions.
- Deliver game audio as **OGG or WAV**. The course keeps MP3 and MP4 files out of GitHub, and Godot imports OGG with loop settings directly.

### Integrate into the game without changing how it plays

- **Art:** replace or supplement the drawing in `godot/features/player/player.gd` and `godot/game/session.gd`. Keep the collider and movement tuning from Assignment 1. Make sure the sprite flips with facing, changes with state, and lines up with the collider while standing, moving, and in the air. For pixel art, check the texture import filter so frames do not blur.
- **Sound:** trigger each effect from the existing state change that already represents the event. Sound must never decide game state; a missing or muted sound must not change what happens.
- **Music:** loop it, and implement the pause and finish behavior you predicted. Provide a way to mute music and effects, separately if you can.
- **Readability without sound:** the game must remain understandable muted, as it was in Assignment 1.

Ask Claude to propose a plan before editing, then implement one bounded change at a time:

```text
Read my README, CHANGE-BRIEF.md, STORYBOARD.md, and CHARACTER-SHEET.md.
Use Walker's brief → build → playtest → inspect → revise workflow.
Locate the character drawing, collider, state changes for jump, landing,
failure, and finish, and the relevant tests. Propose the smallest plan
to integrate my generated character, my four sound events, and my
music loop. Do not edit yet. After I approve a step, implement only that
step, show the diff, run the existing checks, and tell me what still
requires human listening or playtesting.
```

This is a prompt to Claude Code, not an installed shell command. You decide whether to accept the plan.

## 3. Use It — play it, listen to it, compare it to the design

Play the game yourself with normal controls, with sound on and then muted. Record actual results in `TEST-REPORT.md`, with the source revision and engine version:

| Check | Evidence to collect |
|---|---|
| Unchanged behavior | Assignment 1's mechanics and keyboard checks still pass; controls, tuning, collider, retry, pause, and completion behave as before. |
| Character against the sheet | In-game screenshots of each state, left- and right-facing, beside the character sheet poses; any visual/collision mismatch noted. |
| Storyboard against the game | Each storyboard panel beside an in-game screenshot of the same moment; differences listed and explained. |
| Sound events | Each of the four events produces exactly one sound per occurrence, including a held jump, repeated retries, and a hazard touched twice in one attempt. |
| Music | The loop repeats without a click or gap; pause, failure, retry, and finish behave as predicted. |
| Muted play | The level can still be completed and understood with all sound muted. |
| Automated checks | Commands and results, plus at least one **new** automated check for your audio or art integration (for example, counting sound triggers per event during a scripted route). |

Do not delete a failing assertion or weaken an expected result merely to obtain a green report.

Include **at least one documented inspect-and-revise cycle** driven by an observation: a regenerated asset, a changed prompt, a moved loop point, a palette change after the silhouette test. If another person plays or listens, record their actual feedback; do not invent a playtester. Your own playtest is required, and an automated route does not replace it.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-gamedev`** workflow with the **`walker`** modifier. This film explains how your game's art and audio were made and wired in. Ask Claude Code to read the installed skill instructions and follow them. If your checkout lacks the skill, request the course-provided version before proceeding.

Make **one** landscape film that:

1. Identifies your Assignment 1 starting revision and what this revision adds.
2. Traces **one asset from design to game**: storyboard panel or character sheet → prompt → raw output → edits → in-game result.
3. Shows the character in the running game in at least two states, and the four sound events occurring in real play.
4. Includes **at least one clearly labeled segment where the game's own audio is audible without narration over it**. Check the skill's audio policy first; if it silences captured gameplay by default, ask for the course-provided method rather than dubbing sounds in afterwards.
5. Explains at least one cause-and-effect connection between a source change and what the player sees or hears.
6. States what you tested, what remains uncertain, one concrete next improvement, the human and AI contributions, **which model produced which asset**, and the game revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label reconstructed interface views, scripted-input captures, and held frames accurately. Do not present a raw generation as in-game footage.

Follow the skill's native **4K landscape** rendering and quality checks, then watch and listen to the final export. Duration should follow the explanation; there is no minimum runtime. A second film, a vertical Short, paid media generation, and public YouTube publication are **not required**.

### Post the version on GitHub

Your submitted source includes:

- The modified Godot project and its **used** generated assets (OGG/WAV/PNG), within the size limits; exclude caches and credentials.
- `README.md`: project name, Assignment 1 revision, starter credit, engine version, run instructions, controls including mute, changes, known limitations, and final-film link.
- `STORYBOARD.md`, `CHARACTER-SHEET.md` and their images, `CHANGE-BRIEF.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md` with the asset log, and rejected-output thumbnails.
- The film's beat sheet, script/prompts, and relevant evidence/coverage records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Use commit messages that describe a meaningful change and its purpose or check. For example: `Add jump and landing sounds; verify one trigger per jump`.

## 5. Verify and submit to Canvas

Run the project from a fresh copy of the revision you are submitting and confirm every used asset is present. Submit a source ZIP of that same GitHub revision, excluding caches, credentials, and large media, together with `SUBMISSION.md`:

```text
Assignment: Assignment 2 - Generate Walker Jumpman's Art, Sound, and Music
Student:
Project name:
GitHub repository/folder URL:
Assignment 1 revision this builds on:
Submitted commit SHA:
Game-source revision shown in the film:
Godot version and operating system:
Generative models used (name, version, where run, license):
Final film URL and filename:
Final film SHA-256:
Summary of my changes:
Known limitations:
```

It is fine to render from a game-source commit and then add the film documentation in a final commit. Identify both revisions and verify that the final commit does not change the demonstrated game source. Canvas, GitHub, and the film must refer to the same submitted work.

## Rubric — 100 points

| Component | Points |
|---|---:|
| Implementation and explanation | 60 |
| Frictional — honest log of the design thinking | 10 |
| GitHub version posting matching Canvas | 10 |
| Relative Quartile | 20 |
| **Total** | **100** |

### Implementation and explanation — 60 points

| Criterion | Points |
|---|---:|
| Design before generation: storyboard with at least six complete panels (5); character sheet with silhouette test, facing, states, collider overlay, palette, and consistency rules (5); both committed before the first generation (2). | 12 |
| Generated art in the game: meets the character sheet or storyboard it was made for (6); correct facing, states, and visual/collision alignment with Assignment 1 behavior preserved (5); reproducible asset log with accepted and rejected outputs (3). | 14 |
| Generated sound and music in the game: four event sounds, each firing once per event (6); a seamless music loop with the predicted pause/finish behavior (4); mute works and the game stays readable muted (2); reproducible asset log entries (2). | 14 |
| Verification: Assignment 1 checks still pass, plus one new automated check (4); human playtest with sound on and muted, storyboard-versus-game comparison (3); an evidence-based revision and an honest limitation (3). | 10 |
| Brutalist explainer: accurate design-to-game trace of one asset (4); real gameplay with audible game audio (3); models, contributions, and limits stated (2); readable, audible final film using the required workflow (1). | 10 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive assets do not repair an incorrect explanation or a broken game.

### Frictional — honest log of the design thinking — 10 points

In `FRICTIONAL.md`, keep a dated log of the design as it happened. This assignment's log should show the thinking, not only the steps: what you were trying to make the player see or hear, what you asked the model for, what came back, and what you decided.

- **3 points:** Specific, honest accounts of attempts: the prompt or setting you tried, what you expected, and what the model actually produced.
- **3 points:** Your judgment in response: why you accepted, edited, or rejected an output against the storyboard or character sheet, what you changed next, and what you still have not resolved.
- **2 points:** Explicit human/AI contributions, separating Claude's contributions (code, prompts, plans) from the generative models' outputs and from your own decisions and edits.
- **2 points:** Traceability to asset-log rows, commits, prompts, screenshots, or tests.

An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If a generation was usable on the first try, say so and explain how you judged it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or taste.

### GitHub version posting matching Canvas — 10 points

- **4 points:** Required, accessible game source, used assets, and documentation are actually posted.
- **3 points:** Canvas identifies the exact submitted commit and the Assignment 1 revision, with matching source files and clear run instructions.
- **3 points:** Accessible film link, identified media version, and film source/evidence correspond to the submitted game.

### Relative Quartile — 20 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.

Meeting the stated criteria can earn the other **80 points**; it does not guarantee these **20 points**. A coherent, readable game with modest assets outranks a gallery of striking images that do not fit the game. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.

## You must be able to explain it

Use `SOURCES.md` to credit the starter, your Assignment 1 revision, every generative model and its terms, collaborators, and tools. Describe what AI contributed to the game code, the prompts, the assets, the script, and the narration, along with what you personally decided, checked, changed, or rejected.

The instructor or a TA may ask you to reproduce an asset from your log, or to explain why you rejected one. Inability to explain reduces points under the relevant criteria. Misrepresenting authorship, provenance, or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.

## Appendix — starting templates

Copy these into your repository and fill them in. They are prompts for your thinking, not forms to pad.

### `STORYBOARD.md` panel

```text
## Panel 3 — First failure
![sketch](design/storyboard/03-first-failure.png)
- Player action and state: runs into the spikes; PLAYING → DYING
- See: failure pose, hazard stays visible, cause message
- Hear: failure sound (SFX-FAIL); music ducks, resumes on retry
- Assets: CHAR-FAIL, SFX-FAIL, MUS-LOOP
- Design reason: the player should know exactly what killed them and want one more try
```

### `CHARACTER-SHEET.md` sections

```text
# Character sheet — <name>
- Concept in one sentence:
- Silhouette at in-game size: design/character/silhouette.png
- Facing: right drawn, left flipped at runtime
- States: idle (loop) · run (loop) · jump (single) · fail (single) · celebrate (loop)
- Collider overlay: design/character/collider.png — art beyond the box and why it is fair:
- Palette: #______ #______ #______ (checked against the level background)
- Consistency rules: same proportions, eye height, outline weight in every frame
```

### `FRICTIONAL.md` entry

```text
## 2026-10-__ — character reference
- Wanted: a character that reads as <idea> at 640 × 360 (sheet: silhouette, palette)
- Asked: <model, version> — prompt "<…>", seed <…> (asset log row CHAR-REF-03)
- Got: <what actually came back>
- Decided: rejected / edited / accepted, because <judged against the sheet>
- Next: <what I changed>
- Human / Claude / model: <who did what>
- Still unresolved:
```
