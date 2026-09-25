# Assignment 2 - Generate Art, Sound, and Music for Your Game

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies.

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

**In one paragraph:** pick the game you actually want to build. Design its look and sound on paper first, then use generative models to make the art, sound effects, and music, then prove them in a small playable Godot scene. The design lives in a short concept, a storyboard, and a character sheet. The generation is logged prompt by prompt, including what you threw away and why. The result is judged in the running scene, not in the image folder. Your Frictional log is where the design thinking shows: what you wanted, what the model gave you, and what you decided.

## Your task

Choose **the game you want to build this semester**. It can be any genre that fits a small Godot project: a platformer, a top-down adventure, a puzzle game, a shooter, a narrative piece. It does not have to resemble Walker Jumpman. Before generating anything, write a one-page concept, a **storyboard** of the play experience, and a **character sheet** for your main character or main controllable object. Use them as the specification that your prompts and edits must meet.

Then generate the game's art, sound effects, and music, and put them into an **asset slice**: a small playable Godot scene where the player controls the main character, sees it change state, hears the sounds fire on real events, and hears the music loop. The slice is a proof that the assets work together in the engine. It is not the whole game.

Your project name must begin with **`walker-`**, for example `walker-tidepool-maya-k`. Use a new repository or folder for this game. You may start from the [walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) structure, from your Assignment 1 project if this is the game you want, or from an empty Godot 4 project. Credit whatever you started from.

Claude Code assistance is expected. Use your Northeastern access and free or locally run generative models; **no purchased API credits or paid generation service is required**, and paid output earns no bonus. Claude can write code, prompts, and scripts, but it is not itself an image or audio generator: code-drawn or SVG art written by Claude is welcome in your game, and it does not satisfy the generative-model requirement below.

### What counts as a generated asset

Each of the three categories needs **at least one asset in the running slice that a generative model produced**:

| Category | Minimum in the running slice |
|---|---|
| Art | Your main character's in-game appearance in at least two states (sprite frames, a sprite sheet, or a 3D model) **and** at least one environment asset (background, tiles, prop, or hazard). |
| Sound effects | At least **four** events from your game's core loop, each with its own sound. Choose them from your design: for example an action, a success, a failure, and a completion. |
| Music | At least **one** loop that plays during the slice and repeats without an audible click or gap. |

You may edit any generated output by hand (cleanup, recolor, trim, loop point, slicing into frames, background removal). Record every edit. A model output that you redraw completely is your art, which is fine, and the log must say so.

Walker's asset tools include free local helpers you may use: background removal (`rembg_matting.py`), sheet slicing (`grid_slice.py`), and loop-frame finding (`find_loop_frame.py`). Its image, video, and 3D generation commands call paid services. They are optional and not required.

### Rights and responsible use

- Do not prompt with, or feed in as reference, a named living artist's style, a copyrighted character, a brand, or existing music or recordings.
- Do not clone or imitate a real person's voice. Synthetic voices from a free local text-to-speech model are allowed if your game uses voice.
- Record each model's name, version, and license or terms of use in `SOURCES.md`. Some open models carry non-commercial or attribution terms. That is acceptable for coursework, and you must state it.
- Never commit API keys or account credentials.

## 1. Predict — design before you generate

Commit these before your first generation. Retain the original versions; add later revisions rather than rewriting the record.

### `CONCEPT.md` — the game in one page

- **The game in two sentences:** who the player is and what they do.
- **Core loop:** the action the player repeats, what they decide each time, and what they risk.
- **Three or four design pillars:** the experiences every asset must serve. For each, name one visual or sound choice that honors it.
- **Art direction:** the style you chose and why it serves those pillars, in two or three sentences. Include two or three reference notes in words (materials, lighting, era, mood), not other artists' names.
- **Audio direction:** what the sound and music should make the player feel, and when music should change or stop.

Walker's `/gdd` skill can help: `/gdd v1` runs a vision intake and `/gdd v2` drafts pillars. You are responsible for the decisions it records.

### `STORYBOARD.md` — the play experience, in order

A storyboard shows the key moments of play in sequence: what the player sees, hears, and does. Make **at least six panels**, covering at least: the first thing the player sees, the core action, a success, a failure, a moment of recovery or retry, and the end of a play session. Hand sketches photographed from paper are fine and often faster.

Across the whole storyboard:

