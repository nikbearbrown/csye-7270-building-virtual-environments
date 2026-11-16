# BUILD-LOG.md — claude-liam-lecture-first-shaders-materials-godot

## What this is, what was found
The LAYOUT of a film of Assignment 5 ("Shaders, Materials, and the Godot Shading Language") for CSYE 7270, narrated by Liam in for Bear (Kokoro `am_onyx`, channel claude-liam, @NikBearBrown), laid out with the `lecture` skill on 2026-10-16 by a Cowork session. It follows the assignment in ten acts and ends with the recap, the Your Turn prompt and the channel outro. **Nothing is voiced, rendered, built, staged or published yet.** The next stage is `BUILD-PROMPT.md` (Claude Code, launched from `books/`).

What matters before anyone builds or watches it:
- **The example is an AI-written INSTRUCTOR EXAMPLE.** The shaders, materials, tests and notes of the worked example (`walker-claude/`) were written by an AI (Codex) under Bear's direction. The film says so (B06, B07) and every example picture carries the on-screen chip `instructor example · A. I.-written`. Nothing is called hand-written, student work, or a Claude Code session.
- **No Claude Code session ran for the example, so none is shown.** The assignment's prompts (the CLAUDE.md prompt, the driver prompt, the audit prompt, the `claude -p` commands) appear as the assignment's own text, labelled "documented, not run".
- **The real tools were run for this film.** Godot 4.7.2 ran the assignment's own wrapper, three mutations on the real files, the hint experiment and the pad values in BOTH renderers, and a probe of the 3-5 byte colour shortfall (`evidence/runs/`, `captures/forward-plus/`). Real Godot editor frames (49, scripted, `captures/editor/`) stand in wherever the subject is the editor. Every number on screen is read from a log or json (`evidence/verify_claims.py`: 99 checks, 0 failed); pixel numbers carry their renderer.
- **Nobody has heard or seen any of it.** No audio exists, so no scene has been paced against real speech.

Lane histogram: 69 Manim, 6 Remotion (CCPlainShell: B20, B21, B22, B48, B58, B71), 6 bookends. 81 beats (BOPEN, BIDEA, BDEFS, 75 body beats B01-B74 plus B55B, BVDT, BHTF, BOUT); 79 SHOW / 2 CARD. Estimated runtime 957 s (15.9 min) at 3.2 words per second. Acts: Opening 45 s, I 92, II 114, III 66, IV 107, V 52, VI 100, VII 103, VIII 40, IX 119, X 80, Closing 39.

## Request and interpretation
Bear: "I do the assignments in my class in the Walker Claude directory. Look at the two YouTube videos ('Your First 3D Game Assets with Claude and Blender', 'Building the Claude Mascot with Claude Code and the Blender MCP') ... Use these as models. Make a film using materials from the Walker Claude directory ... for Assignment 5: Shaders, Materials, and the Godot Shading Language", with the full assignment text pasted. Interpreted as the `lecture` skill (the whole assignment as ONE act-structured film), Liam in for Bear, free build with no approval gate, stop at the master, never publish.
The suggested slug `claude-liam-lecture-assignment-five-shaders-materials` was renamed `claude-liam-lecture-first-shaders-materials-godot` (no number in a slug or title; the sibling film is `claude-liam-lecture-first-3d-assets-blender-mcp`). The course is named in BOPEN and BIDEA only.
The series line on the title card and in BOPEN is "CSYE 7270 Virtual Environments" (30 characters). The course's full title, "CSYE 7270 Virtual Environments and Real-Time 3D" (47 characters, still in `metadata.course`), does not fit the card's 42-character copy budget. The sibling film was staged for the playlist "Virtual Environments and Real-Time 3D"; this film's `metadata.playlist` is the short form, so check the name before `art post` (see Open items).

## How it was laid out
- Narration, the sheet and the act map by me (`narration.py`, `make_sheet.py`, `ACTS.md`, `LANE-PLAN.md`, `BUILDER-BRIEF.md`); one evidence pass produced the real runs (`evidence/`, `EVIDENCE-INDEX.md`) and another recorded the editor frames; seven builders wrote the scenes (`scenes_act1.py`..`scenes_act10.py`, `lanes/actN.json`, `factcheck/actN.md`); `assemble_scenes.py` pastes them with `kit.py` into `scenes.py`; `build_docs.py` writes SHOTLIST / FACTCHECK / CHECKS-REPORT.
- Every body beat auditioned two lanes; the pick and runner-up are in `SHOTLIST.md`. Tools are shown as themselves: real Godot editor frames and engine renders, the real terminal, code from the real files with their real line numbers. Where the real Shader Editor strips fail GATE T at 4K (light-on-dark glyph halos), the same lines are drawn on the stage from the file's own text, and the real editor frames are used elsewhere (B49).

