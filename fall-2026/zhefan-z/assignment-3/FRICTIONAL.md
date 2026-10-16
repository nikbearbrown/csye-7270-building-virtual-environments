# FRICTIONAL — Assignment 3

## 2026-10-09 — Copying the Assignment 2 project into assignment-3

**What happened**
- The project `walker-magic-zhefan` was copied into `walker-magic-zhefan/` here from branch `zhefan-z/assignment-2` at `946f1f1`, using `git archive` written to a temporary tar file outside the repository and then extracted with `tar -xf` (commit `249647b`). The copy was checked before committing: 227 files and 30,015,318 bytes, the same as the tracked project on that branch; nothing over 25 MB; no `.godot/`, caches, media or Blender backups; and `git write-tree` for the new folder gave tree ID `aab78206197db6c0b3149b95d313ff1cc84d0d40`, the same as the Assignment 2 folder, so the copy is byte-for-byte identical.
- The Assignment 2 submission docs (`README.md`, `SUBMISSION.md`, `TODO.md`, `HANDOFF.md`, `FRICTIONAL.md`, `TEST-REPORT.md`, `CHANGE-BRIEF.md` and `youtube/`) were moved into `walker-magic-zhefan/docs/a2/` with `git mv`. Every move is an exact rename (content unchanged), and the `youtube/` tree ID is the same before and after. Also added: `docs/.gdignore`, so Godot skips `docs/`; a dated block in the project `.gitignore` for the moved film folders; and `docs/README.md`, a note explaining the copies.
- Nothing on branch `zhefan-z/assignment-2` or under `fall-2026/zhefan-z/assignment-2/` was changed; that branch still points to `946f1f1` locally and on origin.

**Claude Code's mistake**
- Claude Code wrote the new note to `docs/a2/README.md` and so overwrote the Assignment 2 README it had just moved to that same path, because it did not check the target path first. It found this before committing, restored the original from git (blob `fc1c4fe`) and confirmed the staged file matched that blob, so nothing was lost. The note went to `docs/README.md` instead.

**My own decisions**
- Create the assignment-3 folder ourselves, because the instructor's folder was not present.
- Keep the Assignment 2 branch, PR and folder read-only.
- My standing rule that committed docs only get dated additions, never rewrites.

**Suggested by Claude (claude.ai chat), approved by me**
- Keep `ASSIGNMENT-3.txt` and my untracked Assignment 2 film working files out of git through `.git/info/exclude`.
- Copy the project with `git archive` into the new path only, instead of `git checkout zhefan-z/assignment-2 -- <path>`, which would have duplicated the Assignment 2 files in this PR.
- Write the archive to a temporary file instead of piping it into `tar`, because a PowerShell pipeline can corrupt binary data.
- Sort the docs into game docs that stay and Assignment 2 submission docs that move to `docs/a2/`.
- Applying my rule here: leave the stale mentions in `CONCEPT.md` and `SOURCES.md` unedited.