- **At least three views (shot sizes):** for example a wide or establishing shot of the whole space, a medium shot of the character in action, and a close-up of a face, a hand, a prop, or a key UI element.
- **At least three camera angles:** for example eye level, high angle or bird's-eye, low angle, over-the-shoulder, or a tilted (Dutch) angle.
- **Motion indicated on at least two panels:** arrows for character or object movement, motion lines for speed, and a note for any camera move (pan, zoom, shake, follow).
- **Frame shape:** your choice. **16:9 is recommended**, since that is the shape of most screens and of the course films. Keep one frame shape throughout.

Gameplay panels should show what the game's camera actually shows. The other views and angles can be moments the player sees outside normal play (a title screen, an intro, a cutscene, a transition) or design shots that establish how the world and character should feel. Label which is which.

For each panel record:

- **The picture:** a sketch or thumbnail, in `design/storyboard/`.
- **Shot:** the view (wide, medium, close-up), the angle, any motion or camera move, and whether it is a gameplay view or a design view.
- **Player action:** what the player is doing, and what the game is doing in response.
- **What the player should see:** the character state and the environment elements on screen.
- **What the player should hear:** the sound event and the music state (playing, quieter, changed, stopped).
- **Asset IDs:** the assets this panel depends on, matching your asset log.
- **The design reason:** the one thing this moment should communicate, tied to a pillar.

### `CHARACTER-SHEET.md` — the specification for your main character

If your game has no character, make the sheet for the main thing the player controls (a ship, a cursor creature, a piece). The sheet is the contract your generated assets must meet. Put the images in `design/character/`. Include:

- **Silhouette test:** the character filled solid black at its actual on-screen size in your chosen viewport. It must read at that size.
- **Facing or orientation:** the directions it appears in, and which you will flip or rotate at runtime instead of generating.
- **At least 10 distinct poses** of the same character, drawn or generated from one reference so proportions hold. A full production model sheet is not required. A mirrored copy of a pose does not count as a new pose, and several frames of one loop count once unless they are genuinely different key poses (the contact and passing poses of a walk are two). Label each pose with the game state it serves, and note which poses loop and which play once. Choose poses your game will actually use; the suggestions below are a menu, not a checklist.
- **Collision overlay:** the collision shape you plan to use, drawn over each pose at the same scale, with a note on any art beyond it and why that is fair to the player.
- **Palette:** three to six colors with hex values, checked against your environment so the character stays visible.
- **Consistency rules:** what must stay identical in every frame (proportions, eye position, outline weight, silhouette), so you can judge generated frames against it.

#### Suggested poses

Pick at least 10 that fit your game. For a side-view game, draw them in profile; for top-down or 3D, pick the view the player actually sees.

| Group | Pose | Why a game needs it |
|---|---|---|
| Reference | **Neutral turnaround:** front, side, three-quarter, and back at the same height, with a height bar | Locks proportions; every later pose is checked against it. Counts as one pose. |
| Reference | **Silhouette at game size** | Proves the shape reads before any detail is added. |
| Rest | **Idle** (breathing or blinking) | The pose the player sees most. |
| Rest | **Waiting / bored** (after a few seconds of no input) | Personality at no gameplay cost. |
| Movement | **Walk: contact** and **walk: passing** | The two key poses a walk cycle is built from. |
| Movement | **Run** (leaning forward, longer stride) | Tells the player speed changed. |
| Movement | **Jump anticipation** (crouch) | Makes the jump feel intentional. |
| Movement | **Rising** and **falling** | Lets the player read the arc and time the landing. |
| Movement | **Landing** (squash) | Confirms contact with the ground. |
| Movement | **Climb, swim, crouch, or dash** | Only if your game has that verb. |
| Action | **Core action** (attack, cast, throw, interact, pick up, shoot) | The verb your core loop is built on. |
| Action | **Core action follow-through** | Shows the action happened and when control returns. |
| Reaction | **Hurt / hit** | Tells the player they took damage and from which side. |
| Reaction | **Fail / defeat** | The failure moment in your storyboard. |
| Reaction | **Recover / respawn** | The return to control after failure. |
| Emotion | **Success / celebrate** | The completion moment in your storyboard. |
| Emotion | **Expression row:** neutral, happy, surprised, worried, determined | Portraits for dialogue or UI, if your game has them. Counts as one pose per distinct expression. |
| Props | **Holding the main prop** (tool, weapon, lantern) with a prop callout | Keeps the prop's size and grip consistent. |