## Gates run at the layout stage (no audio, no render)
- Gate L (`beat_lint`) clean; build_safety clean; Gate A (static) and Gate W on all 69 Manim classes: 0 failures (`evidence/GATES-STATIC.md`).
- Gate F: `factcheck_check.py` clean, 482 rows, 81 beats covered, 0 uncovered, verdicts PASS / CORRECTED / EXEMPT only, zero OPEN (`FACTCHECK.md`). The numbers table: `evidence/NUMBERS-CHECK.md`, 99 checks, 0 failed.
- Gate B (`manim_layout_audit --curve-strict`) over every class: `evidence/GATE-B.md`.
- Builders also ran real 3840x2160 GATE T + Gate V frames (50% and 85%, one class at a time) where a dark capture or a dense picture made it worth it: scripts or results for Acts I (scripts only), II, IV, V, VI and IX are under `evidence/actN/` (`gate4k*`, `GATE-RUN-4K.txt`, `gateT_4k.out`, `gate-4k.log`). All were clean at 50% except "underfill" on B60, B64 and B68 (phased beats; `sparse: true` waives it). The recorded Act IX run still shows two 85% rows that GATE T does not sample (B63 label overlap, B64 mean contrast 4.19:1) and predates the last edit of `scenes_act9.py` (13:00): re-check B63 and B64 first. Acts III, VII, VIII, X and the six Remotion beats have no 4K run yet; they have Gate A / W / B only.
- Every class was also re-rendered at low quality on 2026-10-16 (after the last scene edit) and the final-state frames of all 69 were looked at: no overlap, clipped or empty picture found (`_qc/stills/<Class>.png`, five frames each). Their `[pace]` lines (clip content versus estimated narration) are all under the target.
- `pace_report.py` and Gate V / GATE T / loudness / master / SRT cannot run until the voice and the 4K render exist (see BUILD-PROMPT).

