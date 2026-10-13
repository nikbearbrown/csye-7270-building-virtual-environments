# Conducting records: walker-jumpman starter and walker-jumpman-clawd

**What this is.** The real record of what the human asked for, what the AI did, and what was checked. It is evidence for film 1, "Conducting AI for Games". Every quote is exact, with file:line. (Written by the evidence subagent; saved here by the main session.)

**What it found.**
- The records (written by the AI) are unusually candid. They record four machine-found failures in the starter, two capture takes the harness marked PASS or exit-0 that the AI then rejected, and three production errors.
- No record contains a human finding. Every human play-feel judgment is still pending.

**Sources.**
- **C** = /Users/bear/Documents/CoWork/bear-textbooks/books/walker-jumpman-clawd/
- **S** = /Users/bear/Documents/CoWork/bear-textbooks/books/walker/games/walker-jumpman/

The path given in the brief, /Users/bear/Documents/CoWork/bear-textbooks/books/walker-jumpman/, does not exist. S is its own git repo (origin github.com/nikbearbrown/walker-jumpman, HEAD 9387542, which is Clawd's baseline commit). C's copies of these files are byte-identical to S's: BUILD-REPORT, DESIGN-REVIEW, PLAYTEST-PLAN, GAME-BRIEF, GDD, DESIGN-STATUS, evidence/build-manifest.json. So C file:line equals S file:line for those files.

**Who wrote the records.** The AI. C/FRICTIONAL.md:71–72 says: "AI implemented, captured, tested, wrote and rendered this iteration." The "Human contribution" entries are the AI's account of what Bear did.

## (1) The change brief (C/CHANGE-BRIEF.md, 2026-09-11)

**What the human asked for:**
- :9–10: "Bear wants the player to be a coding agent, represented by Clawd. Eventually, mini-goals will represent completed tasks and the final goal a full agentic loop."
- :12: "First inspect the character in the existing level, then decide the next change."
- C/FRICTIONAL.md:9–11: "Bear chose Clawd, named the separate project walker-jumpman-clawd, supplied its GitHub destination, and asked for one change at a time."

**What was out of scope:**
- :11: "**Those task goals, new hazards, and the level extension are not implemented now.**"
- :4–5: "This iteration is not a completed Assignment 1 submission: the required level extension is later."
- :25–27: "Change drawing and presentation selection only. Preserve the player physics function, tuning, collision shape, level JSON, hazards, camera, input bindings, and recovery."

**The three predicted failures:**
1. :16–17: "The wide Clawd silhouette may overhang the unchanged collision box. An arm can overlap a hazard without contact; inspect rather than silently retune."
2. :18–19: "Playing a decorative jump loop on a physically jumping body could create two apparent jump arcs. The airborne pose must not add a second displacement."
3. :20–21: "A library of 18 animations might be mistaken for 18 implemented abilities. Separate the gallery from actual gameplay and label the difference."

**What happened to each prediction:**
- **Prediction 1 came true and was left open.** FRICTIONAL.md:59–63: "the broad arms can extend beyond the left world boundary, and the character can pass in front of world labels … readability and collision fairness are questions for Bear's next play session." C/README.md:23–24: "that tradeoff needs human inspection."
- **Prediction 2 was resolved by design.** FRICTIONAL.md:17–18: "physics supplies the airborne trajectory. Hold the mascot's apex pose instead of adding the gallery animation's second jump arc."
- **Prediction 3 was handled by separating and labelling.** C/README.md:20: "This is a **separate visual gallery, not 18 new gameplay abilities**."

**The division of labour** (CHANGE-BRIEF.md:42–43): "AI: code, inspection, test execution, documentation, narrated film production. Human: intent, scope, art judgment, play-feel review, and the next decision."

## (2) Where a claim or a machine PASS was weaker than it looked

**A. The starter's first 25-check run found 4 failures** (S/evidence/mechanics-1789078423.29998.json)
- The receipt has "failures": 4 (:4). FAIL status at :149 respawn, :156 manual-restart-not-death, :164 twenty-retries (observed deaths 22), and :189 complete-real-route (deaths 1, 145 ticks).
- **The check:** the automated mechanics suite.
- **The explanation**, BUILD-REPORT.md:19: "stale Area2D contacts after teleporting to spawn created a second death, and the first route lacked a safe landing between a hazard jump and a gap … The jump tuning and acceptance tolerances were not weakened."
- **What happened next:** the next run passed 25/25 (mechanics-1789078494.18347.json), 71 seconds later (created_at 22:13:43Z, then 22:14:54Z). The failed receipt is retained and tracked in git.
- No record shows the AI claiming "done" before this run. The failure was caught by the check itself.

**B. The gallery-two capture take: the harness said PASS, the AI rejected it**
- capture/gallery-two-receipt.json:4 says "frames": 343 and :8 says "status": "PASS". The process record shows exit_code 0.
- Path: C/youtube/claude-liam-walker-jumpman-clawd-walkthrough/capture/
- FRICTIONAL.md:39–44: "one 18-second gallery take contained 343 saved frames instead of the expected 540. Its driver counted process updates while render callbacks could be throttled. The early receipt's PASS is insufficient; the take is rejected for the film and retained."
- **The check:** the saved frame count compared with the expected 540.
- **What happened next:** the harness was revised to "advance the display clock per rendered frame and require 600 saved frames for 20 seconds" (:42–44). It was re-recorded as gallery-one-v2, gallery-two-v2 and gallery-three-v2, 600 frames each.
- The original 540-frame gallery-one, gallery-three and inspector takes, each marked PASS, were also superseded. The evidence/ copies now point to the v2 and v3 takes.

**C. inspector-v2: exit code 0, no receipt**
- inspector-v2-process.json:16 says "exit_code": 0, and :11 shows --quit-after 2400.
- There is no inspector-v2-receipt.json. Only 416 frames are on disk, against the 600 required.
- FRICTIONAL.md:48–49: "the first revised inspector stopped at its process limit without a completion receipt. Exit code zero did not establish success."
- **What happened next** (:50–53): the take was "Rejected … retained its partial frames/logs. Increased only the diagnostic harness's bounded process allowance". inspector-v3 used --quit-after 9600 (inspector-v3-process.json:11) and produced 600 frames, PASS (inspector-v3-receipt.json:4, :8).

**D. A production-script error**
- FRICTIONAL.md:33–36: "the film-authoring script initially had two malformed dictionary entries … Python's syntax check rejected it before execution. Added the missing `value` keys and reran successfully."

**E. A visual pilot failure**
- FRICTIONAL.md:54–58: "the title-card correction used a multi-word trigger that the existing component's word matcher did not recognize. The first render left the wrong sentence on screen."
- **The check:** visual inspection of the render.
- **What happened next:** the trigger was changed to one word, a fresh render was forced, and the correction was re-inspected.

**F. A publication verification miss**
- FRICTIONAL.md:85–88: "The first immediate playlist verification did not yet see the new entry … reconciled it without a duplicate upload or playlist insertion. Added bounded read-only verification retries and an insertion-attempt guard to the publisher."

**G. Checks narrower than the words around them**
- **"Physics function byte-identical"** (evidence/clawd/build-manifest.json:36; FRICTIONAL.md:25–26).
  - The check, scripts/clawd-build.cjs:7–8, slices player.gd from `func _physics_process(` to the next `\nfunc ` and compares only that slice. The whole player.gd did change: 33 lines in the diff, and its hash differs between the S and C manifests.
  - The automated invariant check covers the physics function plus tuning.gd, first_steps.json and hud.gd (clawd-build.cjs:9). Collision shape, camera, input bindings and recovery, also listed in CHANGE-BRIEF:25–27, are not in that script.
  - `git diff 9387542 HEAD -- godot` shows main.tscn unchanged. project.godot changes only config/name. session.gd gains one 8-line read-only method, player_animation_context().
- **Capture receipts** say "game_source": "unmodified main.tscn and dependencies", while player.gd and session.gd differ from the starter. The receipts add "source_worktree": "Clawd modifications, exact build_id is authoritative". That wording is ambiguous, not false.
- **"AI visual review complete"** (CLAWD-STATUS.json:17). The walkthrough QC.md:3 says: "Reviewed 2026-09-11 by the AI production agent, not a human playtester."
- **Starter DESIGN-STATUS.json:59–60** cites mechanics-1789078842 and keyboard-1789078680. evidence/build-manifest.json cites the later mechanics-1789079935 and keyboard-1789079926. Both pairs pass; the status file was simply not updated to the newest receipts.

**H. Stale statements in the public files**
- BUILD-REPORT.md:37 says: "no export download, Web package, repository push, or game publication occurred". Both repos now have GitHub origins with main...origin/main. This was true when written.
- C/README.md:109 and S/README.md:43 say "The original `/Users/bear/walker-jumpman` stays untouched". That path does not exist on disk today.

## (3) The numbers, with sources

**Starter mechanics**
- 25 checks. The first run had 21 PASS and 4 FAIL, and 71 seconds later the next run had 25 PASS (mechanics-1789078423.29998.json, mechanics-1789078494.18347.json).
- There are 5 mechanics receipts in all: 4 from the starter and 1 from Clawd (1789103433, 2026-09-11T05:10:33Z). Every run after the first passed 25/25.

**Keyboard checks**
- 9 checks, 3 receipts, 9/9 each. Scope: "Synthetic keyboard events through Godot Input, not human playtesting".

**Starter measurements** (BUILD-REPORT.md:23, :25, :27; S/evidence/build-manifest.json)
- Jump rise: 56.07 logical px.
- Largest retry interval: 34 ticks, about 0.567 s.
- Known route: 325 ticks, about 5.42 s, with zero deaths and five jumps.
- "machine_checks_passed": 34, "human_playtest_sessions": 0, and 17 source hashes.

**Design checks** (DESIGN-REVIEW.md:8–10)
- 12 feature IDs, 8 of them CORE, giving the "66.7% scope warning".
- 22 acceptance cases, "none is marked as executed or passing".
- 22 tickets plus 4 deferred.

**Clawd checks**
- 25/0 mechanics and 9/0 keyboard (CLAWD-STATUS.json:9–10).
- 162 animation samples, 1,944 scalar comparisons, 6 presentation cases (:11). The receipt evidence/clawd/animation-1789103540.86128.json:2–4 shows "checks": 1950 and "failures": 0, which is 1,944 + 6.
- 18 animations, 6 of them used in gameplay (C/design/GAME-BRIEF.md:11).
- The code change against the baseline is 14 files, +3,480/−11 (git diff --stat 9387542 HEAD -- godot). Of that, 3,246 lines are the tests/clawd-reference.json fixture.

**Capture takes** (walkthrough capture/ folder)
- Normal gameplay takes, all PASS, each with "no_skipped_physics_ticks": true: controls 189 frames, jump 191, spike 164, fall 205, pause 276, coyote 207, buffer 156, finish 302, mouse 152, plus a pilot of 107.
- Diagnostic takes: gallery-one 540 (superseded), gallery-two 343 (rejected), gallery-three 540 (superseded), the three v2 takes at 600 each, inspector 540 (superseded), inspector-v2 416 with no receipt (rejected), inspector-v3 600.

**Films**
- Walkthrough: 376.133 s (6:16). Gamedev: 461.467 s (7:41). Both 3840×2160 at 30 fps (FRICTIONAL.md:64–65).
- 68 + 79 contact pages (:83).
- Walkthrough QC (QC.md:8–11): 857 sampled frames, 807 of them pixel-distinct; 21 beat-to-master audio comparisons; 128 SRT cues.
- Published at 2026-09-11T06:00:50Z (0yXF1BMiokc) and 06:00:51Z (azoGEpdrcqo), playlist PLMhsxBEsgHFU positions 2 and 3, with "continuous_4k_playback_test": false (youtube/*/evidence/publication.json).

**Timeline** (git log, local time)
- Starter commit 9387542: 2026-09-10 18:39.
- Clawd feat commit f1cc442: 2026-09-11 01:25.
- Films and evidence commit 382f2ba: 2026-09-11 02:04.
- Zelda design package ce011ca: 2026-09-27.

## (4) What a human decided or found, and what is PENDING

**Human decisions on record.** All are quoted or paraphrased by the AI. None is written by Bear.
- S/BUILD-REPORT.md:3: "Built September 10, 2026 under Bear's request: **“Build a simple level for walker-jumpman.”**" Also S/DESIGN-STATUS.json:45.
- S/DESIGN-STATUS.json:78: "Bear requested: build all the design work."
- S/DESIGN-STATUS.json:24–26: "confirmed_by": "Bear" … "Explicit user instruction: all project names should start with walker, e.g. walker-jumpman."
- C/FRICTIONAL.md:9–11, quoted in (1). Also C/SOURCES.md:16: "Bear supplied purpose, character choice, project name, future game idea, iteration discipline, and destination."
- C/SOURCES.md:13–14: "Bear supplied the comment about rapid first output and continued iteration."
- C/FRICTIONAL.md:79–81: "Bear subsequently requested both 4K films be published … That authorizes publication; it does not invent a human playtest or a claim that Bear watched and approved every frame."
- C/design/GAME-BRIEF.md:5: "Concept as given by Bear, 2026-09-18: Clawd, a coding agent, goes through an agentic loop on every level". This is a 2026-09-18 silent Zelda draft.

**Human findings on record: none.** No file records a human playtest, a human play-feel judgment, or a human approval of a film or a design gate.

**Still PENDING:**
- C/CLAWD-STATUS.json:12: "human_playtest": "pending". At :16: "assignment_1_complete": false.
- C/CHANGE-BRIEF.md:37: "Bear plays and chooses one improvement or test."
- C/FRICTIONAL.md:72–74: "Human play-feel judgments, film approval and the next design decision remain pending."
- C/README.md:50: "This character pass is not a completed assignment or a human playtest."
- S/DESIGN-STATUS.json:38–41: gate_approvals vision, systems, world and scope are all null. At :57: "human_sessions": 0. Every feature is "approved": false.
- C/design/DESIGN-STATUS.json:10–13: all four gates have "signed_by": null. At :19: "Silent draft. Nothing here is approved. Gates are signed by humans only."
- C/design/decisions.md:7–14: Q-01 to Q-08 all have Owner "Bear" and Status "Open". For example, Q-01: "Does malware undoing a completed task read as a setback or a punishment?"
- S/PLAYTEST-PLAN.md:22: "CASE-020–021 are human sessions, never filled by simulated agents."
- Walkthrough QC.md:8: "not human listening approval or a true-peak certification."

## (5) Ten quotable lines (each under 25 words)

1. "Exit code zero did not establish success." (C/FRICTIONAL.md:49)
2. "The early receipt's PASS is insufficient; the take is rejected for the film and retained." (C/FRICTIONAL.md:41–42)
3. "A failed attempt can be progress; it is not evidence that the feature works." (C/README.md:46–47)
4. "Machine checks cannot decide whether the new silhouette feels fair or whether the game is fun." (C/CHANGE-BRIEF.md:32–33)
5. "AI checks mechanics; you judge the game." (S/BUILD-REPORT.md:35)
6. "Never invent human playtests, multiple days of work, approvals or test passes." (C/AGENTS.md:13)
7. "This establishes sampled parity, not that every possible frame is right." (C/FRICTIONAL.md:29)
8. "The jump tuning and acceptance tolerances were not weakened." (S/BUILD-REPORT.md:19)
9. "Never “fix” a failed test by silently lowering its threshold." (S/PLAYTEST-PLAN.md:77)
10. "A syntactically complete GDD is not an approved or implemented game." (S/DESIGN-REVIEW.md:24)

Alternates:
- "Human: intent, scope, art judgment, play-feel review, and the next decision." (C/CHANGE-BRIEF.md:43)
- "Do not invent a failure just to fill this log." (C/FRICTIONAL.md:101)

## What is tracked in git, and so public

Public visibility on GitHub was not confirmed (no network). What could be checked locally:

**C (walker-jumpman-clawd)**
- Origin is github.com/nikbearbrown/walker-jumpman-clawd, main is level with origin/main, and the worktree is clean. 374 files are tracked.
- Tracked: README.md, AGENTS.md, CHANGE-BRIEF.md, GAME-BRIEF.md, FRICTIONAL.md, BUILD-REPORT.md, DESIGN-REVIEW.md, PLAYTEST-PLAN.md, CLAWD-STATUS.json and SOURCES.md.
- All 16 files in evidence/ are tracked: build-manifest, clawd/ (3), keyboard (3), mechanics (5, including the failed run) and screens (4).
- 75 walkthrough capture/ records are tracked, including the rejected gallery-two-receipt.json and inspector-v2-process.json.
- Not tracked (gitignored): MP4s, frames, _qc/, audio and mp3.

**S (walker-jumpman starter)**
- Origin is github.com/nikbearbrown/walker-jumpman and main is level with origin/main. 43 files are tracked.
- Tracked: README, GAME-BRIEF, GDD, BUILD-REPORT, DESIGN-REVIEW, PLAYTEST-PLAN, DESIGN-STATUS, ASSET-PLAN, LEVEL-DESIGN and PRODUCTION-PLAN.
- Also tracked: evidence/ (4 mechanics including the failed run, 2 keyboard, build-manifest, 4 screens) and design/ (3 files).
- youtube/ is untracked.
- S has no AGENTS.md, CHANGE-BRIEF, FRICTIONAL or CLAWD-STATUS; those files do not exist there.
- The parent walker repo ignores /games/ (walker/.gitignore:2).

**walker**
- publish.sh, prompts/runtime.md and four other files are modified but uncommitted. gdd/ is untracked.