A reasonable set for a platformer: turnaround, idle, walk contact, walk passing, run, jump anticipation, rising, falling, landing, hurt, fail, celebrate. For a top-down action game: turnaround, idle, walk, dash, attack, attack follow-through, hurt, defeat, interact, celebrate.

### `CHANGE-BRIEF.md` — the plan and the predictions

- The asset list: every asset the slice needs, with an ID, and which storyboard panel it serves.
- The event-to-sound map: each sound, the exact game event that triggers it, and how you will prevent double triggers.
- Music behavior on pause, failure, success, and the end of the slice.
- **At least three predicted failure cases** and how you will check them. For example: generated frames drift in proportion between poses; a sound fires twice on one event; the music loop clicks at the seam; the character disappears against the background; the slice is unreadable with sound muted.

## 2. Build It — generate against the design

### Generate in inspectable steps

Work from the character sheet and storyboard, not from a blank prompt box. Keep an **asset log** (a table in `SOURCES.md` or a separate `ASSET-LOG.md`) with one row per generation you kept or seriously considered:

| Field | What to record |
|---|---|
| Asset ID | Matches your storyboard and character sheet. |
| Model and version | Where it ran (local or institution-provided) and its license or terms. |
| Prompt and settings | The exact prompt, negative prompt if any, seed, size, duration, and other settings needed to reproduce it. |
| Outcome | Accepted, edited, or rejected, with the reason judged against the sheet, storyboard, or pillars. |
| Edits | What you changed by hand or with which tool. |
| Where used | The file path in the project and the storyboard panel it serves. |

Keep rejected outputs as small thumbnails or a contact sheet, not full-size files. The rejections are evidence of design judgment, and graders will read them.

Practical guidance:

- For characters, generate one reference image first, check it against the character sheet, then derive every pose from it. Consistency comes from the reference, not from repeating the text prompt.
- Prompt for a solid background color and remove it afterwards. Prompting for "transparent" usually produces a drawn checkerboard.
- Scale art to on-screen size before judging it. Detail that disappears at game size is not detail.
- For sound effects, keep them short and trim silence from the front so they feel immediate.
- For music, generate longer than you need and cut a loop at a bar boundary. Check the seam by listening to at least three repetitions.
- Deliver game audio as **OGG or WAV**. The course keeps MP3 and MP4 files out of GitHub, and Godot imports OGG with loop settings directly.

### Build the asset slice in Godot

The slice is one small scene, playable with keyboard or controller:

- **Character:** the player moves the main character, and it visibly changes between at least two states. Facing or orientation follows input. The art lines up with the collision shape you specified.
- **Environment:** at least one generated environment asset is in the scene, and the character stays readable against it.
- **Sound:** each of your four sound events is triggered by a real event in the scene, from the code that already represents that event. Sound must never decide game state; a missing or muted sound must not change what happens.
- **Music:** the loop plays, repeats cleanly, and follows the pause and end behavior you predicted. Provide a way to mute music and effects, separately if you can.
- **Readability without sound:** the slice must remain understandable muted.

For pixel art, check the texture import filter so frames do not blur.

Ask Claude to propose a plan before editing, then implement one bounded change at a time:

```text
Read my CONCEPT.md, STORYBOARD.md, CHARACTER-SHEET.md, and CHANGE-BRIEF.md.
Use Walker's brief → build → playtest → inspect → revise workflow.
Propose the smallest Godot 4 scene that proves my assets: a controllable
character with its states, one environment, my four sound events on real
events, a looping music track, and mute controls. List the files and nodes
you would create. Do not edit yet. After I approve a step, implement only
that step, show the diff, run it, and tell me what still requires human
listening or playtesting.
```

This is a prompt to Claude Code, not an installed shell command. You decide whether to accept the plan.

## 3. Use It — play it, listen to it, compare it to the design

Play the slice yourself with normal controls, with sound on and then muted. Record actual results in `TEST-REPORT.md`, with the source revision and engine version:

| Check | Evidence to collect |
|---|---|
| Startup and controls | The scene runs from a fresh copy; movement and every state change work with the intended input. |
| Character against the sheet | In-engine screenshots of each state and orientation beside the character sheet poses; any mismatch with the collision shape noted. |
| Storyboard against the slice | Each storyboard panel the slice covers, beside an in-engine screenshot of the same moment; differences listed and explained, and panels the slice does not cover named. |
| Sound events | Each of the four events produces exactly one sound per occurrence, including rapid repeats and a held input. |
| Music | The loop repeats without a click or gap; pause and end behave as predicted. |
| Muted play | The slice can still be played and understood with all sound muted. |
| Automated check | At least one automated check you added, for example counting sound triggers per event during a scripted input sequence, with its command and result. |

Do not delete a failing assertion or weaken an expected result merely to obtain a green report.

Include **at least one documented inspect-and-revise cycle** driven by an observation: a regenerated asset, a changed prompt, a moved loop point, a palette change after the silhouette test. If another person plays or listens, record their actual feedback; do not invent a playtester. Your own playtest is required, and an automated input sequence does not replace it.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-gamedev`** workflow with the **`walker`** modifier. This film explains how your game's art and audio were designed, generated, and wired in. Ask Claude Code to read the installed skill instructions and follow them. If your checkout lacks the skill, request the course-provided version before proceeding.

Make **one** landscape film that:

1. Introduces your game concept and its pillars in plain terms.
2. Traces **one asset from design to game**: storyboard panel or character sheet → prompt → raw output → edits → in-engine result.
3. Shows the character in the running slice in at least two states, and the four sound events occurring in real play.
4. Includes **at least one clearly labeled segment where the slice's own audio is audible without narration over it**. Check the skill's audio policy first; if it silences captured gameplay by default, ask for the course-provided method rather than dubbing sounds in afterwards.
5. Explains at least one cause-and-effect connection between a source change and what the player sees or hears.
6. States what you tested, what remains uncertain, one concrete next step toward the full game, the human and AI contributions, **which model produced which asset**, and the source revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label reconstructed interface views, scripted-input captures, and held frames accurately. Do not present a raw generation as in-engine footage.

Follow the skill's native **4K landscape** rendering and quality checks, then watch and listen to the final export. Duration should follow the explanation; there is no minimum runtime. A second film, a vertical Short, paid media generation, and public YouTube publication are **not required**.

### Post the version on GitHub

Your submitted source includes:

- The Godot project for the slice and its **used** generated assets (OGG/WAV/PNG or model files), within the size limits; exclude caches and credentials.
- `README.md`: project name, what you started from and its credit, engine version, run instructions, controls including mute, what the slice demonstrates, known limitations, and final-film link.
- `CONCEPT.md`, `STORYBOARD.md`, `CHARACTER-SHEET.md` and their images, `CHANGE-BRIEF.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md` with the asset log, and rejected-output thumbnails.
- The film's beat sheet, script/prompts, and relevant evidence/coverage records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Use commit messages that describe a meaningful change and its purpose or check. For example: `Add hurt and win sounds; verify one trigger per event`.

## 5. Verify and submit to Canvas

Run the project from a fresh copy of the revision you are submitting and confirm every used asset is present. Submit a source ZIP of that same GitHub revision, excluding caches, credentials, and large media, together with `SUBMISSION.md`:

```text
Assignment: Assignment 2 - Generate Art, Sound, and Music for Your Game
Student:
Project name:
Game concept in one sentence:
GitHub repository/folder URL:
Started from (walker-jumpman, my Assignment 1 project, or an empty project):
Submitted commit SHA:
Source revision shown in the film:
Godot version and operating system:
Generative models used (name, version, where run, license):
Final film URL and filename:
Final film SHA-256:
Summary of my work:
Known limitations:
```

It is fine to render from a source commit and then add the film documentation in a final commit. Identify both revisions and verify that the final commit does not change the demonstrated source. Canvas, GitHub, and the film must refer to the same submitted work.

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
| Design before generation: a concept with core loop, pillars, and art and audio direction (3); a storyboard with at least six complete panels using at least three views, three angles, and motion on at least two panels (4); a character sheet with at least 10 distinct labeled poses, silhouette test, orientation, collision overlay, palette, and consistency rules (4); all committed before the first generation (1). | 12 |
| Generated art in the slice: meets the character sheet, storyboard, and pillars it was made for (6); readable states, correct orientation, and sensible art/collision alignment (5); reproducible asset log with accepted and rejected outputs (3). | 14 |
| Generated sound and music in the slice: four event sounds, each firing once per event (6); a seamless music loop with the predicted pause and end behavior (4); mute works and the slice stays readable muted (2); reproducible asset log entries (2). | 14 |
| Verification: the slice runs from a fresh copy, plus one automated check you added (4); human playtest with sound on and muted, storyboard-versus-slice comparison (3); an evidence-based revision and an honest limitation (3). | 10 |
| Brutalist explainer: accurate design-to-game trace of one asset (4); real play with audible slice audio (3); models, contributions, and limits stated (2); readable, audible final film using the required workflow (1). | 10 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive assets do not repair an incorrect explanation or a broken slice.

### Frictional — honest log of the design thinking — 10 points

In `FRICTIONAL.md`, keep a dated log of the design as it happened. This assignment's log should show the thinking, not only the steps: what you were trying to make the player see or hear, what you asked the model for, what came back, and what you decided.

- **3 points:** Specific, honest accounts of attempts: the prompt or setting you tried, what you expected, and what the model actually produced.
- **3 points:** Your judgment in response: why you accepted, edited, or rejected an output against the storyboard, character sheet, or pillars, what you changed next, and what you still have not resolved.
- **2 points:** Explicit human/AI contributions, separating Claude's contributions (code, prompts, plans) from the generative models' outputs and from your own decisions and edits.
- **2 points:** Traceability to asset-log rows, commits, prompts, screenshots, or tests.

An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If a generation was usable on the first try, say so and explain how you judged it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or taste.

### GitHub version posting matching Canvas — 10 points

- **4 points:** Required, accessible source, used assets, and documentation are actually posted.
- **3 points:** Canvas identifies the exact submitted commit, with matching source files and clear run instructions.
- **3 points:** Accessible film link, identified media version, and film source/evidence correspond to the submitted slice.

### Relative Quartile — 20 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.

Meeting the stated criteria can earn the other **80 points**; it does not guarantee these **20 points**. A coherent, readable slice with modest assets that clearly serve the design outranks a gallery of striking images that do not fit together. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.

## You must be able to explain it

Use `SOURCES.md` to credit what you started from, every generative model and its terms, collaborators, and tools. Describe what AI contributed to the code, the prompts, the assets, the script, and the narration, along with what you personally decided, checked, changed, or rejected.

The instructor or a TA may ask you to reproduce an asset from your log, or to explain why you rejected one. Inability to explain reduces points under the relevant criteria. Misrepresenting authorship, provenance, or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.

## Appendix — starting templates

Copy these into your repository and fill them in. They are prompts for your thinking, not forms to pad.

### `STORYBOARD.md` panel

```text
## Panel 4 — First failure
![sketch](design/storyboard/04-first-failure.png)
- Shot: medium · eye level · gameplay view · motion: fall arrow down the gap, camera shake on impact
- Player action: misjudges the gap and falls; the game resets to the last safe spot
- See: hurt pose, the cause stays visible, a short message
- Hear: failure sound (SFX-FAIL); music dips, returns on retry
- Assets: CHAR-HURT, ENV-GAP, SFX-FAIL, MUS-LOOP
- Design reason (pillar "every failure teaches"): the player should know why and want one more try
```

### `CHARACTER-SHEET.md` sections

```text
# Character sheet — <name>
- Concept in one sentence:
- Silhouette at on-screen size: design/character/silhouette.png
- Orientation: right drawn, left flipped at runtime
- Reference: design/character/turnaround.png (front, side, three-quarter, back, height bar)
- Poses (at least 10, each labeled with its game state):
  1. idle (loop)            6. rising (single)
  2. walk contact (loop)    7. falling (single)
  3. walk passing (loop)    8. landing (single)
  4. run (loop)             9. hurt (single)
  5. jump anticipation      10. celebrate (loop)
- Collision overlay: design/character/collision.png — art beyond the shape and why it is fair:
- Palette: #______ #______ #______ (checked against the environment)
- Consistency rules: same proportions, eye height, outline weight in every frame
```

### `FRICTIONAL.md` entry

```text
## 2026-10-__ — character reference
- Wanted: a character that reads as <idea> at on-screen size (sheet: silhouette, palette)
- Asked: <model, version> — prompt "<…>", seed <…> (asset log row CHAR-REF-03)
- Got: <what actually came back>
- Decided: rejected / edited / accepted, because <judged against the sheet or a pillar>
- Next: <what I changed>
- Human / Claude / model: <who did what>
- Still unresolved:
```