## Corrections made because the real runs or the files disagreed with my first text or the assignment
- **The example has no hint predictions on record.** The assignment asks for predictions before the experiment; the example recorded none. The film shows the assignment's formula (137/188/225) plus the measurement in both renderers, labelled "predicted, not measured" / "re-run for this film". It never says the example predicted anything.
- **The hint result depends on the renderer.** Forward+ measured 64/128/192 and 137/188/225; Compatibility measured 64/128/192 for both quads (B40-B42, B63). Stated with its renderer.
- **The example's pad predictions fit Compatibility only**, within 5 byte values; on Forward+ the same shader misses by tens of byte values (the largest: blue at full activation on the dark stripe, 250 predicted, 181 measured; B63). The 3-5 byte Compatibility shortfall has no known mechanism: the constant-ALBEDO probe shows it is not the mix arithmetic, the stripe, a uniform or the hint. The film says "not explained".
- **Vertex ALBEDO:** my first draft said the colour line could be moved into `vertex()`. It does not compile (`Unknown identifier in expression: 'ALBEDO'`, recorded in `evidence/act7/vertex_albedo_check.log`); B52 shows the real log and then the varying route (values at the corners only).
- **The Import dock** hides the Normal Map row for a Lossless texture, so B35 shows `compress/normal_map=2` from the `.import` file, not a dock row; the Inspector groups are Surface and Pattern, not "Shader Parameters" (the assignment's wording is not repeated).
- **The example's mutations were in memory** (test mode flags); the film shows the real-file re-run mutations (deleted semicolon: 4 failures; renamed uniform: 1 failure while the driver test still passes 10/10; hint removed: 2 failures). Counts match the example's own `mutation-results.json`.
- **The example's brief is shorter than the assignment's** (B09 shows the example's real brief and the real git log of its commit; the assignment's own requirements are presented as the framework, not attributed to the example).
- **No Use External, no normal map in the game's materials, no WorldEnvironment in the example's hint fixture:** the example's specimens are plain boxes made in code and its fixture builds the picture in memory. B46-B47 and B68 say so; the re-run fixture adds an explicit WorldEnvironment (Linear, exposure 1.0) and the film says that too.
- **B32 shows render samples 16 / 34 / 83** (the DURATION line's samples while charging), not the whole-test counts (294 / 409 / 726).
- **B73 shows surface lines 3-4** with line 4 (`ROUGHNESS` data sampler) as the data line.
- **B71** (clone and verify) has no clone command: the assignment gives none, so none is invented.
- **Lab panel provenance.** `captures/lab/` frames come from an EARLIER take (14 Oct 01:52, scripted input); the panel text there differs from today's `verification.gd`. Every lab frame is tagged "scripted input" and only the sentence "Render and play still need checking." (present in both) is quoted or ringed.
- **Prompts and commands the assignment gives but nobody ran** (B22, B24, B29, B68, B71) carry "documented, not run".
- **Left out, and why** (full table in `ACTS.md`): the required-viewing link, the submission template's field-by-field text, rubric prose beyond the point weights, and "your game, one more layer" (a request for the student's own game, not something the example shows).

## Known gate caveats for the build session (not failures, things to look at first)
- B55 (and B06, B07) use the `claude-code` logo after the clip midpoint; GATE T samples only the 50% frame, and the logo's terracotta mark can trip §8.3 as accent text if it lands early. A toolkit exemption (`STRUCTURAL_TERRACOTTA_PATTERNS`) is Bear's call; do not edit the toolkit.
- B74's late frame (the dark review-panel crop, past the 85% mark) fails a local-contrast check; GATE T samples only the 50% frame, but Gate V samples 85%: look at it in the Gate V result.
- B72's last row ("8 the film") lands at the very end of its narration and the clip has about 3 % to spare (content 10.0 s of 10.31 s): if the real voice is faster than the estimate, `pace_report.py` will call it OVER; shorten the scene's fixed run_times, not the narration.
- B67 has dark-green bands about 47.6 from INK: recheck the midpoint frame after the real render.
- `sparse: true` beats (B35, B37, B49, B60, B64, B68 and some in Act VI) are deliberate: the content is real code or captures, not filler.
- Code soft-wraps as continuation rows with a hook (wrapper line 6, the flag line; `surface` line 12; `standard_generated` lines 4/7/19; hint lines 9/10 in B38, B50, B53). The characters are verbatim; the hook is not part of the code.
- Cues are `until()` character-share cues on ESTIMATED durations. After the audio exists, run `pace_report.py`, and run `retime_cues.py` after every `make_sheet.py` to scale the Remotion cue frames of B20, B21, B22, B48, B58 and B71 by actual / estimated (tested on a copy with simulated durations; see BUILD-PROMPT).

## Mistakes worth not repeating (from this layout stage)
- Gate A needs the code as embedded literals in the scene file; reading it from disk at render time fails the static check.
- `still_remotion.py` hung until it was given the Playwright headless shell (`--browser-executable`); it now passes it.
- A copy of the narration with an unescaped pipe in a fact-check cell breaks the FACTCHECK table (write `\|`); five rows were repaired.
- A renumber of beat ids in the middle of a build desynchronised the lane files and the sheet; rebuilt from `narration.py`. Never renumber after the builders start.
- `_qc/stills/*.png` go stale the moment a scene file is edited: re-run `qstill.py` before judging a still.
- Manim 0.20.1 measured Menlo advances: 20 = 0.15, 22 = 0.20, 24 = 0.20, 28 = 0.25, 32 = 0.25 units per character; Pango trims leading spaces in `Text()` (the kit's `code_block` keeps indentation itself).

## Open items for Bear (nothing is voiced, staged or published)
Before the build (they change the narration): (1) length, about 16 minutes against the 10-14 minute target; candidate cuts by beat and seconds are in `ToDo.md` (B57, B46, B55B, B70, then B65 and B66, which are assignment requirements); (2) the series line "CSYE 7270 Virtual Environments" on the title card versus the playlist name at posting time; (3) pronunciations to listen for.
Any time: (4) a Poly Haven logo (none exists; adding one needs a download and Bear's yes); (5) the `claude-code` logo and GATE T accent-text rule (toolkit exemption is Bear's call); (6) the lab frames are an earlier take; (7) the real Shader Editor strips fail GATE T at 4K, so B50 draws the lines; (8) soft-wrapped code rows; (9) nobody has listened to it or watched it.
Note: `./brutalist.art/art todo` rewrites `ToDo.md` and writes `STATUS.md` / `todo.json`; run before BOPEN's card exists it lists BOPEN as a human slot, which is wrong (the title-card builder makes it).

---

## Build session — 2026-10-16 (Claude Code render pass)

Build ran from `books/` following `BUILD-PROMPT.md`. Three fixes required to pass all gates; no narration, scene design or beat sheet structure changed.

### Fix 1 — B58: windowMargin 24→96, fontSize 25.5→24 (Gate V BLOCKER: edge-bleed)

Gate V (final_frame_check.py, 50% frame) reported BLOCKER on B58: ink pixels detected left of x=89 (title-safe boundary). Root cause: `beat_sheet.json` B58 remotion props had `"windowMargin": 24`, placing the CCPlainShell terminal window at CSS `left: 24px` at the 1920 design width — inside the title-safe zone (x=96). Fix: set `"windowMargin": 96` (window left edge at x=96, the safe boundary) and `"fontSize": 24` (down from 25.5) so the 113-character SCRIPT ERROR lines still fit in the narrower text area (1728px / 14.4px/char = 120 chars). B58 re-rendered with `remotion_scenes.py $R --only B58 --force`; Gate V re-run: clean.

### Fix 2 — B10: qc.contrast_regions added (Gate V MAJOR: low-contrast)

Gate V reported MAJOR on B10: whole-frame ink/cream average too close (sep < 0.30). B10 shows three real game captures (warm sandy background) plus dark INK percentage labels at y_manim≈0.16. The warm captures pulled the whole-frame average close to cream. Fix: added `qc.contrast_regions` to B10 in beat_sheet.json — `[{"label": "activation-labels", "box": [0.15, 0.44, 0.85, 0.56]}]` — to tell Gate V to check ONLY the text-label strip (yn 0.44–0.56) instead of the whole frame. Box geometry: yn=0.44 → y_manim=0.48, below the pad image bottoms (yn≈0.420), so the warm captures are excluded; the percentage labels sit inside the box. First attempt used yn_top=0.40 (y_manim=0.80, above pad bottoms — still included warm pixels, sep=0.28, still MAJOR). Second attempt yn_top=0.44: Gate V PASS, regional sep >> 0.30. Also added `contrast_reason` to document the geometry.

### Fix 3 — BOUT: handle "@NikBearBrown" added to props (bookend_check FAIL)

`bookend_check.py` reads `handle` from BOUT's remotion props in beat_sheet.json and requires `@NikBearBrown`. The BOUT props lacked `"handle"` (ClaudeTitleOutro.tsx hardcodes the handle internally, but the external gate reads beat_sheet). Fix: added `"handle": "@NikBearBrown"` to BOUT remotion props. BOUT re-rendered with `remotion_scenes.py $R --only BOUT --force`; bookend_check: PASS.

### Gate results — build session

| Gate | Result | Note |
|---|---|---|
| Gate L (beat_lint) | PASS | 81 beats clean |
| Gate A (manim_layout_audit) | PASS | 69 Manim classes |
| Gate B (manim_layout_audit --curve-strict) | PASS | |
| Gate F (factcheck_check.py) | PASS | 482 rows, 81 beats, 0 uncovered |
| PROOF GATE (CHECKS-REPORT) | PASS | 81 beats, 1011 s (16.8 min) |
| Gate V (final_frame_check.py) | PASS | 162 frames, BLOCKER 0, MAJOR 0 |
| GATE T (type_check.py) | PASS | |
| Bookend check | PASS | BOPEN, BVDT, BHTF, BOUT all match |
| GATE LOUDNESS | PASS | −24.40 LUFS, TP −2.95 dBTP |
| Pace | PASS | all beats ok, OVER: none |
| Gate W (whisper_check.py) | PASS | no mispronunciations |
| GATE SRT | PASS | 81 cues, 1011 s |
| Master | PASS | 3840×2160, 1012.6 s (16.88 min), 121 MB, silent tail 1.629 s |

BVDT §8.10 advisory: 0.96 ← below 1.00 threshold. This is an ADVISORY (not a gate failure); the single-word recap at the footer is intentional.

### Master

`/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/exports/landscape/claude-liam-lecture-first-shaders-materials-godot.mp4`
3840×2160 · h264 · 1012.6 s (16.88 min) · 121 MB · no beat labels · silent tail 1.629 s

### Open items after build (not blocking)

1. **Remotion version BEHIND**: 4.0.535 installed, 4.0.536 is latest. `./art remotion-upgrade` was run but failed: `npm error EALLOWSCRIPTS — --allow-scripts is not allowed in project-scoped installs`. This is a security restriction in the npm config; the upgrade requires Bear's manual intervention (add entries to the `allowScripts` field in `package.json` or `.npmrc`, then re-run `./art remotion-upgrade`). All gates passed with 4.0.535.
2. **Length**: 16.88 min vs. 10–14 min target. Bear's decision.
3. **Playlist name**: "CSYE 7270 Virtual Environments" on title card vs. actual playlist at posting time.
4. **Lab frames**: B74 lab panel from earlier take (14 Oct 01:52); both takes show "Render and play still need checking."
