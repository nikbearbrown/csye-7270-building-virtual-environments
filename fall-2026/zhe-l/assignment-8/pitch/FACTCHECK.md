# Fact check — walker-survival-shooting pitch

Status: checked by Claude Code (Claude Opus 5.5) on 2026-11-26; claims about the author's own play and opinions come from the author (2026-11-25). Author sign-off on the finished film: pending.

Every spoken or on-screen claim, with where it can be checked. Verdict PASS = Claude checked the claim against the source on 2026-11-26 and the narration says no more than the source does; opinions and the author's own play are passed only as what they are (said as the author's view). "Commit" means the course repository, folder `fall-2026/zhe-l/assignment-8/`. Tense: past or present only for things that exist at commit f13431bf; "will" for the rest.

| Beat | Claim | Kind | Verdict | Source |
|---|---|---|---|---|
| B00 | The author is Zhe Liu; the game is walker-survival-shooting; the player carries a military tablet in a subway | exists | PASS | `pitch/README.md`; the tablet and the subway base in `walker-survival-shooting/godot/` (f13431bf); capture `tablet-scripted.mp4` |
| B01 | The world does not stop while the tablet is open | exists | PASS | the game has no pause; the tablet raise and the OS run while the scene keeps updating (`humanoid.gd`, `player_controller.gd`, f13431bf) |
| B01 | Players use apps, above all a memo app, to sort out clues and work out quests | design (will) | PASS | `pitch/PROJECT-BRIEF.md` §1–2 |
| B02 | A playable Windows desktop slice with one room, made in Godot 4.7.2 with Forward Plus | will (no build exists) | PASS | `pitch/PROJECT-BRIEF.md` stack line; `project.godot` (Forward+, D3D12) |
| B03 | Shooting and extraction already have many examples | opinion, not a market figure | PASS | the author's statement (PROJECT-BRIEF §2); no numbers claimed |
| B04 | Escape from Tarkov quests name the map, the kill count, the item to bring back | the author's own play | PASS | author played Tarkov (confirmed 2026-11-25) |
| B04 | Many games tick off each step and tell you the next | the author's general observation | PASS | author's words, 2026-11-25 |
| B05 | Final-goal quests, faction testimonies in memos, copying and comparing | design, said aloud "This is a design. It is not built yet." | PASS | `pitch/PROJECT-BRIEF.md` §2; design notes |
| B06 | Played each of Metal Gear Solid V: The Phantom Pain, Subnautica, Abiotic Factor for more than 100 hours | the author's statement | PASS | author, 2026-11-25 (Phantom Pain about 320 h) |
| B06 | Phantom Pain's computer is like an escape menu inside a computer; Subnautica's PDA combines backpack, logs, settings; Abiotic Factor's mail, compendium, recipes are mostly status displays; they rarely make apps that act on the world | the author's own observation from play | PASS | author, 2026-11-25; words kept to what the author said ("escape menu", "rarely") |
| B07 | Windows, a taskbar, minimize, show desktop; This PC opens folders and goes back up | exists | PASS | capture `tablet-scripted.mp4` frames 165–470; engine log `logs/capture-tablet.log` |
| B08 | ThoughtPad runs on its own in its debug scene, shows a read-only document, can be typed in; not in the tablet system yet | exists | PASS | captures `mome1/mome2-scripted.mp4`; logs show the read-only text unchanged and the typed words added |
| B09 | Keys in the README; no on-screen hints | exists | PASS | `pitch/README.md` Keys section (document frame) |
| B10 | One state machine runs raise / put away / one to two hands; the screen lights only in place, stays dark if interrupted | exists | PASS | capture `b10-scripted.mp4`, log: lit on frame 54, interrupted raise never lit; `humanoid.gd` AnimationTree |
| B11 | The screen glow shader was written by the author by hand | exists | PASS | `shaders/pad_base_light.gdshader`; tag `zhe-l-a5` commit history (shader committed alone, no co-author) |
| B11 | Landing dust is a particle effect; its cost on the author's laptop GPU is almost nothing (+0.001 ms GPU) | measured earlier | PASS | tag `zhe-l-a6` README: NVIDIA GeForce RTX 5070 Ti Laptop GPU, Effect A +0.001 ms |
| B12 | Screen glow and effects have automated tests that rerun headless; the author breaks code on purpose (mutation runs); tablet system and memo have no tests yet | exists / true | PASS | fresh run in the f13431bf copy: 55 / 29 / 157 / 27 / 110 / 41 PASS, exit 0 (`logs/b12-*.txt`); mutation logs in tags `zhe-l-a5`, `zhe-l-a6`, `zhe-l-a7`; no tests for `computer_system/` at f13431bf |
| B13 | Two hands: cannot walk, keys go to the tablet; one hand: keys only control the character | exists | PASS | capture log: W held 45 frames with two hands moved 0.000 m; one hand 5.698 m; `player_controller.gd` `_input` / `_read_intent` |
| B14 | No shooting, extraction or looting for now; they will come later; the first piece is the smallest clue loop; real play labelled with its version will show it runs | plan | PASS | `pitch/PROJECT-BRIEF.md` §6 |
| B15 | Risk: too big for one person; core idea first; code easy to fix and extend; a friend makes the art on commission | plan / exists (commissioned model) | PASS | PROJECT-BRIEF §7; `assets/characters/main_character/ATTRIBUTION.md` |
| B16 | Mostly to learn; engine, shaders, particles, animation, Blender new; earlier programming helped little; wants to show gameplay | the author's statement | PASS | PROJECT-BRIEF §8 |
| B17 | The next world-changing step (USB into the base computer, or a lock minigame) is not decided | plan | PASS | PROJECT-BRIEF "will exist" list |