**Proposed by Claude Code, approved by me**
- Place the note at `docs/README.md` and keep its line about `design/…` paths (Claude Code's proposal; Claude in my claude.ai chat recommended accepting it).
- Copy everything exactly; put `CHANGE-BRIEF.md` with the moved docs; add `docs/.gdignore`, the `.gitignore` entries and the note. The per-file sorting of the two groups was also Claude Code's proposal.

**Claude Code's work**
- Ran the git commands and every check listed above.
- Searched the project for references to the moved paths and reported what would break. The Assignment 2 reel scripts find the project by their own position (`scripts/common.py`), so they would look in the wrong folder after the move (left unchanged, not meant to run). The project `.gitignore` film entries only matched a top-level `youtube/` (fixed with the dated block). The `../FRICTIONAL.md` link in the old stub no longer reaches the Assignment 2 log (explained in the note). It also found that `youtube/.gdignore` moves with the folder, so Godot still ignores it.
- Proposed `CHANGE-BRIEF.md` for the moved group, and drafted the note's wording, including the line about `design/…` paths.

## 2026-10-08 — Reading the assignment and choosing the assets (retrospective, written 2026-10-14)

> Organised by Claude (claude.ai chat) from my chat decisions; reviewed by me.

**What I wanted:** to understand Assignment 3 and pick three assets my game can actually use.

**My own decisions**
- Visual direction for the semester game: 2D pixel character in a 3D environment, like Octopath Traveler (HD-2D). The fireball is one attack method; the content leans toward RPG exploration without heavy levelling; exact gameplay still open.
- Three assets: rock (a roadblock the player jumps over, box collision later), crystal (decoration, deep cold blue), treasure chest (appears at the exit after a cleared level, warm on purpose).
- The mage counts as 1.45 m tall. Size tolerance ±0.02 m.
- I refined the Assignment 2 palette pillar: fire is still the only warmth, but warmth can also mark what fire makes safe, such as a rest point with the chest and later a campfire.

**Suggested by Claude (claude.ai chat), approved or modified by me**
- The first sizes (rock 1.0 × 0.8 × 0.7, crystal 0.35 × 0.35 × 0.6, chest 0.8 × 0.5 × 0.6 m), the shape breakdowns, the triangle budgets and the draft failure cases.
- Rejected: a 3D character with a 2D background; it would discard my sprites and need rigging, which this assignment rules out. My Assignment 2 cave background image is not an asset here: it is a generated 2D image, not geometry I built.

## 2026-10-09 — Instructor answer on the a3 tag

The assignment asks for an `a3` git tag, but this semester we submit through the shared course repo, where tags are repo-wide. I asked in class; the instructor said not to add a tag. I identify the submitted version by commit SHA, branch `zhefan-z/assignment-3` and the PR instead.

## 2026-10-14 — MCP setup and connection (setup part retrospective)

**What I did before today:** uv was already on my computer from earlier Unity-related work, so I did not need to install it. I installed the MCP by following the prompts, and it worked the first time. (My words, translated from Chinese.) That first registration used the README's plain line; the assignment's telemetry line was tried later and failed, as below.

**After a power loss Blender would not start**, with the Windows error "the application's side-by-side configuration is incorrect". Some of Blender's files were missing; I restored them, and Blender started again. (My words, translated from Chinese.)

**Connection test.** Claude (claude.ai chat) pointed out that Blender's default scene is the same for everyone, so Claude could report it from memory without calling the tool. On its suggestion I renamed the cube to `ConnectionTest` and set its X location to 1.23 by hand; Claude Code's `get_scene_info` then reported `ConnectionTest` at (1.23, 0.0, 0.0), so the connection was real.

**What differed from the assignment's instructions**
- My server had been registered with the README's plain line, so `DISABLE_TELEMETRY=true` was not set (the add-on itself reported telemetry consent false).
- The assignment's line `claude mcp add -e DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender` failed on my machine with `Invalid environment variable format: blender`, because `-e` takes several values. Claude Code found the working order: `claude mcp add -s user blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender==2.1.9`.
- Claude Code found that an unpinned `uvx mcp-for-blender` re-resolves from PyPI on later runs (a dependency had already moved from 2.15.0 to 2.16.0). I decided to pin the server to 2.1.9 so its tool names cannot change mid-assignment.
- Blender is 5.2.2 LTS, not the chapter's 5.1.2. The server's after-install message names the add-on 'Interface: Blender MCP' and the button 'Start MCP Server'; in my Blender the sidebar tab reads 'MCP for Blender'.
- The add-on reports a `drain_human_activity` capability, which suggests it can send my own actions in Blender back to the server. I left telemetry off.
- One tool call failed with WinError 10053 (connection dropped); the retry worked.

## 2026-10-14 — Learning the window and committing the brief

I measured the shapes myself in Scene Statistics (my readings are in CHANGE-BRIEF.md and BLENDER-NOTES.md): a default UV sphere is 960 triangles, almost twice the course limit. I also saw that an ico sphere with a 1 m radius measures 1.79 × 1.70 × 2.00 m, not 2 × 2 × 2, so sizes must be checked from dimensions; this became failure case 8. Only the rock colours were sampled by Claude Code from my Assignment 2 cave tiles; the crystal and chest colours were proposed by Claude in my claude.ai chat and approved by me. I approved the lit-rock colours #343539 and #797069 instead of the near-black main fill, because a 3D material is shaded again by the light. The brief was committed and pushed before any building (c75176a).

## 2026-10-14 — Building the Rock

- Claude Code proposed the steps; I approved, including its own proposals of roughness 0.9 and turning the two base stones (Rock_A and Rock_B) so a flat face rests on the floor; the top stone is tilted and does not touch the floor.
- First build: correct numbers, but it read as three separate stones, and the final fit had stretched it X 1.19 and Y 1.12 (outside your own predicted ±10%). Claude Code found the cause: `get_scene_info` overstates the size of rotated parts.
- I looked in the viewport and agreed, and asked for Revision 1: parts overlapping as one mass, sized from real vertex bounds, fit factors within 0.95–1.05. Result: fit factors 1.000; the top notch gone; a 0.066 m gap at the floor remained.
- My decision after looking from low angles: accept the gap as a known limitation (at the base, in shadow at game camera height, and the planned box collider covers it).
- The exported `rock.glb` was read outside Blender: one node, Y up, 1.0 × 0.7 × 0.8 in glTF axes, 60 triangles, colours as in Blender. Commit 33ac9b2.

## 2026-10-14 — Building the Crystal and my hand edit

- Claude (claude.ai chat) suggested making my hand edit on the crystal before the join, while the cones were still separate objects. I agreed.
- My first three attempts did not register: Claude Code re-measured each time and saw no change. Its first suggestions were a cancelled or undone rotation and the far-out view; only after the third attempt did it conclude my edits were going to a different Blender. My screenshot showed the same Blender, and it corrected itself. The rotation was probably cancelled.
- Fourth attempt: I selected Crystal_Short_B and typed rotation Z = 20 in the sidebar, then Enter. The title bar showed `*`, and the re-measure showed Z −2.54° → 20.00°.
- What this taught me (my words, translated from Chinese): typing the number directly into the sidebar is the most reliable way, and only when the title bar shows `*` has the change really been made.
- My edit narrowed the crystal to 0.323 m, 0.027 m under the brief. I chose Claude Code's option 1: lengthen Short_B along its own axis (×1.2125) and keep my rotation. Final: 0.35 × 0.35 × 0.60 m, fit factors 1.000, 30 triangles.
- I started a new Blender file before Claude Code had finished: `crystal.blend` had been saved, but the export then failed (`KeyError: Crystal`) because my session no longer held the crystal. Claude Code checked the saved file in a separate windowless Blender (SHA-256 unchanged), and exported `crystal.glb` from it headlessly (`export_crystal.py`). Commit 90547ca.

## 2026-10-14 — Building the Treasure chest

- 5 parts, joined: 0.8 × 0.5 × 0.6 m, 76 triangles as predicted. The lid's true top is at 0.600 m with a flat top face. The body/lid split came out 0.376 + 0.224 m instead of the brief's 0.35 + 0.25; the total height is unchanged (recorded as a dated revision in CHANGE-BRIEF.md).
- Claude Code reported that fully metallic gold read dark olive in Blender's preview. Claude (claude.ai chat) explained that a metal shows mostly reflections and suggested metallic 0.3 / roughness 0.5; I approved.
- `chest.glb` read outside Blender: the lock reaches +Z 0.25, so the Blender −Y front became +Z, as the brief predicted. Commit fd1dc48.

## 2026-10-14 — Godot import, prop room and check

- Headless import: exit 0, three `.glb.import` files, no other file changed.
- Scene `res://showcase3d/prop_room.tscn` and check `res://tests/test_a3_assets.gd`, both written by Claude Code. The check passes 22 of 22. Claude Code also showed it can fail: with the rock's brief width changed to 1.1 in a scratch copy, it reported one failure and exit 1.
- My look (see TEST-REPORT.md): upright, on the floor, closed undersides; fixes for the grey background, the floor edges and the mage turning into a line from the side.
- When I opened the project in the Godot editor, the editor changed files I had not touched: `project.godot`, and the import setting of `mage_idle.png`, which it switched to VRAM compression because the sprite is now used in 3D. Claude Code restored `project.godot` and set `detect_3d/compress_to=0` so the 2D sprite stays lossless (1bacec8). Assignment 2's branch and folder were confirmed untouched (946f1f1).
- Commit 4f4b880.

## Human and AI contributions (this assignment)
- **Mine:** the asset choices and their roles, the 1.45 m scale, the palette rule refinement, every approval and rejection above, the Blender interface session and its measurements, the hand edit, the looks in Blender and Godot, accepting the rock's floor gap, and the decision to pin the MCP server.
- **Claude (claude.ai chat):** first size and budget proposals, the connection test idea, the order of work, the colour suggestions, the metallic fix, and drafting these documents from the session records.
- **Claude Code:** all Blender code through the MCP, the exports, the glTF reads outside Blender, the Godot scene and check script, git operations, and the errors listed in TEST-REPORT.md ("What Claude got wrong").

## 2026-10-15 — The explainer film (drafted by Claude Code from its session records; reviewed by me)

Most of this ran on the evening of 2026-10-14; the film was finished and checked on 2026-10-15.

- **Plan.** Claude Code read the Brutalist `godot-gamedev` skill, the `walker` bookends and the capture contract, and proposed a 23-beat sheet and script; I approved them, the title, the B04 prompt excerpt, Claude Code's labelled look renders and listing the Assignment 2 files as out of scope.
- **Capture.** Three `git archive` copies of `8d8895c` outside the repository: a snapshot (never run, for the checker), a reference copy (headless check and `.glb` read) and a capture copy (3840×2160 viewport and a camera harness only). After a headless dry run, a probe (21:19, 3.5 s) and the take run-01 (21:21:44–21:22:38, 12 s, a scripted camera orbit of `prop_room.tscn`) were recorded with Godot's Movie Maker while I left the computer alone. Both passed the harness checks (one light, props at y = 0, the mage on Y-billboard).
- **Build.** Kokoro `am_onyx` narration for 22 beats; cards from my screenshots (labelled "My screenshot") and from Claude Code's MCP look renders (labelled as Claude Code's); the Remotion scenes; `./art godot-gamedev --check` and `./art godot-waikthrough --check` both PASS.
- **Two refused final runs, both on B01.** The hesitant-writer beat's two-word correction was never applied in the first render, because the component matches single words only; it became one word ("look" → "size"), with "also" added to keep the beat at least 9 s. The first `./art final` was then refused by Gate V for underfill (21% of the safe area): I approved four lines at a larger size. The second was refused at B01's midpoint (51%, minimum 55%) at size 170; at 190 the third run passed: Gate V 46 frames, 0 BLOCKER, 0 MAJOR.
- **Five wording changes after my review:** B01 in four lines; B03 "Before any build prompt"; B19 "Each was caught by checking, not by trust."; B20 adds "drafted the build prompts"; the B16 label names the capture copy's 3840×2160 viewport. Only B03, B19 and B20 were re-voiced. Earlier, before my review, Claude Code had changed B10 ("Line 134 then asks"), B21's prompt wording and the spoken spelling of the commit; all are listed in SCRIPT.md.
- **Claude Code's mistakes here:** it estimated the script at about 650 words (it was about 1,000, so the film runs 5:42, not 4–5 minutes); the first card drafts had a black inset (wrong crop coordinates) and Chinese characters drawn as boxes in one label, both fixed before rendering; the B01 phrase correction above.
- **Master:** 342.2 s, 34,357,326 bytes, SHA-256 `5d3d8a1ed0708f3763ba398f4f99d1c619e91b93a4bd169a5140ac4afcadc7f7`. I watched and listened to the whole final export, then uploaded it to Google Drive renamed `csye7270-a3-zhefan-z-walker-magic-3d-assets.mp4` and tested the link in a private window.

Correction (2026-10-15): in the Rock entry, 'your own predicted ±10%' means Claude Code's prediction, not mine.
Note (2026-10-15): the build prompts for each asset were drafted by Claude in my claude.ai chat, adapted from the assignment's template; I sent them to Claude Code.
